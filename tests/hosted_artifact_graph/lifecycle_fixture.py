"""Independent, synthetic Phase 3 input; no real approvals or product assurance."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "docs/engineering/lifecycle-pilot"
WORK = "WO-P3-001"
VER = "VER-P3-001"
REL = "REL-P3-001"


def formal(ident, kind, title, body, relations=None, fields=None, tables=None):
    values = {"id": ident, "type": kind, "title": title, "status": "draft",
              "owners": ["test-owner"], "created": "2026-10-06", "updated": "2026-10-06", **(fields or {})}
    lines = ["+++"] + [f"{k} = {json.dumps(v)}" for k, v in values.items()]
    for name, table in (tables or {}).items():
        lines += ["", f"[{name}]"] + [f"{k} = {json.dumps(v)}" for k, v in table.items()]
    lines += ["", "[relations]"] + [f"{k} = {json.dumps(v)}" for k, v in (relations or {}).items()]
    lines += ["+++", "", "# " + title, "", "Synthetic rehearsal input. This is not a real human decision.", "", body, ""]
    return "\n".join(lines).encode()


def files():
    """Seven complete drafts. All lifecycle history must come from the release."""
    return {
        f"{DOMAIN}/intent/INT-P3-001.md": formal("INT-P3-001", "intent", "Inspect one rehearsal greeting",
            "An operator needs a fixed greeting for a disposable lifecycle rehearsal.\n"
            "Success is an observed exact greeting and exported test evidence. No real product or release is involved.",
            fields={"outcome": "The test operator observes Hello rehearsal."}),
        f"{DOMAIN}/capabilities/CAP-P3-001.md": formal("CAP-P3-001", "capability", "Read the rehearsal greeting",
            "The operator can read the fixed greeting from the local test fixture.",
            {"derives_from": ["INT-P3-001"]}, {"ability": "Read the exact rehearsal greeting."}),
        f"{DOMAIN}/requirements/REQ-P3-001.md": formal("REQ-P3-001", "requirement", "Return the exact rehearsal greeting",
            "## Acceptance\n\nCalling greeting() returns exactly `Hello rehearsal`.",
            {"derives_from": ["CAP-P3-001"]}, {"statement": "Calling greeting() returns Hello rehearsal.",
             "verification_method": ["test"], "priority": "must", "source": "Synthetic Phase 3 fixture"}),
        f"{DOMAIN}/specifications/SPEC-P3-001.md": formal("SPEC-P3-001", "specification", "Fixed rehearsal greeting",
            "**P3-GREET-001.** The fixture function greeting() returns the string `Hello rehearsal`.\n\n"
            "## Coverage\n\n| Requirement | Rules |\n| --- | --- |\n| REQ-P3-001 | P3-GREET-001 |",
            {"specifies": ["REQ-P3-001"]}, {"contract": "Return the fixed greeting without external effects."}),
        f"{DOMAIN}/verification/{VER}.md": formal(VER, "verification", "Independently assert the greeting",
            "## Independence\n\nExpected text is fixed by REQ-P3-001, not candidate output.\n\n"
            "## Requirement-to-evidence matrix\n\n| Requirement | Method | Case | Pass condition |\n"
            "| --- | --- | --- | --- |\n| REQ-P3-001 | test | exact greeting assertion | Equals Hello rehearsal |\n\n"
            f"Retain the actual assertion result in {DOMAIN}/evidence/{WORK}/assertion.json.",
            {"verifies": ["REQ-P3-001"]}),
        f"{DOMAIN}/work-orders/{WORK}.md": formal(WORK, "work_order", "Implement the synthetic greeting",
            "## Objective\n\nReturn the exact test greeting.\n\n## In scope\n\n"
            "Only the synthetic source, pilot definitions and test evidence.\n\n## Out of scope\n\n"
            "Real engineering records, real human decisions and external actions.\n\n"
            "## Authorized decision envelope\n\nAll supplied actors are synthetic test labels.\n\n"
            "## Required verification\n\nRun VER-P3-001 on the exact clean fixture commit.\n\n"
            "## Stop conditions\n\nStop when the released evaluator refuses.\n\n"
            "## Completion\n\nRetain actual outputs and candidate identity.",
            {"implements": ["REQ-P3-001"], "specifications": ["SPEC-P3-001"], "verification": [VER]},
            tables={"assurance": {"commit_bound_verification": "required", "rationale": "Synthetic fixture decision for test assurance.", "decided_by": "test-owner"},
                    "execution_scope": {"paths": ["src/greeting.py", DOMAIN + "/"]}}),
        f"{DOMAIN}/release/{REL}.md": formal(REL, "release_contract", "Prepare a test release record only",
            "Test version 0.0.1 binds this work and its verified test candidate. No tags, publication or deployment. "
            "Discard the disposable test project if replay fails. Retain the verification record and exact evidence.",
            {"gates": [WORK]}),
    }


def write(root: Path):
    for name, raw in files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

