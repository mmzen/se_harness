from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import __version__
from se_harness import evaluator_identity as IDENTITY
from se_harness.evaluator_identity import InstalledEvaluatorIdentity
from se_harness.runtime_identity import inspect_runtime_identity


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class EvaluatorIdentityTests(unittest.TestCase):
    def test_payload_manifest_is_ordered_and_content_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first.py"
            second = root / "second.md"
            first.write_bytes(b"first\n")
            second.write_bytes(b"second\n")
            files = [("templates/repository/standard/second.md", second), ("se_harness/first.py", first)]
            with mock.patch.object(IDENTITY, "_payload_files", return_value=files):
                manifest = IDENTITY.canonical_payload_manifest()
                digest = IDENTITY.installed_payload_sha256()
            parsed = json.loads(manifest)
            self.assertEqual(
                ["se_harness/first.py", "templates/repository/standard/second.md"],
                [item["path"] for item in parsed["files"]],
            )
            self.assertEqual(hashlib.sha256(manifest).hexdigest(), digest)
            first.write_bytes(b"changed\n")
            with mock.patch.object(IDENTITY, "_payload_files", return_value=files):
                self.assertNotEqual(digest, IDENTITY.installed_payload_sha256())

    def test_pep610_archive_identity_is_verified(self) -> None:
        class Distribution:
            def locate_file(self, name: str) -> Path:
                return Path(IDENTITY.__file__).resolve().parent.parent

            def read_text(self, name: str) -> str:
                self_name = f"se_harness-{__version__}-py3-none-any.whl"
                return json.dumps(
                    {
                        "url": f"file:///tmp/{self_name}",
                        "archive_info": {"hashes": {"sha256": "a" * 64}},
                    }
                )

        with mock.patch.object(IDENTITY.importlib.metadata, "distribution", return_value=Distribution()):
            self.assertEqual(
                (f"se_harness-{__version__}-py3-none-any.whl", "a" * 64),
                IDENTITY._direct_url_archive(),
            )

    def test_pep610_duplicate_or_conflicting_hashes_fail_closed(self) -> None:
        class Distribution:
            def __init__(self, value: str) -> None:
                self.value = value

            def locate_file(self, name: str) -> Path:
                return Path(IDENTITY.__file__).resolve().parent.parent

            def read_text(self, name: str) -> str:
                return self.value

        wheel = f"se_harness-{__version__}-py3-none-any.whl"
        digest = "a" * 64
        duplicate = f'{{"url":"file:///{wheel}","url":"file:///{wheel}","archive_info":{{"hashes":{{"sha256":"{digest}"}}}}}}'
        with mock.patch.object(IDENTITY.importlib.metadata, "distribution", return_value=Distribution(duplicate)):
            with self.assertRaisesRegex(IDENTITY.EvaluatorIdentityError, "repeats field"):
                IDENTITY._direct_url_archive()
        conflicting = json.dumps(
            {
                "url": f"file:///{wheel}",
                "archive_info": {
                    "hash": f"sha256={'a' * 64}",
                    "hashes": {"sha256": "b" * 64},
                },
            }
        )
        with mock.patch.object(IDENTITY.importlib.metadata, "distribution", return_value=Distribution(conflicting)):
            with self.assertRaisesRegex(IDENTITY.EvaluatorIdentityError, "values disagree"):
                IDENTITY._direct_url_archive()

    def test_runtime_rejects_payload_and_archive_mismatch(self) -> None:
        installed = InstalledEvaluatorIdentity(
            version=__version__,
            payload_manifest=IDENTITY.PAYLOAD_MANIFEST,
            payload_sha256="a" * 64,
            archive_name=f"se_harness-{__version__}-py3-none-any.whl",
            archive_sha256="b" * 64,
        )
        with mock.patch("se_harness.runtime_identity.installed_evaluator_identity", return_value=installed):
            report = inspect_runtime_identity(
                role="released-evaluator",
                expected_version=__version__,
                expected_root=Path(sys.prefix),
                checkout_root=REPOSITORY_ROOT,
                evaluator_payload_sha256="c" * 64,
                evaluator_wheel_sha256="d" * 64,
            )
        codes = {item.code for item in report.diagnostics}
        self.assertIn("RID021", codes)
        self.assertIn("RID022", codes)


if __name__ == "__main__":
    unittest.main()
