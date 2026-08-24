"""Declared environment entry-point safety rule for the package runtime.

The rule itself lives in ``se_harness/interpreter_safety.json``. This module is
one of two conforming loaders; the other is ``repository_tools``' loader, which
reads the same declaration without importing this package. Neither loader may
import the other runtime, so the two evaluate the declared cases independently
and a conformance check holds them in agreement.

The safe execution boundary is the *lexical* interpreter path. A POSIX virtual
environment normally exposes ``bin/python`` as a terminal symbolic link, so
dereferencing the final component before deriving the environment root escapes
the environment and loses its installed distribution, templates, and entry
point. Every link above the final component remains forbidden, because such a
link lets the whole environment be relocated after a check has passed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


DECLARATION_SCHEMA = "se-harness-interpreter-safety-v1"
WITHIN_EXPECTED_ROOT = "within-expected-root"
WITHIN_CHECKOUT_ROOT = "within-checkout-root"
OUTSIDE_DECLARED_ROOTS = "outside-declared-roots"
POSITION_CLASSES = (OUTSIDE_DECLARED_ROOTS, WITHIN_CHECKOUT_ROOT, WITHIN_EXPECTED_ROOT)
OUTCOMES = ("accepted", "refused")
RUNTIMES = ("repository_tools", "se_harness")
BOUNDARY_KINDS = ("delegating", "rule")
PLATFORMS = ("linux", "windows")
CASE_PATTERN = re.compile(r"EPS[0-9]{3}")
CORPUS_PATTERN = re.compile(r"ISC[0-9]{3}")
DIGEST_BLOCK_BYTES = 1024 * 1024
MAX_INTERPRETER_BYTES = 128 * 1024 * 1024

#: The 3.12+ junction predicate on ``pathlib.Path``.
JUNCTION_PREDICATE = "is_junction"
#: The reparse-point constants that carry the same predicate on Python 3.11.
REPARSE_CONSTANTS = ("FILE_ATTRIBUTE_REPARSE_POINT", "IO_REPARSE_TAG_MOUNT_POINT")
#: The ``os.stat_result`` members through which a filesystem reports reparse
#: information. A runtime whose stat result carries neither member observes no
#: reparse point on any path, so the junction predicate answers ``False`` by
#: construction there rather than being unavailable.
REPARSE_STAT_MEMBERS = ("st_file_attributes", "st_reparse_tag")

CASE_KEYS = frozenset({"id", "subject", "outcome", "summary"})
BOUNDARY_KEYS = frozenset({"id", "runtime", "module", "purpose", "kind"})
BOUNDARY_DELEGATING_KEYS = BOUNDARY_KEYS | {"delegates_to"}
CORPUS_KEYS = frozenset({"id", "form", "expected", "constructable_on", "summary"})
CORPUS_OPTIONAL_KEYS = CORPUS_KEYS | {"unconstructable_reason"}
DECLARATION_KEYS = frozenset(
    {"schema", "outcomes", "position_classes", "cases", "boundaries", "corpus"}
)

#: The declared cases in declared evaluation order. The first refusal wins, so a
#: path form yields a stable case identifier regardless of which boundary
#: evaluates it. This tuple is compared against the declaration in both
#: directions, so neither side can define its own passing condition.
EVALUATION_ORDER = (
    "EPS010",
    "EPS011",
    "EPS001",
    "EPS002",
    "EPS003",
    "EPS004",
    "EPS005",
    "EPS006",
    "EPS007",
    "EPS008",
    "EPS009",
)


class InterpreterSafetyError(ValueError):
    """The interpreter-safety declaration is missing, malformed, or ambiguous."""


class InterpreterSafetyRefusal(ValueError):
    """A supplied interpreter path is refused by a declared case."""

    def __init__(self, case: str, subject: str, detail: str) -> None:
        super().__init__(f"{case} {subject}: {detail}")
        self.case = case
        self.subject = subject
        self.detail = detail


@dataclass(frozen=True)
class SafeEntryPoint:
    """An accepted environment entry point and the facts recorded about it."""

    entry_point: Path
    environment_root: Path
    resolved_target: Path
    entry_is_link: bool
    binary_position: str
    binary_sha256: str


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InterpreterSafetyError(f"ISD101: duplicate JSON key: {key}")
        result[key] = value
    return result


def _exact_keys(value: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        raise InterpreterSafetyError(f"ISD102: {label} is missing field: {sorted(missing)[0]}")
    if unknown:
        raise InterpreterSafetyError(f"ISD103: {label} has unknown field: {sorted(unknown)[0]}")


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InterpreterSafetyError(f"ISD104: {label} must be a non-empty string")
    return value


def _declaration_path() -> Path:
    return Path(__file__).with_name("interpreter_safety.json")


def declaration_bytes(path: Path | None = None) -> bytes:
    selected = path or _declaration_path()
    try:
        return selected.read_bytes()
    except OSError as exc:
        raise InterpreterSafetyError(f"ISD105: cannot read the declaration: {exc}") from exc


def load_declaration(path: Path | None = None) -> dict[str, Any]:
    """Read and strictly validate the declared interpreter-safety rule."""

    raw = declaration_bytes(path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InterpreterSafetyError("ISD106: the declaration must be UTF-8") from exc
    try:
        declaration = json.loads(text, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as exc:
        raise InterpreterSafetyError(f"ISD107: invalid declaration JSON: {exc.msg}") from exc
    if not isinstance(declaration, dict):
        raise InterpreterSafetyError("ISD108: the declaration root must be an object")
    _exact_keys(declaration, DECLARATION_KEYS, "declaration")
    if declaration["schema"] != DECLARATION_SCHEMA:
        raise InterpreterSafetyError(
            f"ISD109: the declaration schema must be {DECLARATION_SCHEMA!r}"
        )
    if tuple(declaration["outcomes"]) != OUTCOMES:
        raise InterpreterSafetyError("ISD110: the declared outcome domain differs from the loader")
    if tuple(declaration["position_classes"]) != POSITION_CLASSES:
        raise InterpreterSafetyError("ISD111: the declared position classes differ from the loader")
    _validate_cases(declaration["cases"])
    _validate_boundaries(declaration["boundaries"])
    _validate_corpus(declaration["corpus"], declaration["cases"])
    return declaration


def _validate_cases(cases: Any) -> None:
    if not isinstance(cases, list) or not cases:
        raise InterpreterSafetyError("ISD112: cases must be a non-empty array")
    order: list[str] = []
    for entry in cases:
        if not isinstance(entry, dict):
            raise InterpreterSafetyError("ISD113: each case must be an object")
        _exact_keys(entry, CASE_KEYS, "case")
        identifier = _text(entry["id"], "case id")
        if CASE_PATTERN.fullmatch(identifier) is None:
            raise InterpreterSafetyError(f"ISD114: invalid case identifier: {identifier}")
        _text(entry["subject"], f"case {identifier} subject")
        _text(entry["summary"], f"case {identifier} summary")
        if entry["outcome"] not in OUTCOMES:
            raise InterpreterSafetyError(f"ISD115: case {identifier} has an unknown outcome")
        order.append(identifier)
    if len(set(order)) != len(order):
        raise InterpreterSafetyError("ISD116: the case list contains a duplicate identifier")
    if tuple(order) != EVALUATION_ORDER:
        raise InterpreterSafetyError(
            "ISD117: the declared case order differs from the implemented evaluation order"
        )


def _validate_boundaries(boundaries: Any) -> None:
    if not isinstance(boundaries, list) or not boundaries:
        raise InterpreterSafetyError("ISD118: boundaries must be a non-empty array")
    identifiers: list[str] = []
    rules: set[str] = set()
    delegations: list[tuple[str, str]] = []
    for entry in boundaries:
        if not isinstance(entry, dict):
            raise InterpreterSafetyError("ISD119: each boundary must be an object")
        kind = entry.get("kind")
        if kind == "delegating":
            _exact_keys(entry, BOUNDARY_DELEGATING_KEYS, "delegating boundary")
        else:
            _exact_keys(entry, BOUNDARY_KEYS, "boundary")
        identifier = _text(entry["id"], "boundary id")
        _text(entry["module"], f"boundary {identifier} module")
        _text(entry["purpose"], f"boundary {identifier} purpose")
        if entry["runtime"] not in RUNTIMES:
            raise InterpreterSafetyError(f"ISD120: boundary {identifier} has an unknown runtime")
        if kind not in BOUNDARY_KINDS:
            raise InterpreterSafetyError(f"ISD121: boundary {identifier} has an unknown kind")
        if not identifier.startswith(f"{entry['runtime']}."):
            raise InterpreterSafetyError(
                f"ISD122: boundary {identifier} does not name its own runtime"
            )
        identifiers.append(identifier)
        if kind == "rule":
            rules.add(identifier)
        else:
            delegations.append((identifier, _text(entry["delegates_to"], "delegates_to")))
    if len(set(identifiers)) != len(identifiers):
        raise InterpreterSafetyError("ISD123: the boundary registry contains a duplicate")
    if identifiers != sorted(identifiers):
        raise InterpreterSafetyError("ISD124: the boundary registry must be sorted by identifier")
    for identifier, target in delegations:
        if target not in rules:
            raise InterpreterSafetyError(
                f"ISD125: boundary {identifier} delegates to an unregistered rule boundary"
            )


def _validate_corpus(corpus: Any, cases: Any) -> None:
    if not isinstance(corpus, list) or not corpus:
        raise InterpreterSafetyError("ISD126: the corpus must be a non-empty array")
    declared = {entry["id"] for entry in cases}
    identifiers: list[str] = []
    for entry in corpus:
        if not isinstance(entry, dict):
            raise InterpreterSafetyError("ISD127: each corpus entry must be an object")
        platforms = entry.get("constructable_on")
        if platforms == [] or "unconstructable_reason" in entry:
            _exact_keys(entry, CORPUS_OPTIONAL_KEYS, "corpus entry")
        else:
            _exact_keys(entry, CORPUS_KEYS, "corpus entry")
        identifier = _text(entry["id"], "corpus id")
        if CORPUS_PATTERN.fullmatch(identifier) is None:
            raise InterpreterSafetyError(f"ISD128: invalid corpus identifier: {identifier}")
        _text(entry["form"], f"corpus {identifier} form")
        _text(entry["summary"], f"corpus {identifier} summary")
        expected = entry["expected"]
        if expected != "accepted" and expected not in declared:
            raise InterpreterSafetyError(
                f"ISD129: corpus {identifier} expects an undeclared case: {expected}"
            )
        if not isinstance(platforms, list) or any(item not in PLATFORMS for item in platforms):
            raise InterpreterSafetyError(f"ISD130: corpus {identifier} names an unknown platform")
        if sorted(set(platforms)) != platforms:
            raise InterpreterSafetyError(
                f"ISD131: corpus {identifier} platforms must be sorted and unique"
            )
        if len(platforms) != len(PLATFORMS) and "unconstructable_reason" not in entry:
            raise InterpreterSafetyError(
                f"ISD132: corpus {identifier} omits a platform without recording a reason"
            )
        if "unconstructable_reason" in entry:
            _text(entry["unconstructable_reason"], f"corpus {identifier} reason")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise InterpreterSafetyError("ISD133: the corpus contains a duplicate identifier")
    if identifiers != sorted(identifiers):
        raise InterpreterSafetyError("ISD134: the corpus must be sorted by identifier")
    reached = {entry["expected"] for entry in corpus} - {"accepted"}
    unreached = declared - reached
    if unreached:
        raise InterpreterSafetyError(
            f"ISD135: declared case has no corpus entry: {sorted(unreached)[0]}"
        )


def declared_cases(path: Path | None = None) -> tuple[dict[str, Any], ...]:
    return tuple(load_declaration(path)["cases"])


def declared_boundaries(path: Path | None = None) -> tuple[dict[str, Any], ...]:
    return tuple(load_declaration(path)["boundaries"])


def declared_corpus(path: Path | None = None) -> tuple[dict[str, Any], ...]:
    return tuple(load_declaration(path)["corpus"])


def reparse_information_observable() -> bool:
    """Report whether this runtime's stat result can carry reparse information.

    The members are named by the constant above rather than written inline, so a
    conformance test can withdraw or supply this route on either platform and
    prove which condition decided the rule.
    """

    return all(hasattr(os.stat_result, name) for name in REPARSE_STAT_MEMBERS)


def link_classification_available() -> bool:
    """Report whether this runtime can classify a path as a symbolic link or junction.

    Symbolic-link detection is present on every supported runtime. Junction
    detection has three routes, any one of which decides the predicate:

    * ``pathlib.Path.is_junction``, which exists from Python 3.12;
    * the reparse-point ``stat`` constants, which carry the same predicate on
      Python 3.11 from the reparse information a ``stat`` result reports;
    * a stat result that carries no reparse member at all, which observes a
      filesystem on which no path is a reparse point, so the predicate answers
      ``False`` by construction.

    The third route is not a platform test. ``IO_REPARSE_TAG_MOUNT_POINT`` is
    published only where the platform defines it, so a runtime below Python 3.12
    on a filesystem without reparse information has neither of the first two
    routes while having nothing for either to classify. On such a runtime
    ``pathlib.Path.is_junction`` would itself return ``False`` for every path, so
    treating the two conditions differently would refuse a runtime that a later
    Python accepts without gaining any detection.

    Only where reparse information is observable and neither predicate route
    exists does the rule refuse with ``EPS011`` rather than passing the junction
    check silently: there the platform can present a junction that this runtime
    cannot classify.

    Every route is named by a module constant rather than written inline, so a
    conformance test can withdraw any of them on a runtime that has it and prove
    which surviving route decided the rule.
    """

    if hasattr(Path, JUNCTION_PREDICATE):
        return True
    if all(hasattr(stat, name) for name in REPARSE_CONSTANTS):
        return True
    return not reparse_information_observable()


def _is_symlink(path: Path) -> bool:
    try:
        return path.is_symlink()
    except OSError:
        return False


def _is_junction(path: Path) -> bool:
    predicate = getattr(Path, JUNCTION_PREDICATE, None)
    if predicate is not None:
        try:
            return bool(predicate(path))
        except OSError:
            return False
    reparse_flag = getattr(stat, REPARSE_CONSTANTS[0], None)
    mount_tag = getattr(stat, REPARSE_CONSTANTS[1], None)
    if reparse_flag is None or mount_tag is None:
        return False
    try:
        attributes = os.lstat(path)
    except OSError:
        return False
    flags = getattr(attributes, "st_file_attributes", None)
    if flags is None or not flags & reparse_flag:
        return False
    return getattr(attributes, "st_reparse_tag", None) == mount_tag


def _lexical(path: Path | str) -> Path:
    return Path(os.path.abspath(Path(path).expanduser()))


def _lexically_within(path: Path, boundary: Path) -> bool:
    try:
        _lexical(path).relative_to(_lexical(boundary))
    except ValueError:
        return False
    return True


def _resolved_within(resolved: Path, boundary: Path) -> bool:
    """Test containment of an already-resolved path inside a boundary.

    The supplied interpreter path is resolved exactly once per observation, so
    this helper resolves only the boundary and never the interpreter again.
    """

    try:
        resolved.relative_to(boundary.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def _traverses_link(path: Path, *, include_self: bool) -> Path | None:
    """Return the first enclosing link, or the path itself when it is one."""

    probe = path if include_self else path.parent
    while True:
        if _is_symlink(probe) or _is_junction(probe):
            return probe
        parent = probe.parent
        if probe == parent:
            return None
        probe = parent


def _digest(target: Path, supplied: bytes | None) -> str:
    if supplied is not None:
        if len(supplied) > MAX_INTERPRETER_BYTES:
            raise InterpreterSafetyRefusal(
                "EPS004", "target", "the resolved interpreter exceeds the readable bound"
            )
        return hashlib.sha256(supplied).hexdigest()
    digest = hashlib.sha256()
    total = 0
    try:
        with target.open("rb") as handle:
            while True:
                block = handle.read(DIGEST_BLOCK_BYTES)
                if not block:
                    break
                total += len(block)
                if total > MAX_INTERPRETER_BYTES:
                    raise InterpreterSafetyRefusal(
                        "EPS004", "target", "the resolved interpreter exceeds the readable bound"
                    )
                digest.update(block)
    except OSError as exc:
        raise InterpreterSafetyRefusal(
            "EPS004", "target", "the resolved interpreter cannot be read"
        ) from exc
    return digest.hexdigest()


def evaluate(
    path: Path | str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
    target_bytes: bytes | None = None,
) -> SafeEntryPoint:
    """Apply the declared rule to a supplied interpreter path.

    Refuses with the first matching declared case, before any interpreter is
    spawned and before any target is validated. On acceptance the environment
    root is a lexical function of the supplied path alone and never depends on
    the resolved target.
    """

    lexical = _lexical(path)

    # Rule 2: the environment root is the lexical path's second parent.
    parents = lexical.parents
    if len(parents) < 2:
        raise InterpreterSafetyRefusal(
            "EPS010", "environment_root", "the interpreter path has no environment root"
        )
    environment_root = parents[1]

    # Rule 4: junction detection is a predicate distinct from symbolic-link
    # detection, and its absence refuses rather than passes.
    if not link_classification_available():
        raise InterpreterSafetyRefusal(
            "EPS011", "link_predicate", "this runtime cannot classify a directory junction"
        )

    # Rule 3: no enclosing directory may be a link.
    enclosing = _traverses_link(lexical, include_self=False)
    if enclosing is not None:
        if _is_symlink(enclosing):
            raise InterpreterSafetyRefusal(
                "EPS001", "parent", "an enclosing directory is a symbolic link"
            )
        raise InterpreterSafetyRefusal(
            "EPS002", "parent", "an enclosing directory is a directory junction"
        )

    # Rule 5: strict resolution. A resolution failure is reported as an
    # ``OSError`` on some runtimes and, for a symbolic-link cycle below Python
    # 3.13, as a ``RuntimeError`` that replaces the underlying ``ELOOP``. Both
    # mean the same thing to this rule: the path does not resolve.
    try:
        target = lexical.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InterpreterSafetyRefusal(
            "EPS003", "interpreter", "the interpreter path does not resolve"
        ) from exc

    # Rule 6: both the entry and its target must be ordinary files.
    if not lexical.is_file() or not target.is_file():
        raise InterpreterSafetyRefusal(
            "EPS004", "interpreter", "the interpreter path is not an ordinary file"
        )

    # Rule 7: only a terminal symbolic link may stand in the final position.
    # Rule 3 has already proven that no enclosing directory is a link, so the
    # only link the final component can still traverse is itself. One stat
    # therefore decides the rule and the ancestor walk is not repeated.
    entry_is_link = _is_symlink(lexical)
    if not entry_is_link and _is_junction(lexical):
        raise InterpreterSafetyRefusal(
            "EPS005",
            "interpreter",
            "the final component traverses a link without being a symbolic link",
        )

    # Rule 8: the resolved target may not traverse a link of its own.
    if _traverses_link(target, include_self=True) is not None:
        raise InterpreterSafetyRefusal(
            "EPS006", "target", "the resolved interpreter target traverses a link"
        )

    # Rule 9: neither the entry nor the target may sit inside the checkout.
    if checkout_root is not None:
        if _lexically_within(lexical, checkout_root):
            raise InterpreterSafetyRefusal(
                "EPS007", "interpreter", "the interpreter path is inside the checkout"
            )
        if _resolved_within(target, Path(checkout_root)):
            raise InterpreterSafetyRefusal(
                "EPS008", "target", "the resolved interpreter target is inside the checkout"
            )

    # Rule 10: the entry must sit lexically inside a supplied declared root.
    if declared_root is not None:
        try:
            remainder = _lexical(lexical).relative_to(_lexical(declared_root))
        except ValueError as exc:
            raise InterpreterSafetyRefusal(
                "EPS009", "interpreter", "the interpreter path is outside its declared root"
            ) from exc
        if not remainder.parts:
            raise InterpreterSafetyRefusal(
                "EPS009", "interpreter", "the interpreter path is its own declared root"
            )

    expected_root = Path(declared_root) if declared_root is not None else environment_root
    if _resolved_within(target, expected_root):
        position = WITHIN_EXPECTED_ROOT
    elif checkout_root is not None and _resolved_within(target, Path(checkout_root)):
        position = WITHIN_CHECKOUT_ROOT
    else:
        position = OUTSIDE_DECLARED_ROOTS

    return SafeEntryPoint(
        entry_point=lexical,
        environment_root=environment_root,
        resolved_target=target,
        entry_is_link=entry_is_link,
        binary_position=position,
        binary_sha256=_digest(target, target_bytes),
    )


def refusal_case(
    path: Path | str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
    target_bytes: bytes | None = None,
) -> str | None:
    """Return the first refused case identifier, or ``None`` when accepted."""

    try:
        evaluate(
            path,
            checkout_root=checkout_root,
            declared_root=declared_root,
            target_bytes=target_bytes,
        )
    except InterpreterSafetyRefusal as refusal:
        return refusal.case
    return None


def normalized_origin(entry: SafeEntryPoint, marker: str = "<evaluator-root>") -> str:
    """Render an accepted entry point relative to its environment root."""

    relative = entry.entry_point.relative_to(entry.environment_root).as_posix()
    return f"{marker}/{relative}" if relative else marker


def boundary_identifiers(runtime: str | None = None) -> tuple[str, ...]:
    values: Iterable[dict[str, Any]] = declared_boundaries()
    if runtime is not None:
        values = [entry for entry in values if entry["runtime"] == runtime]
    return tuple(entry["id"] for entry in values)
