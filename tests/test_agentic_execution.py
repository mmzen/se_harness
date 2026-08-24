from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pathlib import PurePosixPath

from se_harness.skill_contract import (
    CONTRACT_SCHEMA,
    CONTRACT_SCHEMA_V2,
    MANIFEST_SCHEMA,
    SkillContractError,
    build_skill_manifest,
    canonical_json_bytes,
    load_skill_contract,
    parse_skill_contract_bytes,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-orient"
SKILLS_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills"
PHASE3_ROOTS = {
    name: SKILLS_ROOT / name
    for name in (
        "harness-draft-change",
        "harness-execute-work-order",
        "harness-prepare-assurance",
    )
}
ORIENT = SKILL_ROOT / "scripts/orient.py"
FAKE_EVALUATOR = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/fake_evaluator.py"
VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/canonical_vectors.json"
PHASE3_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase3/portable_vectors.json"
HOST_SURFACE_VECTORS = REPOSITORY_ROOT / "tests/fixtures/agentic_execution/host_activation/expected_surfaces.json"
CLAUDE_SKILLS_ROOT = REPOSITORY_ROOT / "templates/repository/standard/.claude/skills"
ALL_SKILL_NAMES = {"harness-orient", *PHASE3_ROOTS}


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


class SkillContractTests(unittest.TestCase):
    def test_canonical_harness_orient_contract_and_manifest_validate(self) -> None:
        contract = load_skill_contract(SKILL_ROOT / "skill-contract.json")
        manifest = build_skill_manifest(SKILL_ROOT)
        vectors = json.loads(VECTORS.read_text(encoding="utf-8"))

        self.assertEqual(CONTRACT_SCHEMA, contract.value["schema"])
        self.assertEqual("harness-orient", contract.name)
        self.assertEqual("read-only", contract.value["mutation_class"])
        self.assertFalse(contract.value["delegation"]["allowed"])
        self.assertFalse(contract.value["evidence"]["target_retention"])
        self.assertEqual(MANIFEST_SCHEMA, manifest.value["schema"])
        self.assertEqual(
            ["SKILL.md", "scripts/orient.py", "skill-contract.json"],
            [item["path"] for item in manifest.value["files"]],
        )
        self.assertRegex(manifest.sha256, r"^[0-9a-f]{64}$")
        self.assertEqual(vectors["portable_core"]["files"], manifest.value["files"])
        self.assertEqual(vectors["portable_core"]["manifest_sha256"], manifest.sha256)

    def test_contract_rejects_duplicate_and_unknown_fields(self) -> None:
        raw = (SKILL_ROOT / "skill-contract.json").read_bytes()
        duplicate = raw.replace(b'{\n  "schema":', b'{\n  "schema": "se-harness-skill-contract-v1",\n  "schema":', 1)
        with self.assertRaisesRegex(SkillContractError, "SKC002"):
            parse_skill_contract_bytes(duplicate)

        value = json.loads(raw)
        value["authority"] = "invented"
        with self.assertRaisesRegex(SkillContractError, "SKC006"):
            parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_contract_rejects_authority_delegation_and_target_retention(self) -> None:
        original = json.loads((SKILL_ROOT / "skill-contract.json").read_text(encoding="utf-8"))
        cases = (
            ("mutation", lambda value: value.__setitem__("mutation_class", "write"), "SKC013"),
            ("delegation", lambda value: value["delegation"].__setitem__("allowed", True), "SKC018"),
            ("retention", lambda value: value["evidence"].__setitem__("target_retention", True), "SKC019"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                value = json.loads(json.dumps(original))
                mutate(value)
                with self.assertRaisesRegex(SkillContractError, code):
                    parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_closed_phase3_contracts_and_manifests_validate(self) -> None:
        expected = {
            "harness-draft-change": ("draft-writing", ["draft-create", "draft-revise", "planning-note-write"]),
            "harness-execute-work-order": (
                "governed-mutation",
                ["implementation-write", "test-execution", "evidence-write"],
            ),
            "harness-prepare-assurance": ("governed-mutation", ["verification-record-prepare"]),
        }
        for name, root in PHASE3_ROOTS.items():
            with self.subTest(skill=name):
                contract = load_skill_contract(root / "skill-contract.json")
                manifest = build_skill_manifest(root)
                self.assertEqual(CONTRACT_SCHEMA_V2, contract.value["schema"])
                self.assertEqual(name, contract.name)
                self.assertEqual(expected[name][0], contract.value["mutation_class"])
                self.assertEqual(expected[name][1], contract.value["effects"]["permitted"])
                self.assertEqual([], contract.value["effects"]["lifecycle_transitions"])
                self.assertTrue(contract.value["activation"]["explicit"])
                self.assertFalse(contract.value["activation"]["implicit"])
                self.assertFalse(contract.value["delegation"]["allowed"])
                self.assertEqual("single-agent", contract.value["delegation"]["fallback"])
                self.assertEqual(
                    sorted(["SKILL.md", "agents/openai.yaml", next(item for item in [
                        "scripts/guard.py", "scripts/check_scope.py", "scripts/check_prepare.py"
                    ] if (root / item).exists()), "skill-contract.json"]),
                    sorted(item["path"] for item in manifest.value["files"]),
                )
                self.assertEqual("1.0.1", contract.value["version"])
                self.assertEqual(
                    b"policy:\n  allow_implicit_invocation: false\n",
                    (root / "agents/openai.yaml").read_bytes(),
                )

    def test_all_four_portable_cores_match_retained_phase3_vectors(self) -> None:
        vectors = json.loads(PHASE3_VECTORS.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-phase3-portable-vectors-v1", vectors["schema"])
        for name, expected in vectors["skills"].items():
            with self.subTest(skill=name):
                root = SKILLS_ROOT / name
                contract = load_skill_contract(root / "skill-contract.json")
                self.assertEqual(expected["schema"], contract.value["schema"])
                self.assertEqual(expected["manifest_sha256"], build_skill_manifest(root).sha256)
                self.assertEqual(
                    expected["contract_sha256"],
                    hashlib.sha256(canonical_json_bytes(contract.value)).hexdigest(),
                )

    def test_phase3_contracts_reject_implicit_activation_transitions_and_unknown_fields(self) -> None:
        original = json.loads(
            (PHASE3_ROOTS["harness-draft-change"] / "skill-contract.json").read_text(encoding="utf-8")
        )
        cases = (
            ("implicit", lambda value: value["activation"].__setitem__("implicit", True), "SKC023"),
            (
                "transition",
                lambda value: value["effects"]["lifecycle_transitions"].append("draft-to-approved"),
                "SKC027",
            ),
            ("authority", lambda value: value.__setitem__("authority", "engineering-owner"), "SKC006"),
            ("delegation", lambda value: value["delegation"].__setitem__("allowed", True), "SKC018"),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                value = json.loads(json.dumps(original))
                mutate(value)
                with self.assertRaisesRegex(SkillContractError, code):
                    parse_skill_contract_bytes(json.dumps(value).encode("utf-8"))

    def test_repository_host_surfaces_bind_one_canonical_core_per_name(self) -> None:
        vectors = json.loads(HOST_SURFACE_VECTORS.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-host-surface-vectors-v1", vectors["schema"])
        self.assertEqual(ALL_SKILL_NAMES, set(vectors["skills"]))
        self.assertEqual(
            ALL_SKILL_NAMES,
            {path.name for path in CLAUDE_SKILLS_ROOT.iterdir() if path.is_dir()},
        )
        for name, expected in sorted(vectors["skills"].items()):
            with self.subTest(skill=name):
                adapter = CLAUDE_SKILLS_ROOT / name / "SKILL.md"
                self.assertEqual(["SKILL.md"], [path.name for path in adapter.parent.iterdir()])
                raw = adapter.read_text(encoding="utf-8")
                front, body = raw.removeprefix("---\n").split("\n---\n", 1)
                self.assertIn(f"name: {name}\n", front + "\n")
                self.assertIn("adapter-schema: se-harness-host-adapter-v1", front)
                self.assertIn(f"canonical-name: {name}", front)
                self.assertIn(f"canonical-path: {expected['canonical_path']}", front)
                self.assertEqual(
                    expected["claude_disable_model_invocation"] is True,
                    "disable-model-invocation: true" in front,
                )
                self.assertIn("non-authoritative Claude Code discovery adapter", body)
                self.assertIn(f"${{CLAUDE_PROJECT_DIR}}/{expected['canonical_path']}", body)
                self.assertIn("Read the complete canonical `SKILL.md`", body)
                self.assertIn("yield entirely to the canonical procedure", body)
                for forbidden in (
                    "allowed-tools:", "disallowed-tools:", "model:", "context:",
                    "agent:", "hooks:", "http://", "https://", "$(`", "scripts/",
                ):
                    self.assertNotIn(forbidden, raw)

                canonical = PurePosixPath(f".agents/skills/{name}")
                self.assertFalse(canonical.is_absolute())
                self.assertNotIn("..", canonical.parts)
                contract = load_skill_contract(SKILLS_ROOT / name / "skill-contract.json")
                self.assertEqual(name, contract.name)
                policy = expected["codex_policy_path"]
                self.assertEqual(policy is not None, (SKILLS_ROOT / name / (policy or "agents/openai.yaml")).exists())

    def test_host_surfaces_fail_static_binding_checks_for_hostile_changes(self) -> None:
        source = (CLAUDE_SKILLS_ROOT / "harness-draft-change/SKILL.md").read_text(encoding="utf-8")
        attacks = {
            "wrong-schema": source.replace("se-harness-host-adapter-v1", "unknown-adapter"),
            "wrong-name": source.replace("canonical-name: harness-draft-change", "canonical-name: harness-orient"),
            "traversal": source.replace(
                ".agents/skills/harness-draft-change", "../.agents/skills/harness-draft-change"
            ),
            "absolute": source.replace(
                ".agents/skills/harness-draft-change", "/.agents/skills/harness-draft-change"
            ),
            "permission": source.replace("metadata:\n", "allowed-tools: Bash\nmetadata:\n"),
            "remote": source + "\nhttps://example.invalid/skill\n",
        }
        required = (
            "adapter-schema: se-harness-host-adapter-v1",
            "canonical-name: harness-draft-change",
            "canonical-path: .agents/skills/harness-draft-change",
            "disable-model-invocation: true",
        )
        forbidden = ("allowed-tools:", "http://", "https://", "../", "canonical-path: /")
        for label, raw in attacks.items():
            with self.subTest(attack=label):
                self.assertTrue(any(item not in raw for item in required) or any(item in raw for item in forbidden))


class Phase3EffectGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.draft = load_script(
            "phase3_draft_guard", PHASE3_ROOTS["harness-draft-change"] / "scripts/guard.py"
        )
        cls.execute = load_script(
            "phase3_execute_guard", PHASE3_ROOTS["harness-execute-work-order"] / "scripts/check_scope.py"
        )
        cls.assurance = load_script(
            "phase3_assurance_guard", PHASE3_ROOTS["harness-prepare-assurance"] / "scripts/check_prepare.py"
        )

    def test_draft_guard_invokes_effect_once_only_after_fresh_closed_plan(self) -> None:
        request = {
            "explicit_skill": "harness-draft-change",
            "effect_class": "draft-create",
            "planned_paths": ["docs/engineering/example/requirements/REQ-EX-001.md"],
            "allowed_paths": ["docs/engineering/example/requirements/REQ-EX-001.md"],
            "revisions": {},
        }
        calls: list[tuple[str, ...]] = []
        result = self.draft.admit_draft_effect(
            request,
            recheck=lambda: {"allowed_paths": request["allowed_paths"], "revisions": {}},
            effect=lambda paths: calls.append(paths) or "done",
        )
        self.assertEqual("done", result)
        self.assertEqual([tuple(request["planned_paths"])], calls)

        for label, mutate in (
            ("implicit", lambda value: value.__setitem__("explicit_skill", "")),
            ("escape", lambda value: value.__setitem__("planned_paths", ["../outside.md"])),
            ("scope", lambda value: value.__setitem__("planned_paths", ["README.md"])),
            ("state", lambda value: value.__setitem__("revisions", {"REQ-EX-001": "approved"})),
        ):
            with self.subTest(label=label):
                rejected = json.loads(json.dumps(request))
                mutate(rejected)
                calls.clear()
                with self.assertRaises(self.draft.DraftGuardError):
                    self.draft.admit_draft_effect(
                        rejected,
                        recheck=lambda: {"allowed_paths": rejected["allowed_paths"], "revisions": rejected["revisions"]},
                        effect=lambda paths: calls.append(paths),
                    )
                self.assertEqual([], calls)

    def test_work_order_state_matrix_and_path_attacks_fail_before_effect(self) -> None:
        base = {
            "explicit_skill": "harness-execute-work-order",
            "work_order": "WO-AEX-003",
            "state": "in_progress",
            "effect_class": "implementation-write",
            "planned_paths": ["se_harness/skill_contract.py"],
            "execution_scope": ["se_harness/skill_contract.py", "tests/fixtures/agentic_execution/phase3/"],
        }
        scope = self.execute._paths(base["execution_scope"], allow_prefix=True)
        fresh = {
            "work_order": "WO-AEX-003",
            "state": "in_progress",
            "scope_sha256": self.execute.scope_digest(scope),
        }
        calls: list[tuple[str, ...]] = []
        self.execute.admit_work_order_effect(base, recheck=lambda: fresh, effect=lambda paths: calls.append(paths))
        self.assertEqual(1, len(calls))

        for state in ("draft", "approved", "implemented", "verified", "rejected"):
            rejected = {**base, "state": state}
            calls.clear()
            with self.subTest(state=state), self.assertRaises(self.execute.ScopeGuardError):
                self.execute.admit_work_order_effect(rejected, recheck=lambda: fresh, effect=lambda paths: calls.append(paths))
            self.assertEqual([], calls)
        for hostile in ("../escape.py", "/absolute.py", "file://host/path", "tests/*.py", "Tests/case.py"):
            rejected = {**base, "planned_paths": [hostile]}
            calls.clear()
            with self.subTest(path=hostile), self.assertRaises(self.execute.ScopeGuardError):
                self.execute.admit_work_order_effect(rejected, recheck=lambda: fresh, effect=lambda paths: calls.append(paths))
            self.assertEqual([], calls)

    def test_assurance_guard_requires_exact_candidate_actor_and_unused_record(self) -> None:
        request = {
            "explicit_skill": "harness-prepare-assurance",
            "record_id": "VREC-AEX-003",
            "record_destination": "docs/engineering/agentic-execution/verification-records/VREC-AEX-003.md",
            "candidate_commit": "a" * 40,
            "candidate_ready": True,
            "record_exists": False,
            "preparation_actor": "engineering-owner",
        }
        fresh = {
            key: request[key]
            for key in ("candidate_commit", "candidate_ready", "record_exists", "record_id", "record_destination")
        }
        calls: list[str] = []
        self.assurance.admit_assurance_preparation(
            request, recheck=lambda: fresh, effect=lambda path: calls.append(path)
        )
        self.assertEqual([request["record_destination"]], calls)

        for label, change in (
            ("actor", {"preparation_actor": ""}),
            ("dirty", {"candidate_ready": False}),
            ("collision", {"record_exists": True}),
            ("implicit", {"explicit_skill": ""}),
        ):
            rejected = {**request, **change}
            calls.clear()
            with self.subTest(label=label), self.assertRaises(self.assurance.AssuranceGuardError):
                self.assurance.admit_assurance_preparation(
                    rejected, recheck=lambda: fresh, effect=lambda path: calls.append(path)
                )
            self.assertEqual([], calls)

    def test_canonical_json_is_stable_and_rejects_floats(self) -> None:
        self.assertEqual(b'{"a":1,"z":[true,null]}\n', canonical_json_bytes({"z": [True, None], "a": 1}))
        with self.assertRaisesRegex(SkillContractError, "SKC003"):
            canonical_json_bytes({"not_allowed": 1.25})

    def test_independent_canonical_receipt_vector_matches_exact_bytes_and_digest(self) -> None:
        vector = json.loads(VECTORS.read_text(encoding="utf-8"))["receipt"]
        encoded = canonical_json_bytes(vector["value"])
        self.assertEqual(vector["canonical"].encode("utf-8"), encoded)
        self.assertEqual(vector["sha256"], hashlib.sha256(encoded).hexdigest())

    def test_manifest_normalizes_line_endings_and_detects_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            shutil.copytree(SKILL_ROOT, first)
            shutil.copytree(SKILL_ROOT, second)
            for path in second.rglob("*"):
                if path.is_file():
                    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))

            baseline = build_skill_manifest(first)
            self.assertEqual(baseline.sha256, build_skill_manifest(second).sha256)
            (second / "SKILL.md").write_bytes((second / "SKILL.md").read_bytes() + b"changed\r\n")
            self.assertNotEqual(baseline.sha256, build_skill_manifest(second).sha256)

    def test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "SKILL.md").unlink()
            with self.assertRaisesRegex(SkillContractError, "SKM008"):
                build_skill_manifest(root)

            shutil.copy2(SKILL_ROOT / "SKILL.md", root / "SKILL.md")
            invalid = root / "invalid.txt"
            invalid.write_bytes(b"\xff")
            with self.assertRaisesRegex(SkillContractError, "SKM007"):
                build_skill_manifest(root)
            invalid.unlink()

            reserved = root / "NUL.txt"
            try:
                reserved.write_text("reserved\n", encoding="utf-8")
            except OSError:
                pass
            else:
                with self.assertRaisesRegex(SkillContractError, "SKM003"):
                    build_skill_manifest(root)

    @unittest.skipIf(os.name == "nt", "creating an unprivileged symlink is not portable on Windows")
    def test_manifest_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "linked").symlink_to(root / "SKILL.md")
            with self.assertRaisesRegex(SkillContractError, "SKM005"):
                build_skill_manifest(root)

    @unittest.skipIf(os.name == "nt", "Windows cannot create the hostile portable names")
    def test_manifest_rejects_case_collisions_and_alternate_separators(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "skill"
            shutil.copytree(SKILL_ROOT, root)
            (root / "Case.txt").write_text("one\n", encoding="utf-8")
            (root / "case.txt").write_text("two\n", encoding="utf-8")
            with self.assertRaisesRegex(SkillContractError, "SKM004"):
                build_skill_manifest(root)
            (root / "Case.txt").unlink()
            (root / "case.txt").unlink()
            (root / "alternate\\separator.txt").write_text("unsafe\n", encoding="utf-8")
            with self.assertRaisesRegex(SkillContractError, "SKM003"):
                build_skill_manifest(root)


class HarnessOrientBlackBoxTests(unittest.TestCase):
    def invoke(
        self,
        target: Path,
        *,
        mode: str = "healthy",
        version: str = "0.6.0",
        artifact: str | None = None,
        preflight_phase: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        launcher = json.dumps([sys.executable, "-B", str(FAKE_EVALUATOR)])
        command = [
            sys.executable,
            "-B",
            str(ORIENT),
            str(target),
            "--evaluator-launcher-json",
            launcher,
            "--expected-evaluator-version",
            version,
            "--expected-evaluator-root",
            str(Path(sys.prefix)),
        ]
        if artifact is not None:
            command.extend(["--artifact", artifact])
        if preflight_phase is not None:
            command.extend(["--preflight-phase", preflight_phase])
        environment = os.environ.copy()
        environment["AEX_FAKE_MODE"] = mode
        environment["AEX_FAKE_VERSION"] = version
        return subprocess.run(command, capture_output=True, text=True, check=False, env=environment)

    def make_target(self, parent: Path) -> Path:
        target = parent / "repository"
        (target / ".git/refs/heads").mkdir(parents=True)
        (target / ".git/HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (target / ".git/refs/heads/main").write_text("a" * 40 + "\n", encoding="utf-8")
        (target / "README.md").write_text("fixture\n", encoding="utf-8")
        return target

    def test_healthy_selected_orientation_is_deterministic_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            first = self.invoke(target, artifact="WO-TST-001")
            after = snapshot(target)

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(before, after)
            result = json.loads(first.stdout)
            self.assertEqual("completed", result["outcome"])
            self.assertEqual("in_progress", result["selected"]["lifecycle_state"])
            self.assertEqual("fixture-repository", result["repository"]["name"])
            receipt = result["execution_receipt"]
            self.assertEqual([], receipt["effects"]["changed_paths"])
            self.assertEqual(receipt["effects"]["state_before"], receipt["effects"]["state_after"])
            self.assertEqual(["single-agent-orientation"], receipt["execution"]["profiles"])
            self.assertEqual([], receipt["execution"]["worker_results"])
            self.assertEqual(
                hashlib.sha256(canonical_json_bytes(receipt)).hexdigest(),
                result["execution_receipt_sha256"],
            )

    def test_candidate_source_content_and_repository_secret_are_not_governing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            (target / "se_harness").mkdir()
            (target / "se_harness/__init__.py").write_text('__version__ = "999.0.0"\n', encoding="utf-8")
            (target / "private.txt").write_text("credential=do-not-expose\n", encoding="utf-8")
            completed = self.invoke(target)

            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertNotIn("999.0.0", completed.stdout)
            self.assertNotIn("do-not-expose", completed.stdout)
            result = json.loads(completed.stdout)
            self.assertEqual({"governing": False, "status": "not_assessed"}, result["candidate_source"])
            self.assertEqual("0.6.0", result["released_evaluator"]["version"])

    def test_exact_0_5_without_focus_degrades_only_selected_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="no-focus", version="0.5.0", artifact="WO-TST-001")

            self.assertEqual(0, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual("degraded", result["outcome"])
            self.assertEqual("not_assessable", result["selected"]["status"])
            self.assertEqual("passed", result["integrity"]["outcome"])
            self.assertTrue(result["validation"]["valid"])
            operation_ids = [item["id"] for item in result["execution_receipt"]["execution"]["operations"]]
            self.assertNotIn("focus-json", operation_ids)
            self.assertIn(
                {"code": "AEXORI030", "operation": "focus-json", "status": "not_assessable"},
                result["execution_receipt"]["validation"]["deviations"],
            )

    def test_required_identity_failure_blocks_before_integrity_and_preserves_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            completed = self.invoke(target, mode="identity-fail")

            self.assertEqual(2, completed.returncode)
            self.assertEqual(before, snapshot(target))
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertEqual(
                ["version", "identity"],
                [item["id"] for item in result["execution_receipt"]["execution"]["operations"]],
            )

    def test_invalid_graph_blocks_before_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="invalid-graph")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertFalse(result["validation"]["valid"])
            operation_ids = [item["id"] for item in result["execution_receipt"]["execution"]["operations"]]
            self.assertIn("validate-json", operation_ids)
            self.assertNotIn("inspect-json", operation_ids)

    def test_malformed_required_json_fails_and_large_output_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            malformed = self.invoke(target, mode="malformed-validation")
            self.assertEqual(2, malformed.returncode)
            malformed_result = json.loads(malformed.stdout)
            self.assertEqual("failed", malformed_result["outcome"])
            self.assertIn("AEXORI021", malformed.stdout)

            large = self.invoke(target, mode="large-output")
            self.assertEqual(2, large.returncode)
            large_result = json.loads(large.stdout)
            self.assertEqual("blocked", large_result["outcome"])
            self.assertLess(len(large.stdout), 50_000)

    def test_managed_integrity_diagnostic_redacts_secret_and_host_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, mode="doctor-fail")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            rendered = json.dumps(result, sort_keys=True)
            self.assertNotIn("top-secret", rendered)
            self.assertNotIn(str(target), rendered)
            self.assertIn("secret=<redacted>", rendered)

    def test_preflight_is_explicit_and_cannot_be_rendered_as_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(
                target,
                mode="preflight-blocked",
                artifact="WO-TST-001",
                preflight_phase="review",
            )

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual("blocked", result["outcome"])
            self.assertFalse(result["preflight"]["ready"])
            self.assertNotIn("approved", completed.stdout.lower())

    def test_preflight_rejects_non_work_order_selection_without_running_evaluator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            completed = self.invoke(target, artifact="REQ-TST-001", preflight_phase="start")

            self.assertEqual(2, completed.returncode)
            result = json.loads(completed.stdout)
            self.assertEqual([], result["execution_receipt"]["execution"]["operations"])
            self.assertEqual("blocked", result["outcome"])

    def test_unsupported_old_evaluator_and_missing_launcher_block_without_target_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_target(Path(temporary))
            before = snapshot(target)
            old = self.invoke(target, version="0.4.9")
            self.assertEqual(2, old.returncode)
            self.assertEqual([], json.loads(old.stdout)["execution_receipt"]["execution"]["operations"])

            command = [
                sys.executable,
                "-B",
                str(ORIENT),
                str(target),
                "--evaluator-launcher-json",
                json.dumps([str(Path(temporary) / "missing-evaluator")]),
                "--expected-evaluator-version",
                "0.6.0",
                "--expected-evaluator-root",
                str(Path(temporary) / "missing-root"),
            ]
            missing = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(2, missing.returncode)
            self.assertEqual("blocked", json.loads(missing.stdout)["outcome"])
            self.assertEqual(before, snapshot(target))


if __name__ == "__main__":
    unittest.main()
