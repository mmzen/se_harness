"""Focused boundary tests. Synthetic wheel fixtures are not release evidence.

Run with a Python environment containing the selected released se-harness;
the builder calls its canonical hash function in an isolated subprocess.
"""
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from repository_tools import plugin_distribution as pkg


def git(root, *args):
    run = subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(root), *args],
                         capture_output=True, check=True)
    return run.stdout.decode().strip()


def synthetic_wheel():
    result = io.BytesIO()
    with zipfile.ZipFile(result, "w") as archive:
        archive.writestr("se_harness/__init__.py", "# synthetic, never imported\n")
        archive.writestr("se_harness-1.2.3.data/data/share/se-harness/templates/repository/standard/README.md", "fixture\n")
        archive.writestr("se_harness-1.2.3.dist-info/METADATA", "Metadata-Version: 2.1\nName: se-harness\nVersion: 1.2.3\n")
    return result.getvalue()


class PackageAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="assembly-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "source"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "fixture@example.invalid")
        git(self.repo, "config", "user.name", "Assembly fixture")
        self.wheel = self.base / "se_harness-1.2.3-py3-none-any.whl"
        self.wheel.write_bytes(synthetic_wheel())
        self.sha = hashlib.sha256(self.wheel.read_bytes()).hexdigest()
        self.write("release.md", ('+++\ntype = "release_record"\nstatus = "released"\nversion = "1.2.3"\n'
                   '[distribution]\nwheel = "' + self.wheel.name + '"\nwheel_sha256 = "' + self.sha + '"\n+++\n'))
        self.write("shared.py", "# shared fixture\n")
        self.write("README.md", "Synthetic test fixture, not a production plugin.\n")
        for host in pkg.HOSTS:
            self.write(f"{host}.json", json.dumps({"name": "test-plugin"}))
        self.plan = {"schema": pkg.SCHEMA, "name": "test-plugin",
                     "shared": {"scripts/shared.py": "shared.py", "README.md": "README.md"},
                     "hosts": {host: {manifest: f"{host}.json"} for host, manifest in pkg.HOSTS.items()}}
        self.commit_plan()
        self.release_revision = self.revision
        self.out = self.base / "output"

    def write(self, path, value):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value if isinstance(value, bytes) else value.encode())

    def commit_plan(self):
        self.write("plan.json", pkg.json_bytes(self.plan))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "synthetic fixture", "--allow-empty")
        self.revision = git(self.repo, "rev-parse", "HEAD")

    def prepare(self, **changes):
        args = dict(repository=self.repo, revision=self.revision, plan_path="plan.json",
                    release_revision=self.release_revision, release_record="release.md",
                    expected_wheel_sha256=self.sha, wheel=self.wheel,
                    evaluator_python=Path(sys.executable).absolute())
        args.update(changes)
        return pkg.prepare(**args)

    def test_same_source_wheel_and_deterministic_archives(self):
        assembly = self.prepare()
        first = pkg.build(assembly, self.out)
        second = pkg.build(self.prepare(), self.base / "repeat")
        self.assertEqual(first["archives"], second["archives"])
        self.assertEqual(assembly.source["revision"], self.revision)
        for host, own in pkg.HOSTS.items():
            folder = self.out / host / assembly.name
            inventory = json.loads((folder / pkg.INVENTORY).read_bytes())
            self.assertEqual(inventory["evaluator"]["archive_sha256"], self.sha)
            self.assertEqual((folder / "packages" / self.wheel.name).read_bytes(), self.wheel.read_bytes())
            self.assertIn(own, inventory["files"])
            self.assertNotIn(pkg.HOSTS["claude" if host == "codex" else "codex"], inventory["files"])
            for destination, source in self.plan["shared"].items():
                self.assertEqual((folder / destination).read_bytes(), (self.repo / source).read_bytes())
            with zipfile.ZipFile(self.out / f"{assembly.name}-{host}.zip") as archive:
                for path, entry in inventory["files"].items():
                    info = archive.getinfo(f"{assembly.name}/{path}")
                    self.assertEqual(hashlib.sha256(archive.read(info)).hexdigest(), entry["sha256"])
                    self.assertEqual((info.external_attr >> 16) & 0o777, entry["mode"])

    def test_missing_and_corrupt_wheel(self):
        self.wheel.unlink()
        with self.assertRaisesRegex(pkg.AssemblyError, "missing.*wheel"):
            self.prepare()
        self.wheel.write_bytes(synthetic_wheel() + b"changed")
        with self.assertRaisesRegex(pkg.AssemblyError, "SHA-256 mismatch"):
            self.prepare()
        self.assertFalse(self.out.exists())

    def test_git_executable_mode_and_host_only_scripts(self):
        for host in pkg.HOSTS:
            self.write(f"{host}.py", f"# {host} integration fixture\n")
            self.plan["hosts"][host][f"scripts/{host}.py"] = f"{host}.py"
        self.commit_plan()
        git(self.repo, "update-index", "--chmod=+x", "shared.py")
        git(self.repo, "commit", "-qm", "executable shared source")
        self.revision = git(self.repo, "rev-parse", "HEAD")
        assembly = self.prepare()
        pkg.build(assembly, self.out)
        for host in pkg.HOSTS:
            foreign = "claude" if host == "codex" else "codex"
            with zipfile.ZipFile(self.out / f"test-plugin-{host}.zip") as archive:
                executable = archive.getinfo("test-plugin/scripts/shared.py")
                self.assertEqual((executable.external_attr >> 16) & 0o777, 0o755)
                self.assertIn(f"test-plugin/scripts/{host}.py", archive.namelist())
                self.assertNotIn(f"test-plugin/scripts/{foreign}.py", archive.namelist())

    def test_independent_release_identity_required(self):
        for changes, message in [({"expected_wheel_sha256": "0" * 64}, "disagrees"),
                                 ({"revision": "HEAD"}, "immutable"),
                                 ({"release_revision": "main"}, "immutable"),
                                 ({"evaluator_python": Path("python")}, "absolute")]:
            with self.subTest(changes=changes), self.assertRaisesRegex(pkg.AssemblyError, message):
                self.prepare(**changes)
        self.write("release.md", (self.repo / "release.md").read_text().replace('status = "released"', 'status = "draft"'))
        self.commit_plan()
        with self.assertRaisesRegex(pkg.AssemblyError, "not released"):
            self.prepare(release_revision=self.revision)

    def test_forbidden_inputs(self):
        original = deepcopy(self.plan)
        for path, raw in [("runtime/python.exe", b"MZruntime"), ("bin/run.py", b"# script"),
                          ("packages/candidate.whl", b"PK\x03\x04"), ("assets/dependency.whl", b"PK\x03\x04"),
                          ("scripts/site-packages/vendor.py", b"# library"), ("assets/python.png", b"\x7fELF"),
                          ("scripts/payload.py", b"\xff\0binary")]:
            with self.subTest(path=path):
                self.plan = deepcopy(original)
                self.plan["shared"][path] = "forbidden"
                self.write("forbidden", raw)
                self.commit_plan()
                with self.assertRaisesRegex(pkg.AssemblyError, "forbidden|unsupported|non-text|executable"):
                    self.prepare()
                self.assertFalse(self.out.exists())

    def test_committed_source_only_and_missing_source(self):
        self.write("shared.py", "uncommitted change\n")
        assembly = self.prepare()
        self.assertEqual(assembly.files["codex"]["scripts/shared.py"][0], b"# shared fixture\n")
        self.plan["shared"]["scripts/shared.py"] = "absent.py"
        self.commit_plan()
        with self.assertRaisesRegex(pkg.AssemblyError, "missing committed source: absent.py"):
            self.prepare()

    def test_conflicts_host_separation_and_manifest_name(self):
        original = deepcopy(self.plan)
        for destination, source in [("scripts/shared.py", "shared.py"), ("Scripts/Shared.py", "shared.py"),
                                    ("scripts/shared.py/child.py", "shared.py"),
                                    (".claude-plugin/plugin.json", "claude.json")]:
            self.plan = deepcopy(original)
            self.plan["hosts"]["codex"][destination] = source
            self.commit_plan()
            with self.subTest(destination=destination), self.assertRaisesRegex(pkg.AssemblyError, "conflicting|forbidden"):
                self.prepare()
        self.plan = original
        self.write("codex.json", '{"name":"another-plugin"}')
        self.commit_plan()
        with self.assertRaisesRegex(pkg.AssemblyError, "manifest name"):
            self.prepare()

    def test_unsafe_paths_preserve_outside_sentinel(self):
        sentinel = self.base / "sentinel.txt"
        sentinel.write_bytes(b"keep me")
        listing = sorted(p.name for p in self.base.iterdir())
        original = deepcopy(self.plan)
        for path in ["../sentinel.txt", "/sentinel.txt", "C:/sentinel.txt", "scripts/../sentinel.txt",
                     "scripts\\sentinel.txt", "scripts/NUL.txt", "scripts/name.", "scripts//name.py"]:
            self.plan = deepcopy(original)
            self.plan["shared"][path] = "shared.py"
            self.commit_plan()
            with self.subTest(path=path), self.assertRaisesRegex(pkg.AssemblyError, "unsafe path"):
                self.prepare()
            self.assertEqual(sentinel.read_bytes(), b"keep me")
            self.assertEqual(sorted(p.name for p in self.base.iterdir()), listing)

    def test_altered_output_and_omitted_inventory_entry(self):
        assembly = self.prepare()
        pkg.build(assembly, self.out)
        target = self.out / "claude/test-plugin/scripts/shared.py"
        target.write_bytes(b"divergent")
        with self.assertRaisesRegex(pkg.AssemblyError, "shared.py"):
            pkg.accept(assembly, self.out)
        target.write_bytes(b"# shared fixture\n")
        inventory_path = self.out / "codex/test-plugin" / pkg.INVENTORY
        inventory = json.loads(inventory_path.read_bytes())
        del inventory["files"]["scripts/shared.py"]
        inventory_path.write_bytes(pkg.json_bytes(inventory))
        with self.assertRaisesRegex(pkg.AssemblyError, "missing entries.*scripts/shared.py"):
            pkg.accept(assembly, self.out)

    def test_extra_file_archive_change_and_false_inventory_digest(self):
        assembly = self.prepare()
        pkg.build(assembly, self.out)
        target = self.out / "extra.py"
        target.write_bytes(b"# extra")
        with self.assertRaisesRegex(pkg.AssemblyError, "extra.py"):
            pkg.accept(assembly, self.out)
        target.unlink()
        archive = self.out / "test-plugin-codex.zip"
        raw = archive.read_bytes()
        archive.write_bytes(raw + b"changed")
        with self.assertRaisesRegex(pkg.AssemblyError, "test-plugin-codex.zip"):
            pkg.accept(assembly, self.out)
        archive.write_bytes(raw)
        target = self.out / "codex/test-plugin" / pkg.INVENTORY
        inventory = json.loads(target.read_bytes())
        inventory["files"]["scripts/shared.py"]["sha256"] = "0" * 64
        target.write_bytes(pkg.json_bytes(inventory))
        with self.assertRaisesRegex(pkg.AssemblyError, pkg.INVENTORY):
            pkg.accept(assembly, self.out)

    def test_interruption_is_not_accepted_and_fresh_retry_rechecked(self):
        assembly = self.prepare()
        original_write = pkg._write
        count = 0

        def interrupted(path, raw):
            nonlocal count
            if count == 1:
                raise OSError("injected interruption after first file")
            original_write(path, raw)
            count += 1

        with patch.object(pkg, "_write", interrupted), self.assertRaisesRegex(OSError, "interruption"):
            pkg.build(assembly, self.out)
        with self.assertRaisesRegex(pkg.AssemblyError, "incomplete"):
            pkg.accept(self.prepare(), self.out)
        before = sorted(p.relative_to(self.out).as_posix() for p in self.out.rglob("*"))
        with self.assertRaisesRegex(pkg.AssemblyError, "already exists"):
            pkg.build(assembly, self.out)
        self.assertEqual(before, sorted(p.relative_to(self.out).as_posix() for p in self.out.rglob("*")))
        self.assertTrue(pkg.build(self.prepare(), self.base / "retry")["accepted"])

    def test_output_links_are_rejected(self):
        assembly = self.prepare()
        pkg.build(assembly, self.out)
        source = self.out / "codex/test-plugin/scripts/shared.py"
        link = self.out / "hard-link.py"
        os.link(source, link)
        with self.assertRaisesRegex(pkg.AssemblyError, "hard-linked"):
            pkg.accept(assembly, self.out)
        # Exercise junction detection even with the Python 3.11 pathlib API.
        fake = type("FileStat", (), {"st_file_attributes": stat.FILE_ATTRIBUTE_REPARSE_POINT})()
        with patch.object(Path, "lstat", return_value=fake), self.assertRaisesRegex(pkg.AssemblyError, "linked output"):
            pkg._safe_directory(self.base / "junction/output")

    def test_git_symlink_is_not_read(self):
        oid = git(self.repo, "hash-object", "-w", "shared.py")
        git(self.repo, "update-index", "--add", "--cacheinfo", f"120000,{oid},linked.py")
        self.plan["shared"]["scripts/linked.py"] = "linked.py"
        self.write("plan.json", pkg.json_bytes(self.plan))
        git(self.repo, "add", "plan.json")
        git(self.repo, "commit", "-qm", "symlink fixture")
        self.revision = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(pkg.AssemblyError, "regular committed file"):
            self.prepare()

    def test_duplicate_json_key_and_malformed_release(self):
        self.write("plan.json", '{"schema":1,"schema":2}')
        git(self.repo, "add", "plan.json")
        git(self.repo, "commit", "-qm", "duplicate key")
        self.revision = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(pkg.AssemblyError, "duplicate JSON"):
            self.prepare()
        self.write("release.md", '+++\nversion="1.2.3"\ndistribution=[]\n+++')
        self.commit_plan()
        with self.assertRaisesRegex(pkg.AssemblyError, "invalid released evaluator record"):
            self.prepare(release_revision=self.revision)

    def test_candidate_evaluator_is_never_imported(self):
        marker = self.base / "candidate-executed"
        self.write("se_harness/__init__.py", f'from pathlib import Path\nPath({str(marker)!r}).touch()\nraise RuntimeError("candidate")\n')
        self.commit_plan()
        with patch.dict(os.environ, {"PYTHONPATH": str(self.repo)}):
            self.prepare()
        self.assertFalse(marker.exists())

    def test_cli_build_check_and_refusal(self):
        args = [sys.executable, "-B", str(ROOT / "scripts/build_plugin_archives.py"), "build",
                "--repository", str(self.repo), "--revision", self.revision, "--plan", "plan.json",
                "--release-revision", self.release_revision, "--release-record", "release.md",
                "--expected-wheel-sha256", self.sha, "--wheel", str(self.wheel),
                "--evaluator-python", sys.executable, "--output-directory", str(self.out)]
        run = subprocess.run(args, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)["accepted"])
        args[3] = "check"
        run = subprocess.run(args, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        (self.out / "test-plugin-codex.zip").unlink()
        run = subprocess.run(args, capture_output=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertFalse(json.loads(run.stderr)["accepted"])


if __name__ == "__main__":
    unittest.main()
