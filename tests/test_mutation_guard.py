from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness import __version__
from se_harness.agent_contract import validate_contract
from se_harness.artifact_layout import create_artifact, scaffold_domain
from se_harness.cli import main
from se_harness.evaluator_evidence import (
    EvaluatorEvidenceError,
    build_evaluator_evidence,
    parse_evaluator_evidence,
)
from se_harness.evaluator_identity import InstalledEvaluatorIdentity, PAYLOAD_MANIFEST
from se_harness.effect_broker import apply_change_bundle
from se_harness.hash_bound import LOCK_RELATIVE, MATCH_DECLARED, MATCH_LEGACY_NEWLINE
from se_harness.installer import HarnessError, apply_changes, plan_install
from se_harness.integrity import canonical_sha256, raw_sha256
from se_harness.mutation_guard import (
    PUBLIC_MUTATION_OPERATIONS,
    require_mutation_authority,
)
from se_harness.provenance import capture_verification, prepare_release
from se_harness.renumber import apply_renumber_plan
from se_harness.runtime_identity import IdentityDiagnostic, RuntimeIdentity
from se_harness.workflow import apply_transition


class MutationGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _snapshot(root: Path) -> tuple[tuple[str, str, bytes], ...]:
        observed: list[tuple[str, str, bytes]] = []
        if not root.exists():
            return ()
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                observed.append((relative, "link", str(path.readlink()).encode("utf-8")))
            elif path.is_dir():
                observed.append((relative, "directory", b""))
            elif path.is_file():
                observed.append((relative, "file", path.read_bytes()))
        return tuple(observed)

    @staticmethod
    def _invoke(*arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def _write_identity_root(self, *, schema: int = 3, config_version: str | None = None) -> Path:
        root = self.base / f"identity-{schema}-{len(list(self.base.iterdir()))}"
        root.mkdir()
        selected = config_version or __version__
        (root / ".engineering-harness.toml").write_text(
            f'[harness]\ntool_version = "{selected}"\n',
            encoding="utf-8",
        )
        lock: dict[str, object] = {
            "schema": schema,
            "tool_version": __version__,
            "hash_algorithm": "sha256",
            "hash_mode": "utf8-text-lf-v1",
            "files": {},
        }
        if schema == 3:
            lock["evaluator"] = {
                "version": __version__,
                "payload_manifest": PAYLOAD_MANIFEST,
                "payload_sha256": "a" * 64,
                "archive_name": f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl",
                "archive_sha256": "b" * 64,
            }
        (root / ".engineering-harness.lock").write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return root

    def _passing_identity(self, root: Path) -> RuntimeIdentity:
        environment = self.base / "released-evaluator"
        return RuntimeIdentity(
            schema="se-harness-runtime-identity-v3",
            passed=True,
            role="released-evaluator",
            python_executable=str(environment / "Scripts" / "python.exe"),
            python_version="3.12.0",
            harness_version=__version__,
            module_origin=str(environment / "Lib" / "site-packages" / "se_harness" / "__init__.py"),
            distribution_origin=str(environment / "Lib" / "site-packages"),
            template_origin=str(environment / "share" / "se-harness" / "templates" / "repository" / "standard"),
            entry_point_origin=str(environment / "Scripts" / "harnessctl.exe"),
            expected_root=str(environment),
            checkout_root=str(root),
            candidate_commit=None,
            evaluator_payload_manifest=PAYLOAD_MANIFEST,
            evaluator_payload_sha256="a" * 64,
            evaluator_archive_name=f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl",
            evaluator_archive_sha256="b" * 64,
            evaluator_wheel_sha256="b" * 64,
            isolated_python=True,
            user_site_enabled=False,
            pythonpath_present=False,
            python_entry_is_link=False,
            python_binary_position="within-expected-root",
            python_binary_sha256="c" * 64,
            diagnostics=(),
        )

    def test_matching_runtime_returns_canonical_privacy_bounded_evidence(self) -> None:
        root = self._write_identity_root()
        identity = self._passing_identity(root)
        with mock.patch("se_harness.mutation_guard._runtime_report", return_value=identity):
            authority = require_mutation_authority(root, operation="create-artifact")
        parsed = parse_evaluator_evidence(authority.evidence_bytes)
        self.assertEqual(authority.evidence_sha256, parsed.sha256)
        rendered = authority.evidence_bytes.decode("utf-8")
        self.assertNotIn(str(self.base), rendered)
        self.assertIn("<evaluator-root>/", rendered)
        self.assertEqual([], parsed.value["diagnostics"])

    def test_lock_and_upgrade_transition_failures_have_stable_diagnostics(self) -> None:
        missing = self.base / "missing-lock"
        missing.mkdir()
        with self.assertRaisesRegex(HarnessError, r"MG001 \(create-artifact\)"):
            require_mutation_authority(missing, operation="create-artifact")

        legacy = self._write_identity_root(schema=2)
        with self.assertRaisesRegex(HarnessError, r"MG002 \(create-artifact\)"):
            require_mutation_authority(legacy, operation="create-artifact")

        mismatched = self._write_identity_root(config_version="9.9.9")
        with self.assertRaisesRegex(HarnessError, r"MG003 \(create-artifact\)"):
            require_mutation_authority(mismatched, operation="create-artifact")

        target = self._write_identity_root()
        unpackaged = InstalledEvaluatorIdentity(__version__, PAYLOAD_MANIFEST, "a" * 64)
        with mock.patch(
            "se_harness.mutation_guard.installed_evaluator_identity",
            return_value=unpackaged,
        ), self.assertRaisesRegex(HarnessError, r"MG004 \(upgrade-apply\)"):
            require_mutation_authority(
                target,
                operation="upgrade-apply",
                allow_upgrade_transition=True,
            )

        lock_path = target / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"].pop("archive_name")
        lock["evaluator"].pop("archive_sha256")
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(HarnessError, r"MG004 \(prepare-release\)"):
            require_mutation_authority(
                target,
                operation="prepare-release",
                require_archive=True,
            )

    def test_evaluator_transition_requires_exact_packet_and_retains_atomic_evidence(self) -> None:
        root = self.base / "governed-transition"
        changes, old_lock = plan_install(root, project_name="Governed Transition", mode="init")
        apply_changes(root, changes, old_lock, allow_updates=False)
        target_identity = InstalledEvaluatorIdentity(
            __version__,
            PAYLOAD_MANIFEST,
            "a" * 64,
            f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl",
            "b" * 64,
        )
        lock_path = root / LOCK_RELATIVE
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"] = {
            **target_identity.to_lock(),
            "payload_sha256": "c" * 64,
            "archive_sha256": "d" * 64,
        }
        # Explicit LF, and the recorded digest is the lock's declared mode rather
        # than this platform's bytes, so the packet reads the same on either default.
        lock_path.write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
        self.assertNotIn(b"\r", lock_path.read_bytes())
        prior_lock_sha256 = canonical_sha256(lock_path.read_bytes())
        work_order = root / "docs/engineering/upgrade/work-orders/WO-TST-001.md"
        work_order.parent.mkdir(parents=True)
        work_order.write_text(
            f'''+++
id = "WO-TST-001"
type = "work_order"
title = "Adopt exact released evaluator"
status = "in_progress"
owners = ["repository-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "{prior_lock_sha256}"
target_version = "{target_identity.version}"
target_payload_sha256 = "{target_identity.payload_sha256}"
target_archive_name = "{target_identity.archive_name}"
target_archive_sha256 = "{target_identity.archive_sha256}"
publication = "immutable"
authorized_by = "repository-owner"

[relations]
+++

# Work Order
''',
            encoding="utf-8",
        )
        changes, old_lock = plan_install(root, project_name=None, mode="upgrade")
        before = self._snapshot(root)
        passing = self._passing_identity(root)
        with mock.patch(
            "se_harness.mutation_guard.installed_evaluator_identity",
            return_value=target_identity,
        ), mock.patch(
            "se_harness.installer.installed_evaluator_identity",
            return_value=target_identity,
        ), mock.patch(
            "se_harness.mutation_guard._runtime_report",
            return_value=passing,
        ):
            with self.assertRaisesRegex(HarnessError, r"MG007.*separately approved --work-order"):
                apply_changes(root, changes, old_lock, allow_updates=True)
            self.assertEqual(before, self._snapshot(root))

            with self.assertRaisesRegex(HarnessError, "requires --evidence-output"):
                apply_changes(
                    root,
                    changes,
                    old_lock,
                    allow_updates=True,
                    upgrade_work_order="WO-TST-001",
                )
            self.assertEqual(before, self._snapshot(root))

            evidence_relative = Path(
                "docs/engineering/upgrade/evidence/WO-TST-001-evaluator-upgrade.json"
            )
            evidence_path = root / evidence_relative
            evidence_path.parent.mkdir(parents=True)
            evidence_path.write_text("existing evidence\n", encoding="utf-8")
            collision_before = self._snapshot(root)
            with self.assertRaisesRegex(HarnessError, "evidence output already exists"):
                apply_changes(
                    root,
                    changes,
                    old_lock,
                    allow_updates=True,
                    upgrade_work_order="WO-TST-001",
                    evidence_output=evidence_relative,
                )
            self.assertEqual(collision_before, self._snapshot(root))
            evidence_path.unlink()

            changed_identity = InstalledEvaluatorIdentity(
                __version__,
                PAYLOAD_MANIFEST,
                "e" * 64,
                target_identity.archive_name,
                target_identity.archive_sha256,
            )
            transition_before = self._snapshot(root)
            with mock.patch(
                "se_harness.installer.installed_evaluator_identity",
                return_value=changed_identity,
            ), self.assertRaisesRegex(HarnessError, "changed after authorization"):
                apply_changes(
                    root,
                    changes,
                    old_lock,
                    allow_updates=True,
                    upgrade_work_order="WO-TST-001",
                    evidence_output=evidence_relative,
                )
            self.assertEqual(transition_before, self._snapshot(root))

            result = apply_changes(
                root,
                changes,
                old_lock,
                allow_updates=True,
                upgrade_work_order="WO-TST-001",
                evidence_output=evidence_relative,
            )
        self.assertEqual(target_identity.to_lock(), result["evaluator"])
        evidence = json.loads((root / evidence_relative).read_bytes())
        self.assertEqual("se-harness-evaluator-upgrade-evidence-v1", evidence["schema"])
        self.assertEqual("WO-TST-001", evidence["work_order"])
        self.assertEqual(prior_lock_sha256, evidence["prior"]["lock_sha256"])
        self.assertEqual(MATCH_DECLARED, evidence["prior"]["lock_match"])
        self.assertEqual(target_identity.to_lock(), evidence["target"])
        self.assertTrue(evidence["transaction"]["atomic"])
        self.assertTrue(evidence["postconditions"]["no_op_replay"])
        self.assertFalse(evidence["postconditions"]["product_release_performed"])

    def test_prior_lock_authority_is_indifferent_to_the_checkout_newline(self) -> None:
        root = self.base / "newline-materialization"
        changes, old_lock = plan_install(root, project_name="Newline", mode="init")
        apply_changes(root, changes, old_lock, allow_updates=False)
        target_identity = InstalledEvaluatorIdentity(
            __version__,
            PAYLOAD_MANIFEST,
            "a" * 64,
            f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl",
            "b" * 64,
        )
        lock_path = root / LOCK_RELATIVE
        lock_lf = lock_path.read_bytes().replace(b"\r\n", b"\n")
        prior_lock_sha256 = canonical_sha256(lock_lf)
        work_order = root / "docs/engineering/upgrade/work-orders/WO-TST-002.md"
        work_order.parent.mkdir(parents=True)
        work_order.write_text(
            f'''+++
id = "WO-TST-002"
type = "work_order"
title = "Adopt exact released evaluator"
status = "in_progress"
owners = ["repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "{prior_lock_sha256}"
target_version = "{target_identity.version}"
target_payload_sha256 = "{target_identity.payload_sha256}"
target_archive_name = "{target_identity.archive_name}"
target_archive_sha256 = "{target_identity.archive_sha256}"
publication = "immutable"
authorized_by = "repository-owner"

[relations]
+++

# Work Order
''',
            encoding="utf-8",
            newline="\n",
        )
        # The guard supplies the lock's exact bytes and the declaration decides the
        # mode, so a CRLF checkout of the same blob must reach the same authority.
        for materialization, payload in (("lf", lock_lf), ("crlf", lock_lf.replace(b"\n", b"\r\n"))):
            with self.subTest(materialization=materialization):
                lock_path.write_bytes(payload)
                with mock.patch(
                    "se_harness.mutation_guard.installed_evaluator_identity",
                    return_value=target_identity,
                ), mock.patch(
                    "se_harness.mutation_guard._runtime_report",
                    return_value=self._passing_identity(root),
                ):
                    authority = require_mutation_authority(
                        root,
                        operation="upgrade-apply",
                        allow_upgrade_transition=True,
                        upgrade_work_order="WO-TST-002",
                    )
                authorization = authority.upgrade_authorization
                self.assertIsNotNone(authorization)
                self.assertEqual(MATCH_DECLARED, authorization.prior_lock_match)
                self.assertEqual(prior_lock_sha256, authorization.prior_lock_sha256)

    def test_a_legacy_recorded_prior_lock_still_applies_and_is_reported(self) -> None:
        root = self.base / "legacy-recorded-prior"
        changes, old_lock = plan_install(root, project_name="Legacy Prior", mode="init")
        apply_changes(root, changes, old_lock, allow_updates=False)
        target_identity = InstalledEvaluatorIdentity(
            __version__,
            PAYLOAD_MANIFEST,
            "a" * 64,
            f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl",
            "b" * 64,
        )
        lock_path = root / LOCK_RELATIVE
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"] = {
            **target_identity.to_lock(),
            "payload_sha256": "c" * 64,
            "archive_sha256": "d" * 64,
        }
        lock_bytes = (json.dumps(lock, indent=2, sort_keys=True) + "\n").encode("utf-8")
        lock_path.write_bytes(lock_bytes)
        # Recorded the way a pre-declaration authorization recorded it: the raw
        # digest of a CRLF checkout of these exact LF bytes.
        prior_lock_sha256 = raw_sha256(lock_bytes.replace(b"\n", b"\r\n"))
        self.assertNotEqual(prior_lock_sha256, canonical_sha256(lock_bytes))
        work_order = root / "docs/engineering/upgrade/work-orders/WO-TST-003.md"
        work_order.parent.mkdir(parents=True)
        work_order.write_text(
            f'''+++
id = "WO-TST-003"
type = "work_order"
title = "Adopt exact released evaluator"
status = "in_progress"
owners = ["repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "{prior_lock_sha256}"
target_version = "{target_identity.version}"
target_payload_sha256 = "{target_identity.payload_sha256}"
target_archive_name = "{target_identity.archive_name}"
target_archive_sha256 = "{target_identity.archive_sha256}"
publication = "immutable"
authorized_by = "repository-owner"

[relations]
+++

# Work Order
''',
            encoding="utf-8",
            newline="\n",
        )
        evidence_relative = Path(
            "docs/engineering/upgrade/evidence/WO-TST-003-evaluator-upgrade.json"
        )
        changes, old_lock = plan_install(root, project_name=None, mode="upgrade")
        with mock.patch(
            "se_harness.mutation_guard.installed_evaluator_identity",
            return_value=target_identity,
        ), mock.patch(
            "se_harness.installer.installed_evaluator_identity",
            return_value=target_identity,
        ), mock.patch(
            "se_harness.mutation_guard._runtime_report",
            return_value=self._passing_identity(root),
        ):
            result = apply_changes(
                root,
                changes,
                old_lock,
                allow_updates=True,
                upgrade_work_order="WO-TST-003",
                evidence_output=evidence_relative,
            )
        self.assertEqual(target_identity.to_lock(), result["evaluator"])
        evidence = json.loads((root / evidence_relative).read_bytes())
        # The authorization still succeeds, and the report names how it matched
        # instead of letting a legacy digest pass as an ordinary one.
        self.assertEqual(prior_lock_sha256, evidence["prior"]["lock_sha256"])
        self.assertEqual(MATCH_LEGACY_NEWLINE, evidence["prior"]["lock_match"])

    def test_runtime_failures_preserve_bounded_identity_codes(self) -> None:
        root = self._write_identity_root()
        passing = self._passing_identity(root)
        cases = {
            "RID002": "version",
            "RID003": "module_origin",
            "RID006": "checkout_root",
            "RID008": "PYTHONPATH",
            "RID009": "user_site",
            "RID010": "entry_point_origin",
            "RID021": "evaluator_payload_sha256",
            "RID022": "evaluator_wheel_sha256",
        }
        for code, subject in cases.items():
            with self.subTest(code=code):
                rejected = replace(
                    passing,
                    passed=False,
                    diagnostics=(IdentityDiagnostic(code, subject, "injected mismatch"),),
                )
                with mock.patch("se_harness.mutation_guard._runtime_report", return_value=rejected):
                    with self.assertRaisesRegex(HarnessError, rf"MG005.*{code} {subject}"):
                        require_mutation_authority(root, operation="create-artifact")

    def test_evidence_parser_rejects_noncanonical_or_untrusted_content(self) -> None:
        root = self._write_identity_root()
        canonical = build_evaluator_evidence(self._passing_identity(root)).canonical_bytes
        value = json.loads(canonical)
        cases: list[bytes] = []
        cases.append(json.dumps(value, indent=2, sort_keys=True).encode("utf-8"))
        candidate = json.loads(canonical)
        candidate["role"] = "candidate-source"
        cases.append((json.dumps(candidate, separators=(",", ":"), sort_keys=True) + "\n").encode())
        absolute = json.loads(canonical)
        absolute["origins"]["module"] = "C:/Users/example/se_harness/__init__.py"
        cases.append((json.dumps(absolute, separators=(",", ":"), sort_keys=True) + "\n").encode())
        traversal = json.loads(canonical)
        traversal["origins"]["module"] = "<evaluator-root>/../outside.py"
        cases.append((json.dumps(traversal, separators=(",", ":"), sort_keys=True) + "\n").encode())
        contaminated = json.loads(canonical)
        contaminated["environment"]["pythonpath_present"] = True
        cases.append((json.dumps(contaminated, separators=(",", ":"), sort_keys=True) + "\n").encode())
        duplicate = canonical.decode("utf-8").replace(
            '"role":"released-evaluator"',
            '"role":"released-evaluator","role":"released-evaluator"',
        ).encode("utf-8")
        cases.append(duplicate)
        for raw in cases:
            with self.subTest(raw=raw[:80]), self.assertRaises(EvaluatorEvidenceError):
                parse_evaluator_evidence(raw)

    def test_candidate_source_is_rejected_before_real_artifact_creation(self) -> None:
        root = self.base / "candidate-target"
        code, _, error = self._invoke("init", str(root), "--project-name", "Boundary Sample")
        self.assertEqual(0, code, error)
        before = self._snapshot(root)
        code, _, error = self._invoke(
            "create-artifact",
            str(root),
            "--domain",
            "boundary",
            "--type",
            "requirement",
            "--id",
            "REQ-TST-001",
        )
        self.assertEqual(2, code)
        self.assertIn("mutation guard MG005", error)
        self.assertEqual(before, self._snapshot(root))

    def test_every_public_mutator_rejects_before_any_target_write(self) -> None:
        root = self.base / "all-mutators"
        changes, old_lock = plan_install(root, project_name="All Mutators", mode="init")
        apply_changes(root, changes, old_lock, allow_updates=False)
        retained = root / "docs" / "engineering" / "evidence" / "WO-TST-001-input.txt"
        retained.parent.mkdir(parents=True, exist_ok=True)
        retained.write_text("test evidence\n", encoding="utf-8")

        catalog = {
            "WO-TST-001": {"id": "WO-TST-001", "type": "work_order", "status": "implemented"},
            "VER-TST-001": {"id": "VER-TST-001", "type": "verification", "status": "approved"},
            "REL-TST-001": {"id": "REL-TST-001", "type": "release_contract", "status": "approved"},
            "VREC-TST-001": {"id": "VREC-TST-001", "type": "verification_record", "status": "verified"},
        }

        def metadata(_root: Path, artifact: dict[str, object]) -> dict[str, object]:
            artifact_id = artifact["id"]
            if artifact_id == "WO-TST-001":
                return {"relations": {"verification": ["VER-TST-001"]}}
            if artifact_id == "REL-TST-001":
                return {"relations": {"gates": ["WO-TST-001"]}}
            if artifact_id == "VREC-TST-001":
                return {
                    "commit": "a" * 40,
                    "git_object_format": "sha1",
                    "relations": {"verifies_work_order": ["WO-TST-001"]},
                }
            return {"relations": {}}

        rejected = HarnessError("injected mutation guard rejection")
        before = self._snapshot(root)
        observed: list[str] = []
        upgrade_changes, upgrade_lock = plan_install(root, project_name=None, mode="upgrade")
        effect_envelope = validate_contract(
            {
                "schema": "se-harness-autonomy-envelope-v2",
                "selection": {
                    "work_order": "WO-TST-001",
                    "work_order_sha256": "1" * 64,
                    "repository_state": "2" * 64,
                    "evaluator_payload_sha256": "3" * 64,
                },
                "delegation": {
                    "asserted_by": "engineering-owner",
                    "operations": ["change-bundle-apply"],
                    "path_scope": ["docs/"],
                    "execution_profiles": ["implementer"],
                    "max_parallel_writers": 1,
                    "retry_limits": {"change-bundle-apply": 0},
                    "stop_before": [
                        "accountable-decision-required",
                        "action-time-authorization-required",
                    ],
                },
                "evidence": {"required_receipt": True, "required_paths": []},
                "authority": {
                    "decision_right": None,
                    "delegate": "worker",
                    "execution_profile": "implementer",
                    "delegation_sha256": "4" * 64,
                    "work_order_sha256": "1" * 64,
                    "expected_repository_state": "2" * 64,
                    "previous_receipt_sha256": None,
                    "nonce": "5" * 32,
                    "issued_at": "2026-08-25T10:00:00Z",
                    "not_after": "2026-08-25T10:05:00Z",
                    "retry_ordinal": 0,
                },
            }
        )

        def guard(_repository: Path, *, operation: str, **_kwargs: object) -> None:
            observed.append(operation)
            raise rejected

        with mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=guard,
        ), mock.patch(
            "se_harness.effect_broker.require_mutation_authority",
            side_effect=guard,
        ), mock.patch(
            "se_harness.provenance._validation_catalog",
            return_value=catalog,
        ), mock.patch(
            "se_harness.provenance._load_metadata",
            side_effect=metadata,
        ), mock.patch(
            "se_harness.provenance._record_domain",
            return_value="test",
        ):
            operations = (
                lambda: scaffold_domain(root, domain="boundary", title=None, dry_run=False),
                lambda: create_artifact(
                    root,
                    domain="boundary",
                    artifact_type="requirement",
                    artifact_id="REQ-TST-002",
                    dry_run=False,
                ),
                lambda: apply_changes(root, [], {"tool_version": __version__}, allow_updates=False),
                lambda: apply_changes(root, upgrade_changes, upgrade_lock, allow_updates=True),
                lambda: apply_renumber_plan(SimpleNamespace(repository_root=root)),
                lambda: apply_transition(SimpleNamespace(root=root)),
                lambda: capture_verification(
                    root,
                    record_id="VREC-TST-002",
                    work_order_ids=["WO-TST-001"],
                    verification_ids=["VER-TST-001"],
                    evidence_paths=[retained.relative_to(root).as_posix()],
                    owner="quality-owner",
                    output=None,
                ),
                lambda: prepare_release(
                    root,
                    record_id="RLS-TST-001",
                    release_contract_id="REL-TST-001",
                    verification_record_ids=["VREC-TST-001"],
                    work_order_ids=["WO-TST-001"],
                    version="9.9.9",
                    authorized_by="release-owner",
                    tag=None,
                    output=None,
                ),
                lambda: apply_change_bundle(
                    root,
                    bundle_bytes=b"",
                    object_store=self.base / "objects",
                    envelope=effect_envelope,
                    current_delegation_sha256="4" * 64,
                    evaluator=SimpleNamespace(payload_sha256="3" * 64),
                    runtime_store=None,
                    session=None,
                    gates_passed=True,
                ),
            )
            for operation in operations:
                with self.subTest(operation=len(observed)), self.assertRaisesRegex(
                    HarnessError,
                    "injected mutation guard rejection",
                ):
                    operation()
                self.assertEqual(before, self._snapshot(root))

        self.assertEqual(
            {
                "scaffold-domain",
                "create-artifact",
                "installed-root-apply",
                "upgrade-apply",
                "renumber-artifacts-apply",
                "transition-apply",
                "capture-verification",
                "prepare-release",
                "change-bundle-apply",
            },
            set(observed),
        )
        self.assertEqual(set(PUBLIC_MUTATION_OPERATIONS), set(observed))

    def test_unregistered_mutation_operation_is_rejected(self) -> None:
        root = self._write_identity_root()
        with self.assertRaisesRegex(HarnessError, "operation is not registered"):
            require_mutation_authority(root, operation="future-unregistered-mutator")

    def test_upgrade_apply_rejects_a_caller_supplied_stale_plan_without_writes(self) -> None:
        root = self.base / "stale-upgrade"
        changes, old_lock = plan_install(root, project_name="Stale Plan", mode="init")
        apply_changes(root, changes, old_lock, allow_updates=False)
        before = self._snapshot(root)
        current_lock = json.loads((root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        with mock.patch("se_harness.mutation_guard.require_mutation_authority") as guard:
            with self.assertRaisesRegex(HarnessError, "upgrade plan or installed root changed"):
                apply_changes(root, [], current_lock, allow_updates=True)
        guard.assert_not_called()
        self.assertEqual(before, self._snapshot(root))


if __name__ == "__main__":
    unittest.main()
