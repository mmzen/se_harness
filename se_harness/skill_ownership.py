"""Explicit, data-only retained-skill ownership and recoverable transactions.

The committed lock contains portable selected identities, never installation roots.
Local paths and complete input hashes belong to a reviewed plan. Nothing here loads
or executes plugin code. Installer imports are deliberately local: the installer,
lock parser, doctor, and mutation guard all consume this module's one catalog.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Iterable

from se_harness.integrity import (
    IntegrityError, atomic_write_bytes, canonical_json_bytes, canonical_sha256,
    canonical_text_bytes, pretty_json_bytes, raw_sha256, stage_bytes, unique_object_hook,
)


class OwnershipError(IntegrityError):
    """An ownership input or transaction cannot be safely accepted."""


_CONTRACT = json.loads(Path(__file__).with_name("skill_ownership_contract.json").read_text(encoding="utf-8"))
BINDING_SCHEMA = _CONTRACT["binding_schema"]
OWNERSHIP_SCHEMA = _CONTRACT["ownership_schema"]
ASSEMBLY_SCHEMA = _CONTRACT["assembly_schema"]
CATALOG = frozenset(_CONTRACT["catalog"])
DISCOVERY_PATHS = CATALOG | {".claude/skills/harness-operator-brief/SKILL.md"}
HOSTS = _CONTRACT["hosts"]
MAX_CONTROL = _CONTRACT["limits"]["control_bytes"]
MAX_FILES = _CONTRACT["limits"]["files"]
MAX_FILE = _CONTRACT["limits"]["file_bytes"]
MAX_TOTAL = _CONTRACT["limits"]["total_bytes"]
LOCK_NAME = ".engineering-harness.lock"
RECOVERY_NAME = ".engineering-harness.skill-ownership.pending.json"
MUTEX_NAME = ".engineering-harness.skill-ownership.mutex"
RECOVERY_SCHEMA = "se-harness-skill-ownership-recovery-v1"
_HASH = re.compile(r"[0-9a-f]{64}")
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
_NAME = re.compile(r"[a-z][a-z0-9-]{0,63}")
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_unique = unique_object_hook(lambda key: OwnershipError(f"duplicate JSON key: {key}"))


def _fault_hook(stage: str, path: str | None = None) -> None:
    """No-op injection boundary used by independent exception/crash tests."""


def catalog_paths() -> frozenset[str]:
    return CATALOG


def _json(raw: bytes, *, limit: int = MAX_CONTROL) -> dict:
    if not raw or len(raw) > limit:
        raise OwnershipError("control document exceeds its size bound or is empty")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise OwnershipError(f"invalid ownership JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise OwnershipError("ownership document must be an object")
    return value


def _fields(value: Any, fields: Iterable[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != set(fields):
        raise OwnershipError(f"invalid {label} field set")
    return value


def _hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        raise OwnershipError(f"invalid SHA-256: {label}")
    return value


def _relative(value: Any) -> str:
    if not isinstance(value, str) or not value or len(value) > 240:
        raise OwnershipError("unsafe inventory path")
    for part in value.split("/"):
        if (not re.fullmatch(r"[A-Za-z0-9_. -]+", part) or part in {".", ".."}
                or part != part.strip() or part.endswith(".")
                or re.fullmatch(r"(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?", part)):
            raise OwnershipError(f"unsafe inventory path: {value}")
    return value


def _ordinary(path: Path, *, directory: bool = False, missing: bool = False) -> os.stat_result | None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        if missing:
            return None
        raise OwnershipError(f"missing required path: {path}") from None
    except OSError as exc:
        raise OwnershipError(f"cannot inspect path: {path}: {exc}") from exc
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & _REPARSE:
        raise OwnershipError(f"linked or reparse path is forbidden: {path}")
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise OwnershipError(f"ordinary directory required: {path}")
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise OwnershipError(f"ordinary, singly linked file required: {path}")
    return info


def _root(value: Path | str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    # Do not resolve links before checking each ancestor.
    candidate = Path(os.path.abspath(candidate))
    for ancestor in reversed((candidate, *candidate.parents)):
        _ordinary(ancestor, directory=True)
    return candidate


def _destination(root: Path, relative: str, *, missing: bool = False) -> Path:
    _relative(relative)
    probe = root
    for index, part in enumerate(relative.split("/")):
        if probe.exists():
            _ordinary(probe, directory=True)
            try:
                collisions = [entry.name for entry in probe.iterdir() if entry.name.casefold() == part.casefold()]
            except OSError as exc:
                raise OwnershipError(f"cannot enumerate path parent: {probe}") from exc
            if collisions and collisions != [part]:
                raise OwnershipError(f"case-colliding path: {relative}")
        probe = probe / part
        final = index == len(relative.split("/")) - 1
        if final:
            _ordinary(probe, missing=missing)
        elif probe.exists() or probe.is_symlink():
            _ordinary(probe, directory=True)
        elif not missing:
            raise OwnershipError(f"missing parent directory: {relative}")
    return probe


def _read(path: Path, *, limit: int = MAX_FILE) -> bytes:
    before = _ordinary(path)
    if before.st_size > limit:
        raise OwnershipError(f"file exceeds size bound: {path}")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino) or opened.st_nlink != 1:
                raise OwnershipError(f"path changed while opening: {path}")
            chunks = []
            remaining = limit + 1
            while remaining:
                chunk = handle.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            after = os.fstat(handle.fileno())
        current = _ordinary(path)
    except OSError as exc:
        raise OwnershipError(f"cannot read input: {path}: {exc}") from exc
    if len(raw) > limit or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) or (
            current.st_dev, current.st_ino) != (before.st_dev, before.st_ino):
        raise OwnershipError(f"input changed during read: {path}")
    return raw


def _template_catalog(templates: Iterable[Any] | None = None) -> dict[str, bytes]:
    if templates is None:
        from se_harness.installer import template_files
        templates = template_files()
    items = {item.target.as_posix(): item for item in templates if item.target.as_posix() in CATALOG}
    if set(items) != CATALOG or any(item.mode != "managed" for item in items.values()):
        raise OwnershipError("selected evaluator has an incompatible retained-skill catalog")
    return {path: canonical_text_bytes(_read(item.source)) for path, item in sorted(items.items())}


def _retained_paths() -> frozenset[str]:
    return frozenset(path.removeprefix(".agents/") for path in CATALOG if path.startswith(".agents/"))


def _expected(value: Any) -> dict:
    selected = _fields(value, _CONTRACT["expected_fields"], "expected plugin identity")
    if not isinstance(selected["plugin"], str) or _NAME.fullmatch(selected["plugin"]) is None:
        raise OwnershipError("invalid expected plugin name")
    if not isinstance(selected["version"], str) or _VERSION.fullmatch(selected["version"]) is None:
        raise OwnershipError("invalid expected plugin version")
    _hash(selected["inventory_sha256"], "assembly inventory")
    retained = _fields(selected["retained_files"], _retained_paths(), "retained file inventory")
    for path, digest in retained.items():
        _hash(digest, path)
    return selected


def validate_ownership_binding(value: Any, *, templates: Iterable[Any] | None = None) -> dict:
    """Validate a portable lock binding and its selected evaluator compatibility."""
    binding = _fields(value, _CONTRACT["ownership_fields"], "skill ownership")
    if binding["schema"] != OWNERSHIP_SCHEMA or binding["provider"] != "plugin":
        raise OwnershipError("unsupported skill ownership schema or provider")
    _hash(binding["binding_sha256"], "portable binding")
    if binding["binding_sha256"] != _digest({key: item for key, item in binding.items() if key != "binding_sha256"}):
        raise OwnershipError("portable ownership binding consistency digest mismatch")
    catalog = _fields(binding["catalog"], CATALOG, "ownership catalog")
    expected_catalog = {path: canonical_sha256(raw) for path, raw in _template_catalog(templates).items()}
    if catalog != expected_catalog:
        raise OwnershipError("plugin ownership catalog is incompatible with the selected evaluator")
    hosts = binding["hosts"]
    if not isinstance(hosts, dict) or not hosts or not set(hosts) <= set(HOSTS):
        raise OwnershipError("select at least one supported plugin host")
    for selected in hosts.values():
        _expected(selected)
    return binding


def effective_templates(templates: Iterable[Any], lock: dict) -> list[Any]:
    items = list(templates)
    if lock.get("schema") == 4:
        validate_ownership_binding(lock.get("skill_ownership"), templates=items)
        return [item for item in items if item.target.as_posix() not in CATALOG]
    if "skill_ownership" in lock:
        raise OwnershipError("repository-owned lock must not contain a plugin binding")
    return items


def _skill_tree(root: Path) -> dict[str, str]:
    """Inventory only the selected discovery directories, never unrelated skills."""
    found: dict[str, str] = {}
    bases = {str(Path(path).parent.as_posix()).split("/scripts")[0] for path in CATALOG}
    # Also reject unexpected same-name Claude briefing/Codex metadata copies.
    bases.add(".claude/skills/harness-operator-brief")
    for base in sorted(bases):
        _destination(root, base + "/.ownership-path-check", missing=True)
        parent, name = base.rsplit("/", 1)
        parent_path = root / parent
        if not parent_path.exists():
            continue
        _ordinary(parent_path, directory=True)
        matches = [entry.name for entry in parent_path.iterdir() if entry.name.casefold() == name.casefold()]
        if not matches:
            continue
        if matches != [name]:
            raise OwnershipError(f"case-colliding retained skill: {base}")
        directory = root / base
        _ordinary(directory, directory=True)
        stack = [directory]
        while stack:
            selected = stack.pop()
            entries = list(selected.iterdir())
            folds = [entry.name.casefold() for entry in entries]
            if len(set(folds)) != len(folds):
                raise OwnershipError(f"case collision in retained skill: {selected}")
            for entry in entries:
                relative = entry.relative_to(root).as_posix()
                _relative(relative)
                info = entry.lstat()
                if stat.S_ISDIR(info.st_mode):
                    _ordinary(entry, directory=True)
                    stack.append(entry)
                else:
                    _ordinary(entry)
                    found[relative] = raw_sha256(_read(entry))
                if len(found) > MAX_FILES:
                    raise OwnershipError("retained-skill inventory exceeds file bound")
    return dict(sorted(found.items()))


def assert_ownership_state(target: Path, lock: dict, *, templates: Iterable[Any] | None = None) -> None:
    """Prove declared ownership without replacing default installer integrity rules.

    Existing repository-owned roots may precede the Claude adapter. Their six
    canonical core entries distinguish them from a stripped plugin-owned lock;
    Default planning, repair, and doctor retain their existing file classification;
    migration separately requires the complete current seven-file distribution.
    """
    if lock.get("schema") == 4:
        validate_ownership_binding(lock.get("skill_ownership"), templates=templates)
        if set(lock.get("files", {})) & CATALOG:
            raise OwnershipError("plugin-owned catalog remains in repository lock files")
        if set(_skill_tree(_root(target))) & DISCOVERY_PATHS:
            raise OwnershipError("unexpected repository copy of a plugin-owned retained skill")
    elif "skill_ownership" in lock:
        raise OwnershipError("plugin binding is forbidden in a repository-owned lock")
    elif lock.get("schema") == 3 and lock.get("tool_version") is not None:
        version = re.match(r"^(\d+)\.(\d+)\.(\d+)", str(lock["tool_version"]))
        if version and tuple(map(int, version.groups())) >= (0, 17, 0):
            root = _root(target)
            required_core = {path for path in CATALOG if path.startswith(".agents/")}
            for path in required_core:
                entry = lock.get("files", {}).get(path)
                if not isinstance(entry, dict) or entry.get("mode") != "managed":
                    raise OwnershipError(f"repository-owned lock is missing retained catalog entry: {path}")
            observed = set(_skill_tree(root))
            if observed & (DISCOVERY_PATHS - CATALOG):
                raise OwnershipError("unexpected retained-skill discovery shadow")


def ensure_no_pending_recovery(target: Path) -> None:
    path = Path(target) / RECOVERY_NAME
    if path.exists() or path.is_symlink():
        raise OwnershipError("pending skill-ownership recovery blocks mutation; review a skill-ownership recovery plan")


def _inspect_plugin(root: Path, host: str, expected: dict, evaluator: dict, catalog: dict[str, bytes]) -> dict:
    inventory_raw = _read(_destination(root, "assembly-inventory.json"), limit=MAX_CONTROL)
    if raw_sha256(inventory_raw) != expected["inventory_sha256"]:
        raise OwnershipError(f"{host} assembly inventory differs from independently expected SHA-256")
    inventory = _fields(_json(inventory_raw), _CONTRACT["inventory_fields"], "assembly inventory")
    if inventory["schema"] != ASSEMBLY_SCHEMA or inventory["host"] != host or inventory["plugin"] != expected["plugin"]:
        raise OwnershipError(f"{host} assembly identity mismatch")
    source = _fields(inventory["source"], {"revision", "plan", "plan_sha256"}, "assembly source")
    if not isinstance(source["revision"], str) or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", source["revision"]) is None:
        raise OwnershipError("invalid assembly source revision")
    _relative(source["plan"])
    _hash(source["plan_sha256"], "assembly plan")
    identity = _fields(inventory["evaluator"], {"version", "archive", "archive_sha256", "payload_sha256", "release_revision", "release_record", "release_record_sha256"}, "assembly evaluator")
    if identity["version"] != evaluator.get("version") or identity["payload_sha256"] != evaluator.get("payload_sha256"):
        raise OwnershipError("plugin evaluator identity is incompatible with repository evaluator")
    _hash(identity["archive_sha256"], "evaluator archive")
    _hash(identity["payload_sha256"], "evaluator payload")
    _hash(identity["release_record_sha256"], "release record")
    if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", str(identity["release_revision"])) is None:
        raise OwnershipError("invalid release revision")
    _relative(identity["release_record"])
    archive = f"se_harness-{str(identity['version']).replace('-', '_')}-py3-none-any.whl"
    if identity["archive"] != archive or (evaluator.get("archive_sha256") is not None and (
            identity["archive_sha256"] != evaluator["archive_sha256"] or archive != evaluator.get("archive_name"))):
        raise OwnershipError("plugin evaluator archive identity mismatch")
    files = inventory["files"]
    if not isinstance(files, dict) or not files or len(files) > MAX_FILES:
        raise OwnershipError("assembly file inventory exceeds its bound or is empty")
    folded: set[str] = set()
    total = 0
    raw_files: dict[str, bytes] = {}
    for path, entry in files.items():
        _relative(path)
        fold = path.casefold()
        if any(fold == old or fold.startswith(old + "/") or old.startswith(fold + "/") for old in folded):
            raise OwnershipError("colliding assembly inventory paths")
        folded.add(fold)
        _fields(entry, _CONTRACT["inventory_file_fields"], "assembly file")
        _hash(entry["sha256"], path)
        if type(entry["bytes"]) is not int or not 0 <= entry["bytes"] <= MAX_FILE:
            raise OwnershipError("assembly file size exceeds its bound")
        if type(entry["mode"]) is not int or entry["mode"] not in {0o644, 0o755} or not isinstance(entry["origin"], str) or entry["origin"] not in {"shared", host, "evaluator"}:
            raise OwnershipError("invalid assembly mode or origin")
        total += entry["bytes"]
        if total > MAX_TOTAL:
            raise OwnershipError("assembly aggregate payload exceeds its bound")
        raw = _read(_destination(root, path))
        if len(raw) != entry["bytes"] or raw_sha256(raw) != entry["sha256"]:
            raise OwnershipError(f"assembly payload mismatch: {path}")
        raw_files[path] = raw
    observed: set[str] = set()
    stack = [root]
    visited = 0
    while stack:
        directory = stack.pop()
        names: set[str] = set()
        for path in directory.iterdir():
            visited += 1
            if visited > MAX_FILES * 2 + 1:
                raise OwnershipError("external package directory inventory exceeds its bound")
            relative = path.relative_to(root).as_posix()
            _relative(relative)
            if path.name.casefold() in names:
                raise OwnershipError("case collision in external package")
            names.add(path.name.casefold())
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                _ordinary(path, directory=True)
                stack.append(path)
            else:
                _ordinary(path)
                observed.add(relative)
            if len(observed) + len(stack) > MAX_FILES + 1:
                raise OwnershipError("external package exceeds inventory bound")
    if observed != set(files) | {"assembly-inventory.json"}:
        raise OwnershipError("external package contains missing or unlisted files")
    manifest = _json(raw_files.get(HOSTS[host], b""))
    if manifest.get("name") != expected["plugin"] or manifest.get("version") != expected["version"]:
        raise OwnershipError("native manifest name or version differs from expected identity")
    if raw_sha256(raw_files.get("packages/" + archive, b"")) != identity["archive_sha256"]:
        raise OwnershipError("bundled evaluator payload is missing or mismatched")
    for path, digest in expected["retained_files"].items():
        raw = raw_files.get(path)
        if raw is None or raw_sha256(raw) != digest:
            raise OwnershipError(f"retained plugin file mismatch: {path}")
        # Path-adapted SKILL.md is independently selected. Contracts and executable
        # helpers must still be the evaluator distribution's unchanged core bytes.
        if not path.endswith("/SKILL.md") and canonical_text_bytes(raw) != catalog[".agents/" + path]:
            raise OwnershipError(f"retained core is incompatible with evaluator: {path}")
    return {"inventory_sha256": raw_sha256(inventory_raw), "files": {path: raw_sha256(raw) for path, raw in sorted(raw_files.items())}}


def _mutex_descriptor(path: Path) -> int:
    if os.name != "nt":
        return os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    # Python's usual Windows open does not share deletion. Delete sharing lets
    # the holder unlink the name while still owning the native lock; a delayed
    # contender must then fail the handle/name identity check below.
    import ctypes
    from ctypes import wintypes
    import msvcrt
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                       wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    create.restype = wintypes.HANDLE
    handle = create(str(path), 0x80000000 | 0x40000000, 1 | 2 | 4, None, 4, 0x00200000, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return msvcrt.open_osfhandle(handle, os.O_RDWR | os.O_BINARY)
    except BaseException:
        kernel.CloseHandle(handle)
        raise


@contextmanager
def ownership_mutex(target: Path):
    """Serialize every installed-root writer with ownership transactions."""
    root = _root(target)
    path = _destination(root, MUTEX_NAME, missing=True)
    existing = _ordinary(path, missing=True)
    if existing is not None and existing.st_size != 0:
        raise OwnershipError("ownership mutex path contains unrecognized owner content")
    descriptor = None
    acquired = False
    owned_name = False
    try:
        descriptor = _mutex_descriptor(path)
        if os.name == "nt":
            import msvcrt
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        acquired = True
        opened = os.fstat(descriptor)
        named = _ordinary(path)
        if (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino) or opened.st_nlink != 1 or opened.st_size != 0:
            raise OwnershipError("ownership mutex changed during acquisition")
        owned_name = True
        yield
    except OSError as exc:
        if not acquired:
            raise OwnershipError("another installed-root operation holds the ownership mutex") from exc
        raise
    finally:
        if descriptor is not None:
            if acquired:
                # No transactional writes follow this unlink. A process that
                # opened the old inode before unlink is rejected after locking.
                try:
                    named = path.lstat()
                    opened = os.fstat(descriptor)
                    if owned_name and (named.st_dev, named.st_ino) == (opened.st_dev, opened.st_ino):
                        path.unlink()
                except FileNotFoundError:
                    pass
                finally:
                    if os.name == "nt":
                        import msvcrt
                        os.lseek(descriptor, 0, os.SEEK_SET)
                        msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)


def _identity() -> dict:
    from se_harness.evaluator_identity import EvaluatorIdentityError, installed_evaluator_identity
    try:
        return installed_evaluator_identity().to_lock()
    except EvaluatorIdentityError as exc:
        raise OwnershipError(f"cannot identify selected evaluator: {exc}") from exc


def _parse_lock(raw: bytes) -> dict:
    from se_harness.integrity import parse_lock
    try:
        return parse_lock(raw.decode("utf-8"))
    except (UnicodeError, IntegrityError) as exc:
        raise OwnershipError(f"invalid ownership source lock: {exc}") from exc


def _load_repository(root: Path, *, check_installation: bool = True) -> tuple[dict, bytes, dict[str, bytes], dict[str, str]]:
    raw = _read(_destination(root, LOCK_NAME), limit=MAX_CONTROL)
    lock = _parse_lock(raw)
    catalog = _template_catalog()
    if lock.get("evaluator") != _identity():
        raise OwnershipError("upgrade the repository to the selected installed evaluator before ownership migration")
    version = str(lock.get("tool_version"))
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if match is None or tuple(map(int, match.groups())) < (0, 17, 0):
        raise OwnershipError("unsupported repository baseline; use the supported evaluator upgrade first")
    if check_installation:
        from se_harness.installer import plan_install
        changes, read_lock = plan_install(root, project_name=None, mode="upgrade")
        if read_lock != lock or any(item.action != "unchanged" and item.mode in {"managed", "fragment"} for item in changes):
            raise OwnershipError("repository is not an unchanged current standard installation; inspect doctor and upgrade")
    assert_ownership_state(root, lock)
    tree = _skill_tree(root)
    if lock.get("schema") == 3 and (not CATALOG <= set(tree) or set(tree) & (DISCOVERY_PATHS - CATALOG)):
        raise OwnershipError("retained repository skill inventory is missing, customized, or unowned")
    inputs = {LOCK_NAME: raw_sha256(raw)}
    for path, entry in lock["files"].items():
        _relative(path)
        destination = _destination(root, path, missing=entry["mode"] == "seed")
        if destination.exists():
            inputs[path] = raw_sha256(_read(destination))
        elif entry["mode"] != "seed":
            raise OwnershipError(f"missing managed file: {path}")
        else:
            inputs[path] = "absent"
    for path in CATALOG:
        if lock["schema"] == 3:
            entry = lock["files"].get(path)
            current = _read(_destination(root, path))
            if entry != {"mode": "managed", "sha256": canonical_sha256(catalog[path])} or canonical_sha256(current) != entry["sha256"]:
                raise OwnershipError(f"retained file does not match both lock and selected distribution: {path}")
        else:
            inputs[path] = "absent"
    # Owner notes beside the selected catalog are retained, not retired. Their
    # exact input hashes distinguish preexisting content from post-crash edits.
    inputs.update({path: digest for path, digest in tree.items() if path not in CATALOG})
    return lock, raw, catalog, dict(sorted(inputs.items()))


def _binding_input(path: Path, root: Path, evaluator: dict, catalog: dict[str, bytes]) -> tuple[dict, dict]:
    selected_path = Path(os.path.abspath(path))
    _root(selected_path.parent)
    raw = _read(selected_path, limit=MAX_CONTROL)
    value = _fields(_json(raw), _CONTRACT["binding_fields"], "binding input")
    if value["schema"] != BINDING_SCHEMA:
        raise OwnershipError("unsupported binding-input schema")
    hosts = value["hosts"]
    if not isinstance(hosts, dict) or not hosts or not set(hosts) <= set(HOSTS):
        raise OwnershipError("binding input requires an explicit supported host set")
    bindings = {}
    inputs = {"binding_input": str(selected_path), "binding_input_sha256": raw_sha256(raw), "hosts": {}}
    for host, value in sorted(hosts.items()):
        _fields(value, _CONTRACT["host_input_fields"], "host binding input")
        expected = _expected(value["expected"])
        if not isinstance(value["root"], str) or not Path(value["root"]).is_absolute():
            raise OwnershipError("plugin root must be explicitly absolute")
        package = _root(value["root"])
        if package == root or root in package.parents or package in root.parents:
            raise OwnershipError("external plugin root must not overlap the target repository")
        inspection = _inspect_plugin(package, host, expected, evaluator, catalog)
        inputs["hosts"][host] = {"root": str(package), **inspection}
        bindings[host] = json.loads(json.dumps(expected))
    record = {"schema": OWNERSHIP_SCHEMA, "provider": "plugin", "catalog": {
        path: canonical_sha256(raw) for path, raw in sorted(catalog.items())}, "hosts": bindings}
    # This detects inconsistent edits to portable selected identity fields. It is
    # not authentication: coherent rewriting is not proof of provider approval.
    record["binding_sha256"] = _digest(record)
    validate_ownership_binding(record)
    return record, inputs


def _result(provider: str, *, outcome: str = "planned", passed: bool = True, **members: Any) -> dict:
    return {"schema": "se-harness-command-result-v1", "command": "skill-ownership", "outcome": outcome,
            "passed": passed, "provider": provider, "availability": "unobserved", "native_discovery": "unobserved",
            "conflicts": [], "recovery": {"status": "none"}, "written": False, **members}


def _digest(value: Any) -> str:
    try:
        return raw_sha256(canonical_json_bytes(value, ensure_ascii=True))
    except (TypeError, ValueError, RecursionError) as exc:
        raise OwnershipError("ownership structure cannot be canonically hashed") from exc


def _assert_reviewed_external(plan: dict) -> None:
    inputs = plan["inputs"]
    if _identity() != inputs["evaluator"]:
        raise OwnershipError("selected evaluator changed after planning")
    external = inputs["external"]
    if not external:
        return
    if raw_sha256(_read(Path(external["binding_input"]), limit=MAX_CONTROL)) != external["binding_input_sha256"]:
        raise OwnershipError("binding input changed after planning")
    catalog = _template_catalog()
    for host, observed in external["hosts"].items():
        current = _inspect_plugin(_root(observed["root"]), host, plan["binding"]["hosts"][host], inputs["evaluator"], catalog)
        if current != {key: value for key, value in observed.items() if key != "root"}:
            raise OwnershipError("external plugin inventory changed after planning")


def _assert_reviewed_repository(root: Path, plan: dict) -> None:
    for path, digest in plan["inputs"]["repository"].items():
        current = _current(root, path)
        if ("absent" if current is None else raw_sha256(current)) != digest:
            raise OwnershipError(f"reviewed repository input changed before transaction: {path}")
    if set(_skill_tree(root)) - set(plan["inputs"]["repository"]):
        raise OwnershipError("retained-skill inventory changed before transaction")


def _normal_plan(root: Path, provider: str, binding_input: Path | None) -> tuple[dict, dict[str, tuple[bytes | None, bytes | None]]]:
    ensure_no_pending_recovery(root)
    lock, lock_raw, catalog, repository_inputs = _load_repository(root)
    if provider == "plugin":
        if binding_input is None:
            raise OwnershipError("plugin ownership requires --binding-input")
        binding, external_inputs = _binding_input(binding_input, root, lock["evaluator"], catalog)
    else:
        if binding_input is not None:
            raise OwnershipError("repository restoration does not accept plugin binding input")
        binding, external_inputs = None, {}
    after_lock = json.loads(json.dumps(lock))
    transaction: dict[str, tuple[bytes | None, bytes | None]] = {}
    if provider == "plugin":
        after_lock["schema"] = 4
        after_lock["skill_ownership"] = binding
        for path in sorted(CATALOG):
            if path in after_lock["files"]:
                transaction[path] = (_read(_destination(root, path)), None)
                del after_lock["files"][path]
    else:
        after_lock["schema"] = 3
        after_lock.pop("skill_ownership", None)
        if lock["schema"] == 4:
            for path, raw in sorted(catalog.items()):
                _destination(root, path, missing=True)
                transaction[path] = (None, raw)
                after_lock["files"][path] = {"mode": "managed", "sha256": canonical_sha256(raw)}
    if after_lock != lock:
        transaction[LOCK_NAME] = (lock_raw, pretty_json_bytes(after_lock, ensure_ascii=True))
    changes = [{"path": path, "action": "remove" if new is None else "add" if old is None else "update"}
               for path, (old, new) in transaction.items()]
    inputs = {"repository": repository_inputs, "external": external_inputs, "evaluator": lock["evaluator"]}
    description = {"target": str(root), "provider": provider, "inputs": inputs, "binding": binding,
                   "changes": changes, "after_lock_sha256": raw_sha256(transaction.get(LOCK_NAME, (lock_raw, lock_raw))[1])}
    plan_digest = _digest(description)
    result = _result(provider, outcome="planned" if changes else "unchanged", plan_sha256=plan_digest,
                     changes=changes, inputs=inputs, binding=binding, source_identity=lock["evaluator"],
                     transaction_paths=[MUTEX_NAME, RECOVERY_NAME],
                     temporary_stages={"pattern": _stage_prefix({"plan_sha256": plan_digest}) + "*",
                                       "maximum_files": sum(raw is not None for pair in transaction.values() for raw in pair),
                                       "paths": []}, target=str(root))
    return result, transaction


def _encoded(value: bytes | None) -> str | None:
    return None if value is None else base64.b64encode(value).decode("ascii")


def _decoded(value: Any) -> bytes | None:
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > MAX_CONTROL:
        raise OwnershipError("invalid recovery snapshot")
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise OwnershipError("invalid recovery snapshot encoding") from exc


def _created_directories(root: Path, transaction: dict) -> list[str]:
    absent = set()
    for relative, (_, after) in transaction.items():
        if after is None:
            continue
        current = Path(relative).parent
        while current.as_posix() != ".":
            if not (root / current).exists():
                absent.add(current.as_posix())
            current = current.parent
    return sorted(absent, key=lambda value: (len(value.split("/")), value))


def _file_identity(root: Path, path: str) -> dict | None:
    destination = _destination(root, path, missing=True)
    info = _ordinary(destination, missing=True)
    return None if info is None else {"device": info.st_dev, "inode": info.st_ino}


def _identity_value(value: Any, *, absent: bool = False) -> dict | None:
    if absent and value is None:
        return None
    identity = _fields(value, {"device", "inode"}, "filesystem identity")
    if any(type(item) is not int or item < 0 for item in identity.values()):
        raise OwnershipError("invalid filesystem identity")
    return identity


def _directory_inputs(root: Path) -> dict:
    paths = {parent.as_posix() for path in CATALOG for parent in Path(path).parents if parent.as_posix() != "."}
    result = {}
    for relative in sorted(paths):
        _destination(root, relative + "/.ownership-path-check", missing=True)
        info = _ordinary(root / relative, directory=True, missing=True)
        result[relative] = None if info is None else {"device": info.st_dev, "inode": info.st_ino}
    return result


def _write_journal(root: Path, payload: dict) -> None:
    from se_harness.integrity import fsync_directory
    atomic_write_bytes(_destination(root, RECOVERY_NAME, missing=True), _journal_bytes(payload))
    fsync_directory(root)


def _stage_prefix(payload: dict) -> str:
    return ".engineering-harness.ownership-" + payload["plan_sha256"][:16] + "-"


def _transaction_evidence(payload: dict) -> dict:
    """Report the bounded planned stage family and the actual recorded names."""
    paths = sorted(stage["path"] for entry in payload["entries"].values()
                   for label in ("before_stage", "after_stage") if (stage := entry[label]) is not None)
    return {"transaction_paths": [MUTEX_NAME, RECOVERY_NAME, *paths],
            "temporary_stages": {"pattern": _stage_prefix(payload) + "*",
                                 "maximum_files": sum(entry[label] is not None for entry in payload["entries"].values()
                                                      for label in ("before", "after")),
                                 "paths": paths}}


def _prepare_stages(root: Path, payload: dict, transaction: dict) -> None:
    """Persist backup/replacement inode identities before any catalog mutation."""
    from se_harness.integrity import fsync_directory
    for path, (before, after) in transaction.items():
        for label, raw in (("before_stage", before), ("after_stage", after)):
            if raw is None:
                continue
            staged = stage_bytes(root / LOCK_NAME, raw, prefix=_stage_prefix(payload))
            payload["entries"][path][label] = {"path": staged.name, "identity": _file_identity(root, staged.name)}
            fsync_directory(root)
            _write_journal(root, payload)
            _fault_hook("stage-journal-updated", path + ":" + label)
    payload["phase"] = "applying"
    _write_journal(root, payload)
    _fault_hook("stages-prepared")


def _journal_bytes(payload: dict) -> bytes:
    value = {"schema": RECOVERY_SCHEMA, "payload": payload, "sha256": _digest(payload)}
    raw = pretty_json_bytes(value, ensure_ascii=True)
    if len(raw) > MAX_CONTROL:
        raise OwnershipError("recovery record exceeds control-document size bound")
    return raw


def _journal(root: Path, plan: dict, transaction: dict) -> dict:
    root_stat = root.stat()
    return {"target": str(root), "root_device": root_stat.st_dev, "root_inode": root_stat.st_ino,
            "plan_sha256": plan["plan_sha256"], "provider": plan["provider"], "inputs": plan["inputs"]["repository"],
            "entries": {path: {"before": _encoded(before), "after": _encoded(after),
                               "original_identity": _file_identity(root, path), "before_stage": None, "after_stage": None}
                        for path, (before, after) in transaction.items()},
            "created_directories": _created_directories(root, transaction), "directory_inputs": _directory_inputs(root),
            "directory_identities": {}, "completed": [], "phase": "prepared"}


def _load_journal(root: Path) -> tuple[dict, bytes, dict[str, tuple[bytes | None, bytes | None]]]:
    raw = _read(_destination(root, RECOVERY_NAME), limit=MAX_CONTROL)
    value = _fields(_json(raw), {"schema", "payload", "sha256"}, "recovery envelope")
    payload = _fields(value["payload"], {"target", "root_device", "root_inode", "plan_sha256", "provider", "inputs", "entries", "created_directories", "directory_inputs", "directory_identities", "completed", "phase"}, "recovery payload")
    if value["schema"] != RECOVERY_SCHEMA or value["sha256"] != _digest(payload):
        raise OwnershipError("tampered or unsupported ownership recovery record")
    current_root = root.stat()
    if payload["target"] != str(root) or type(payload["root_device"]) is not int or type(payload["root_inode"]) is not int or (
            payload["root_device"], payload["root_inode"]) != (current_root.st_dev, current_root.st_ino):
        raise OwnershipError("recovery record belongs to another repository")
    _hash(payload["plan_sha256"], "recovery plan")
    if not isinstance(payload["provider"], str) or payload["provider"] not in {"plugin", "repository"}:
        raise OwnershipError("invalid recovery provider")
    if not isinstance(payload["phase"], str) or payload["phase"] not in {"prepared", "applying", "committed", "rolled-back"}:
        raise OwnershipError("invalid recovery phase")
    entries = payload["entries"]
    if not isinstance(entries, dict) or LOCK_NAME not in entries or not set(entries) <= CATALOG | {LOCK_NAME}:
        raise OwnershipError("recovery record contains an out-of-catalog destination")
    transaction = {}
    stage_names: set[str] = set()
    for path, entry in entries.items():
        _relative(path)
        _fields(entry, {"before", "after", "original_identity", "before_stage", "after_stage"}, "recovery entry")
        transaction[path] = (_decoded(entry["before"]), _decoded(entry["after"]))
        _identity_value(entry["original_identity"], absent=entry["before"] is None)
        if (entry["before"] is None) != (entry["original_identity"] is None):
            raise OwnershipError("recovery original identity does not match snapshot")
        for label, content in zip(("before_stage", "after_stage"), transaction[path]):
            staged = entry[label]
            if staged is None:
                if payload["phase"] in {"applying", "committed"} and content is not None:
                    raise OwnershipError("recovery stage identity is missing")
                continue
            _fields(staged, {"path", "identity"}, "recovery stage")
            name = _relative(staged["path"])
            if "/" in name or not name.startswith(_stage_prefix(payload)) or content is None or name in stage_names:
                raise OwnershipError("unsafe recovery stage path")
            stage_names.add(name)
            _identity_value(staged["identity"])
            stage_path = _destination(root, name, missing=True)
            if stage_path.exists() and (_file_identity(root, name) != staged["identity"] or _read(stage_path) != content):
                raise OwnershipError("recovery stage was replaced or corrupted")
    before_raw, after_raw = transaction[LOCK_NAME]
    if before_raw is None or after_raw is None:
        raise OwnershipError("recovery lock snapshots must both exist")
    before_lock = _parse_lock(before_raw)
    after_lock = _parse_lock(after_raw)
    if before_lock.get("evaluator") != _identity() or after_lock.get("evaluator") != before_lock.get("evaluator"):
        raise OwnershipError("recovery evaluator identity mismatch")
    remainder = lambda lock: {key: val for key, val in lock.items() if key not in {"schema", "files", "skill_ownership"}}
    if remainder(before_lock) != remainder(after_lock) or (
            {path: val for path, val in before_lock["files"].items() if path not in CATALOG} !=
            {path: val for path, val in after_lock["files"].items() if path not in CATALOG}):
        raise OwnershipError("recovery would alter unrelated lock ownership")
    if (payload["provider"] == "plugin") != (after_lock["schema"] == 4):
        raise OwnershipError("recovery destination provider does not match lock")
    catalog = _template_catalog()
    required = {LOCK_NAME}
    if before_lock["schema"] != after_lock["schema"]:
        required |= CATALOG
    if set(entries) != required:
        raise OwnershipError("recovery snapshot has an incomplete transaction inventory")
    for path in required - {LOCK_NAME}:
        for raw_value, lock in zip(transaction[path], (before_lock, after_lock)):
            if lock["schema"] == 4:
                if raw_value is not None or path in lock["files"]:
                    raise OwnershipError("plugin-owned recovery snapshot contains repository core")
            elif raw_value is None or canonical_sha256(raw_value) != canonical_sha256(catalog[path]) or lock["files"].get(path) != {
                    "mode": "managed", "sha256": canonical_sha256(catalog[path])}:
                raise OwnershipError("recovery core snapshot does not match the trusted evaluator")
    completed = payload["completed"]
    if not isinstance(completed, list) or any(not isinstance(path, str) for path in completed) or len(completed) != len(set(completed)) or not set(completed) <= set(entries):
        raise OwnershipError("invalid recovery progress")
    directories = payload["created_directories"]
    allowed_directories = {parent.as_posix() for path in CATALOG for parent in Path(path).parents if parent.as_posix() != "."}
    if not isinstance(directories, list) or any(not isinstance(path, str) for path in directories) or len(set(directories)) != len(directories) or not set(directories) <= allowed_directories:
        raise OwnershipError("unsafe recovery directory inventory")
    directory_inputs = _fields(payload["directory_inputs"], allowed_directories, "original directory inventory")
    for identity in directory_inputs.values():
        _identity_value(identity, absent=True)
    addition_parents = {parent.as_posix() for path, (before, after) in transaction.items() if before is None and after is not None
                        for parent in Path(path).parents if parent.as_posix() != "."}
    if set(directories) != {path for path in addition_parents if directory_inputs[path] is None}:
        raise OwnershipError("recovery directory claim conflicts with original owner directories")
    directory_ids = payload["directory_identities"]
    if not isinstance(directory_ids, dict) or not set(directory_ids) <= set(directories):
        raise OwnershipError("invalid created-directory identities")
    for identity in directory_ids.values():
        _identity_value(identity)
    inputs = payload["inputs"]
    skill_prefixes = tuple(prefix + "/" for prefix in {
        ".agents/skills/harness-orient", ".agents/skills/harness-operator-brief",
        ".claude/skills/harness-orient", ".claude/skills/harness-operator-brief"})
    if not isinstance(inputs, dict) or not (set(before_lock["files"]) | CATALOG | {LOCK_NAME}) <= set(inputs) or any(path not in set(before_lock["files"]) | CATALOG | {LOCK_NAME}
            and (not isinstance(path, str) or not path.startswith(skill_prefixes)) for path in inputs):
        raise OwnershipError("invalid recovery source inventory")
    for path, digest in inputs.items():
        _relative(path)
        if digest != "absent":
            _hash(digest, path)
    if inputs.get(LOCK_NAME) != raw_sha256(before_raw):
        raise OwnershipError("recovery source lock digest mismatch")
    return payload, raw, transaction


def _current(root: Path, path: str) -> bytes | None:
    destination = _destination(root, path, missing=True)
    return _read(destination, limit=MAX_CONTROL if path == LOCK_NAME else MAX_FILE) if destination.exists() else None


def _matches(root: Path, path: str, raw: bytes | None, identity: dict | None) -> bool:
    return _current(root, path) == raw and _file_identity(root, path) == identity


def _before_matches(root: Path, path: str, payload: dict, before: bytes | None) -> bool:
    entry = payload["entries"][path]
    if _matches(root, path, before, entry["original_identity"]):
        return True
    stage = entry["before_stage"]
    return stage is not None and _matches(root, path, before, stage["identity"])


def _after_matches(root: Path, path: str, payload: dict, after: bytes | None) -> bool:
    stage = payload["entries"][path]["after_stage"]
    return _matches(root, path, after, None if stage is None else stage["identity"])


def _directory_conflicts(root: Path, payload: dict) -> list[str]:
    conflicts = []
    for path, before_identity in payload["directory_inputs"].items():
        info = _ordinary(root / path, directory=True, missing=True)
        current = None if info is None else {"device": info.st_dev, "inode": info.st_ino}
        if before_identity is not None:
            if current != before_identity:
                conflicts.append(f"intervening owner directory change: {path}")
        elif current is not None and current != payload["directory_identities"].get(path):
            conflicts.append(f"unproven owner directory: {path}")
    return conflicts


def _recovery_conflicts(root: Path, payload: dict, transaction: dict) -> list[str]:
    conflicts = _directory_conflicts(root, payload)
    for path, (before, after) in transaction.items():
        if not _before_matches(root, path, payload, before) and not _after_matches(root, path, payload, after):
            conflicts.append(f"intervening owner change: {path}")
    for path, digest in payload["inputs"].items():
        if path in transaction:
            continue
        raw = _current(root, path)
        if ("absent" if raw is None else raw_sha256(raw)) != digest:
            conflicts.append(f"intervening reviewed-input change: {path}")
    unexpected = set(_skill_tree(root)) - CATALOG - set(payload["inputs"])
    conflicts.extend(f"intervening owner file: {path}" for path in sorted(unexpected))
    return conflicts


def _recovery_plan(root: Path, provider: str) -> tuple[dict, dict, dict]:
    payload, raw, transaction = _load_journal(root)
    conflicts = _recovery_conflicts(root, payload, transaction)
    if payload["phase"] == "committed" and any(not _after_matches(root, path, payload, after) for path, (_, after) in transaction.items()):
        conflicts.append("committed ownership state changed before cleanup")
    observed = {path: {"sha256": None if (content := _current(root, path)) is None else raw_sha256(content),
                      "identity": _file_identity(root, path)} for path in transaction}
    plan_digest = _digest({"target": str(root), "requested_provider": provider, "recovery_sha256": raw_sha256(raw), "observed": observed})
    committed = payload["phase"] == "committed"
    before_lock = _parse_lock(transaction[LOCK_NAME][0])
    resulting_provider = payload["provider"] if committed else "plugin" if before_lock["schema"] == 4 else "repository"
    result = _result(resulting_provider, requested_provider=provider, outcome="recovery-required", passed=not conflicts,
                     plan_sha256=plan_digest,
                     changes=[{"path": path, "action": "finalize-applied-state" if committed else "restore-prior-state"}
                              for path in transaction], inputs={"recovery_sha256": raw_sha256(raw)},
                     binding=None, conflicts=conflicts,
                     recovery={"status": "required", "phase": payload["phase"],
                               "original_target_provider": payload["provider"], "resulting_provider": resulting_provider,
                               "original_plan_sha256": payload["plan_sha256"]},
                     target=str(root), **_transaction_evidence(payload))
    return result, payload, transaction


def plan_skill_ownership(target: Path, *, provider: str, binding_input: Path | None = None) -> dict:
    """Plan a migration, restoration, or pending recovery without writing."""
    if not isinstance(provider, str) or provider not in {"plugin", "repository"}:
        raise OwnershipError("provider must be plugin or repository")
    root = _root(target)
    if (root / RECOVERY_NAME).exists() or (root / RECOVERY_NAME).is_symlink():
        return _recovery_plan(root, provider)[0]
    return _normal_plan(root, provider, binding_input)[0]


def _write_destination(root: Path, path: str, value: bytes | None, *, staged: dict | None = None) -> None:
    destination = _destination(root, path, missing=True)
    if value is None:
        destination.unlink(missing_ok=True)
    else:
        if staged is None:
            raise OwnershipError("replacement has no durable stage identity")
        stage = _destination(root, staged["path"])
        if _file_identity(root, staged["path"]) != staged["identity"] or _read(stage) != value:
            raise OwnershipError("replacement stage identity or bytes changed")
        os.replace(stage, destination)
    from se_harness.integrity import fsync_directory
    fsync_directory(destination.parent)
    if destination.parent != root:
        fsync_directory(root)


def _ensure_created_directories(root: Path, payload: dict) -> None:
    from se_harness.integrity import fsync_directory
    conflicts = _directory_conflicts(root, payload)
    if conflicts:
        raise OwnershipError("; ".join(conflicts))
    for relative in payload["created_directories"]:
        path = root / relative
        info = _ordinary(path, directory=True, missing=True)
        if info is not None:
            identity = {"device": info.st_dev, "inode": info.st_ino}
            if identity != payload["directory_identities"].get(relative):
                raise OwnershipError(f"owner created a planned directory: {relative}")
            continue
        path.mkdir()
        info = _ordinary(path, directory=True)
        payload["directory_identities"][relative] = {"device": info.st_dev, "inode": info.st_ino}
        fsync_directory(path.parent)
        _write_journal(root, payload)
        _fault_hook("directory-journal-updated", relative)


def _cleanup_stages(root: Path, payload: dict, transaction: dict) -> None:
    from se_harness.integrity import fsync_directory
    declared = {}
    for path, (before, after) in transaction.items():
        for label, raw in (("before_stage", before), ("after_stage", after)):
            stage = payload["entries"][path][label]
            if stage is not None:
                declared[stage["path"]] = (stage["identity"], raw)
    observed = {path.name for path in root.iterdir() if path.name.startswith(_stage_prefix(payload))}
    if not observed <= set(declared):
        raise OwnershipError("unrecorded staged file requires explicit recovery assessment")
    for path in sorted(observed):
        identity, raw = declared[path]
        if not _matches(root, path, raw, identity):
            raise OwnershipError("owner changed a recovery stage; it will be preserved")
    for path in sorted(observed):
        _destination(root, path).unlink()
        fsync_directory(root)
        _fault_hook("stage-cleaned", path)
    fsync_directory(root)


def _restore(root: Path, payload: dict, transaction: dict) -> None:
    conflicts = _recovery_conflicts(root, payload, transaction)
    if conflicts:
        raise OwnershipError("; ".join(conflicts))
    # Validate the whole recovery before its first write. Before-byte stages
    # retain their inode through replacement, allowing interrupted recovery retry.
    for path, (before, after) in reversed(tuple(transaction.items())):
        if _before_matches(root, path, payload, before):
            continue
        if not _after_matches(root, path, payload, after):
            raise OwnershipError(f"intervening owner change during recovery: {path}")
        _fault_hook("recovery-before-write", path)
        if not _after_matches(root, path, payload, after):
            raise OwnershipError(f"intervening owner change during recovery: {path}")
        _write_destination(root, path, before, staged=payload["entries"][path]["before_stage"])
        _fault_hook("recovery-after-write", path)
    for relative in sorted(payload["created_directories"], key=lambda value: (-len(value.split("/")), value)):
        path = root / relative
        if path.exists():
            info = _ordinary(path, directory=True)
            if {"device": info.st_dev, "inode": info.st_ino} != payload["directory_identities"].get(relative):
                raise OwnershipError(f"unproven owner directory will be preserved: {relative}")
            if any(path.iterdir()):
                raise OwnershipError(f"owner content prevents directory recovery: {relative}")
            path.rmdir()
            from se_harness.integrity import fsync_directory
            fsync_directory(path.parent)
    if any(not _before_matches(root, path, payload, before) for path, (before, _) in transaction.items()):
        raise OwnershipError("recovery postcondition did not restore prior bytes")
    payload["phase"] = "rolled-back"
    _write_journal(root, payload)


def _assert_after(root: Path, payload: dict, transaction: dict) -> None:
    conflicts = _recovery_conflicts(root, payload, transaction)
    if conflicts or any(not _after_matches(root, path, payload, after) for path, (_, after) in transaction.items()):
        raise OwnershipError("ownership postcondition or input identity changed: " + "; ".join(conflicts))
    lock = _parse_lock(_read(_destination(root, LOCK_NAME), limit=MAX_CONTROL))
    assert_ownership_state(root, lock)


def _finish_journal(root: Path, payload: dict, transaction: dict) -> None:
    from se_harness.integrity import fsync_directory
    _cleanup_stages(root, payload, transaction)
    if payload["phase"] == "committed":
        _assert_after(root, payload, transaction)
    elif _recovery_conflicts(root, payload, transaction) or any(
            not _before_matches(root, path, payload, before) for path, (before, _) in transaction.items()):
        raise OwnershipError("owner state changed during recovery cleanup")
    _destination(root, RECOVERY_NAME).unlink()
    fsync_directory(root)


def apply_skill_ownership(target: Path, *, provider: str, binding_input: Path | None = None,
                          expected_plan_sha256: str) -> dict:
    """Apply exactly one reviewed plan, requiring the installed evaluator authority."""
    if not isinstance(provider, str) or provider not in {"plugin", "repository"}:
        raise OwnershipError("provider must be plugin or repository")
    _hash(expected_plan_sha256, "reviewed ownership plan")
    root = _root(target)
    from se_harness.mutation_guard import require_mutation_authority
    with ownership_mutex(root):
        # The authority guard exempts only this registered operation from pending
        # recovery refusal. It still proves the exact installed evaluator identity.
        require_mutation_authority(root, operation="skill-ownership-apply")
        if (root / RECOVERY_NAME).exists() or (root / RECOVERY_NAME).is_symlink():
            plan, payload, transaction = _recovery_plan(root, provider)
            if plan["plan_sha256"] != expected_plan_sha256:
                raise OwnershipError("stale reviewed recovery plan")
            if plan["conflicts"]:
                return plan
            try:
                if payload["phase"] == "committed":
                    _assert_after(root, payload, transaction)
                else:
                    _restore(root, payload, transaction)
                _finish_journal(root, payload, transaction)
            except (OSError, OwnershipError) as exc:
                return {**plan, "passed": False, "conflicts": [str(exc)],
                        "recovery": {**plan["recovery"], "status": "required", "phase": payload["phase"]}}
            committed = payload["phase"] == "committed"
            return {**plan, "outcome": "applied" if committed else "rolled-back", "passed": True, "written": True,
                    "recovery": {**plan["recovery"], "status": "finalized" if committed else "restored", "phase": payload["phase"]}}
        plan, transaction = _normal_plan(root, provider, binding_input)
        if plan["plan_sha256"] != expected_plan_sha256:
            raise OwnershipError("stale reviewed ownership plan; inputs changed")
        if not transaction:
            return plan
        payload = _journal(root, plan, transaction)
        journal_raw = _journal_bytes(payload)
        journal_path = _destination(root, RECOVERY_NAME, missing=True)
        try:
            atomic_write_bytes(journal_path, journal_raw)
            from se_harness.integrity import fsync_directory
            fsync_directory(root)
            _fault_hook("journal-prepared")
            _prepare_stages(root, payload, transaction)
            plan = {**plan, **_transaction_evidence(payload)}
            _assert_reviewed_repository(root, plan)
            _assert_reviewed_external(plan)
            _ensure_created_directories(root, payload)
            for path, (before, after) in transaction.items():
                if not _matches(root, path, before, payload["entries"][path]["original_identity"]):
                    raise OwnershipError(f"reviewed input changed before write: {path}")
                _fault_hook("before-write", path)
                if not _matches(root, path, before, payload["entries"][path]["original_identity"]):
                    raise OwnershipError(f"reviewed input changed at write boundary: {path}")
                _write_destination(root, path, after, staged=payload["entries"][path]["after_stage"])
                _fault_hook("after-write", path)
                payload["completed"].append(path)
                atomic_write_bytes(journal_path, _journal_bytes(payload))
                fsync_directory(root)
                _fault_hook("journal-updated", path)
            _fault_hook("before-postcondition")
            _assert_after(root, payload, transaction)
            _assert_reviewed_external(plan)
            _fault_hook("after-postcondition")
            _fault_hook("before-journal-cleanup")
            _assert_after(root, payload, transaction)
            _assert_reviewed_external(plan)
            # The durable commit marker is written only after final hooks and
            # revalidation. A later cleanup interruption finalizes this applied
            # state rather than pretending deleted backup stages can roll back.
            payload["phase"] = "committed"
            _write_journal(root, payload)
            _fault_hook("committed")
            _finish_journal(root, payload, transaction)
            return {**plan, "outcome": "applied", "written": True}
        except BaseException as failure:
            # Process death leaves the already durable journal. Catchable failures
            # return actual rollback evidence, never claim a successful migration.
            plan = {**plan, **_transaction_evidence(payload)}
            try:
                if payload["phase"] == "committed":
                    return {**plan, "outcome": "recovery-required", "passed": False, "written": True,
                            "conflicts": [str(failure)], "recovery": {"status": "required"}}
                _restore(root, payload, transaction)
                _finish_journal(root, payload, transaction)
            except BaseException as recovery_failure:
                return {**plan, "outcome": "recovery-required", "passed": False, "written": True,
                        "conflicts": [str(failure), str(recovery_failure)], "recovery": {"status": "required"}}
            return {**plan, "outcome": "rolled-back", "passed": False, "written": False,
                    "conflicts": [str(failure)], "recovery": {"status": "restored"}}
