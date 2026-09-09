"""Formal-artifact fixtures shared by the suite (SPEC-TST-002 TST-HYG-003, TST-HYG-006).

One `write`, one `formal` and the chain builders that every module needing a
standard repository with a governed chain imports. Nothing here reads the
repository under test; each helper writes exactly the bytes its caller names.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

COMPLETE_TITLE_SUFFIX = " title"

#: The released-evaluator evidence the chain builders write beside a record (SPEC-REV-001).
RELEASED_EVALUATOR_EVIDENCE_PATH = (
    "docs/engineering/product/evidence/released-evaluator.json"
)
RELEASED_EVALUATOR_EVIDENCE = {
    "schema": "se-harness-evaluator-evidence-v1",
    "role": "released-evaluator",
    "evaluator": {
        "version": "0.6.0",
        "payload_manifest": "se-harness-installed-payload-v1",
        "payload_sha256": "a" * 64,
        "archive_name": "se_harness-0.6.0-py3-none-any.whl",
        "archive_sha256": "b" * 64,
    },
    "origins": {
        "python_executable": "<evaluator-root>/bin/python",
        "module": "<evaluator-root>/lib/se_harness/runtime_identity.py",
        "distribution": "<evaluator-root>/lib/site-packages",
        "templates": "<evaluator-root>/share/se-harness/templates/repository/standard",
        "entry_point": "<evaluator-root>/bin/harnessctl",
    },
    "environment": {
        "isolated_python": True,
        "user_site_enabled": False,
        "pythonpath_present": False,
        "entry_point_resolved": True,
        "checkout_excluded": True,
    },
    "diagnostics": [],
}
RELEASED_EVALUATOR_EVIDENCE_BYTES = (
    json.dumps(
        RELEASED_EVALUATOR_EVIDENCE,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    + "\n"
).encode("utf-8")
RELEASED_EVALUATOR_EVIDENCE_SHA256 = hashlib.sha256(
    RELEASED_EVALUATOR_EVIDENCE_BYTES
).hexdigest()


def write(path: Path, content: str | bytes) -> Path:
    """Write `content` at `path`, creating parents. Text gets one trailing newline; bytes are exact."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def _array(values: list[str]) -> str:
    return json.dumps(list(values), ensure_ascii=False)


def formal(
    artifact_id: str,
    artifact_type: str,
    status: str,
    relations: dict[str, list[str]],
    extra: str = "",
    *,
    assessment: dict[str, object] | None = None,
    assessment_raw: str | None = None,
    complete: bool = False,
) -> str:
    """One formal artifact as TOML front matter.

    The minimal form (default) carries the identity, the lifecycle status, one
    owner, `extra` verbatim and the relations. The `complete` form is the
    architecture-traceability fixture: a technical owner, a statement on a
    requirement, an assurance table on a work order, an optional
    `[decision_assessment]` and a body heading, so the validator reads the
    artifact as approvable.
    """
    if not complete:
        relation_lines = "\n".join(f"{name} = {_array(targets)}" for name, targets in relations.items())
        return f'''+++
id = "{artifact_id}"
type = "{artifact_type}"
title = "{artifact_id}"
status = "{status}"
owners = ["owner"]
created = "2026-08-11"
updated = "2026-08-11"
{extra.strip()}

[relations]
{relation_lines}
+++

# {artifact_id}
'''
    lines = [
        "+++",
        f'id = "{artifact_id}"',
        f'type = "{artifact_type}"',
        f'title = "{artifact_id}{COMPLETE_TITLE_SUFFIX}"',
        f'status = "{status}"',
        'owners = ["technical-owner"]',
        'created = "2026-08-12"',
        'updated = "2026-08-12"',
    ]
    if artifact_type == "requirement":
        lines.extend(
            [
                'statement = "WHEN selected, THE SYSTEM SHALL behave deterministically."',
                'verification_method = "automated-test"',
            ]
        )
    if artifact_type == "work_order":
        lines.extend(
            [
                "",
                "[assurance]",
                'commit_bound_verification = "required"',
                'rationale = "The fixture changes trusted engineering behavior."',
                'decided_by = "test-owner"',
            ]
        )
    if extra.strip():
        lines.extend(["", extra.strip()])
    lines.extend(["", "[relations]"])
    lines.extend(f"{name} = {_array(values)}" for name, values in relations.items())
    if assessment is not None:
        lines.extend(
            [
                "",
                "[decision_assessment]",
                f'outcome = {json.dumps(assessment.get("outcome"), ensure_ascii=False)}',
                f'triggers = {_array(assessment.get("triggers", []))}',
                f'rationale = {json.dumps(assessment.get("rationale"), ensure_ascii=False)}',
                f'assessed_by = {json.dumps(assessment.get("assessed_by"), ensure_ascii=False)}',
            ]
        )
    elif assessment_raw is not None:
        lines.extend(["", "[decision_assessment]", assessment_raw])
    lines.extend(["+++", "", f"# {artifact_type}: {artifact_id}", ""])
    return "\n".join(lines)


def write_revision_policy(root: Path, *, required_for_verified_work: bool) -> None:
    write(
        root / ".engineering-harness.toml",
        f'''[revision_provenance]
required_for_verified_work = {str(required_for_verified_work).lower()}
required_for_release = false''',
    )


#: SPEC-AUT-004 (WO-AUT-006): the fixture architectures carry the typed relations
#: and a decision assessment, the shape the validator admits since the
#: compatibility windows closed; each is decided by the ADR beside it.
FIXTURE_ASSESSMENT = "\n".join(
    (
        "[decision_assessment]",
        'outcome = "adr_required"',
        'triggers = ["public-interface-or-protocol"]',
        'rationale = "The fixture architecture selects a public metadata contract."',
        'assessed_by = "technical-owner"',
    )
)


def create_base_chain(
    root: Path,
    *,
    work_order_status: str = "implemented",
    operating_contract_status: str = "approved",
) -> None:
    base = root / "docs/engineering/product"
    write(base / "intent/INT-001.md", formal("INT-001", "intent", "approved", {}))
    write(base / "capabilities/CAP-001.md", formal("CAP-001", "capability", "approved", {"derives_from": ["INT-001"]}))
    write(
        base / "requirements/REQ-001.md",
        formal(
            "REQ-001",
            "requirement",
            "implemented",
            {"derives_from": ["CAP-001"]},
            'statement = "THE SYSTEM SHALL retain revision provenance."\nverification_method = "automated-test"',
        ),
    )
    write(base / "specifications/SPEC-001.md", formal("SPEC-001", "specification", "implemented", {"specifies": ["REQ-001"]}))
    write(
        base / "architecture/ARCH-001.md",
        formal("ARCH-001", "architecture", "implemented", {"addresses": ["REQ-001"], "conforms_to": ["SPEC-001"]}, FIXTURE_ASSESSMENT),
    )
    write(base / "architecture/adr/ADR-001.md", formal("ADR-001", "adr", "approved", {"decides": ["ARCH-001"]}))
    write(base / "verification/VER-001.md", formal("VER-001", "verification", "approved", {"verifies": ["REQ-001"]}))
    write(
        base / "work-orders/WO-001.md",
        formal(
            "WO-001",
            "work_order",
            work_order_status,
            {
                "implements": ["REQ-001"],
                "specifications": ["SPEC-001"],
                "architecture": ["ARCH-001", "ADR-001"],
                "verification": ["VER-001"],
            },
        ),
    )
    write(base / "release/REL-001.md", formal("REL-001", "release_contract", "approved", {"gates": ["WO-001"]}))
    write(
        base / "operations/OPS-001.md",
        formal(
            "OPS-001",
            "operating_contract",
            operating_contract_status,
            {"assures": ["REQ-001"]},
        ),
    )
    write(base / "evidence/WO-001-verification.md", "# Evidence\n\nCandidate checks passed.")
    evaluator_evidence_path = root / RELEASED_EVALUATOR_EVIDENCE_PATH
    evaluator_evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evaluator_evidence_path.write_bytes(RELEASED_EVALUATOR_EVIDENCE_BYTES)


def create_additional_chain(root: Path, *, work_order_status: str = "implemented") -> None:
    base = root / "docs/engineering/product"
    write(
        base / "requirements/REQ-002.md",
        formal(
            "REQ-002",
            "requirement",
            "implemented",
            {"derives_from": ["CAP-001"]},
            'statement = "THE SYSTEM SHALL retain aggregate release scope."\nverification_method = "automated-test"',
        ),
    )
    write(base / "specifications/SPEC-002.md", formal("SPEC-002", "specification", "implemented", {"specifies": ["REQ-002"]}))
    write(
        base / "architecture/ARCH-002.md",
        formal("ARCH-002", "architecture", "implemented", {"addresses": ["REQ-002"], "conforms_to": ["SPEC-002"]}, FIXTURE_ASSESSMENT),
    )
    write(base / "architecture/adr/ADR-002.md", formal("ADR-002", "adr", "approved", {"decides": ["ARCH-002"]}))
    write(base / "verification/VER-002.md", formal("VER-002", "verification", "approved", {"verifies": ["REQ-002"]}))
    write(
        base / "work-orders/WO-002.md",
        formal(
            "WO-002",
            "work_order",
            work_order_status,
            {
                "implements": ["REQ-002"],
                "specifications": ["SPEC-002"],
                "architecture": ["ARCH-002", "ADR-002"],
                "verification": ["VER-002"],
            },
        ),
    )
    write(base / "release/REL-001.md", formal("REL-001", "release_contract", "approved", {"gates": ["WO-001", "WO-002"]}))
    write(base / "evidence/WO-002-verification.md", "# Evidence\n\nAggregate candidate checks passed.")


def verification_record(commit: str, object_format: str = "sha1", *, status: str = "verified", evidence: str = "docs/engineering/product/evidence/WO-001-verification.md") -> str:
    return formal(
        "VREC-001",
        "verification_record",
        status,
        {"verifies_work_order": ["WO-001"], "conforms_to": ["VER-001"]},
        f'''commit = "{commit}"
git_object_format = "{object_format}"
worktree_state = "clean"
verified_at = "2026-08-11T12:00:00Z"
artifact_snapshot_sha256 = "{'c' * 64}"
evidence_paths = ["{evidence}"]''',
    )


def release_record(commit: str, object_format: str = "sha1", *, record_id: str = "RLS-001", version: str = "1.0.0", status: str = "released") -> str:
    return formal(
        record_id,
        "release_record",
        status,
        {
            "satisfies": ["REL-001"],
            "includes_verification": ["VREC-001"],
            "releases_work": ["WO-001"],
        },
        f'''version = "{version}"
commit = "{commit}"
git_object_format = "{object_format}"
released_at = "2026-08-11T14:00:00Z"
authorized_by = "release-owner"
tag = "v{version}"
evaluator_evidence_path = "{RELEASED_EVALUATOR_EVIDENCE_PATH}"
evaluator_evidence_sha256 = "{RELEASED_EVALUATOR_EVIDENCE_SHA256}"''',
    ).replace('owners = ["owner"]', 'owners = ["release-owner"]')


def aggregate_verification_record(commit: str, *, status: str = "verified") -> str:
    return formal(
        "VREC-002",
        "verification_record",
        status,
        {"verifies_work_order": ["WO-001", "WO-002"], "conforms_to": ["VER-001", "VER-002"]},
        f'''commit = "{commit}"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-11T12:00:00Z"
artifact_snapshot_sha256 = "{'d' * 64}"
evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md", "docs/engineering/product/evidence/WO-002-verification.md"]''',
    )


def aggregate_release_record(commit: str, *, status: str = "released") -> str:
    return formal(
        "RLS-002",
        "release_record",
        status,
        {
            "satisfies": ["REL-001"],
            "includes_verification": ["VREC-002"],
            "releases_work": ["WO-001", "WO-002"],
        },
        f'''version = "2.0.0"
commit = "{commit}"
git_object_format = "sha1"
released_at = "2026-08-11T14:00:00Z"
authorized_by = "release-owner"
tag = "v2.0.0"
evaluator_evidence_path = "{RELEASED_EVALUATOR_EVIDENCE_PATH}"
evaluator_evidence_sha256 = "{RELEASED_EVALUATOR_EVIDENCE_SHA256}"''',
    ).replace('owners = ["owner"]', 'owners = ["release-owner"]')


def superseded_record(record: str, successor_id: str) -> str:
    lines = record.splitlines()
    lines = ['status = "superseded"' if line.startswith("status = ") else line for line in lines]
    relation_index = lines.index("[relations]")
    lines[relation_index:relation_index] = [
        'superseded_at = "2026-08-11T15:00:00Z"',
        'supersession_authorized_by = "quality-owner"',
        "",
    ]
    closing_index = lines.index("+++", relation_index)
    lines[closing_index:closing_index] = [f'superseded_by = ["{successor_id}"]']
    return "\n".join(lines) + "\n"
