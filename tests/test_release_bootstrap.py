from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from repository_tools import release_bootstrap as BOOTSTRAP


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load test module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


CANDIDATE_VALIDATOR = load_module(
    "release_bootstrap_candidate_validator",
    REPOSITORY_ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
)
PUBLICATION = load_module(
    "release_bootstrap_publication",
    REPOSITORY_ROOT / ".github/scripts/publish_dashboard.py",
)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class ReleaseBootstrapBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Harness Test")
        self.git("config", "user.email", "harness-test@example.invalid")
        self.write("source.txt", b"candidate\n")
        self.git("add", ".")
        self.git("commit", "-m", "candidate")
        self.candidate = self.git("rev-parse", "HEAD")

        self.write(".engineering-harness.toml", b'[harness]\ntool_version = "0.5.0"\n')
        self.lock_bytes = (
            json.dumps(
                {
                    "schema": 2,
                    "tool_version": "0.5.0",
                    "hash_algorithm": "sha256",
                    "hash_mode": "utf8-text-lf-v1",
                    "files": {},
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        self.write(".engineering-harness.lock", self.lock_bytes)

        self.evaluator_root = Path(self.temporary.name) / "released-evaluator"
        self.python = self.evaluator_root / "Scripts" / "python.exe"
        self.entry_point = self.evaluator_root / "Scripts" / "harnessctl.exe"
        self.module = self.evaluator_root / "Lib" / "site-packages" / "se_harness" / "runtime_identity.py"
        self.distribution = self.evaluator_root / "Lib" / "site-packages"
        self.templates = self.evaluator_root / "share" / "se-harness" / "templates" / "repository" / "standard"
        for path in (self.python, self.entry_point, self.module, self.templates / "ENGINEERING_HARNESS.md.tpl"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"test\n")
        self.wheel = Path(self.temporary.name) / "se_harness-0.5.0-py3-none-any.whl"
        with zipfile.ZipFile(self.wheel, "w") as archive:
            archive.writestr("se_harness/runtime_identity.py", b"test\n")
            archive.writestr(
                "se_harness-0.5.0.data/data/share/se-harness/templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
                b"test\n",
            )
        self.wheel_sha = sha256(self.wheel.read_bytes())

        self.contract_path = Path("docs/engineering/release/release/REL-TST-001.md")
        self.record_path = Path("docs/engineering/release/releases/RLS-TST-001.md")
        self.evidence_path = self.root / "docs/engineering/release/evidence/RLS-TST-001-evaluator.json"
        self.evidence_path.parent.mkdir(parents=True, exist_ok=True)
        self.write(self.contract_path, self.contract().encode("utf-8"))
        self.write(
            "docs/engineering/release/verification-records/VREC-TST-001.md",
            self.verification_record().encode("utf-8"),
        )
        self.write(self.record_path, self.release_record().encode("utf-8"))
        self.original_record = (self.root / self.record_path).read_bytes()
        self.identity = {
            "schema": "se-harness-runtime-identity-v2",
            "passed": True,
            "role": "released-evaluator",
            "python_executable": str(self.python.resolve()),
            "harness_version": "0.5.0",
            "module_origin": str(self.module.resolve()),
            "distribution_origin": str(self.distribution.resolve()),
            "template_origin": str(self.templates.resolve()),
            "entry_point_origin": str(self.entry_point.resolve()),
            "expected_root": str(self.evaluator_root.resolve()),
            "checkout_root": str(self.root.resolve()),
            "candidate_commit": None,
            "isolated_python": True,
            "user_site_enabled": False,
            "pythonpath_present": False,
            "diagnostics": [],
        }
        self.identity_patch = mock.patch.object(
            BOOTSTRAP, "_run_released_evaluator", return_value=self.identity
        )
        self.payload_patch = mock.patch.object(
            BOOTSTRAP,
            "_installed_payload",
            side_effect=lambda _identity, _root: BOOTSTRAP._wheel_payload(self.wheel, "0.5.0"),
        )
        self.identity_patch.start()
        self.payload_patch.start()

    def tearDown(self) -> None:
        self.payload_patch.stop()
        self.identity_patch.stop()
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return completed.stdout.strip()

    def write(self, relative: str | Path, content: bytes) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def contract(self) -> str:
        return f'''+++
id = "REL-TST-001"
type = "release_contract"
title = "Bootstrap release"
status = "approved"
owners = ["release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-TST-001"
version = "1.2.3"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "{sha256(self.lock_bytes)}"
evaluator_version = "0.5.0"
evaluator_archive_name = "{self.wheel.name}"
evaluator_archive_sha256 = "{self.wheel_sha}"

[relations]
gates = ["WO-TST-001"]
+++
'''

    def verification_record(self) -> str:
        return f'''+++
id = "VREC-TST-001"
type = "verification_record"
title = "Verified candidate"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
commit = "{self.candidate}"
git_object_format = "sha1"

[relations]
verifies_work_order = ["WO-TST-001"]
conforms_to = ["VER-TST-001"]
+++
'''

    def release_record(self) -> str:
        return f'''+++
id = "RLS-TST-001"
type = "release_record"
title = "Predecessor-prepared release"
status = "ready"
owners = ["release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
version = "1.2.3"
commit = "{self.candidate}"
git_object_format = "sha1"
released_at = "2026-08-21T12:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"

[relations]
satisfies = ["REL-TST-001"]
includes_verification = ["VREC-TST-001"]
releases_work = ["WO-TST-001"]
+++

# Candidate body

Body bytes are predecessor-owned.
'''

    def arguments(self) -> tuple[Path, Path, Path, Path, Path, Path]:
        return (
            self.root,
            self.record_path,
            self.contract_path,
            self.python,
            self.entry_point,
            self.wheel,
        )

    def test_plan_is_read_only_and_apply_is_atomic_and_idempotent(self) -> None:
        plan = BOOTSTRAP.plan_bootstrap_binding(*self.arguments())
        self.assertTrue(plan.changed)
        self.assertFalse(plan.applied)
        self.assertFalse(self.evidence_path.exists())
        self.assertEqual(self.original_record, (self.root / self.record_path).read_bytes())

        applied = BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertTrue(applied.changed)
        self.assertTrue(applied.applied)
        evidence = self.evidence_path.read_bytes()
        self.assertEqual(applied.evaluator_evidence_sha256, sha256(evidence))
        updated = (self.root / self.record_path).read_text(encoding="utf-8")
        self.assertIn('preparation_schema = "se-harness-predecessor-bootstrap-v1"', updated)
        self.assertIn(f'evaluator_evidence_sha256 = "{sha256(evidence)}"', updated)
        self.assertEqual(self.release_record().split("+++", 2)[2], updated.split("+++", 2)[2])

        exact_record = (self.root / self.record_path).read_bytes()
        exact_evidence = self.evidence_path.read_bytes()
        replay = BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertFalse(replay.changed)
        self.assertEqual(exact_record, (self.root / self.record_path).read_bytes())
        self.assertEqual(exact_evidence, self.evidence_path.read_bytes())

    def test_canonical_lock_identity_accepts_platform_line_endings(self) -> None:
        crlf = self.lock_bytes.replace(b"\n", b"\r\n")
        (self.root / ".engineering-harness.lock").write_bytes(crlf)
        plan = BOOTSTRAP.plan_bootstrap_binding(*self.arguments())
        self.assertEqual(sha256(self.lock_bytes), plan.lock_sha256)
        self.assertTrue(plan.changed)
        self.assertFalse(plan.applied)
        self.assertFalse(self.evidence_path.exists())
        self.assertEqual(crlf, (self.root / ".engineering-harness.lock").read_bytes())

    def test_wheel_lock_and_relation_drift_fail_without_writes(self) -> None:
        cases = (
            (self.wheel, b"tampered wheel\n", "wheel digest"),
            (self.root / ".engineering-harness.lock", b"{}\n", "lock digest"),
            (
                self.root / self.record_path,
                self.release_record().replace('releases_work = ["WO-TST-001"]', 'releases_work = ["WO-OTHER-001"]').encode("utf-8"),
                "work set",
            ),
        )
        for path, changed, message in cases:
            with self.subTest(message=message):
                originals = {
                    self.wheel: self.wheel.read_bytes(),
                    self.root / ".engineering-harness.lock": (self.root / ".engineering-harness.lock").read_bytes(),
                    self.root / self.record_path: (self.root / self.record_path).read_bytes(),
                }
                path.write_bytes(changed)
                observed_record = (self.root / self.record_path).read_bytes()
                with self.assertRaisesRegex(BOOTSTRAP.ReleaseBootstrapError, message):
                    BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
                self.assertEqual(observed_record, (self.root / self.record_path).read_bytes())
                self.assertFalse(self.evidence_path.exists())
                for target, original in originals.items():
                    target.write_bytes(original)

    def test_record_replace_failure_rolls_back_exclusively_created_evidence(self) -> None:
        with mock.patch.object(
            BOOTSTRAP, "_atomic_replace", side_effect=BOOTSTRAP.ReleaseBootstrapError("injected replace")
        ):
            with self.assertRaisesRegex(BOOTSTRAP.ReleaseBootstrapError, "injected replace"):
                BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertFalse(self.evidence_path.exists())
        self.assertEqual(self.original_record, (self.root / self.record_path).read_bytes())

    def test_existing_nonidentical_evidence_is_never_overwritten(self) -> None:
        self.evidence_path.write_bytes(b"conflict\n")
        before = self.evidence_path.read_bytes()
        with self.assertRaisesRegex(BOOTSTRAP.ReleaseBootstrapError, "differs from canonical"):
            BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertEqual(before, self.evidence_path.read_bytes())
        self.assertEqual(self.original_record, (self.root / self.record_path).read_bytes())

    def test_contract_parser_is_closed_typed_and_order_independent(self) -> None:
        metadata, *_unused = BOOTSTRAP._read_front_matter(
            self.root / self.contract_path, "release contract"
        )
        expected = BOOTSTRAP.parse_bootstrap_contract(metadata)
        reordered = copy.deepcopy(metadata)
        reordered["bootstrap"] = dict(reversed(list(reordered["bootstrap"].items())))
        self.assertEqual(expected, BOOTSTRAP.parse_bootstrap_contract(reordered))

        cases = (
            (lambda value: value.__setitem__("status", "draft"), "approved"),
            (lambda value: value.__setitem__("status", "rejected"), "approved"),
            (lambda value: value.__setitem__("type", "requirement"), "approved"),
            (lambda value: value["bootstrap"].pop("from_lock_sha256"), "field set"),
            (lambda value: value["bootstrap"].__setitem__("unexpected", True), "field set"),
            (lambda value: value["bootstrap"].__setitem__("schema", "other"), "schema"),
            (lambda value: value["bootstrap"].__setitem__("from_lock_schema", True), "integer 2"),
            (
                lambda value: value["bootstrap"].__setitem__(
                    "evaluator_archive_name", "../se_harness-0.5.0-py3-none-any.whl"
                ),
                "archive_name",
            ),
            (
                lambda value: value["bootstrap"].__setitem__(
                    "evaluator_archive_sha256", "A" * 64
                ),
                "lowercase",
            ),
        )
        for mutate, message in cases:
            with self.subTest(message=message):
                changed = copy.deepcopy(metadata)
                mutate(changed)
                with self.assertRaisesRegex(BOOTSTRAP.ReleaseBootstrapError, message):
                    BOOTSTRAP.parse_bootstrap_contract(changed)

    def test_second_approved_bootstrap_contract_fails_before_writes(self) -> None:
        second = self.contract().replace("REL-TST-001", "REL-TST-002").replace(
            "RLS-TST-001", "RLS-TST-002"
        )
        self.write(
            "docs/engineering/release/release/REL-TST-002.md", second.encode("utf-8")
        )
        with self.assertRaisesRegex(
            BOOTSTRAP.ReleaseBootstrapError, "exactly one approved predecessor bootstrap"
        ):
            BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertFalse(self.evidence_path.exists())
        self.assertEqual(self.original_record, (self.root / self.record_path).read_bytes())

    def test_external_identity_matrix_is_checked_with_pythonpath_removed(self) -> None:
        def invoke(identity: dict) -> tuple[dict, list[dict]]:
            calls: list[dict] = []

            def run(command, **kwargs):
                calls.append({"command": command, **kwargs})
                if "identity" in command:
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout=json.dumps(identity).encode("utf-8"),
                        stderr=b"",
                    )
                return subprocess.CompletedProcess(command, 0, stdout=b"{}\n", stderr=b"")

            with mock.patch.object(BOOTSTRAP.subprocess, "run", side_effect=run):
                result = BOOTSTRAP._run_released_evaluator(
                    self.root,
                    self.python,
                    self.entry_point,
                    BOOTSTRAP.parse_bootstrap_contract(
                        BOOTSTRAP._read_front_matter(
                            self.root / self.contract_path, "release contract"
                        )[0]
                    ),
                )
            return result, calls

        self.identity_patch.stop()
        try:
            observed, calls = invoke(self.identity)
            self.assertEqual(self.identity, observed)
            self.assertEqual(2, len(calls))
            self.assertTrue(all("PYTHONPATH" not in call["env"] for call in calls))
            self.assertTrue(all(call["cwd"] == self.root for call in calls))

            mutations = (
                ("passed", False),
                ("isolated_python", False),
                ("user_site_enabled", True),
                ("pythonpath_present", True),
                ("candidate_commit", "a" * 40),
                ("harness_version", "0.6.0"),
            )
            for field, value in mutations:
                with self.subTest(field=field):
                    changed = {**self.identity, field: value}
                    with self.assertRaisesRegex(
                        BOOTSTRAP.ReleaseBootstrapError, "identity proof is not acceptable"
                    ):
                        invoke(changed)
        finally:
            self.identity_patch.start()

    def test_record_change_after_plan_rolls_back_exclusive_evidence(self) -> None:
        prepared = BOOTSTRAP._prepare(*self.arguments())
        changed_record = prepared.record_original + b"changed\n"

        def changed_after_plan(*_arguments: Path):
            prepared.record_path.write_bytes(changed_record)
            return prepared

        with mock.patch.object(BOOTSTRAP, "_prepare", side_effect=changed_after_plan):
            with self.assertRaisesRegex(
                BOOTSTRAP.ReleaseBootstrapError, "changed after bootstrap planning"
            ):
                BOOTSTRAP.apply_bootstrap_binding(*self.arguments())
        self.assertFalse(self.evidence_path.exists())
        self.assertEqual(changed_record, prepared.record_path.read_bytes())


class CandidateBootstrapValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / ".engineering-harness.toml").write_text(
            '[harness]\ntool_version = "0.5.0"\n', encoding="utf-8", newline="\n"
        )
        self.lock_bytes = (
            json.dumps(
                {
                    "schema": 2,
                    "tool_version": "0.5.0",
                    "hash_algorithm": "sha256",
                    "hash_mode": "utf8-text-lf-v1",
                    "files": {},
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        (self.root / ".engineering-harness.lock").write_bytes(self.lock_bytes)
        self.evidence_relative = "docs/engineering/release/evidence/RLS-TST-009-evaluator.json"
        evaluator = {
            "version": "0.5.0",
            "payload_manifest": "se-harness-installed-payload-v1",
            "payload_sha256": "c" * 64,
            "archive_name": "se_harness-0.5.0-py3-none-any.whl",
            "archive_sha256": "d" * 64,
        }
        evidence = {
            "schema": "se-harness-evaluator-evidence-v1",
            "role": "released-evaluator",
            "evaluator": evaluator,
            "origins": {
                "python_executable": "<evaluator-root>/Scripts/python.exe",
                "module": "<evaluator-root>/Lib/site-packages/se_harness/runtime_identity.py",
                "distribution": "<evaluator-root>/Lib/site-packages",
                "templates": "<evaluator-root>/share/se-harness/templates/repository/standard",
                "entry_point": "<evaluator-root>/Scripts/harnessctl.exe",
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
        self.evidence_bytes = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
        ).encode("utf-8")
        evidence_path = self.root / self.evidence_relative
        evidence_path.parent.mkdir(parents=True)
        evidence_path.write_bytes(self.evidence_bytes)
        self.contract = CANDIDATE_VALIDATOR.Artifact(
            path=self.root / "docs/engineering/release/release/REL-TST-009.md",
            metadata={
                "id": "REL-TST-009",
                "type": "release_contract",
                "status": "approved",
                "relations": {"gates": ["WO-TST-001"]},
                "bootstrap": {
                    "schema": "se-harness-release-bootstrap-v1",
                    "release_record": "RLS-TST-009",
                    "version": "1.2.3",
                    "from_lock_schema": 2,
                    "from_lock_tool_version": "0.5.0",
                    "from_lock_sha256": sha256(self.lock_bytes),
                    "evaluator_version": "0.5.0",
                    "evaluator_archive_name": "se_harness-0.5.0-py3-none-any.whl",
                    "evaluator_archive_sha256": "d" * 64,
                },
            },
            body="",
        )
        self.release = CANDIDATE_VALIDATOR.Artifact(
            path=self.root / "docs/engineering/release/releases/RLS-TST-009.md",
            metadata={
                "id": "RLS-TST-009",
                "type": "release_record",
                "status": "ready",
                "owners": ["release-owner"],
                "version": "1.2.3",
                "commit": "a" * 40,
                "git_object_format": "sha1",
                "released_at": "2026-08-21T12:00:00Z",
                "authorized_by": "release-owner",
                "tag": "v1.2.3",
                "preparation_schema": "se-harness-predecessor-bootstrap-v1",
                "evaluator_evidence_path": self.evidence_relative,
                "evaluator_evidence_sha256": sha256(self.evidence_bytes),
                "relations": {
                    "satisfies": ["REL-TST-009"],
                    "includes_verification": ["VREC-TST-009"],
                    "releases_work": ["WO-TST-001"],
                },
            },
            body="",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def diagnostics(self) -> list:
        return CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.contract, self.release], self.root
        )

    def test_exact_bootstrap_accepts_schema_two_without_missing_evidence_bypass(self) -> None:
        self.assertEqual([], self.diagnostics())
        self.assertNotIn(
            "RLS-TST-009", CANDIDATE_VALIDATOR.LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE
        )

    def test_bootstrap_lifecycle_matrix_accepts_only_closed_matching_states(self) -> None:
        for release_status, contract_status, accepted in (
            ("ready", "approved", True),
            ("ready", "rejected", False),
            ("rejected", "approved", False),
            ("rejected", "rejected", True),
        ):
            with self.subTest(release=release_status, contract=contract_status):
                self.release.metadata["status"] = release_status
                self.contract.metadata["status"] = contract_status
                if release_status == "rejected":
                    self.release.metadata.update(
                        {
                            "rejected_at": "2026-08-21T12:30:00Z",
                            "rejected_by": "release-owner",
                            "rejection_reason": "retained checkout qualification failure",
                        }
                    )
                else:
                    for field in ("rejected_at", "rejected_by", "rejection_reason"):
                        self.release.metadata.pop(field, None)
                findings = self.diagnostics()
                if accepted:
                    self.assertEqual([], findings)
                else:
                    self.assertTrue(
                        any("requires one exact" in item.message for item in findings),
                        findings,
                    )

    def test_rejected_bootstrap_history_requires_its_exact_rejected_contract(self) -> None:
        self.release.metadata.update(
            {
                "status": "rejected",
                "rejected_at": "2026-08-21T12:30:00Z",
                "rejected_by": "release-owner",
                "rejection_reason": "retained checkout qualification failure",
            }
        )
        self.contract.metadata["status"] = "rejected"
        self.assertEqual([], self.diagnostics())

        findings = CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.release], self.root
        )
        self.assertTrue(any("exact rejected release contract" in item.message for item in findings))

        self.contract.metadata["bootstrap"]["release_record"] = "RLS-TST-010"
        self.assertTrue(any(item.code == "E012" for item in self.diagnostics()))

    def test_lock_archive_and_record_drift_fail_closed(self) -> None:
        mutations = (
            lambda: (self.root / ".engineering-harness.lock").write_bytes(b"{}\n"),
            lambda: self.release.metadata.__setitem__("id", "RLS-TST-010"),
            lambda: self.release.metadata.__setitem__(
                "evaluator_evidence_sha256", "e" * 64
            ),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                original_lock = (self.root / ".engineering-harness.lock").read_bytes()
                original_id = self.release.metadata["id"]
                original_digest = self.release.metadata["evaluator_evidence_sha256"]
                mutate()
                self.assertTrue(any(item.code == "E012" for item in self.diagnostics()))
                (self.root / ".engineering-harness.lock").write_bytes(original_lock)
                self.release.metadata["id"] = original_id
                self.release.metadata["evaluator_evidence_sha256"] = original_digest

    def test_crlf_evidence_is_never_normalized_for_digest_or_canonical_validation(self) -> None:
        evidence_path = self.root / self.evidence_relative
        crlf = self.evidence_bytes.replace(b"\n", b"\r\n")
        evidence_path.write_bytes(crlf)
        findings = self.diagnostics()
        self.assertTrue(
            any("digest does not match" in item.message for item in findings),
            findings,
        )

        self.release.metadata["evaluator_evidence_sha256"] = sha256(crlf)
        findings = self.diagnostics()
        self.assertTrue(
            any("not canonical" in item.message for item in findings),
            findings,
        )

    def test_nonisolated_evidence_and_a_second_bootstrap_fail_closed(self) -> None:
        evidence_path = self.root / self.evidence_relative
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence["environment"]["isolated_python"] = False
        changed = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")
        evidence_path.write_bytes(changed)
        self.release.metadata["evaluator_evidence_sha256"] = sha256(changed)
        self.assertTrue(any(item.code == "E012" for item in self.diagnostics()))

        evidence_path.write_bytes(self.evidence_bytes)
        self.release.metadata["evaluator_evidence_sha256"] = sha256(self.evidence_bytes)
        second = CANDIDATE_VALIDATOR.Artifact(
            path=self.root / "docs/engineering/release/release/REL-TST-010.md",
            metadata={
                **self.contract.metadata,
                "id": "REL-TST-010",
                "bootstrap": {
                    **self.contract.metadata["bootstrap"],
                    "release_record": "RLS-TST-010",
                },
            },
            body="",
        )
        findings = CANDIDATE_VALIDATOR.validate_type_specific_metadata(
            [self.contract, second, self.release], self.root
        )
        self.assertTrue(
            any("at most one approved predecessor bootstrap" in item.message for item in findings)
        )

    def test_schema_two_ordinary_ready_record_cannot_reuse_bootstrap(self) -> None:
        marker = self.release.metadata.pop("preparation_schema")
        try:
            self.assertTrue(any(item.code == "E012" for item in self.diagnostics()))
        finally:
            self.release.metadata["preparation_schema"] = marker

    def test_released_bootstrap_remains_historical_after_schema_three_rotation(self) -> None:
        self.release.metadata["status"] = "released"
        (self.root / ".engineering-harness.lock").write_text(
            json.dumps(
                {
                    "schema": 3,
                    "tool_version": "0.6.0",
                    "hash_algorithm": "sha256",
                    "hash_mode": "utf8-text-lf-v1",
                    "files": {},
                    "evaluator": {
                        "version": "0.6.0",
                        "payload_manifest": "se-harness-installed-payload-v1",
                        "payload_sha256": "e" * 64,
                        "archive_name": "se_harness-0.6.0-py3-none-any.whl",
                        "archive_sha256": "f" * 64,
                    },
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        self.assertEqual([], self.diagnostics())

    def test_bootstrap_lock_identity_is_line_ending_invariant(self) -> None:
        lock_path = self.root / ".engineering-harness.lock"
        lock_path.write_bytes(self.lock_bytes.replace(b"\n", b"\r\n"))
        self.assertEqual([], self.diagnostics())

    def test_rejected_history_does_not_claim_an_active_release_version(self) -> None:
        cases = (
            ("rejected", "ready", False),
            ("rejected", "released", False),
            ("rejected", "rejected", False),
            ("ready", "ready", True),
            ("ready", "released", True),
            ("released", "released", True),
        )
        for first_status, second_status, expected_duplicate in cases:
            with self.subTest(first=first_status, second=second_status):
                records = []
                for index, status in enumerate((first_status, second_status), start=10):
                    record = copy.deepcopy(self.release)
                    record.path = self.root / f"docs/engineering/release/releases/RLS-TST-{index:03}.md"
                    record.metadata["id"] = f"RLS-TST-{index:03}"
                    record.metadata["status"] = status
                    if status == "rejected":
                        record.metadata.update(
                            {
                                "rejected_at": "2026-08-21T12:30:00Z",
                                "rejected_by": "release-owner",
                                "rejection_reason": "retained failure",
                            }
                        )
                    records.append(record)
                findings = CANDIDATE_VALIDATOR.validate_revision_consistency(records, self.root)
                duplicate = any("duplicate release record version" in item.message for item in findings)
                self.assertEqual(expected_duplicate, duplicate)


class PublicationBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Harness Test")
        self.git("config", "user.email", "harness-test@example.invalid")
        self.write("README.md", "candidate\n")
        self.commit("candidate")
        self.candidate = self.git("rev-parse", "HEAD")
        self.git("tag", "-a", "v1.2.3", "-m", "release 1.2.3")
        self.write(".engineering-harness.toml", '[harness]\ntool_version = "0.5.0"\n')
        self.lock_bytes = (
            json.dumps(
                {
                    "schema": 2,
                    "tool_version": "0.5.0",
                    "hash_algorithm": "sha256",
                    "hash_mode": "utf8-text-lf-v1",
                    "files": {},
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        (self.root / ".engineering-harness.lock").write_bytes(self.lock_bytes)
        evaluator = {
            "version": "0.5.0",
            "payload_manifest": "se-harness-installed-payload-v1",
            "payload_sha256": "c" * 64,
            "archive_name": "se_harness-0.5.0-py3-none-any.whl",
            "archive_sha256": "d" * 64,
        }
        evidence = {
            "schema": "se-harness-evaluator-evidence-v1",
            "role": "released-evaluator",
            "evaluator": evaluator,
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
        self.evidence_path = "docs/engineering/release/evidence/RLS-TST-009-evaluator.json"
        self.evidence_text = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
        )
        self.write(self.evidence_path, self.evidence_text)
        self.contract_path = "docs/engineering/release/release/REL-TST-009.md"
        self.write(self.contract_path, self.contract())
        self.record_path = "docs/engineering/release/releases/RLS-TST-009.md"
        self.write(self.record_path, self.release_record())
        self.commit("integrate bootstrap release")
        self.governance = self.git("rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return completed.stdout.strip()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def commit(self, message: str) -> None:
        self.git("add", ".")
        self.git("commit", "-m", message)

    def contract(self) -> str:
        return f'''+++
id = "REL-TST-009"
type = "release_contract"
title = "Bootstrap release"
status = "approved"
owners = ["release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-TST-009"
version = "1.2.3"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "{sha256(self.lock_bytes)}"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "{'d' * 64}"

[relations]
gates = ["WO-TST-001"]
+++
'''

    def release_record(self) -> str:
        return f'''+++
id = "RLS-TST-009"
type = "release_record"
title = "Released bootstrap"
status = "released"
owners = ["release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
version = "1.2.3"
commit = "{self.candidate}"
git_object_format = "sha1"
released_at = "2026-08-21T12:00:00Z"
authorized_by = "release-owner"
tag = "v1.2.3"
preparation_schema = "se-harness-predecessor-bootstrap-v1"
evaluator_evidence_path = "{self.evidence_path}"
evaluator_evidence_sha256 = "{sha256(self.evidence_text.encode('utf-8'))}"

[relations]
satisfies = ["REL-TST-009"]
includes_verification = ["VREC-TST-009"]
releases_work = ["WO-TST-001"]
+++
'''

    def test_release_replay_and_evaluator_resolution_use_exact_bootstrap_tuple(self) -> None:
        provenance = PUBLICATION.resolve_release(
            self.root,
            "v1.2.3",
            release_record="RLS-TST-009",
            default_ref="refs/heads/main",
        )
        self.assertEqual(self.governance, provenance.governance_commit)
        descriptor = PUBLICATION.read_evaluator(self.root, release_record="RLS-TST-009")
        self.assertEqual("0.5.0", descriptor.version)
        self.assertEqual("d" * 64, descriptor.sha256)
        self.assertEqual("c" * 64, descriptor.payload_sha256)

    def test_contract_archive_drift_and_unbound_schema_two_resolution_fail(self) -> None:
        contract = self.contract().replace(
            f'evaluator_archive_sha256 = "{"d" * 64}"',
            f'evaluator_archive_sha256 = "{"e" * 64}"',
        )
        self.write(self.contract_path, contract)
        self.commit("tamper bootstrap contract")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "differs from the bootstrap contract"):
            PUBLICATION.read_evaluator(self.root, release_record="RLS-TST-009")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "schema-3"):
            PUBLICATION.read_evaluator(self.root)

    def test_nonisolated_evidence_is_rejected(self) -> None:
        evidence = json.loads(self.evidence_text)
        evidence["environment"]["isolated_python"] = False
        self.evidence_text = (
            json.dumps(evidence, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            + "\n"
        )
        self.write(self.evidence_path, self.evidence_text)
        self.write(self.record_path, self.release_record())
        self.commit("tamper evaluator isolation")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "environment proof"):
            PUBLICATION.read_evaluator(self.root, release_record="RLS-TST-009")

    def test_second_approved_bootstrap_contract_is_rejected(self) -> None:
        second = self.contract().replace("REL-TST-009", "REL-TST-010").replace(
            "RLS-TST-009", "RLS-TST-010"
        )
        self.write("docs/engineering/release/release/REL-TST-010.md", second)
        self.commit("add ambiguous predecessor bootstrap")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "ambiguous"):
            PUBLICATION.read_evaluator(self.root, release_record="RLS-TST-009")

    def test_rejected_bootstrap_contract_has_no_publication_authority(self) -> None:
        self.write(
            self.contract_path,
            self.contract().replace('status = "approved"', 'status = "rejected"'),
        )
        self.commit("reject bootstrap contract")
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "no exact approved"):
            PUBLICATION.read_evaluator(self.root, release_record="RLS-TST-009")

    def test_publication_lock_canonicalization_is_line_ending_invariant(self) -> None:
        lf = b'{"schema":2}\n'
        crlf = b'{"schema":2}\r\n'
        self.assertEqual(
            PUBLICATION._canonical_utf8_text_lf(lf, label="lock"),
            PUBLICATION._canonical_utf8_text_lf(crlf, label="lock"),
        )
        with self.assertRaisesRegex(PUBLICATION.PublicationError, "invalid UTF-8"):
            PUBLICATION._canonical_utf8_text_lf(b"\xff", label="lock")


if __name__ == "__main__":
    unittest.main()
