"""Declared hash-bound text classes, mode determination and read-only assessment."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping

from se_harness._process import run_git
from se_harness.integrity import (
    HASH_MODE,
    IntegrityError,
    canonical_sha256,
    canonical_text,
    raw_sha256,
    unique_object_hook,
)


HASH_BOUND_SCHEMA = "se-harness-hash-bound-classes-v1"
RAW_MODE = "raw"
CANONICAL_MODE = HASH_MODE
MODES = frozenset({RAW_MODE, CANONICAL_MODE})
MATCH_DECLARED = "declared"
MATCH_MISMATCH = "mismatch"
MATCH_RESULTS = (MATCH_DECLARED, MATCH_MISMATCH)
LOCK_RELATIVE = ".engineering-harness.lock"
REQUIRED_ATTRIBUTES = frozenset({"text eol=lf"})
CLASS_FIELDS = frozenset({"id", "mode", "patterns", "required_attribute"})
CHECK_CLASS_DECLARED = "hash-bound-class-declared"
CHECK_ATTRIBUTE_EFFECTIVE = "hash-bound-attribute-effective"
CHECK_MODE_CONSISTENT = "hash-bound-mode-consistent"
CHECK_NAMES = (CHECK_CLASS_DECLARED, CHECK_ATTRIBUTE_EFFECTIVE, CHECK_MODE_CONSISTENT)
ATTRIBUTES_NAME = ".gitattributes"
ATTRIBUTE_BEGIN_MARKER = "# se-harness:begin"
ATTRIBUTE_END_MARKER = "# se-harness:end"
_CLASS_ID = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_PATTERN = re.compile(r"^[A-Za-z0-9_.*/-]+$")
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


@dataclass(frozen=True)
class Declaration:
    classes: tuple[HashBoundClass, ...]


_object = unique_object_hook(lambda key: HashBoundError(f"duplicate declaration key: {key}"))


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
    attribute = raw["required_attribute"]
    if mode == RAW_MODE:
        if attribute not in REQUIRED_ATTRIBUTES:
            raise HashBoundError(f"raw class {class_id} must require a supported Git attribute")
    elif attribute is not None:
        raise HashBoundError(f"canonical class {class_id} must not require a Git attribute")
    return HashBoundClass(
        class_id=class_id,
        patterns=tuple(_pattern(item, class_id) for item in patterns),
        mode=mode,
        required_attribute=attribute,

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
    if set(raw) != {"classes", "schema"}:
        raise HashBoundError("declaration fields must be schema and classes")
    entries = raw["classes"]
    if not isinstance(entries, list) or not entries:
        raise HashBoundError("declaration must contain at least one class")
    classes = tuple(_class(item) for item in entries)
    seen: set[str] = set()
    for item in classes:
        if item.class_id in seen:
            raise HashBoundError(f"duplicate class ID: {item.class_id}")
        seen.add(item.class_id)
    return Declaration(classes=classes)


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
    # ECP-PRM-003: the one launcher; the refusal keeps this module's wording.
    completed = run_git(
        root, *arguments, stdin=stdin, timeout=_GIT_TIMEOUT,
        error=lambda message: HashBoundError(
            message if message.startswith("git executable is unavailable") else f"git {arguments[0]} failed: {message}"
        ),
    )
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








def _detail(items: Iterable[str]) -> str:
    selected = sorted(items)
    head = "; ".join(selected[:_MAX_DETAIL_ITEMS])
    remainder = len(selected) - _MAX_DETAIL_ITEMS
    return f"{head} (+{remainder} more)" if remainder > 0 else head




def _attribute_effective(
    root: Path, declaration: Declaration, tracked: tuple[str, ...]
) -> tuple[bool, str]:
    failures: list[str] = []
    raw_classes = [item for item in declaration.classes if item.mode == RAW_MODE]
    covered: dict[str, list[str]] = {}
    for item in raw_classes:
        paths: list[str] = []
        for pattern in item.patterns:
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
        (CHECK_CLASS_DECLARED, lambda: (True, f"{len(known.classes)} file formats declared; consuming formats validate their own fields")),
        (CHECK_ATTRIBUTE_EFFECTIVE, lambda: _attribute_effective(root, known, tracked())),
        (CHECK_MODE_CONSISTENT, lambda: _mode_consistent(known)),
    ):
        try:
            passed, detail = evaluate()
        except HashBoundError as exc:
            passed, detail = False, str(exc)
        results.append((name, passed, detail))
    return tuple(results)
