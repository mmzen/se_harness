"""The suite's own shape (SPEC-TST-002 TST-HYG-001 to TST-HYG-003, TST-HYG-008).

Every defined test is discovered exactly once, no class that carries tests is
subclassed, no test module imports another test module, and no test module
extends `sys.path` when it is imported. Everything here is read from the loaded
modules, never from their source text.
"""

from __future__ import annotations

import importlib
import inspect
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def _leaves(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _leaves(item)
        else:
            yield item


def _is_test_module(name: str) -> bool:
    return name.startswith("test_") or name.startswith("tests.test_")


class SuiteHygieneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        loader = unittest.TestLoader()
        cls.prefix = loader.testMethodPrefix
        # every module under its `tests.` name, the one the support modules use, so nothing is imported twice
        suite = unittest.TestSuite()
        for path in sorted(TESTS.glob("test_*.py")):
            suite.addTests(loader.loadTestsFromModule(importlib.import_module(f"tests.{path.stem}")))
        cls.leaves = list(_leaves(suite))
        cls.failed = [item for item in cls.leaves if type(item).__name__ == "_FailedTest"]
        cls.classes = sorted({type(item) for item in cls.leaves if type(item).__name__ != "_FailedTest"}, key=lambda c: (c.__module__, c.__qualname__))

    def own_tests(self, case: type) -> list[str]:
        return sorted(name for name, value in vars(case).items() if name.startswith(self.prefix) and callable(value))

    def test_every_module_loads(self) -> None:
        self.assertEqual([], [item.id() for item in self.failed])

    def test_every_defined_test_is_discovered_exactly_once(self) -> None:
        # TST-HYG-002: the loader's count equals the count of defined methods, class by class.
        discovered: dict[type, list[str]] = {}
        for item in self.leaves:
            if type(item).__name__ != "_FailedTest":
                discovered.setdefault(type(item), []).append(item._testMethodName)
        defined_total = 0
        for case in self.classes:
            with self.subTest(case=f"{case.__module__}.{case.__qualname__}"):
                self.assertEqual(self.own_tests(case), sorted(discovered[case]))
            defined_total += len(self.own_tests(case))
        self.assertEqual(defined_total, sum(len(names) for names in discovered.values()))

    def test_no_class_that_carries_tests_is_subclassed(self) -> None:
        # TST-HYG-001: shared setup lives in a mixin or a test-free base class.
        for case in self.classes:
            for base in case.__mro__[1:]:
                if base is unittest.TestCase or not issubclass(base, unittest.TestCase):
                    continue
                with self.subTest(case=case.__qualname__, base=base.__qualname__):
                    self.assertEqual([], self.own_tests(base), f"{base.__qualname__} carries tests and is subclassed by {case.__qualname__}")

    def test_no_test_module_imports_another_test_module(self) -> None:
        # TST-HYG-003: helpers live in support modules; a test module is never a library.
        offenders: list[str] = []
        for module_name in sorted({case.__module__ for case in self.classes}):
            module = sys.modules[module_name]
            for attribute, value in vars(module).items():
                origin = getattr(value, "__module__", None)
                if not (inspect.isclass(value) or inspect.isfunction(value)) or not isinstance(origin, str):
                    continue
                if origin != module_name and _is_test_module(origin) and origin.split(".")[-1] != module_name.split(".")[-1]:
                    offenders.append(f"{module_name} imports {attribute} from {origin}")
        self.assertEqual([], offenders)

    def test_no_test_module_extends_sys_path_at_import(self) -> None:
        # TST-HYG-008: the engine and the repository scripts are loaded by path, never by search.
        # A fresh interpreter imports every test module and reports what the imports added.
        script = "\n".join(
            (
                "import sys, importlib, pathlib",
                "before = list(sys.path)",
                "for path in sorted(pathlib.Path('tests').glob('test_*.py')):",
                "    importlib.import_module(f'tests.{path.stem}')",
                "print(chr(10).join(entry for entry in sys.path if entry not in before))",
            )
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=600,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        # A repository script loaded by path may extend the path for its own siblings; a test
        # module may not reach the engine or the scripts directory that way.
        forbidden = {(ROOT / "se_harness" / "engine").resolve(), (ROOT / "scripts").resolve()}
        added = [line for line in completed.stdout.splitlines() if line.strip()]
        offenders = [entry for entry in added if Path(entry).resolve() in forbidden]
        self.assertEqual([], offenders, f"imports put a searched directory on sys.path: {added}")
