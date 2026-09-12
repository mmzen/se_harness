"""Exploratory boundary checks, run against both original and chunked readers."""
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

sys.path.insert(0, str(Path(sys.argv.pop(1)).resolve()))
from se_harness import skill_ownership as ownership


class ReadBoundaries(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='bounded-reader-')
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / 'input.bin'
        self.path.write_bytes(b'a' * 70000)

    def after_first_read(self, callback):
        original = os.fdopen
        class Reader:
            def __init__(self, *args, **kwargs):
                self.handle = original(*args, **kwargs)
                self.called = False
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return self.handle.__exit__(*args)
            def fileno(self):
                return self.handle.fileno()
            def read(self, size):
                raw = self.handle.read(size)
                if not self.called:
                    self.called = True
                    callback()
                return raw
        return mock.patch.object(ownership.os, 'fdopen', Reader)

    def test_exact_bytes_at_chunk_and_size_boundaries(self):
        for size in (0, 1, 65535, 65536, 65537, 131073, ownership.MAX_FILE):
            with self.subTest(size=size):
                expected = (b'0123456789abcdef' * ((size + 15) // 16))[:size]
                self.path.write_bytes(expected)
                self.assertEqual(expected, ownership._read(self.path, limit=size))

    def test_existing_oversize_refuses_before_open(self):
        with mock.patch.object(ownership.os, 'open') as opened:
            with self.assertRaises(ownership.OwnershipError):
                ownership._read(self.path, limit=69999)
            opened.assert_not_called()

    def test_growth_during_read_refuses(self):
        def grow():
            with self.path.open('ab') as stream:
                stream.write(b'x' * 40000)
        with self.after_first_read(grow), self.assertRaises(ownership.OwnershipError):
            ownership._read(self.path, limit=80000)
        self.assertEqual(110000, self.path.stat().st_size)

    def test_truncation_during_read_refuses(self):
        def shrink():
            with self.path.open('r+b') as stream:
                stream.truncate(10)
        with self.after_first_read(shrink), self.assertRaises(ownership.OwnershipError):
            ownership._read(self.path)
        self.assertEqual(10, self.path.stat().st_size)

    def test_changed_timestamp_during_read_refuses(self):
        before = self.path.stat()
        def touch():
            os.utime(self.path, ns=(before.st_atime_ns, before.st_mtime_ns + 10000000000))
        with self.after_first_read(touch), self.assertRaises(ownership.OwnershipError):
            ownership._read(self.path)
        self.assertNotEqual(before.st_mtime_ns, self.path.stat().st_mtime_ns)

    def test_opened_identity_mismatch_refuses(self):
        before = self.path.stat()
        changed = SimpleNamespace(st_dev=before.st_dev, st_ino=before.st_ino + 1, st_nlink=1)
        with mock.patch.object(ownership.os, 'fstat', return_value=changed):
            with self.assertRaises(ownership.OwnershipError):
                ownership._read(self.path)

    def test_final_path_identity_mismatch_refuses(self):
        before = self.path.stat()
        changed = SimpleNamespace(st_dev=before.st_dev, st_ino=before.st_ino + 1)
        with mock.patch.object(ownership, '_ordinary', side_effect=[before, changed]):
            with self.assertRaises(ownership.OwnershipError):
                ownership._read(self.path)

    def test_hard_link_refuses(self):
        os.link(self.path, self.path.with_name('alias.bin'))
        with self.assertRaises(ownership.OwnershipError):
            ownership._read(self.path)

    def test_read_error_refuses(self):
        def fail():
            raise OSError('injected read error')
        with self.after_first_read(fail), self.assertRaises(ownership.OwnershipError):
            ownership._read(self.path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
