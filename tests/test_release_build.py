from __future__ import annotations

import base64
import gzip
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import zipfile

from se_harness import __version__


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

    def test_portable_skill_distribution_surface_is_explicit_and_unique(self) -> None:
        pyproject = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        data_files = pyproject["tool"]["setuptools"]["data-files"]
        prefix = "share/se-harness/templates/repository/standard/.agents/skills/harness-orient"
        distributed = [
            relative
            for destination, relatives in data_files.items()
            if destination == prefix or destination.startswith(prefix + "/")
            for relative in relatives
        ]
        self.assertEqual(
            [
                "templates/repository/standard/.agents/skills/harness-orient/SKILL.md",
                "templates/repository/standard/.agents/skills/harness-orient/skill-contract.json",
                "templates/repository/standard/.agents/skills/harness-orient/scripts/orient.py",
            ],
            distributed,
        )
        self.assertEqual(len(distributed), len(set(distributed)))
        manifest = (REPOSITORY_ROOT / "MANIFEST.in").read_text(encoding="utf-8")
        self.assertIn(
            "recursive-include templates/repository/standard/.agents/skills/harness-orient *.json *.md *.py",
            manifest,
        )
        self.assertFalse((REPOSITORY_ROOT / "se_harness/skills").exists())

    def test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core(self) -> None:
        def record_digest(raw: bytes) -> str:
            encoded = base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b"=")
            return "sha256=" + encoded.decode("ascii")

        with tempfile.TemporaryDirectory(prefix="se-harness-non-promotable-") as temporary:
            root = Path(temporary)
            wheel_dir = root / "non-promotable-ephemeral-wheel"
            wheel_dir.mkdir()
            wheel = wheel_dir / f"se_harness-{__version__}-py3-none-any.whl"
            distribution = f"se_harness-{__version__}.dist-info"
            data_prefix = f"se_harness-{__version__}.data/data/share/se-harness/templates/repository/standard"
            members: dict[str, bytes] = {}
            for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*")):
                if path.is_file() and path.suffix in {".py", ".json"}:
                    members[f"se_harness/{path.name}"] = path.read_bytes()
            template_root = REPOSITORY_ROOT / "templates/repository/standard"
            for path in sorted(template_root.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    members[f"{data_prefix}/{path.relative_to(template_root).as_posix()}"] = path.read_bytes()
            members[f"{distribution}/METADATA"] = (
                "Metadata-Version: 2.1\n"
                "Name: se-harness\n"
                f"Version: {__version__}\n"
                "Requires-Python: >=3.11\n"
            ).encode("utf-8")
            members[f"{distribution}/WHEEL"] = (
                "Wheel-Version: 1.0\n"
                "Generator: verifier-owned-non-promotable-fixture\n"
                "Root-Is-Purelib: true\n"
                "Tag: py3-none-any\n"
            ).encode("utf-8")
            members[f"{distribution}/entry_points.txt"] = b"[console_scripts]\nharnessctl = se_harness.cli:main\n"
            record_path = f"{distribution}/RECORD"
            record_lines = [
                f"{name},{record_digest(raw)},{len(raw)}"
                for name, raw in sorted(members.items())
            ]
            record_lines.append(f"{record_path},,")
            members[record_path] = ("\n".join(record_lines) + "\n").encode("utf-8")
            with zipfile.ZipFile(wheel, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, raw in sorted(members.items()):
                    archive.writestr(name, raw)

            with zipfile.ZipFile(wheel) as archive:
                skill_members = [
                    name
                    for name in archive.namelist()
                    if "/.agents/skills/harness-orient/" in name
                ]
                self.assertEqual(
                    [
                        f"{data_prefix}/.agents/skills/harness-orient/SKILL.md",
                        f"{data_prefix}/.agents/skills/harness-orient/scripts/orient.py",
                        f"{data_prefix}/.agents/skills/harness-orient/skill-contract.json",
                    ],
                    skill_members,
                )
                self.assertFalse(any("/se_harness/skills/" in name for name in archive.namelist()))

            environment = root / "fresh-environment"
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, cwd=root)
            python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
            installed = subprocess.run(
                [str(python), "-I", "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, installed.returncode, installed.stderr)
            target = root / "fresh-repository"
            initialized = subprocess.run(
                [str(python), "-I", "-m", "se_harness", "init", str(target), "--project-name", "Wheel Fixture"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, initialized.returncode, initialized.stderr)
            for relative in ("SKILL.md", "scripts/orient.py", "skill-contract.json"):
                source = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-orient" / relative
                self.assertEqual(source.read_bytes(), (target / ".agents/skills/harness-orient" / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
