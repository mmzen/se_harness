from __future__ import annotations

import gzip
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NORMALIZER = REPOSITORY_ROOT / "scripts/normalize_sdist.py"
FIXED_EPOCH = 1_700_000_000


class DeterministicSdistTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def add_member(
        self,
        archive: tarfile.TarFile,
        name: str,
        *,
        data: bytes | None,
        seed: int,
    ) -> None:
        member = tarfile.TarInfo(name)
        member.mtime = 1_600_000_000 + seed
        member.uid = 1000 + seed
        member.gid = 2000 + seed
        member.uname = f"builder-{seed}"
        member.gname = f"group-{seed}"
        member.pax_headers = {"comment": f"build-{seed}"}
        if data is None:
            member.type = tarfile.DIRTYPE
            member.mode = 0o755
            archive.addfile(member)
        else:
            member.mode = 0o644
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))

    def write_sdist(
        self,
        path: Path,
        *,
        seed: int,
        reverse: bool = False,
    ) -> None:
        members = [
            ("sample-1.0", None),
            ("sample-1.0/package", None),
            ("sample-1.0/package/__init__.py", b'VERSION = "1.0"\n'),
            ("sample-1.0/pyproject.toml", b"[build-system]\n"),
        ]
        if reverse:
            members.reverse()
        with path.open("wb") as raw:
            with gzip.GzipFile(
                filename=f"raw-build-{seed}.tar",
                mode="wb",
                fileobj=raw,
                mtime=1_500_000_000 + seed,
            ) as compressed:
                with tarfile.open(
                    fileobj=compressed,
                    mode="w",
                    format=tarfile.PAX_FORMAT,
                ) as archive:
                    for name, data in members:
                        self.add_member(archive, name, data=data, seed=seed)

    def invoke(self, source: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(NORMALIZER),
                str(source),
                str(output),
                "--epoch",
                str(FIXED_EPOCH),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_normalization_is_reproducible_and_preserves_payload(self) -> None:
        raw_a = self.root / "raw-a.tar.gz"
        raw_b = self.root / "raw-b.tar.gz"
        output_a = self.root / "normalized-a.tar.gz"
        output_b = self.root / "normalized-b.tar.gz"
        self.write_sdist(raw_a, seed=1)
        self.write_sdist(raw_b, seed=2, reverse=True)

        first = self.invoke(raw_a, output_a)
        second = self.invoke(raw_b, output_b)

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(output_a.read_bytes(), output_b.read_bytes())
        header = output_a.read_bytes()[:10]
        self.assertEqual(b"\x1f\x8b", header[:2])
        self.assertEqual(0, header[3] & gzip.FNAME)
        self.assertEqual(FIXED_EPOCH, int.from_bytes(header[4:8], "little"))

        with tarfile.open(output_a, "r:gz") as archive:
            members = archive.getmembers()
            self.assertEqual(sorted(item.name for item in members), [item.name for item in members])
            for member in members:
                self.assertEqual(FIXED_EPOCH, member.mtime)
                self.assertEqual(0, member.uid)
                self.assertEqual(0, member.gid)
                self.assertEqual("", member.uname)
                self.assertEqual("", member.gname)
                self.assertEqual({}, member.pax_headers)
            payload = archive.extractfile("sample-1.0/package/__init__.py")
            self.assertIsNotNone(payload)
            assert payload is not None
            self.assertEqual(b'VERSION = "1.0"\n', payload.read())

    def test_rejects_unsafe_duplicate_and_special_members_atomically(self) -> None:
        cases = [
            ("unsafe", [("sample/../escape", b"unsafe")]),
            ("duplicate", [("sample/file", b"one"), ("sample/file", b"two")]),
            ("symlink", [("sample/link", "symlink")]),
        ]
        for label, members in cases:
            with self.subTest(label=label):
                source = self.root / f"{label}.tar.gz"
                output = self.root / f"{label}-normalized.tar.gz"
                with tarfile.open(source, "w:gz") as archive:
                    for name, value in members:
                        member = tarfile.TarInfo(name)
                        if value == "symlink":
                            member.type = tarfile.SYMTYPE
                            member.linkname = "target"
                            archive.addfile(member)
                        else:
                            assert isinstance(value, bytes)
                            member.size = len(value)
                            archive.addfile(member, io.BytesIO(value))

                result = self.invoke(source, output)
                self.assertEqual(2, result.returncode)
                self.assertFalse(output.exists())

    def test_refuses_to_overwrite_existing_output(self) -> None:
        source = self.root / "raw.tar.gz"
        output = self.root / "normalized.tar.gz"
        self.write_sdist(source, seed=1)
        output.write_bytes(b"repository-owned")

        result = self.invoke(source, output)

        self.assertEqual(2, result.returncode)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(b"repository-owned", output.read_bytes())


if __name__ == "__main__":
    unittest.main()
