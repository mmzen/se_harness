from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

from se_harness.agent_contract import canonical_json_bytes
from se_harness.change_bundle import (
    CHANGE_BUNDLE_SCHEMA,
    MAX_BUNDLE_BYTES,
    MAX_CHANGES,
    MAX_FILE_BYTES,
    MAX_TOTAL_AFTER_BYTES,
    ChangeBundleError,
    construct_change_bundle,
    parse_change_bundle_bytes,
    read_content_object,
    validate_change_bundle,
)


class ChangeBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.baseline = self.root / "baseline"
        self.proposed = self.root / "proposed"
        self.objects = self.root / "object-store"
        self.baseline.mkdir()
        self.proposed.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _write(root: Path, relative: str, content: bytes) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    @staticmethod
    def _value() -> dict[str, object]:
        digest = "a" * 64
        return {
            "schema": CHANGE_BUNDLE_SCHEMA,
            "identity": {
                "work_order": "WO-AEX-006",
                "envelope_sha256": "b" * 64,
                "repository_state_before": "c" * 64,
            },
            "changes": [
                {
                    "operation": "create",
                    "path": "docs/new.txt",
                    "before": None,
                    "after": {
                        "sha256": digest,
                        "size": 1,
                        "object": f"objects/{digest}",
                    },
                }
            ],
        }

    def test_constructs_only_ordered_deltas_and_shares_content_objects(self) -> None:
        self._write(self.baseline, "replace.txt", b"before")
        self._write(self.baseline, "delete.txt", b"delete")
        self._write(self.baseline, "same.txt", b"same")
        self._write(self.proposed, "replace.txt", b"shared")
        self._write(self.proposed, "create.txt", b"shared")
        self._write(self.proposed, "same.txt", b"same")
        result = construct_change_bundle(
            baseline_workspace=self.baseline,
            proposed_workspace=self.proposed,
            object_store=self.objects,
            work_order="WO-AEX-006",
            envelope_sha256="1" * 64,
            repository_state_before="2" * 64,
            intended_deletions=("delete.txt",),
        )
        changes = result.bundle.value["changes"]
        self.assertEqual(
            ["create.txt", "delete.txt", "replace.txt"],
            [item["path"] for item in changes],
        )
        self.assertEqual(["create", "delete", "replace"], [item["operation"] for item in changes])
        self.assertEqual(1, len(result.object_paths))
        self.assertNotIn(b"owners", result.bundle.canonical_bytes)
        self.assertNotIn(b"execution_scope", result.bundle.canonical_bytes)
        parsed = parse_change_bundle_bytes(result.bundle.canonical_bytes)
        self.assertEqual(result.bundle.sha256, parsed.sha256)
        after = changes[0]["after"]
        self.assertEqual(
            b"shared",
            read_content_object(self.objects, after["sha256"], after["size"]),
        )

    def test_explicit_deletion_and_closed_operation_invariants(self) -> None:
        self._write(self.baseline, "removed.txt", b"prior")
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND007"):
            construct_change_bundle(
                baseline_workspace=self.baseline,
                proposed_workspace=self.proposed,
                object_store=self.objects,
                work_order="WO-AEX-006",
                envelope_sha256="1" * 64,
                repository_state_before="2" * 64,
            )
        for operation, before, after in (
            ("create", {"sha256": "1" * 64, "size": 1}, None),
            ("replace", None, None),
            ("delete", None, {"sha256": "1" * 64, "size": 1, "object": "objects/" + "1" * 64}),
        ):
            value = self._value()
            value["changes"][0].update(
                {"operation": operation, "before": before, "after": after}
            )
            with self.subTest(operation=operation), self.assertRaisesRegex(
                ChangeBundleError, "AEXBND007"
            ):
                validate_change_bundle(value)

    def test_parser_rejects_duplicates_unknowns_noncanonical_order_and_paths(self) -> None:
        raw = (
            b'{"schema":"se-harness-change-bundle-v1","schema":"x",'
            b'"identity":{},"changes":[]}'
        )
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND001"):
            parse_change_bundle_bytes(raw)
        value = self._value()
        raw = json.dumps(value, indent=2).encode("utf-8")
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND002"):
            parse_change_bundle_bytes(raw)
        unknown = copy.deepcopy(value)
        unknown["authority"] = {}
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND003"):
            validate_change_bundle(unknown)
        attacked = copy.deepcopy(value)
        attacked["changes"][0]["path"] = "../escape"
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND006"):
            validate_change_bundle(attacked)
        duplicate = copy.deepcopy(value["changes"][0])
        value["changes"] = [value["changes"][0], duplicate]
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND006"):
            validate_change_bundle(value)
        value = self._value()
        collision = copy.deepcopy(value["changes"][0])
        collision["path"] = "DOCS/NEW.TXT"
        value["changes"] = [collision, value["changes"][0]]
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND006"):
            validate_change_bundle(value)
        value = self._value()
        second = copy.deepcopy(value["changes"][0])
        second["path"] = "A.txt"
        value["changes"] = [value["changes"][0], second]
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND002"):
            validate_change_bundle(value)

    def test_entry_file_total_and_document_bounds_are_exact(self) -> None:
        value = self._value()
        entries = []
        for index in range(MAX_CHANGES):
            entry = copy.deepcopy(value["changes"][0])
            entry["path"] = f"files/{index:04d}.txt"
            entries.append(entry)
        value["changes"] = entries
        self.assertEqual(MAX_CHANGES, len(validate_change_bundle(value).value["changes"]))
        value["changes"].append(copy.deepcopy(entries[-1]))
        value["changes"][-1]["path"] = "files/overflow.txt"
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND004"):
            validate_change_bundle(value)

        value = self._value()
        value["changes"][0]["after"]["size"] = MAX_FILE_BYTES
        self.assertEqual(
            MAX_FILE_BYTES,
            validate_change_bundle(value).value["changes"][0]["after"]["size"],
        )
        value["changes"][0]["after"]["size"] = MAX_FILE_BYTES + 1
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND004"):
            validate_change_bundle(value)

        value = self._value()
        entries = []
        for index in range(4):
            entry = copy.deepcopy(value["changes"][0])
            entry["path"] = f"files/{index}.bin"
            entry["after"]["size"] = MAX_FILE_BYTES
            entries.append(entry)
        value["changes"] = entries
        self.assertEqual(
            MAX_TOTAL_AFTER_BYTES,
            sum(
                item["after"]["size"]
                for item in validate_change_bundle(value).value["changes"]
            ),
        )
        overflow = copy.deepcopy(entries[-1])
        overflow["path"] = "files/4.bin"
        value["changes"].append(overflow)
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND004"):
            validate_change_bundle(value)

        with self.assertRaisesRegex(ChangeBundleError, "AEXBND004"):
            parse_change_bundle_bytes(b"x" * (MAX_BUNDLE_BYTES + 1))

    def test_workspace_links_and_hard_link_aliases_are_rejected(self) -> None:
        self._write(self.proposed, "linked.txt", b"content")
        os.link(self.proposed / "linked.txt", self.proposed / "alias.txt")
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND008"):
            construct_change_bundle(
                baseline_workspace=self.baseline,
                proposed_workspace=self.proposed,
                object_store=self.objects,
                work_order="WO-AEX-006",
                envelope_sha256="1" * 64,
                repository_state_before="2" * 64,
            )

        (self.proposed / "alias.txt").unlink()
        try:
            (self.proposed / "link.txt").symlink_to(self.proposed / "linked.txt")
        except OSError:
            self.skipTest("host does not permit symlink creation")
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND008"):
            construct_change_bundle(
                baseline_workspace=self.baseline,
                proposed_workspace=self.proposed,
                object_store=self.objects,
                work_order="WO-AEX-006",
                envelope_sha256="1" * 64,
                repository_state_before="2" * 64,
            )

    def test_object_path_digest_and_corruption_are_rejected(self) -> None:
        value = self._value()
        value["changes"][0]["after"]["object"] = "objects/" + "d" * 64
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND008"):
            validate_change_bundle(value)
        self._write(self.proposed, "new.txt", b"content")
        result = construct_change_bundle(
            baseline_workspace=self.baseline,
            proposed_workspace=self.proposed,
            object_store=self.objects,
            work_order="WO-AEX-006",
            envelope_sha256="1" * 64,
            repository_state_before="2" * 64,
        )
        object_path = result.object_paths[0]
        object_path.chmod(0o600)
        object_path.write_bytes(b"corrupt")
        after = result.bundle.value["changes"][0]["after"]
        with self.assertRaisesRegex(ChangeBundleError, "AEXBND008"):
            read_content_object(self.objects, after["sha256"], after["size"])

    def test_catalog_is_packaged_and_names_no_authority_fields(self) -> None:
        catalog_path = Path(__file__).resolve().parents[1] / "se_harness" / "effect_contract.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-effect-contract-catalog-v1", catalog["schema"])
        self.assertEqual(
            {
                "se-harness-change-bundle-v1",
                "se-harness-effect-journal-v1",
                "se-harness-effect-receipt-v1",
            },
            {item["id"] for item in catalog["schemas"]},
        )
        self.assertTrue(all(item["authority_fields"] == [] for item in catalog["schemas"]))
        self.assertEqual(4_194_304, catalog["bounds"]["max_effect_journal_bytes"])
        self.assertEqual(
            canonical_json_bytes(json.loads(canonical_json_bytes(catalog))),
            canonical_json_bytes(catalog),
        )

    def test_independent_canonical_reference_vector_is_exact(self) -> None:
        vector_path = (
            Path(__file__).resolve().parents[1]
            / "tests/fixtures/agentic_execution/phase4/broker/canonical-vectors.json"
        )
        vector = json.loads(vector_path.read_text(encoding="utf-8"))["bundle"]
        document = validate_change_bundle(self._value())
        self.assertEqual(vector["canonical"].encode("utf-8"), document.canonical_bytes)
        self.assertEqual(vector["sha256"], document.sha256)


if __name__ == "__main__":
    unittest.main()
