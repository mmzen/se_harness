#!/usr/bin/env python3
"""Apply the four steward decisions of AUT-MIG-006 by script.

Retained evidence for `WO-AUT-005`. `migrate_verification_methods.py` cannot
map these four strings: none of them names a test, review, analysis or
demonstration word its rules recognise, although each describes an automated
suite. `SPEC-AUT-003` rule `AUT-MIG-006` names the four requirements and fixes
the mapping to `["test"]`, with the original string kept in
`verification_notes`. ``--apply`` writes; the default is a dry run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DECISIONS: dict[str, dict[str, str]] = {
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-004.md": {
        "requirement": "REQ-REB-004",
        "original": "automated-active-surface-invariant",
        "reason": (
            "The measure is an invariant over the released evaluator's active surface, asserted by "
            "the candidate suite on every run. It is executed, not read, so the closed vocabulary "
            "word is test; no human reading is required for the verdict."
        ),
    },
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-011.md": {
        "requirement": "REQ-REB-011",
        "original": "automated-release-version-lifecycle-matrix",
        "reason": (
            "A matrix of release versions and lifecycle states is a parametrised automated suite. "
            "The word matrix names the shape of the cases, not a second method, so the vocabulary "
            "word is test."
        ),
    },
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-014.md": {
        "requirement": "REQ-REB-014",
        "original": "automated-python311-linux-windows-failure-injection-matrix",
        "reason": (
            "Failure injection across two platforms and one interpreter version is executed by the "
            "hosted lanes and the local suite. Platform coverage is a case dimension, so the "
            "vocabulary word is test."
        ),
    },
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-018.md": {
        "requirement": "REQ-REB-018",
        "original": "automated-contract-consumer-conformance",
        "reason": (
            "Consumer conformance to the published contract is asserted by executing the consumer "
            "against it. Conformance here is an executed comparison rather than an inspected one, "
            "so the vocabulary word is test."
        ),
    },
}

METHOD_LINE = re.compile(r'^verification_method = "(.*)"$', re.MULTILINE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true", help="write the files; default is a dry run")
    parser.add_argument("--report", type=Path, help="write the JSON decision record to this path")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    record: dict[str, object] = {
        "schema": "se-harness-steward-decision-record-v1",
        "work_order": "WO-AUT-005",
        "rule": "AUT-MIG-006",
        "decided_by": "requirements-steward",
        "applied": bool(args.apply),
        "decisions": {},
    }
    for relative, decision in DECISIONS.items():
        path = root / relative
        raw = path.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        text = raw.decode("utf-8").replace("\r\n", "\n")
        match = METHOD_LINE.search(text)
        if match is None:
            print(f"refusing {relative}: no string verification_method", file=sys.stderr)
            return 2
        if match.group(1) != decision["original"]:
            print(f"refusing {relative}: expected {decision['original']!r}, read {match.group(1)!r}", file=sys.stderr)
            return 2
        replacement = (
            'verification_method = ["test"]\n'
            f"verification_notes = {json.dumps(decision['original'])}"
        )
        migrated = text[: match.start()] + replacement + text[match.end() :]
        if args.apply:
            path.write_bytes(migrated.replace("\n", newline).encode("utf-8"))
        record["decisions"][decision["requirement"]] = {
            "path": relative,
            "original": decision["original"],
            "mapped": ["test"],
            "reason": decision["reason"],
        }
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        # LF bytes: `.gitattributes` declares `docs/engineering/**/evidence/*.json`
        # as `text eol=lf`, and text mode would write CRLF on Windows.
        args.report.write_bytes(rendered.encode("utf-8"))
    else:
        print(rendered, end="")
    print(f"{len(record['decisions'])} steward decisions", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
