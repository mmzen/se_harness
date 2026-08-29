"""Evidence for REQ-TST-003 (WO-TST-002): the cached fixture install equals a direct init."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from se_harness.cli import main
from tests import fixture_support
from tests.fixture_support import standard_repository


def _tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class FixtureSupportTests(unittest.TestCase):
    def test_copies_are_byte_identical_to_a_direct_init_and_init_runs_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            direct = base / "direct"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", str(direct), "--project-name", "Cache Equality"]))
            before = len(fixture_support.initialisations())
            first = standard_repository(base / "first", "Cache Equality")
            second = standard_repository(base / "second", "Cache Equality")
            self.assertEqual(before + 1, len(fixture_support.initialisations()))  # one init for two copies
            self.assertEqual(_tree(direct), _tree(first))
            self.assertEqual(_tree(first), _tree(second))
            self.assertIn(".engineering-harness.lock", _tree(first))
            # 46 installed files and the lock: WO-ECP-006 retired the three writing skills (15 files).
            self.assertEqual(47, len(_tree(first)))

    def test_destination_must_be_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            occupied = Path(temporary) / "occupied"
            occupied.mkdir()
            (occupied / "keep.txt").write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not empty"):
                standard_repository(occupied, "Cache Equality")
            self.assertEqual("x", (occupied / "keep.txt").read_text(encoding="utf-8"))

    def test_a_removed_cache_directory_is_reinitialised(self) -> None:
        import shutil

        cached = fixture_support._initialise("Cache Reinit")
        shutil.rmtree(cached)
        again = fixture_support._initialise("Cache Reinit")
        self.assertTrue(again.is_dir())
        self.assertTrue((again / ".engineering-harness.lock").is_file())


if __name__ == "__main__":
    unittest.main()
