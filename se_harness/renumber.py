"""Plan and apply explicit, evidence-preserving artifact renumbering."""

from __future__ import annotations

import bisect
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
import uuid
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from se_harness import __version__
from se_harness.artifact_layout import ARTIFACT_PREFIXES, ID_PATTERN
from se_harness.installer import HarnessError, ensure_target, load_lock, safe_destination, template_root


SCHEMA = "se-harness-renumber-v1"
AUTHORITY_BOUNDARY = (
    "This command does not approve, verify, release, commit, reserve an identifier, "
    "or exercise any external authority."
)
ELIGIBLE_STATUSES = {"draft", "approved", "in_progress", "implemented"}
RECORD_TYPES = {"verification_record", "release_record"}
RECOVERY_PREFIX = ".harness-renumber-recovery-"
MAX_MAPPINGS = 64
MAX_TRACKED_FILES = 100_000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_REFERENCES = 20_000
MAX_PATH_BYTES = 4096
WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


class RenumberError(HarnessError):
    """A stable renumbering boundary failure."""

    def __init__(self, code: str, phase: str, message: str, *, subject: str = "") -> None:
        super().__init__(_bounded(message, 1000))
        self.code = code
        self.phase = phase
        self.subject = _bounded(subject, 512)

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "phase": self.phase,
            "subject": self.subject,
            "message": str(self),
        }


@dataclass(frozen=True, order=True)
class IdentifierMapping:
    old: str
    new: str


@dataclass(frozen=True, order=True)
class StructuredChange:
    original_path: str
    resulting_path: str
    line: int
    field: str
    old_id: str
    new_id: str


@dataclass(frozen=True, order=True)
class ManualReference:
    original_path: str
    resulting_path: str
    line: int
    column: int
    old_id: str
    new_id: str
    occurrences: int = 1


@dataclass(frozen=True, order=True)
class PreservedEvidenceReference:
    original_path: str
    resulting_path: str
    old_id: str
    occurrences: int
    sha256: str


@dataclass(frozen=True, order=True)
class UnsupportedReference:
    original_path: str
    resulting_path: str
    old_id: str
    occurrences: int
    reason: str


@dataclass(frozen=True)
class TrackedFile:
    path: str
    git_mode: str
    object_id: str
    permissions: int
    content: bytes


@dataclass(frozen=True)
class ParsedArtifact:
    artifact_id: str
    artifact_type: str
    status: str
    path: str
    metadata: dict[str, Any] = field(compare=False, repr=False)
    text: str = field(compare=False, repr=False)
    bom: bool = field(compare=False, repr=False)
    id_span: tuple[int, int, int] = field(compare=False, repr=False)
    relation_spans: tuple[tuple[int, int, int, str], ...] = field(compare=False, repr=False)


@dataclass(frozen=True)
class FileChange:
    original_path: str
    resulting_path: str
    git_mode: str
    permissions: int
    before_sha256: str
    after_sha256: str
    before: bytes = field(compare=False, repr=False)
    after: bytes = field(compare=False, repr=False)


@dataclass(frozen=True)
class RenumberPlan:
    repository_root: Path = field(compare=False, repr=False)
    original_head: str
    mappings: tuple[IdentifierMapping, ...]
    selected_artifacts: tuple[dict[str, str], ...]
    structured_changes: tuple[StructuredChange, ...]
    file_changes: tuple[FileChange, ...] = field(compare=False, repr=False)
    path_moves: tuple[dict[str, str], ...]
    evidence_path_moves: tuple[dict[str, str], ...]
    manual_references: tuple[ManualReference, ...]
    preserved_evidence_references: tuple[PreservedEvidenceReference, ...]
    unsupported_references: tuple[UnsupportedReference, ...]
    validation: dict[str, Any]

    @property
    def manual_action_required(self) -> bool:
        return bool(self.manual_references or self.unsupported_references)

    @property
    def repository_repair_complete(self) -> bool:
        return not self.manual_action_required

    def public_dict(
        self,
        *,
        mode: str,
        applied: bool,
        rollback_outcome: str = "not-needed",
    ) -> dict[str, Any]:
        changed_files = [
            {
                "original_path": item.original_path,
                "resulting_path": item.resulting_path,
                "before_sha256": item.before_sha256,
                "after_sha256": item.after_sha256,
                "git_mode": item.git_mode,
            }
            for item in self.file_changes
        ]
        return {
            "schema": SCHEMA,
            "command_version": __version__,
            "mode": mode,
            "applied": applied,
            "automatic": False,
            "repository_root": str(self.repository_root),
            "original_head": self.original_head,
            "mappings": [asdict(item) for item in self.mappings],
            "selected_artifacts": list(self.selected_artifacts),
            "structured_changes": [asdict(item) for item in self.structured_changes],
            "changed_files": changed_files,
            "path_moves": list(self.path_moves),
            "evidence_path_moves": list(self.evidence_path_moves),
            "manual_references": [asdict(item) for item in self.manual_references],
            "preserved_evidence_references": [
                asdict(item) for item in self.preserved_evidence_references
            ],
            "unsupported_references": [asdict(item) for item in self.unsupported_references],
            "manual_action_required": self.manual_action_required,
            "repository_repair_complete": self.repository_repair_complete,
            "blockers": [],
            "warnings": [],
            "validation": self.validation,
            "rollback_outcome": rollback_outcome,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }

    def fingerprint(self) -> str:
        value = self.public_dict(mode="plan", applied=False)
        value.pop("mode")
        value.pop("applied")
        value.pop("rollback_outcome")
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(payload.encode("ascii")).hexdigest()


def _fail(code: str, phase: str, message: str, subject: str = "") -> RenumberError:
    return RenumberError(code, phase, message, subject=subject)


def _bounded(value: object, limit: int) -> str:
    text = str(value)
    return text if len(text) <= limit else f"{text[:limit]}..."


def _human(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=True)[1:-1]


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int = 60,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            check=False,
            capture_output=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise _fail("REN001", "inventory", f"command failed to start safely: {exc}") from exc


def _decode_output(value: bytes, label: str) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _fail("REN002", "inventory", f"{label} was not valid UTF-8") from exc


def _git(root: Path, *arguments: str, allow: Iterable[int] = (0,)) -> subprocess.CompletedProcess[bytes]:
    executable = shutil.which("git")
    if executable is None:
        raise _fail("REN003", "inventory", "Git is required for artifact renumbering")
    environment = os.environ.copy()
    for name in tuple(environment):
        if name.startswith("GIT_"):
            environment.pop(name, None)
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    environment["GIT_TERMINAL_PROMPT"] = "0"
    completed = _run(
        [
            executable,
            "-c",
            "core.fsmonitor=false",
            "-c",
            "core.untrackedCache=false",
            "-C",
            str(root),
            *arguments,
        ],
        cwd=root,
        environment=environment,
    )
    if completed.returncode not in set(allow):
        detail = _decode_output(completed.stderr, "Git diagnostic").strip().splitlines()
        message = detail[0] if detail else "Git command failed"
        raise _fail("REN004", "inventory", message)
    return completed


def _repository(target: Path) -> tuple[Path, str]:
    target = ensure_target(target, must_exist=True)
    root_result = _git(target, "rev-parse", "--show-toplevel")
    root_text = _decode_output(root_result.stdout, "repository root").strip()
    if not root_text:
        raise _fail("REN005", "inventory", "target is not an ordinary Git worktree")
    root = Path(root_text).resolve()
    bare = _decode_output(
        _git(root, "rev-parse", "--is-bare-repository").stdout,
        "bare-repository result",
    ).strip()
    if bare != "false":
        raise _fail("REN006", "inventory", "bare repositories cannot be renumbered")
    recovery = sorted(path.name for path in root.glob(f"{RECOVERY_PREFIX}*") if path.exists())
    if recovery:
        raise _fail(
            "REN007",
            "inventory",
            f"unfinished renumber recovery state requires inspection: {recovery[0]}",
            recovery[0],
        )
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD", "rebase-apply", "rebase-merge", "sequencer"):
        marker_text = _decode_output(
            _git(root, "rev-parse", "--git-path", marker).stdout,
            "Git state path",
        ).strip()
        marker_path = Path(marker_text)
        if not marker_path.is_absolute():
            marker_path = root / marker_path
        if marker_path.exists():
            raise _fail("REN008", "inventory", f"Git operation is in progress: {marker}", marker)
    head = _decode_output(_git(root, "rev-parse", "HEAD").stdout, "HEAD").strip().lower()
    if len(head) not in {40, 64} or re.fullmatch(r"[0-9a-f]+", head) is None:
        raise _fail("REN009", "inventory", "HEAD did not resolve to a full supported object ID")
    status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if status.stdout:
        raise _fail("REN010", "inventory", "renumbering requires a clean Git worktree")
    return root, head


def normalize_mappings(values: Iterable[str]) -> tuple[IdentifierMapping, ...]:
    supplied = list(values)
    if not supplied:
        raise _fail("REN011", "input", "at least one --map OLD=NEW is required")
    if len(supplied) > MAX_MAPPINGS:
        raise _fail("REN012", "input", f"mapping count exceeds {MAX_MAPPINGS}")
    mappings: list[IdentifierMapping] = []
    for value in supplied:
        if not isinstance(value, str) or value.count("=") != 1:
            raise _fail("REN013", "input", "each mapping must contain exactly one OLD=NEW pair", str(value))
        old, new = (part.strip() for part in value.split("=", 1))
        if ID_PATTERN.fullmatch(old) is None or ID_PATTERN.fullmatch(new) is None:
            raise _fail("REN014", "input", "mapping identifiers must use the formal ID grammar", value)
        if old == new:
            raise _fail("REN015", "input", "old and new identifiers must differ", old)
        mappings.append(IdentifierMapping(old, new))
    old_values = [item.old for item in mappings]
    new_values = [item.new for item in mappings]
    if len(set(old_values)) != len(old_values):
        raise _fail("REN016", "input", "mapping contains a duplicate old identifier")
    if len(set(new_values)) != len(new_values):
        raise _fail("REN017", "input", "mapping contains a duplicate new identifier")
    overlap = sorted(set(old_values) & set(new_values))
    if overlap:
        raise _fail("REN018", "input", "mapping chains and cycles are unsupported", overlap[0])
    all_values = old_values + new_values
    for old in old_values:
        nested = next(
            (
                value
                for value in all_values
                if value != old and _token_pattern(old).search(value) is not None
            ),
            None,
        )
        if nested is not None:
            raise _fail(
                "REN018",
                "input",
                "mapping identifiers contain an ambiguous nested old-identifier token",
                f"{old} in {nested}",
            )
    return tuple(sorted(mappings))


def _validator_report(root: Path) -> dict[str, Any]:
    script = template_root() / "scripts" / "validate_engineering_artifacts.py"
    if not script.is_file():
        raise _fail("REN019", "inventory", f"missing installed validator: {script}")
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONNOUSERSITE"] = "1"
    completed = _run(
        [sys.executable, "-B", str(script), "--root", str(root), "--json"],
        cwd=root,
        environment=environment,
    )
    try:
        report = json.loads(_decode_output(completed.stdout, "validator output"))
    except json.JSONDecodeError as exc:
        raise _fail("REN020", "inventory", "validator did not return its JSON contract") from exc
    if completed.returncode != 0 or not report.get("valid"):
        errors = report.get("errors", [])
        first = errors[0].get("message") if errors and isinstance(errors[0], dict) else "artifact graph is invalid"
        raise _fail("REN021", "inventory", f"artifact graph must be valid before renumbering: {first}")
    return report


def _tracked_files(root: Path) -> tuple[TrackedFile, ...]:
    completed = _git(root, "ls-files", "--stage", "-z")
    records = completed.stdout.split(b"\0")
    records = records[:-1] if records and records[-1] == b"" else records
    if len(records) > MAX_TRACKED_FILES:
        raise _fail("REN022", "inventory", f"tracked file count exceeds {MAX_TRACKED_FILES}")
    result: list[TrackedFile] = []
    aggregate = 0
    for record in records:
        try:
            header, raw_path = record.split(b"\t", 1)
            git_mode, object_id, stage = header.decode("ascii").split(" ")
            relative = raw_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise _fail("REN023", "inventory", "Git returned an unsupported tracked-path record") from exc
        if stage != "0":
            raise _fail("REN024", "inventory", "unmerged index entries cannot be renumbered", relative)
        _validate_relative_path(relative, phase="inventory")
        if git_mode == "160000":
            result.append(TrackedFile(relative, git_mode, object_id, 0, b""))
            continue
        if git_mode == "120000":
            blob = _git(root, "cat-file", "blob", object_id).stdout
            result.append(TrackedFile(relative, git_mode, object_id, 0, blob))
            aggregate += len(blob)
            continue
        path = safe_destination(root, Path(*PurePosixPath(relative).parts))
        try:
            info = path.stat(follow_symlinks=False)
            content = path.read_bytes()
        except OSError as exc:
            raise _fail("REN025", "inventory", f"cannot read tracked file: {exc}", relative) from exc
        if not stat.S_ISREG(info.st_mode):
            raise _fail("REN026", "inventory", "tracked path is not a regular file", relative)
        if len(content) > MAX_FILE_BYTES:
            raise _fail("REN027", "inventory", f"tracked file exceeds {MAX_FILE_BYTES} bytes", relative)
        aggregate += len(content)
        if aggregate > MAX_TOTAL_BYTES:
            raise _fail("REN028", "inventory", f"tracked byte inventory exceeds {MAX_TOTAL_BYTES}")
        result.append(
            TrackedFile(relative, git_mode, object_id, stat.S_IMODE(info.st_mode), content)
        )
    return tuple(sorted(result, key=lambda item: item.path))


def _validate_relative_path(value: str, *, phase: str) -> None:
    if not value or "\\" in value or len(value.encode("utf-8")) > MAX_PATH_BYTES:
        raise _fail("REN029", phase, "path is empty, non-normalized, or too long", value)
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise _fail("REN030", phase, "path is not a normalized repository-relative path", value)


def _validate_destination_path(value: str) -> None:
    _validate_relative_path(value, phase="plan")
    for component in PurePosixPath(value).parts:
        if len(component.encode("utf-8")) > 255:
            raise _fail("REN031", "plan", "destination component is too long", value)
        if component.endswith((".", " ")) or any(ord(char) < 32 for char in component):
            raise _fail("REN032", "plan", "destination is not portable across supported filesystems", value)
        if any(char in '<>:"\\|?*' for char in component):
            raise _fail("REN032", "plan", "destination is not portable across supported filesystems", value)
        stem = component.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED:
            raise _fail("REN033", "plan", "destination uses a reserved filesystem name", value)


def _is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _validate_path_chain(root: Path, value: str, *, phase: str) -> Path:
    parts = PurePosixPath(value).parts
    probe = root
    for part in parts:
        probe = probe / part
        if probe.exists() or _is_link_like(probe):
            if _is_link_like(probe):
                raise _fail("REN080", phase, "affected path traverses a link or reparse point", value)
    return safe_destination(root, Path(*parts))


def _decode_utf8(content: bytes) -> tuple[str, bool]:
    bom = content.startswith(b"\xef\xbb\xbf")
    payload = content[3:] if bom else content
    return payload.decode("utf-8"), bom


def _line_without_ending(value: str) -> str:
    return value[:-2] if value.endswith("\r\n") else value[:-1] if value.endswith(("\n", "\r")) else value


def _quoted_literals(line: str, base: int) -> list[tuple[int, int, str]]:
    result: list[tuple[int, int, str]] = []
    index = 0
    while index < len(line):
        character = line[index]
        if character == "#":
            break
        if character not in {"'", '"'}:
            index += 1
            continue
        quote = character
        start = index + 1
        index += 1
        escaped = False
        while index < len(line):
            current = line[index]
            if quote == '"' and current == "\\":
                escaped = True
                index += 2
                continue
            if current == quote:
                raw = line[start:index]
                if not escaped:
                    result.append((base + start, base + index, raw))
                index += 1
                break
            index += 1
        else:
            break
    return result


def _nested_occurrences(value: Any, targets: set[str]) -> int:
    if isinstance(value, str):
        return int(value in targets)
    if isinstance(value, list):
        return sum(_nested_occurrences(item, targets) for item in value)
    if isinstance(value, dict):
        return sum(_nested_occurrences(item, targets) for item in value.values())
    return 0


def _parse_artifact(entry: dict[str, Any], tracked: dict[str, TrackedFile]) -> ParsedArtifact:
    path = entry.get("path")
    if not isinstance(path, str) or path not in tracked:
        raise _fail("REN034", "inventory", "formal artifact is not a regular tracked file", str(path))
    tracked_file = tracked[path]
    if tracked_file.git_mode in {"120000", "160000"}:
        raise _fail("REN035", "inventory", "formal artifact cannot be linked or a submodule", path)
    try:
        text, bom = _decode_utf8(tracked_file.content)
    except UnicodeDecodeError as exc:
        raise _fail("REN036", "inventory", "formal artifact is not valid UTF-8", path) from exc
    lines = text.splitlines(keepends=True)
    if not lines or _line_without_ending(lines[0]) != "+++":
        raise _fail("REN037", "inventory", "formal artifact has no TOML front matter", path)
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if _line_without_ending(line) == "+++"),
        None,
    )
    if closing is None:
        raise _fail("REN038", "inventory", "formal artifact front matter is not closed", path)
    metadata_text = "".join(lines[1:closing])
    try:
        metadata = tomllib.loads(metadata_text)
    except tomllib.TOMLDecodeError as exc:
        raise _fail("REN039", "inventory", f"formal artifact metadata is invalid: {exc}", path) from exc
    artifact_id = entry.get("id")
    artifact_type = entry.get("type")
    status = entry.get("status")
    if not all(isinstance(item, str) for item in (artifact_id, artifact_type, status)):
        raise _fail("REN040", "inventory", "validator artifact entry is incomplete", path)
    offset = len(lines[0])
    active_table: str | None = None
    id_spans: list[tuple[int, int, int]] = []
    relation_spans: list[tuple[int, int, int, str]] = []
    header_pattern = re.compile(r"^\s*\[([A-Za-z0-9_.-]+)\]\s*(?:#.*)?$")
    id_pattern = re.compile(r"^\s*id\s*=\s*(['\"])([A-Z][A-Z0-9-]*-\d{3})\1\s*(?:#.*)?$")
    for line_number, raw_line in enumerate(lines[1:closing], start=2):
        line = _line_without_ending(raw_line)
        header = header_pattern.fullmatch(line)
        if header is not None:
            active_table = header.group(1)
        elif active_table is None:
            match = id_pattern.fullmatch(line)
            if match is not None:
                start = offset + match.start(2)
                id_spans.append((start, start + len(match.group(2)), line_number))
        elif active_table == "relations":
            for start, end, literal in _quoted_literals(line, offset):
                if ID_PATTERN.fullmatch(literal) is not None:
                    relation_spans.append((start, end, line_number, literal))
        offset += len(raw_line)
    if len(id_spans) != 1 or text[id_spans[0][0] : id_spans[0][1]] != artifact_id:
        raise _fail("REN041", "inventory", "formal artifact ID field cannot be located exactly", path)
    relations = metadata.get("relations", {})
    if not isinstance(relations, dict):
        raise _fail("REN042", "inventory", "formal artifact relations table is invalid", path)
    parsed_relation_ids = sorted(
        item
        for value in relations.values()
        if isinstance(value, list)
        for item in value
        if isinstance(item, str) and ID_PATTERN.fullmatch(item) is not None
    )
    located_relation_ids = sorted(item[3] for item in relation_spans)
    if parsed_relation_ids != located_relation_ids:
        raise _fail(
            "REN043",
            "inventory",
            "typed relation values cannot be located without rewriting unrelated text",
            path,
        )
    return ParsedArtifact(
        artifact_id,
        artifact_type,
        status,
        path,
        metadata,
        text,
        bom,
        id_spans[0],
        tuple(relation_spans),
    )


def _token_pattern(identifier: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(identifier)}(?![A-Za-z0-9])")


def _byte_occurrences(content: bytes, identifier: str) -> list[int]:
    token = identifier.encode("ascii")
    result: list[int] = []
    start = 0
    ascii_alnum = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    while True:
        index = content.find(token, start)
        if index < 0:
            return result
        before = content[index - 1] if index else None
        after_index = index + len(token)
        after = content[after_index] if after_index < len(content) else None
        if (before is None or before not in ascii_alnum) and (after is None or after not in ascii_alnum):
            result.append(index)
        start = index + len(token)


def _mapped_path(path: str, mappings: tuple[IdentifierMapping, ...]) -> str:
    result = path
    for mapping in mappings:
        result = _token_pattern(mapping.old).sub(mapping.new, result)
    return result


def _evidence_path(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return len(parts) >= 4 and parts[:2] == ("docs", "engineering") and "evidence" in parts[2:-1]


def _line_starts(text: str) -> tuple[int, ...]:
    return (0, *(match.end() for match in re.finditer(r"\r\n|\r|\n", text)))


def _line_column(starts: tuple[int, ...], offset: int) -> tuple[int, int]:
    line = bisect.bisect_right(starts, offset)
    return line, offset - starts[line - 1] + 1


def _apply_text_patches(
    text: str,
    patches: list[tuple[int, int, str]],
) -> str:
    result = text
    previous = len(text) + 1
    for start, end, replacement in sorted(patches, reverse=True):
        if start < 0 or end > len(text) or start >= end or end > previous:
            raise _fail("REN044", "plan", "structured text patches overlap or escape their file")
        result = result[:start] + replacement + result[end:]
        previous = start
    return result


def _frontmatter_contains(metadata: dict[str, Any], identifiers: set[str]) -> bool:
    return _nested_occurrences(metadata, identifiers) > 0


def _protected_paths(root: Path) -> set[str]:
    try:
        lock = load_lock(root)
    except HarnessError as exc:
        raise _fail("REN045", "inventory", f"cannot validate managed-file ownership: {exc}") from exc
    entries = lock.get("files", {})
    if not isinstance(entries, dict):
        return set()
    return {
        path
        for path, value in entries.items()
        if isinstance(path, str)
        and isinstance(value, dict)
        and value.get("mode") in {"managed", "fragment"}
    }


def build_renumber_plan(target: Path, mapping_values: Iterable[str]) -> RenumberPlan:
    mappings = normalize_mappings(mapping_values)
    root, head = _repository(target)
    report = _validator_report(root)
    tracked_files = _tracked_files(root)
    tracked = {item.path: item for item in tracked_files}
    artifact_entries = [item for item in report.get("artifacts", []) if isinstance(item, dict)]
    artifacts = tuple(_parse_artifact(item, tracked) for item in artifact_entries)
    by_id = {item.artifact_id: item for item in artifacts}
    if len(by_id) != len(artifacts):
        raise _fail("REN046", "plan", "artifact identifiers are not unique")
    selected: list[dict[str, str]] = []
    mapping_by_old = {item.old: item for item in mappings}
    all_ids = set(by_id)
    for mapping in mappings:
        artifact = by_id.get(mapping.old)
        if artifact is None:
            raise _fail("REN047", "plan", "old identifier does not resolve to one artifact", mapping.old)
        if artifact.artifact_type in RECORD_TYPES:
            raise _fail("REN048", "plan", "verification and release records cannot be renumbered", mapping.old)
        if artifact.status not in ELIGIBLE_STATUSES:
            raise _fail("REN049", "plan", f"artifact lifecycle is not eligible: {artifact.status}", mapping.old)
        expected_prefix = ARTIFACT_PREFIXES.get(artifact.artifact_type)
        if expected_prefix is None or not mapping.new.startswith(expected_prefix):
            raise _fail("REN050", "plan", "new identifier is not type-compatible", mapping.new)
        if mapping.new in all_ids:
            raise _fail("REN051", "plan", "new identifier already exists", mapping.new)
        selected.append(
            {
                "old_id": mapping.old,
                "new_id": mapping.new,
                "type": artifact.artifact_type,
                "status": artifact.status,
                "source_path": artifact.path,
                "resulting_path": _mapped_path(artifact.path, mappings),
            }
        )
    old_ids = set(mapping_by_old)
    for artifact in artifacts:
        if artifact.artifact_type in RECORD_TYPES and (
            _frontmatter_contains(artifact.metadata, old_ids)
            or any(_byte_occurrences(tracked[artifact.path].content, old) for old in old_ids)
        ):
            raise _fail(
                "REN052",
                "plan",
                "commit-bound verification or release provenance references a selected identifier",
                artifact.artifact_id,
            )

    resulting_paths = {item.path: _mapped_path(item.path, mappings) for item in tracked_files}
    for original, resulting in resulting_paths.items():
        if resulting != original:
            _validate_destination_path(resulting)
    exact_results: dict[str, str] = {}
    for original, resulting in sorted(resulting_paths.items()):
        prior = exact_results.setdefault(resulting, original)
        if prior != original:
            raise _fail("REN053", "plan", "multiple paths map to one destination", resulting)
    folded_results: dict[str, set[str]] = {}
    for resulting in resulting_paths.values():
        folded_results.setdefault(resulting.casefold(), set()).add(resulting)
    for original, resulting in resulting_paths.items():
        if resulting == original:
            continue
        if len(folded_results[resulting.casefold()]) > 1:
            raise _fail("REN054", "plan", "destination has a case-folding collision", resulting)
    for original, resulting in resulting_paths.items():
        if resulting == original:
            continue
        destination = _validate_path_chain(root, resulting, phase="plan")
        if destination.exists() or destination.is_symlink():
            raise _fail("REN055", "plan", "destination already exists", resulting)
        ignored = _git(
            root,
            "check-ignore",
            "-q",
            "--no-index",
            "--",
            resulting,
            allow=(0, 1),
        )
        if ignored.returncode == 0:
            raise _fail("REN081", "plan", "destination would be hidden by Git ignore rules", resulting)

    artifact_by_path = {item.path: item for item in artifacts}
    structured_changes: list[StructuredChange] = []
    file_changes: list[FileChange] = []
    manual_references: list[ManualReference] = []
    preserved_references: list[PreservedEvidenceReference] = []
    unsupported_references: list[UnsupportedReference] = []
    path_moves: list[dict[str, str]] = []
    evidence_moves: list[dict[str, str]] = []
    protected = _protected_paths(root)
    reference_count = 0

    for tracked_file in tracked_files:
        original = tracked_file.path
        resulting = resulting_paths[original]
        moved = resulting != original
        if moved:
            movement = {"original_path": original, "resulting_path": resulting}
            path_moves.append(movement)
            if _evidence_path(original):
                evidence_moves.append(movement)
        link_like = tracked_file.git_mode in {"120000", "160000"}
        linked_occurrence = any(_byte_occurrences(tracked_file.content, item.old) for item in mappings)
        if link_like and (moved or linked_occurrence):
            raise _fail("REN056", "plan", "affected linked paths and submodules are unsupported", original)
        patches: list[tuple[int, int, str]] = []
        excluded_spans: set[tuple[int, int]] = set()
        artifact = artifact_by_path.get(original)
        if artifact is not None:
            mapping = mapping_by_old.get(artifact.artifact_id)
            if mapping is not None:
                start, end, line = artifact.id_span
                patches.append((start, end, mapping.new))
                excluded_spans.add((start, end))
                structured_changes.append(
                    StructuredChange(original, resulting, line, "id", mapping.old, mapping.new)
                )
            for start, end, line, relation_id in artifact.relation_spans:
                relation_mapping = mapping_by_old.get(relation_id)
                if relation_mapping is None:
                    continue
                patches.append((start, end, relation_mapping.new))
                excluded_spans.add((start, end))
                structured_changes.append(
                    StructuredChange(
                        original,
                        resulting,
                        line,
                        "relations",
                        relation_mapping.old,
                        relation_mapping.new,
                    )
                )
        after = tracked_file.content
        if patches:
            assert artifact is not None
            rewritten = _apply_text_patches(artifact.text, patches)
            after = (b"\xef\xbb\xbf" if artifact.bom else b"") + rewritten.encode("utf-8")
        content_changed = after != tracked_file.content
        if (content_changed or moved) and original in protected:
            raise _fail("REN057", "plan", "renumbering would modify a protected managed file", original)
        if content_changed or moved:
            path = _validate_path_chain(root, original, phase="plan")
            try:
                info = path.stat(follow_symlinks=False)
            except OSError as exc:
                raise _fail("REN058", "plan", f"cannot assess affected path: {exc}", original) from exc
            if getattr(info, "st_nlink", 1) > 1:
                raise _fail("REN059", "plan", "affected hard-linked files are unsupported", original)
            file_changes.append(
                FileChange(
                    original,
                    resulting,
                    tracked_file.git_mode,
                    tracked_file.permissions,
                    _sha256(tracked_file.content),
                    _sha256(after),
                    tracked_file.content,
                    after,
                )
            )

        if _evidence_path(original):
            digest = _sha256(tracked_file.content)
            for mapping in mappings:
                count = len(_byte_occurrences(tracked_file.content, mapping.old))
                if count:
                    reference_count += count
                    preserved_references.append(
                        PreservedEvidenceReference(original, resulting, mapping.old, count, digest)
                    )
            if reference_count > MAX_REFERENCES:
                raise _fail("REN060", "plan", f"reference count exceeds {MAX_REFERENCES}")
            continue
        try:
            text, _ = _decode_utf8(tracked_file.content)
            binary_reason = "embedded-nul" if "\x00" in text else ""
        except UnicodeDecodeError:
            text = ""
            binary_reason = "non-utf8"
        if binary_reason:
            for mapping in mappings:
                count = len(_byte_occurrences(tracked_file.content, mapping.old))
                if count:
                    reference_count += count
                    unsupported_references.append(
                        UnsupportedReference(original, resulting, mapping.old, count, binary_reason)
                    )
            if reference_count > MAX_REFERENCES:
                raise _fail("REN060", "plan", f"reference count exceeds {MAX_REFERENCES}")
            continue
        resulting_text = _decode_utf8(after)[0] if patches else text
        resulting_line_starts = _line_starts(resulting_text)
        for mapping in mappings:
            for match in _token_pattern(mapping.old).finditer(text):
                if (match.start(), match.end()) in excluded_spans:
                    continue
                result_offset = match.start() + sum(
                    len(replacement) - (end - start)
                    for start, end, replacement in patches
                    if end <= match.start()
                )
                line, column = _line_column(resulting_line_starts, result_offset)
                reference_count += 1
                manual_references.append(
                    ManualReference(original, resulting, line, column, mapping.old, mapping.new)
                )
        if reference_count > MAX_REFERENCES:
            raise _fail("REN060", "plan", f"reference count exceeds {MAX_REFERENCES}")

    validation = {
        "valid": True,
        "artifact_count": len(artifact_entries),
        "error_count": len(report.get("errors", [])),
        "warning_count": len(report.get("warnings", [])),
    }
    return RenumberPlan(
        root,
        head,
        mappings,
        tuple(sorted(selected, key=lambda item: item["old_id"])),
        tuple(sorted(structured_changes)),
        tuple(sorted(file_changes, key=lambda item: item.original_path)),
        tuple(sorted(path_moves, key=lambda item: item["original_path"])),
        tuple(sorted(evidence_moves, key=lambda item: item["original_path"])),
        tuple(sorted(manual_references)),
        tuple(sorted(preserved_references)),
        tuple(sorted(unsupported_references)),
        validation,
    )


def _make_parent(root: Path, relative: str, created: list[Path]) -> Path:
    parts = PurePosixPath(relative).parts
    destination = safe_destination(root, Path(*parts))
    probe = root
    for part in parts[:-1]:
        probe = probe / part
        if probe.exists():
            if _is_link_like(probe) or not probe.is_dir():
                raise _fail("REN061", "apply", "destination parent is linked or not a directory", relative)
            continue
        probe.mkdir()
        created.append(probe)
    return destination


def _write_file(path: Path, content: bytes, permissions: int, *, exclusive: bool) -> None:
    if exclusive:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, permissions or 0o600)
        temporary: str | None = None
    else:
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        target = path if exclusive else Path(temporary or "")
        os.chmod(target, permissions)
        if not exclusive:
            os.replace(target, path)
    finally:
        if not exclusive and temporary and os.path.exists(temporary):
            os.unlink(temporary)


def _write_recovery_state(state: Path, plan: RenumberPlan) -> None:
    state.mkdir(mode=0o700)
    originals = state / "originals"
    originals.mkdir(mode=0o700)
    manifest: list[dict[str, Any]] = []
    for index, change in enumerate(plan.file_changes):
        name = f"{index:06d}.bin"
        _write_file(originals / name, change.before, 0o600, exclusive=True)
        manifest.append(
            {
                "backup": name,
                "original_path": change.original_path,
                "resulting_path": change.resulting_path,
                "permissions": change.permissions,
                "before_sha256": change.before_sha256,
            }
        )
    payload = {
        "schema": SCHEMA,
        "original_head": plan.original_head,
        "plan_fingerprint": plan.fingerprint(),
        "files": manifest,
    }
    _write_file(
        state / "manifest.json",
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        0o600,
        exclusive=True,
    )


def _remove_recovery_state(state: Path) -> None:
    resolved = state.resolve()
    if resolved.parent != state.parent.resolve() or not resolved.name.startswith(RECOVERY_PREFIX):
        raise _fail("REN062", "rollback", "recovery state path is outside the transaction boundary")
    shutil.rmtree(resolved)


def _restore(plan: RenumberPlan, created_directories: list[Path]) -> list[str]:
    failures: list[str] = []
    for change in reversed(plan.file_changes):
        try:
            original = safe_destination(
                plan.repository_root,
                Path(*PurePosixPath(change.original_path).parts),
            )
            resulting = safe_destination(
                plan.repository_root,
                Path(*PurePosixPath(change.resulting_path).parts),
            )
            if resulting != original and (resulting.exists() or resulting.is_symlink()):
                resulting.unlink()
            original.parent.mkdir(parents=True, exist_ok=True)
            _write_file(original, change.before, change.permissions, exclusive=False)
        except (OSError, HarnessError) as exc:
            failures.append(f"{change.original_path}: {type(exc).__name__}: {exc}")
    for directory in reversed(created_directories):
        try:
            directory.rmdir()
        except OSError:
            pass
    for change in plan.file_changes:
        original = plan.repository_root / Path(*PurePosixPath(change.original_path).parts)
        try:
            if not original.is_file() or _sha256(original.read_bytes()) != change.before_sha256:
                failures.append(f"{change.original_path}: restoration hash mismatch")
        except OSError as exc:
            failures.append(f"{change.original_path}: restoration check failed: {exc}")
    return failures


def _status_paths(root: Path, *, ignore_recovery: str | None = None) -> set[str]:
    completed = _git(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--no-renames",
    )
    paths: set[str] = set()
    for record in completed.stdout.split(b"\0"):
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise _fail("REN063", "postcondition", "Git status returned an unsupported record")
        path = _decode_output(record[3:], "Git status path")
        if ignore_recovery and (path == ignore_recovery or path.startswith(f"{ignore_recovery}/")):
            continue
        paths.add(path)
    return paths


def _postconditions(plan: RenumberPlan, state_name: str) -> dict[str, Any]:
    if _decode_output(_git(plan.repository_root, "rev-parse", "HEAD").stdout, "HEAD").strip().lower() != plan.original_head:
        raise _fail("REN064", "postcondition", "HEAD changed during renumbering")
    for change in plan.file_changes:
        original = plan.repository_root / Path(*PurePosixPath(change.original_path).parts)
        resulting = plan.repository_root / Path(*PurePosixPath(change.resulting_path).parts)
        if resulting != original and original.exists():
            raise _fail("REN065", "postcondition", "moved source path still exists", change.original_path)
        try:
            content = resulting.read_bytes()
        except OSError as exc:
            raise _fail("REN066", "postcondition", f"cannot read resulting path: {exc}", change.resulting_path) from exc
        if _sha256(content) != change.after_sha256:
            raise _fail("REN067", "postcondition", "resulting file hash does not match the plan", change.resulting_path)
    expected_paths = {
        path
        for change in plan.file_changes
        for path in {change.original_path, change.resulting_path}
    }
    actual_paths = _status_paths(plan.repository_root, ignore_recovery=state_name)
    if actual_paths != expected_paths:
        unexpected = sorted(actual_paths ^ expected_paths)
        raise _fail(
            "REN068",
            "postcondition",
            f"Git reports changes outside the plan: {', '.join(unexpected[:5])}",
        )
    report = _validator_report(plan.repository_root)
    catalog = {
        item.get("id"): item
        for item in report.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for mapping in plan.mappings:
        if mapping.old in catalog or mapping.new not in catalog:
            raise _fail("REN069", "postcondition", "resulting artifact identity is incomplete", mapping.old)
    for item in report.get("artifacts", []):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        path = plan.repository_root / Path(*PurePosixPath(item["path"]).parts)
        try:
            text, _ = _decode_utf8(path.read_bytes())
            lines = text.splitlines()
            closing = lines.index("+++", 1)
            metadata = tomllib.loads("\n".join(lines[1:closing]))
        except (OSError, UnicodeError, ValueError, tomllib.TOMLDecodeError) as exc:
            raise _fail("REN070", "postcondition", f"cannot reassess artifact metadata: {exc}", item["path"]) from exc
        if metadata.get("id") in {mapping.old for mapping in plan.mappings}:
            raise _fail("REN071", "postcondition", "old identifier remains in an id field", item["path"])
        relations = metadata.get("relations", {})
        if _nested_occurrences(relations, {mapping.old for mapping in plan.mappings}):
            raise _fail("REN072", "postcondition", "old identifier remains in a typed relation", item["path"])
    return {
        "valid": True,
        "artifact_count": len(report.get("artifacts", [])),
        "error_count": len(report.get("errors", [])),
        "warning_count": len(report.get("warnings", [])),
    }


def apply_renumber_plan(plan: RenumberPlan) -> RenumberPlan:
    from se_harness import mutation_guard

    mutation_guard.require_mutation_authority(
        plan.repository_root,
        operation="renumber-artifacts-apply",
    )
    refreshed = build_renumber_plan(
        plan.repository_root,
        [f"{item.old}={item.new}" for item in plan.mappings],
    )
    if refreshed.fingerprint() != plan.fingerprint():
        raise _fail("REN073", "apply", "repository plan changed before application")
    plan = refreshed
    state = plan.repository_root / f"{RECOVERY_PREFIX}{os.getpid()}-{uuid.uuid4().hex}"
    created_directories: list[Path] = []
    try:
        _write_recovery_state(state, plan)
        for change in plan.file_changes:
            original = safe_destination(
                plan.repository_root,
                Path(*PurePosixPath(change.original_path).parts),
            )
            if _sha256(original.read_bytes()) != change.before_sha256:
                raise _fail("REN074", "apply", "source changed after plan attestation", change.original_path)
            resulting = _make_parent(plan.repository_root, change.resulting_path, created_directories)
            if resulting != original:
                if resulting.exists() or resulting.is_symlink():
                    raise _fail("REN075", "apply", "destination appeared during application", change.resulting_path)
                _write_file(resulting, change.after, change.permissions, exclusive=True)
                original.unlink()
            else:
                _write_file(original, change.after, change.permissions, exclusive=False)
        validation = _postconditions(plan, state.name)
        plan = replace(plan, validation=validation)
        _remove_recovery_state(state)
        expected_paths = {
            path
            for change in plan.file_changes
            for path in {change.original_path, change.resulting_path}
        }
        if _status_paths(plan.repository_root) != expected_paths:
            raise _fail("REN076", "postcondition", "final Git status changed after recovery cleanup")
        return plan
    except BaseException as exc:
        failures = _restore(plan, created_directories)
        try:
            remaining_status = _status_paths(
                plan.repository_root,
                ignore_recovery=state.name if state.exists() else None,
            )
            if remaining_status:
                failures.append(
                    "restoration left Git changes: " + ", ".join(sorted(remaining_status)[:5])
                )
        except (HarnessError, OSError) as status_error:
            failures.append(f"restoration status check failed: {status_error}")
        if failures:
            detail = "; ".join(failures[:5])
            if isinstance(exc, RenumberError):
                raise _fail(
                    "REN077",
                    "rollback",
                    f"{exc}; rollback was incomplete: {detail}; recovery state: {state.name}",
                    state.name,
                ) from exc
            raise _fail(
                "REN077",
                "rollback",
                f"transaction failed and rollback was incomplete: {detail}; recovery state: {state.name}",
                state.name,
            ) from exc
        if state.exists():
            try:
                _remove_recovery_state(state)
            except (OSError, RenumberError) as cleanup_error:
                raise _fail(
                    "REN078",
                    "rollback",
                    f"transaction was restored but recovery cleanup failed: {cleanup_error}",
                    state.name,
                ) from exc
        if isinstance(exc, RenumberError):
            raise _fail(
                exc.code,
                exc.phase,
                f"{exc}; rollback restored the original repository",
                exc.subject,
            ) from exc
        raise _fail(
            "REN079",
            "apply",
            f"transaction failed and rollback restored the original repository: {type(exc).__name__}: {exc}",
        ) from exc


def render_json_error(error: RenumberError) -> str:
    return json.dumps(
        {
            "schema": SCHEMA,
            "mode": "blocked",
            "applied": False,
            "automatic": False,
            "blockers": [error.to_dict()],
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
        indent=2,
        sort_keys=True,
    )


def render_human_error(error: RenumberError) -> str:
    subject = f" ({_human(error.subject)})" if error.subject else ""
    return f"harnessctl: [{error.code} {error.phase}]{subject} {_human(error)}"


def render_json(plan: RenumberPlan, *, applied: bool) -> str:
    return json.dumps(
        plan.public_dict(mode="apply" if applied else "plan", applied=applied),
        indent=2,
        sort_keys=True,
    )


def render_human(plan: RenumberPlan, *, applied: bool) -> str:
    lines = [
        "STRUCTURED RENUMBERING: APPLIED" if applied else "STRUCTURED RENUMBERING PLAN: READY",
        f"Repository: {_human(plan.repository_root)}",
        f"HEAD: {plan.original_head}",
        "Mappings:",
    ]
    lines.extend(f"  {item.old} -> {item.new}" for item in plan.mappings)
    lines.append(f"Structured field changes: {len(plan.structured_changes)}")
    lines.extend(
        f"  {_human(item.resulting_path)}:{item.line} [{item.field}] {item.old_id} -> {item.new_id}"
        for item in plan.structured_changes
    )
    lines.append(f"Path moves: {len(plan.path_moves)}")
    lines.extend(
        f"  {_human(item['original_path'])} -> {_human(item['resulting_path'])}"
        for item in plan.path_moves
    )
    if plan.manual_references:
        lines.append(
            f"MANUAL ACTION REQUIRED: {len(plan.manual_references)} free-form references must be reviewed and changed or explicitly documented"
        )
        lines.extend(
            f"  {_human(item.resulting_path)}:{item.line}:{item.column}  {item.old_id} -> {item.new_id}"
            for item in plan.manual_references
        )
    else:
        lines.append("MANUAL REFERENCES: none")
    preserved_count = sum(item.occurrences for item in plan.preserved_evidence_references)
    lines.append(
        f"PRESERVED EVIDENCE REFERENCES: {preserved_count} occurrences; do not rewrite captured evidence"
    )
    lines.extend(
        f"  {_human(item.resulting_path)}  {item.old_id} ({item.occurrences}; sha256 {item.sha256})"
        for item in plan.preserved_evidence_references
    )
    if plan.unsupported_references:
        lines.append(
            f"UNSUPPORTED REFERENCES: {len(plan.unsupported_references)} paths require manual inspection"
        )
        lines.extend(
            f"  {_human(item.resulting_path)}  {item.old_id} ({item.occurrences}; {item.reason})"
            for item in plan.unsupported_references
        )
    else:
        lines.append("UNSUPPORTED REFERENCES: none")
    lines.append(
        f"REPOSITORY REPAIR COMPLETE: {'yes' if plan.repository_repair_complete else 'no'}"
    )
    lines.append(
        f"Formal validation: PASS ({plan.validation.get('artifact_count', 0)} artifacts; "
        f"{plan.validation.get('warning_count', 0)} warnings)"
    )
    lines.append("Automatic: false")
    lines.append(
        "No files were written; rerun this exact mapping with --apply after review."
        if not applied
        else "Structured changes were applied and left uncommitted for review."
    )
    lines.append(AUTHORITY_BOUNDARY)
    return "\n".join(lines)
