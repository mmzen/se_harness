"""Real released-0.17 census for the approved OWN07 compatibility boundary.

The caller supplies the existing independent ownership fixture. No released
authority guard is mocked. A known protected-path failure remains a failure.
"""
import base64
import importlib.util
import json
import os
from pathlib import Path
import subprocess


ARTIFACT_TYPES = {
    "intent": "INT", "capability": "CAP", "requirement": "REQ", "specification": "SPEC",
    "architecture": "ARCH", "adr": "ADR", "verification": "VER", "work_order": "WO",
    "verification_record": "VREC", "release_contract": "REL", "release_record": "RLS",
    "operating_contract": "OPS", "decision": "DEC", "risk": "RISK",
}
PUBLIC_COMMANDS = {
    "init", "validate", "inspect", "dashboard", "doctor", "preflight", "check", "evidence", "pr-body",
    "transition", "decide", "raise-risk", "risks", "select-work-order", "upgrade", "scaffold-domain",
    "create-artifact", "release-unit", "identity", "qualify", "capture-verification", "prepare-release",
}


class LegacyReaderCases:
    def _legacy_command(self, arguments, *, module=True, environment=None):
        legacy = os.environ.get("SE_HARNESS_OWNERSHIP_LEGACY_PYTHON")
        if not legacy:
            self.skipTest("actual released 0.17.0 interpreter not supplied; expanded old-reader observation unavailable")
        before = self._legacy_snapshot(self.base)
        before_bytes = {path: (self.base / path).read_bytes() for path, entry in before.items() if entry["kind"] == "file"}
        command = [legacy, "-I", "-B", *(["-m", "se_harness"] if module else []), *map(str, arguments)]
        result = subprocess.run(command, cwd=self.base, env=environment, capture_output=True, timeout=120)
        after = self._legacy_snapshot(self.base)
        changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
        event = {"operation": "released-0.17-expanded-census", "arguments": command,
                 "exit_status": result.returncode, "stdout": result.stdout.decode(errors="replace"),
                 "stderr": result.stderr.decode(errors="replace"), "before": before, "after": after,
                 "changed_destinations": changed,
                 "changed_bytes": {path: {
                     "before_base64": base64.b64encode(before_bytes[path]).decode() if path in before_bytes else None,
                     "after_base64": base64.b64encode((self.base / path).read_bytes()).decode() if after.get(path, {}).get("kind") == "file" else None,
                 } for path in changed}}
        self.events.append(event)
        self.assertNotIn("unrecognized arguments", event["stderr"])
        return event

    def _legacy_write_artifact(self, folder, identifier, kind, relations, extra="", status="draft"):
        support = self._legacy_artifact_support()
        return support.write(self.root / "docs/engineering/legacy-probe" / folder / (identifier + ".md"),
                             support.formal(identifier, kind, status, relations, extra, complete=True))

    def _legacy_artifact_support(self):
        spec = importlib.util.spec_from_file_location("ownership_legacy_artifacts", self._legacy_source_root / "tests/artifact_support.py")
        support = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(support)
        return support

    def _legacy_validate(self):
        event = self._legacy_command(["validate", self.root, "--json"])
        self.assertEqual(0, event["exit_status"], event["stderr"])
        graph = json.loads(event["stdout"])
        self.assertTrue(graph["valid"])
        self.assertEqual([], graph["errors"])
        self.assertEqual([], event["changed_destinations"])

    def _prepare_legacy_census(self):
        version = self._legacy_command(["--version"])
        self.assertEqual(0, version["exit_status"])
        self.assertEqual("0.17.0", version["stdout"].strip())
        for folder, identifier, kind, relations in (
            ("intent", "INT-LEG-001", "intent", {}),
            ("capabilities", "CAP-LEG-001", "capability", {"derives_from": ["INT-LEG-001"]}),
            ("requirements", "REQ-LEG-001", "requirement", {"derives_from": ["CAP-LEG-001"]}),
            ("specifications", "SPEC-LEG-001", "specification", {"specifies": ["REQ-LEG-001"]}),
            ("verification", "VER-LEG-001", "verification", {"verifies": ["REQ-LEG-001"]}),
            ("work-orders", "WO-LEG-001", "work_order", {"implements": ["REQ-LEG-001"], "specifications": ["SPEC-LEG-001"], "verification": ["VER-LEG-001"]}),
        ):
            extra = '[execution_scope]\npaths = ["src/probe.py"]' if kind == "work_order" else ""
            self._legacy_write_artifact(folder, identifier, kind, relations, extra)
        (self.root / ".agents/skills/harness-orient/owner-note.txt").write_bytes(b"Independent owner content preserves this parent.\n")
        self.migrate()
        from se_harness.preflight import inspect_installation
        self.assertTrue(all(check.passed for check in inspect_installation(self.root)))
        self._legacy_validate()

    def _assert_legacy_protected_refusal(self, arguments):
        event = self._legacy_command(arguments)
        self.assertEqual([], event["changed_destinations"])
        self.assertNotEqual(0, event["exit_status"])
        self.assertIn("unsupported lock schema", (event["stdout"] + event["stderr"]).lower())

    def test_own07_released_017_protected_authoring_interfaces(self):
        self._prepare_legacy_census()
        census = self._legacy_command(["-c", (
            "import json; from se_harness.cli import build_parser; "
            "from se_harness.artifact_layout import ARTIFACT_PREFIXES; "
            "from se_harness.mutation_guard import PUBLIC_MUTATION_OPERATIONS; "
            "p=build_parser(); a=next(a for a in p._actions if getattr(a,'choices',None)); "
            "print(json.dumps({'commands': sorted(a.choices), 'artifact_types': ARTIFACT_PREFIXES, "
            "'guarded_operations': sorted(PUBLIC_MUTATION_OPERATIONS)}))"
        )], module=False)
        self.assertEqual(0, census["exit_status"], census["stderr"])
        census = json.loads(census["stdout"])
        self.assertEqual(PUBLIC_COMMANDS, set(census["commands"]))
        self.assertEqual({kind: prefix + "-" for kind, prefix in ARTIFACT_TYPES.items()}, census["artifact_types"])
        commands = [["init", self.root, "--json"], ["upgrade", self.root, "--apply", "--json"],
                    ["upgrade", self.root, "--apply", "--evidence-output", "docs/engineering/legacy-probe/evidence/upgrade-observation.json", "--json"],
                    ["scaffold-domain", self.root, "--domain", "legacy-new", "--json"]]
        commands += [["create-artifact", self.root, "--domain", "legacy-probe", "--type", kind,
                      "--id", prefix + "-LEG-099", "--json"] for kind, prefix in ARTIFACT_TYPES.items()]
        risk = ["raise-risk", self.root, "--domain", "legacy-probe", "--title", "Compatibility fixture risk",
                "--stage", "implementation", "--category", "quality", "--cause", "The fixture input changes.",
                "--effect", "The fixture observation becomes invalid.", "--likelihood", "1", "--impact", "1",
                "--threatens", "WO-LEG-001", "--raised-by", "fixture-owner", "--id", "RISK-LEG-099", "--json"]
        commands += [risk, risk + ["--with-decision", "--decision-id", "DEC-LEG-099"]]
        capture = ["capture-verification", self.root, "--id", "VREC-LEG-099", "--work-order", "WO-LEG-001",
                   "--verification", "VER-LEG-001", "--evidence", "docs/engineering/legacy-probe/verification/VER-LEG-001.md", "--json"]
        release = ["prepare-release", self.root, "--id", "RLS-LEG-099", "--release-contract", "REL-LEG-099",
                   "--verification-record", "VREC-LEG-099", "--work-order", "WO-LEG-001", "--version", "0.18.0",
                   "--owner", "release-owner", "--json"]
        commands += [capture, capture + ["--owner", "delegated-executor"], capture + ["--domain", "legacy-probe"],
                     capture + ["--output", "docs/engineering/legacy-probe/verification-records/VREC-LEG-099.md"],
                     release, release + ["--domain", "legacy-probe"],
                     release + ["--output", "docs/engineering/legacy-probe/releases/RLS-LEG-099.md"]]
        for arguments in commands:
            with self.subTest(arguments=list(map(str, arguments))):
                self._assert_legacy_protected_refusal(arguments)

    def test_own07_released_017_ordinary_transitions_and_decisions(self):
        self._prepare_legacy_census()
        self._legacy_write_artifact("intent", "INT-LEG-901", "intent", {})
        self._legacy_write_artifact("decisions", "DEC-LEG-901", "decision",
                                    {"concerns": ["REQ-LEG-001"], "blocks": ["REQ-LEG-001"]},
                                    'kind = "question"\nquestion = "Which fixture option applies?"\nraised_by = "fixture-author"\n'
                                    'recommendation = "first"\n[[options]]\nid = "first"\nlabel = "First fixture option"\n'
                                    '[[options]]\nid = "second"\nlabel = "Second fixture option"', status="open")
        self._legacy_validate()
        commands = [["transition", self.root, "--set", "INT-LEG-901=rejected", "--decision", "INT-LEG-901=technical-owner",
                     "--reason", "INT-LEG-901=Disposable compatibility probe", "--apply", "--json"]]
        decision = ["decide", self.root, "--artifact", "DEC-LEG-901", "--decision", "technical-owner",
                    "--reason", "Disposable compatibility probe", "--apply", "--json"]
        commands += [decision + mode for mode in (["--option", "first"], ["--defer", "--scope", "REQ-LEG-001:draft-approved",
                                                                "--revisit", "2026-12-01"], ["--withdraw"])]
        for arguments in commands:
            with self.subTest(arguments=list(map(str, arguments))):
                self._assert_legacy_protected_refusal(arguments)

    def test_own07_released_017_default_reports_preserve_protected_bytes(self):
        self._prepare_legacy_census()
        evidence = "repository/docs/engineering/legacy-probe/evidence"
        commands = [(["evidence", self.root, "--artifact", "WO-LEG-001", "--checkpoint", checkpoint,
                      "--rebound-at", "2026-09-12T18:00:00Z", "--json"], evidence, 0)
                    for checkpoint in ("start", "pre-action", "transition", "handoff")]
        commands += [(["dashboard", self.root, "--json"], "repository/target", 0),
                     (["dashboard", self.root, "--output", "target/legacy-report", "--json"], "repository/target", 0),
                     (["qualify", "released-root", self.root, "--output", self.base / "legacy-qualification.json", "--json"],
                      "legacy-qualification.json", 1)]
        for arguments, permitted, expected_status in commands:
            with self.subTest(arguments=list(map(str, arguments))):
                event = self._legacy_command(arguments)
                self.assertEqual(expected_status, event["exit_status"], event["stderr"])
                self.assertTrue(event["changed_destinations"], "report output was not observed")
                for path in event["changed_destinations"]:
                    self.assertTrue(path == permitted or path.startswith(permitted + "/"), path)

    def _legacy_delegation_fixture(self, status):
        self._prepare_legacy_census()
        self._legacy_artifact_support().create_base_chain(
            self.root, work_order_status=status, operating_contract_status="draft")
        original = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order = original.with_name("WO-PRD-001.md")
        original.rename(work_order)
        for artifact in (self.root / "docs/engineering/product").rglob("*.md"):
            content = artifact.read_text(encoding="utf-8")
            if "WO-001" in content:
                artifact.write_text(content.replace("WO-001", "WO-PRD-001"), encoding="utf-8", newline="\n")
        content = work_order.read_text(encoding="utf-8")
        content = content.replace("[relations]", '[assurance]\ncommit_bound_verification = "required"\n'
                                  'rationale = "Synthetic fixture requires exact-candidate assurance."\n'
                                  'decided_by = "engineering-owner"\n[execution_scope]\npaths = ["src/"]\n'
                                  '[delegation]\nclass = "execution"\n\n[relations]', 1)
        work_order.write_text(content, encoding="utf-8", newline="\n")
        (self.root / ".engineering-harness.delegation.toml").write_text(
            '[delegation]\ngate_source = "local-file"\ncheck_name = "validate"\n'
            'base_ref = "main"\nlocal_file = "gate.json"\n', encoding="utf-8", newline="\n")
        with (self.root / ".gitignore").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write("\ngate.json\n.engineering-harness.delegation.toml\n*.log\n")
        commands = [("init", "-q", "-b", "main"), ("config", "user.email", "fixture@example.invalid"),
                    ("config", "user.name", "Disposable Fixture"), ("config", "core.autocrlf", "false"),
                    ("config", "gc.auto", "0"), ("config", "maintenance.auto", "false"), ("add", "-A"),
                    ("commit", "-q", "-m", "Synthetic delegated fixture baseline"),
                    ("checkout", "-q", "-b", "wo/fixture"), ("rev-parse", "HEAD")]
        for arguments in commands:
            command = ["git", "-C", str(self.root), *arguments]
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            self.events.append({"operation": "synthetic-delegation-fixture-setup", "arguments": command,
                                "exit_status": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
            self.assertEqual(0, result.returncode, result.stderr)
        (self.root / "gate.json").write_text(json.dumps({"sha": result.stdout.strip(),
            "conclusion": "success", "check_run_id": "4242"}), encoding="utf-8")
        self._legacy_validate()

    def _assert_legacy_delegated_refusal(self, status, target, operation):
        self._legacy_delegation_fixture(status)
        event = self._legacy_command(["transition", self.root, "--set", "WO-PRD-001=" + target,
                                      "--decision", "WO-PRD-001=delegated-executor", "--apply", "--json"],
                                     environment=dict(os.environ, SE_HARNESS_REHEARSAL="1"))
        event["fixture_authority"] = "Synthetic local-file gate; actual released guard, no authority mock."
        event["explicit_environment"] = {"SE_HARNESS_REHEARSAL": "1"}
        self.assertEqual([], event["changed_destinations"])
        self.assertEqual(2, event["exit_status"])
        self.assertIn("MG001 (" + operation + ")", event["stderr"])
        self.assertIn("unsupported lock schema", event["stderr"])

    def test_own07_released_017_delegated_start(self):
        self._assert_legacy_delegated_refusal("approved", "in_progress", "delegated-work-order-start")

    def test_own07_released_017_delegated_completion(self):
        self._assert_legacy_delegated_refusal("in_progress", "implemented", "delegated-work-order-complete")

    def test_own07_released_017_retained_check_output_preserves_protected_bytes(self):
        self._prepare_legacy_census()
        for arguments in (("init", "-q", "-b", "main"), ("config", "user.email", "fixture@example.invalid"),
                          ("config", "user.name", "Disposable Fixture"), ("config", "core.autocrlf", "false"),
                          ("config", "gc.auto", "0"), ("config", "maintenance.auto", "false"),
                          ("add", "-A"), ("commit", "-q", "-m", "Synthetic retained-check fixture")):
            command = ["git", "-C", str(self.root), *arguments]
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            self.events.append({"operation": "synthetic-retained-check-fixture-setup", "arguments": command,
                                "exit_status": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
            self.assertEqual(0, result.returncode, result.stderr)
        event = self._legacy_command(["evidence", self.root, "--artifact", "WO-LEG-001", "--checkpoint", "handoff",
                                      "--rebound-at", "2026-09-12T18:00:00Z", "--json"])
        self.assertEqual(0, event["exit_status"], event["stderr"])
        work_order = self.root / "docs/engineering/legacy-probe/work-orders/WO-LEG-001.md"
        work_order.write_bytes(work_order.read_bytes() + b"\n<!-- Synthetic body change for handoff rebind observation. -->\n")
        self._legacy_validate()
        for attempt in range(2):
            with self.subTest(attempt=attempt):
                event = self._legacy_command(["check", self.root, "--artifact", "WO-LEG-001", "--checkpoint", "handoff",
                                              "--from-git", "HEAD", "--json"])
                self.assertEqual(0, event["exit_status"], event["stderr"])
                self.assertEqual("completed", json.loads(event["stdout"])["operation"]["outcome"])
                self.assertTrue(event["changed_destinations"])
                for path in event["changed_destinations"]:
                    self.assertTrue(path.startswith("repository/docs/engineering/legacy-probe/evidence/WO-LEG-001/"), path)
                self.assertTrue((self.root / "docs/engineering/legacy-probe/evidence/WO-LEG-001/handoff.json").is_file())

    def test_own07_released_017_qualification_output_cannot_recreate_retired_core(self):
        self._prepare_legacy_census()
        target = self.root / ".agents/skills/harness-orient/SKILL.md"
        self.assertFalse(target.exists())
        self.assertTrue(target.parent.is_dir())
        event = self._legacy_command(["qualify", "released-root", self.root, "--output", target, "--json"])
        self.assertEqual([], event["changed_destinations"], "legacy qualification output changed a protected installation path")
        self.assertNotEqual(0, event["exit_status"])

    def test_own07_released_017_dashboard_output_cannot_replace_installed_workflow(self):
        self._prepare_legacy_census()
        self.assertTrue((self.root / ".github/workflows/engineering-harness.yml").is_file())
        event = self._legacy_command(["dashboard", self.root, "--output", ".github", "--json"])
        self.assertEqual([], event["changed_destinations"], "legacy dashboard output changed protected installation bytes")
        self.assertNotEqual(0, event["exit_status"])
