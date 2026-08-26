"""Generating measurement for the frozen set in `SPEC-DLC-001` rule DLC-GEN-001.

The set of architectures exempt from the required decision assessment was measured
from this repository's own graph, not asserted. This module is that measurement. It
is read-only: it opens governed artifacts, reads front matter, and writes nothing.

The criterion is historical. It reproduces exactly which architectures the removed
lifecycle-status proxy exempted: an architecture carrying no `decision_assessment`
whose status was one of the three the proxy accepted. That criterion reads status on
purpose - it is a census of what the old rule did, and it is the only place in this
increment that does. The rule replacing it reads no status at all.

`unassessed_with_an_ongoing_status` is the figure that makes the frozen set complete.
It is empty, so every unassessed architecture in the graph is a member, and no
architecture is left needing an exemption the closed set cannot give it.

Regenerate the committed evidence from the repository root:

    python -m tests.definition_generation_measurement \\
      > docs/engineering/definition-lifecycle/evidence/WO-DLC-001/frozen_set_measurement.json
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path
from typing import Any


SCHEMA = "se-harness-definition-generation-measurement-v1"
SPECIFICATION = "SPEC-DLC-001"
RULE = "DLC-GEN-001"

# The three statuses the removed proxy accepted, reproduced here as the historical
# criterion of the census. No other code in this increment reads them.
PROXY_STATUSES = ("implemented", "verified", "released")

CRITERION = (
    "an architecture with no decision_assessment table, whose status was one of "
    + ", ".join(PROXY_STATUSES)
    + "; that is, exactly what the removed lifecycle-status proxy exempted"
)

EXCLUDED_PARTS = {".git", "evidence", "node_modules", "target", "templates"}


def _front_matter(path: Path) -> dict[str, Any] | None:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "+++":
        return None
    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "+++"
        )
    except StopIteration:
        return None
    value = tomllib.loads("\n".join(lines[1:closing]))
    return value if isinstance(value, dict) else None


def architectures(repository: Path) -> list[dict[str, Any]]:
    """Return every governed architecture with the two fields the census reads."""

    found: list[dict[str, Any]] = []
    artifact_root = repository / "docs" / "engineering"
    if not artifact_root.is_dir():
        return found
    for path in sorted(artifact_root.rglob("*.md"), key=lambda item: item.as_posix()):
        relative = path.relative_to(artifact_root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        metadata = _front_matter(path)
        if metadata is None or metadata.get("type") != "architecture":
            continue
        identifier = metadata.get("id")
        if not isinstance(identifier, str) or not identifier:
            continue
        found.append(
            {
                "id": identifier,
                "status": metadata.get("status"),
                "assessed": metadata.get("decision_assessment") is not None,
            }
        )
    return found


def measure(repository: Path) -> dict[str, Any]:
    """Return the census. Deterministic: no clock, no environment, no Git state."""

    found = architectures(repository)
    unassessed = [item for item in found if not item["assessed"]]
    return {
        "schema": SCHEMA,
        "specification": SPECIFICATION,
        "rule": RULE,
        "criterion": CRITERION,
        "architectures": len(found),
        "architectures_with_decision_assessment": len(found) - len(unassessed),
        "architectures_without_decision_assessment": sorted(
            item["id"] for item in unassessed if item["status"] in PROXY_STATUSES
        ),
        "unassessed_with_an_ongoing_status": sorted(
            item["id"] for item in unassessed if item["status"] not in PROXY_STATUSES
        ),
    }


def main(arguments: list[str]) -> int:
    repository = Path(arguments[0]) if arguments else Path(".")
    json.dump(measure(repository.resolve()), sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
