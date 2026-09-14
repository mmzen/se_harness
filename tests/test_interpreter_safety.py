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
PERMITTED_PACKAGE_IMPORTS = frozenset()
PERMITTED_TOOLS_IMPORTS = frozenset()
LOADER_MODULES = frozenset({"se_harness/interpreter_safety.py"})

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

    def test_identity_has_no_python_binary_digest_and_ignores_unused_pythonpath(self):
        with mock.patch.dict(os.environ, {"PYTHONPATH": "unused-setting"}), mock.patch("se_harness.runtime_identity.site.ENABLE_USER_SITE", False):
            report = runtime_identity.inspect_runtime_identity(role="candidate-source", expected_version=runtime_identity.__version__, expected_root=REPOSITORY_ROOT, checkout_root=REPOSITORY_ROOT, candidate_commit="a" * 40)
        self.assertNotIn("python_binary_sha256", report.to_dict())
        self.assertNotIn("RID008", {item.code for item in report.diagnostics})
        self.assertTrue(report.python_version)

class ImportBarrierTests(unittest.TestCase):
    @staticmethod
    def _imported(package: str) -> dict[str, set[str]]:
        found: dict[str, set[str]] = {}
        for source in sorted((REPOSITORY_ROOT / package).glob("*.py")):
            relative = source.relative_to(REPOSITORY_ROOT).as_posix()
            names: set[str] = set()
            for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    names.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and not node.level:
                    module = node.module or ""
                    names.update(f"{module}.{alias.name}" for alias in node.names)
            found[relative] = names
        return found

    def test_repository_tools_imports_only_the_standard_library_and_its_own_package(self) -> None:
        crossings: set[str] = set()
        for relative, names in self._imported("repository_tools").items():
            for name in sorted(names):
                head = name.split(".")[0]
                if head == "repository_tools":
                    continue
                if head == "se_harness":
                    crossings.add(name)
                    continue
                with self.subTest(module=relative, imported=name):
                    self.assertIn(head, sys.stdlib_module_names, f"{relative} imports {name}")
        self.assertEqual(
            sorted(PERMITTED_PACKAGE_IMPORTS),
            sorted(crossings),
            "the repository_tools -> se_harness crossing inventory changed",
        )

    def test_no_crossing_from_repository_tools_into_the_package_remains(self) -> None:
        # WO-REB-028: the deleted modules held the only se_harness.hash_bound import.
        self.assertEqual(frozenset(), PERMITTED_PACKAGE_IMPORTS)
        for relative, names in self._imported("repository_tools").items():
            with self.subTest(module=relative):
                self.assertEqual(
                    set(), {name for name in names if name.split(".")[0] == "se_harness"}
                )

    def test_no_crossing_from_the_package_into_repository_tools_remains(self) -> None:
        # WO-REB-028: qualify_predecessor_view held the one guarded function-local
        # import. The package neither names nor needs repository_tools now, at any
        # import level, so an installed evaluator has nothing left to refuse.
        self.assertEqual(frozenset(), PERMITTED_TOOLS_IMPORTS)
        crossings: set[str] = set()
        for relative, names in self._imported("se_harness").items():
            for name in sorted(names):
                if name.split(".")[0] == "repository_tools":
                    crossings.add(f"{relative}: {name}")
        self.assertEqual(set(), crossings)

    def test_neither_package_crossing_carries_an_interpreter_safety_name(self) -> None:
        for name in sorted(PERMITTED_PACKAGE_IMPORTS | PERMITTED_TOOLS_IMPORTS):
            with self.subTest(imported=name):
                self.assertNotIn("interpreter_safety", name)

    def test_neither_loader_imports_the_other_runtime(self) -> None:
        for relative in sorted(LOADER_MODULES):
            with self.subTest(module=relative):
                source = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
                for node in ast.walk(ast.parse(source)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertIn(alias.name.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.ImportFrom) and not node.level:
                        head = (node.module or "").split(".")[0]
                        self.assertIn(head, sys.stdlib_module_names, f"{relative}: {node.module}")
