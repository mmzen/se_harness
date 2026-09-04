"""Generate the diagnostic-code index note from the candidate source.

`WO-TCM-003` (`REQ-TCM-005`, `SPEC-TCM-002` TCM-DCI): one scanner parses the
candidate source's string literals and renders `docs/notes/diagnostic-codes.md`
deterministically, so the page cannot drift from the code; a test pins it.
Codes are extracted only from string literals through the language parser, so
a code named in a comment or an identifier never enters the index. Only the
prefixes registered below are diagnostics; artifact and specification
identifiers share the code shape and are excluded by construction.

This module is standard-library only; `repository_tools` may not widen its
pinned import crossing into `se_harness` (the import-barrier tests pin it).
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

NOTE_RELATIVE = "docs/notes/diagnostic-codes.md"
#: The candidate source trees. The hash-locked root `scripts/` copies are the
#: released evaluator's files and are never scanned (TCM-DCI-001).
SCAN_ROOTS = (
    "se_harness",
    "repository_tools",
    "templates/repository/standard/scripts",
)
#: Diagnostic prefixes only (TCM-DCI-002): (component, one-sentence meaning),
#: in the order the page presents them.
PREFIXES: dict[str, tuple[str, str]] = {
    "E": ("installed validator", "an artifact-graph or integrity error; validation fails."),
    "E-AUT": ("installed validator", "an authoring-rule error on a formal artifact."),
    "E-CIP": ("installed validator", "a CI-pipeline rule error."),
    "E-DCM": ("installed validator", "a decision-artifact rule error."),
    "E-ECP": ("installed validator", "a control-plane rule error."),
    "W": ("installed validator", "a warning; validation still passes."),
    "W-ADS": ("installed validator", "an agent-directive-surface warning."),
    "W-AUT": ("installed validator", "an authoring-style advisory, raised only on drafts."),
    "W-DCM": ("installed validator", "a decision-artifact warning."),
    "W-ECP": ("installed validator", "a control-plane warning."),
    "W-REB": ("installed validator", "a released-evaluator-boundary warning."),
    "W-REV": ("installed validator", "a revision-provenance warning."),
    "W-HEX": ("dashboard and inspection scripts", "a Harness Explorer publication warning."),
    "A": ("preflight", "the artifact graph could not be read or validated."),
    "I": ("preflight", "an installation check failed."),
    "WEX": ("workflow execution", "a check, transition, or evidence operation is refused."),
    "WEX-ADS": ("workflow execution", "a directive-surface workflow refusal."),
    "WEX-ECP": ("workflow execution", "a control-plane workflow refusal."),
    "MG": ("mutation guard", "an installed-root write is refused before any file changes."),
    "RID": ("runtime identity", "the running evaluator's identity could not be proven."),
    "EPS": ("interpreter safety", "the environment entry-point safety rule failed."),
    "JNL": ("journaled apply", "the journaled writer refused or could not recover."),
    "PRE": ("evaluator-facts derivation", "CI could not derive a complete fact set from the declared root."),
    "REN": ("renumber-artifacts", "an identifier-renumbering plan or apply is refused."),
    "RQ": ("release qualification", "a qualification result could not be produced or retained."),
    "CC": ("release qualification", "a complete-candidate check."),
    "CP": ("release qualification", "a candidate-package check."),
    "RR": ("release qualification", "a released-root check."),
    "PI": ("release qualification", "a public-install check."),
    "PV": ("release qualification", "retired predecessor-view codes, reserved and emitted by no path."),
}
_CODE = re.compile(r"\b([A-Z]+(?:-[A-Z]+)*?)-?(\d{3})\b")
#: Roots whose hyphenated rule-family forms are diagnostics by construction
#: (`E-DCM-001`, `W-AUT-002`, `WEX-ECP-030`); a family under one of these roots
#: that is absent from the registry is a defect of the registry, not a
#: non-diagnostic (WO-TCM-004). Artifact and rule identifiers never start with
#: a single letter or `WEX`, so they are outside the guard by construction.
_GUARDED_ROOTS = frozenset({"E", "W", "WEX"})
_MESSAGE_LIMIT = 110
_MESSAGES_SHOWN = 2


class IndexError_(RuntimeError):
    """A source file could not be parsed; the index would be incomplete."""


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _sources(repository: Path) -> list[Path]:
    found: list[Path] = []
    for root in SCAN_ROOTS:
        found.extend(
            path
            for path in sorted((repository / root).rglob("*.py"))
            if "__pycache__" not in path.parts
        )
    return found


def _literal_codes(repository: Path):
    """Yield (prefix, code, collapsed message) for every code-shaped match in a string literal."""

    for path in _sources(repository):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeError) as exc:
            raise IndexError_(f"cannot parse {path}: {exc}") from exc
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            message = " ".join(node.value.split())
            if len(message) > _MESSAGE_LIMIT:
                message = message[: _MESSAGE_LIMIT - 1] + "…"
            for match in _CODE.finditer(node.value):
                yield match.group(1), match.group(0), message


def scan(repository: Path) -> dict[str, dict[str, set[str]]]:
    """Return {prefix: {code: {message literals}}} for registered prefixes only."""

    codes: dict[str, dict[str, set[str]]] = {prefix: {} for prefix in PREFIXES}
    for prefix, code, message in _literal_codes(repository):
        if prefix in PREFIXES:
            codes[prefix].setdefault(code, set()).add(message)
    for code, messages in _composed_codes(repository).items():
        prefix = _CODE.fullmatch(code).group(1)
        if prefix in codes:
            codes[prefix].setdefault(code, set()).update(messages)
    return codes


def _composed_codes(repository: Path) -> dict[str, set[str]]:
    """Codes the CLI composes at run time as `family + cause digit` (ECP-CLI-007).

    Both facts are read from the source through the parser, never restated:
    the cause table from `se_harness/provenance.py` and the family literals
    from the `_record_code(exc, "...")` call sites in `se_harness/cli.py`.
    """

    causes: dict[str, str] = {}
    tree = ast.parse((repository / "se_harness/provenance.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "CAUSE_SUFFIX" for t in node.targets)
            and isinstance(node.value, ast.Dict)
        ):
            causes = {
                key.value: value.value
                for key, value in zip(node.value.keys, node.value.values)
                if isinstance(key, ast.Constant) and isinstance(value, ast.Constant)
            }
    families: set[str] = set()
    tree = ast.parse((repository / "se_harness/cli.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_record_code"
            and len(node.args) == 2
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
        ):
            families.add(node.args[1].value)
    legend = ", ".join(f"{cause} {digit}" for cause, digit in causes.items())
    composed: dict[str, set[str]] = {}
    for family in families:
        for cause, digit in causes.items():
            composed[family + digit] = {
                f"Composed at run time as {family} plus the cause digit ({legend}); this one is the {cause} cause."
            }
    return composed


def unregistered_families(repository: Path) -> dict[str, set[str]]:
    """Return {family prefix: {codes}} for guarded hyphenated families absent from the registry.

    An empty result means every `E-`, `W-` and `WEX-` rule family the source
    can emit is registered and therefore indexed; a non-empty result is the
    case `VER-TCM-002` left to review, made mechanical.
    """

    missing: dict[str, set[str]] = {}
    for prefix, code, _ in _literal_codes(repository):
        if "-" in prefix and prefix.split("-", 1)[0] in _GUARDED_ROOTS and prefix not in PREFIXES:
            missing.setdefault(prefix, set()).add(code)
    return missing


def _guard_report(missing: dict[str, set[str]]) -> str:
    families = "; ".join(
        f"{prefix} ({', '.join(sorted(codes, key=_code_order))})" for prefix, codes in sorted(missing.items())
    )
    return f"unregistered diagnostic families in the source: {families}; register them in PREFIXES"


def _code_order(code: str) -> tuple[int, str]:
    return int(_CODE.fullmatch(code).group(2)), code


def render(codes: dict[str, dict[str, set[str]]]) -> str:
    total = sum(len(members) for members in codes.values())
    lines = [
        "<!-- GENERATED FILE (WO-TCM-003). Do not edit by hand: regenerate with",
        "     python -m repository_tools.diagnostic_code_index --write",
        "     tests/test_diagnostic_code_index.py fails when this page drifts. -->",
        "",
        "# Diagnostic code index",
        "",
        "<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->",
        "",
        "## Summary",
        "",
        "When a harness command refuses, or a validation reports a problem, it",
        "prints a short code such as `MG001`, `WEX210` or `E012` beside its",
        "message. This page lists every diagnostic code the candidate source can",
        "emit, grouped by prefix, with the message text each code appears in. It",
        "is generated from the source by",
        "`repository_tools/diagnostic_code_index.py`, so it cannot drift, and a",
        "test fails the suite when it does. The installed root evaluator is a",
        "released version and may emit a slightly older set until the repository",
        "adopts the next release.",
        "",
        f"{total} codes across {len(PREFIXES)} registered prefixes.",
        "",
        "## How to read a code",
        "",
        "The prefix names the component that speaks; the number identifies the",
        "exact rule or failure. Artifact identifiers such as `WO-ECP-010` and",
        "specification rule identifiers such as `ECP-DLG-001` share this shape",
        "but are not diagnostics and are not listed here.",
        "",
        "| Prefix | Component | Meaning | Codes |",
        "| --- | --- | --- | ---: |",
    ]
    for prefix, (component, meaning) in PREFIXES.items():
        lines.append(f"| `{prefix}` | {component} | {meaning} | {len(codes[prefix])} |")
    lines.append("")
    lines.append("## Codes")
    for prefix, (component, _) in PREFIXES.items():
        members = codes[prefix]
        if not members:
            continue
        lines.append("")
        lines.append(f"### `{prefix}` — {component}")
        lines.append("")
        lines.append("| Code | Message text in the source |")
        lines.append("| --- | --- |")
        for code in sorted(members, key=_code_order):
            messages = sorted(members[code])
            shown = "; ".join(f"`{item}`" for item in messages[:_MESSAGES_SHOWN])
            if len(messages) > _MESSAGES_SHOWN:
                shown += f" (+{len(messages) - _MESSAGES_SHOWN} more)"
            lines.append(f"| `{code}` | {shown} |")
    lines.append("")
    return "\n".join(lines)


def generate(repository: Path | None = None) -> str:
    return render(scan(repository or _repository_root()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m repository_tools.diagnostic_code_index",
        description=__doc__.split("\n\n")[0],
    )
    parser.add_argument("--repository", default=None, help="checkout root (default: this checkout)")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true", help=f"write {NOTE_RELATIVE}")
    action.add_argument("--check", action="store_true", help="exit 1 when the committed page differs")
    args = parser.parse_args(argv)
    repository = Path(args.repository).resolve() if args.repository else _repository_root()
    missing = unregistered_families(repository)
    if missing:
        print(_guard_report(missing), file=sys.stderr)
        return 1
    rendered = generate(repository)
    note = repository / NOTE_RELATIVE
    if args.write:
        note.write_bytes(rendered.encode("utf-8"))
        print(f"wrote {NOTE_RELATIVE}")
        return 0
    if args.check:
        committed = note.read_bytes().decode("utf-8").replace("\r\n", "\n") if note.is_file() else ""
        if committed != rendered:
            print(f"{NOTE_RELATIVE} differs from the regeneration; run --write", file=sys.stderr)
            return 1
        print(f"{NOTE_RELATIVE} matches the source")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
