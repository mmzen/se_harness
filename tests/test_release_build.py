from __future__ import annotations

import copy
import base64
import gzip
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from repository_tools import release_build as BUILD
from se_harness import __version__


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = REPOSITORY_ROOT / "release" / "build-recipe.json"
LOCK_PATH = REPOSITORY_ROOT / "release" / "build-toolchain.lock"
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


class BuildRecipeSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.recipe_bytes = RECIPE_PATH.read_bytes()
        self.lock_bytes = LOCK_PATH.read_bytes()
        self.recipe = json.loads(self.recipe_bytes)

    def encoded(self, value: object) -> bytes:
        return BUILD.canonical_json_bytes(value)

    def test_canonical_recipe_binds_complete_identity(self) -> None:
        recipe = BUILD.validate_recipe_bytes(
            self.recipe_bytes,
            path="release/build-recipe.json",
            lock=self.lock_bytes,
        )
        self.assertEqual(BUILD.RECIPE_SCHEMA, recipe.value["schema"])
        self.assertEqual(hashlib.sha256(self.recipe_bytes).hexdigest(), recipe.sha256)
        self.assertEqual("linux", recipe.value["producer"]["os"])
        self.assertEqual("amd64", recipe.value["producer"]["architecture"])
        self.assertRegex(recipe.image, r"@sha256:[0-9a-f]{64}\Z")
        self.assertEqual([], recipe.value["environment"]["inherit"])
        self.assertEqual(7, len(recipe.inventory))

    def test_noncanonical_duplicate_and_open_recipe_forms_fail(self) -> None:
        with self.assertRaisesRegex(BUILD.BuildRecipeError, "canonical"):
            BUILD.validate_recipe_bytes(
                json.dumps(self.recipe).encode("utf-8"),
                path="release/build-recipe.json",
                lock=self.lock_bytes,
            )
        duplicate = self.recipe_bytes.replace(
            b'{\n  "commands":', b'{\n  "schema": "duplicate",\n  "commands":', 1
        )
        with self.assertRaisesRegex(BUILD.BuildRecipeError, "duplicate key"):
            BUILD.validate_recipe_bytes(
                duplicate, path="release/build-recipe.json", lock=self.lock_bytes
            )
        for field, replacement, message in (
            ("image", "python:3.11", "immutable"),
            ("inherit", ["PATH"], "inheritance"),
            ("commands", "python -m build", "argument-array"),
        ):
            changed = copy.deepcopy(self.recipe)
            if field == "image":
                changed["producer"][field] = replacement
            elif field == "inherit":
                changed["environment"][field] = replacement
            else:
                changed[field] = replacement
            with self.subTest(field=field):
                with self.assertRaisesRegex(BUILD.BuildRecipeError, message):
                    BUILD.validate_recipe_bytes(
                        self.encoded(changed),
                        path="release/build-recipe.json",
                        lock=self.lock_bytes,
                    )

    def test_toolchain_lock_hash_and_inventory_are_closed(self) -> None:
        changed_lock = self.lock_bytes.replace(b"build==1.3.0", b"build==1.3.1")
        with self.assertRaisesRegex(BUILD.BuildRecipeError, "lock_sha256"):
            BUILD.validate_recipe_bytes(
                self.recipe_bytes,
                path="release/build-recipe.json",
                lock=changed_lock,
            )
        changed = copy.deepcopy(self.recipe)
        changed["toolchain"]["inventory"].pop()
        with self.assertRaisesRegex(BUILD.BuildRecipeError, "inventory"):
            BUILD.validate_recipe_bytes(
                self.encoded(changed),
                path="release/build-recipe.json",
                lock=self.lock_bytes,
            )

    def test_producer_executes_arrays_with_only_declared_and_internal_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            (source / "scripts").mkdir()
            producer_recipe = copy.deepcopy(self.recipe)
            producer_recipe["environment"]["fixed"]["HOME"] = (root / "home").as_posix()
            (root / "recipe.json").write_bytes(self.encoded(producer_recipe))
            shutil.copyfile(LOCK_PATH, root / "lock.txt")
            (source / "scripts" / "normalize_sdist.py").write_text("# fixture\n", encoding="utf-8")
            install_environment: dict[str, str] = {}
            build_environments: list[dict[str, str]] = []

            def execute(
                arguments: list[str],
                *,
                timeout: int,
                environment: dict[str, str],
                cwd: Path,
            ) -> object:
                self.assertIn(timeout, {300, 600})
                self.assertEqual(source, cwd)
                if arguments[1:3] == ["-m", "pip"]:
                    install_environment.update(environment)
                elif arguments[1:3] == ["-m", "build"]:
                    build_environments.append(dict(environment))
                    raw = Path(arguments[arguments.index("--outdir") + 1])
                    (raw / "se_harness-1.2.3-py3-none-any.whl").write_bytes(b"wheel")
                    (raw / "se_harness-1.2.3.tar.gz").write_bytes(b"raw-sdist")
                else:
                    build_environments.append(dict(environment))
                    Path(arguments[3]).write_bytes(b"normalized-sdist")
                return subprocess.CompletedProcess(arguments, 0, "", "")

            with (
                mock.patch.object(BUILD, "_bounded_run", side_effect=execute),
                mock.patch.object(BUILD, "_installed_inventory") as inventory,
                mock.patch.object(BUILD.platform, "system", return_value="Linux"),
                mock.patch.object(BUILD.platform, "machine", return_value="x86_64"),
                mock.patch.object(BUILD.platform, "python_implementation", return_value="CPython"),
                mock.patch.object(BUILD.platform, "python_version", return_value="3.11.9"),
                mock.patch.object(BUILD.struct, "calcsize", return_value=8),
            ):
                inventory.return_value = BUILD.validate_recipe_bytes(
                    self.recipe_bytes,
                    path="release/build-recipe.json",
                    lock=self.lock_bytes,
                ).inventory
                BUILD._producer(
                    root / "recipe.json",
                    root / "lock.txt",
                    source,
                    root / "final",
                    "1.2.3",
                    1710000000,
                    root / "producer.json",
                )
            declared = set(self.recipe["environment"]["fixed"]) | {"SOURCE_DATE_EPOCH"}
            self.assertEqual(declared, set(install_environment))
            self.assertEqual(2, len(build_environments))
            for environment in build_environments:
                self.assertEqual(declared | {"PYTHONPATH"}, set(environment))
            self.assertTrue((root / "producer.json").is_file())


class ReplayBuildTests(unittest.TestCase):
    def repository(self, root: Path) -> str:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Harness Test"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "harness@example.invalid"], check=True)
        (root / "release").mkdir()
        shutil.copyfile(RECIPE_PATH, root / "release" / "build-recipe.json")
        shutil.copyfile(LOCK_PATH, root / "release" / "build-toolchain.lock")
        (root / "source.txt").write_text("candidate\n", encoding="utf-8", newline="\n")
        subprocess.run(["git", "-C", str(root), "add", "release", "source.txt"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "candidate"], check=True)
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    @staticmethod
    def fake_docker_build(
        _control: Path,
        workspace: Path,
        recipe: BUILD.BuildRecipe,
        version: str,
        _epoch: int,
    ) -> dict[str, object]:
        final = workspace / "final"
        final.mkdir()
        wheel = recipe.value["outputs"]["wheel"].format(version=version)
        sdist = recipe.value["outputs"]["sdist"].format(version=version)
        (final / wheel).write_bytes(b"exact-wheel")
        (final / sdist).write_bytes(b"exact-sdist")
        return {"schema": "se-harness-release-build-producer/v1", "recipe_sha256": recipe.sha256}

    def test_two_fresh_producers_equal_accepted_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            container = Path(temporary)
            root = container / "repository"
            root.mkdir()
            commit = self.repository(root)
            output = container / "out" / "bundle"
            with (
                mock.patch.object(BUILD, "_docker_image_identity", side_effect=lambda image: image),
                mock.patch.object(BUILD, "_docker_build", side_effect=self.fake_docker_build) as producer,
            ):
                result = BUILD.replay_build(
                    root,
                    commit,
                    "1.2.3",
                    output,
                    expected_wheel_sha256=hashlib.sha256(b"exact-wheel").hexdigest(),
                    expected_sdist_sha256=hashlib.sha256(b"exact-sdist").hexdigest(),
                )
            self.assertEqual(2, producer.call_count)
            self.assertEqual("exact", result["state"])
            self.assertEqual(BUILD.REPLAY_SCHEMA, result["schema"])
            self.assertEqual("se-harness-release-bundle/v2", result["manifest"]["schema"])
            self.assertEqual(
                {"SHA256SUMS", "se_harness-1.2.3-py3-none-any.whl", "se_harness-1.2.3.tar.gz"},
                {path.name for path in output.iterdir()},
            )

    def test_expected_hash_is_immutable_and_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            container = Path(temporary)
            root = container / "repository"
            root.mkdir()
            commit = self.repository(root)
            with (
                mock.patch.object(BUILD, "_docker_image_identity", side_effect=lambda image: image),
                mock.patch.object(BUILD, "_docker_build", side_effect=self.fake_docker_build),
            ):
                with self.assertRaisesRegex(BUILD.BuildRecipeError, "accepted hash"):
                    BUILD.replay_build(
                        root,
                        commit,
                        "1.2.3",
                        container / "bundle",
                        expected_wheel_sha256="0" * 64,
                        expected_sdist_sha256=hashlib.sha256(b"exact-sdist").hexdigest(),
                    )
            self.assertFalse((container / "bundle").exists())

    def test_output_inside_candidate_repository_is_refused_before_docker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            commit = self.repository(root)
            with mock.patch.object(BUILD, "_docker_image_identity") as docker:
                with self.assertRaisesRegex(BUILD.BuildRecipeError, "outside the repository"):
                    BUILD.replay_build(root, commit, "1.2.3", root / "bundle")
            docker.assert_not_called()


class ReplayWorkflowTests(unittest.TestCase):
    def test_ready_replay_has_one_input_read_permission_and_no_credentials(self) -> None:
        workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "release-candidate-replay.yml"
        ).read_text(encoding="utf-8")
        self.assertEqual(1, workflow.count("        required: true\n"))
        self.assertIn("      release_record:\n", workflow)
        self.assertIn("      contents: read\n", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("python scripts/replay_release_build.py", workflow)
        self.assertIn("python scripts/validate_engineering_artifacts.py --root .", workflow)
        self.assertIn("python scripts/validate_release_distributions.py", workflow)
        self.assertIn("--require-status ready", workflow)
        self.assertIn("release-build-replay.json", workflow)
        for forbidden in (
            "contents: write",
            "id-token: write",
            "environment:",
            "secrets.",
            "python -m build",
            "pip install",
            "normalize_sdist.py",
            "git push",
            "gh release",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, workflow)
        action_lines = [line.strip() for line in workflow.splitlines() if "uses:" in line]
        self.assertTrue(action_lines)
        for line in action_lines:
            with self.subTest(line=line):
                self.assertRegex(line, r"@[0-9a-f]{40}(?:\s|$)")


if __name__ == "__main__":
    unittest.main()
