"""Composition boundaries with inert synthetic packages; native smoke is separate."""
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import build_plugin_marketplace as market
from repository_tools import plugin_distribution as pkg


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="marketplace-tests-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.repo = self.base / "source"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Marketplace fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.catalogs = {
            ".agents/plugins/marketplace.json": {"name": "se-harness", "plugins": [{"name": "verity-plane",
                "source": {"source": "local", "path": "./packages/codex/verity-plane"}}]},
            ".claude-plugin/marketplace.json": {"name": "se-harness", "plugins": [{"name": "verity-plane",
                "source": "./packages/claude/verity-plane"}]}}
        for name in ("README.md", "submissions/README.md", "submissions/reviewer-test-cases.md"):
            self.write("release/plugin-marketplace/" + name, "Committed fixture " + name)
        self.write("LICENSE", "Fixture license")
        self.write("docs/images/verity-plane-logo.png", b"fixture image")
        self.commit_catalogs()
        shared = {"LICENSE": b"Fixture license", "scripts/setup.py": b"# inert fixture\n",
                  "packages/se_harness-0.18.0-py3-none-any.whl": b"inert synthetic wheel"}
        shared.update({f"skills/{name}/SKILL.md": b"# inert skill\n" for name in
                       ("setup", "change", "evidence", "harness-orient", "harness-operator-brief")})
        files = {}
        for host, manifest in pkg.HOSTS.items():
            files[host] = {path: (raw, 0o644, "shared") for path, raw in shared.items()}
            files[host][manifest] = (pkg.json_bytes({"name": "verity-plane", "version": "0.1.0"}), 0o644, host)
        self.assembly = pkg.Assembly("verity-plane", {"revision": self.revision}, {"version": "0.18.0"}, files)
        self.output = self.base / "distribution"

    def git(self, *args):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-C", str(self.repo), *args]).decode().strip()

    def write(self, name, value):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value if isinstance(value, bytes) else value.encode())

    def commit_catalogs(self):
        for name, catalog in self.catalogs.items():
            self.write("release/plugin-marketplace/" + name, pkg.json_bytes(catalog))
        self.git("add", ".")
        self.git("commit", "-qm", "synthetic catalog fixture")
        self.revision = self.git("rev-parse", "HEAD")

    def test_complete_composition_preserves_native_output_and_committed_assets(self):
        # Uncommitted changes cannot become publication contents.
        self.write("release/plugin-marketplace/README.md", "uncommitted replacement")
        result = market.compose(self.repo, self.assembly, self.output)
        self.assertTrue(result["accepted"])
        self.assertEqual((self.output / "README.md").read_text(), "Committed fixture README.md")
        plain = self.base / "native"
        self.assertEqual(result["archives"], pkg.build(self.assembly, plain)["archives"])
        for path in plain.rglob("*"):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (self.output / "packages" / path.relative_to(plain)).read_bytes())
        identity = json.loads((self.output / "PACKAGE-IDENTITY.json").read_bytes())
        actual = {p.relative_to(self.output).as_posix(): pkg.digest(p.read_bytes())
                  for p in self.output.rglob("*") if p.is_file() and p.name != "PACKAGE-IDENTITY.json"}
        self.assertEqual(identity["files"], actual)
        self.assertTrue(market.compose(self.repo, self.assembly, self.output, check=True)["accepted"])

    def test_missing_escaping_and_wrong_host_sources_fail_before_output(self):
        original = deepcopy(self.catalogs)
        for source in ("./missing", "../../outside", "./packages/codex/verity-plane"):
            with self.subTest(source=source):
                self.catalogs = deepcopy(original)
                self.catalogs[".claude-plugin/marketplace.json"]["plugins"][0]["source"] = source
                self.commit_catalogs()
                self.assembly.source["revision"] = self.revision
                with self.assertRaisesRegex(pkg.AssemblyError, "catalog must select complete package"):
                    market.compose(self.repo, self.assembly, self.output)
                self.assertFalse(self.output.exists())

    def test_incomplete_package_and_version_disagreement_fail_before_output(self):
        incomplete = deepcopy(self.assembly)
        del incomplete.files["claude"]["skills/setup/SKILL.md"]
        with self.assertRaisesRegex(pkg.AssemblyError, "incomplete claude"):
            market.compose(self.repo, incomplete, self.output)
        mismatch = deepcopy(self.assembly)
        mismatch.files["claude"][pkg.HOSTS["claude"]] = (b'{"name":"verity-plane","version":"0.2.0"}', 0o644, "claude")
        with self.assertRaisesRegex(pkg.AssemblyError, "versions disagree"):
            market.compose(self.repo, mismatch, self.output)
        self.assertFalse(self.output.exists())

    def test_modified_wrapper_native_archive_and_unexpected_directory_are_refused(self):
        market.compose(self.repo, self.assembly, self.output)
        for name in ("README.md", "PACKAGE-IDENTITY.json", ".claude-plugin/marketplace.json", "packages/verity-plane-codex.zip"):
            path = self.output / name
            original = path.read_bytes()
            path.write_bytes(original + b"modified")
            with self.subTest(path=name), self.assertRaises(pkg.AssemblyError):
                market.compose(self.repo, self.assembly, self.output, check=True)
            path.write_bytes(original)
        (self.output / "unexpected").mkdir()
        with self.assertRaisesRegex(pkg.AssemblyError, "unexpected marketplace directory"):
            market.compose(self.repo, self.assembly, self.output, check=True)

    def test_existing_output_and_source_overlap_preserve_sentinel(self):
        self.output.mkdir()
        sentinel = self.output / "owner.txt"
        sentinel.write_text("preserve")
        with self.assertRaisesRegex(pkg.AssemblyError, "already exists"):
            market.compose(self.repo, self.assembly, self.output)
        with self.assertRaisesRegex(pkg.AssemblyError, "outside the source"):
            market.compose(self.repo, self.assembly, self.repo / "output")
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_redirected_and_interrupted_output_are_not_accepted(self):
        outside = self.base / "outside.txt"
        outside.write_text("preserve")
        with patch.object(market, "identity", side_effect=OSError("injected interruption")):
            with self.assertRaisesRegex(OSError, "interruption"):
                market.compose(self.repo, self.assembly, self.output)
        with self.assertRaises(pkg.AssemblyError):
            market.compose(self.repo, self.assembly, self.output, check=True)
        self.assertEqual(outside.read_text(), "preserve")
        retry = self.base / "retry"
        market.compose(self.repo, self.assembly, retry)
        (retry / "LICENSE").unlink()
        os.link(outside, retry / "LICENSE")
        with self.assertRaisesRegex(pkg.AssemblyError, "hard-linked"):
            market.compose(self.repo, self.assembly, retry, check=True)
        self.assertEqual(outside.read_text(), "preserve")


if __name__ == "__main__":
    unittest.main()
