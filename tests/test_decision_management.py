"""Evidence for REQ-DCM-001 through REQ-DCM-003 (WO-DCM-001): the governed decision artifact."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.artifact_layout import ARTIFACT_DIRECTORIES, ARTIFACT_PREFIXES
from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, formal, write


def decision_text(
    decision_id: str,
    *,
    kind: str = "question",
    options: tuple[tuple[str, str], ...] = (("keep", "Keep the current shape."), ("split", "Split the record in two.")),
    recommendation: str = "keep",
    concerns: tuple[str, ...] = ("WO-001",),
    blocks: tuple[str, ...] = ("WO-001",),
    against: str | None = None,
    observed: str | None = None,
    status: str = "open",
    extra: str = "",
) -> str:
    scalars = [
        f'kind = "{kind}"',
        'question = "Which shape does the record take?"',
        'raised_by = "coding-agent"',
        f'recommendation = "{recommendation}"',
    ]
    if against is not None:
        scalars.append(f'against = "{against}"')
    if observed is not None:
        scalars.append(f'observed = "{observed}"')
    if extra:
        scalars.append(extra)
    tables = "\n\n".join(f'[[options]]\nid = "{option_id}"\nlabel = "{label}"' for option_id, label in options)
    return formal(
        decision_id,
        "decision",
        status,
        {"concerns": list(concerns), "blocks": list(blocks)},
        "\n".join(scalars) + "\n\n" + tables,
    )


class DecisionManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Decision Fixture")
        self.assertEqual(0, code, error)
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        guard.start()
        self.addCleanup(guard.stop)
        create_base_chain(self.root, operating_contract_status="draft")

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def in_progress_work_order(self) -> Path:
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace('status = "implemented"', 'status = "in_progress"', 1)
        text = text.replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\n'
            'rationale = "Decision fixture."\ndecided_by = "repository-owner"\n\n'
            '[execution_scope]\npaths = ["src/"]\n\n[relations]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        return path

    def decision_path(self, decision_id: str = "DEC-001") -> Path:
        return self.root / f"docs/engineering/product/decisions/{decision_id}.md"

    def raise_decision(self, decision_id: str = "DEC-001", **fields) -> Path:
        path = self.decision_path(decision_id)
        write(path, decision_text(decision_id, **fields))
        return path

    def validate(self):
        validator = _load_validator_module()
        return validator.validate_repository(self.root)

    def decision_errors(self) -> list[str]:
        return sorted(f"{item.code}: {item.message}" for item in self.validate().errors if item.code.startswith("E-DCM"))

    def handoff_check(self) -> dict:
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--changed-path", "src/main.py", "--changes-complete", "--json",
        )
        self.assertIn(code, (0, 1), error)
        return json.loads(output)

    @staticmethod
    def predicates(result: dict) -> dict:
        return {p["id"]: p for gate in result["compliance"]["gates"] for p in gate["predicates"]}

    # ---------------------------------------------------------------- REQ-DCM-001: the artifact and its validation

    def test_layout_registry_and_template_route_the_decision_type(self) -> None:
        self.assertEqual(("decisions",), ARTIFACT_DIRECTORIES["decision"])
        self.assertEqual("DEC-", ARTIFACT_PREFIXES["decision"])
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "decision", "--id", "DEC-PRD-001",
        )
        self.assertEqual(0, code, error + output)
        text = self.decision_path("DEC-PRD-001").read_text(encoding="utf-8")
        self.assertIn('type = "decision"', text)
        self.assertIn('status = "open"', text)
        self.assertIn("[[options]]", text)
        self.assertIn("## Disposition", text)
        self.assertIn("harnessctl decide", text)

    def test_a_well_formed_decision_validates_and_the_validator_names_each_defect(self) -> None:
        self.raise_decision()
        self.assertEqual([], self.decision_errors())
        path = self.decision_path()
        original = path.read_text(encoding="utf-8")

        path.write_text(original.replace('kind = "question"', 'kind = "hunch"'), encoding="utf-8")
        self.assertTrue(any(item.startswith("E-DCM-002") and "question or deviation" in item for item in self.decision_errors()))

        one_option = original.split("[[options]]", 2)
        path.write_text(one_option[0] + "[[options]]" + one_option[1] + "[relations]" + original.split("[relations]", 1)[1], encoding="utf-8")
        self.assertTrue(any("at least two options" in item for item in self.decision_errors()))

        path.write_text(original.replace('recommendation = "keep"', 'recommendation = "burn"'), encoding="utf-8")
        self.assertTrue(any("not a declared option" in item for item in self.decision_errors()))

        path.write_text(original.replace('concerns = ["WO-001"]', 'concerns = ["REQ-001"]'), encoding="utf-8")
        self.assertTrue(any(item.startswith("E-DCM-001") and "not also in concerns" in item for item in self.decision_errors()))

        path.write_text(original.replace('blocks = ["WO-001"]', 'blocks = []'), encoding="utf-8")
        self.assertTrue(any(item.startswith("E-DCM-001") and "blocks at least one artifact" in item for item in self.decision_errors()))

        hand_written = original.replace("[relations]", '[disposition]\noption = "keep"\nlabel = "x"\ndecided_by = "owner"\ndecided_at = "2026-08-12T00:00:00Z"\nreason = "typed by hand"\n\n[relations]')
        path.write_text(hand_written, encoding="utf-8")
        self.assertTrue(any(item.startswith("E-DCM-003") and "open decision carries no disposition" in item for item in self.decision_errors()))

        path.write_text(original.replace('status = "open"', 'status = "decided"'), encoding="utf-8")
        self.assertTrue(any(item.startswith("E-DCM-003") and "carries a [disposition] table" in item for item in self.decision_errors()))

    def test_a_deviation_names_the_rule_the_fact_and_the_closed_option_set(self) -> None:
        deviation = dict(
            kind="deviation",
            against="SPEC-001#rule-3",
            observed="The evaluator cannot read the field on Windows.",
            options=(("amend", "Amend rule 3."), ("accept", "Accept the deviation."), ("stop", "Stop the work.")),
            recommendation="accept",
            concerns=("SPEC-001", "WO-001"),
            blocks=("WO-001",),
        )
        self.raise_decision(**deviation)
        self.assertEqual([], self.decision_errors())
        path = self.decision_path()
        original = path.read_text(encoding="utf-8")

        path.write_text(original.replace('against = "SPEC-001#rule-3"\n', ""), encoding="utf-8")
        self.assertTrue(any("names the departed rule" in item for item in self.decision_errors()))
        path.write_text(original.replace("SPEC-001#rule-3", "SPEC-404#rule-3"), encoding="utf-8")
        self.assertTrue(any("unknown artifact 'SPEC-404'" in item for item in self.decision_errors()))
        path.write_text(original.replace("SPEC-001#rule-3", "REQ-001#rule-3"), encoding="utf-8")
        self.assertTrue(any("departs from a specification, not a requirement" in item for item in self.decision_errors()))
        path.write_text(original.replace('id = "stop"', 'id = "punt"'), encoding="utf-8")
        self.assertTrue(any("include stop" in item for item in self.decision_errors()))
        path.write_text(original.replace('observed = "The evaluator cannot read the field on Windows."\n', ""), encoding="utf-8")
        self.assertTrue(any("observed" in item for item in self.decision_errors()))

    def test_open_decisions_section_accepts_none_or_decision_ids_only(self) -> None:
        from se_harness.workflow_compliance import authoring_ready

        path = self.root / "docs/engineering/product/requirements/REQ-001.md"
        body = (
            "\n## Statement\n\nTHE SYSTEM SHALL retain revision provenance.\n\n## Rationale\n\nProvenance is the proof.\n\n"
            "## Acceptance criteria\n\n- The commit is recorded.\n\n## Open decisions\n\n{open}\n"
        )
        text = path.read_text(encoding="utf-8")
        head = text.split("# REQ-001", 1)[0] + "# REQ-001\n"
        write(path, head + body.format(open="None"))
        artifact = next(item for item in self.validate().artifacts if item.artifact_id == "REQ-001")
        self.assertEqual("pass", authoring_ready(artifact)[0], authoring_ready(artifact))
        write(path, head + body.format(open="- `DEC-001` (open)"))
        artifact = next(item for item in self.validate().artifacts if item.artifact_id == "REQ-001")
        self.assertEqual("pass", authoring_ready(artifact)[0], authoring_ready(artifact))
        write(path, head + body.format(open="We still need to pick the field name."))
        artifact = next(item for item in self.validate().artifacts if item.artifact_id == "REQ-001")
        status, message = authoring_ready(artifact)
        self.assertEqual("fail", status)
        self.assertIn("E-DCM-004", message)

    # ---------------------------------------------------------------- REQ-DCM-002: the gate and the disposition

    def test_an_open_decision_blocks_the_handoff_until_it_is_decided(self) -> None:
        self.in_progress_work_order()
        self.raise_decision()
        result = self.handoff_check()
        predicate = self.predicates(result)["QGP-G4I-DECISION"]
        self.assertEqual("fail", predicate["status"], predicate)
        self.assertIn("DEC-001", predicate["message"])
        self.assertIn("Which shape does the record take?", predicate["message"])
        self.assertIn("keep", predicate["message"])
        self.assertIn("harnessctl decide", predicate["message"])
        self.assertIn("owner", predicate["message"])
        self.assertTrue(any(item.startswith("QGP-G4I-DECISION:") for item in result["restitution"]["blocked_by"]))

        code, output, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-001", "--option", "keep",
            "--decision", "owner", "--reason", "One record; the split buys nothing.", "--apply", "--json",
        )
        self.assertEqual(0, code, error + output)
        text = self.decision_path().read_text(encoding="utf-8")
        self.assertIn('status = "decided"', text)
        self.assertIn("[disposition]", text)
        self.assertIn('option = "keep"', text)
        self.assertIn('label = "Keep the current shape."', text)
        self.assertIn('decided_by = "owner"', text)
        self.assertIn('reason = "One record; the split buys nothing."', text)
        self.assertIn("[[lifecycle_events]]", text)
        self.assertLess(text.index("[disposition]"), text.index("[[lifecycle_events]]"))
        self.assertEqual([], self.decision_errors())
        self.assertEqual("pass", self.predicates(self.handoff_check())["QGP-G4I-DECISION"]["status"])

    def test_disposition_is_refused_for_the_wrong_role_a_missing_reason_or_an_undeclared_option(self) -> None:
        self.raise_decision()
        base = ("decide", str(self.root), "--artifact", "DEC-001")
        code, output, error = self.invoke(*base, "--option", "keep", "--decision", "release-owner", "--reason", "fine", "--apply")
        self.assertEqual(1, code)
        self.assertIn("DR-DECISION-DISPOSE", output + error)
        self.assertIn("owner", output + error)
        code, output, error = self.invoke(*base, "--option", "keep", "--decision", "owner", "--apply")
        self.assertEqual(1, code)
        self.assertIn("requires --reason", output + error)
        code, output, error = self.invoke(*base, "--option", "burn", "--decision", "owner", "--reason", "x", "--apply")
        self.assertEqual(1, code)
        self.assertIn("declares options keep, split", output + error)
        self.assertIn('status = "open"', self.decision_path().read_text(encoding="utf-8"))
        code, _, error = self.invoke(*base, "--option", "split", "--decision", "owner", "--reason", "Two records read better.", "--apply")
        self.assertEqual(0, code, error)
        code, output, error = self.invoke(*base, "--option", "keep", "--decision", "owner", "--reason", "again", "--apply")
        self.assertEqual(1, code)
        self.assertIn("decided -> decided is not allowed", output + error)

    def test_a_decision_is_never_transitioned_by_hand(self) -> None:
        self.raise_decision()
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "DEC-001=decided",
            "--decision", "DEC-001=owner", "--reason", "DEC-001=keep", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("harnessctl decide", output + error)
        self.assertIn('status = "open"', self.decision_path().read_text(encoding="utf-8"))

    def test_a_deferral_needs_a_scope_and_a_revisit_and_admits_only_the_scoped_transition(self) -> None:
        self.in_progress_work_order()
        self.raise_decision(concerns=("WO-001", "REQ-001"), blocks=("WO-001", "REQ-001"))
        base = ("decide", str(self.root), "--artifact", "DEC-001", "--defer", "--decision", "owner", "--reason", "Not before the field lands.")
        code, output, error = self.invoke(*base, "--apply")
        self.assertEqual(1, code)
        self.assertIn("requires --scope", output + error)
        code, output, error = self.invoke(*base, "--scope", "SPEC-001:draft-approved", "--revisit", "v1.1.0", "--apply")
        self.assertEqual(1, code)
        self.assertIn("does not block", output + error)
        code, output, error = self.invoke(*base, "--scope", "WO-001:in_progress-implemented", "--apply")
        self.assertEqual(1, code)
        self.assertIn("requires --revisit", output + error)
        code, _, error = self.invoke(*base, "--scope", "WO-001:in_progress-implemented", "--revisit", "v1.1.0", "--apply")
        self.assertEqual(0, code, error)
        text = self.decision_path().read_text(encoding="utf-8")
        self.assertIn('status = "deferred"', text)
        self.assertIn('scope = ["WO-001:in_progress-implemented"]', text)
        self.assertIn('revisit = "v1.1.0"', text)
        self.assertEqual([], self.decision_errors())
        # the admitted transition passes; every other blocked transition still waits
        self.assertEqual("pass", self.predicates(self.handoff_check())["QGP-G4I-DECISION"]["status"])
        from se_harness.workflow import _catalog, _validation
        from se_harness.workflow_compliance import blocking_decisions

        catalog = _catalog(_validation(self.root)[1])
        self.assertEqual([], [item.artifact_id for item in blocking_decisions(catalog, catalog["WO-001"], "implemented")])
        self.assertEqual(["DEC-001"], [item.artifact_id for item in blocking_decisions(catalog, catalog["WO-001"], "verified")])
        self.assertEqual(["DEC-001"], [item.artifact_id for item in blocking_decisions(catalog, catalog["REQ-001"], "approved")])
        # a deferred decision is still disposed later
        code, _, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-001", "--option", "keep",
            "--decision", "owner", "--reason", "The field landed.", "--apply",
        )
        self.assertEqual(0, code, error)
        self.assertIn('status = "decided"', self.decision_path().read_text(encoding="utf-8"))

    def test_withdrawal_records_a_disposition_and_closes_the_decision(self) -> None:
        self.raise_decision()
        code, _, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-001", "--withdraw",
            "--decision", "owner", "--reason", "The record was removed with WO-002.", "--apply",
        )
        self.assertEqual(0, code, error)
        text = self.decision_path().read_text(encoding="utf-8")
        self.assertIn('status = "withdrawn"', text)
        self.assertIn('option = "withdrawn"', text)
        self.assertEqual([], self.decision_errors())
        code, output, error = self.invoke("check", str(self.root), "--artifact", "DEC-001", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual("WFL-DEC-CLOSED", json.loads(output)["compliance"]["workflow_rule_id"])

    # ---------------------------------------------------------------- REQ-DCM-003: deviations and their standing

    def test_an_accepted_deviation_is_time_bounded_and_stands_on_the_rule_the_work_and_its_records(self) -> None:
        deviation = dict(
            kind="deviation",
            against="SPEC-001#rule-3",
            observed="The evaluator cannot read the field on Windows.",
            options=(("amend", "Amend rule 3."), ("accept", "Accept the deviation."), ("stop", "Stop the work.")),
            recommendation="accept",
            concerns=("SPEC-001", "WO-001"),
            blocks=("WO-001",),
        )
        self.raise_decision(**deviation)
        base = ("decide", str(self.root), "--artifact", "DEC-001", "--option", "accept", "--decision", "owner", "--reason", "Windows lacks the field; the Linux lane proves it.")
        code, output, error = self.invoke(*base, "--apply")
        self.assertEqual(1, code)
        self.assertIn("acceptance is time-bounded", output + error)
        code, output, error = self.invoke("decide", str(self.root), "--artifact", "DEC-001", "--option", "accept", "--decision", "quality-owner", "--reason", "x", "--revisit", "v2.0.0", "--apply")
        self.assertEqual(1, code)
        self.assertIn("DR-DECISION-DISPOSE", output + error)
        code, _, error = self.invoke(*base, "--revisit", "v2.0.0", "--apply")
        self.assertEqual(0, code, error)
        text = self.decision_path().read_text(encoding="utf-8")
        self.assertIn('status = "decided"', text)
        self.assertIn('revisit = "v2.0.0"', text)
        self.assertEqual([], self.decision_errors())

        validator = _load_validator_module()
        report = self.validate()
        standing = validator.standing_deviations(report.artifacts)
        self.assertEqual({"SPEC-001": ["DEC-001"], "WO-001": ["DEC-001"]}, standing)
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            formal(
                "VREC-001", "verification_record", "ready",
                {"verifies_work_order": ["WO-001"], "conforms_to": ["VER-001"]},
                f'commit = "{"a" * 40}"\ngit_object_format = "sha1"\nworktree_state = "clean"\n'
                'prepared_at = "2026-08-20T10:00:00Z"\nprepared_by = "quality-owner"\n'
                f'artifact_snapshot_sha256 = "{"b" * 64}"\n'
                'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md"]',
            ),
        )
        standing = validator.standing_deviations(self.validate().artifacts)
        self.assertEqual(["DEC-001"], standing["VREC-001"])

        # a second acceptance against the same rule is a maintenance warning
        self.raise_decision("DEC-002", **deviation)
        code, _, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-002", "--option", "accept", "--decision", "owner",
            "--reason", "Same fact, second work order.", "--revisit", "v2.0.0", "--apply",
        )
        self.assertEqual(0, code, error)
        warnings = [item for item in self.validate().warnings if item.code == "W-DCM-002"]
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("2 accepted deviations stand against SPEC-001#rule-3", warnings[0].message)
        # amending the rule closes the standing
        self.raise_decision("DEC-003", **deviation)
        code, _, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-003", "--option", "amend", "--decision", "owner",
            "--reason", "Rule 3 now names the Linux lane.", "--apply",
        )
        self.assertEqual(0, code, error)
        self.assertEqual({}, validator.standing_deviations(self.validate().artifacts))

    # ---------------------------------------------------------------- surfaces: projection, inspection, Explorer

    def test_check_inspect_and_dashboard_surface_the_open_decision(self) -> None:
        self.in_progress_work_order()
        self.raise_decision()
        code, output, error = self.invoke("check", str(self.root), "--artifact", "DEC-001", "--json")
        self.assertEqual(0, code, error)
        projection = json.loads(output)
        self.assertEqual("WFL-DEC-OPEN", projection["compliance"]["workflow_rule_id"])
        self.assertEqual("STEP-DEC-DISPOSE", projection["restitution"]["next"]["step_id"])
        self.assertEqual("DR-DECISION-DISPOSE", projection["restitution"]["decision_required"]["decision_right"])
        self.assertIn("WO-001", projection["scope"]["governing"])
        code, output, error = self.invoke("inspect", str(self.root), "--json")
        self.assertEqual(0, code, error)
        queue = json.loads(output)["queues"]["decision_required"]
        self.assertIn(("DEC-001", "dispose-decision"), [(item["id"], item["action"]) for item in queue])
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        bundle_dir = self.root / "target/harness-dashboard"
        catalog = "".join(
            path.read_text(encoding="utf-8")
            for path in (bundle_dir / "data/artifacts").rglob("*")
            if path.is_file()
        )
        self.assertIn('"deciding_roles"', catalog)
        self.assertIn('"kind":"question"', catalog.replace(" ", ""))
        summary = "".join(
            path.read_text(encoding="utf-8") for path in bundle_dir.rglob("*.json") if path.is_file()
        )
        self.assertIn('"decisions_open"', summary)


class DecisionGateFamilyTests(DecisionManagementTests):
    """VER-DCM-001: the gate per blocked family, contract coverage, and the surfaces' safety."""

    def write_draft_chain(self) -> dict[str, Path]:
        base = self.root / "docs/engineering/product"
        paths = {
            "REQ-002": base / "requirements/REQ-002.md",
            "SPEC-002": base / "specifications/SPEC-002.md",
            "ADR-002": base / "architecture/adr/ADR-002.md",
            "VER-002": base / "verification/VER-002.md",
            "WO-002": base / "work-orders/WO-002.md",
        }
        write(paths["REQ-002"], formal("REQ-002", "requirement", "draft", {"derives_from": ["CAP-001"]},
                                      'statement = "THE SYSTEM SHALL retain aggregate release scope."\nverification_method = "automated-test"'))
        write(paths["SPEC-002"], formal("SPEC-002", "specification", "draft", {"specifies": ["REQ-002"]}))
        write(paths["ADR-002"], formal("ADR-002", "adr", "draft", {"decides": ["ARCH-001"]}))
        write(paths["VER-002"], formal("VER-002", "verification", "draft", {"verifies": ["REQ-002"]}))
        write(paths["WO-002"], formal(
            "WO-002", "work_order", "approved",
            {"implements": ["REQ-001"], "specifications": ["SPEC-001"], "architecture": ["ARCH-001", "ADR-001"], "verification": ["VER-001"]},
            '[assurance]\ncommit_bound_verification = "required"\nrationale = "Decision fixture."\n'
            'decided_by = "repository-owner"\n\n[execution_scope]\npaths = ["src/"]',
        ))
        return paths

    def test_every_blockable_family_is_refused_and_nothing_is_written(self) -> None:
        paths = self.write_draft_chain()
        blocked = tuple(paths)
        self.raise_decision(concerns=blocked, blocks=blocked)
        self.assertEqual([], self.decision_errors())
        before = {name: path.read_bytes() for name, path in paths.items()}
        decision_before = self.decision_path().read_bytes()
        expected_predicate = {
            "REQ-002": "QGP-G1-DECISION", "VER-002": "QGP-G1-DECISION",
            "SPEC-002": "QGP-G2-DECISION", "ADR-002": "QGP-G2-DECISION",
            "WO-002": "QGP-G3-DECISION",
        }
        for artifact_id, predicate in expected_predicate.items():
            target = "in_progress" if artifact_id == "WO-002" else "approved"
            with self.subTest(artifact=artifact_id):
                code, output, error = self.invoke(
                    "transition", str(self.root), "--set", f"{artifact_id}={target}",
                    "--decision", f"{artifact_id}=owner", "--reason", f"{artifact_id}=ready", "--apply",
                )
                self.assertEqual(1, code, output + error)
                text = output + error
                self.assertIn(predicate, text)
                self.assertIn("DEC-001", text)
                self.assertIn("Which shape does the record take?", text)
                self.assertIn("harnessctl decide", text)
                self.assertEqual(before[artifact_id], paths[artifact_id].read_bytes())
        self.assertEqual(decision_before, self.decision_path().read_bytes())

    def test_a_record_family_cannot_be_named_in_blocks(self) -> None:
        # SPEC-DCM-001 rule 4 closes `blocks` to six types; a record is reached through
        # the work it covers, never named directly.
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            formal(
                "VREC-001", "verification_record", "ready",
                {"verifies_work_order": ["WO-001"], "conforms_to": ["VER-001"]},
                f'commit = "{"a" * 40}"\ngit_object_format = "sha1"\nworktree_state = "clean"\n'
                'prepared_at = "2026-08-20T10:00:00Z"\nprepared_by = "quality-owner"\n'
                f'artifact_snapshot_sha256 = "{"b" * 64}"\n'
                'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md"]',
            ),
        )
        self.raise_decision(concerns=("WO-001", "VREC-001"), blocks=("VREC-001",))
        errors = [f"{item.code}: {item.message}" for item in self.validate().errors]
        self.assertTrue(any("E011" in item and "VREC-001" in item and "blocks" in item for item in errors), errors)
        self.raise_decision(concerns=("WO-001", "CAP-001"), blocks=("WO-001", "CAP-404"))
        errors = [f"{item.code}: {item.message}" for item in self.validate().errors]
        self.assertTrue(any("CAP-404" in item for item in errors), errors)

    def test_the_refusal_is_deterministic(self) -> None:
        self.in_progress_work_order()
        self.raise_decision()
        first = self.predicates(self.handoff_check())["QGP-G4I-DECISION"]
        second = self.predicates(self.handoff_check())["QGP-G4I-DECISION"]
        self.assertEqual("fail", first["status"])
        self.assertEqual(first, second)

    def test_a_past_revisit_on_an_accepted_deviation_is_a_maintenance_warning(self) -> None:
        from tests.test_revision_provenance import release_record, verification_record

        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", verification_record("a" * 40))
        write(self.root / "docs/engineering/product/releases/RLS-001.md", release_record("a" * 40))
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.validate().errors])
        self.raise_decision(
            kind="deviation", against="SPEC-001#rule-3", observed="The field is unreadable on Windows.",
            options=(("accept", "Accept."), ("stop", "Stop.")), recommendation="accept",
            concerns=("SPEC-001", "WO-001"), blocks=("WO-001",),
        )
        code, _, error = self.invoke(
            "decide", str(self.root), "--artifact", "DEC-001", "--option", "accept", "--decision", "owner",
            "--reason", "Accepted for one release.", "--revisit", "v1.0.0", "--apply",
        )
        self.assertEqual(0, code, error)
        warnings = [item for item in self.validate().warnings if item.code == "W-DCM-001"]
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("past its revisit 'v1.0.0'", warnings[0].message)
        self.assertEqual(
            {"RLS-001": ["DEC-001"], "SPEC-001": ["DEC-001"], "VREC-001": ["DEC-001"], "WO-001": ["DEC-001"]},
            _load_validator_module().standing_deviations(self.validate().artifacts),
        )

    def test_contract_copies_carry_the_family_the_predicates_and_the_policy_rows(self) -> None:
        templates = Path(__file__).resolve().parents[1] / "templates/repository/standard/docs/engineering"
        package = Path(__file__).resolve().parents[1] / "se_harness"
        workflow = json.loads((templates / "WORKFLOW.json").read_text(encoding="utf-8"))
        quality = json.loads((templates / "QUALITY_GATES.json").read_text(encoding="utf-8"))
        self.assertEqual((templates / "WORKFLOW.json").read_bytes(), (package / "workflow_contract.json").read_bytes())
        self.assertEqual((templates / "QUALITY_GATES.json").read_bytes(), (package / "quality_gates_contract.json").read_bytes())
        self.assertIn("decision", workflow["lifecycles"])
        self.assertEqual(
            {"open": ["decided", "deferred", "withdrawn"], "deferred": ["decided", "withdrawn"], "decided": [], "withdrawn": []},
            {state: sorted(entry["transitions_to"]) for state, entry in workflow["lifecycles"]["decision"].items()},
        )
        predicates = {p["id"]: p for gate in quality["gates"] for p in gate["predicates"]}
        decision_predicates = sorted(pid for pid in predicates if pid.endswith("-DECISION"))
        self.assertEqual(
            ["QGP-G1-DECISION", "QGP-G2-DECISION", "QGP-G3-DECISION", "QGP-G4A-DECISION", "QGP-G4I-DECISION", "QGP-G4V-DECISION", "QGP-G5D-DECISION", "QGP-G5P-DECISION"],
            decision_predicates,
        )
        self.assertTrue(all(predicates[pid]["evaluator"] == "decision_gate_clear" for pid in decision_predicates))
        self.assertNotIn("scope", predicates["QGP-G4I-DECISION"]["checkpoints"])
        # every transition check with gate predicates carries the decision predicate of its gate
        for binding in quality["transition_bindings"]:
            gated = [pid for pid in binding.get("predicates", []) if pid.startswith("QGP-")]
            if gated and binding.get("family") != "decision":
                with self.subTest(binding=binding):
                    self.assertTrue(any(pid.endswith("-DECISION") for pid in gated), binding)
        self.assertIn("| `DR-DECISION-DISPOSE` |", (templates / "DECISION_RIGHTS.md").read_text(encoding="utf-8"))
        traceability = (templates / "TRACEABILITY.md").read_text(encoding="utf-8")
        for token in ("`TRC-REL-020`", "`TRC-REL-021`", "`TRC-REL-022`", "| `decision` | `DEC-` |", "`TRC-015`"):
            self.assertIn(token, traceability)
        self.assertIn("## decision", (templates / "ARTIFACT_AUTHORING.md").read_text(encoding="utf-8"))

    def test_only_the_transition_path_writes_a_disposition(self) -> None:
        package = Path(__file__).resolve().parents[1] / "se_harness"
        writers = sorted(path.name for path in package.glob("*.py") if '"[disposition]"' in path.read_text(encoding="utf-8"))
        self.assertEqual(["workflow.py"], writers)

    def test_hostile_decision_text_stays_data(self) -> None:
        hostile = "<script>alert(1)</script> +++ </script><b>x</b>"
        path = self.raise_decision()
        text = path.read_text(encoding="utf-8").replace('question = "Which shape does the record take?"', f'question = "{hostile}"')
        path.write_text(text, encoding="utf-8")
        self.assertEqual([], self.decision_errors())
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        bundle_dir = self.root / "target/harness-dashboard"
        index = (bundle_dir / "index.html").read_text(encoding="utf-8")
        self.assertNotIn(hostile, index)
        data = "".join(p.read_text(encoding="utf-8") for p in (bundle_dir / "data/artifacts").rglob("*") if p.is_file())
        self.assertTrue(json.dumps(hostile)[1:-1] in data or json.dumps(hostile)[1:-1].replace("<", "\\u003c").replace(">", "\\u003e") in data, data[:200])


if __name__ == "__main__":
    unittest.main()
