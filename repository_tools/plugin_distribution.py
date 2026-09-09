"""Assemble inert native plugin archives from committed, explicitly selected inputs.

This repository-owned builder does not import candidate evaluator code, install
anything, authenticate a release owner, or establish host support. The caller
selects a trusted released record and an independently obtained wheel digest.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import tomllib
import zipfile

SCHEMA = "se-harness-plugin-assembly-v1"
INVENTORY = "assembly-inventory.json"
HOSTS = {"codex": ".codex-plugin/plugin.json", "claude": ".claude-plugin/plugin.json"}
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
MAX_FILES = 2000
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".yaml", ".yml", ".sh", ".ps1", ".txt", ".svg"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".ico"}


class AssemblyError(ValueError):
    """Input or output cannot be accepted as a complete assembly."""


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode()


def _object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssemblyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _json(raw: bytes) -> dict:
    try:
        value = json.loads(raw, object_pairs_hook=_object)
    except (ValueError, UnicodeError) as exc:
        raise AssemblyError(f"invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AssemblyError("expected a JSON object")
    return value


def _path(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 240:
        raise AssemblyError(f"unsafe path: {value!r}")
    for part in value.split("/"):
        if (not re.fullmatch(r"[A-Za-z0-9_. -]+", part) or part in {".", ".."}
                or part != part.strip() or part.endswith(".")
                or re.fullmatch(r"(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?", part)):
            raise AssemblyError(f"unsafe path: {value!r}")
    return value


def _git(repository: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repository), *args], capture_output=True, timeout=30)
    if result.returncode:
        raise AssemblyError(f"Git input unavailable: {' '.join(args)}")
    return result.stdout


def _revision(repository: Path, revision: str) -> str:
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision):
        raise AssemblyError("source and release revisions must be full immutable commit IDs")
    if _git(repository, "rev-parse", "--verify", revision + "^{commit}").decode().strip() != revision:
        raise AssemblyError("revision is not the selected commit")
    return revision


def _blob(repository: Path, revision: str, path: str) -> tuple[bytes, int]:
    _path(path)
    entries = _git(repository, "ls-tree", "-z", revision, "--", path).split(b"\0")
    if len(entries) != 2 or not entries[0]:
        raise AssemblyError(f"missing committed source: {path}")
    metadata, actual = entries[0].split(b"\t", 1)
    mode, kind, oid = metadata.decode().split()
    if actual.decode() != path or kind != "blob" or mode not in {"100644", "100755"}:
        raise AssemblyError(f"source must be a regular committed file: {path}")
    size = int(_git(repository, "cat-file", "-s", oid))
    if size > MAX_FILE:
        raise AssemblyError(f"source exceeds size limit: {path}")
    return _git(repository, "cat-file", "blob", oid), int(mode, 8) & 0o777


def _asset(path: str, raw: bytes, host: str | None) -> None:
    _path(path)
    prefix = path.split("/")[0]
    allowed = {"skills", "scripts", "agents", "assets", "hooks"}
    if host:
        allowed.add(HOSTS[host].split("/")[0])
    if prefix not in allowed and path not in {"README.md", "LICENSE", "LICENSE.txt", ".mcp.json", ".app.json"}:
        raise AssemblyError(f"forbidden payload destination: {path}")
    parts = {part.lower() for part in path.split("/")}
    if parts & {"bin", "python", "python3", "runtime", "site-packages", "__pycache__", "node_modules", ".venv"}:
        raise AssemblyError(f"forbidden runtime or dependency: {path}")
    suffix = Path(path).suffix.lower()
    if suffix not in TEXT_SUFFIXES | IMAGE_SUFFIXES and path != "LICENSE":
        raise AssemblyError(f"unsupported payload type: {path}")
    if raw.startswith((b"MZ", b"\x7fELF", b"PK\x03\x04", b"\x1f\x8b", b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf")):
        raise AssemblyError(f"executable or dependency archive: {path}")
    if suffix in TEXT_SUFFIXES or path == "LICENSE":
        try:
            text = raw.decode("utf8")
        except UnicodeError as exc:
            raise AssemblyError(f"non-text payload: {path}") from exc
        if "\0" in text:
            raise AssemblyError(f"binary payload: {path}")


def _payload_hash(python: Path, repository: Path, wheel_bytes: bytes, name: str, version: str) -> str:
    if not python.is_absolute() or not python.is_file() or python.resolve().is_relative_to(repository.resolve()):
        raise AssemblyError("select an absolute released-evaluator Python outside the source repository")
    # Hash the already verified bytes in a private temporary file. Never import
    # the wheel, install it, or let a concurrent wheel edit change the input.
    code = ("from pathlib import Path; import sys; "
            "from se_harness.evaluator_identity import wheel_payload_sha256; "
            "print(wheel_payload_sha256(Path(sys.argv[1]), sys.argv[2]))")
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    with tempfile.TemporaryDirectory(prefix="plugin-wheel-") as temporary:
        selected = Path(temporary) / name
        selected.write_bytes(wheel_bytes)
        run = subprocess.run([str(python), "-I", "-c", code, str(selected), version],
                             cwd=temporary, env=env, capture_output=True, timeout=30)
    value = run.stdout.decode("ascii", errors="replace").strip()
    if run.returncode or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise AssemblyError("released evaluator could not compute canonical wheel payload SHA-256")
    return value


@dataclass
class Assembly:
    name: str
    source: dict
    evaluator: dict
    files: dict[str, dict[str, tuple[bytes, int, str]]]

    def inventory(self, host: str) -> dict:
        return {"schema": SCHEMA, "host": host, "plugin": self.name,
                "source": self.source, "evaluator": self.evaluator,
                "files": {path: {"sha256": digest(raw), "bytes": len(raw), "mode": mode, "origin": origin}
                          for path, (raw, mode, origin) in self.files[host].items()}}


def prepare(repository: Path, revision: str, plan_path: str, release_revision: str,
            release_record: str, expected_wheel_sha256: str, wheel: Path,
            evaluator_python: Path) -> Assembly:
    """Resolve all inputs and policy checks before any output directory is created."""
    repository = repository.resolve(strict=True)
    revision = _revision(repository, revision)
    release_revision = _revision(repository, release_revision)
    if not re.fullmatch(r"[0-9a-f]{64}", expected_wheel_sha256):
        raise AssemblyError("expected wheel SHA-256 must be independently supplied")
    record_raw, _ = _blob(repository, release_revision, release_record)
    try:
        record = tomllib.loads(record_raw.decode().split("+++", 2)[1])
        version = record["version"]
        distribution = record["distribution"]
        if not isinstance(distribution, dict):
            raise ValueError("distribution must be a table")
    except (ValueError, KeyError, IndexError, UnicodeError) as exc:
        raise AssemblyError("invalid released evaluator record") from exc
    if record.get("type") != "release_record" or record.get("status") != "released":
        raise AssemblyError("selected evaluator record is not released")
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise AssemblyError("select a stable published evaluator version")
    name = f"se_harness-{version}-py3-none-any.whl"
    if distribution.get("wheel") != name or distribution.get("wheel_sha256") != expected_wheel_sha256:
        raise AssemblyError("released wheel identity disagrees with independently expected archive")
    if wheel.name != name or not wheel.is_file() or wheel.is_symlink() or wheel.stat().st_size > MAX_FILE:
        raise AssemblyError(f"missing or invalid released wheel: {wheel.name}")
    wheel_bytes = wheel.read_bytes()
    if digest(wheel_bytes) != expected_wheel_sha256:
        raise AssemblyError(f"released wheel SHA-256 mismatch: {wheel.name}")
    payload = _payload_hash(evaluator_python, repository, wheel_bytes, name, version)
    with zipfile.ZipFile(io.BytesIO(wheel_bytes)) as archive:
        metadata = archive.read(f"se_harness-{version}.dist-info/METADATA").decode()
        if f"\nVersion: {version}\n" not in "\n" + metadata or "\nName: se-harness\n" not in "\n" + metadata:
            raise AssemblyError("wheel metadata disagrees with selected release")
    plan_raw, _ = _blob(repository, revision, plan_path)
    plan = _json(plan_raw)
    if set(plan) != {"schema", "name", "shared", "hosts"} or plan["schema"] != SCHEMA:
        raise AssemblyError("invalid assembly plan schema or fields")
    if not isinstance(plan["name"], str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", plan["name"]):
        raise AssemblyError("invalid plugin name")
    if not isinstance(plan["hosts"], dict) or set(plan["hosts"]) != set(HOSTS):
        raise AssemblyError("plan must select exactly Codex and Claude integration files")
    if not isinstance(plan["shared"], dict) or not plan["shared"]:
        raise AssemblyError("plan must inventory nonempty shared assets")
    files = {}
    total = 0
    for host in HOSTS:
        mapping = plan["hosts"][host]
        if not isinstance(mapping, dict) or HOSTS[host] not in mapping:
            raise AssemblyError(f"missing {host} manifest")
        entries = {}
        folded = set()
        for origin, mapping in [("shared", plan["shared"]), (host, mapping)]:
            for destination, source in mapping.items():
                _path(destination)
                _path(source)
                key = destination.lower()
                if any(key == old or key.startswith(old + "/") or old.startswith(key + "/") for old in folded):
                    raise AssemblyError(f"conflicting output path: {destination}")
                folded.add(key)
                raw, mode = _blob(repository, revision, source)
                _asset(destination, raw, None if origin == "shared" else host)
                total += len(raw)
                entries[destination] = (raw, mode, origin)
        manifest = _json(entries[HOSTS[host]][0])
        if manifest.get("name") != plan["name"]:
            raise AssemblyError(f"{host} manifest name differs from plugin directory")
        entries[f"packages/{name}"] = (wheel_bytes, 0o644, "evaluator")
        if len(entries) > MAX_FILES or total > MAX_TOTAL:
            raise AssemblyError("assembly input exceeds file or byte limit")
        files[host] = dict(sorted(entries.items()))
    return Assembly(plan["name"], {"revision": revision, "plan": plan_path, "plan_sha256": digest(plan_raw)},
                    {"version": version, "archive": name, "archive_sha256": expected_wheel_sha256,
                     "payload_sha256": payload, "release_revision": release_revision,
                     "release_record": release_record, "release_record_sha256": digest(record_raw)}, files)


def _safe_directory(path: Path) -> None:
    for part in (path, *path.parents):
        try:
            attributes = getattr(part.lstat(), "st_file_attributes", 0)
        except FileNotFoundError:
            continue
        # FILE_ATTRIBUTE_REPARSE_POINT also covers junctions on Python 3.11,
        # where Path.is_junction is not available.
        if part.is_symlink() or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise AssemblyError(f"linked output destination: {part}")


def _write(path: Path, raw: bytes) -> None:
    _safe_directory(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def _archive(assembly: Assembly, host: str) -> bytes:
    entries = {path: (raw, mode) for path, (raw, mode, _) in assembly.files[host].items()}
    entries[INVENTORY] = (json_bytes(assembly.inventory(host)), 0o644)
    result = io.BytesIO()
    with zipfile.ZipFile(result, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, (raw, mode) in sorted(entries.items()):
            info = zipfile.ZipInfo(f"{assembly.name}/{path}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, raw)
    return result.getvalue()


def accept(assembly: Assembly, output: Path) -> dict:
    """Compare disk and ZIP contents with committed sources, not inventory claims."""
    _safe_directory(output)
    expected = {}
    for host in HOSTS:
        prefix = f"{host}/{assembly.name}/"
        for path, (raw, _mode, _origin) in assembly.files[host].items():
            expected[prefix + path] = raw
        expected[prefix + INVENTORY] = json_bytes(assembly.inventory(host))
        expected[f"{assembly.name}-{host}.zip"] = _archive(assembly, host)
    actual = set()
    for directory, dirs, names in os.walk(output, followlinks=False):
        for name in dirs + names:
            path = Path(directory) / name
            _safe_directory(path)
            if path.is_file():
                if path.stat().st_nlink != 1:
                    raise AssemblyError(f"hard-linked output: {path.relative_to(output)}")
                actual.add(path.relative_to(output).as_posix())
            elif not path.is_dir():
                raise AssemblyError(f"non-regular output: {path.relative_to(output)}")
    if actual != set(expected):
        raise AssemblyError(f"incomplete or extra output files: {sorted(actual ^ set(expected))}")
    for path, raw in expected.items():
        selected = output / path
        if path.endswith("/" + INVENTORY) and selected.stat().st_size <= MAX_FILE:
            inventory = _json(selected.read_bytes())
            listed = inventory.get("files")
            wanted = _json(raw)["files"]
            if not isinstance(listed, dict):
                raise AssemblyError(f"invalid file inventory: {path}")
            missing = sorted(set(wanted) - set(listed))
            extra = sorted(set(listed) - set(wanted))
            if missing or extra:
                raise AssemblyError(f"inventory {path}: missing entries {missing}; extra entries {extra}")
        if selected.stat().st_size != len(raw) or selected.read_bytes() != raw:
            raise AssemblyError(f"output differs from committed source/inventory: {path}")
    return {"schema": SCHEMA, "accepted": True, "source": assembly.source, "evaluator": assembly.evaluator,
            "archives": {f"{assembly.name}-{host}.zip": digest(expected[f"{assembly.name}-{host}.zip"]) for host in HOSTS},
            "claim": "Package contents only; no host support, release or publication decision."}


def build(assembly: Assembly, output: Path) -> dict:
    """Write only a new directory. Keep interrupted output for inspection; retry elsewhere."""
    _safe_directory(output)
    if output.exists():
        raise AssemblyError("output already exists; inspect it or retry in a fresh directory")
    output.mkdir(parents=True)
    for host in HOSTS:
        directory = output / host / assembly.name
        for path, (raw, mode, _) in assembly.files[host].items():
            _write(directory / path, raw)
            (directory / path).chmod(mode)
    # Inventories and archives come after both copies; a partial directory is
    # never accepted merely because it happens to contain a manifest.
    for host in HOSTS:
        _write(output / host / assembly.name / INVENTORY, json_bytes(assembly.inventory(host)))
        _write(output / f"{assembly.name}-{host}.zip", _archive(assembly, host))
    return accept(assembly, output)
