"""Small current evidence and a read-only assessment of committed archives (K31)."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.inventory_evidence import inventory
from scripts.record_evidence import raw_status
from tests.git_support import git, init_repository


ROOT = Path(__file__).resolve().parents[1]


class EvidenceRetentionTests(unittest.TestCase):
    def test_inventory_uses_committed_sizes_and_follows_release_record_references(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            init_repository(root)
            bundle = "docs/engineering/example/evidence/WO-EX-001"
            files = {
                bundle + "/output.log": "x" * 10000,
                "docs/engineering/example/verification-records/VREC-EX-001.md":
                    '+++\nid="VREC-EX-001"\nstatus="verified"\nevidence_paths=["' + bundle + '/output.log"]\n+++\n',
                "docs/engineering/example/releases/RLS-EX-001.md":
                    '+++\nid="RLS-EX-001"\nstatus="released"\n[relations]\nverification_records=["VREC-EX-001"]\n+++\n',
                bundle + "/copy/VREC-EX-999.md": "a copied fixture, not a formal record",
            }
            for name, text in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(text.encode())
            git(root, "add", ".")
            git(root, "commit", "-qm", "evidence fixture")
            (root / bundle / "output.log").write_text("dirty", encoding="utf-8")
            before = git(root, "status", "--porcelain")
            result = inventory(root)
            self.assertEqual(10000 + len(files[bundle + "/copy/VREC-EX-999.md"]), result["evidence_bytes"])
            self.assertEqual(["RLS-EX-001", "VREC-EX-001"], result["bundles"][0]["records"])
            self.assertNotIn("VREC-EX-999", result["records"])
            self.assertEqual(before, git(root, "status", "--porcelain"))
            self.assertEqual("dirty", (root / bundle / "output.log").read_text())

    def test_run_keeps_full_logs_small_summaries_and_the_actual_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            init_repository(root)
            package = root / "se_harness"
            package.mkdir()
            (package / "__init__.py").write_text('__version__ = "test-version"\n')
            git(root, "add", ".")
            git(root, "commit", "-qm", "source fixture")
            sha = git(root, "rev-parse", "HEAD").strip()
            for code in (0, 7):
                output = Path(temporary) / f"run-{code}"
                result = subprocess.run([
                    sys.executable, str(ROOT / "scripts/record_evidence.py"),
                    "--repository", str(root), "--candidate", sha, "--output", str(output),
                    "--artifact", "test-raw", "--retention-days", "14", "--", "-c",
                    f"print('x' * 1000000); print('useful failure detail'); raise SystemExit({code})",
                ], capture_output=True, env={**os.environ, "GITHUB_RUN_ID": "123", "GITHUB_REPOSITORY": "owner/project"})
                self.assertEqual(code, result.returncode, result.stderr)
                summary = json.loads((output / "summary.json").read_text())
                self.assertLess((output / "summary.json").stat().st_size, 6000)
                self.assertGreater((output / "output.log").stat().st_size, 1000000)
                self.assertEqual("pass" if code == 0 else "fail", summary["result"])
                self.assertEqual(sha, summary["candidate"])
                self.assertEqual("clean", summary["working_tree"])
                self.assertEqual("test-version", summary["checker"]["version"])
                self.assertEqual(str(package / "__init__.py"), summary["checker"]["origin"])
                self.assertIn("useful failure detail", summary["output_tail"])
                self.assertEqual("test-raw", summary["raw"]["download_command"][-1])
                self.assertIn("not yet confirmed", summary["raw"]["availability"])
            self.assertEqual("", git(root, "status", "--porcelain"))

    def test_missing_or_expired_raw_results_are_unavailable_even_after_a_pass(self):
        summary = dict(result="pass", raw=dict(run_id="123", repository="owner/project",
                                             artifact="raw", download_command=["gh", "run", "download", "123"]))
        for artifacts, expected in (([], "unavailable"),
                                    ([dict(name="raw", expired=True)], "unavailable"),
                                    ([dict(name="raw", expired=False, expires_at="2026-09-28T00:00:00Z")], "available for download")):
            with patch("scripts.record_evidence.subprocess.check_output", return_value=json.dumps([dict(artifacts=artifacts)])):
                self.assertEqual(expected, raw_status(summary)["availability"])
        with patch("scripts.record_evidence.subprocess.check_output", side_effect=OSError("offline")):
            self.assertEqual("unavailable", raw_status(summary)["availability"])


if __name__ == "__main__":
    unittest.main()
