"""Resolve a usable interpreter entry point without rejecting linked environments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


WITHIN_EXPECTED_ROOT = "within-expected-root"
WITHIN_CHECKOUT_ROOT = "within-checkout-root"
OUTSIDE_DECLARED_ROOTS = "outside-declared-roots"

class InterpreterSafetyRefusal(ValueError):
    """A supplied interpreter path is refused by a declared case."""

    def __init__(self, case: str, subject: str, detail: str) -> None:
        super().__init__(f"{case} {subject}: {detail}")
        self.case = case
        self.subject = subject
        self.detail = detail
        # SPEC-ECP-023 ECP-PRM-017: the two attributes of a coded refusal, without importing the
        # registry; SPEC-REB-015 rule 2 keeps this module standard-library only.
        self.code = case
        self.message = f"{subject}: {detail}"


@dataclass(frozen=True)
class SafeEntryPoint:
    """An accepted environment entry point and the facts recorded about it."""

    entry_point: Path
    environment_root: Path
    resolved_target: Path
    entry_is_link: bool
    binary_position: str


def _is_symlink(path: Path) -> bool:
    try:
        return path.is_symlink()
    except OSError:
        return False


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


def evaluate(
    path: Path | str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
) -> SafeEntryPoint:
    """Apply the declared rule to a supplied interpreter path.

    Refuses with the first matching declared case, before any interpreter is
    spawned and before any target is validated. On acceptance the environment
    root is a lexical function of the supplied path alone and never depends on
    the resolved target.
    """

    lexical = _lexical(path)

    # the environment root is the lexical path's second parent.
    parents = lexical.parents
    if len(parents) < 2:
        raise InterpreterSafetyRefusal(
            "EPS010", "environment_root", "the interpreter path has no environment root"
        )
    environment_root = parents[1]

    # strict resolution. A resolution failure is reported as an
    # ``OSError`` on some runtimes and, for a symbolic-link cycle below Python
    # 3.13, as a ``RuntimeError`` that replaces the underlying ``ELOOP``. Both
    # mean the same thing to this rule: the path does not resolve.
    try:
        target = lexical.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InterpreterSafetyRefusal(
            "EPS003", "interpreter", "the interpreter path does not resolve"
        ) from exc

    # both the entry and its target must be ordinary files.
    if not lexical.is_file() or not target.is_file():
        raise InterpreterSafetyRefusal(
            "EPS004", "interpreter", "the interpreter path is not an ordinary file"
        )

    entry_is_link = _is_symlink(lexical)

    # neither the entry nor the target may sit inside the checkout.
    if checkout_root is not None:
        if _lexically_within(lexical, checkout_root):
            raise InterpreterSafetyRefusal(
                "EPS007", "interpreter", "the interpreter path is inside the checkout"
            )
        if _resolved_within(target, Path(checkout_root)):
            raise InterpreterSafetyRefusal(
                "EPS008", "target", "the resolved interpreter target is inside the checkout"
            )

    # Resolve parent directories, keeping a terminal virtualenv launcher intact.
    if declared_root is not None:
        try:
            lexical.parent.resolve(strict=True).relative_to(Path(declared_root).resolve(strict=True))
        except (OSError, RuntimeError, ValueError) as exc:
            raise InterpreterSafetyRefusal(
                "EPS009", "interpreter", "the interpreter path is outside its declared root"
            ) from exc

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
    )


def refusal_case(
    path: Path | str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
) -> str | None:
    """Return the first refused case identifier, or ``None`` when accepted."""

    try:
        evaluate(
            path,
            checkout_root=checkout_root,
            declared_root=declared_root,
        )
    except InterpreterSafetyRefusal as refusal:
        return refusal.case
    return None


def normalized_origin(entry: SafeEntryPoint, marker: str = "<evaluator-root>") -> str:
    """Render an accepted entry point relative to its environment root."""

    relative = entry.entry_point.relative_to(entry.environment_root).as_posix()
    return f"{marker}/{relative}" if relative else marker
