from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_harness_dashboard import build_dashboard_bundle, generate_snapshot  # noqa: E402
from inspect_engineering_artifacts import build_inspection  # noqa: E402
from validate_engineering_artifacts import evidence_work_order_keys, validate_repository  # noqa: E402
from tests.mutation_guard_support import trusted_mutation_authority  # noqa: E402

from se_harness.cli import main  # noqa: E402
from se_harness.preflight import _load_validator_module  # noqa: E402
from se_harness.provenance import _evidence_work_order_keys  # noqa: E402
from tests.fixture_support import standard_repository


EVIDENCE_KEY_CASES = (
    ("docs/engineering/example/evidence/WO-ABC-001-check.md", ("WO-ABC-001",)),
    ("docs/engineering/example/evidence/WO-ABC-001/check.md", ("WO-ABC-001",)),
    ("docs/engineering/example/evidence/archive/WO-ABC-001/check.md", ("WO-ABC-001",)),
    ("docs/engineering/WO-ABC-001/evidence/check.md", ()),
    ("docs/engineering/example/evidence/X-WO-ABC-001/check.md", ()),
    ("docs/engineering/example/evidence/wo-abc-001/check.md", ()),
    ("docs/engineering/example/evidence/WO-ABC-0010/check.md", ()),
    ("docs/engineering/example/evidence/WO-ABC-001_check.md", ()),
    ("docs/engineering/example/Evidence/WO-ABC-001/check.md", ()),
    (
        "docs/engineering/example/evidence/WO-ABC-001/WO-ABC-001-check.md",
        ("WO-ABC-001",),
    ),
    (
        "docs/engineering/example/evidence/WO-XYZ-002/WO-ABC-001-check.md",
        ("WO-ABC-001", "WO-XYZ-002"),
    ),
    ("reports/WO-ABC-001.md", ("WO-ABC-001",)),
)

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


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_revision_policy(root: Path, *, required_for_verified_work: bool) -> None:
    write(
        root / ".engineering-harness.toml",
        f'''[revision_provenance]
required_for_verified_work = {str(required_for_verified_work).lower()}
required_for_release = false''',
    )


def formal(
    artifact_id: str,
    artifact_type: str,
    status: str,
    relations: dict[str, list[str]],
    extra: str = "",
) -> str:
    relation_lines = "\n".join(
        f"{name} = [{', '.join(json.dumps(item) for item in targets)}]"
        for name, targets in relations.items()
    )
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
    write(base / "architecture/ARCH-001.md", formal("ARCH-001", "architecture", "implemented", {"constrains": ["REQ-001"]}))
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
    write(base / "architecture/ARCH-002.md", formal("ARCH-002", "architecture", "implemented", {"constrains": ["REQ-002"]}))
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


class EvidenceKeyContractTests(unittest.TestCase):
    def test_package_and_portable_predicates_share_the_complete_contract_matrix(self) -> None:
        for path, expected in EVIDENCE_KEY_CASES:
            with self.subTest(path=path):
                self.assertEqual(expected, _evidence_work_order_keys(path))
                self.assertEqual(expected, evidence_work_order_keys(path))


class RevisionValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        create_base_chain(self.root, work_order_status="released")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def errors(self) -> set[str]:
        return {item.code for item in validate_repository(self.root).errors}

    def test_valid_sha1_and_sha256_records(self) -> None:
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("a" * 40))
        write(self.root / "docs/engineering/releases/RLS-001.md", release_record("a" * 40))
        self.assertEqual([], validate_repository(self.root).errors)

        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("b" * 64, "sha256"))
        write(self.root / "docs/engineering/releases/RLS-001.md", release_record("b" * 64, "sha256"))
        self.assertEqual([], validate_repository(self.root).errors)

    def test_invalid_revision_metadata_and_evidence_are_blocking(self) -> None:
        invalid = verification_record("ABC", evidence="../outside.md").replace('worktree_state = "clean"', 'worktree_state = "dirty"')
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", invalid)
        self.assertTrue({"E009", "E012"}.issubset(self.errors()))

    def test_missing_and_absolute_evidence_are_blocking(self) -> None:
        record = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        for evidence in ("docs/engineering/product/evidence/absent.md", "C:/outside.md"):
            with self.subTest(evidence=evidence):
                write(record, verification_record("a" * 40, evidence=evidence))
                self.assertIn("E012", self.errors())

    def test_symlinked_evidence_is_blocking_when_supported(self) -> None:
        evidence_link = self.root / "docs/engineering/product/evidence-link.md"
        evidence_target = self.root / "docs/engineering/product/evidence/WO-001-verification.md"
        try:
            os.symlink(evidence_target, evidence_link)
        except OSError as exc:
            self.skipTest(f"host cannot create test symlink: {exc}")
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            verification_record("a" * 40, evidence="docs/engineering/product/evidence-link.md"),
        )
        self.assertIn("E012", self.errors())

    def test_typed_relations_commit_consistency_and_duplicate_versions(self) -> None:
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("a" * 40, status="ready"))
        invalid_release = release_record("b" * 40).replace('includes_verification = ["VREC-001"]', 'includes_verification = ["VER-001"]')
        write(self.root / "docs/engineering/releases/RLS-001.md", invalid_release)
        self.assertIn("E011", self.errors())

        write(self.root / "docs/engineering/releases/RLS-001.md", release_record("b" * 40))
        write(self.root / "docs/engineering/releases/RLS-002.md", release_record("a" * 40, record_id="RLS-002"))
        self.assertIn("E010", self.errors())

    def test_existing_chain_without_records_remains_valid(self) -> None:
        self.assertEqual([], validate_repository(self.root).errors)

        write_revision_policy(self.root, required_for_verified_work=False)
        self.assertEqual([], validate_repository(self.root).errors)

    def test_configured_verified_work_requires_eligible_verification_record(self) -> None:
        write_revision_policy(self.root, required_for_verified_work=True)
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertIn(
            "released work order requires coverage by a verified or released verification record",
            messages,
        )

        record_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(record_path, verification_record("a" * 40, status="ready"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertIn(
            "released work order requires coverage by a verified or released verification record",
            messages,
        )

        write(record_path, verification_record("a" * 40, status="verified"))
        self.assertEqual([], validate_repository(self.root).errors)

        write(record_path, verification_record("a" * 40, status="released"))
        self.assertEqual([], validate_repository(self.root).errors)

    def test_dashboard_uses_authoritative_verified_work_error_without_duplicate_warning(self) -> None:
        write_revision_policy(self.root, required_for_verified_work=True)
        snapshot, report, _ = generate_snapshot(self.root)

        self.assertFalse(report.valid)
        self.assertIn("E010", {item["code"] for item in snapshot["diagnostics"]})
        self.assertNotIn("W-REV-001", {item["rule"] for item in snapshot["findings"]})

    def test_existing_single_work_record_may_select_declared_contract_subset(self) -> None:
        base = self.root / "docs/engineering/product"
        write(base / "verification/VER-002.md", formal("VER-002", "verification", "approved", {"verifies": ["REQ-001"]}))
        work_order = formal(
            "WO-001",
            "work_order",
            "released",
            {
                "implements": ["REQ-001"],
                "specifications": ["SPEC-001"],
                "architecture": ["ARCH-001", "ADR-001"],
                "verification": ["VER-001", "VER-002"],
            },
        )
        write(base / "work-orders/WO-001.md", work_order)
        write(base / "verification-records/VREC-001.md", verification_record("a" * 40))
        self.assertEqual([], validate_repository(self.root).errors)

    def test_valid_aggregate_records_cover_all_work_at_one_commit(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", aggregate_verification_record("a" * 40))
        write(self.root / "docs/engineering/releases/RLS-002.md", aggregate_release_record("a" * 40))
        self.assertEqual([], validate_repository(self.root).errors)

        snapshot, _, _ = generate_snapshot(self.root)
        release = next(item for item in snapshot["revision_provenance"] if item["id"] == "RLS-002")
        self.assertEqual(["WO-001", "WO-002"], release["work_orders"])
        self.assertEqual(["VREC-002"], release["verification_records"])

    def test_directory_keyed_aggregate_record_drives_validation_findings_and_readiness(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        flat_one = self.root / "docs/engineering/product/evidence/WO-001-verification.md"
        flat_two = self.root / "docs/engineering/product/evidence/WO-002-verification.md"
        flat_one.unlink()
        flat_two.unlink()
        first_path = "docs/engineering/product/evidence/WO-001/check.md"
        second_path = "docs/engineering/product/evidence/archive/WO-002/check.md"
        write(self.root / first_path, "# Evidence one")
        write(self.root / second_path, "# Evidence two")
        record = aggregate_verification_record("a" * 40).replace(
            'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md", "docs/engineering/product/evidence/WO-002-verification.md"]',
            f'evidence_paths = ["{first_path}", "{second_path}"]',
        )
        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", record)

        snapshot, report, _ = generate_snapshot(self.root)
        self.assertTrue(report.valid)
        self.assertNotIn(
            "W-HEX-001",
            {
                finding["rule"]
                for finding in snapshot["findings"]
                if set(finding["artifacts"]) & {"WO-001", "WO-002"}
            },
        )
        inspection = build_inspection(snapshot, report)
        self.assertNotIn(
            "W-HEX-001",
            {
                finding["rule"]
                for finding in inspection["findings"]
                if set(finding["artifacts"]) & {"WO-001", "WO-002"}
            },
        )
        evidence = {item["work_order"]: item["paths"] for item in snapshot["evidence"]}
        self.assertEqual([first_path], evidence["WO-001"])
        self.assertEqual([second_path], evidence["WO-002"])
        for work_order_id, expected_path in (("WO-001", first_path), ("WO-002", second_path)):
            readiness = next(
                item for item in snapshot["readiness"] if item["work_order"] == work_order_id
            )
            implementation_gate = next(
                gate for gate in readiness["gates"] if gate["gate"] == "G3"
            )
            evidence_condition = next(
                condition
                for condition in implementation_gate["conditions"]
                if condition["id"] == "verification_evidence"
            )
            self.assertEqual("satisfied", evidence_condition["state"])
            self.assertEqual([expected_path], evidence_condition["evidence"])

    def test_aggregate_records_reject_incomplete_or_extra_scope(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        record = aggregate_verification_record("a" * 40).replace(
            'conforms_to = ["VER-001", "VER-002"]',
            'conforms_to = ["VER-001"]',
        )
        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", record)
        self.assertIn("E010", self.errors())

        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", aggregate_verification_record("a" * 40))
        release = aggregate_release_record("a" * 40).replace(
            'releases_work = ["WO-001", "WO-002"]',
            'releases_work = ["WO-001"]',
        )
        write(self.root / "docs/engineering/releases/RLS-002.md", release)
        self.assertIn("E010", self.errors())

    def test_aggregate_records_reject_duplicate_and_unkeyed_evidence(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        duplicate = aggregate_verification_record("a" * 40).replace(
            'verifies_work_order = ["WO-001", "WO-002"]',
            'verifies_work_order = ["WO-001", "WO-002", "WO-002"]',
        )
        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", duplicate)
        self.assertIn("E010", self.errors())

        unkeyed = aggregate_verification_record("a" * 40).replace(
            'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md", "docs/engineering/product/evidence/WO-002-verification.md"]',
            'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md"]',
        )
        write(self.root / "docs/engineering/product/verification-records/VREC-002.md", unkeyed)
        self.assertIn("E010", self.errors())

    def test_dashboard_projects_declared_commit_and_checkout_state(self) -> None:
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("a" * 40))
        write(self.root / "docs/engineering/releases/RLS-001.md", release_record("a" * 40))
        snapshot, report, _ = generate_snapshot(self.root)
        self.assertTrue(report.valid)
        self.assertEqual({"VREC-001", "RLS-001"}, {item["id"] for item in snapshot["revision_provenance"]})
        self.assertTrue(all(item["match_state"] == "not_assessable" for item in snapshot["revision_provenance"]))
        self.assertTrue(all(item["commit_available"] is None for item in snapshot["revision_provenance"]))
        vrec = next(item for item in snapshot["artifacts"] if item["id"] == "VREC-001")
        self.assertEqual("a" * 40, vrec["commit"])

    def test_dashboard_reports_exact_and_different_checkout_states(self) -> None:
        subprocess.run(["git", "init", "-b", "main", str(self.root)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "candidate"], check=True, capture_output=True)
        candidate = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record(candidate))
        snapshot, _, _ = generate_snapshot(self.root)
        self.assertEqual("exact", snapshot["revision_provenance"][0]["match_state"])
        self.assertTrue(snapshot["revision_provenance"][0]["commit_available"])
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "governance"], check=True, capture_output=True)
        snapshot, _, _ = generate_snapshot(self.root)
        self.assertEqual("different", snapshot["revision_provenance"][0]["match_state"])
        self.assertIn("I-REV-001", {item["rule"] for item in snapshot["findings"]})

    def test_valid_supersession_preserves_coverage_and_projects_lineage(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        source = superseded_record(verification_record("a" * 40), "VREC-002")
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", source)
        write(
            self.root / "docs/engineering/product/verification-records/VREC-002.md",
            aggregate_verification_record("b" * 40),
        )

        report = validate_repository(self.root)
        self.assertEqual([], report.errors)
        snapshot, _, _ = generate_snapshot(self.root)
        source_projection = next(item for item in snapshot["revision_provenance"] if item["id"] == "VREC-001")
        successor_projection = next(item for item in snapshot["revision_provenance"] if item["id"] == "VREC-002")
        self.assertEqual("historical", source_projection["lifecycle_class"])
        self.assertEqual(["VREC-002"], source_projection["superseded_by"])
        self.assertEqual("2026-08-11T15:00:00Z", source_projection["superseded_at"])
        self.assertEqual("quality-owner", source_projection["supersession_authorized_by"])
        self.assertEqual(["VREC-001"], successor_projection["supersedes"])
        self.assertNotIn("W-REV-004", {item["rule"] for item in snapshot["findings"]})
        _, manifest, resources, _ = build_dashboard_bundle(snapshot)
        readiness = json.loads(resources[manifest["entrypoints"]["readiness"]["path"]])
        source = next(item for item in readiness["revision_provenance"] if item["id"] == "VREC-001")
        self.assertEqual(["VREC-002"], source["superseded_by"])
        self.assertEqual("quality-owner", source["supersession_authorized_by"])

    def test_prepared_supersession_uses_preparation_not_verification_decision_fields(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        candidate_validator = _load_validator_module()
        current_source = verification_record("a" * 40).replace(
            'verified_at = "2026-08-11T12:00:00Z"',
            'prepared_at = "2026-08-11T12:00:00Z"\nprepared_by = "quality-owner"',
        )
        valid_source = superseded_record(current_source, "VREC-002")
        source_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(source_path, valid_source)
        write(
            self.root / "docs/engineering/product/verification-records/VREC-002.md",
            aggregate_verification_record("b" * 40),
        )
        self.assertEqual([], candidate_validator.validate_repository(self.root).errors)

        for decision_field in (
            'verified_at = "2026-08-11T12:00:00Z"',
            'verified_by = "quality-owner"',
        ):
            with self.subTest(decision_field=decision_field):
                invalid = valid_source.replace(
                    'artifact_snapshot_sha256 =',
                    f'{decision_field}\nartifact_snapshot_sha256 =',
                    1,
                )
                write(source_path, invalid)
                messages = {
                    item.message
                    for item in candidate_validator.validate_repository(self.root).errors
                }
                field_name = decision_field.split(" =", 1)[0]
                self.assertIn(
                    f"prepared superseded verification_record must omit decision field '{field_name}'",
                    messages,
                )

    def test_supersession_requires_structured_fields_only_on_superseded_records(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        record_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(record_path, verification_record("a" * 40, status="superseded"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("superseded_at" in message for message in messages))
        self.assertTrue(any("supersession_authorized_by" in message for message in messages))
        self.assertTrue(any("superseded_by" in message for message in messages))

        invalid_ready = superseded_record(verification_record("a" * 40, status="ready"), "VREC-002").replace(
            'status = "superseded"', 'status = "ready"', 1
        )
        write(record_path, invalid_ready)
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("allowed only" in message and "superseded_at" in message for message in messages))
        self.assertTrue(any("allowed only" in message and "superseded_by" in message for message in messages))

        write(
            self.root / "docs/engineering/product/verification-records/VREC-002.md",
            aggregate_verification_record("b" * 40),
        )
        invalid_fields = superseded_record(verification_record("a" * 40), "VREC-002").replace(
            'superseded_at = "2026-08-11T15:00:00Z"',
            'superseded_at = "2026-08-11"',
        ).replace(
            'supersession_authorized_by = "quality-owner"',
            'supersession_authorized_by = " "',
        )
        write(record_path, invalid_fields)
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("superseded_at" in message and "YYYY-MM-DDTHH:MM:SSZ" in message for message in messages))
        self.assertTrue(any("supersession_authorized_by" in message and "non-empty string" in message for message in messages))

    def test_supersession_rejects_ineligible_target_lost_coverage_and_cycles(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        first_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        second_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"

        write(first_path, superseded_record(verification_record("a" * 40), "VREC-002"))
        write(second_path, aggregate_verification_record("b" * 40, status="ready"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("must be verified or released" in message for message in messages))

        aggregate_source = superseded_record(aggregate_verification_record("b" * 40), "VREC-001")
        write(first_path, verification_record("a" * 40))
        write(second_path, aggregate_source)
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("omits work orders: WO-002" in message for message in messages))

        write(first_path, superseded_record(verification_record("a" * 40), "VREC-002"))
        write(second_path, superseded_record(aggregate_verification_record("b" * 40), "VREC-001"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("supersession cycle detected" in message for message in messages))

    def test_supersession_rejects_wrong_type_duplicate_and_active_release_reference(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        source_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        successor_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"
        write(successor_path, aggregate_verification_record("a" * 40))

        write(source_path, superseded_record(verification_record("a" * 40), "VER-001"))
        self.assertIn("E011", self.errors())

        write(source_path, superseded_record(verification_record("a" * 40), "VREC-999"))
        self.assertIn("E006", self.errors())

        write(source_path, superseded_record(verification_record("a" * 40), "VREC-001"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("supersession cycle detected" in message for message in messages))

        third = aggregate_verification_record("c" * 40).replace("VREC-002", "VREC-003")
        write(self.root / "docs/engineering/product/verification-records/VREC-003.md", third)
        multiple = superseded_record(verification_record("a" * 40), "VREC-002").replace(
            'superseded_by = ["VREC-002"]',
            'superseded_by = ["VREC-002", "VREC-003"]',
        )
        write(source_path, multiple)
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("must contain exactly one verification record" in message for message in messages))

        duplicate = superseded_record(verification_record("a" * 40), "VREC-002").replace(
            'superseded_by = ["VREC-002"]',
            'superseded_by = ["VREC-002", "VREC-002"]',
        )
        write(source_path, duplicate)
        self.assertTrue({"E009", "E010"}.issubset(self.errors()))

        write(source_path, superseded_record(verification_record("a" * 40), "VREC-002"))
        write(self.root / "docs/engineering/releases/RLS-001.md", release_record("a" * 40, status="ready"))
        messages = {item.message for item in validate_repository(self.root).errors}
        self.assertTrue(any("must not include superseded" in message for message in messages))

    def test_dashboard_reports_stale_ready_without_inferring_supersession(self) -> None:
        create_additional_chain(self.root, work_order_status="released")
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            verification_record("a" * 40, status="ready"),
        )
        write(
            self.root / "docs/engineering/product/verification-records/VREC-002.md",
            aggregate_verification_record("b" * 40),
        )
        snapshot, report, _ = generate_snapshot(self.root)
        self.assertTrue(report.valid)
        findings = [item for item in snapshot["findings"] if item["rule"] == "W-REV-004"]
        self.assertEqual(1, len(findings))
        self.assertEqual(["VREC-001", "VREC-002"], findings[0]["artifacts"])
        source = next(item for item in snapshot["revision_provenance"] if item["id"] == "VREC-001")
        self.assertEqual("ready", source["status"])
        self.assertEqual([], source["superseded_by"])


class RevisionCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(arguments))
        return code, stdout.getvalue(), stderr.getvalue()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        return completed.stdout.strip()

    def initialize_candidate(self, *, aggregate: bool = False) -> str:
        standard_repository(self.root, "Revision Sample")
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        evaluator = lock["evaluator"]
        evaluator["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        evaluator["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        create_base_chain(self.root, operating_contract_status="draft")
        if aggregate:
            create_additional_chain(self.root)
        self.git("init", "-b", "main")
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", ".")
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "candidate")
        return self.git("rev-parse", "HEAD")

    def test_capture_and_prepare_bind_candidate_without_commits_or_tags(self) -> None:
        candidate = self.initialize_candidate()
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(0, code, error)
        self.assertIn("ready verification record", output)
        vrec_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        self.assertIn(f'commit = "{candidate}"', vrec_path.read_text(encoding="utf-8"))
        self.assertIn('status = "ready"', vrec_path.read_text(encoding="utf-8"))
        self.assertIn('prepared_by = "quality-owner"', vrec_path.read_text(encoding="utf-8"))
        self.assertNotIn("verified_at =", vrec_path.read_text(encoding="utf-8"))
        self.assertEqual(candidate, self.git("rev-parse", "HEAD"))
        self.assertEqual("", self.git("tag", "--list"))
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)

        evaluator_evidence = self.root / "docs/engineering/product/evidence/VREC-001-evaluator.json"
        self.assertTrue(evaluator_evidence.is_file())
        self.git(
            "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid",
            "add", str(vrec_path), str(evaluator_evidence),
        )
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "verification governance")
        governance = self.git("rev-parse", "HEAD")
        self.assertNotEqual(candidate, governance)
        lock_before_release = (self.root / ".engineering-harness.lock").read_bytes()

        code, output, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-001",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-001",
            "--work-order", "WO-001",
            "--version", "1.0.0",
            "--owner", "release-owner",
            "--tag", "v1.0.0",
            "--domain", "delivery",
        )
        self.assertEqual(0, code, error)
        self.assertIn("ready release record", output)
        release_path = self.root / "docs/engineering/delivery/releases/RLS-001.md"
        release_text = release_path.read_text(encoding="utf-8")
        self.assertIn(f'commit = "{candidate}"', release_text)
        self.assertIn('status = "ready"', release_text)
        self.assertIn('prepared_by = "release-owner"', release_text)
        self.assertNotIn("released_at =", release_text)
        self.assertNotIn("authorized_by =", release_text)
        self.assertEqual(governance, self.git("rev-parse", "HEAD"))
        self.assertEqual("", self.git("tag", "--list"))
        self.assertEqual(lock_before_release, (self.root / ".engineering-harness.lock").read_bytes())
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

        validator = self.root / "scripts/validate_engineering_artifacts.py"
        completed = subprocess.run(
            [sys.executable, str(validator), "--root", str(self.root), "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        historical_release = (
            release_text
            .replace('status = "ready"', 'status = "released"')
            .replace(
                'prepared_by = "release-owner"',
                'prepared_by = "release-owner"\n'
                'released_at = "2026-08-21T12:00:00Z"\n'
                'authorized_by = "release-owner"',
            )
        )
        release_path.write_text(historical_release, encoding="utf-8")
        vrec_path.write_text(
            vrec_path.read_text(encoding="utf-8").replace(
                'status = "ready"',
                'status = "verified"',
            ),
            encoding="utf-8",
        )
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["payload_sha256"] = "b" * 64
        lock["evaluator"]["archive_sha256"] = "b" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(validator), "--root", str(self.root), "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

        unbound = historical_release
        unbound = "\n".join(
            line
            for line in unbound.splitlines()
            if not line.startswith("evaluator_evidence_")
        ) + "\n"
        release_path.write_text(unbound, encoding="utf-8")
        (self.root / "docs/engineering/delivery/evidence/RLS-001-evaluator.json").unlink()
        completed = subprocess.run(
            [sys.executable, str(validator), "--root", str(self.root), "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, completed.returncode)
        report = json.loads(completed.stdout)
        self.assertIn("E012", {item["code"] for item in report["errors"]})

    def test_installed_validator_rejects_modified_evaluator_evidence(self) -> None:
        self.initialize_candidate()
        code, _, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(0, code, error)
        validator = self.root / "scripts/validate_engineering_artifacts.py"
        completed = subprocess.run(
            [sys.executable, str(validator), "--root", str(self.root), "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

        evidence = self.root / "docs/engineering/product/evidence/VREC-001-evaluator.json"
        value = json.loads(evidence.read_text(encoding="utf-8"))
        value["environment"]["isolated_python"] = not value["environment"]["isolated_python"]
        evidence.write_text(
            json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, str(validator), "--root", str(self.root), "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, completed.returncode)
        report = json.loads(completed.stdout)
        self.assertIn("E012", {item["code"] for item in report["errors"]})

    def test_explicit_domain_and_output_precedence_are_deterministic(self) -> None:
        self.initialize_candidate()
        explicit_output = "docs/engineering/governance/VREC-001.md"
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
            "--domain", "assurance",
            "--output", explicit_output,
        )
        self.assertEqual(0, code, error)
        self.assertIn(explicit_output, output)
        self.assertTrue((self.root / explicit_output).is_file())
        self.assertFalse((self.root / "docs/engineering/assurance/verification-records/VREC-001.md").exists())

        (self.root / explicit_output).unlink()
        (self.root / "docs/engineering/assurance/evidence/VREC-001-evaluator.json").unlink()
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
            "--domain", "requirements",
            "--output", explicit_output,
        )
        self.assertEqual(1, code)
        self.assertIn("reserved", output)
        self.assertEqual(1, output.count("WEX304"), output)  # ECP-CLI-006/-007: one code, the cause class
        self.assertFalse((self.root / explicit_output).exists())

        code, _, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-002",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
            "--domain", "assurance",
        )
        self.assertEqual(0, code, error)
        self.assertTrue((self.root / "docs/engineering/assurance/verification-records/VREC-002.md").is_file())

    def test_cross_domain_verification_defaults_to_repository_aggregate_root(self) -> None:
        self.initialize_candidate(aggregate=True)
        source = self.root / "docs/engineering/product/work-orders/WO-002.md"
        destination = self.root / "docs/engineering/billing/work-orders/WO-002.md"
        destination.parent.mkdir(parents=True)
        self.git("mv", str(source), str(destination))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "place second work order in billing")

        code, _, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-002",
            "--work-order", "WO-001",
            "--work-order", "WO-002",
            "--verification", "VER-001",
            "--verification", "VER-002",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
            "--evidence", "docs/engineering/product/evidence/WO-002-verification.md",
        )
        self.assertEqual(0, code, error)
        aggregate = self.root / "docs/engineering/verification-records/VREC-002.md"
        self.assertTrue(aggregate.is_file())
        self.assertFalse((self.root / "docs/engineering/product/verification-records/VREC-002.md").exists())
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_capture_fails_for_dirty_worktree_without_output(self) -> None:
        self.initialize_candidate()
        (self.root / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertIn("clean Git worktree", output)
        self.assertEqual(1, output.count("WEX302"), output)  # ECP-CLI-006/-007: one code, the cause class
        self.assertFalse((self.root / "docs/engineering/product/verification-records/VREC-001.md").exists())

    def test_capture_names_the_evidence_class_when_the_dashboard_generator_fails(self) -> None:
        # ECP-CLI-007: an evaluator-evidence failure is WEX303, not the state code.
        from se_harness.provenance import EvidenceRefusal

        self.initialize_candidate()
        with mock.patch("se_harness.provenance._generate_snapshot", side_effect=EvidenceRefusal("dashboard generation must pass before recording verification")):
            code, output, error = self.invoke(
                "capture-verification", str(self.root), "--id", "VREC-002",
                "--work-order", "WO-001", "--verification", "VER-001",
                "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
            )
        self.assertEqual(1, code)
        self.assertEqual("", error)
        self.assertIn("WEX303: dashboard generation must pass", output)
        self.assertEqual(1, output.count("WEX303"))

    def test_capture_requires_implemented_work_order(self) -> None:
        self.initialize_candidate()
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        path.write_text(
            path.read_text(encoding="utf-8")
            .replace('status = "implemented"', 'status = "approved"')
            .replace(
                "\n[relations]",
                '\n[assurance]\ncommit_bound_verification = "required"\n'
                'rationale = "This fixture requires accountable candidate verification."\n'
                'decided_by = "owner"\n\n[relations]',
            ),
            encoding="utf-8",
        )
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", str(path))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "approved work only")
        code, output, error = self.invoke(
            "capture-verification", str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertIn("must be implemented", output)
        self.assertEqual(1, output.count("WEX301"), output)  # ECP-CLI-006/-007: one code, the cause class

    def test_capture_and_prepare_mixed_layout_aggregate_scope_deterministically(self) -> None:
        self.initialize_candidate(aggregate=True)
        directory_evidence = "docs/engineering/product/evidence/WO-002/check.md"
        (self.root / directory_evidence).parent.mkdir(parents=True)
        self.git(
            "mv",
            "docs/engineering/product/evidence/WO-002-verification.md",
            directory_evidence,
        )
        self.git(
            "-c",
            "user.name=Harness Test",
            "-c",
            "user.email=harness@example.invalid",
            "commit",
            "-m",
            "organize evidence by work order",
        )
        candidate = self.git("rev-parse", "HEAD")
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-002",
            "--work-order", "WO-002",
            "--work-order", "WO-001",
            "--verification", "VER-002",
            "--verification", "VER-001",
            "--evidence", directory_evidence,
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(0, code, error)
        self.assertIn("ready verification record", output)
        vrec_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"
        vrec = vrec_path.read_text(encoding="utf-8")
        self.assertIn(f'commit = "{candidate}"', vrec)
        self.assertIn('verifies_work_order = ["WO-001", "WO-002"]', vrec)
        self.assertIn('conforms_to = ["VER-001", "VER-002"]', vrec)
        self.assertIn(directory_evidence, vrec)
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-002=verified",
            "--decision", "VREC-002=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)

        evaluator_evidence = self.root / "docs/engineering/product/evidence/VREC-002-evaluator.json"
        self.assertTrue(evaluator_evidence.is_file())
        self.git(
            "-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid",
            "add", str(vrec_path), str(evaluator_evidence),
        )
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "aggregate verification governance")
        governance = self.git("rev-parse", "HEAD")

        code, output, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-002",
            "--work-order", "WO-002",
            "--work-order", "WO-001",
            "--version", "2.0.0",
            "--owner", "release-owner",
            "--tag", "v2.0.0",
        )
        self.assertEqual(0, code, error)
        self.assertIn("ready release record", output)
        release = (self.root / "docs/engineering/product/releases/RLS-002.md").read_text(encoding="utf-8")
        self.assertIn(f'commit = "{candidate}"', release)
        self.assertIn('releases_work = ["WO-001", "WO-002"]', release)
        self.assertEqual(governance, self.git("rev-parse", "HEAD"))
        self.assertEqual("", self.git("tag", "--list"))
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_prepare_release_remains_format_neutral(self) -> None:
        candidate = self.initialize_candidate()
        record_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(record_path, verification_record(candidate))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", str(record_path))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "verification governance")
        code, _, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-001",
            "--work-order", "WO-001",
            "--version", "1.2.3",
            "--owner", "release-owner",
            "--tag", "v1.2.3",
        )
        self.assertEqual(0, code, error)
        release = (self.root / "docs/engineering/product/releases/RLS-002.md").read_text(encoding="utf-8")
        self.assertNotIn("[distribution]", release)
        self.assertNotIn("wheel", release.lower())
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

        release_path = self.root / "docs/engineering/product/releases/RLS-002.md"
        release_path.write_text(
            release.replace(
                "[relations]",
                '[distribution]\nrepository_policy = "opaque-to-core"\n\n[relations]',
            ),
            encoding="utf-8",
        )
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_aggregate_capture_rejects_duplicate_and_incomplete_scope(self) -> None:
        self.initialize_candidate(aggregate=True)
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-002",
            "--work-order", "WO-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertIn("duplicate", output)
        self.assertEqual(1, output.count("WEX304"), output)  # ECP-CLI-006/-007: one code, the cause class

        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-002",
            "--work-order", "WO-001",
            "--work-order", "WO-002",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertIn("missing VER-002", output)
        self.assertEqual(1, output.count("WEX304"), output)  # ECP-CLI-006/-007: one code, the cause class
        self.assertFalse((self.root / "docs/engineering/product/verification-records/VREC-002.md").exists())

    def test_prepare_release_combines_multiple_records_at_one_commit(self) -> None:
        candidate = self.initialize_candidate(aggregate=True)
        first = verification_record(candidate)
        second = (
            verification_record(candidate)
            .replace("VREC-001", "VREC-002")
            .replace("WO-001", "WO-002")
            .replace("VER-001", "VER-002")
        )
        first_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        second_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"
        write(first_path, first)
        write(second_path, second)
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", str(first_path), str(second_path))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "verification governance")

        code, _, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-002",
            "--verification-record", "VREC-001",
            "--work-order", "WO-002",
            "--work-order", "WO-001",
            "--version", "2.0.0",
            "--owner", "release-owner",
        )
        self.assertEqual(0, code, error)
        release = (self.root / "docs/engineering/product/releases/RLS-002.md").read_text(encoding="utf-8")
        self.assertIn('includes_verification = ["VREC-001", "VREC-002"]', release)
        self.assertIn('releases_work = ["WO-001", "WO-002"]', release)
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_prepare_release_rejects_verification_records_at_different_commits(self) -> None:
        candidate = self.initialize_candidate(aggregate=True)
        first_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        second_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"
        write(first_path, verification_record(candidate))
        second = (
            verification_record("b" * 40)
            .replace("VREC-001", "VREC-002")
            .replace("WO-001", "WO-002")
            .replace("VER-001", "VER-002")
        )
        write(second_path, second)
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", str(first_path), str(second_path))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "mixed verification governance")

        code, output, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-001",
            "--verification-record", "VREC-002",
            "--work-order", "WO-001",
            "--work-order", "WO-002",
            "--version", "2.0.0",
            "--owner", "release-owner",
        )
        self.assertEqual(1, code)
        self.assertIn("one candidate commit", output)
        self.assertEqual(1, output.count("WEX404"), output)  # ECP-CLI-006/-007: one code, the cause class
        self.assertFalse((self.root / "docs/engineering/product/releases/RLS-002.md").exists())

    def test_prepare_release_rejects_superseded_verification_record(self) -> None:
        candidate = self.initialize_candidate(aggregate=True)
        source_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        successor_path = self.root / "docs/engineering/product/verification-records/VREC-002.md"
        write(source_path, superseded_record(verification_record(candidate), "VREC-002"))
        write(successor_path, aggregate_verification_record(candidate))
        self.git(
            "-c", "user.name=Harness Test",
            "-c", "user.email=harness@example.invalid",
            "add", str(source_path), str(successor_path),
        )
        self.git(
            "-c", "user.name=Harness Test",
            "-c", "user.email=harness@example.invalid",
            "commit", "-m", "verification supersession governance",
        )

        code, output, error = self.invoke(
            "prepare-release",
            str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-001",
            "--work-order", "WO-001",
            "--version", "2.0.0",
            "--owner", "release-owner",
        )
        self.assertEqual(1, code)
        self.assertIn("must be verified", output)
        self.assertEqual(1, output.count("WEX401"), output)  # ECP-CLI-006/-007: one code, the cause class
        self.assertFalse((self.root / "docs/engineering/product/releases/RLS-002.md").exists())

    def test_prepare_release_rejects_ready_verification_record(self) -> None:
        candidate = self.initialize_candidate()
        record_path = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(record_path, verification_record(candidate, status="ready"))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "add", str(record_path))
        self.git("-c", "user.name=Harness Test", "-c", "user.email=harness@example.invalid", "commit", "-m", "ready verification candidate")
        code, output, error = self.invoke(
            "prepare-release", str(self.root),
            "--id", "RLS-002",
            "--release-contract", "REL-001",
            "--verification-record", "VREC-001",
            "--work-order", "WO-001",
            "--version", "2.0.0",
            "--owner", "release-owner",
        )
        self.assertEqual(1, code)
        self.assertIn("must be verified", output)
        self.assertEqual(1, output.count("WEX401"), output)  # ECP-CLI-006/-007: one code, the cause class

    def test_capture_refuses_existing_output(self) -> None:
        self.initialize_candidate()
        output = self.root / "docs/engineering/product/verification-records/VREC-001.md"
        write(output, "repository owned")
        code, stdout, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertIn("already exists", stdout)
        self.assertEqual(1, stdout.count("WEX304"), stdout)  # ECP-CLI-006/-007: one code, the cause class
        self.assertEqual("repository owned\n", output.read_text(encoding="utf-8"))

    def test_capture_fails_when_repository_has_no_head(self) -> None:
        standard_repository(self.root, "No Head")
        create_base_chain(self.root, operating_contract_status="draft")
        self.git("init", "-b", "main")
        info_exclude = self.root / ".git/info/exclude"
        info_exclude.write_text("*\n", encoding="utf-8")
        code, output, error = self.invoke(
            "capture-verification",
            str(self.root),
            "--id", "VREC-001",
            "--work-order", "WO-001",
            "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-001-verification.md",
        )
        self.assertEqual(1, code)
        self.assertTrue("HEAD" in output or "revision" in output.lower(), output)
        self.assertEqual(1, output.count("WEX302"), output)  # ECP-CLI-006/-007: one code, the cause class


if __name__ == "__main__":
    unittest.main()
