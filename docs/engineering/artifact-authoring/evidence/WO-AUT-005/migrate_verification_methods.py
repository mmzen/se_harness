#!/usr/bin/env python3
"""Map free-text requirement verification_method strings to the closed vocabulary (SPEC-AUT-001 AUT-VOC-003).

Repository-owned. Touches only the ``verification_method`` line of each requirement's
front matter and adds ``verification_notes`` carrying the original string. Idempotent:
a requirement whose value is already an array is skipped. Refuses a file whose front
matter cannot be parsed. ``--apply`` writes; the default is a dry run that prints the
mapping report as JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

VOCABULARY = ("test", "analysis", "inspection", "demonstration")
RULES = (
    ("test", ("test",)),
    ("inspection", ("review", "inspection", "walkthrough")),
    ("analysis", ("analysis", "assessment", "replay")),
    ("demonstration", ("demonstration", "rehearsal", "end-to-end")),
)
METHOD_LINE = re.compile(r'^verification_method = "(.*)"$', re.MULTILINE)


def map_value(value: str) -> list[str]:
    lowered = value.lower()
    mapped = [method for method, needles in RULES if any(needle in lowered for needle in needles)]
    return mapped


def migrate_text(text: str) -> tuple[str, dict[str, object]]:
    match = METHOD_LINE.search(text)
    if match is None:
        return text, {"state": "skipped", "reason": "no string verification_method"}
    original = match.group(1)
    closing = text.find("\n+++", 3)
    if closing < 0:
        raise ValueError("front matter is not closed")
    tomllib.loads(text[4:closing])  # refuse unparseable front matter
    mapped = map_value(original)
    if not mapped:
        return text, {"state": "unmatched", "original": original}
    array = "[" + ", ".join(json.dumps(item) for item in mapped) + "]"
    replacement = f"verification_method = {array}\nverification_notes = {json.dumps(original)}"
    if "\nverification_notes = " in text[:closing]:
        replacement = f"verification_method = {array}"
    return text[: match.start()] + replacement + text[match.end():], {"state": "mapped", "original": original, "mapped": mapped}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true", help="write the migrated files; default is a dry run")
    parser.add_argument("--report", type=Path, help="write the JSON mapping report to this path")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    files = sorted((root / "docs" / "engineering").rglob("requirements/REQ-*.md"))
    report: dict[str, object] = {"schema": "se-harness-verification-method-migration-v1", "applied": bool(args.apply), "files": {}}
    unmatched = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        text = raw.decode("utf-8").replace("\r\n", "\n")
        try:
            migrated, entry = migrate_text(text)
        except (ValueError, tomllib.TOMLDecodeError) as exc:
            print(f"refusing {relative}: {exc}", file=sys.stderr)
            return 2
        report["files"][relative] = entry
        if entry["state"] == "unmatched":
            unmatched += 1
        if args.apply and migrated != text:
            path.write_bytes(migrated.replace("\n", newline).encode("utf-8"))
    counts = {state: sum(1 for item in report["files"].values() if item["state"] == state) for state in ("mapped", "unmatched", "skipped")}
    report["counts"] = counts
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    print(f"{counts['mapped']} mapped, {counts['unmatched']} unmatched (steward decision), {counts['skipped']} already migrated", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
