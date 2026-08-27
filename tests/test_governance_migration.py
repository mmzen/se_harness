from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import re
import subprocess
import tempfile
import tomllib
import unittest
import venv
from importlib import resources
from pathlib import Path
from unittest import mock

import se_harness
from se_harness.cli import build_parser, main
from se_harness.governance_migration import (
    REPORT_NAME,
    GovernanceMigrationError,
    _semantic_value,
    run_governance_migration,
    verify_result_digest,
)
from se_harness.governance_migration_contract import (
    STAGE_ORDER,
    MigrationContractError,
    canonical_json,
    classify_migration,
    load_migration_contract,
    load_migration_scenario,
    sha256_bytes,
)
from se_harness.workflow_contract import load_lifecycle_registry


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/governance_migration"
HISTORICAL = FIXTURES / "historical-0.5.0-to-0.6.0.json"
CANDIDATE = FIXTURES / "candidate-0.7.1-to-0.8.0.json"
# The retained pair of the previous candidate (WO-RLS-013); the root moved to 0.7.1 under WO-HUP-007.
PREVIOUS_CANDIDATE = FIXTURES / "candidate-0.6.0-to-0.7.1.json"
SYNTHETIC = FIXTURES / "synthetic-n-minus-1-to-n.json"
SCENARIOS = (HISTORICAL, PREVIOUS_CANDIDATE, CANDIDATE, SYNTHETIC)
WORKFLOW = ROOT / ".github/workflows/candidate-evidence.yml"

# Already-public predecessor wheels, measured from the index with
# `pip download --only-binary=:all: --no-deps` and hashed as files. A scenario
# that pins a predecessor archive is fabricated against these, so a wrong digest
# in either place fails rather than agreeing with itself.
PUBLIC_PREDECESSOR_ARCHIVES = {
    "0.5.0": (
        "se_harness-0.5.0-py3-none-any.whl",
        "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f",
    ),
    "0.6.0": (
        "se_harness-0.6.0-py3-none-any.whl",
        "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7",
    ),
    "0.7.0": (
        "se_harness-0.7.0-py3-none-any.whl",
        "e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3",
    ),
    # 0.7.1: published by RLS-SEH-016 (WO-RLS-013); the digest PyPI serves for the file.
    "0.7.1": (
        "se_harness-0.7.1-py3-none-any.whl",
        "ddd403cde17fc3770460809cbe8f9edb68f47c3aaa0422fe021334279994225d",
    ),
}


class GovernanceMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temporary.name)
        cls.predecessor = cls._create_runtime("predecessor")
        cls.successor = cls._create_runtime("successor")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    @classmethod
    def _create_runtime(cls, name: str) -> tuple[Path, Path]:
        root = cls.base / name
        venv.EnvBuilder(with_pip=False, clear=True).create(root)
        python = root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        completed = subprocess.run(
            [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
            check=True,
            capture_output=True,
            text=True,
        )
        package = Path(completed.stdout.strip()) / "se_harness"
        package.mkdir(parents=True)
        return python, package

    def setUp(self) -> None:
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.base))
        self.repository = self.case / "operational"
        self.repository.mkdir()
        (self.repository / "preserved.txt").write_text("operational bytes\n", encoding="utf-8")

    def _versions(self, predecessor: str, successor: str) -> None:
        self.predecessor[1].joinpath("__init__.py").write_text(
            f'__version__ = "{predecessor}"\n', encoding="utf-8", newline="\n"
        )
        self.successor[1].joinpath("__init__.py").write_text(
            f'__version__ = "{successor}"\n', encoding="utf-8", newline="\n"
        )
        evaluator_identity = self.predecessor[1] / "evaluator_identity.py"
        archive = PUBLIC_PREDECESSOR_ARCHIVES.get(predecessor)
        if archive is not None:
            name, digest = archive
            evaluator_identity.write_text(
                "class Identity:\n"
                f"    archive_name = '{name}'\n"
                f"    archive_sha256 = '{digest}'\n"
                "    payload_sha256 = '1111111111111111111111111111111111111111111111111111111111111111'\n"
                "def installed_evaluator_identity():\n"
                "    return Identity()\n",
                encoding="utf-8",
                newline="\n",
            )
        else:
            evaluator_identity.unlink(missing_ok=True)

    def _run(
        self,
        output: str,
        *,
        scenario: Path = SYNTHETIC,
        fault: str | None = None,
        environment: dict[str, str] | None = None,
    ) -> dict:
        declared = json.loads(scenario.read_bytes())["versions"]
        self._versions(declared["predecessor"], declared["successor"])
        return run_governance_migration(
            self.repository,
            scenario_path=scenario,
            predecessor_python=self.predecessor[0],
            successor_python=self.successor[0],
            output=self.case / output,
            environment={} if environment is None else environment,
            _fault_stage=fault,
        )

    def test_contract_and_every_scenario_are_strict_complete_and_packaged(self) -> None:
        contract = load_migration_contract()
        self.assertEqual(list(STAGE_ORDER), contract["stage_order"])
        self.assertEqual(set(STAGE_ORDER), set(contract["stages"]))
        module_digest = sha256_bytes((ROOT / "se_harness/governance_migration.py").read_bytes())
        self.assertEqual(
            {module_digest},
            {item["implementation_sha256"] for item in contract["adapters"].values()},
        )
        self.assertEqual(sorted(path.name for path in SCENARIOS), sorted(path.name for path in FIXTURES.glob("*.json")))
        for path in SCENARIOS:
            scenario, raw = load_migration_scenario(path, contract)
            self.assertEqual(raw, canonical_json(scenario))
            self.assertEqual(list(STAGE_ORDER), [stage["id"] for stage in scenario["stages"]])
        packaged = resources.files("se_harness").joinpath("governance_migration_contract.json").read_bytes()
        self.assertEqual((ROOT / "se_harness/governance_migration_contract.json").read_bytes(), packaged)
        self.assertIn(
            '"governance_migration_contract.json"',
            (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        )

    def test_synthetic_rehearsal_is_complete_disposable_private_and_deterministic(self) -> None:
        before = (self.repository / "preserved.txt").read_bytes()
        first = self._run("first")
        second = self._run("second")
        self.assertEqual("pass", first["overall_result"])
        self.assertEqual("successor", first["final_selected_evaluator"])
        self.assertEqual(list(STAGE_ORDER), [stage["id"] for stage in first["stages"]])
        self.assertTrue(all(stage["result"] == "pass" for stage in first["stages"]))
        self.assertEqual(first["semantic_sha256"], second["semantic_sha256"])
        self.assertTrue(verify_result_digest(first))
        self.assertTrue(first["operational_state"]["unchanged"])
        self.assertTrue(all(value is False for value in first["external_actions"].values()))
        self.assertEqual(before, (self.repository / "preserved.txt").read_bytes())
        self.assertFalse((self.case / "first/disposable-workspace").exists())
        retained = (self.case / "first" / REPORT_NAME).read_bytes()
        self.assertEqual(first, json.loads(retained))
        self.assertEqual(retained, canonical_json(first))
        self.assertNotIn(str(self.base).encode(), retained)

    def test_semantic_digest_normalizes_platform_build_facts_but_retains_them(self) -> None:
        report = self._run("platform-base")
        other = copy.deepcopy(report)
        other["host"] = {"implementation": "OtherPython", "os": "OtherOS"}
        for runtime in other["runtimes"].values():
            runtime["archive_sha256"] = "a" * 64
            runtime["executable_sha256"] = "b" * 64
            runtime["package_tree_sha256"] = "d" * 64
            runtime["payload_sha256"] = "e" * 64
            runtime["python_version"] = "99.0.0"
        for snapshot in other["operational_state"].values():
            if isinstance(snapshot, dict):
                snapshot["source_sha256"] = "c" * 64
        for stage in other["stages"]:
            stage["duration_ms"] += 1000

        self.assertNotEqual(canonical_json(report), canonical_json(other))
        self.assertEqual(
            sha256_bytes(canonical_json(_semantic_value(report))),
            sha256_bytes(canonical_json(_semantic_value(other))),
        )

    def test_historical_scenario_preserves_distinct_complete_and_compatible_claims(self) -> None:
        report = self._run("historical", scenario=HISTORICAL)
        self.assertEqual("migration-required", report["classification"]["outcome"])
        validation = next(stage for stage in report["stages"] if stage["id"] == "validate-complete")
        self.assertEqual("migration-required", validation["report"]["validation"]["outcome"])
        self.assertEqual(
            ["missing-evaluator-evidence", "unsupported-release-record-schema"],
            validation["report"]["validation"]["codes"],
        )
        assessment = next(stage for stage in report["stages"] if stage["id"] == "assess")
        self.assertEqual("complete-successor-validation", assessment["report"]["complete"]["claim"])
        self.assertEqual("predecessor-compatible-view", assessment["report"]["compatible"]["claim"])
        self.assertEqual(
            "refused-unsupported-rejected-state",
            assessment["report"]["predecessor_complete_graph"],
        )
        rejection = next(stage for stage in report["stages"] if stage["id"] == "reject")
        adoption = next(stage for stage in report["stages"] if stage["id"] == "adopt")
        self.assertEqual("proposal-status-rejected", rejection["authority_effect"])
        self.assertEqual("disposable-root-evaluator-selected", adoption["authority_effect"])
        self.assertTrue(adoption["report"]["rollback_exact"])
        self.assertTrue(adoption["report"]["noop_replay"])

    def test_rejected_predecessor_observation_matches_registry_adapter_marker(self) -> None:
        registry = load_lifecycle_registry()
        scenario, _ = load_migration_scenario(HISTORICAL, load_migration_contract())
        self.assertFalse(scenario["fixture"]["predecessor_accepts_rejected"])
        self.assertEqual(
            {"required"},
            {
                registry[family]["rejected"].predecessor_adapter
                for family in ("verification_record", "release_record")
            },
        )

    def _lane_scenarios(self) -> list[Path]:
        # WO-CIP-003: the lane no longer names a scenario file; candidate-source
        # derives it from the declared root and the candidate version, and the
        # migration job takes it from that job's outputs.
        from repository_tools.predecessor_facts import derive

        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("$scenario = Join-Path $env:GITHUB_WORKSPACE $env:MIGRATION_SCENARIO", workflow)
        self.assertNotIn("governance_migration/", workflow)
        return [ROOT / derive(ROOT).scenario]

    def _lane_predecessor_pin(self) -> tuple[str, str]:
        from repository_tools.predecessor_facts import derive

        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("PREDECESSOR_VERSION: ${{ needs.candidate-source.outputs.predecessor_version }}", workflow)
        self.assertIn("PREDECESSOR_WHEEL_SHA256: ${{ needs.candidate-source.outputs.predecessor_wheel_sha256 }}", workflow)
        self.assertIsNone(re.search(r'PREDECESSOR_WHEEL_SHA256:\s*"', workflow))
        facts = derive(ROOT)
        return facts.version, facts.wheel_sha256

    def test_lane_scenario_declares_the_version_the_candidate_builds(self) -> None:
        # The gate exists to prove that evaluator N-1 governs *this* candidate, so
        # the scenario the lane runs has to name the version the candidate builds.
        # When they diverge the rehearsal refuses with MIG211 on a hosted runner;
        # this test moves that refusal onto the author's workstation.
        declared = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
        self.assertEqual(se_harness.__version__, declared)
        selected = self._lane_scenarios()
        self.assertEqual([CANDIDATE], selected)
        scenario, _ = load_migration_scenario(selected[0], load_migration_contract())
        self.assertEqual(declared, scenario["versions"]["successor"])
        self.assertEqual(declared, scenario["runtime_expectations"]["successor"]["version"])

        # A non-historical scenario is not forced to pin its predecessor archive,
        # so WO-REB-023 requires the pin and this asserts the workflow, the
        # scenario, and the measured public wheel all name the same one.
        predecessor = scenario["runtime_expectations"]["predecessor"]
        self.assertEqual(self._lane_predecessor_pin(), (predecessor["version"], predecessor["archive_sha256"]))
        self.assertEqual(
            PUBLIC_PREDECESSOR_ARCHIVES[predecessor["version"]],
            (predecessor["archive_name"], predecessor["archive_sha256"]),
        )

    def test_candidate_pair_classifies_compatible_over_the_whole_vocabulary(self) -> None:
        # Route A of WO-REB-023 asserts less than the historical pair does, so the
        # outcome it does assert is pinned here: a later version that introduces a
        # boundary the contract can name must fail this instead of passing quietly.
        contract = load_migration_contract()
        scenario, _ = load_migration_scenario(CANDIDATE, contract)
        self.assertEqual(sorted(contract["capabilities"]), sorted(scenario["capabilities"]["predecessor"]))
        self.assertEqual(
            scenario["capabilities"]["predecessor"],
            scenario["capabilities"]["successor_required"],
        )
        self.assertEqual(
            {"affected_operations": [], "missing_capabilities": [], "outcome": "compatible"},
            classify_migration(scenario, contract),
        )

    def test_candidate_rehearsal_is_complete_compatible_and_deterministic(self) -> None:
        first = self._run("candidate-first", scenario=CANDIDATE)
        second = self._run("candidate-second", scenario=CANDIDATE)
        self.assertEqual("pass", first["overall_result"])
        self.assertIsNone(first["first_failed_stage"])
        self.assertTrue(all(stage["result"] == "pass" for stage in first["stages"]))
        self.assertTrue(
            all(stage["observed_mutations"] == [] or set(stage["observed_mutations"]) <= set(stage["permitted_mutations"]) for stage in first["stages"])
        )
        self.assertEqual("compatible", first["classification"]["outcome"])
        self.assertTrue(first["operational_state"]["unchanged"])
        self.assertTrue(all(value is False for value in first["external_actions"].values()))
        self.assertEqual(first["semantic_sha256"], second["semantic_sha256"])

        # 0.6.0 already supports schema 3, evaluator evidence, and the rejected
        # terminal state, so the bootstrap it rejects is complete and the
        # predecessor can read the rejected history. Both differ from the
        # 0.5.0-to-0.6.0 pair and are the substance of "compatible".
        validation = next(stage for stage in first["stages"] if stage["id"] == "validate-complete")
        self.assertEqual({"codes": [], "outcome": "valid"}, validation["report"]["validation"])
        assessment = next(stage for stage in first["stages"] if stage["id"] == "assess")
        self.assertEqual("pass", assessment["report"]["predecessor_complete_graph"])

    def test_candidate_prefix_is_what_withdraws_the_boundary_guard(self) -> None:
        # MIG404 only guards a `historical-` scenario. Renaming the candidate pair
        # into that family is refused, which is why the prefix is deliberate and
        # why the compatible outcome above needs its own assertion.
        value = json.loads(CANDIDATE.read_bytes())
        value["scenario_id"] = "historical-0.6.0-to-0.7.0"
        renamed = self.case / "renamed-historical.json"
        renamed.write_bytes(canonical_json(value))
        report = self._run("renamed-historical", scenario=renamed)
        self.assertEqual("fail", report["overall_result"])
        self.assertEqual("validate-complete", report["first_failed_stage"])
        self.assertIn("MIG404", report["stages"][1]["diagnostic"])
        self.assertTrue(report["operational_state"]["unchanged"])

    def test_historical_pair_left_the_lane_and_is_still_exercised_here(self) -> None:
        # WO-REB-023 removed the historical pair from the hosted lane because its
        # successor can only ever be 0.6.0. Dropped from the lane must not become
        # quietly unexercised, so both halves are asserted together.
        self.assertNotIn(HISTORICAL.name, WORKFLOW.read_text(encoding="utf-8"))
        report = self._run("historical-still-exercised", scenario=HISTORICAL)
        self.assertEqual("pass", report["overall_result"])
        self.assertEqual("migration-required", report["classification"]["outcome"])

    def test_every_stage_fails_closed_and_later_stages_do_not_run(self) -> None:
        for index, stage_id in enumerate(STAGE_ORDER):
            with self.subTest(stage=stage_id):
                report = self._run(f"fault-{index}", fault=stage_id)
                self.assertEqual("fail", report["overall_result"])
                self.assertEqual(stage_id, report["first_failed_stage"])
                selected = next(i for i, stage in enumerate(report["stages"]) if stage["id"] == stage_id)
                self.assertEqual("fail", report["stages"][selected]["result"])
                self.assertTrue(all(stage["result"] == "not-run" for stage in report["stages"][selected + 1 :]))
                self.assertTrue(report["operational_state"]["unchanged"])

    def test_scenario_rejects_noncanonical_reordered_role_and_decision_inputs(self) -> None:
        contract = load_migration_contract()
        original = json.loads(SYNTHETIC.read_bytes())
        noncanonical = self.case / "noncanonical.json"
        noncanonical.write_text(json.dumps(original, indent=2), encoding="utf-8")
        with self.assertRaisesRegex(MigrationContractError, "MIG146"):
            load_migration_scenario(noncanonical, contract)

        reordered_value = json.loads(SYNTHETIC.read_bytes())
        reordered_value["stages"][0], reordered_value["stages"][1] = (
            reordered_value["stages"][1],
            reordered_value["stages"][0],
        )
        reordered = self.case / "reordered.json"
        reordered.write_bytes(canonical_json(reordered_value))
        with self.assertRaisesRegex(MigrationContractError, "MIG166"):
            load_migration_scenario(reordered, contract)

        role_value = json.loads(SYNTHETIC.read_bytes())
        role_value["stages"][1]["technical_role"] = "predecessor"
        role = self.case / "role.json"
        role.write_bytes(canonical_json(role_value))
        with self.assertRaisesRegex(MigrationContractError, "MIG167"):
            load_migration_scenario(role, contract)

        decision_value = json.loads(SYNTHETIC.read_bytes())
        decision_value["decisions"][0]["artifact_id"] = "RLS-MIG-999"
        decision = self.case / "decision.json"
        decision.write_bytes(canonical_json(decision_value))
        with self.assertRaisesRegex(MigrationContractError, "MIG143"):
            load_migration_scenario(decision, contract)

    def test_runtime_output_and_credential_boundaries_fail_before_mutation(self) -> None:
        self._versions("41.2.0", "42.0.0")
        with self.assertRaisesRegex(GovernanceMigrationError, "MIG223"):
            run_governance_migration(
                self.repository,
                scenario_path=SYNTHETIC,
                predecessor_python=self.predecessor[0],
                successor_python=self.predecessor[0],
                output=self.case / "shared-runtime",
                environment={},
            )
        with self.assertRaisesRegex(GovernanceMigrationError, "MIG222"):
            run_governance_migration(
                self.repository,
                scenario_path=SYNTHETIC,
                predecessor_python=self.predecessor[0],
                successor_python=self.successor[0],
                output=self.case / "credential",
                environment={"GITHUB_TOKEN": "secret"},
            )
        with self.assertRaisesRegex(GovernanceMigrationError, "MIG219"):
            run_governance_migration(
                self.repository,
                scenario_path=SYNTHETIC,
                predecessor_python=self.predecessor[0],
                successor_python=self.successor[0],
                output=self.repository / "forbidden-output",
                environment={},
            )
        self.assertFalse((self.repository / "forbidden-output").exists())

        self._versions("0.5.0", "0.6.0")
        identity_module = self.predecessor[1] / "evaluator_identity.py"
        identity_module.write_text(
            identity_module.read_text(encoding="utf-8").replace(
                "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f",
                "0" * 64,
            ),
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaisesRegex(GovernanceMigrationError, "MIG229"):
            run_governance_migration(
                self.repository,
                scenario_path=HISTORICAL,
                predecessor_python=self.predecessor[0],
                successor_python=self.successor[0],
                output=self.case / "wrong-predecessor",
                environment={},
            )

    def test_authority_oracle_rejects_undeclared_and_operational_mutations(self) -> None:
        from se_harness import governance_migration as migration

        self._versions("41.2.0", "42.0.0")
        original_prepare = migration.STAGE_DRIVERS["prepare"]

        def undeclared(workspace: Path, scenario: dict, stage: dict) -> dict:
            details = original_prepare(workspace, scenario, stage)
            (workspace / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
            return details

        with mock.patch.dict(migration.STAGE_DRIVERS, {"prepare": undeclared}):
            report = run_governance_migration(
                self.repository,
                scenario_path=SYNTHETIC,
                predecessor_python=self.predecessor[0],
                successor_python=self.successor[0],
                output=self.case / "undeclared",
                environment={},
            )
        self.assertEqual("fail", report["overall_result"])
        self.assertIn("MIG415", report["stages"][0]["diagnostic"])

        preserved = self.repository / "preserved.txt"
        before = preserved.read_bytes()

        def operational_mutation(workspace: Path, scenario: dict, stage: dict) -> dict:
            details = original_prepare(workspace, scenario, stage)
            preserved.write_text("changed by injected test\n", encoding="utf-8")
            return details

        try:
            with mock.patch.dict(migration.STAGE_DRIVERS, {"prepare": operational_mutation}):
                report = run_governance_migration(
                    self.repository,
                    scenario_path=SYNTHETIC,
                    predecessor_python=self.predecessor[0],
                    successor_python=self.successor[0],
                    output=self.case / "operational-mutation",
                    environment={},
                )
            self.assertEqual("fail", report["overall_result"])
            self.assertIn("MIG419", report["stages"][0]["diagnostic"])
            self.assertFalse(report["operational_state"]["unchanged"])
        finally:
            preserved.write_bytes(before)

    def test_output_collision_fails_without_overwrite(self) -> None:
        self._versions("41.2.0", "42.0.0")
        occupied = self.case / "occupied"
        occupied.mkdir()
        marker = occupied / "marker.txt"
        marker.write_bytes(b"preserve\n")
        with self.assertRaisesRegex(GovernanceMigrationError, "MIG220"):
            run_governance_migration(
                self.repository,
                scenario_path=SYNTHETIC,
                predecessor_python=self.predecessor[0],
                successor_python=self.successor[0],
                output=occupied,
                environment={},
            )
        self.assertEqual(b"preserve\n", marker.read_bytes())

    def test_cli_contract_is_exact_and_json_result_is_canonical(self) -> None:
        parsed = build_parser().parse_args(
            [
                "rehearse-migration",
                str(self.repository),
                "--scenario",
                str(SYNTHETIC),
                "--predecessor-python",
                str(self.predecessor[0]),
                "--successor-python",
                str(self.successor[0]),
                "--output",
                str(self.case / "parser-output"),
                "--json",
            ]
        )
        self.assertEqual("rehearse-migration", parsed.command)
        self._versions("41.2.0", "42.0.0")
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(
                [
                    "rehearse-migration",
                    str(self.repository),
                    "--scenario",
                    str(SYNTHETIC),
                    "--predecessor-python",
                    str(self.predecessor[0]),
                    "--successor-python",
                    str(self.successor[0]),
                    "--output",
                    str(self.case / "cli-output"),
                    "--json",
                ]
            )
        self.assertEqual(0, code, error.getvalue())
        value = json.loads(output.getvalue())
        self.assertEqual("pass", value["overall_result"])
        self.assertEqual(output.getvalue().encode(), canonical_json(value))


if __name__ == "__main__":
    unittest.main()
