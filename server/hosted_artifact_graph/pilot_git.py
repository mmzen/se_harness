"""Bounded, disposable ordinary Git history for test-copy lifecycle records."""
from __future__ import annotations

import base64
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

from .canonical import canonical_json, named_digest
from .protocol import MAX_RESPONSE, Refusal, require

SNAPSHOT = "se-harness-test-snapshot/v2"
AUTHORITY = "rehearsal-only; Git remains authoritative"


def safe_path(value):
    require(isinstance(value, str) and value and not value.startswith("/")
            and "\\" not in value and ":" not in value and not any(ord(c) < 32 or ord(c) == 127 for c in value)
            and all(p.casefold() not in ("", ".", "..", ".git") and p.rstrip(" .") == p
                    and p.split(".", 1)[0].upper() not in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}
                    for p in value.split("/")),
            422, "UNEXPECTED_OUTPUT", "Unsafe test projection path.")
    return value


def encoded(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "content_base64": base64.b64encode(raw).decode("ascii")}


def decoded(value):
    try:
        raw = base64.b64decode(value["content_base64"], validate=True)
        require(encoded(raw) == {k: value[k] for k in ("bytes", "sha256", "content_base64")},
                422, "BINDING_UNAVAILABLE", "Stored test bytes differ from their digest.")
        return raw
    except (ValueError, TypeError, KeyError) as exc:
        raise Refusal(422, "BINDING_UNAVAILABLE", "Invalid stored test bytes.") from exc


def scan(root):
    files = {}
    for folder, directories, names in os.walk(root, followlinks=False):
        if Path(folder) == root:
            directories[:] = [d for d in directories if d != ".git"]
        for name in [*directories, *names]:
            path = Path(folder) / name
            require(not path.is_symlink(), 422, "UNEXPECTED_OUTPUT", "Projection links are forbidden.")
        for name in names:
            path = Path(folder) / name
            relative = safe_path(path.relative_to(root).as_posix())
            require(path.is_file(), 422, "UNEXPECTED_OUTPUT", "Projection contains a nonregular file.")
            files[relative] = path.read_bytes()
    require(len(files) <= 10000 and sum(map(len, files.values())) <= MAX_RESPONSE,
            429, "RESOURCE_LIMIT", "Test projection exceeds 10,000 files or 2 MiB.")
    require(len({p.casefold() for p in files}) == len(files), 422,
            "UNEXPECTED_OUTPUT", "Case-ambiguous projection paths.")
    return files


def git(root, *args, binary=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "PYTHON"))}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               GIT_TERMINAL_PROMPT="0", GIT_AUTHOR_DATE="2000-01-01T00:00:00Z",
               GIT_COMMITTER_DATE="2000-01-01T00:00:00Z")
    argv = ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "core.autocrlf=false",
            "-c", "commit.gpgsign=false", "-c", "user.name=Rehearsal Test",
            "-c", "user.email=rehearsal@example.invalid", *map(str, args)]
    try:
        result = subprocess.run(argv, cwd=root, env=env, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Refusal(422, "BINDING_UNAVAILABLE", "Disposable Git operation failed or timed out.") from exc
    require(result.returncode == 0 and len(result.stdout) <= 8 * MAX_RESPONSE, 422,
            "BINDING_UNAVAILABLE", "Disposable Git history is unavailable or exceeds its bound.",
            evaluator_output={"git_exit": result.returncode, "stderr": result.stderr.decode("utf-8", "replace")[:4096]})
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def commit(root, message):
    scan(root)
    git(root, "add", "--all")
    if git(root, "status", "--porcelain"):
        git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD")


def verify_snapshot(value):
    require(value.get("schema") == SNAPSHOT and value.get("test_copy") is True,
            422, "BINDING_UNAVAILABLE", "Missing test snapshot identity.")
    body = {k: v for k, v in value.items() if k != "snapshot_id"}
    require(value.get("snapshot_id") == "sha256:" + named_digest(SNAPSHOT, body),
            422, "BINDING_UNAVAILABLE", "Test snapshot digest differs.")
    require(len(canonical_json(value)) <= MAX_RESPONSE, 429, "RESOURCE_LIMIT", "Stored test snapshot exceeds 2 MiB.")
    for name, item in value["files"].items():
        safe_path(name)
        decoded(item)
    decoded(value["git_bundle"])
    return value


def restore(root, value):
    """Never accept uploaded bundles; restore only a guarded retained snapshot."""
    verify_snapshot(value)
    require(not (root / ".git").exists(), 422, "BINDING_UNAVAILABLE", "Projection already has Git state.")
    git(root, "init", "--quiet", "--template=", "-b", "rehearsal")
    with tempfile.TemporaryDirectory(prefix="harness-test-history-") as scratch:
        bundle = Path(scratch) / "history.bundle"
        bundle.write_bytes(decoded(value["git_bundle"]))
        git(root, "bundle", "verify", bundle)
        git(root, "fetch", "--quiet", bundle, "refs/heads/rehearsal")
        git(root, "update-ref", "refs/heads/rehearsal", "FETCH_HEAD")
    require(git(root, "rev-parse", "refs/heads/rehearsal") == value["head"],
            422, "BINDING_UNAVAILABLE", "Git bundle HEAD differs from snapshot.")
    # Read blobs directly: no checkout filters, executable files, hooks or links.
    rows = git(root, "ls-tree", "-rz", value["head"], binary=True).split(b"\0")
    observed = {}
    for row in rows:
        if not row:
            continue
        header, path = row.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split()
        require(mode in ("100644", "100755") and kind == "blob", 422,
                "BINDING_UNAVAILABLE", "Git test history contains a link or non-file entry.")
        name = safe_path(path.decode("utf-8"))
        observed[name] = git(root, "cat-file", "blob", oid, binary=True)
    expected = {p: decoded(v) for p, v in value["files"].items()}
    require(observed == expected, 422, "BINDING_UNAVAILABLE", "Snapshot files differ from retained Git HEAD.")
    # The caller's base projection is disposable. Its old regular files can be removed.
    for path in scan(root):
        (root / path).unlink()
    for path, raw in observed.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    git(root, "read-tree", value["head"])
    git(root, "fsck", "--full", "--no-reflogs")
    require(not git(root, "status", "--porcelain"), 422, "BINDING_UNAVAILABLE", "Restored test history is not clean.")


def initial(root):
    git(root, "init", "--quiet", "--template=", "-b", "rehearsal")
    return commit(root, "Initial disposable test projection")


def snapshot(root, *, source, evaluator, candidates):
    head = commit(root, "Retain complete rehearsal result")
    files = {p: encoded(raw) for p, raw in sorted(scan(root).items())}
    tracked = {p.decode("utf-8") for p in git(root, "ls-files", "-z", binary=True).split(b"\0") if p}
    require(tracked == set(files), 422, "BINDING_UNAVAILABLE", "Ignored or untracked test bytes cannot be omitted from history.")
    with tempfile.TemporaryDirectory(prefix="harness-test-export-") as scratch:
        bundle = Path(scratch) / "history.bundle"
        git(root, "bundle", "create", bundle, "refs/heads/rehearsal")
        bundle_bytes = bundle.read_bytes()
    value = {"schema": SNAPSHOT, "test_copy": True, "authority": AUTHORITY,
             "source": source, "head": head, "evaluator": evaluator, "candidates": candidates,
             "files": files, "git_bundle": encoded(bundle_bytes)}
    value["snapshot_id"] = "sha256:" + named_digest(SNAPSHOT, value)
    verify_snapshot(value)
    return value
