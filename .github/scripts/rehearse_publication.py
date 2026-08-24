#!/usr/bin/env python3
"""Rehearse the credential-free SE Harness publication path on any runner platform.

Repository-owned implementation of SPEC-RLO-004 under WO-RLO-004. This program
exercises the mechanics that ``.github/workflows/publish-pypi.yml`` performs before
any credential is used, on whichever platform it is invoked on, and checks that the
orchestrator has not drifted away from the rehearsed set.

It acquires no credential, contacts no index for writing, and creates no tag, ref,
release, deployment, or artifact lifecycle state. Every result it emits is derived
operational evidence and never formal repository authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import sysconfig
import tarfile
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

DECLARATION_SCHEMA = "se-harness-publication-rehearsal-mechanics/v1"
RESULT_SCHEMA = "se-harness-publication-rehearsal-result/v1"
DIVERGENCE_SCHEMA = "se-harness-publication-rehearsal-divergence/v1"
REFUSAL_SCHEMA = "se-harness-release-result/v1"
AUTHORITY = "derived operational evidence; no formal lifecycle transition"

RELEASE_RECORD_PATTERN = re.compile(r"RLS-[A-Z0-9-]+-[0-9]{3}")
WHEEL_NAME_PATTERN = re.compile(r"^se_harness-(?P<version>[0-9][^-]*)-py3-none-any\.whl$")
BUILD_PINS = ("build==1.3.0", "setuptools==84.0.0", "wheel==0.48.0")
#: The default-branch spelling a rehearsal resolves a plan against. The orchestrator
#: passes ``refs/heads/main`` because it checks out main; a rehearsal runs on a pull
#: request head, where the remote-tracking ref is the faithful equivalent and is also
#: ``publish_release.resolve_plan``'s own default.
DEFAULT_REF = "refs/remotes/origin/main"

#: Markers written into a candidate-mode plan so it can never be read as authority.
CANDIDATE_PLAN_MARKERS = {
    "release_record": "REHEARSAL-CANDIDATE-MODE-NOT-A-RELEASE-RECORD",
    "release_record_path": "",
    "tag": "rehearsal-candidate-mode",
    "released_at": "",
    "release_contract": "",
    "verification_records": [],
    "released_work": [],
    "evaluator_evidence_path": "",
    "evaluator_evidence_sha256": "",
}

#: Distribution-identity fields a candidate-mode plan takes from the first built set,
#: mapped from the bundle manifest's own field names.
CANDIDATE_PLAN_MEASURED = {
    "candidate_commit": "commit",
    "git_object_format": "git_object_format",
    "version": "version",
    "source_date_epoch": "source_date_epoch",
    "wheel": "wheel",
    "wheel_sha256": "wheel_sha256",
    "sdist": "sdist",
    "sdist_sha256": "sdist_sha256",
    "checksums": "checksums",
    "checksums_sha256": "checksums_sha256",
    "source_manifest_sha256": "source_manifest_sha256",
}

KNOWN_EXECUTABLES = frozenset(
    {
        "python",
        "python3",
        "python.exe",
        "python3.exe",
        "pip",
        "pip.exe",
        "harnessctl",
        "harnessctl.exe",
        "git",
        "curl",
        "tar",
        "jq",
        "cmp",
        "sha256sum",
        "cygpath",
    }
)

#: Shell words that introduce a compound command rather than name a program.
LEADING_KEYWORDS = frozenset({"if", "then", "elif", "else", "!", "time"})

PLACEHOLDER = "<placeholder>"


class RehearsalError(Exception):
    """A rehearsal or divergence condition that must fail closed."""


# ---------------------------------------------------------------------------
# platform and path primitives
# ---------------------------------------------------------------------------


def platform_family() -> str:
    """Name the runner platform family the way the declaration names it."""
    if os.name == "nt":
        return "Windows"
    if sys.platform.startswith("linux"):
        return "Linux"
    if sys.platform == "darwin":
        return "macOS"
    return f"posix-{sys.platform}"


def runner_platform_family(runs_on: Any) -> str:
    """Map a workflow ``runs-on`` label onto a platform family."""
    if not isinstance(runs_on, str):
        raise RehearsalError(f"runs-on must be a single label; found {runs_on!r}")
    label = runs_on.strip().lower()
    if label.startswith("ubuntu"):
        return "Linux"
    if label.startswith("windows"):
        return "Windows"
    if label.startswith("macos"):
        return "macOS"
    raise RehearsalError(f"runs-on label has no known platform family: {runs_on}")


def venv_scripts_directory(root: Path) -> Path:
    """Resolve a virtual environment's console-script directory from this platform.

    SPEC-RLO-004 rule 6: the ``bin`` and ``Scripts`` layouts are never hardcoded.
    """
    scheme = "nt_venv" if os.name == "nt" else "posix_venv"
    if scheme not in sysconfig.get_scheme_names():  # pragma: no cover - old interpreters
        scheme = sysconfig.get_default_scheme()
    base = str(root)
    raw = sysconfig.get_path(
        "scripts",
        scheme,
        vars={
            "base": base,
            "platbase": base,
            "installed_base": base,
            "installed_platbase": base,
        },
    )
    return Path(raw)


def venv_python(root: Path) -> Path:
    """Resolve a virtual environment's interpreter from this platform."""
    name = "python.exe" if os.name == "nt" else "python"
    return venv_scripts_directory(root) / name


def venv_entry_point(root: Path, name: str) -> Path:
    """Resolve a virtual environment's console entry point from this platform."""
    suffix = ".exe" if os.name == "nt" else ""
    return venv_scripts_directory(root) / f"{name}{suffix}"


def assert_venv_layout(root: Path) -> Path:
    """Fail naming the expected layout and platform when it is absent."""
    scripts = venv_scripts_directory(root)
    interpreter = venv_python(root)
    if not scripts.is_dir() or not interpreter.exists():
        raise RehearsalError(
            f"virtual-environment layout is absent on {platform_family()}: "
            f"expected {scripts.name}/{interpreter.name} under {root}"
        )
    return interpreter


def canonical_existing_directory(path: str | os.PathLike[str], *, label: str) -> Path:
    """Resolve aliases such as Windows 8.3 short names before anything is created.

    SPEC-RLO-004 rule 8.
    """
    try:
        resolved = Path(os.path.realpath(os.fspath(path), strict=True))
    except OSError as exc:
        raise RehearsalError(f"{label} cannot be canonicalized: {path}: {exc}") from exc
    if not resolved.is_dir():
        raise RehearsalError(f"{label} is not a directory: {resolved}")
    return resolved


def sha256_file(path: Path) -> str:
    """Digest a file with the standard library so both platforms agree."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_difference(left: Path, right: Path) -> int | None:
    """Return the first differing byte offset of two files, or ``None`` when equal."""
    offset = 0
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            chunk_a = a.read(1 << 20)
            chunk_b = b.read(1 << 20)
            if not chunk_a and not chunk_b:
                return None
            limit = min(len(chunk_a), len(chunk_b))
            for index in range(limit):
                if chunk_a[index] != chunk_b[index]:
                    return offset + index
            if len(chunk_a) != len(chunk_b):
                return offset + limit
            offset += limit


def assert_temporary_identity(expected: str, observed: str) -> None:
    """Refuse a temporary root a child process does not agree on.

    Incident I-16 of the ``0.6.0`` recovery: the runner spelled ``TEMP`` as a
    Windows 8.3 short alias, so a child observed a different string for the same
    directory. Both sides are already canonical here, so the comparison is exact
    up to the platform's case rule.
    """
    if os.path.normcase(observed) != os.path.normcase(expected):
        raise RehearsalError(
            "temporary-path identity divergence: the rehearsal set "
            f"{expected!r} and a child process reported {observed!r}"
        )


def derive_rehearsal_plan(
    base_plan: dict[str, Any], manifest: dict[str, Any], candidate_commit: str
) -> dict[str, Any]:
    """Derive a candidate-mode plan from a measured bundle manifest.

    SPEC-RLO-004 rule 12: candidate mode never reads release authority. The
    distribution identity comes from the manifest of the first built set, the
    authority fields are overwritten with markers that cannot be read as a
    release, and the field set stays exactly the orchestrator's own.
    """
    plan = dict(base_plan)
    for plan_key, manifest_key in CANDIDATE_PLAN_MEASURED.items():
        if manifest_key not in manifest:
            raise RehearsalError(f"bundle manifest has no {manifest_key}")
        plan[plan_key] = manifest[manifest_key]
    plan["governance_commit"] = candidate_commit
    plan.update(CANDIDATE_PLAN_MARKERS)
    if set(plan) != set(base_plan):
        raise RehearsalError("derived candidate plan field set is not canonical")
    return plan


def path_is_within(root_real: str, candidate: str | os.PathLike[str]) -> bool:
    """Report whether ``candidate`` resolves to ``root_real`` or to a path inside it.

    The comparison is component-wise, so a sibling sharing a textual prefix is
    outside, and a cross-drive path on Windows is outside rather than an error.
    """
    candidate_real = os.path.realpath(candidate)
    try:
        shared = os.path.commonpath([root_real, candidate_real])
    except ValueError:  # different drives on Windows
        return False
    return os.path.normcase(shared) == os.path.normcase(root_real)


def _path_is_junction(path: Path) -> bool:
    checker = getattr(os.path, "isjunction", None)
    if checker is None:  # pragma: no cover - interpreters before 3.12
        return False
    try:
        return bool(checker(path))
    except OSError:  # pragma: no cover - transient filesystem state
        return False


def _force_writable(path: Path) -> None:
    try:
        path.chmod(stat.S_IWRITE | stat.S_IREAD)
    except OSError:  # pragma: no cover - best effort before a retry
        pass


def _is_link(entry: os.DirEntry[str]) -> bool:
    if entry.is_symlink():
        return True
    junction = getattr(entry, "is_junction", None)
    if junction is None:  # pragma: no cover - interpreters before 3.12
        return False
    try:
        return bool(junction())
    except OSError:  # pragma: no cover - transient filesystem state
        return False


def remove_tree_without_following_links(root: Path, deleted: list[str]) -> None:
    """Delete a tree by unlinking links instead of recursing through their targets.

    SPEC-RLO-004 rules 19 and 21: a link planted inside a derived tree can never
    cause a deletion outside ``root``.
    """
    root_real = os.path.realpath(root)

    def guard(candidate: Path) -> None:
        # The parent is canonicalized, never the candidate itself: a link's own
        # target must not influence whether the link may be unlinked.
        if not path_is_within(root_real, candidate.parent):
            raise RehearsalError(
                f"teardown refused a path outside the rehearsal root: {candidate}"
            )

    def unlink(candidate: Path, *, directory: bool) -> None:
        try:
            os.rmdir(candidate) if directory else os.unlink(candidate)
        except PermissionError:
            _force_writable(candidate)
            os.rmdir(candidate) if directory else os.unlink(candidate)
        deleted.append(candidate.as_posix())

    def walk(directory: Path) -> None:
        with os.scandir(directory) as iterator:
            entries = list(iterator)
        for entry in entries:
            candidate = Path(entry.path)
            guard(candidate)
            if _is_link(entry):
                # A link is removed as a link. Its target is never touched.
                if entry.is_dir(follow_symlinks=False) or (
                    os.name == "nt" and os.path.isdir(candidate)
                ):
                    unlink(candidate, directory=True)
                else:
                    unlink(candidate, directory=False)
                continue
            if entry.is_dir(follow_symlinks=False):
                walk(candidate)
                unlink(candidate, directory=True)
                continue
            unlink(candidate, directory=False)

    if not root.exists():
        return
    if root.is_symlink() or _path_is_junction(root):
        # A linked root would make every containment test meaningless.
        raise RehearsalError(f"teardown refused a linked rehearsal root: {root}")
    walk(root)
    unlink(root, directory=True)


# ---------------------------------------------------------------------------
# declaration
# ---------------------------------------------------------------------------

RESERVED_DECLARATION_KEYS = frozenset(
    {"code", "eval", "exec", "import", "lambda", "run", "script", "shell"}
)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise RehearsalError(f"declaration repeats the key {key!r}")
        seen[key] = value
    return seen


def _assert_data_only(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise RehearsalError(f"declaration key at {path} is not a string")
            if key.startswith("__") or key in RESERVED_DECLARATION_KEYS:
                raise RehearsalError(f"declaration key at {path} is executable-shaped: {key}")
            _assert_data_only(item, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_data_only(item, f"{path}[{index}]")
        return
    if isinstance(value, (str, int, float, bool)) or value is None:
        return
    raise RehearsalError(f"declaration value at {path} is not data: {type(value).__name__}")


def load_declaration(path: Path) -> dict[str, Any]:
    """Read the mechanic declaration as data only (SPEC-RLO-004 rule 23)."""
    if path.suffix != ".json":
        raise RehearsalError(f"mechanic declaration must be JSON data: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RehearsalError(f"mechanic declaration is unreadable: {path}: {exc}") from exc
    try:
        value = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise RehearsalError(f"mechanic declaration is not strict JSON data: {exc}") from exc
    if not isinstance(value, dict):
        raise RehearsalError("mechanic declaration must be a mapping")
    _assert_data_only(value, "declaration")
    if value.get("schema") != DECLARATION_SCHEMA:
        raise RehearsalError(
            f"mechanic declaration schema must be {DECLARATION_SCHEMA}; found {value.get('schema')!r}"
        )
    for key in (
        "mechanics",
        "steps",
        "trivia_commands",
        "required_platforms",
        "realization_surfaces",
    ):
        if not isinstance(value.get(key), list):
            raise RehearsalError(f"mechanic declaration {key} must be an array")
    identifiers = [item.get("id") for item in value["mechanics"]]
    if len(identifiers) != len(set(identifiers)):
        raise RehearsalError("mechanic declaration repeats a mechanic identifier")
    # The surface that realizes a mechanic comes from a closed vocabulary, so a
    # mechanic can never claim coverage by naming something the rehearsal has not
    # got.
    surfaces = set(value["realization_surfaces"])
    for mechanic in value["mechanics"]:
        if mechanic.get("realized_by") not in surfaces:
            raise RehearsalError(
                f"mechanic {mechanic.get('id')!r} names an undeclared realization "
                f"surface: {mechanic.get('realized_by')!r}"
            )
    return value


def declaration_index(declaration: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in declaration["mechanics"]}


# ---------------------------------------------------------------------------
# rehearsal
# ---------------------------------------------------------------------------


@dataclass
class MechanicOutcome:
    mechanic: str
    outcome: str
    detail: str = ""
    reason: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    def as_json(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "mechanic": self.mechanic,
            "outcome": self.outcome,
            "detail": self.detail,
        }
        if self.outcome != "executed":
            value["reason"] = self.reason or "no reason recorded"
        if self.evidence:
            value["evidence"] = self.evidence
        return value


class Rehearsal:
    """Execute the credential-free publication mechanics on this platform."""

    def __init__(
        self,
        repository: Path,
        root: Path,
        *,
        mode: str,
        release_record: str | None,
        declaration: dict[str, Any],
        keep_root: bool = False,
        default_ref: str = DEFAULT_REF,
    ) -> None:
        if mode not in {"candidate", "release-record"}:
            raise RehearsalError(f"unknown rehearsal mode: {mode}")
        self.repository = canonical_existing_directory(repository, label="repository")
        self.root = canonical_existing_directory(root, label="rehearsal root")
        self.mode = mode
        self.declaration = declaration
        self.index = declaration_index(declaration)
        self.keep_root = keep_root
        self.default_ref = default_ref
        self.outcomes: list[MechanicOutcome] = []
        self.transcript: list[dict[str, Any]] = []
        self.deleted_paths: list[str] = []
        self.env = dict(os.environ)
        self.env["PYTHONNOUSERSITE"] = "1"
        self.temporary_root: Path | None = None
        self.candidate_commit = self._git("rev-parse", "HEAD").strip()
        self.source_date_epoch = self._git(
            "show", "-s", "--format=%ct", self.candidate_commit
        ).strip()
        self.git_status_before = self._git("status", "--porcelain")
        self.line_ending_conversion = (
            self._git_optional("config", "--get", "core.autocrlf").strip() or "unset"
        )
        self.release_record = release_record
        self.subject_record = release_record or self._default_released_record()
        self.evaluator: dict[str, Any] = {}
        self.evaluator_env = self.root / "evaluator-env"
        self.build_env = self.root / "build-env"
        self.candidate_checkout = self.root / "candidate-checkout"
        self.plan_path: Path | None = None
        self.plan: dict[str, Any] = {}
        self.plan_source = ""
        self.distribution: dict[str, Any] = {}
        self.failed = False

    # -- process helpers ---------------------------------------------------

    def _git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repository), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if completed.returncode != 0:
            raise RehearsalError(
                f"git {' '.join(arguments)} failed: {completed.stderr.strip()[:400]}"
            )
        return completed.stdout

    def _git_optional(self, *arguments: str) -> str:
        """Read a Git value that may legitimately be absent."""
        completed = subprocess.run(
            ["git", "-C", str(self.repository), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout if completed.returncode == 0 else ""

    def _run(
        self,
        argv: Sequence[str | os.PathLike[str]],
        *,
        cwd: Path | None = None,
        extra_env: dict[str, str] | None = None,
        check: bool = True,
        label: str = "",
    ) -> subprocess.CompletedProcess[str]:
        command = [str(item) for item in argv]
        environment = dict(self.env)
        if extra_env:
            environment.update(extra_env)
        completed = subprocess.run(
            command,
            cwd=str(cwd or self.repository),
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.transcript.append(
            {
                "mechanic": label,
                "command": " ".join(shlex.quote(item) for item in command),
                "cwd": (cwd or self.repository).as_posix(),
                "exit": completed.returncode,
                "stdout_tail": completed.stdout.strip()[-600:],
                "stderr_tail": completed.stderr.strip()[-600:],
            }
        )
        if check and completed.returncode != 0:
            raise RehearsalError(
                f"{command[0]} exited {completed.returncode}: "
                f"{(completed.stderr or completed.stdout).strip()[-600:]}"
            )
        return completed

    def _default_released_record(self) -> str:
        """Name the released record the governing evaluator version corresponds to.

        Candidate mode reads committed data to give the resolution mechanics a real
        subject. It exercises no decision right over that record.
        """
        import tomllib

        configuration = tomllib.loads(
            (self.repository / ".engineering-harness.toml").read_text(encoding="utf-8")
        )
        version = configuration.get("harness", {}).get("tool_version")
        candidates: list[str] = []
        for path in sorted((self.repository / "docs" / "engineering").rglob("RLS-*.md")):
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\+\+\+\n(.*?)\n\+\+\+", text, re.S)
            if match is None:
                continue
            metadata = tomllib.loads(match.group(1))
            if metadata.get("status") == "released" and metadata.get("version") == version:
                identifier = metadata.get("id")
                if isinstance(identifier, str):
                    candidates.append(identifier)
        if not candidates:
            raise RehearsalError(
                f"no released record declares the governing version {version!r}"
            )
        return sorted(candidates)[-1]

    # -- mechanic driver ---------------------------------------------------

    def _record(self, mechanic: str, body: Callable[[], tuple[str, dict[str, Any]]]) -> bool:
        if mechanic not in self.index:
            raise RehearsalError(f"mechanic is not declared: {mechanic}")
        try:
            detail, evidence = body()
        except (RehearsalError, OSError, subprocess.SubprocessError) as exc:
            self.failed = True
            self.outcomes.append(
                MechanicOutcome(
                    mechanic=mechanic,
                    outcome="failed",
                    detail=f"{platform_family()}: {type(exc).__name__}",
                    reason=str(exc)[:1200],
                )
            )
            return False
        self.outcomes.append(
            MechanicOutcome(
                mechanic=mechanic, outcome="executed", detail=detail, evidence=evidence
            )
        )
        return True

    def _blocked(self, mechanic: str, prerequisite: str) -> None:
        self.failed = True
        self.outcomes.append(
            MechanicOutcome(
                mechanic=mechanic,
                outcome="failed",
                detail=f"{platform_family()}: not attempted",
                reason=f"prerequisite mechanic {prerequisite} did not complete",
            )
        )

    # -- mechanics ---------------------------------------------------------

    def _temporary_path_identity(self) -> tuple[str, dict[str, Any]]:
        raw = self.root / "temp"
        raw.mkdir(exist_ok=True)
        canonical = canonical_existing_directory(raw, label="rehearsal temporary root")
        self.temporary_root = canonical
        spelling = str(canonical)
        for name in ("TMPDIR", "TEMP", "TMP"):
            self.env[name] = spelling
        probe = self._run(
            [
                sys.executable,
                "-c",
                "import os, tempfile; print(os.path.realpath(tempfile.gettempdir()))",
            ],
            label="temporary-path-identity",
        )
        observed = probe.stdout.strip()
        assert_temporary_identity(spelling, observed)
        return (
            f"child processes observe {spelling}",
            {"set": spelling, "observed_by_child": observed, "variables": ["TMPDIR", "TEMP", "TMP"]},
        )

    def _release_record_format_validation(self) -> tuple[str, dict[str, Any]]:
        rejected = [
            "rls-seh-012",
            "RLS-SEH-12",
            "RLS-SEH-0123",
            "RLS-SEH-012 ",
            "RLS_SEH_012",
            "",
        ]
        for sample in rejected:
            if RELEASE_RECORD_PATTERN.fullmatch(sample) is not None:
                raise RehearsalError(
                    f"release-record validation accepted a non-canonical identifier: {sample!r}"
                )
        if RELEASE_RECORD_PATTERN.fullmatch(self.subject_record) is None:
            raise RehearsalError(
                f"release_record must be a canonical RLS identifier: {self.subject_record!r}"
            )
        return (
            f"accepted {self.subject_record} and refused {len(rejected)} non-canonical forms",
            {"accepted": self.subject_record, "refused": rejected},
        )

    def _evaluator_resolution(self) -> tuple[str, dict[str, Any]]:
        output = self.root / "evaluator.json"
        argv: list[str | os.PathLike[str]] = [
            sys.executable,
            self.repository / ".github" / "scripts" / "publish_dashboard.py",
            "evaluator",
            "--repository",
            self.repository,
            "--output",
            output,
        ]
        if self.mode == "release-record":
            argv += ["--release-record", self.subject_record]
        self._run(argv, label="evaluator-resolution")
        self.evaluator = json.loads(output.read_text(encoding="utf-8"))
        for key in ("version", "wheel", "url", "sha256", "payload_sha256"):
            if not isinstance(self.evaluator.get(key), str) or not self.evaluator[key]:
                raise RehearsalError(f"resolved evaluator descriptor has no {key}")
        return (
            f"released evaluator {self.evaluator['version']}",
            {
                "version": self.evaluator["version"],
                "wheel": self.evaluator["wheel"],
                "wheel_sha256": self.evaluator["sha256"],
            },
        )

    def _evaluator_acquisition_and_hash_proof(self) -> tuple[str, dict[str, Any]]:
        self._run(
            [sys.executable, "-m", "venv", self.evaluator_env],
            label="evaluator-acquisition-and-hash-proof",
        )
        interpreter = assert_venv_layout(self.evaluator_env)
        url = self.evaluator["url"]
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https":
            raise RehearsalError(f"evaluator wheel URL is not https: {url}")
        wheel = self.root / self.evaluator["wheel"]
        request = urllib.request.Request(url, headers={"Accept": "application/octet-stream"})
        with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310 - https asserted
            payload = response.read()
        wheel.write_bytes(payload)
        observed = hashlib.sha256(payload).hexdigest()
        if observed != self.evaluator["sha256"]:
            raise RehearsalError(
                "evaluator wheel digest differs before installation: "
                f"expected {self.evaluator['sha256']}, read {observed}"
            )
        self._run(
            [
                interpreter,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-deps",
                wheel,
            ],
            label="evaluator-acquisition-and-hash-proof",
        )
        return (
            f"proved and installed {wheel.name} through the "
            f"{venv_scripts_directory(self.evaluator_env).name} layout",
            {
                "wheel": wheel.name,
                "bytes": len(payload),
                "sha256": observed,
                "layout": venv_scripts_directory(self.evaluator_env).name,
            },
        )

    def _evaluator_identity_proof(self) -> tuple[str, dict[str, Any]]:
        interpreter = assert_venv_layout(self.evaluator_env)
        entry_point = venv_entry_point(self.evaluator_env, "harnessctl")
        if not entry_point.exists():
            raise RehearsalError(
                f"evaluator console entry point is absent on {platform_family()}: {entry_point}"
            )
        isolated = {"PYTHONNOUSERSITE": "1", "PYTHONPATH": ""}
        arguments: list[str | os.PathLike[str]] = [
            "--role",
            "released-evaluator",
            "--expected-version",
            self.evaluator["version"],
            "--expected-root",
            self.evaluator_env,
            "--checkout-root",
            self.repository,
            "--evaluator-wheel-sha256",
            self.evaluator["sha256"],
            "--entry-point",
            entry_point,
            "--require-isolated-python",
            "--require-entry-point",
        ]
        probe = self._run(
            [interpreter, "-I", "-m", "se_harness", "identity", "--help"],
            cwd=self.root,
            extra_env=isolated,
            check=False,
            label="evaluator-identity-proof",
        )
        payload_supported = "--evaluator-payload-sha256" in (probe.stdout + probe.stderr)
        if payload_supported:
            arguments += ["--evaluator-payload-sha256", self.evaluator["payload_sha256"]]
        self._run(
            [interpreter, "-I", "-m", "se_harness", "identity", *arguments],
            cwd=self.root,
            extra_env=isolated,
            label="evaluator-identity-proof",
        )
        return (
            f"released-evaluator identity proved with the {entry_point.name} entry point",
            {
                "entry_point": entry_point.name,
                "payload_digest_asserted": payload_supported,
                "expected_version": self.evaluator["version"],
            },
        )

    def _declared_predecessor_evaluator(self, identifier: str) -> dict[str, Any] | None:
        """Read the evaluator identity a committed release record binds as its predecessor.

        Data only: the record's frontmatter names an evidence path, and that evidence
        declares the evaluator that qualified the record. Nothing here decides anything
        about the record.
        """
        import tomllib

        for path in sorted((self.repository / "docs" / "engineering").rglob("RLS-*.md")):
            text = path.read_text(encoding="utf-8")
            match = re.match(r"\+\+\+\n(.*?)\n\+\+\+", text, re.S)
            if match is None:
                continue
            metadata = tomllib.loads(match.group(1))
            if metadata.get("id") != identifier:
                continue
            evidence_path = metadata.get("evaluator_evidence_path")
            if not isinstance(evidence_path, str) or not evidence_path:
                return None
            target = self.repository / evidence_path
            if not target.is_file():
                return None
            evaluator = json.loads(target.read_text(encoding="utf-8")).get("evaluator")
            return evaluator if isinstance(evaluator, dict) else None
        return None

    def _predecessor_view_exclusion(self) -> tuple[str, dict[str, Any]] | None:
        """State why the subject record cannot host a predecessor-view qualification.

        The orchestrator resolves the evaluator from the schema-3 lock and then asks the
        subject record's bootstrap contract to name that same evaluator. A record under
        preparation does, because the governing evaluator is the one that qualified it.
        A record already released names the evaluator that governed its own preparation,
        one version behind the lock that the release then advanced. Candidate mode has no
        prepared record, so the mismatch is reported with both measured identities instead
        of surfacing as a `PV001` failure that would read as a defect in publication.

        `release-record` mode never excludes: there a mismatch is a real defect in the
        record under preparation and must fail.
        """
        if self.mode == "release-record":
            return None
        resolved = self.evaluator.get("sha256")
        resolved_version = self.evaluator.get("version")
        declared = self._declared_predecessor_evaluator(self.subject_record)
        if declared is not None and declared.get("archive_sha256") == resolved:
            return None
        evidence = {
            "release_record": self.subject_record,
            "resolved_evaluator_version": resolved_version,
            "resolved_evaluator_sha256": resolved,
            "record_predecessor_evaluator_version": (
                declared.get("version") if declared else None
            ),
            "record_predecessor_evaluator_sha256": (
                declared.get("archive_sha256") if declared else None
            ),
        }
        if declared is None:
            reason = (
                f"{self.subject_record} binds no predecessor evaluator contract, so the "
                f"resolved evaluator {resolved_version} has no committed subject to be "
                "qualified against; only release-record mode against a record under "
                "preparation exercises this mechanic"
            )
        else:
            reason = (
                f"the resolved evaluator {resolved_version} is not the predecessor "
                f"evaluator {declared.get('version')} that {self.subject_record} binds, "
                "because a released record names the evaluator that qualified it while "
                "the lock names the evaluator that release advanced to; only "
                "release-record mode against a record under preparation exercises this "
                "mechanic"
            )
        return reason, evidence

    def _predecessor_view_qualification(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.evaluator_env)
        output = self.root / "predecessor-view-qualification.json"
        self._run(
            [
                sys.executable,
                "-m",
                "se_harness",
                "qualify",
                "predecessor-view",
                self.repository,
                "--release-record",
                self.subject_record,
                "--evaluator-python",
                interpreter,
                "--output",
                output,
                "--json",
            ],
            label="predecessor-view-qualification",
        )
        return (
            f"predecessor view of {self.subject_record} qualified",
            {"release_record": self.subject_record, "result": output.name},
        )

    def _distribution_policy_validation(self) -> tuple[str, dict[str, Any]]:
        self._run(
            [
                sys.executable,
                self.repository / "scripts" / "validate_release_distributions.py",
                "--root",
                self.repository,
                "--require-record",
                self.subject_record,
            ],
            label="distribution-policy-validation",
        )
        return (
            f"distribution policy requires {self.subject_record}",
            {"release_record": self.subject_record},
        )

    def _plan_resolution(self) -> tuple[str, dict[str, Any]]:
        resolved = self.root / "resolved-release-plan.json"
        self._run(
            [
                sys.executable,
                self.repository / ".github" / "scripts" / "publish_release.py",
                "resolve",
                "--repository",
                self.repository,
                "--default-ref",
                self.default_ref,
                "--release-record",
                self.subject_record,
                "--output",
                resolved,
            ],
            label="plan-resolution",
        )
        value = json.loads(resolved.read_text(encoding="utf-8"))
        if self.mode == "release-record":
            self.plan_path = resolved
            self.plan = value
            self.plan_source = "orchestrator-resolution-of-an-authorized-release-record"
        else:
            self.plan = value
            self.plan_source = "pending-derivation-from-the-first-distribution-set"
        return (
            f"canonical plan resolved for {self.subject_record}",
            {
                "release_record": self.subject_record,
                "candidate_commit": value.get("candidate_commit"),
                "version": value.get("version"),
                "used_for_verification": self.mode == "release-record",
            },
        )

    def _resolution_refusal_document(self) -> tuple[str, dict[str, Any]]:
        path = self.root / "release-refusal.json"
        document = {
            "schema": REFUSAL_SCHEMA,
            "authority": "derived operational evidence; no formal lifecycle transition",
            "release": {"release_record": self.subject_record},
            "stages": {
                "resolution": {"state": "failed"},
                "qualification": {"state": "not_run"},
                "github": {"state": "not_run"},
                "pypi": {"state": "not_run"},
                "pages": {"state": "not_run"},
                "public_install": {"state": "not_run"},
            },
        }
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        reread = json.loads(path.read_text(encoding="utf-8"))
        expected_stages = {
            "resolution",
            "qualification",
            "github",
            "pypi",
            "pages",
            "public_install",
        }
        if set(reread) != {"schema", "authority", "release", "stages"}:
            raise RehearsalError("refusal document field set is not canonical")
        if set(reread["stages"]) != expected_stages:
            raise RehearsalError("refusal document stage set is not canonical")
        return (
            "bounded refusal document written and re-read canonically",
            {"path": path.name, "stages": sorted(expected_stages)},
        )

    def _candidate_export(self) -> tuple[str, dict[str, Any]]:
        self._run(
            [
                "git",
                "-C",
                self.repository,
                "worktree",
                "add",
                "--detach",
                self.candidate_checkout,
                self.candidate_commit,
            ],
            label="candidate-export",
        )
        trees: dict[str, int] = {}
        for suffix in ("a", "b"):
            archive = self.root / f"source-{suffix}.tar"
            target = self.root / f"source-{suffix}"
            target.mkdir()
            self._run(
                [
                    "git",
                    "-C",
                    self.repository,
                    "archive",
                    "--format=tar",
                    "--output",
                    archive,
                    self.candidate_commit,
                ],
                label="candidate-export",
            )
            with tarfile.open(archive, "r:") as bundle:
                bundle.extractall(target, filter="data")
            archive.unlink()
            if not (target / "pyproject.toml").is_file():
                raise RehearsalError(f"exported tree {target.name} has no pyproject.toml")
            trees[target.name] = sum(1 for _ in target.rglob("*") if _.is_file())
        return (
            f"candidate {self.candidate_commit[:12]} exported twice from the repository archive",
            {"candidate_commit": self.candidate_commit, "files": trees},
        )

    def _pinned_build_tool_installation(self) -> tuple[str, dict[str, Any]]:
        self._run(
            [sys.executable, "-m", "venv", self.build_env],
            label="pinned-build-tool-installation",
        )
        interpreter = assert_venv_layout(self.build_env)
        self._run(
            [
                interpreter,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                *BUILD_PINS,
            ],
            label="pinned-build-tool-installation",
        )
        return (
            "pinned build tools installed into a rehearsal-root environment",
            {
                "pins": list(BUILD_PINS),
                "layout": venv_scripts_directory(self.build_env).name,
                "locality": (
                    "the orchestrator installs into its ephemeral runner interpreter; the "
                    "rehearsal installs into an environment under the rehearsal root so "
                    "nothing outside that root is modified"
                ),
            },
        )

    def _complete_candidate_qualification(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        output = self.root / "complete-candidate-qualification.json"
        self._run(
            [
                interpreter,
                "-m",
                "se_harness",
                "qualify",
                "complete-candidate",
                ".",
                "--candidate-commit",
                self.candidate_commit,
                "--output",
                output,
                "--json",
            ],
            cwd=self.candidate_checkout,
            label="complete-candidate-qualification",
        )
        return (
            f"complete candidate graph qualified at {self.candidate_commit[:12]}",
            {"result": output.name},
        )

    def _candidate_unit_suite(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        completed = self._run(
            [interpreter, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            cwd=self.candidate_checkout,
            check=False,
            label="candidate-unit-suite",
        )
        combined = completed.stdout + completed.stderr
        ran = re.search(r"^Ran (\d+) tests", combined, re.M)
        names = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\S+)", combined, re.M)))
        evidence = {
            "tests": int(ran.group(1)) if ran else None,
            "exit": completed.returncode,
            "failing_tests": names,
        }
        if completed.returncode != 0:
            raise RehearsalError(
                f"candidate unit suite exited {completed.returncode} with "
                f"{len(names)} failing tests: {', '.join(names) or 'unnamed'}"
            )
        return (f"candidate unit suite passed ({evidence['tests']} tests)", evidence)

    def _cli_smoke_check(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        completed = self._run(
            [interpreter, "-m", "se_harness", "--help"],
            cwd=self.candidate_checkout,
            label="cli-smoke-check",
        )
        if "usage" not in completed.stdout.lower():
            raise RehearsalError("candidate command line did not report its usage")
        return ("candidate command line reported its usage", {"exit": completed.returncode})

    def _deterministic_build(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        built: dict[str, dict[str, str]] = {}
        for suffix in ("a", "b"):
            source = self.root / f"source-{suffix}"
            raw = self.root / f"raw-{suffix}"
            raw.mkdir()
            self._run(
                [
                    interpreter,
                    "-m",
                    "build",
                    "--wheel",
                    "--sdist",
                    "--no-isolation",
                    "--outdir",
                    raw,
                    ".",
                ],
                cwd=source,
                extra_env={"SOURCE_DATE_EPOCH": self.source_date_epoch},
                label="deterministic-build",
            )
            wheels = sorted(item.name for item in raw.glob("*.whl"))
            sdists = sorted(item.name for item in raw.glob("*.tar.gz"))
            if len(wheels) != 1 or len(sdists) != 1:
                raise RehearsalError(
                    f"exported tree {source.name} produced {len(wheels)} wheels and "
                    f"{len(sdists)} sdists; exactly one of each is required"
                )
            built[suffix] = {"wheel": wheels[0], "sdist": sdists[0]}
        if built["a"] != built["b"]:
            raise RehearsalError(
                f"the two builds produced different distribution names: {built['a']} vs {built['b']}"
            )
        match = WHEEL_NAME_PATTERN.match(built["a"]["wheel"])
        if match is None:
            raise RehearsalError(f"built wheel name is not canonical: {built['a']['wheel']}")
        self.distribution = {
            "wheel": built["a"]["wheel"],
            "raw_sdist": built["a"]["sdist"],
            "version": match.group("version"),
        }
        return (
            f"two independent builds produced {built['a']['wheel']}",
            {"names": built["a"], "version": self.distribution["version"]},
        )

    def _sdist_normalization(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        sdist_name = f"se_harness-{self.distribution['version']}.tar.gz"
        for suffix in ("a", "b"):
            source = self.root / f"source-{suffix}"
            raw = self.root / f"raw-{suffix}"
            final = self.root / f"final-{suffix}"
            final.mkdir()
            shutil.copy2(raw / self.distribution["wheel"], final / self.distribution["wheel"])
            self._run(
                [
                    interpreter,
                    source / "scripts" / "normalize_sdist.py",
                    raw / self.distribution["raw_sdist"],
                    final / sdist_name,
                    "--epoch",
                    self.source_date_epoch,
                ],
                label="sdist-normalization",
            )
        self.distribution["sdist"] = sdist_name
        return (
            f"both sdists normalized at epoch {self.source_date_epoch}",
            {"sdist": sdist_name, "epoch": self.source_date_epoch},
        )

    def _build_determinism_comparison(self) -> tuple[str, dict[str, Any]]:
        digests: dict[str, dict[str, str]] = {}
        for name in (self.distribution["wheel"], self.distribution["sdist"]):
            left = self.root / "final-a" / name
            right = self.root / "final-b" / name
            offset = first_difference(left, right)
            left_digest = sha256_file(left)
            right_digest = sha256_file(right)
            if offset is not None:
                raise RehearsalError(
                    f"the two independent builds of {name} differ at byte offset {offset}: "
                    f"set A sha256 {left_digest}, set B sha256 {right_digest}"
                )
            digests[name] = {"sha256": left_digest}
        return ("both distribution sets compared byte-identical", {"digests": digests})

    def _bundle_assembly(self) -> tuple[str, dict[str, Any]]:
        bundle = self.root / "release-bundle"
        bundle.mkdir()
        wheel = self.distribution["wheel"]
        sdist = self.distribution["sdist"]
        # SPEC-RLO-004 rule 15: the bundle is assembled from the second built set and
        # verified against a manifest and plan derived from the first.
        shutil.copy2(self.root / "final-b" / wheel, bundle / wheel)
        shutil.copy2(self.root / "final-b" / sdist, bundle / sdist)
        if self.mode == "release-record":
            digests = {
                "wheel": self.plan["wheel_sha256"],
                "sdist": self.plan["sdist_sha256"],
            }
            source = "authorized release record"
        else:
            digests = {
                "wheel": sha256_file(self.root / "final-a" / wheel),
                "sdist": sha256_file(self.root / "final-a" / sdist),
            }
            source = "first distribution set"
        checksums = f"{digests['wheel']}  {wheel}\n{digests['sdist']}  {sdist}\n"
        (bundle / "SHA256SUMS").write_bytes(checksums.encode("utf-8"))
        return (
            "bundle assembled from the second distribution set",
            {
                "files": sorted(item.name for item in bundle.iterdir()),
                "checksum_source": source,
                "declared_digests": digests,
            },
        )

    def _bundle_manifest_creation(self) -> tuple[str, dict[str, Any]]:
        interpreter = venv_python(self.build_env)
        script = self.repository / "scripts" / "create_release_bundle_manifest.py"
        wheel = self.distribution["wheel"]
        sdist = self.distribution["sdist"]
        outputs: dict[str, str] = {}
        for label, directory in (
            ("a", self.root / "final-a"),
            ("b", self.root / "release-bundle"),
        ):
            output = self.root / f"bundle-manifest-{label}.json"
            self._run(
                [
                    interpreter,
                    script,
                    "--repository",
                    self.repository,
                    "--commit",
                    self.candidate_commit,
                    "--version",
                    self.distribution["version"],
                    "--wheel",
                    directory / wheel,
                    "--sdist",
                    directory / sdist,
                    "--output",
                    output,
                ],
                label="bundle-manifest-creation",
            )
            outputs[label] = output.name
        if self.mode == "candidate":
            self._derive_candidate_plan()
        return (
            "manifests created for the first set and for the assembled bundle",
            {"manifests": outputs, "plan_source": self.plan_source},
        )

    def _derive_candidate_plan(self) -> None:
        """Build a plan from the first distribution set, never from release authority."""
        if not self.plan:
            raise RehearsalError("candidate plan derivation requires a resolved plan shape")
        manifest = json.loads(
            (self.root / "bundle-manifest-a.json").read_text(encoding="utf-8")
        )
        plan = derive_rehearsal_plan(self.plan, manifest, self.candidate_commit)
        path = self.root / "candidate-rehearsal-plan.json"
        path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.plan_path = path
        self.plan = plan
        self.plan_source = "derivation-from-the-first-distribution-set"

    def _build_manifest_verification(self) -> tuple[str, dict[str, Any]]:
        if self.plan_path is None:
            raise RehearsalError("no plan is available for build-manifest verification")
        output = self.root / "rebuilt-manifest-result.json"
        self._run(
            [
                sys.executable,
                self.repository / ".github" / "scripts" / "publish_release.py",
                "verify-build-manifest",
                "--plan",
                self.plan_path,
                "--manifest",
                self.root / "bundle-manifest-b.json",
                "--output",
                output,
            ],
            label="build-manifest-verification",
        )
        return (
            "the second set's manifest verified against the first set's plan",
            {"mode": self.mode, "plan_source": self.plan_source},
        )

    def _bundle_verification(self) -> tuple[str, dict[str, Any]]:
        if self.plan_path is None:
            raise RehearsalError("no plan is available for bundle verification")
        output = self.root / "qualification.json"
        self._run(
            [
                sys.executable,
                self.repository / ".github" / "scripts" / "publish_release.py",
                "verify-bundle",
                "--plan",
                self.plan_path,
                "--directory",
                self.root / "release-bundle",
                "--output",
                output,
            ],
            label="bundle-verification",
        )
        return (
            "the assembled bundle verified against the plan",
            {
                "mode": self.mode,
                "plan_source": self.plan_source,
                "compares_against_authorized_release_identity": self.mode == "release-record",
            },
        )

    def _teardown(self) -> tuple[str, dict[str, Any]]:
        if self.candidate_checkout.exists():
            self._run(
                [
                    "git",
                    "-C",
                    self.repository,
                    "worktree",
                    "remove",
                    "--force",
                    self.candidate_checkout,
                ],
                check=False,
                label="teardown",
            )
        remove_tree_without_following_links(self.root, self.deleted_paths)
        self._run(["git", "-C", self.repository, "worktree", "prune"], check=False, label="teardown")
        if self.root.exists():
            raise RehearsalError(f"teardown left the rehearsal root behind: {self.root}")
        root_real = os.path.realpath(self.root)
        root_key = os.path.normcase(root_real)
        for candidate in self.deleted_paths:
            # The root itself is the last path teardown removes, and its parent lies
            # outside the root by construction. Every other deleted path is audited by
            # its parent, so a link's own target cannot make it look contained.
            if os.path.normcase(os.path.realpath(candidate)) == root_key:
                continue
            if not path_is_within(root_real, Path(candidate).parent):
                raise RehearsalError(f"teardown deleted a path outside the rehearsal root: {candidate}")
        after = self._git("status", "--porcelain")
        before_lines = set(self.git_status_before.splitlines())
        residue = sorted(set(after.splitlines()) - before_lines)
        if residue:
            raise RehearsalError(
                f"teardown left {len(residue)} untracked or modified entries: {residue[:8]}"
            )
        return (
            f"{len(self.deleted_paths)} derived paths removed without following a link",
            {
                "removed_paths": len(self.deleted_paths),
                "repository_worktree_clean": not after.strip(),
                "residue": residue,
            },
        )

    # -- orchestration -----------------------------------------------------

    def run(self) -> dict[str, Any]:
        ok_temp = self._record("temporary-path-identity", self._temporary_path_identity)
        self._record("release-record-format-validation", self._release_record_format_validation)
        ok_resolution = self._record("evaluator-resolution", self._evaluator_resolution)
        if ok_resolution:
            ok_acquire = self._record(
                "evaluator-acquisition-and-hash-proof",
                self._evaluator_acquisition_and_hash_proof,
            )
        else:
            self._blocked("evaluator-acquisition-and-hash-proof", "evaluator-resolution")
            ok_acquire = False
        if ok_acquire:
            ok_identity = self._record("evaluator-identity-proof", self._evaluator_identity_proof)
        else:
            self._blocked("evaluator-identity-proof", "evaluator-acquisition-and-hash-proof")
            ok_identity = False
        if not ok_identity:
            self._blocked("predecessor-view-qualification", "evaluator-identity-proof")
        else:
            exclusion = self._predecessor_view_exclusion()
            if exclusion is None:
                self._record(
                    "predecessor-view-qualification", self._predecessor_view_qualification
                )
            else:
                reason, evidence = exclusion
                self.outcomes.append(
                    MechanicOutcome(
                        mechanic="predecessor-view-qualification",
                        outcome="excluded",
                        detail="no committed record binds the resolved evaluator as its predecessor",
                        reason=reason,
                        evidence=evidence,
                    )
                )
        self._record("distribution-policy-validation", self._distribution_policy_validation)
        ok_plan = self._record("plan-resolution", self._plan_resolution)
        self._record("resolution-refusal-document", self._resolution_refusal_document)

        if not ok_temp:
            for mechanic in (
                "candidate-export",
                "pinned-build-tool-installation",
                "complete-candidate-qualification",
                "candidate-unit-suite",
                "cli-smoke-check",
                "deterministic-build",
                "sdist-normalization",
                "build-determinism-comparison",
                "bundle-assembly",
                "bundle-manifest-creation",
                "build-manifest-verification",
                "bundle-verification",
            ):
                self._blocked(mechanic, "temporary-path-identity")
            self._record("teardown", self._teardown)
            return self.result()

        ok_export = self._record("candidate-export", self._candidate_export)
        ok_tools = self._record("pinned-build-tool-installation", self._pinned_build_tool_installation)
        if ok_export and ok_tools:
            self._record("complete-candidate-qualification", self._complete_candidate_qualification)
            self._record("candidate-unit-suite", self._candidate_unit_suite)
            self._record("cli-smoke-check", self._cli_smoke_check)
            ok_build = self._record("deterministic-build", self._deterministic_build)
        else:
            for mechanic in (
                "complete-candidate-qualification",
                "candidate-unit-suite",
                "cli-smoke-check",
                "deterministic-build",
            ):
                self._blocked(
                    mechanic,
                    "candidate-export" if not ok_export else "pinned-build-tool-installation",
                )
            ok_build = False
        if ok_build:
            ok_normalize = self._record("sdist-normalization", self._sdist_normalization)
        else:
            self._blocked("sdist-normalization", "deterministic-build")
            ok_normalize = False
        if ok_normalize:
            self._record("build-determinism-comparison", self._build_determinism_comparison)
            ok_bundle = self._record("bundle-assembly", self._bundle_assembly)
            if ok_bundle:
                ok_manifest = self._record(
                    "bundle-manifest-creation", self._bundle_manifest_creation
                )
            else:
                self._blocked("bundle-manifest-creation", "bundle-assembly")
                ok_manifest = False
        else:
            for mechanic in (
                "build-determinism-comparison",
                "bundle-assembly",
                "bundle-manifest-creation",
            ):
                self._blocked(mechanic, "sdist-normalization")
            ok_manifest = ok_bundle = False
        if ok_manifest and ok_bundle and (ok_plan or self.mode == "candidate"):
            self._record("build-manifest-verification", self._build_manifest_verification)
            self._record("bundle-verification", self._bundle_verification)
        else:
            for mechanic in ("build-manifest-verification", "bundle-verification"):
                self._blocked(mechanic, "bundle-manifest-creation")

        if self.keep_root:
            self.outcomes.append(
                MechanicOutcome(
                    mechanic="teardown",
                    outcome="excluded",
                    detail="retained for inspection",
                    reason="--keep-root was requested, so teardown was not rehearsed",
                )
            )
        else:
            self._record("teardown", self._teardown)
        return self.result()

    def preconditions(self) -> dict[str, Any]:
        """Report the checkout state the rehearsal inherited.

        A hosted run starts from a clean checkout. An implementer's run may not,
        and the orchestrator's own qualification refuses a dirty worktree, so the
        inherited state is reported rather than left to be rediscovered in a
        mechanic's transcript.

        Line-ending conversion is reported for the same reason. The candidate checkout
        is created with `git worktree add`, exactly as the orchestrator creates it, so
        it inherits this setting; the candidate suite contains assertions on exact bytes
        whose outcome therefore depends on it.
        """
        entries = sorted(
            line for line in self.git_status_before.splitlines() if line.strip()
        )
        return {
            "clean_worktree": not entries,
            "uncommitted_entries": len(entries),
            "uncommitted_sample": entries[:8],
            "line_ending_conversion": self.line_ending_conversion,
        }

    def result(self) -> dict[str, Any]:
        ordered = [outcome.as_json() for outcome in self.outcomes]
        declared = {
            item["id"]
            for item in self.declaration["mechanics"]
        }
        reported = {outcome.mechanic for outcome in self.outcomes}
        missing = sorted(declared - reported)
        return {
            "schema": RESULT_SCHEMA,
            "authority": AUTHORITY,
            "platform": platform_family(),
            "mode": self.mode,
            "verification_compares_against_authorized_release_identity": (
                self.mode == "release-record"
            ),
            "verification_plan_source": self.plan_source,
            "candidate_commit": self.candidate_commit,
            "source_date_epoch": self.source_date_epoch,
            "resolution_subject_record": self.subject_record,
            "preconditions": self.preconditions(),
            "distribution": self.distribution,
            "state": self._state(missing),
            "unreported_mechanics": missing,
            "mechanics": ordered,
            "transcript": self.transcript,
        }

    def _state(self, missing: Sequence[str]) -> str:
        if missing:
            return "failed"
        return "failed" if self.failed else "rehearsed"


# ---------------------------------------------------------------------------
# bounded workflow reader
# ---------------------------------------------------------------------------

# SE Harness declares no runtime dependency, and its unit suite runs on a bare
# interpreter, so the divergence check reads workflow YAML with a bounded reader for
# the GitHub Actions subset instead of adding a parser dependency. The reader accepts
# only the constructs these workflows use and refuses everything else, which suits
# untrusted input: an unrecognized construct fails the check rather than being guessed
# at. `--cross-check-yaml` compares its job structure with PyYAML wherever PyYAML
# happens to be installed.

_YAML_TRUE = frozenset({"true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"})
_YAML_FALSE = frozenset({"false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"})
_YAML_NULL = frozenset({"", "~", "null", "Null", "NULL"})
_PLAIN_KEY = re.compile(r"^([^:#'\"\s][^:#]*):(?=\s|$)")


class _WorkflowReader:
    """Read the GitHub Actions YAML subset, refusing anything outside it."""

    def __init__(self, text: str, name: str) -> None:
        self.name = name
        self.lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.index = 0

    # -- lexical helpers ---------------------------------------------------

    def _fail(self, message: str) -> RehearsalError:
        return RehearsalError(f"{self.name} line {self.index + 1}: {message}")

    @staticmethod
    def _indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    def _skip(self) -> None:
        while self.index < len(self.lines):
            line = self.lines[self.index]
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                self.index += 1
                continue
            if "\t" in line[: self._indent(line) + 1]:
                raise self._fail("indentation uses a tab")
            return

    def _at_end(self) -> bool:
        self._skip()
        return self.index >= len(self.lines)

    @staticmethod
    def _strip_comment(text: str) -> str:
        quote: str | None = None
        for position, character in enumerate(text):
            if quote:
                if character == quote:
                    quote = None
                continue
            if character in "'\"":
                quote = character
                continue
            if character == "#" and (position == 0 or text[position - 1] in " \t"):
                return text[:position].rstrip()
        return text.rstrip()

    # -- structure ---------------------------------------------------------

    def parse(self) -> dict[str, Any]:
        if self._at_end():
            raise self._fail("the workflow is empty")
        value = self._node(self._indent(self.lines[self.index]))
        if not self._at_end():
            raise self._fail("trailing content follows the document")
        if not isinstance(value, dict):
            raise RehearsalError(f"{self.name} is not a mapping")
        return value

    def _node(self, indent: int) -> Any:
        self._skip()
        body = self.lines[self.index][indent:]
        if body.startswith("- ") or body.strip() == "-":
            return self._sequence(indent)
        if _PLAIN_KEY.match(body) or body[:1] in {"'", '"'} and self._quoted_key(body) is not None:
            return self._mapping(indent)
        self.index += 1
        return self._scalar(self._strip_comment(body))

    def _quoted_key(self, body: str) -> tuple[str, str] | None:
        quote = body[0]
        position = 1
        while position < len(body):
            if body[position] == "\\" and quote == '"':
                position += 2
                continue
            if body[position] == quote:
                remainder = body[position + 1 :]
                if not remainder.startswith(":"):
                    return None
                return self._scalar(body[: position + 1]), remainder[1:]
            position += 1
        return None

    def _mapping(self, indent: int) -> dict[str, Any]:
        mapping: dict[str, Any] = {}
        while not self._at_end():
            line = self.lines[self.index]
            current = self._indent(line)
            if current < indent:
                break
            if current > indent:
                raise self._fail("unexpected indentation inside a mapping")
            body = line[indent:]
            if body.startswith("- ") or body.strip() == "-":
                break
            if body[:1] in {"'", '"'}:
                split = self._quoted_key(body)
                if split is None:
                    raise self._fail("a quoted key is not terminated by a colon")
                key, remainder = split
            else:
                match = _PLAIN_KEY.match(body)
                if match is None:
                    raise self._fail("expected a mapping key")
                key = match.group(1).rstrip()
                remainder = body[match.end() :]
            if key in mapping:
                raise self._fail(f"the mapping repeats the key {key!r}")
            mapping[key] = self._value(remainder, indent)
        return mapping

    def _sequence(self, indent: int) -> list[Any]:
        items: list[Any] = []
        while not self._at_end():
            line = self.lines[self.index]
            if self._indent(line) != indent:
                break
            body = line[indent:]
            if body.strip() == "-":
                self.index += 1
                if self._at_end():
                    items.append(None)
                    break
                following = self.lines[self.index]
                if self._indent(following) <= indent:
                    items.append(None)
                    continue
                items.append(self._node(self._indent(following)))
                continue
            if not body.startswith("- "):
                break
            inner = body[2:]
            offset = indent + 2 + (len(inner) - len(inner.lstrip(" ")))
            # Re-spell the dash as indentation so the item parses like any other node.
            self.lines[self.index] = " " * offset + inner.lstrip(" ")
            items.append(self._node(offset))
        return items

    def _value(self, remainder: str, indent: int) -> Any:
        text = self._strip_comment(remainder.strip())
        if text in {"|", "|-", ">", ">-"}:
            return self._block_scalar(text, indent)
        if text in {"|+", ">+"}:
            raise self._fail("keep-chomping block scalars are not supported")
        if text:
            self.index += 1
            return self._scalar(text)
        self.index += 1
        if self._at_end():
            return None
        following = self.lines[self.index]
        offset = self._indent(following)
        if offset > indent:
            return self._node(offset)
        if offset == indent and (
            following[indent:].startswith("- ") or following[indent:].strip() == "-"
        ):
            return self._sequence(indent)
        return None

    def _block_scalar(self, header: str, indent: int) -> str:
        folded = header.startswith(">")
        strip = header.endswith("-")
        self.index += 1
        body: list[str] = []
        block_indent: int | None = None
        while self.index < len(self.lines):
            line = self.lines[self.index]
            if not line.strip():
                body.append("")
                self.index += 1
                continue
            current = self._indent(line)
            if block_indent is None:
                if current <= indent:
                    break
                block_indent = current
            if current < block_indent:
                break
            if "\t" in line[:block_indent]:
                raise self._fail("a block scalar is indented with a tab")
            body.append(line[block_indent:])
            self.index += 1
        while body and not body[-1]:
            body.pop()
        if folded:
            pieces: list[str] = []
            for entry in body:
                if not entry:
                    pieces.append("\n")
                elif pieces and not pieces[-1].endswith("\n"):
                    pieces[-1] = f"{pieces[-1]} {entry}"
                else:
                    pieces.append(entry)
            value = "".join(pieces)
        else:
            value = "\n".join(body)
        if strip:
            return value
        return f"{value}\n" if value else ""

    # -- scalars -----------------------------------------------------------

    def _scalar(self, text: str) -> Any:
        if text.startswith('"'):
            return self._double_quoted(text)
        if text.startswith("'"):
            return self._single_quoted(text)
        if text.startswith("{"):
            return self._flow_mapping(text)
        if text.startswith("["):
            return self._flow_sequence(text)
        if text.startswith(("&", "*", "!")):
            raise self._fail("anchors, aliases, and tags are not supported")
        if text in _YAML_TRUE:
            return True
        if text in _YAML_FALSE:
            return False
        if text in _YAML_NULL:
            return None
        if re.fullmatch(r"-?\d+", text):
            return int(text)
        if re.fullmatch(r"-?\d+\.\d*", text):
            return float(text)
        return text

    def _double_quoted(self, text: str) -> str:
        if len(text) < 2 or not text.endswith('"'):
            raise self._fail("a double-quoted scalar is not terminated")
        inner = text[1:-1]
        out: list[str] = []
        position = 0
        while position < len(inner):
            character = inner[position]
            if character == "\\":
                position += 1
                if position >= len(inner):
                    raise self._fail("a double-quoted scalar ends in an escape")
                out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(inner[position], inner[position]))
            else:
                out.append(character)
            position += 1
        return "".join(out)

    def _single_quoted(self, text: str) -> str:
        if len(text) < 2 or not text.endswith("'"):
            raise self._fail("a single-quoted scalar is not terminated")
        return text[1:-1].replace("''", "'")

    def _split_flow(self, text: str, open_character: str, close_character: str) -> list[str]:
        if not text.endswith(close_character):
            raise self._fail("a flow collection is not terminated")
        inner = text[1:-1]
        parts: list[str] = []
        current: list[str] = []
        quote: str | None = None
        depth = 0
        for character in inner:
            if quote:
                current.append(character)
                if character == quote:
                    quote = None
                continue
            if character in "'\"":
                quote = character
                current.append(character)
                continue
            if character in "{[":
                depth += 1
            elif character in "}]":
                depth -= 1
            if character == "," and depth == 0:
                parts.append("".join(current))
                current = []
                continue
            current.append(character)
        if quote or depth:
            raise self._fail("a flow collection is unbalanced")
        tail = "".join(current).strip()
        if tail:
            parts.append(tail)
        return [part.strip() for part in parts if part.strip()]

    def _flow_mapping(self, text: str) -> dict[str, Any]:
        mapping: dict[str, Any] = {}
        for part in self._split_flow(text, "{", "}"):
            key, separator, value = part.partition(":")
            if not separator:
                raise self._fail("a flow mapping entry has no colon")
            name = self._scalar(key.strip())
            if not isinstance(name, str):
                raise self._fail("a flow mapping key is not a string")
            if name in mapping:
                raise self._fail(f"a flow mapping repeats the key {name!r}")
            mapping[name] = self._scalar(value.strip())
        return mapping

    def _flow_sequence(self, text: str) -> list[Any]:
        return [self._scalar(part) for part in self._split_flow(text, "[", "]")]


def read_workflow(path: Path, *, cross_check: bool = False) -> dict[str, Any]:
    """Read a workflow's structure, optionally cross-checking against PyYAML."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RehearsalError(f"{path.name} is unreadable: {exc}") from exc
    value = _WorkflowReader(text, path.name).parse()
    if not isinstance(value.get("jobs"), dict):
        raise RehearsalError(f"{path.name} has no job mapping")
    for name, job in value["jobs"].items():
        if not isinstance(job, dict):
            raise RehearsalError(f"{path.name}: job {name} is not a mapping")
    if cross_check:
        _cross_check_with_pyyaml(path, text, value)
    return value


def _cross_check_with_pyyaml(path: Path, text: str, value: dict[str, Any]) -> None:
    """Fail when a second parser disagrees about the job structure."""
    try:
        import yaml
    except ImportError as exc:
        raise RehearsalError(
            f"cross-checking {path.name} was requested but PyYAML is not installed"
        ) from exc
    try:
        reference = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise RehearsalError(f"{path.name} is not valid YAML: {exc}") from exc
    if not isinstance(reference, dict) or not isinstance(reference.get("jobs"), dict):
        raise RehearsalError(f"{path.name} has no job mapping under a reference parse")
    if reference["jobs"] != value["jobs"]:
        differing = sorted(
            name
            for name in set(reference["jobs"]) | set(value["jobs"])
            if reference["jobs"].get(name) != value["jobs"].get(name)
        )
        raise RehearsalError(
            f"{path.name}: the bounded reader and PyYAML disagree about "
            f"{', '.join(differing)}"
        )


def normalized_run(text: str) -> bytes:
    """Canonicalize a step script for digesting: LF endings, no trailing blank."""
    return (text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n").encode("utf-8")


def _remove_array_assignments(text: str) -> str:
    out: list[str] = []
    index = 0
    pattern = re.compile(r"(?m)^[ \t]*[A-Za-z_][A-Za-z0-9_]*\+?=\(")
    while True:
        match = pattern.search(text, index)
        if match is None:
            out.append(text[index:])
            return "".join(out)
        out.append(text[index : match.start()])
        depth = 1
        position = match.end()
        while position < len(text) and depth:
            if text[position] == "(":
                depth += 1
            elif text[position] == ")":
                depth -= 1
            position += 1
        index = position


def _extract_substitutions(text: str) -> tuple[str, list[str]]:
    inner: list[str] = []
    out: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("$(", index):
            depth = 1
            position = index + 2
            while position < len(text) and depth:
                if text.startswith("$(", position):
                    depth += 1
                    position += 2
                    continue
                if text[position] == ")":
                    depth -= 1
                    position += 1
                    continue
                position += 1
            inner.append(text[index + 2 : position - 1])
            # No surrounding space: a substitution is part of the shell word it sits in,
            # so gluing it in keeps `"$root/final-a/$(name)"` a single unusable token.
            out.append("<sub>")
            index = position
            continue
        out.append(text[index])
        index += 1
    return "".join(out), inner


def _split_segments(text: str) -> list[str]:
    segments: list[str] = []
    current: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(text):
        char = text[index]
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "'\"":
            quote = char
            current.append(char)
            index += 1
            continue
        if char in "()":
            current.append(" ")
            index += 1
            continue
        if text.startswith("&&", index) or text.startswith("||", index):
            segments.append("".join(current))
            current = []
            index += 2
            continue
        if char == "&":
            # `2>&1` and `>&2` are redirections, not command separators.
            previous = "".join(current).rstrip()
            if (previous and previous[-1] in "<>") or text[index + 1 : index + 2] == ">":
                current.append(char)
                index += 1
                continue
        if char in ";|\n&":
            segments.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    segments.append("".join(current))
    if quote:
        raise RehearsalError("orchestrator step script has an unbalanced quote")
    return [segment for segment in (item.strip() for item in segments) if segment]


def normalize_command_token(token: str) -> str:
    if not token or any(character.isspace() for character in token):
        # A word carrying whitespace is a literal argument, never a path.
        return token
    parts = [part for part in re.split(r"[\\/]+", token) if part]
    if not parts:
        return PLACEHOLDER
    tail = parts[-1]
    if tail in KNOWN_EXECUTABLES:
        return tail[:-4] if tail.endswith(".exe") else tail
    for anchor in (".github", "scripts", "tests"):
        if anchor in parts:
            return "/".join(parts[parts.index(anchor) :])
    if any("$" in part or part.startswith("<") for part in parts):
        return PLACEHOLDER
    return "/".join(parts)


def command_keys(script: str) -> list[str]:
    """Derive one identity per program invocation in a step script."""
    text = script.replace("\\\n", " ")
    text = re.sub(r"\$\{\{.*?\}\}", "<expr>", text, flags=re.S)
    text = _remove_array_assignments(text)
    text, substitutions = _extract_substitutions(text)
    pending = [text, *substitutions]
    keys: list[str] = []
    while pending:
        current = pending.pop(0)
        current, more = _extract_substitutions(current)
        pending.extend(more)
        for segment in _split_segments(current):
            try:
                tokens = shlex.split(segment, posix=True)
            except ValueError as exc:
                raise RehearsalError(f"orchestrator step script cannot be tokenized: {exc}") from exc
            tokens = [
                token
                for token in tokens
                if not re.match(r"^\d*[<>]", token) and token not in {">", ">>", "<", "2>"}
            ]
            while tokens and (
                tokens[0] in LEADING_KEYWORDS
                or re.match(r"^[A-Za-z_][A-Za-z0-9_]*\+?=", tokens[0])
            ):
                tokens = tokens[1:]
            if not tokens:
                continue
            key = _command_key(tokens)
            if key:
                keys.append(key)
    return keys


def _command_key(tokens: Sequence[str]) -> str | None:
    executable = normalize_command_token(tokens[0])
    if executable == PLACEHOLDER or executable.startswith("<"):
        return None
    key = [executable]
    index = 1
    while index < len(tokens) and len(key) < 6:
        token = tokens[index]
        if token in {"-m", "-c"} and index + 1 < len(tokens):
            key.extend([token, tokens[index + 1]])
            index += 2
            continue
        if token == "-I":
            index += 1
            continue
        if token.startswith("-") or token in {".", "..", "-"}:
            break
        normalized = normalize_command_token(token)
        if normalized == PLACEHOLDER or normalized.startswith("<"):
            break
        key.append(normalized)
        index += 1
    return " ".join(key)


@dataclass
class JobClassification:
    name: str
    platform: str
    excluded: bool
    attributes: list[str]


_SECRET_KEY_PATTERN = re.compile(r"TOKEN|SECRET|PASSWORD|CREDENTIAL", re.I)

#: Values that disable an option rather than supply a credential. ``persist-credentials:
#: false`` on ``actions/checkout`` refuses the credential it names, so a credential-shaped
#: key is only an attribute when its value is enabled.
_DISABLED_VALUES = frozenset({"false", "no", "off", "0", ""})


def _is_enabled(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in _DISABLED_VALUES
    if isinstance(value, int):
        return value != 0
    return True


def _secret_attributes(value: Any, where: str, found: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                isinstance(key, str)
                and _SECRET_KEY_PATTERN.search(key)
                and _is_enabled(item)
            ):
                found.append(f"{where} names {key}")
            _secret_attributes(item, where, found)
        return
    if isinstance(value, list):
        for item in value:
            _secret_attributes(item, where, found)
        return
    if isinstance(value, str) and "secrets." in value:
        found.append(f"{where} reads a repository secret")


def classify_jobs(
    workflow: dict[str, Any], external_state_actions: Sequence[str]
) -> dict[str, JobClassification]:
    """Classify orchestrator jobs by their declared attributes (SPEC-RLO-004 rule 2)."""
    classifications: dict[str, JobClassification] = {}
    for name, job in workflow["jobs"].items():
        if not isinstance(job, dict):
            raise RehearsalError(f"job {name} is not a mapping and cannot be classified")
        attributes: list[str] = []
        permissions = job.get("permissions")
        if permissions is None:
            attributes.append("declares no explicit permissions")
        elif isinstance(permissions, str):
            if permissions != "read-all":
                attributes.append(f"permissions: {permissions}")
        elif isinstance(permissions, dict):
            for scope, level in permissions.items():
                if level == "write":
                    attributes.append(f"{scope}: write permission")
                elif scope == "id-token":
                    attributes.append(f"id-token: {level}")
        else:
            raise RehearsalError(f"job {name} has unclassifiable permissions")
        if job.get("environment") is not None:
            attributes.append("declares a protected environment")
        _secret_attributes(job.get("env"), f"job {name} env", attributes)
        steps = job.get("steps")
        if not isinstance(steps, list):
            raise RehearsalError(f"job {name} declares no step list and cannot be classified")
        for step in steps:
            if not isinstance(step, dict):
                raise RehearsalError(f"a step of job {name} is not a mapping")
            uses = step.get("uses")
            if isinstance(uses, str):
                action = uses.split("@", 1)[0]
                if action in external_state_actions:
                    attributes.append(f"uses the external-state action {action}")
            _secret_attributes(step.get("env"), f"step {step.get('name')!r} env", attributes)
            _secret_attributes(step.get("with"), f"step {step.get('name')!r} with", attributes)
        classifications[name] = JobClassification(
            name=name,
            platform=runner_platform_family(job.get("runs-on")),
            excluded=bool(attributes),
            attributes=attributes,
        )
    # SPEC-RLO-004 rule 2: exclusion is transitive. A job that consumes state produced
    # by an excluded job runs after a credential has been used and cannot be rehearsed.
    changed = True
    while changed:
        changed = False
        for name, job in workflow["jobs"].items():
            if classifications[name].excluded:
                continue
            needs = job.get("needs") or []
            if isinstance(needs, str):
                needs = [needs]
            for dependency in needs:
                if dependency not in classifications:
                    raise RehearsalError(f"job {name} needs an unknown job {dependency}")
                if classifications[dependency].excluded:
                    classifications[name].excluded = True
                    classifications[name].attributes.append(
                        f"depends on the excluded job {dependency}"
                    )
                    changed = True
                    break
    return classifications


_ACTION_PIN = re.compile(r"^[0-9a-f]{40}$")


def _classify_action(
    job: str,
    step: dict[str, Any],
    infrastructure: set[str],
    external: set[str],
    findings: list[dict[str, Any]],
) -> None:
    """Refuse an action in a rehearsed job that is neither declared nor pinned.

    A credential-free job can also gain a publication mechanic through a marketplace
    action rather than a shell command, so the action surface is classified too.
    """
    uses = step.get("uses")
    if not isinstance(uses, str):
        return
    action, separator, reference = uses.partition("@")
    if action not in infrastructure and action not in external:
        findings.append(
            {
                "kind": "unclassified_action",
                "direction": "uncovered",
                "job": job,
                "step": step.get("name"),
                "command": action,
                "detail": (
                    "a rehearsed job uses an action that is neither declared "
                    "infrastructure nor a declared external-state action"
                ),
            }
        )
        return
    if not separator or _ACTION_PIN.match(reference) is None:
        findings.append(
            {
                "kind": "unpinned_action",
                "direction": "uncovered",
                "job": job,
                "step": step.get("name"),
                "command": uses,
                "detail": "a rehearsed job uses an action that is not pinned to a full commit",
            }
        )


def _deduplicate(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Report one finding per condition, not one per repeated occurrence."""
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for finding in findings:
        key = json.dumps(finding, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    return unique


def check_divergence(
    repository: Path, declaration: dict[str, Any], *, cross_check: bool = False
) -> dict[str, Any]:
    """Fail closed when the orchestrator and the rehearsed set differ either way."""
    orchestrator_path = repository / declaration["orchestrator"]
    lane_path = repository / declaration["rehearsal_lane"]
    workflow = read_workflow(orchestrator_path, cross_check=cross_check)
    classifications = classify_jobs(workflow, declaration.get("external_state_actions", []))
    required = {name for name, item in classifications.items() if not item.excluded}
    if not required:
        raise RehearsalError("no credential-free orchestrator job remains to rehearse")

    mechanics = declaration_index(declaration)
    trivia = set(declaration["trivia_commands"])
    declared_steps = {(item["job"], item["step"]): item for item in declaration["steps"]}
    findings: list[dict[str, Any]] = []
    covered_commands: dict[str, set[str]] = {}
    for identifier, mechanic in mechanics.items():
        if mechanic["origin"] != "orchestrator":
            continue
        for command in mechanic["commands"]:
            covered_commands.setdefault(mechanic["job"], set()).add(command)

    infrastructure = set(declaration.get("infrastructure_actions", []))
    external = set(declaration.get("external_state_actions", []))
    observed_steps: set[tuple[str, str]] = set()
    observed_commands: dict[str, set[str]] = {}
    for name in sorted(required):
        job = workflow["jobs"][name]
        for step in job["steps"]:
            _classify_action(name, step, infrastructure, external, findings)
            script = step.get("run")
            if script is None:
                continue
            title = step.get("name")
            if not isinstance(title, str):
                findings.append(
                    {
                        "kind": "unnamed_step",
                        "direction": "uncovered",
                        "job": name,
                        "detail": "a credential-free step with a script has no name to declare",
                    }
                )
                continue
            observed_steps.add((name, title))
            declared = declared_steps.get((name, title))
            digest = hashlib.sha256(normalized_run(script)).hexdigest()
            if declared is None:
                findings.append(
                    {
                        "kind": "undeclared_step",
                        "direction": "uncovered",
                        "job": name,
                        "step": title,
                        "run_sha256": digest,
                        "detail": (
                            "a credential-free orchestrator step is absent from the "
                            "declaration; its mechanics are not rehearsed"
                        ),
                    }
                )
            elif declared.get("run_sha256") != digest:
                findings.append(
                    {
                        "kind": "changed_step",
                        "direction": "uncovered",
                        "job": name,
                        "step": title,
                        "declared_sha256": declared.get("run_sha256"),
                        "run_sha256": digest,
                        "detail": (
                            "a credential-free orchestrator step changed; its rehearsal "
                            "coverage must be re-derived and the declaration updated"
                        ),
                    }
                )
            for key in command_keys(script):
                observed_commands.setdefault(name, set()).add(key)
                if key in covered_commands.get(name, set()):
                    continue
                # A mechanic command must match the whole key, so `python` can never
                # satisfy `python -m pip install`. Shell trivia is declared by command
                # name because its arguments carry no mechanic identity; an invocation
                # smuggled into a trivia argument is caught by the step digest instead.
                if key.split(" ", 1)[0] in trivia:
                    continue
                findings.append(
                    {
                        "kind": "unclassified_command",
                        "direction": "uncovered",
                        "job": name,
                        "step": title,
                        "command": key,
                        "detail": (
                            "a credential-free orchestrator command matches no declared "
                            "mechanic and is not declared shell trivia"
                        ),
                    }
                )

    for (job_name, title), declared in sorted(declared_steps.items()):
        if job_name not in required:
            findings.append(
                {
                    "kind": "stale_step",
                    "direction": "stale",
                    "job": job_name,
                    "step": title,
                    "detail": "the declaration names a step of a job that is no longer rehearsed",
                }
            )
        elif (job_name, title) not in observed_steps:
            findings.append(
                {
                    "kind": "stale_step",
                    "direction": "stale",
                    "job": job_name,
                    "step": title,
                    "detail": "the declaration names a step the orchestrator no longer performs",
                }
            )

    mechanic_report: list[dict[str, Any]] = []
    for identifier, mechanic in sorted(mechanics.items()):
        if mechanic["origin"] == "rehearsal-only":
            mechanic_report.append(
                {"mechanic": identifier, "coverage": "rehearsal-only", "job": None}
            )
            continue
        job_name = mechanic["job"]
        state = "covered"
        if job_name not in required:
            state = "stale"
            findings.append(
                {
                    "kind": "stale_mechanic",
                    "direction": "stale",
                    "job": job_name,
                    "mechanic": identifier,
                    "detail": "the declaration names a mechanic of a job that is no longer rehearsed",
                }
            )
        else:
            for command in mechanic["commands"]:
                if command not in observed_commands.get(job_name, set()):
                    state = "stale"
                    findings.append(
                        {
                            "kind": "stale_mechanic",
                            "direction": "stale",
                            "job": job_name,
                            "mechanic": identifier,
                            "command": command,
                            "detail": "the orchestrator no longer invokes this declared command",
                        }
                    )
            expected = [classifications[job_name].platform] if job_name in classifications else []
            if sorted(mechanic["orchestrator_platforms"]) != sorted(expected):
                state = "stale"
                findings.append(
                    {
                        "kind": "platform_claim",
                        "direction": "stale",
                        "job": job_name,
                        "mechanic": identifier,
                        "declared": mechanic["orchestrator_platforms"],
                        "observed": expected,
                        "detail": "the declared orchestrator platform differs from the job's runner type",
                    }
                )
        mechanic_report.append({"mechanic": identifier, "coverage": state, "job": job_name})

    orchestrator_platforms = sorted({classifications[name].platform for name in required})
    lane = _lane_report(lane_path, declaration, findings, cross_check=cross_check)
    findings = _deduplicate(findings)
    verdict = "exact" if not findings else "divergent"
    return {
        "schema": DIVERGENCE_SCHEMA,
        "authority": AUTHORITY,
        "verdict": verdict,
        "orchestrator": declaration["orchestrator"],
        "rehearsal_lane": declaration["rehearsal_lane"],
        "rehearsed_jobs": sorted(required),
        "orchestrator_platforms": orchestrator_platforms,
        "excluded_jobs": [
            {"job": item.name, "attributes": item.attributes}
            for item in sorted(classifications.values(), key=lambda entry: entry.name)
            if item.excluded
        ],
        "mechanics": mechanic_report,
        "lane": lane,
        "findings": findings,
    }


def _lane_report(
    lane_path: Path,
    declaration: dict[str, Any],
    findings: list[dict[str, Any]],
    *,
    cross_check: bool = False,
) -> dict[str, Any]:
    required_platforms = sorted(declaration["required_platforms"])
    if not lane_path.is_file():
        findings.append(
            {
                "kind": "missing_lane",
                "direction": "uncovered",
                "detail": f"the rehearsal lane is absent: {lane_path.name}",
            }
        )
        return {"platforms": [], "permissions_read_only": False}
    lane = read_workflow(lane_path, cross_check=cross_check)
    platforms: set[str] = set()
    read_only = True
    for name, job in lane["jobs"].items():
        permissions = job.get("permissions")
        if permissions != {"contents": "read"}:
            read_only = False
            findings.append(
                {
                    "kind": "lane_permissions",
                    "direction": "uncovered",
                    "job": name,
                    "detail": "a rehearsal lane job does not declare contents: read only",
                }
            )
        if job.get("environment") is not None:
            read_only = False
            findings.append(
                {
                    "kind": "lane_environment",
                    "direction": "uncovered",
                    "job": name,
                    "detail": "a rehearsal lane job declares an environment",
                }
            )
        secrets: list[str] = []
        _secret_attributes(job, f"lane job {name}", secrets)
        if secrets:
            read_only = False
            findings.append(
                {
                    "kind": "lane_secret",
                    "direction": "uncovered",
                    "job": name,
                    "detail": f"a rehearsal lane job references a credential: {secrets[0]}",
                }
            )
        for step in job.get("steps") or []:
            uses = step.get("uses")
            if isinstance(uses, str) and uses.split("@", 1)[0] in declaration.get(
                "external_state_actions", []
            ):
                read_only = False
                findings.append(
                    {
                        "kind": "lane_external_state",
                        "direction": "uncovered",
                        "job": name,
                        "detail": f"a rehearsal lane job uses the external-state action {uses}",
                    }
                )
            _classify_action(
                name,
                step,
                set(declaration.get("infrastructure_actions", [])),
                set(declaration.get("external_state_actions", [])),
                findings,
            )
        strategy = job.get("strategy") or {}
        matrix = strategy.get("matrix") or {}
        candidates: list[Any] = []
        for value in matrix.values():
            if isinstance(value, list):
                candidates.extend(value)
        for candidate in candidates:
            label = candidate.get("runner") if isinstance(candidate, dict) else candidate
            if isinstance(label, str):
                try:
                    platforms.add(runner_platform_family(label))
                except RehearsalError:
                    continue
        runs_on = job.get("runs-on")
        if isinstance(runs_on, str) and "${{" not in runs_on:
            platforms.add(runner_platform_family(runs_on))
    missing = [item for item in required_platforms if item not in platforms]
    if missing:
        findings.append(
            {
                "kind": "missing_platform",
                "direction": "uncovered",
                "detail": f"the rehearsal lane does not declare {', '.join(missing)}",
            }
        )
    return {
        "platforms": sorted(platforms),
        "permissions_read_only": read_only,
        "missing_platforms": missing,
    }


# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------


def human_rehearsal_summary(result: dict[str, Any]) -> str:
    lines = [
        f"Publication rehearsal: {result['state'].upper()}",
        f"Platform: {result['platform']}",
        f"Mode: {result['mode']}",
        f"Candidate: {result['candidate_commit']}",
        f"Verification plan: {result['verification_plan_source'] or 'none'}",
        f"Authority: {result['authority']}",
    ]
    preconditions = result.get("preconditions") or {}
    if preconditions and not preconditions.get("clean_worktree", True):
        lines.append(
            "Inherited checkout: not clean, "
            f"{preconditions['uncommitted_entries']} uncommitted entries"
        )
    conversion = preconditions.get("line_ending_conversion")
    if conversion in {"true", "input"}:
        lines.append(
            f"Inherited checkout: core.autocrlf={conversion}, so the candidate checkout "
            "converts line endings"
        )
    lines.extend(["", "Mechanics:"])
    for item in result["mechanics"]:
        suffix = f" - {item['reason']}" if item["outcome"] != "executed" else ""
        lines.append(f"- {item['outcome']:8} {item['mechanic']}: {item['detail']}{suffix}")
    return "\n".join(lines)


def human_divergence_summary(result: dict[str, Any]) -> str:
    lines = [
        f"Publication rehearsal divergence: {result['verdict'].upper()}",
        f"Orchestrator: {result['orchestrator']}",
        f"Rehearsed jobs: {', '.join(result['rehearsed_jobs'])}"
        f" on {', '.join(result['orchestrator_platforms'])}",
        f"Rehearsal lane platforms: {', '.join(result['lane']['platforms']) or 'none'}",
        f"Authority: {result['authority']}",
        "",
        "Excluded orchestrator jobs:",
    ]
    for item in result["excluded_jobs"]:
        lines.append(f"- {item['job']}: {'; '.join(item['attributes'])}")
    if result["findings"]:
        lines.extend(["", "Divergence:"])
        for item in result["findings"]:
            location = " ".join(
                str(item[key]) for key in ("job", "step", "mechanic", "command") if key in item
            )
            lines.append(f"- {item['direction']:9} {item['kind']} [{location}]: {item['detail']}")
    else:
        lines.extend(["", "No uncovered or stale mechanic."])
    return "\n".join(lines)


def _write(path: Path | None, value: Any) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    rehearse = commands.add_parser(
        "rehearse", help="Run the credential-free publication mechanics on this platform."
    )
    rehearse.add_argument("--repository", type=Path, default=Path("."))
    rehearse.add_argument("--root", type=Path, required=True)
    rehearse.add_argument("--mode", choices=("candidate", "release-record"), default="candidate")
    rehearse.add_argument("--release-record")
    rehearse.add_argument("--declaration", type=Path)
    rehearse.add_argument("--output", type=Path)
    rehearse.add_argument("--summary", type=Path)
    rehearse.add_argument("--default-ref", default=DEFAULT_REF)
    rehearse.add_argument("--keep-root", action="store_true")

    divergence = commands.add_parser(
        "check-divergence", help="Fail closed on an uncovered or stale publication mechanic."
    )
    divergence.add_argument("--repository", type=Path, default=Path("."))
    divergence.add_argument("--declaration", type=Path)
    divergence.add_argument("--output", type=Path)
    divergence.add_argument("--summary", type=Path)
    divergence.add_argument(
        "--cross-check-yaml",
        action="store_true",
        help="Also require PyYAML to agree about the parsed job structure.",
    )
    return parser


def _declaration_path(repository: Path, override: Path | None) -> Path:
    if override is not None:
        return override
    return repository / ".github" / "scripts" / "publication_rehearsal_mechanics.json"


def main(argv: Iterable[str] | None = None) -> int:
    arguments = build_parser().parse_args(list(argv) if argv is not None else None)
    repository = Path(arguments.repository)
    try:
        declaration = load_declaration(_declaration_path(repository, arguments.declaration))
        if arguments.command == "rehearse":
            if arguments.mode == "release-record" and not arguments.release_record:
                raise RehearsalError("release-record mode requires --release-record")
            if arguments.mode == "candidate" and arguments.release_record:
                raise RehearsalError("candidate mode takes no --release-record")
            root = Path(arguments.root)
            root.mkdir(parents=True, exist_ok=True)
            rehearsal = Rehearsal(
                repository,
                root,
                mode=arguments.mode,
                release_record=arguments.release_record,
                declaration=declaration,
                keep_root=arguments.keep_root,
                default_ref=arguments.default_ref,
            )
            result = rehearsal.run()
            _write(arguments.output, result)
            summary = human_rehearsal_summary(result)
            failing = result["state"] != "rehearsed"
        else:
            result = check_divergence(
                repository, declaration, cross_check=arguments.cross_check_yaml
            )
            _write(arguments.output, result)
            summary = human_divergence_summary(result)
            failing = result["verdict"] != "exact"
    except RehearsalError as exc:
        print(f"publication rehearsal: {exc}", file=sys.stderr)
        return 1
    print(summary)
    if arguments.summary is not None:
        with arguments.summary.open("a", encoding="utf-8") as handle:
            handle.write(summary + "\n")
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
