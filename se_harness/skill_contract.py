"""Strict portable-skill contracts and deterministic portable-core identity."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


CONTRACT_SCHEMA = "se-harness-skill-contract-v1"
MANIFEST_SCHEMA = "se-harness-skill-manifest-v1"
CANONICAL_JSON_SCHEMA = "se-harness-canonical-json-v1"
TEXT_MODE = "utf8-text-lf-v1"
RECEIPT_SCHEMA = "se-harness-execution-receipt-v1"
MAX_CANONICAL_INTEGER = (1 << 63) - 1
MAX_SKILL_FILES = 512
MAX_SKILL_FILE_BYTES = 1 << 20
MAX_SKILL_BYTES = 8 << 20

_NAME = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?")
_IDENTIFIER = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,126}[a-z0-9])?")
_VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


class SkillContractError(ValueError):
    """A stable, bounded portable-skill contract diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class SkillContract:
    """A validated v1 portable-skill contract."""

    value: Mapping[str, Any]

    @property
    def name(self) -> str:
        return str(self.value["name"])

    @property
    def version(self) -> str:
        return str(self.value["version"])


@dataclass(frozen=True)
class SkillManifest:
    """Canonical portable-core manifest and its identity digest."""

    value: Mapping[str, Any]
    canonical_bytes: bytes
    sha256: str


def _reject_duplicate_keys(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SkillContractError("SKC002", f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_canonical_value(value: Any, *, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        if not -MAX_CANONICAL_INTEGER <= value <= MAX_CANONICAL_INTEGER:
            raise SkillContractError("SKC003", f"integer outside the canonical range at {path}")
        return
    if isinstance(value, float):
        raise SkillContractError("SKC003", f"floating-point values are prohibited at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_canonical_value(item, path=f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise SkillContractError("SKC003", f"object key is not a string at {path}")
            _validate_canonical_value(item, path=f"{path}.{key}")
        return
    raise SkillContractError("SKC003", f"unsupported canonical JSON value at {path}")


def canonical_json_bytes(value: Any) -> bytes:
    """Encode one ``se-harness-canonical-json-v1`` value."""

    _validate_canonical_value(value)
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (UnicodeEncodeError, ValueError, TypeError) as exc:
        raise SkillContractError("SKC003", "value cannot be canonically encoded as UTF-8 JSON") from exc
    return encoded + b"\n"


def _object(value: Any, fields: set[str], path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SkillContractError("SKC004", f"{path} must be an object")
    missing = sorted(fields - value.keys())
    unknown = sorted(value.keys() - fields)
    if missing:
        raise SkillContractError("SKC005", f"{path} is missing fields: {', '.join(missing)}")
    if unknown:
        raise SkillContractError("SKC006", f"{path} has unknown fields: {', '.join(unknown)}")
    return value


def _text(value: Any, path: str, *, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096 or _CONTROL.search(value):
        raise SkillContractError("SKC007", f"{path} must be bounded non-control text")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise SkillContractError("SKC007", f"{path} has an invalid value")
    return value


def _boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise SkillContractError("SKC008", f"{path} must be a boolean")
    return value


def _list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list) or len(value) > 128:
        raise SkillContractError("SKC009", f"{path} must be a bounded array")
    return value


def _unique_texts(value: Any, path: str, *, allowed: set[str] | None = None) -> list[str]:
    result: list[str] = []
    for index, item in enumerate(_list(value, path)):
        selected = _text(item, f"{path}[{index}]", pattern=_IDENTIFIER)
        if allowed is not None and selected not in allowed:
            raise SkillContractError("SKC010", f"unsupported value at {path}[{index}]: {selected}")
        if selected in result:
            raise SkillContractError("SKC011", f"duplicate value at {path}: {selected}")
        result.append(selected)
    return result


def _typed_entries(
    value: Any,
    path: str,
    fields: set[str],
    *,
    allowed_types: set[str] | None = None,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, item in enumerate(_list(value, path)):
        entry_path = f"{path}[{index}]"
        entry = _object(item, fields, entry_path)
        identity_field = "name" if "name" in fields else "id"
        identity = _text(entry[identity_field], f"{entry_path}.{identity_field}", pattern=_IDENTIFIER)
        if identity in names:
            raise SkillContractError("SKC011", f"duplicate {identity_field} at {path}: {identity}")
        names.add(identity)
        if "type" in fields:
            selected_type = _text(entry["type"], f"{entry_path}.type", pattern=_IDENTIFIER)
            if allowed_types is not None and selected_type not in allowed_types:
                raise SkillContractError("SKC010", f"unsupported input type: {selected_type}")
        if "required" in fields:
            _boolean(entry["required"], f"{entry_path}.required")
        if "description" in fields:
            _text(entry["description"], f"{entry_path}.description")
        if "outcome" in fields:
            outcome = _text(entry["outcome"], f"{entry_path}.outcome", pattern=_IDENTIFIER)
            if outcome not in {"blocked", "degraded", "failed", "stopped"}:
                raise SkillContractError("SKC010", f"unsupported stop outcome: {outcome}")
        if "schema" in fields:
            _text(entry["schema"], f"{entry_path}.schema", pattern=_IDENTIFIER)
        if "retention" in fields:
            retention = _text(entry["retention"], f"{entry_path}.retention", pattern=_IDENTIFIER)
            if retention not in {"inline", "none"}:
                raise SkillContractError("SKC010", f"unsupported output retention: {retention}")
        result.append(entry)
    return result


def parse_skill_contract_bytes(raw: bytes) -> SkillContract:
    """Parse and strictly validate a v1 portable-skill contract."""

    if len(raw) > MAX_SKILL_FILE_BYTES:
        raise SkillContractError("SKC001", "skill contract exceeds the bounded size")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SkillContractError("SKC001", "skill contract is not UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except SkillContractError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise SkillContractError("SKC001", "skill contract is not valid bounded JSON") from exc

    top = _object(
        value,
        {
            "schema",
            "name",
            "version",
            "outcome",
            "activation",
            "inputs",
            "preconditions",
            "mutation_class",
            "evaluator",
            "harness_operations",
            "delegation",
            "evidence",
            "stop_conditions",
            "outputs",
        },
        "$",
    )
    if top["schema"] != CONTRACT_SCHEMA:
        raise SkillContractError("SKC012", f"unsupported skill contract schema: {top['schema']!r}")
    name = _text(top["name"], "$.name", pattern=_NAME)
    _text(top["version"], "$.version", pattern=_VERSION)
    _text(top["outcome"], "$.outcome")
    if top["mutation_class"] != "read-only":
        raise SkillContractError("SKC013", "the pilot skill mutation_class must be read-only")

    activation = _object(top["activation"], {"explicit", "implicit", "must_not_match"}, "$.activation")
    _boolean(activation["explicit"], "$.activation.explicit")
    _boolean(activation["implicit"], "$.activation.implicit")
    negative_matches = _list(activation["must_not_match"], "$.activation.must_not_match")
    if not negative_matches:
        raise SkillContractError("SKC014", "activation must declare at least one non-match example")
    for index, item in enumerate(negative_matches):
        _text(item, f"$.activation.must_not_match[{index}]")

    inputs = _typed_entries(
        top["inputs"],
        "$.inputs",
        {"name", "required", "type"},
        allowed_types={"artifact-id", "directory-path", "evaluator-launcher", "phase", "repository-path", "version"},
    )
    input_map = {entry["name"]: entry for entry in inputs}
    expected_inputs = {
        "target": ("repository-path", True),
        "evaluator-launcher": ("evaluator-launcher", True),
        "expected-evaluator-version": ("version", True),
        "expected-evaluator-root": ("directory-path", True),
        "artifact": ("artifact-id", False),
        "preflight-phase": ("phase", False),
    }
    if set(input_map) != set(expected_inputs):
        raise SkillContractError("SKC015", "harness-orient inputs do not match the closed pilot input set")
    for input_name, (input_type, required) in expected_inputs.items():
        if input_map[input_name]["type"] != input_type or input_map[input_name]["required"] is not required:
            raise SkillContractError("SKC015", f"invalid harness-orient input declaration: {input_name}")

    _typed_entries(top["preconditions"], "$.preconditions", {"id", "description"})
    evaluator = _object(
        top["evaluator"],
        {"minimum_version", "required_operations", "optional_operations", "missing_required", "missing_optional"},
        "$.evaluator",
    )
    _text(evaluator["minimum_version"], "$.evaluator.minimum_version", pattern=_VERSION)
    required_operations = _unique_texts(
        evaluator["required_operations"],
        "$.evaluator.required_operations",
        allowed={"version", "identity", "doctor", "validate-json", "inspect-json"},
    )
    optional_operations = _unique_texts(
        evaluator["optional_operations"],
        "$.evaluator.optional_operations",
        allowed={"focus-json", "preflight"},
    )
    if required_operations != ["version", "identity", "doctor", "validate-json", "inspect-json"]:
        raise SkillContractError("SKC016", "required evaluator operations must use the approved semantic order")
    if optional_operations != ["focus-json", "preflight"]:
        raise SkillContractError("SKC016", "optional evaluator operations must use the approved semantic order")
    if evaluator["missing_required"] != "blocked" or evaluator["missing_optional"] != "degraded":
        raise SkillContractError("SKC016", "evaluator failure policy differs from the approved capability matrix")

    operations = _typed_entries(top["harness_operations"], "$.harness_operations", {"id", "required"})
    expected_operations = [(item, True) for item in required_operations] + [(item, False) for item in optional_operations]
    if [(entry["id"], entry["required"]) for entry in operations] != expected_operations:
        raise SkillContractError("SKC017", "harness operations differ from the evaluator capability matrix")

    delegation = _object(top["delegation"], {"allowed", "fallback"}, "$.delegation")
    if _boolean(delegation["allowed"], "$.delegation.allowed") or delegation["fallback"] != "single-agent":
        raise SkillContractError("SKC018", "the pilot must disable delegation and retain the single-agent fallback")
    evidence = _object(top["evidence"], {"receipt_schema", "target_retention"}, "$.evidence")
    if evidence["receipt_schema"] != RECEIPT_SCHEMA or _boolean(evidence["target_retention"], "$.evidence.target_retention"):
        raise SkillContractError("SKC019", "read-only evidence must be an inline v1 receipt with no target retention")
    _typed_entries(top["stop_conditions"], "$.stop_conditions", {"id", "outcome"})
    outputs = _typed_entries(top["outputs"], "$.outputs", {"name", "schema", "retention"})
    if [(entry["name"], entry["retention"]) for entry in outputs] != [
        ("orientation-result", "inline"),
        ("execution-receipt", "inline"),
    ]:
        raise SkillContractError("SKC020", "harness-orient must return the orientation result and receipt inline")
    if name == "harness-orient" and outputs[1]["schema"] != RECEIPT_SCHEMA:
        raise SkillContractError("SKC020", "execution receipt output uses the wrong schema")
    _validate_canonical_value(top)
    return SkillContract(top)


def load_skill_contract(path: Path) -> SkillContract:
    """Read and validate one regular contract file without following a symlink."""

    if path.is_symlink() or not path.is_file():
        raise SkillContractError("SKC001", "skill contract must be a regular file")
    try:
        return parse_skill_contract_bytes(path.read_bytes())
    except OSError as exc:
        raise SkillContractError("SKC001", "skill contract could not be read") from exc


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except AttributeError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _validate_component(component: str) -> None:
    if (
        not component
        or component in {".", ".."}
        or component[-1:] in {" ", "."}
        or _CONTROL.search(component)
        or "\\" in component
        or any(character in component for character in "*?")
        or "://" in component
    ):
        raise SkillContractError("SKM003", f"unsafe portable skill path component: {component!r}")
    try:
        component.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SkillContractError("SKM003", "portable skill paths must be UTF-8") from exc
    stem = component.split(".", 1)[0].casefold()
    if stem in _WINDOWS_RESERVED:
        raise SkillContractError("SKM003", f"reserved portable skill path component: {component!r}")


def _portable_files(root: Path) -> list[tuple[str, Path]]:
    if not root.is_dir() or root.is_symlink() or _is_reparse_point(root):
        raise SkillContractError("SKM001", "portable skill root must be a regular directory")
    result: list[tuple[str, Path]] = []
    seen_casefolded: dict[str, str] = {}

    def visit(directory: Path, relative_parts: tuple[str, ...]) -> None:
        try:
            entries = list(os.scandir(directory))
        except OSError as exc:
            raise SkillContractError("SKM002", "portable skill directory could not be enumerated") from exc
        for entry in sorted(entries, key=lambda item: item.name.encode("utf-8", "surrogatepass")):
            _validate_component(entry.name)
            path = Path(entry.path)
            parts = (*relative_parts, entry.name)
            relative = "/".join(parts)
            casefolded = relative.casefold()
            prior = seen_casefolded.get(casefolded)
            if prior is not None and prior != relative:
                raise SkillContractError("SKM004", f"case-colliding portable paths: {prior!r} and {relative!r}")
            seen_casefolded[casefolded] = relative
            if entry.is_symlink() or _is_reparse_point(path):
                raise SkillContractError("SKM005", f"portable skill contains a link or reparse point: {relative}")
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                raise SkillContractError("SKM002", f"portable skill entry could not be inspected: {relative}") from exc
            if stat.S_ISDIR(mode):
                visit(path, parts)
            elif stat.S_ISREG(mode):
                result.append((relative, path))
                if len(result) > MAX_SKILL_FILES:
                    raise SkillContractError("SKM006", "portable skill exceeds the bounded file count")
            else:
                raise SkillContractError("SKM005", f"portable skill contains a special file: {relative}")

    visit(root, ())
    return sorted(result, key=lambda item: item[0].encode("utf-8"))


def _canonical_text(path: Path, relative: str) -> bytes:
    if path.is_symlink() or _is_reparse_point(path) or not path.is_file():
        raise SkillContractError("SKM005", f"portable skill file is no longer regular: {relative}")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SkillContractError("SKM002", f"portable skill file could not be read: {relative}") from exc
    if len(raw) > MAX_SKILL_FILE_BYTES:
        raise SkillContractError("SKM006", f"portable skill file exceeds the bounded size: {relative}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SkillContractError("SKM007", f"portable skill file is not UTF-8: {relative}") from exc
    if text.startswith("\ufeff"):
        raise SkillContractError("SKM007", f"portable skill file has a UTF-8 byte-order mark: {relative}")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def build_skill_manifest(root: Path) -> SkillManifest:
    """Validate and bind every regular UTF-8 text file in one portable core."""

    root = root.expanduser()
    files = _portable_files(root)
    paths = {relative for relative, _ in files}
    missing = sorted({"SKILL.md", "skill-contract.json"} - paths)
    if not files or missing:
        detail = f"; missing: {', '.join(missing)}" if missing else ""
        raise SkillContractError("SKM008", f"portable skill is empty or incomplete{detail}")

    records: list[dict[str, str]] = []
    total = 0
    for relative, path in files:
        canonical = _canonical_text(path, relative)
        total += len(canonical)
        if total > MAX_SKILL_BYTES:
            raise SkillContractError("SKM006", "portable skill exceeds the bounded total size")
        records.append(
            {
                "mode": TEXT_MODE,
                "path": relative,
                "sha256": hashlib.sha256(canonical).hexdigest(),
            }
        )
        if relative == "skill-contract.json":
            parse_skill_contract_bytes(canonical)

    value: dict[str, Any] = {"files": records, "schema": MANIFEST_SCHEMA}
    encoded = canonical_json_bytes(value)
    return SkillManifest(value, encoded, hashlib.sha256(encoded).hexdigest())


__all__ = [
    "CANONICAL_JSON_SCHEMA",
    "CONTRACT_SCHEMA",
    "MANIFEST_SCHEMA",
    "RECEIPT_SCHEMA",
    "TEXT_MODE",
    "SkillContract",
    "SkillContractError",
    "SkillManifest",
    "build_skill_manifest",
    "canonical_json_bytes",
    "load_skill_contract",
    "parse_skill_contract_bytes",
]
