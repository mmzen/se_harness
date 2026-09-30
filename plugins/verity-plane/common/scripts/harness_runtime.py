"""Private locators shared by setup, activation and native instruction delivery.

These records select inputs, never lifecycle authority. Policy is obtained from
the selected evaluator; this module contains no policy or resource catalogue.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import tomllib


class DeliveryError(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise DeliveryError("duplicate JSON field in the delivery inputs")
        result[name] = value
    return result


def safe_path(path: Path) -> Path:
    if ".." in path.parts:
        raise DeliveryError("parent traversal is not supported in a selected path")
    path = Path(os.path.abspath(path))
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise DeliveryError(f"linked input is not supported: {item}")
    return path


def read_regular(path: Path, limit: int) -> bytes:
    path = safe_path(path)
    if not path.is_file():
        raise DeliveryError(f"required regular file is unavailable: {path.name}")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise DeliveryError(f"input exceeds the delivery size limit: {path.name}")
    return raw


def private_data(host: str, explicit: Path | None = None, repository: Path | None = None) -> Path:
    value = explicit
    if value is None:
        names = ("PLUGIN_DATA", "CLAUDE_PLUGIN_DATA") if host == "codex" else ("CLAUDE_PLUGIN_DATA",)
        values = {os.environ[name] for name in names if os.environ.get(name)}
        if len(values) != 1:
            raise DeliveryError("the host must supply one unambiguous persistent plugin data directory")
        value = Path(values.pop())
    if not value.is_absolute():
        raise DeliveryError("the plugin data directory must be absolute")
    path = safe_path(value)
    package = Path(__file__).resolve().parents[1]
    if path.is_relative_to(package) or (repository is not None and path.is_relative_to(repository)):
        raise DeliveryError("select private plugin data outside the repository and plugin package")
    return path


def session_file(host: str, session: object, data: Path) -> Path:
    if host not in {"codex", "claude"} or not isinstance(session, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,200}", session):
        raise DeliveryError("a valid host-supplied session_id is required; do not infer it from a transcript")
    key = hashlib.sha256(session.encode()).hexdigest()
    return safe_path(data / "sessions" / host / (key + ".json"))


def read_selection(path: Path, host: str, session: str) -> tuple[Path | None, bytes | None]:
    if path.with_suffix(".lock").exists():
        raise DeliveryError("session selection is being changed; retry after activation completes")
    if not path.exists():
        return None, None
    raw = read_regular(path, 16384)
    value = json.loads(raw, object_pairs_hook=unique_object)
    if (not isinstance(value, dict) or set(value) != {"schema", "host", "session_id", "repository"}
            or value.get("schema") != "se-harness-session-v1" or value.get("host") != host
            or value.get("session_id") != session or not isinstance(value.get("repository"), str)):
        raise DeliveryError("invalid saved session selection; explicitly activate or clear this session")
    root = exact_repository(value["repository"])
    return root, raw


def unchanged_selection(path: Path, expected: bytes | None) -> None:
    if path.with_suffix(".lock").exists():
        raise DeliveryError("session selection changed during delivery")
    current = read_regular(path, 16384) if path.exists() else None
    if current != expected:
        raise DeliveryError("session selection changed during delivery")


@contextmanager
def exclusive(path: Path):
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise DeliveryError(f"another operation owns {path.name}; inspect an interrupted operation before retrying") from exc
    try:
        os.close(descriptor)
        yield
    finally:
        path.unlink()


def atomic_json(path: Path, value: dict) -> None:
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=True, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def exact_repository(value: object) -> Path:
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise DeliveryError("an unambiguous absolute checkout path is required")
    path = Path(value)
    if not path.is_absolute():
        raise DeliveryError("the checkout path must be absolute")
    path = safe_path(path)
    if not path.is_dir():
        raise DeliveryError("the selected checkout is unavailable")
    return path


def selected_repository(cwd: object) -> Path | None:
    current = exact_repository(cwd)
    for directory in (current, *current.parents):
        config, lock = directory / ".engineering-harness.toml", directory / ".engineering-harness.lock"
        if config.exists() or lock.exists() or config.is_symlink() or lock.is_symlink():
            return directory
        if (directory / ".git").exists():
            break
    return None


def release_selection(root: Path) -> tuple[dict, dict, dict[str, bytes]]:
    inputs = {name: read_regular(root / name, 1024 * 1024)
              for name in (".engineering-harness.toml", ".engineering-harness.lock")}
    config = tomllib.loads(inputs[".engineering-harness.toml"].decode("utf-8"))
    lock = json.loads(inputs[".engineering-harness.lock"], object_pairs_hook=unique_object)
    harness = config.get("harness", {})
    version = harness.get("tool_version")
    if (not isinstance(version, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version)
            or not isinstance(lock, dict) or type(lock.get("schema")) is not int or lock["schema"] not in {3, 4, 5}
            or lock.get("tool_version") != version or lock.get("evaluator", {}).get("version") != version):
        raise DeliveryError("configuration and installation record do not select the same supported release")
    layout = harness.get("resource_layout")
    if layout != lock.get("resource_layout") or (lock["schema"] == 5) != (layout == "released-resources-v1"):
        raise DeliveryError("configuration and installation record select an unsupported resource layout")
    return config, lock, inputs


def environment_path(data: Path, identity: dict) -> Path:
    version = identity.get("version")
    digest = identity.get("archive_sha256") or identity.get("payload_sha256")
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise DeliveryError("invalid selected evaluator version")
    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise DeliveryError("the selected evaluator has no valid immutable digest")
    return safe_path(data / "evaluators" / version / digest)


def python_path(environment: Path) -> Path:
    return safe_path(environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python"))


def query_identity(python: Path) -> dict:
    code = "import json; from se_harness.evaluator_identity import installed_evaluator_identity; print(json.dumps(installed_evaluator_identity().to_lock()))"
    result = subprocess.run([str(python), "-I", "-c", code], cwd=python.parent,
                            capture_output=True, text=True, encoding="utf-8", timeout=7)
    if result.returncode:
        raise DeliveryError("the private evaluator cannot validate its installed identity")
    return json.loads(result.stdout, object_pairs_hook=unique_object)


def match_identity(expected: dict, actual: dict) -> None:
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        raise DeliveryError("invalid evaluator identity record")
    for key in ("version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"):
        if expected.get(key) is not None and actual.get(key) != expected[key]:
            raise DeliveryError(f"the private evaluator does not match selected {key}")


def installed_python(data: Path, identity: dict) -> Path:
    environment = environment_path(data, identity)
    ready = json.loads(read_regular(environment / "ready.json", 16384), object_pairs_hook=unique_object)
    match_identity(identity, ready)
    python = python_path(environment)
    if not python.is_file():
        raise DeliveryError("the selected evaluator is unavailable; use setup then activate again")
    return python
