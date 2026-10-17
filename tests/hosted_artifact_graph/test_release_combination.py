"""Synthetic identity boundaries; actual package/service qualification is separate."""
import copy
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sandbox_qualification", ROOT / "server/scripts/qualify.py")
qualify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qualify)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class ReleaseCombinationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-combination-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "source"
        self.repo.mkdir()
        self.git("init", "-q")
        (self.repo / "se_harness").mkdir()
        self.source("0.23.0")
        self.wheel = self.base / "se_harness-0.23.0-py3-none-any.whl"
        self.write_wheel()
        self.replay = {"candidate": {"commit": self.commit}, "manifest": {
            "commit": self.commit, "version": "0.23.0", "wheel": self.wheel.name,
            "wheel_sha256": digest(self.wheel.read_bytes())},
            "builds": [{"wheel_sha256": digest(self.wheel.read_bytes())} for _ in range(2)]}

    def git(self, *args):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
            "-c", "user.name=Release fixture", "-c", "user.email=fixture@example.invalid", *args],
            cwd=self.repo, stderr=subprocess.PIPE).decode().strip()

    def source(self, version, module_version=None):
        (self.repo / "pyproject.toml").write_text(f'[project]\nversion = "{version}"\n')
        (self.repo / "se_harness/__init__.py").write_text(f'__version__ = "{module_version or version}"\n')
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic client version", "--allow-empty")
        self.commit = self.git("rev-parse", "HEAD")

    def write_wheel(self, version="0.23.0", name="se-harness", extra=""):
        with zipfile.ZipFile(self.wheel, "w") as archive:
            archive.writestr(f"se_harness-{version}.dist-info/METADATA",
                f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n{extra}")
            archive.writestr("se_harness/__init__.py", "# synthetic; never imported\n")

    def test_release_client_matches_committed_versions_and_two_builds(self):
        self.assertEqual(qualify.client_identity(self.repo, self.commit, self.wheel, self.replay),
                         {"version": "0.23.0", "wheel_sha256": digest(self.wheel.read_bytes())})

    def test_development_client_still_uses_its_actual_version(self):
        self.source("0.22.2")
        self.wheel = self.base / "se_harness-0.22.2-py3-none-any.whl"
        self.write_wheel("0.22.2")
        value = digest(self.wheel.read_bytes())
        replay = {"candidate": {"commit": self.commit}, "manifest": {"commit": self.commit,
                  "version": "0.22.2", "wheel": self.wheel.name, "wheel_sha256": value},
                  "builds": [{"wheel_sha256": value}, {"wheel_sha256": value}]}
        self.assertEqual("0.22.2", qualify.client_identity(self.repo, self.commit, self.wheel, replay)["version"])

    def test_source_and_module_version_disagreement_are_refused(self):
        for project, module in [("0.22.2", "0.22.2"), ("0.23.0", "0.22.2")]:
            self.source(project, module)
            with self.subTest(project=project, module=module), self.assertRaisesRegex(ValueError, "committed source"):
                qualify.client_identity(self.repo, self.commit, self.wheel, self.replay)

    def test_wrong_or_ambiguous_wheel_metadata_is_refused(self):
        for name, extra in [("unrelated", ""), ("se-harness", "Version: 0.23.0\n")]:
            self.write_wheel(name=name, extra=extra)
            with self.subTest(name=name, extra=extra), self.assertRaisesRegex(ValueError, "one se-harness"):
                qualify.client_identity(self.repo, self.commit, self.wheel, self.replay)
        self.write_wheel()
        with zipfile.ZipFile(self.wheel, "a") as archive:
            archive.writestr("another.dist-info/METADATA", "Name: unrelated\n")
        with self.assertRaisesRegex(ValueError, "one distribution"):
            qualify.client_identity(self.repo, self.commit, self.wheel, self.replay)

    def test_wrong_replay_commit_version_filename_and_digest_are_refused(self):
        cases = [("candidate", "commit", "0" * 40), ("manifest", "commit", "0" * 40),
                 ("manifest", "version", "0.22.2"), ("manifest", "wheel", "other.whl"),
                 ("manifest", "wheel_sha256", "0" * 64)]
        for section, key, value in cases:
            replay = copy.deepcopy(self.replay); replay[section][key] = value
            with self.subTest(section=section, key=key), self.assertRaisesRegex(ValueError, "replay does not bind"):
                qualify.client_identity(self.repo, self.commit, self.wheel, replay)
        for builds in [[], self.replay["builds"][:1], [{"wheel_sha256": "0" * 64}] * 2]:
            replay = {**self.replay, "builds": builds}
            with self.assertRaisesRegex(ValueError, "Both pinned builds"):
                qualify.client_identity(self.repo, self.commit, self.wheel, replay)

    def test_renamed_wheel_is_refused(self):
        renamed = self.base / "wrong.whl"; renamed.write_bytes(self.wheel.read_bytes())
        with self.assertRaisesRegex(ValueError, "filename"):
            qualify.client_identity(self.repo, self.commit, renamed, self.replay)

    def test_dirty_source_stops_before_any_build(self):
        (self.repo / "unexpected.txt").write_text("uncommitted")
        output = self.base / "dirty-output"
        with self.assertRaisesRegex(ValueError, "Commit the reviewed implementation"):
            qualify.prepare(SimpleNamespace(repository=self.repo, output=output))
        self.assertEqual({"source-commit.json", "source-status.json"}, {p.name for p in output.iterdir()})

    def test_staging_options_are_all_or_none(self):
        names = ("plugin_marketplace", "client_bundle", "evaluator_python")
        for selected in itertools.product((False, True), repeat=3):
            args = SimpleNamespace(**{name: self.base if flag else None for name, flag in zip(names, selected)})
            if any(selected) and not all(selected):
                with self.subTest(selected=selected), self.assertRaisesRegex(ValueError, "together"):
                    qualify.staged_plugin_inputs(args)
            else:
                self.assertEqual(all(selected), qualify.staged_plugin_inputs(args))

    def staged_pair(self, entry="verity-plane/skills/setup/SKILL.md"):
        marketplace = self.base / "marketplace"; (marketplace / "packages").mkdir(parents=True)
        accepted = {"archives": {}}
        for host in ("codex", "claude"):
            path = marketplace / "packages" / f"verity-plane-{host}.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(entry, b"exact staged instruction bytes\r\n")
            accepted["archives"][path.name] = digest(path.read_bytes())
        return marketplace, accepted

    def test_checked_staged_bytes_are_preserved_for_both_hosts(self):
        marketplace, accepted = self.staged_pair(); output = self.base / "snapshots"
        qualify.snapshot_plugins(marketplace, output, accepted)
        for host in ("codex", "claude"):
            name = f"verity-plane-{host}.zip"
            self.assertEqual((marketplace / "packages" / name).read_bytes(), (output / name).read_bytes())
            self.assertEqual(b"exact staged instruction bytes\r\n", (output / host / "verity-plane/skills/setup/SKILL.md").read_bytes())

    def test_changed_or_missing_staged_archive_refuses_before_snapshot(self):
        marketplace, accepted = self.staged_pair(); output = self.base / "snapshots"
        archive = marketplace / "packages/verity-plane-claude.zip"
        original = archive.read_bytes(); archive.write_bytes(original + b"changed")
        with self.assertRaisesRegex(ValueError, "changed after"):
            qualify.snapshot_plugins(marketplace, output, accepted)
        self.assertFalse(output.exists())
        archive.unlink()
        with self.assertRaises(FileNotFoundError):
            qualify.snapshot_plugins(marketplace, output, accepted)
        self.assertFalse(output.exists())

    def test_unsafe_archive_path_refuses_before_snapshot(self):
        marketplace, accepted = self.staged_pair("verity-plane/../../outside")
        output = self.base / "snapshots"
        with self.assertRaisesRegex(ValueError, "archive path"):
            qualify.snapshot_plugins(marketplace, output, accepted)
        self.assertFalse(output.exists())

    def test_development_assembly_keeps_selected_evaluator(self):
        output = self.base / "development"
        evaluator = {"version": "0.23.0", "archive_sha256": digest(self.wheel.read_bytes())}
        def run(_label, argv):
            return subprocess.check_output([str(x) for x in argv], cwd=self.base)
        wheel, observed = qualify.prepare_plugins(SimpleNamespace(evaluator_wheel=self.wheel),
            ROOT, ROOT, self.commit, {}, evaluator, output, run)
        self.assertEqual(self.wheel, wheel); self.assertEqual(evaluator, observed)
        for host in ("codex", "claude"):
            with zipfile.ZipFile(output / f"verity-plane-{host}.zip") as archive:
                self.assertIn("verity-plane/DEVELOPMENT.md", archive.namelist())
                self.assertEqual(self.wheel.read_bytes(), archive.read("verity-plane/packages/" + self.wheel.name))


if __name__ == "__main__":
    unittest.main()
