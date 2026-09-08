#!/usr/bin/env python3
"""Amend `SPEC-AUT-001` by record for `AUT-MIG-008` (WO-AUT-005).

`AUT-VOC-003` names `WO-AUT-002` as the work order that runs the vocabulary
migration once. That run never happened, so `SPEC-AUT-003` rule `AUT-MIG-008`
requires an amendment record stating where it did happen and where its
evidence is retained. The script appends one paragraph to the existing
`## Amendment record` section and moves `updated`; it refuses a repository it
has already amended. ``--apply`` writes; the default is a dry run.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

SPECIFICATION = "docs/engineering/artifact-authoring/specifications/SPEC-AUT-001.md"
UPDATED = "2026-09-08"
UPDATED_LINE = re.compile(r'^updated = "\d{4}-\d{2}-\d{2}"$', re.MULTILINE)
HEADING = "## Amendment record"

AMENDMENT = """
**`AUT-VOC-003`'s migration ran under `WO-AUT-005`, applied 2026-09-08.**
`AUT-VOC-003` places the one-shot script under `WO-AUT-002`. That work order
wrote the script and retained its mapping table in
`evidence/WO-AUT-002/verification-method-mapping.json`, but the run itself was
never applied: the root evaluator of the day still required a string
`verification_method`. `WO-AUT-005` applied it once over the 32 `requirements/`
directories under `SPEC-AUT-003` rules `AUT-MIG-005` and `AUT-MIG-006`: 267
strings mapped by the rules of `REQ-AUT-003`, and the four the rules cannot
map (`REQ-REB-004`, `REQ-REB-011`, `REQ-REB-014`, `REQ-REB-018`) set to
`["test"]` as recorded steward decisions. Each migrated requirement keeps its
original string in `verification_notes`. The script, the applied and
second-run reports and the four decisions with their reasons are retained in
`evidence/WO-AUT-005/`; under `AUT-MIG-007` the script then left `scripts/`.
The vocabulary, the mapping rules and the transition `AUT-VOC-002` describes
are unchanged; nothing else in this specification changes.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true", help="write the file; default is a dry run")
    args = parser.parse_args(argv)

    path = args.root.resolve() / SPECIFICATION
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")

    if "WO-AUT-005" in text:
        print("refusing: SPEC-AUT-001 already names WO-AUT-005", file=sys.stderr)
        return 2
    if HEADING not in text:
        print(f"refusing: no {HEADING!r} section", file=sys.stderr)
        return 2
    if not UPDATED_LINE.search(text):
        print("refusing: no updated line in the front matter", file=sys.stderr)
        return 2

    amended = UPDATED_LINE.sub(f'updated = "{UPDATED}"', text, count=1)
    amended = amended.rstrip("\n") + "\n\n" + AMENDMENT.lstrip("\n")

    if amended == text:
        print("refusing: no change computed", file=sys.stderr)
        return 2
    diff = difflib.unified_diff(
        text.splitlines(keepends=True),
        amended.splitlines(keepends=True),
        fromfile=SPECIFICATION,
        tofile=f"{SPECIFICATION} (amended)",
    )
    sys.stdout.writelines(diff)
    if args.apply:
        path.write_bytes(amended.replace("\n", newline).encode("utf-8"))
        print(f"amended {SPECIFICATION}", file=sys.stderr)
    else:
        print("dry run; pass --apply to write", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
