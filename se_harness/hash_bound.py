"""Declared hash-bound text classes, mode determination and read-only assessment."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.integrity import (
    HASH_MODE,
    IntegrityError,
    canonical_sha256,
    raw_sha256,
)


HASH_BOUND_SCHEMA = "se-harness-hash-bound-classes-v1"
RAW_MODE = "raw"
CANONICAL_MODE = HASH_MODE
MODES = frozenset({RAW_MODE, CANONICAL_MODE})
MATCH_DECLARED = "declared"
MATCH_MISMATCH = "mismatch"
MATCH_RESULTS = (MATCH_DECLARED, MATCH_MISMATCH)
LOCK_RELATIVE = ".engineering-harness.lock"
REGIONS = frozenset({"template", "repository"})
REQUIRED_ATTRIBUTES = frozenset({"text eol=lf"})
CLASS_FIELDS = frozenset({"bindings", "id", "mode", "patterns", "region", "required_attribute"})
UNBOUND_FIELDS = frozenset({"field", "reason"})
CHECK_CLASS_DECLARED = "hash-bound-class-declared"
CHECK_ATTRIBUTE_EFFECTIVE = "hash-bound-attribute-effective"
CHECK_MODE_CONSISTENT = "hash-bound-mode-consistent"
CHECK_NAMES = (CHECK_CLASS_DECLARED, CHECK_ATTRIBUTE_EFFECTIVE, CHECK_MODE_CONSISTENT)
ATTRIBUTES_NAME = ".gitattributes"
ATTRIBUTE_BEGIN_MARKER = "# se-harness:begin"
ATTRIBUTE_END_MARKER = "# se-harness:end"
ARTIFACT_ROOT = "docs/engineering"
_CLASS_ID = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_BINDING = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*_sha256$")
_PATTERN = re.compile(r"^[A-Za-z0-9_.*/-]+$")
_REASON = re.compile(r"^[A-Za-z0-9 ;,.()_-]+$")
_DIGEST_FIELD = re.compile(r"^\s*([a-z][a-z0-9_]*_sha256)\s*=")
_FRONT_MATTER = "+++"
_FRONT_MATTER_LIMIT = 8192
_GIT_TIMEOUT = 60
_MAX_DETAIL_ITEMS = 3


class HashBoundError(ValueError):
    """The hash-bound class declaration is malformed or cannot resolve."""


@dataclass(frozen=True)
class HashBoundClass:
    class_id: str
    patterns: tuple[str, ...]
    mode: str
    required_attribute: str | None
    region: str
    bindings: tuple[str, ...]


@dataclass(frozen=True)
class Declaration:
    classes: tuple[HashBoundClass, ...]
    unbound_digest_fields: tuple[tuple[str, str], ...]

    def binding_owner(self) -> dict[str, str]:
        return {
            binding: item.class_id for item in self.classes for binding in item.bindings
        }

    def unbound_names(self) -> frozenset[str]:
        return frozenset(field for field, _ in self.unbound_digest_fields)


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HashBoundError(f"duplicate declaration key: {key}")
        result[key] = value
    return result


def _text(value: object, label: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise HashBoundError(f"invalid {label}: {value!r}")
    return value


def _pattern(value: object, class_id: str) -> str:
    text = _text(value, f"path pattern in class {class_id}", _PATTERN)
    if text.startswith("/") or ".." in text.split("/"):
        raise HashBoundError(f"invalid path pattern in class {class_id}: {text!r}")
    return text


def _class(raw: object) -> HashBoundClass:
    if not isinstance(raw, Mapping):
        raise HashBoundError("class entries must be objects")
    unknown = set(raw) - CLASS_FIELDS
    if unknown or set(raw) != CLASS_FIELDS:
        raise HashBoundError(f"class entry fields must be exactly {sorted(CLASS_FIELDS)}")
    class_id = _text(raw["id"], "class ID", _CLASS_ID)
    patterns = raw["patterns"]
    if not isinstance(patterns, list) or not patterns:
        raise HashBoundError(f"class {class_id} must declare at least one path pattern")
    mode = raw["mode"]
    if mode not in MODES:
        raise HashBoundError(f"class {class_id} declares unsupported mode {mode!r}")
    region = raw["region"]
    if region not in REGIONS:
        raise HashBoundError(f"class {class_id} declares unsupported region {region!r}")
    attribute = raw["required_attribute"]
    if mode == RAW_MODE:
        if attribute not in REQUIRED_ATTRIBUTES:
            raise HashBoundError(f"raw class {class_id} must require a supported Git attribute")
    elif attribute is not None:
        raise HashBoundError(f"canonical class {class_id} must not require a Git attribute")
    bindings = raw["bindings"]
    if not isinstance(bindings, list):
        raise HashBoundError(f"class {class_id} bindings must be a list")
    return HashBoundClass(
        class_id=class_id,
        patterns=tuple(_pattern(item, class_id) for item in patterns),
        mode=mode,
        required_attribute=attribute,
        region=region,
        bindings=tuple(
            _text(item, f"binding in class {class_id}", _BINDING) for item in bindings
        ),
    )


def load_declaration(path: Path | None = None) -> Declaration:
    """Load the declared hash-bound classes as data, all or nothing."""

    source = path or Path(__file__).with_name("hash_bound_classes.json")
    try:
        raw = json.loads(source.read_bytes().decode("utf-8"), object_pairs_hook=_object)
    except HashBoundError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise HashBoundError(f"cannot load hash-bound declaration {source}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schema") != HASH_BOUND_SCHEMA:
        raise HashBoundError(f"{source} must use schema {HASH_BOUND_SCHEMA}")
    if set(raw) != {"classes", "schema", "unbound_digest_fields"}:
        raise HashBoundError("declaration fields must be schema, classes, unbound_digest_fields")
    entries = raw["classes"]
    if not isinstance(entries, list) or not entries:
        raise HashBoundError("declaration must contain at least one class")
    classes = tuple(_class(item) for item in entries)
    seen: set[str] = set()
    for item in classes:
        if item.class_id in seen:
            raise HashBoundError(f"duplicate class ID: {item.class_id}")
        seen.add(item.class_id)
    unbound = raw["unbound_digest_fields"]
    if not isinstance(unbound, list):
        raise HashBoundError("unbound_digest_fields must be a list")
    fields: list[tuple[str, str]] = []
    for item in unbound:
        if not isinstance(item, Mapping) or set(item) != UNBOUND_FIELDS:
            raise HashBoundError(f"unbound_digest_fields entry fields must be {sorted(UNBOUND_FIELDS)}")
        fields.append(
            (
                _text(item["field"], "unbound digest field", _BINDING),
                _text(item["reason"], "unbound digest reason", _REASON),
            )
        )
    owner = {binding for item in classes for binding in item.bindings}
    collision = owner.intersection(field for field, _ in fields)
    if collision:
        raise HashBoundError(f"digest field is both bound and unbound: {sorted(collision)[0]}")
    counts: dict[str, int] = {}
    for item in classes:
        for binding in item.bindings:
            counts[binding] = counts.get(binding, 0) + 1
    duplicated = sorted(field for field, count in counts.items() if count > 1)
    if duplicated:
        raise HashBoundError(f"digest field is bound by two classes: {duplicated[0]}")
    return Declaration(classes=classes, unbound_digest_fields=tuple(fields))


@lru_cache(maxsize=None)
def _regex(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        character = pattern[index]
        if pattern.startswith("**/", index):
            parts.append(r"(?:[^/]+/)*")
            index += 3
            continue
        if character == "*":
            parts.append(r"[^/]*")
        elif character == "?":
            parts.append(r"[^/]")
        else:
            parts.append(re.escape(character))
        index += 1
    return re.compile("^" + "".join(parts) + "$")


def pattern_specificity(pattern: str) -> int:
    """Return 3 for an exact path, 2 for a bounded prefix, 1 for a wildcard span."""

    components = pattern.split("/")
    if not any(character in pattern for character in "*?"):
        return 3
    if any(character in component for component in components[:-1] for character in "*?"):
        return 1
    return 2


def matches(pattern: str, relative: str) -> bool:
    return _regex(pattern).fullmatch(relative) is not None


def resolve_class(relative: str, declaration: Declaration | None = None) -> HashBoundClass:
    """Return the single class covering a repository-relative POSIX path."""

    known = declaration or load_declaration()
    best: list[tuple[int, HashBoundClass]] = []
    for item in known.classes:
        scores = [
            pattern_specificity(pattern)
            for pattern in item.patterns
            if matches(pattern, relative)
        ]
        if scores:
            best.append((max(scores), item))
    if not best:
        raise HashBoundError(f"no declared hash-bound class covers {relative}")
    top = max(score for score, _ in best)
    winners = sorted({item.class_id for score, item in best if score == top})
    if len(winners) != 1:
        raise HashBoundError(
            f"{relative} is covered at equal specificity by {', '.join(winners)}"
        )
    return next(item for score, item in best if score == top)


def resolve_mode(relative: str, declaration: Declaration | None = None) -> str:
    """Return the hash mode declared for a repository-relative POSIX path.

    Total or failing. A path no class covers raises rather than resolving to a
    default, so no caller can hash a bound file under a mode nothing declared.
    """

    return resolve_class(relative, declaration).mode


def _digest(relative: str, value: bytes, mode: str) -> str:
    if mode == RAW_MODE:
        return raw_sha256(value)
    try:
        return canonical_sha256(value)
    except IntegrityError as exc:
        raise HashBoundError(f"cannot hash {relative} as {mode}: {exc}") from exc


def declared_digest(
    relative: str, value: bytes, declaration: Declaration | None = None
) -> str:
    """Hash bytes under the mode their path's declared class fixes."""

    return _digest(relative, value, resolve_mode(relative, declaration))


def compare_declared_digest(
    relative: str, value: bytes, expected: str, declaration: Declaration | None = None
) -> str:
    """Compare a recorded digest under the path's declared mode.

    A canonical class matches through newline canonicalization only; a raw
    class keeps exact-byte trust. The recognition of schema-1-era digests
    recorded over foreign newlines was removed under WO-HUP-012.
    """

    mode = resolve_mode(relative, declaration)
    if _digest(relative, value, mode) == expected:
        return MATCH_DECLARED
    return MATCH_MISMATCH


def _git(root: Path, arguments: list[str], *, stdin: bytes | None = None) -> bytes:
    executable = shutil.which("git")
    if executable is None:
        raise HashBoundError("git executable is unavailable")
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argument vector, shell=False
            [executable, "-C", str(root), *arguments],
            input=stdin,
            capture_output=True,
            shell=False,
            timeout=_GIT_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise HashBoundError(f"git {arguments[0]} failed: {exc}") from exc
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip().splitlines()
        raise HashBoundError(
            f"git {arguments[0]} exited {completed.returncode}: {detail[0] if detail else 'no output'}"
        )
    return completed.stdout


def is_git_worktree(root: Path) -> bool:
    """Return true when the target can carry tracked files and Git is available."""

    return (root / ".git").exists() and shutil.which("git") is not None


def tracked_paths(root: Path) -> tuple[str, ...]:
    output = _git(root, ["ls-files", "-z"])
    return tuple(sorted(item for item in output.decode("utf-8").split("\0") if item))


def resolved_attributes(root: Path, paths: Iterable[str]) -> dict[str, dict[str, str]]:
    """Return the text and eol attributes Git resolves for each path."""

    selected = list(paths)
    if not selected:
        return {}
    payload = ("\0".join(selected) + "\0").encode("utf-8")
    output = _git(root, ["check-attr", "-z", "--stdin", "text", "eol"], stdin=payload)
    fields = output.decode("utf-8").split("\0")
    result: dict[str, dict[str, str]] = {path: {} for path in selected}
    for index in range(0, len(fields) - 2, 3):
        path, attribute, value = fields[index], fields[index + 1], fields[index + 2]
        if path in result:
            result[path][attribute] = value
    return result


def _attribute_satisfied(resolved: Mapping[str, str], required: str) -> bool:
    if required != "text eol=lf":
        return False
    return resolved.get("text") == "set" and resolved.get("eol") == "lf"


def attribute_regions(root: Path) -> dict[str, tuple[str, ...]]:
    """Split committed .gitattributes lines into template and repository regions."""

    path = root / ATTRIBUTES_NAME
    try:
        text = path.read_bytes().decode("utf-8")
    except FileNotFoundError as exc:
        raise HashBoundError(f"{ATTRIBUTES_NAME} is absent") from exc
    except (OSError, UnicodeError) as exc:
        raise HashBoundError(f"cannot read {ATTRIBUTES_NAME}: {exc}") from exc
    template: list[str] = []
    repository: list[str] = []
    inside = False
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.strip()
        if stripped == ATTRIBUTE_BEGIN_MARKER:
            if inside:
                raise HashBoundError(f"{ATTRIBUTES_NAME} managed markers are duplicated")
            inside = True
            continue
        if stripped == ATTRIBUTE_END_MARKER:
            if not inside:
                raise HashBoundError(f"{ATTRIBUTES_NAME} managed markers are unbalanced")
            inside = False
            continue
        if not stripped or stripped.startswith("#"):
            continue
        (template if inside else repository).append(stripped)
    if inside:
        raise HashBoundError(f"{ATTRIBUTES_NAME} managed markers are unbalanced")
    return {"template": tuple(template), "repository": tuple(repository)}


def _front_matter(path: Path, relative: str) -> list[str] | None:
    """Return the artifact's front-matter lines, reading a bounded prefix first."""

    for limit in (_FRONT_MATTER_LIMIT, None):
        try:
            with path.open("rb") as handle:
                raw = handle.read() if limit is None else handle.read(limit)
        except OSError as exc:
            raise HashBoundError(f"cannot read {relative}: {exc}") from exc
        try:
            text = raw.decode("utf-8")
        except UnicodeError:
            if limit is None:
                raise HashBoundError(f"cannot read {relative}: invalid UTF-8")
            continue
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if not lines or lines[0].strip() != _FRONT_MATTER:
            return None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == _FRONT_MATTER:
                return lines[1:index]
        if limit is None:
            raise HashBoundError(f"cannot read {relative}: front matter is unterminated")
    return None


def digest_fields(root: Path, tracked: Iterable[str] | None = None) -> dict[str, tuple[str, ...]]:
    """Return every recorded *_sha256 front-matter field name and where it appears.

    Only committed artifacts can bind a committed file's bytes, so the scan runs
    over the tracked set rather than the working tree.
    """

    prefix = f"{ARTIFACT_ROOT}/"
    candidates = sorted(
        relative
        for relative in (tracked if tracked is not None else tracked_paths(root))
        if relative.startswith(prefix) and relative.endswith(".md")
    )
    found: dict[str, list[str]] = {}
    for relative in candidates:
        lines = _front_matter(root / relative, relative)
        if lines is None:
            continue
        for line in lines:
            match = _DIGEST_FIELD.match(line)
            if match is not None:
                found.setdefault(match.group(1), []).append(relative)
    return {field: tuple(sorted(set(paths))) for field, paths in found.items()}


def _detail(items: Iterable[str]) -> str:
    selected = sorted(items)
    head = "; ".join(selected[:_MAX_DETAIL_ITEMS])
    remainder = len(selected) - _MAX_DETAIL_ITEMS
    return f"{head} (+{remainder} more)" if remainder > 0 else head


def _class_declared(
    root: Path, declaration: Declaration, tracked: tuple[str, ...]
) -> tuple[bool, str]:
    failures: list[str] = []
    owner = declaration.binding_owner()
    known = declaration.unbound_names()
    for field, paths in sorted(digest_fields(root, tracked).items()):
        if field in owner or field in known:
            continue
        failures.append(f"{paths[0]}: digest field {field} resolves to no declared class")
    vacuous: list[str] = []
    for item in declaration.classes:
        # A `repository`-region class was declared by the owner for paths known
        # to exist, so an empty match is a stale declaration and fails closed. A
        # `template`-region class is the evaluator's promise about files the
        # repository will hold later (evidence before its first record), so it is
        # vacuously declared: reported, never failed (SPEC-HBI-001 rule 9).
        matched = False
        for pattern in item.patterns:
            if any(matches(pattern, relative) for relative in tracked):
                matched = True
            elif item.region == "repository":
                failures.append(f"{item.class_id}: pattern {pattern} matches no tracked path")
        if not matched and item.region == "template":
            vacuous.append(f"{item.class_id}: 0 tracked paths")
    if failures:
        return False, _detail(failures)
    covered = sum(
        1
        for relative in tracked
        if any(
            matches(pattern, relative)
            for item in declaration.classes
            for pattern in item.patterns
        )
    )
    detail = (
        f"{len(declaration.classes)} classes cover {covered} tracked paths; "
        f"{len(declaration.unbound_digest_fields)} digest fields declared out of scope"
    )
    if vacuous:
        detail += "; vacuously declared " + _detail(vacuous)
    return True, detail


def _attribute_effective(
    root: Path, declaration: Declaration, tracked: tuple[str, ...]
) -> tuple[bool, str]:
    failures: list[str] = []
    regions = attribute_regions(root)
    raw_classes = [item for item in declaration.classes if item.mode == RAW_MODE]
    covered: dict[str, list[str]] = {}
    for item in raw_classes:
        paths: list[str] = []
        for pattern in item.patterns:
            declared_in = sorted(
                region
                for region, lines in regions.items()
                if any(line.split()[0] == pattern for line in lines)
            )
            if item.region not in declared_in:
                # A pattern present only in the other region is the misplacement
                # rule 10 makes ineffective. Presence in both regions is not a
                # misplacement: the required region carries it, and a duplicate
                # identical rule cannot change what Git resolves.
                observed = ", ".join(declared_in) if declared_in else "no region"
                failures.append(
                    f"{item.class_id}: pattern {pattern} is declared in {observed}; "
                    f"requires the {item.region} region"
                )
            paths.extend(relative for relative in tracked if matches(pattern, relative))
        covered[item.class_id] = sorted(set(paths))
    resolved = resolved_attributes(
        root, sorted({relative for paths in covered.values() for relative in paths})
    )
    for item in raw_classes:
        required = str(item.required_attribute)
        for relative in covered[item.class_id]:
            values = resolved.get(relative, {})
            if _attribute_satisfied(values, required):
                continue
            observed = ", ".join(
                f"{key}={values.get(key, 'unspecified')}" for key in ("text", "eol")
            )
            failures.append(
                f"{item.class_id}: {relative} resolves {observed}; requires {required}"
            )
    if failures:
        return False, _detail(failures)
    total = len({relative for paths in covered.values() for relative in paths})
    return True, f"{len(raw_classes)} raw classes effective for {total} tracked paths"


def _mode_consistent(declaration: Declaration) -> tuple[bool, str]:
    failures: list[str] = []
    for item in declaration.classes:
        if item.mode not in MODES:
            failures.append(f"{item.class_id}: unsupported mode {item.mode}")
        if item.mode == RAW_MODE and item.required_attribute is None:
            failures.append(f"{item.class_id}: raw mode requires a Git attribute")
        if item.mode == CANONICAL_MODE and item.required_attribute is not None:
            failures.append(f"{item.class_id}: canonical mode must not require a Git attribute")
    seen: dict[str, str] = {}
    for item in declaration.classes:
        for binding in item.bindings:
            previous = seen.setdefault(binding, item.class_id)
            if previous != item.class_id:
                failures.append(f"{binding}: bound by {previous} and {item.class_id}")
    for left in declaration.classes:
        for right in declaration.classes:
            if left.class_id >= right.class_id:
                continue
            for first in left.patterns:
                for second in right.patterns:
                    if first == second:
                        failures.append(
                            f"{left.class_id} and {right.class_id} both declare {first}"
                        )
    if failures:
        return False, _detail(failures)
    modes = ", ".join(f"{item.class_id}={item.mode}" for item in declaration.classes)
    return True, f"one mode per class: {modes}"


def assess(
    root: Path, declaration: Declaration | None = None
) -> tuple[tuple[str, bool, str], ...]:
    """Return the three hash-bound checks in specified order, failing closed."""

    try:
        known = declaration or load_declaration()
    except HashBoundError as exc:
        return tuple((name, False, str(exc)) for name in CHECK_NAMES)
    cache: dict[str, tuple[str, ...]] = {}

    def tracked() -> tuple[str, ...]:
        # Enumerated once and shared, so the two Git-dependent checks agree on
        # exactly one tracked set and cannot disagree about what is committed.
        if "paths" not in cache:
            cache["paths"] = tracked_paths(root)
        return cache["paths"]

    results: list[tuple[str, bool, str]] = []
    for name, evaluate in (
        (CHECK_CLASS_DECLARED, lambda: _class_declared(root, known, tracked())),
        (CHECK_ATTRIBUTE_EFFECTIVE, lambda: _attribute_effective(root, known, tracked())),
        (CHECK_MODE_CONSISTENT, lambda: _mode_consistent(known)),
    ):
        try:
            passed, detail = evaluate()
        except HashBoundError as exc:
            passed, detail = False, str(exc)
        results.append((name, passed, detail))
    return tuple(results)
