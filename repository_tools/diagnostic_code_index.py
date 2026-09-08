"""Generate the diagnostic-code index note from the candidate source.

`WO-TCM-003` (`REQ-TCM-005`, `SPEC-TCM-002` TCM-DCI): one scanner parses the
candidate source's string literals and renders `docs/notes/diagnostic-codes.md`
deterministically, so the page cannot drift from the code; a test pins it.
Codes are extracted only from string literals through the language parser, so
a code named in a comment or an identifier never enters the index. Only the
prefixes registered below are diagnostics; artifact and specification
identifiers share the code shape and are excluded by construction.

The package names its codes once in `se_harness/codes.py` (SPEC-ECP-023
ECP-PRM-016); this scanner reads that registry through the parser, never by
import (ECP-PRM-018), and attributes a raise site to its code by the name it
passes: `CodedError(WEX210, "message")`, `Diagnostic(path, E012, message, plane)`,
`f"{WEX201}: message"`. Since WO-ECP-034 the engine under `se_harness/engine/`
names its codes the same way (ECP-ENG-009).

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
#: The candidate source trees. The evaluator's own scripts live under
#: `se_harness/engine/` since WO-DST-024 (SPEC-DST-025); the hash-locked root
#: `scripts/` copies are the released evaluator's files and are never scanned
#: (TCM-DCI-001).
SCAN_ROOTS = (
    "se_harness",
    "repository_tools",
)
#: Diagnostic prefixes only (TCM-DCI-002): (component, one-sentence meaning),
#: in the order the page presents them.
PREFIXES: dict[str, tuple[str, str]] = {
    "E": ("installed validator", "an artifact-graph or integrity error; validation fails."),
    "E-AUT": ("installed validator", "an authoring-rule error on a formal artifact."),
    "E-CIP": ("installed validator", "a CI-pipeline rule error."),
    "E-DCM": ("installed validator", "a decision-artifact rule error."),
    "E-ECP": ("installed validator", "a control-plane rule error."),
    "E-RSK": ("installed validator", "a risk-artifact rule error."),
    "W": ("installed validator", "a warning; validation still passes."),
    "W-ADS": ("installed validator", "an agent-directive-surface warning."),
    "W-AUT": ("installed validator", "an authoring-style advisory, raised only on drafts."),
    "W-DCM": ("installed validator", "a decision-artifact warning."),
    "W-ECP": ("installed validator", "a control-plane warning."),
    "W-REB": ("installed validator", "a released-evaluator-boundary warning."),
    "W-REV": ("installed validator", "a revision-provenance warning."),
    "W-RSK": ("installed validator", "a risk-artifact warning."),
    "W-HEX": ("dashboard and inspection scripts", "a Harness Explorer publication warning."),
    "I-REV": ("dashboard and inspection scripts", "an informational revision-provenance finding."),
    "A": ("preflight", "the artifact graph could not be read or validated."),
    "I": ("preflight", "an installation check failed."),
    "WEX": ("workflow execution", "a check, transition, or evidence operation is refused."),
    "WEX-ADS": ("workflow execution", "a directive-surface workflow refusal."),
    "WEX-ECP": ("workflow execution", "a control-plane workflow refusal."),
    "MG": ("mutation guard", "an installed-root write is refused before any file changes."),
    "RID": ("runtime identity", "the running evaluator's identity could not be proven."),
    "EPS": ("interpreter safety", "the environment entry-point safety rule failed."),
    "PRE": ("evaluator-facts derivation", "CI could not derive a complete fact set from the declared root."),
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
REGISTRY_RELATIVE = "se_harness/codes.py"


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


def _parse(path: Path) -> ast.Module:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError) as exc:
        raise IndexError_(f"cannot parse {path}: {exc}") from exc


def registry(repository: Path) -> dict[str, str]:
    """The package's code registry, {constant name: code}, read through the parser (ECP-PRM-018).

    Every `NAME = "CODE"` assignment of `se_harness/codes.py` whose value has the
    code shape is an entry; an absent registry is empty, so a checkout without the
    package still indexes its literals.
    """

    path = repository / REGISTRY_RELATIVE
    if not path.is_file():
        return {}
    names: dict[str, str] = {}
    for node in _parse(path).body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            continue
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) and _CODE.fullmatch(node.value.value):
            names[node.targets[0].id] = node.value.value
    return names


def _collapse(message: str) -> str:
    message = " ".join(message.split())
    if len(message) > _MESSAGE_LIMIT:
        message = message[: _MESSAGE_LIMIT - 1] + "…"
    return message


def _joined_text(node: ast.AST, names: dict[str, str]) -> str:
    """The message text of a string or f-string node, registry names rendered as their codes."""

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue) and isinstance(value.value, ast.Name) and value.value.id in names:
                parts.append(names[value.value.id])
            else:
                parts.append("{…}")
        return "".join(parts)
    return ""


def _registry_name(node: ast.AST, names: dict[str, str]) -> str | None:
    if isinstance(node, ast.Name) and node.id in names:
        return node.id
    if isinstance(node, ast.Attribute) and node.attr in names:
        return node.attr
    return None


def _named_codes(tree: ast.Module, names: dict[str, str]):
    """Yield (prefix, code, message) for every site that passes a registry name with its message.

    Three shapes: a call whose arguments carry a registry name, the message being the
    longest string argument after it (`CodedError(WEX210, "...")`, `Diagnostic(path,
    E012, "...", plane)`, `_finding(W_HEX_001, "warning", "...")`); a dictionary keyed
    by a registry name whose value carries the text (`{W_REB_003: (owner, "...")}`);
    and an f-string whose first piece is a registry name followed by the message
    (`f"{WEX201}: ..."`).
    """

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.args:
            positions = [index for index, argument in enumerate(node.args) if _registry_name(argument, names) is not None]
            if not positions:
                continue
            first = positions[0]
            code = names[_registry_name(node.args[first], names)]
            texts = [_joined_text(argument, names) for argument in node.args[first + 1 :]]
            texts.extend(_joined_text(keyword.value, names) for keyword in node.keywords)
            texts = [text for text in texts if text]
            message = max(texts, key=len) if texts else ""
            yield _CODE.fullmatch(code).group(1), code, _collapse(f"{code}: {message}" if message else code)
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                name = _registry_name(key, names) if key is not None else None
                if name is None:
                    continue
                code = names[name]
                texts = [_joined_text(item, names) for item in ast.walk(value) if isinstance(item, (ast.Constant, ast.JoinedStr))]
                texts = [text for text in texts if text]
                message = max(texts, key=len) if texts else ""
                yield _CODE.fullmatch(code).group(1), code, _collapse(f"{code}: {message}" if message else code)
        elif isinstance(node, ast.JoinedStr) and node.values:
            first = node.values[0]
            if isinstance(first, ast.FormattedValue):
                name = _registry_name(first.value, names)
                if name is not None:
                    code = names[name]
                    yield _CODE.fullmatch(code).group(1), code, _collapse(_joined_text(node, names))


def _literal_codes(repository: Path):
    """Yield (prefix, code, collapsed message) for every code the source can emit.

    A code-shaped match inside a string literal counts wherever it is written; in
    the package, a raise site that passes a registry name is attributed to that
    code with its message text (ECP-PRM-018).
    """

    names = registry(repository)
    for path in _sources(repository):
        tree = _parse(path)
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            message = _collapse(node.value)
            for match in _CODE.finditer(node.value):
                yield match.group(1), match.group(0), message
        if names and (repository / "se_harness") in path.parents:
            yield from _named_codes(tree, names)


def scan(repository: Path) -> dict[str, dict[str, set[str]]]:
    """Return {prefix: {code: {message literals}}} for registered prefixes only."""

    codes: dict[str, dict[str, set[str]]] = {prefix: {} for prefix in PREFIXES}
    for prefix, code, message in _literal_codes(repository):
        if prefix in PREFIXES:
            codes[prefix].setdefault(code, set()).add(message)
    return codes


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
