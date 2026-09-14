"""Supported interpreter paths and the independent package import barrier."""
from __future__ import annotations
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv
from pathlib import Path
from unittest import mock
from se_harness import interpreter_safety, runtime_identity
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

def link_directory(alias, target):
    if os.name == "nt":
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(alias), str(target)], capture_output=True, text=True)
        if result.returncode:
            raise unittest.SkipTest("directory junction unavailable: " + result.stderr)
    else:
        alias.symlink_to(target, target_is_directory=True)

class InterpreterPathsTests(unittest.TestCase):
    def test_real_external_environment_runs_through_linked_parent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            real = root / "environment"
            venv.EnvBuilder(with_pip=False).create(real)
            python = real / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            query = subprocess.run([str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], check=True, capture_output=True, text=True)
            packages = Path(query.stdout.strip())
            shutil.copytree(REPOSITORY_ROOT / "se_harness", packages / "se_harness", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(REPOSITORY_ROOT / "templates", real / "share/se-harness/templates")
            metadata = packages / f"se_harness-{runtime_identity.__version__}.dist-info"
            metadata.mkdir()
            (metadata / "METADATA").write_text(f"Metadata-Version: 2.1\nName: se-harness\nVersion: {runtime_identity.__version__}\n", encoding="utf-8")
            alias = root / "linked"
            link_directory(alias, real)
            selected = alias / python.relative_to(real)
            result = subprocess.run([str(selected), "-I", "-m", "se_harness", "identity", "--role", "candidate-package", "--expected-version", runtime_identity.__version__, "--expected-root", str(real), "--checkout-root", str(REPOSITORY_ROOT), "--candidate-commit", "a" * 40, "--require-isolated-python", "--json"], env={**os.environ, "PYTHONPATH": str(REPOSITORY_ROOT)}, cwd=root, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            value = json.loads(result.stdout)
            self.assertTrue(value["passed"])
            self.assertIsNone(value["entry_point_origin"])
            self.assertNotIn("python_binary_sha256", value)
            evidence_code = "from pathlib import Path; import sys; from se_harness.runtime_identity import inspect_runtime_identity; from se_harness.evaluator_evidence import build_evaluator_evidence; r=inspect_runtime_identity(role='released-evaluator',expected_version=sys.argv[1],expected_root=Path(sys.argv[2]),checkout_root=Path(sys.argv[3]),verify_payload=False); print(build_evaluator_evidence(r).canonical_bytes.decode())"
            result = subprocess.run([str(selected), "-I", "-c", evidence_code, runtime_identity.__version__, str(real), str(REPOSITORY_ROOT)], env={**os.environ, "PYTHONPATH": str(REPOSITORY_ROOT)}, cwd=root, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            value = json.loads(result.stdout)
            self.assertTrue(value["origins"]["python_executable"].startswith("<evaluator-root>/"))
            self.assertEqual("origin-version", value["inspection"])

    def test_linked_environment_retains_its_entry_point(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            real = root / "real"
            entry = real / "bin/python"
            entry.parent.mkdir(parents=True)
            entry.write_bytes(b"interpreter")
            alias = root / "linked"
            link_directory(alias, real)
            selected = alias / "bin/python"
            observed = interpreter_safety.evaluate(selected, declared_root=real, checkout_root=root / "checkout")
            self.assertEqual(selected, observed.entry_point)
            self.assertEqual(entry, observed.resolved_target)
            self.assertFalse(hasattr(observed, "binary_sha256"))

    @unittest.skipIf(os.name == "nt", "POSIX virtualenv entry point")
    def test_terminal_python_link_keeps_the_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            entry = root / "env/bin/python"
            entry.parent.mkdir(parents=True)
            entry.symlink_to(Path(sys.executable).resolve())
            observed = interpreter_safety.evaluate(entry, declared_root=root / "env")
            self.assertEqual(root / "env", observed.environment_root)
            self.assertEqual(entry, observed.entry_point)

    def test_missing_directory_and_checkout_interpreters_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            entry = root / "checkout/bin/python"
            entry.parent.mkdir(parents=True)
            entry.write_bytes(b"python")
            for path, kwargs in [(root / "missing", {}), (entry.parent, {}), (entry, {"checkout_root": root / "checkout"}), (entry, {"declared_root": root / "elsewhere"})]:
                with self.subTest(path=path, kwargs=kwargs), self.assertRaises(interpreter_safety.InterpreterSafetyRefusal):
                    interpreter_safety.evaluate(path, **kwargs)

    def test_unavailable_path_resolution_reports_one_clear_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            entry = Path(temporary) / "env/bin/python"
            with mock.patch.object(Path, "resolve", side_effect=OSError("path resolution unavailable")):
                with self.assertRaisesRegex(interpreter_safety.InterpreterSafetyRefusal, "EPS003.*does not resolve"):
                    interpreter_safety.evaluate(entry)

class ImportBarrierTests(unittest.TestCase):
    def test_package_and_repository_tools_remain_independent(self) -> None:
        # These are packaging dependencies: the installed wheel omits repository_tools,
        # and the release producer cannot depend on the candidate package it builds.
        for package, forbidden in (("se_harness", "repository_tools"), ("repository_tools", "se_harness")):
            for source in sorted((REPOSITORY_ROOT / package).rglob("*.py")):
                for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                    names = []
                    if isinstance(node, ast.Import):
                        names = [alias.name for alias in node.names]
                    elif isinstance(node, ast.ImportFrom) and not node.level:
                        names = [node.module or ""]
                    for name in names:
                        with self.subTest(module=source.name, imported=name):
                            self.assertNotEqual(forbidden, name.split(".")[0])


if __name__ == "__main__":
    unittest.main()
