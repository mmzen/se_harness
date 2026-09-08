"""WO-ECP-032 (SPEC-ECP-023 ECP-PRM-006 to ECP-PRM-015): the integrity primitives in one home.

Every byte form a caller wrote before is reproduced by the shared primitive; the
atomic writers leave a target untouched when interrupted; the closed sets have one
definition; both wheel parsers apply one grammar; one environment builder serves the
two qualification runtimes.
"""

from __future__ import annotations

import ast
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import candidate_acceptance, integrity, release_qualification, workflow_contract
from se_harness.installer import HarnessError

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class Refusal(RuntimeError):
    pass


class SerializerTests(unittest.TestCase):
    VALUE = {"z": [1, 2, {"b": None, "a": "é"}], "a": True, "m": 1.5}

    def test_canonical_json_bytes_reproduces_both_recorded_forms(self) -> None:
        compact_ascii = (json.dumps(self.VALUE, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
        compact_utf8 = (json.dumps(self.VALUE, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(compact_ascii, integrity.canonical_json_bytes(self.VALUE, ensure_ascii=True))
        self.assertEqual(compact_utf8, integrity.canonical_json_bytes(self.VALUE, ensure_ascii=False))
        self.assertNotEqual(compact_ascii, compact_utf8)

    def test_pretty_json_bytes_reproduces_the_retained_document_form(self) -> None:
        pretty = (json.dumps(self.VALUE, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(pretty, integrity.pretty_json_bytes(self.VALUE, ensure_ascii=True))
        self.assertTrue(integrity.pretty_json_bytes(self.VALUE, ensure_ascii=False).decode("utf-8").count("é"))

    def test_the_duplicate_key_hook_raises_the_callers_error_naming_the_key(self) -> None:
        hook = integrity.unique_object_hook(lambda key: Refusal(f"twice: {key}"))
        self.assertEqual({"a": 1, "b": 2}, json.loads('{"a": 1, "b": 2}', object_pairs_hook=hook))
        with self.assertRaisesRegex(Refusal, "twice: a"):
            json.loads('{"a": 1, "a": 2}', object_pairs_hook=hook)

    def test_canonical_text_folds_crlf_and_lone_cr(self) -> None:
        self.assertEqual("a\nb\nc\n", integrity.canonical_text("a\r\nb\rc\n"))
        self.assertEqual(b"a\nb\nc\n", integrity.canonical_text_bytes(b"a\r\nb\rc\n"))


class AtomicWriterTests(unittest.TestCase):
    def test_atomic_write_replaces_and_leaves_the_target_untouched_when_the_replace_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "nested" / "file.txt"
            integrity.atomic_write_bytes(target, b"one")
            self.assertEqual(b"one", target.read_bytes())
            integrity.atomic_write_bytes(target, b"two")
            self.assertEqual(b"two", target.read_bytes())
            with mock.patch("se_harness.integrity.os.replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    integrity.atomic_write_bytes(target, b"three")
            self.assertEqual(b"two", target.read_bytes())
            self.assertEqual(["file.txt"], sorted(item.name for item in target.parent.iterdir()))

    def test_atomic_create_refuses_an_existing_target_with_the_callers_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "record.md"
            integrity.atomic_create_bytes(target, b"first", exists=lambda: Refusal("exists"), failed=lambda d: Refusal(f"failed: {d}"))
            self.assertEqual(b"first", target.read_bytes())
            with self.assertRaisesRegex(Refusal, "exists"):
                integrity.atomic_create_bytes(target, b"second", exists=lambda: Refusal("exists"), failed=lambda d: Refusal(f"failed: {d}"))
            self.assertEqual(b"first", target.read_bytes())
            self.assertEqual(["record.md"], sorted(item.name for item in target.parent.iterdir()))

    def test_no_package_module_keeps_a_private_atomic_writer_or_a_tmp_stage(self) -> None:
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            if path.name == "integrity.py":
                continue
            source = path.read_text(encoding="utf-8")
            if "mkstemp(" in source or 'with_name(path.name + ".tmp")' in source or "os.fsync(" in source:
                offenders.append(path.name)
        self.assertEqual([], offenders)


class ConfigurationReaderTests(unittest.TestCase):
    def test_read_toml_tolerates_a_bom_and_names_every_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / ".engineering-harness.toml"
            path.write_bytes(b'\xef\xbb\xbf[harness]\r\ntool_version = "0.16.0"\r\n')
            self.assertEqual({"harness": {"tool_version": "0.16.0"}}, integrity.read_toml(path))
            path.write_bytes(b"[harness\n")
            with self.assertRaisesRegex(integrity.IntegrityError, "cannot read"):
                integrity.read_toml(path)
            with self.assertRaisesRegex(integrity.IntegrityError, "cannot read"):
                integrity.read_toml(Path(temporary) / "absent.toml")

    def test_the_package_reads_the_configuration_through_one_reader(self) -> None:
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            if path.name in {"integrity.py", "front_matter.py", "gate_source.py"}:
                continue  # the front-matter parser and the owner-owned delegation file have their own TOML loads
            source = path.read_text(encoding="utf-8")
            if re.search(r"tomllib\.loads\([^\n]*read_text", source):
                offenders.append(path.name)
        self.assertEqual([], offenders)


class ClosedSetTests(unittest.TestCase):
    def test_checkpoint_and_definition_type_sets_have_one_definition(self) -> None:
        self.assertEqual(("start", "pre-action", "transition", "handoff", "scope"), workflow_contract.CHECKPOINT_ORDER)
        self.assertEqual(frozenset(workflow_contract.CHECKPOINT_ORDER), workflow_contract.CHECKPOINTS)
        self.assertEqual(("start", "pre-action", "transition", "handoff"), workflow_contract.EVIDENCE_CHECKPOINTS)
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            if path.name == "workflow_contract.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.Set, ast.Tuple, ast.List)) and len(node.elts) >= 4:
                    values = {item.value for item in node.elts if isinstance(item, ast.Constant)}
                    if {"start", "pre-action", "transition", "handoff"} <= values or {"intent", "capability", "requirement", "specification", "architecture"} <= values:
                        offenders.append(f"{path.name}:{node.lineno}")
        self.assertEqual([], offenders)

    def test_typed_value_sets_exist(self) -> None:
        from se_harness import installer, preflight

        self.assertEqual({"init", "upgrade"}, set(installer.InstallMode.__args__))
        self.assertEqual({"start", "review"}, set(preflight.Phase.__args__))
        self.assertEqual(set(workflow_contract.CHECKPOINT_ORDER), set(workflow_contract.Checkpoint.__args__))
        self.assertIn("remove", installer.ChangeAction.__args__)


class GrammarAndEnvironmentTests(unittest.TestCase):
    def test_both_wheel_parsers_apply_one_grammar(self) -> None:
        self.assertIs(candidate_acceptance.VERSION_PATTERN, integrity.WHEEL_VERSION_PATTERN)
        self.assertIs(release_qualification.VERSION_PATTERN, integrity.WHEEL_VERSION_PATTERN)
        for version, accepted in (("0.16.0", True), ("0.17.0rc1", True), ("0.5.0a1", True), ("1.2", False), ("v1.2.3", False)):
            with self.subTest(version=version):
                self.assertEqual(accepted, integrity.WHEEL_VERSION_PATTERN.fullmatch(version) is not None)

    def test_one_environment_builder_denies_pythonpath_and_user_site_for_both_runtimes(self) -> None:
        with mock.patch.dict(os.environ, {"PYTHONPATH": "evil", "PATH": os.environ.get("PATH", ""), "SECRET_TOKEN": "x"}, clear=False):
            for built in (candidate_acceptance.safe_environment(), release_qualification._safe_environment(), candidate_acceptance._environment()):
                with self.subTest(keys=sorted(built)):
                    self.assertNotIn("PYTHONPATH", built)
                    self.assertNotIn("SECRET_TOKEN", built)
                    self.assertEqual("1", built["PYTHONNOUSERSITE"])
        self.assertIs(release_qualification._safe_environment, candidate_acceptance.safe_environment)
        self.assertEqual("1", candidate_acceptance._environment()["PIP_NO_INPUT"])


class DigestPreservationTests(unittest.TestCase):
    def test_the_acceptance_contract_digest_is_the_recorded_one(self) -> None:
        # ECP-PRM-024: every released verifier records this value; it must not move with the serializer.
        recorded = integrity.raw_sha256(
            json.dumps({"schema": candidate_acceptance.ACCEPTANCE_SCHEMA, "scenarios": candidate_acceptance.SCENARIO_IDS}, sort_keys=True).encode("utf-8")
        )
        self.assertEqual(recorded, candidate_acceptance.CONTRACT_SHA256)

    def test_no_package_module_hashes_or_serializes_privately(self) -> None:
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            if path.name == "integrity.py":
                continue
            source = path.read_text(encoding="utf-8")
            if re.search(r"hashlib\.sha256\([^)]", source):
                offenders.append(f"{path.name}: sha256")
            if re.search(r"separators=\(\",\", \":\"\)", source):
                offenders.append(f"{path.name}: compact json")
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
