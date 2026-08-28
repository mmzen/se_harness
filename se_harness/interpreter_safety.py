"""Environment entry-point safety rule for the package runtime.

The rule is the ordered case list ``EVALUATION_ORDER`` and the ``evaluate``
function below; the first matching refusal wins, so a path form yields a
stable ``EPS`` case identifier. ``WO-REB-021`` introduced the rule as a JSON
declaration with one conforming loader per runtime; once every boundary
outside ``se_harness/runtime_identity.py`` had been retired, ``WO-REB-030``
removed the declaration and the second loader and kept the rule in code.

The safe execution boundary is the *lexical* interpreter path. A POSIX virtual
environment normally exposes ``bin/python`` as a terminal symbolic link, so
dereferencing the final component before deriving the environment root escapes
the environment and loses its installed distribution, templates, and entry
point. Every link above the final component remains forbidden, because such a
link lets the whole environment be relocated after a check has passed.
"""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WITHIN_EXPECTED_ROOT = "within-expected-root"
WITHIN_CHECKOUT_ROOT = "within-checkout-root"
OUTSIDE_DECLARED_ROOTS = "outside-declared-roots"
POSITION_CLASSES = (OUTSIDE_DECLARED_ROOTS, WITHIN_CHECKOUT_ROOT, WITHIN_EXPECTED_ROOT)
OUTCOMES = ("accepted", "refused")
PLATFORMS = ("linux", "windows")
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


#: The cases in evaluation order. The first refusal wins, so a path form yields
#: a stable case identifier. The tests own an independent corpus of filesystem
#: forms and assert the case each one yields.
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
