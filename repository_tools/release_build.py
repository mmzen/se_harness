"""Strict interpreter for repository-owned, recipe-bound release builds."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence


RECIPE_SCHEMA = "se-harness-release-build-recipe/v1"
REPLAY_SCHEMA = "se-harness-release-build-replay/v1"
DEFAULT_RECIPE_PATH = "release/build-recipe.json"
MAX_RECIPE_BYTES = 128 * 1024
MAX_LOCK_BYTES = 128 * 1024
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
IMAGE_PATTERN = re.compile(
    r"[a-z0-9]+(?:[._/-][a-z0-9]+)*@sha256:(?P<digest>[0-9a-f]{64})"
)
VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
PACKAGE_PATTERN = re.compile(r"[a-z0-9]+(?:[._-][a-z0-9]+)*")
LOCK_LINE_PATTERN = re.compile(
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)==(?P<version>[A-Za-z0-9][A-Za-z0-9._+-]*)"
    r" --hash=sha256:(?P<sha256>[0-9a-f]{64})"
)
RECIPE_KEYS = frozenset(
    {"schema", "producer", "python", "toolchain", "environment", "commands", "normalization", "outputs"}
)
DECLARED_SOURCE_DIRECTORY_MODE = 0o775
DECLARED_SOURCE_FILE_MODE = 0o664


class BuildRecipeError(RuntimeError):
    """The build recipe or its execution violates repository release policy."""


@dataclass(frozen=True)
class BuildRecipe:
    value: dict[str, Any]
    raw: bytes
    sha256: str
    path: str
    lock: bytes
    lock_sha256: str

    @property
    def image(self) -> str:
        return str(self.value["producer"]["image"])

    @property
    def inventory(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (_package_name(item["name"]), str(item["version"]))
            for item in self.value["toolchain"]["inventory"]
        )


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildRecipeError(f"build recipe contains duplicate key: {key}")
        result[key] = value
    return result


def _exact_keys(value: Any, expected: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BuildRecipeError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unexpected {', '.join(extra)}")
        raise BuildRecipeError(f"{label} fields are invalid ({'; '.join(details)})")
    return value


def _safe_posix_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise BuildRecipeError(f"{label} must be a safe repository-relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        raise BuildRecipeError(f"{label} must be a safe repository-relative POSIX path")
    return value


def _scalar_string(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 4096
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise BuildRecipeError(f"{label} must be a bounded printable string")
    return value


def _package_name(value: Any) -> str:
    name = _scalar_string(value, "toolchain package name").lower().replace("_", "-").replace(".", "-")
    if PACKAGE_PATTERN.fullmatch(name) is None:
        raise BuildRecipeError("toolchain package name is invalid")
    return name


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_toolchain_lock(payload: bytes) -> tuple[tuple[str, str, str], ...]:
    if not payload or len(payload) > MAX_LOCK_BYTES:
        raise BuildRecipeError("build toolchain lock is empty or too large")
    if payload.startswith(b"\xef\xbb\xbf") or b"\r" in payload or not payload.endswith(b"\n"):
        raise BuildRecipeError("build toolchain lock must be BOM-free canonical LF text")
    try:
        lines = payload.decode("utf-8").splitlines()
    except UnicodeError as exc:
        raise BuildRecipeError("build toolchain lock must be UTF-8") from exc
    entries: list[tuple[str, str, str]] = []
    names: set[str] = set()
    for line in lines:
        match = LOCK_LINE_PATTERN.fullmatch(line)
        if match is None:
            raise BuildRecipeError("build toolchain lock contains a non-canonical requirement")
        name = _package_name(match.group("name"))
        if name in names:
            raise BuildRecipeError(f"build toolchain lock repeats package: {name}")
        names.add(name)
        entries.append((name, match.group("version"), match.group("sha256")))
    if entries != sorted(entries):
        raise BuildRecipeError("build toolchain lock entries must be sorted")
    return tuple(entries)


def validate_recipe_bytes(payload: bytes, *, path: str, lock: bytes) -> BuildRecipe:
    if not payload or len(payload) > MAX_RECIPE_BYTES:
        raise BuildRecipeError("build recipe is empty or too large")
    if payload.startswith(b"\xef\xbb\xbf") or b"\r" in payload or not payload.endswith(b"\n"):
        raise BuildRecipeError("build recipe must be BOM-free canonical LF JSON")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=_duplicate_safe_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BuildRecipeError("build recipe must be valid UTF-8 JSON") from exc
    if canonical_json_bytes(value) != payload:
        raise BuildRecipeError("build recipe JSON is not canonical")
    recipe = _exact_keys(value, RECIPE_KEYS, "build recipe")
    if recipe["schema"] != RECIPE_SCHEMA:
        raise BuildRecipeError(f"build recipe schema must be {RECIPE_SCHEMA}")

    producer = _exact_keys(recipe["producer"], frozenset({"image", "os", "architecture"}), "producer")
    image = _scalar_string(producer["image"], "producer image")
    if IMAGE_PATTERN.fullmatch(image) is None:
        raise BuildRecipeError("producer image must use one immutable sha256 digest")
    if producer["os"] != "linux" or producer["architecture"] != "amd64":
        raise BuildRecipeError("producer platform must be linux/amd64")

    runtime = _exact_keys(recipe["python"], frozenset({"implementation", "version", "pointer_bits"}), "python")
    if runtime["implementation"] != "CPython" or not isinstance(runtime["version"], str) or VERSION_PATTERN.fullmatch(runtime["version"]) is None:
        raise BuildRecipeError("python must name an exact CPython patch version")
    if runtime["pointer_bits"] != 64:
        raise BuildRecipeError("python pointer_bits must be 64")

    toolchain = _exact_keys(recipe["toolchain"], frozenset({"installer", "inventory", "lock", "lock_sha256"}), "toolchain")
    installer = _exact_keys(toolchain["installer"], frozenset({"name", "version"}), "toolchain installer")
    if installer["name"] != "pip" or not isinstance(installer["version"], str):
        raise BuildRecipeError("toolchain installer must be exact pip")
    lock_path = _safe_posix_path(toolchain["lock"], "toolchain lock")
    lock_hash = toolchain["lock_sha256"]
    if not isinstance(lock_hash, str) or SHA256_PATTERN.fullmatch(lock_hash) is None or lock_hash != _sha256_bytes(lock):
        raise BuildRecipeError("toolchain lock_sha256 differs from the raw lock bytes")
    lock_entries = parse_toolchain_lock(lock)
    inventory_value = toolchain["inventory"]
    if not isinstance(inventory_value, list) or not inventory_value:
        raise BuildRecipeError("toolchain inventory must be a non-empty array")
    inventory: list[tuple[str, str]] = []
    for item in inventory_value:
        entry = _exact_keys(item, frozenset({"name", "version"}), "toolchain inventory entry")
        name = _package_name(entry["name"])
        version = _scalar_string(entry["version"], "toolchain package version")
        inventory.append((name, version))
    if inventory != sorted(set(inventory)):
        raise BuildRecipeError("toolchain inventory must be sorted and unique")
    if inventory != [(name, version) for name, version, _digest in lock_entries]:
        raise BuildRecipeError("toolchain inventory differs from the complete hash-locked inventory")
    if ("pip", str(installer["version"])) not in inventory:
        raise BuildRecipeError("toolchain inventory must include the exact installer")

    environment = _exact_keys(recipe["environment"], frozenset({"fixed", "derived", "inherit"}), "environment")
    if environment["inherit"] != []:
        raise BuildRecipeError("build environment inheritance must be empty")
    fixed = _exact_keys(
        environment["fixed"],
        frozenset({"HOME", "LANG", "LC_ALL", "PATH", "PYTHONDONTWRITEBYTECODE", "PYTHONHASHSEED", "TZ"}),
        "fixed environment",
    )
    for name, item in fixed.items():
        _scalar_string(item, f"fixed environment {name}")
    derived = _exact_keys(environment["derived"], frozenset({"SOURCE_DATE_EPOCH"}), "derived environment")
    if derived["SOURCE_DATE_EPOCH"] != "candidate.committer_epoch":
        raise BuildRecipeError("SOURCE_DATE_EPOCH must derive from candidate.committer_epoch")

    expected_commands = [
        {
            "argv": ["python", "-m", "pip", "install", "--disable-pip-version-check", "--no-cache-dir", "--only-binary=:all:", "--require-hashes", "--target", "{toolchain_dir}", "-r", "{toolchain_lock}"],
            "cwd": "{source}",
            "id": "install-toolchain",
        },
        {
            "argv": ["python", "-m", "build", "--wheel", "--sdist", "--no-isolation", "--outdir", "{raw_output}", "."],
            "cwd": "{source}",
            "id": "build-distributions",
        },
        {
            "argv": ["python", "scripts/normalize_sdist.py", "{raw_sdist}", "{final_sdist}", "--epoch", "{source_date_epoch}"],
            "cwd": "{source}",
            "id": "normalize-sdist",
        },
    ]
    if recipe["commands"] != expected_commands:
        raise BuildRecipeError("commands must equal the closed v1 argument-array contract")

    normalization = _exact_keys(
        recipe["normalization"],
        frozenset({"algorithm", "archive_format", "gzip_compresslevel", "gzip_filename", "member_order", "owner_gid", "owner_gname", "owner_uid", "owner_uname", "pax_headers", "path", "timestamp"}),
        "normalization",
    )
    expected_normalization = {
        "algorithm": "se-harness-normalize-sdist/v1", "archive_format": "pax", "gzip_compresslevel": 9,
        "gzip_filename": "empty", "member_order": "lexicographic", "owner_gid": 0, "owner_gname": "",
        "owner_uid": 0, "owner_uname": "", "pax_headers": "empty", "path": "scripts/normalize_sdist.py",
        "timestamp": "source_date_epoch",
    }
    if normalization != expected_normalization:
        raise BuildRecipeError("normalization differs from the supported v1 contract")
    _safe_posix_path(normalization["path"], "normalizer path")

    outputs = _exact_keys(recipe["outputs"], frozenset({"wheel", "sdist", "checksums", "manifest_schema", "replay_schema"}), "outputs")
    if outputs != {
        "wheel": "se_harness-{version}-py3-none-any.whl", "sdist": "se_harness-{version}.tar.gz",
        "checksums": "SHA256SUMS", "manifest_schema": "se-harness-release-bundle/v2", "replay_schema": REPLAY_SCHEMA,
    }:
        raise BuildRecipeError("outputs differ from the supported v1 contract")
    return BuildRecipe(recipe, payload, _sha256_bytes(payload), _safe_posix_path(path, "build recipe"), lock, lock_hash)


def _run_git(repository: Path, *arguments: str, binary: bool = False) -> str | bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=False,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise BuildRecipeError("Git command failed to start") from exc
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip() or "Git command failed"
        raise BuildRecipeError(detail[:8192])
    return completed.stdout if binary else completed.stdout.decode("utf-8", "strict").strip()


def _git_blob(repository: Path, commit: str, path: str) -> bytes:
    value = _run_git(repository, "show", f"{commit}:{path}", binary=True)
    assert isinstance(value, bytes)
    return value


def load_build_recipe_at(
    repository: Path,
    commit: str,
    *,
    path: str = DEFAULT_RECIPE_PATH,
    expected_sha256: str | None = None,
) -> BuildRecipe:
    root = repository.resolve(strict=True)
    recipe_path = _safe_posix_path(path, "build recipe")
    payload = _git_blob(root, commit, recipe_path)
    try:
        preview = json.loads(payload.decode("utf-8"), object_pairs_hook=_duplicate_safe_object)
        lock_path = _safe_posix_path(preview["toolchain"]["lock"], "toolchain lock")
    except (KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        raise BuildRecipeError("cannot resolve toolchain lock from build recipe") from exc
    recipe = validate_recipe_bytes(payload, path=recipe_path, lock=_git_blob(root, commit, lock_path))
    if expected_sha256 is not None and recipe.sha256 != expected_sha256:
        raise BuildRecipeError("build recipe hash differs from the bound identity")
    return recipe


def _safe_extract_candidate(repository: Path, commit: str, destination: Path) -> None:
    archive = destination.parent / f"{destination.name}.tar"
    _run_git(
        repository, "-c", "core.autocrlf=false", "-c", "core.eol=lf",
        "archive", "--format=tar", f"--output={archive}", commit,
    )
    destination.mkdir()
    try:
        with tarfile.open(archive, "r:") as source:
            members = source.getmembers()
            if not members:
                raise BuildRecipeError("candidate archive is empty")
            names: set[str] = set()
            for member in members:
                path = PurePosixPath(member.name)
                canonical = path.as_posix().rstrip("/")
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or "\\" in member.name
                    or not canonical
                    or canonical != member.name.rstrip("/")
                    or ":" in path.parts[0]
                    or canonical in names
                ):
                    raise BuildRecipeError("candidate archive contains an unsafe path")
                names.add(canonical)
                if not (member.isfile() or member.isdir()):
                    raise BuildRecipeError("candidate archive contains an unsupported member type")
            source.extractall(destination)
    finally:
        archive.unlink(missing_ok=True)


def _bounded_run(
    arguments: Sequence[str],
    *,
    timeout: int = 1200,
    environment: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        with tempfile.TemporaryFile() as standard_output, tempfile.TemporaryFile() as standard_error:
            raw = subprocess.run(
                list(arguments),
                check=False,
                stdout=standard_output,
                stderr=standard_error,
                timeout=timeout,
                env=os.environ.copy() if environment is None else environment,
                cwd=cwd,
            )
            streams: list[str] = []
            for stream in (standard_output, standard_error):
                size = stream.tell()
                stream.seek(max(0, size - 8192))
                streams.append(stream.read(8192).decode("utf-8", "replace"))
            completed = subprocess.CompletedProcess(
                raw.args,
                raw.returncode,
                stdout=streams[0],
                stderr=streams[1],
            )
    except (OSError, subprocess.SubprocessError) as exc:
        raise BuildRecipeError(f"command failed to start: {arguments[0]}") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "command failed").strip()[:8192]
        raise BuildRecipeError(f"{arguments[0]} failed: {detail}")
    return completed


def _installed_inventory(path: Path) -> tuple[tuple[str, str], ...]:
    values = {
        (_package_name(distribution.metadata["Name"]), distribution.version)
        for distribution in importlib.metadata.distributions(path=[str(path)])
        if distribution.metadata.get("Name")
    }
    return tuple(sorted(values))


def _establish_declared_source_modes(source: Path) -> None:
    """Bring the source tree this producer builds from to the declared mode set.

    REQ-RLO-017. The exported candidate reaches this process through a bind mount,
    which presents the calling host filesystem's mode semantics. A Windows host has
    no POSIX mode to present, so every entry arrives as `0777`, and both
    `python -m build` and `scripts/normalize_sdist.py` record member modes verbatim:
    the 0.7.0 build of record was accepted with 69 wheel entries marked executable
    that way and had to be rejected after an independent hosted replay disagreed.
    The modes are set here, inside the producer, because a `chmod` on a Windows
    filesystem is not retained; a POSIX export already produces exactly this set,
    so the call changes nothing there.
    """

    try:
        os.chmod(source, DECLARED_SOURCE_DIRECTORY_MODE)
        for current, directories, files in os.walk(source):
            for name in directories:
                os.chmod(Path(current) / name, DECLARED_SOURCE_DIRECTORY_MODE)
            for name in files:
                os.chmod(Path(current) / name, DECLARED_SOURCE_FILE_MODE)
    except OSError as exc:
        raise BuildRecipeError("producer cannot establish the declared source mode set") from exc


def _producer(recipe_path: Path, lock_path: Path, source: Path, output: Path, version: str, epoch: int, evidence: Path) -> None:
    recipe = validate_recipe_bytes(recipe_path.read_bytes(), path=DEFAULT_RECIPE_PATH, lock=lock_path.read_bytes())
    observed_arch = {"x86_64": "amd64", "amd64": "amd64"}.get(platform.machine().lower(), platform.machine().lower())
    observed = {
        "os": platform.system().lower(),
        "architecture": observed_arch,
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "pointer_bits": struct.calcsize("P") * 8,
    }
    expected_runtime = recipe.value["python"]
    if observed != {
        "os": recipe.value["producer"]["os"], "architecture": recipe.value["producer"]["architecture"],
        "python_implementation": expected_runtime["implementation"], "python_version": expected_runtime["version"],
        "pointer_bits": expected_runtime["pointer_bits"],
    }:
        raise BuildRecipeError(f"producer runtime identity differs: {observed}")
    if epoch < 1 or not VERSION_PATTERN.fullmatch(version):
        raise BuildRecipeError("producer version or epoch is invalid")
    for item in (source, recipe_path, lock_path):
        if not item.exists():
            raise BuildRecipeError("producer input is missing")
    _establish_declared_source_modes(source)
    if output.exists():
        raise BuildRecipeError("producer output directory must be fresh")
    output.mkdir()
    toolchain = output.parent / "toolchain"
    raw_output = output.parent / "raw"
    toolchain.mkdir()
    raw_output.mkdir()
    fixed = dict(recipe.value["environment"]["fixed"])
    home = Path(fixed["HOME"])
    if home.exists():
        raise BuildRecipeError("producer HOME must be fresh")
    home.mkdir(parents=True)
    fixed["SOURCE_DATE_EPOCH"] = str(epoch)
    install_command = [
        sys.executable if argument == "python" else str(toolchain) if argument == "{toolchain_dir}" else str(lock_path) if argument == "{toolchain_lock}" else argument
        for argument in recipe.value["commands"][0]["argv"]
    ]
    _bounded_run(install_command, timeout=600, environment=fixed, cwd=source)
    installed = _installed_inventory(toolchain)
    if installed != recipe.inventory:
        raise BuildRecipeError(f"installed toolchain inventory differs: {installed}")
    build_env = dict(fixed)
    build_env["PYTHONPATH"] = str(toolchain)
    build_command = [
        sys.executable if argument == "python" else str(raw_output) if argument == "{raw_output}" else argument
        for argument in recipe.value["commands"][1]["argv"]
    ]
    built = _bounded_run(build_command, cwd=source, environment=build_env, timeout=600)
    wheel_name = recipe.value["outputs"]["wheel"].format(version=version)
    sdist_name = recipe.value["outputs"]["sdist"].format(version=version)
    wheel = raw_output / wheel_name
    raw_sdist = raw_output / sdist_name
    if sorted(item.name for item in raw_output.iterdir() if item.is_file()) != sorted((wheel_name, sdist_name)):
        raise BuildRecipeError("build produced an unexpected file set")
    shutil.copyfile(wheel, output / wheel_name)
    normalize_command = [
        sys.executable if argument == "python" else str(raw_sdist) if argument == "{raw_sdist}" else str(output / sdist_name) if argument == "{final_sdist}" else str(epoch) if argument == "{source_date_epoch}" else argument
        for argument in recipe.value["commands"][2]["argv"]
    ]
    _bounded_run(normalize_command, cwd=source, environment=build_env, timeout=300)
    hashes = {name: _sha256_bytes((output / name).read_bytes()) for name in (wheel_name, sdist_name)}
    evidence.write_bytes(canonical_json_bytes({
        "schema": "se-harness-release-build-producer/v1",
        "recipe_sha256": recipe.sha256,
        "producer_image": recipe.image,
        "observed": observed,
        "toolchain": [{"name": name, "version": item_version} for name, item_version in installed],
        "environment": {key: build_env[key] for key in sorted(fixed)},
        "commands": [command["argv"] for command in recipe.value["commands"]],
        "outputs": hashes,
    }))


def _docker_image_identity(image: str) -> str:
    _bounded_run(["docker", "pull", "--platform", "linux/amd64", image], timeout=600)
    inspected = _bounded_run(["docker", "image", "inspect", "--format", "{{json .RepoDigests}}", image], timeout=60)
    try:
        digests = json.loads(inspected.stdout)
    except json.JSONDecodeError as exc:
        raise BuildRecipeError("Docker returned invalid image identity") from exc
    if not isinstance(digests, list) or image not in digests:
        raise BuildRecipeError("Docker image identity does not include the bound digest")
    return image


def _docker_build(control: Path, workspace: Path, recipe: BuildRecipe, version: str, epoch: int) -> dict[str, Any]:
    command = [
        "docker", "run", "--rm", "--pull", "never", "--platform", "linux/amd64",
        "--mount", f"type=bind,source={workspace},target=/workspace",
        "--mount", f"type=bind,source={control},target=/control,readonly",
        recipe.image, "python", "/control/repository_tools/release_build.py", "producer",
        "--recipe", "/workspace/source/release/build-recipe.json",
        "--lock", "/workspace/source/release/build-toolchain.lock",
        "--source", "/workspace/source", "--output", "/workspace/final",
        "--version", version, "--epoch", str(epoch), "--evidence", "/workspace/producer.json",
    ]
    _bounded_run(command)
    try:
        return json.loads((workspace / "producer.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildRecipeError("producer did not emit valid bounded evidence") from exc


def _is_posix() -> bool:
    return os.name == "posix"


def _hand_back_workspace(work_root: Path, image: str) -> None:
    """Return the producer's root-owned trees to the calling user.

    WO-RLO-007. The producer runs as root inside the bind-mounted workspace; on a
    hosted Linux runner the outputs are then unreadable by the runner user
    (`Permission denied` on `final/<sdist>`) and the `tempfile.TemporaryDirectory`
    teardown fails with `Operation not permitted`. One further run of the same
    pinned image changes the ownership back; it runs right after each producer
    build, before the outputs are read, and once more over the whole work root on
    the failure path. Nothing about the recipe, the lock, the producer's arguments
    or the compared outputs is involved; on a non-POSIX host there is nothing to do.
    """

    if not _is_posix():
        return
    owner = f"{os.getuid()}:{os.getgid()}"
    _bounded_run(
        [
            "docker", "run", "--rm", "--pull", "never", "--platform", "linux/amd64",
            "--mount", f"type=bind,source={work_root},target=/workspace",
            image, "chown", "-R", owner, "/workspace",
        ],
        timeout=300,
    )


def replay_build(
    repository: Path,
    commit: str,
    version: str,
    output_directory: Path,
    *,
    recipe_path: str = DEFAULT_RECIPE_PATH,
    recipe_sha256: str | None = None,
    expected_wheel_sha256: str | None = None,
    expected_sdist_sha256: str | None = None,
) -> dict[str, Any]:
    root = repository.resolve(strict=True)
    recipe = load_build_recipe_at(root, commit, path=recipe_path, expected_sha256=recipe_sha256)
    epoch_text = str(_run_git(root, "show", "-s", "--format=%ct", commit))
    if not epoch_text.isdigit() or int(epoch_text) < 1:
        raise BuildRecipeError("candidate commit timestamp is invalid")
    epoch = int(epoch_text)
    destination = output_directory.resolve()
    if destination.exists():
        raise BuildRecipeError("replay output directory must not already exist")
    try:
        destination.relative_to(root)
    except ValueError:
        pass
    else:
        raise BuildRecipeError("replay output directory must be outside the repository")
    image = _docker_image_identity(recipe.image)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # ignore_cleanup_errors: the hand-back below is what makes teardown possible on a
    # hosted runner; if it fails, the failure is reported on its own and never masked
    # by, or masking, the build result (WO-RLO-007).
    with tempfile.TemporaryDirectory(
        prefix=".se-harness-release-build-", dir=destination.parent, ignore_cleanup_errors=True
    ) as temporary:
        work_root = Path(temporary)
        try:
            result = _replay_in_workspace(
                root, commit, version, recipe, epoch, image, work_root, destination,
                expected_wheel_sha256=expected_wheel_sha256, expected_sdist_sha256=expected_sdist_sha256,
            )
        except BaseException:
            try:
                _hand_back_workspace(work_root, image)
            except BuildRecipeError:
                pass  # the build failure is the result; a hand-back failure only leaves the temporary tree behind
            raise
    return result


def _replay_in_workspace(
    root: Path,
    commit: str,
    version: str,
    recipe: BuildRecipe,
    epoch: int,
    image: str,
    work_root: Path,
    destination: Path,
    *,
    expected_wheel_sha256: str | None,
    expected_sdist_sha256: str | None,
) -> dict[str, Any]:
    from repository_tools.release_distribution import (
        checksum_manifest_bytes,
        create_manifest,
        expected_distribution_names,
        source_manifest_sha256,
    )

    observations: list[dict[str, Any]] = []
    final_paths: list[Path] = []
    for suffix in ("a", "b"):
        workspace = work_root / suffix
        workspace.mkdir()
        _safe_extract_candidate(root, commit, workspace / "source")
        observations.append(_docker_build(root, workspace, recipe, version, epoch))
        _hand_back_workspace(workspace, image)  # before the outputs are read (WO-RLO-007)
        final_paths.append(workspace / "final")
    wheel_name, sdist_name = expected_distribution_names(version)
    hashes: list[dict[str, str]] = []
    for final in final_paths:
        if sorted(item.name for item in final.iterdir()) != sorted((wheel_name, sdist_name)):
            raise BuildRecipeError("producer final output file set differs")
        hashes.append({
            "wheel_sha256": _sha256_bytes((final / wheel_name).read_bytes()),
            "sdist_sha256": _sha256_bytes((final / sdist_name).read_bytes()),
        })
    if hashes[0] != hashes[1] or (final_paths[0] / wheel_name).read_bytes() != (final_paths[1] / wheel_name).read_bytes() or (final_paths[0] / sdist_name).read_bytes() != (final_paths[1] / sdist_name).read_bytes():
        raise BuildRecipeError(f"independent builds differ: {hashes}")
    if expected_wheel_sha256 is not None and hashes[0]["wheel_sha256"] != expected_wheel_sha256:
        raise BuildRecipeError(f"rebuilt wheel differs from accepted hash: {hashes[0]['wheel_sha256']}")
    if expected_sdist_sha256 is not None and hashes[0]["sdist_sha256"] != expected_sdist_sha256:
        raise BuildRecipeError(f"rebuilt sdist differs from accepted hash: {hashes[0]['sdist_sha256']}")
    staged_bundle = work_root / "bundle"
    staged_bundle.mkdir()
    shutil.copyfile(final_paths[0] / wheel_name, staged_bundle / wheel_name)
    shutil.copyfile(final_paths[0] / sdist_name, staged_bundle / sdist_name)
    checksums = checksum_manifest_bytes(version, hashes[0]["wheel_sha256"], hashes[0]["sdist_sha256"])
    (staged_bundle / "SHA256SUMS").write_bytes(checksums)
    manifest = create_manifest(
        root,
        commit,
        version,
        staged_bundle / wheel_name,
        staged_bundle / sdist_name,
        build_recipe=PurePosixPath(recipe.path),
    )
    os.replace(staged_bundle, destination)
    return {
        "schema": REPLAY_SCHEMA,
        "authority": "technical replay evidence only; no lifecycle or external-action authority",
        "state": "exact",
        "candidate": {"commit": commit, "source_manifest_sha256": source_manifest_sha256(root, commit), "source_date_epoch": epoch},
        "recipe": {"schema": RECIPE_SCHEMA, "path": recipe.path, "sha256": recipe.sha256},
        "producer": {"image": image, "os": "linux", "architecture": "amd64"},
        "builds": [{"id": name, **hash_value} for name, hash_value in zip(("a", "b"), hashes)],
        "expected": {"wheel_sha256": expected_wheel_sha256, "sdist_sha256": expected_sdist_sha256},
        "manifest": manifest,
        "observations": observations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay the canonical repository release-build recipe.")
    commands = parser.add_subparsers(dest="command", required=True)
    producer = commands.add_parser("producer", help=argparse.SUPPRESS)
    for name in ("recipe", "lock", "source", "output", "evidence"):
        producer.add_argument(f"--{name}", type=Path, required=True)
    producer.add_argument("--version", required=True)
    producer.add_argument("--epoch", type=int, required=True)
    replay = commands.add_parser("replay", help="build an exact candidate twice in the bound producer")
    replay.add_argument("--repository", type=Path, default=Path.cwd())
    replay.add_argument("--commit", required=True)
    replay.add_argument("--version", required=True)
    replay.add_argument("--output-directory", type=Path, required=True)
    replay.add_argument("--result", type=Path, required=True)
    replay.add_argument("--recipe", default=DEFAULT_RECIPE_PATH)
    replay.add_argument("--recipe-sha256")
    replay.add_argument("--expected-wheel-sha256")
    replay.add_argument("--expected-sdist-sha256")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "producer":
            _producer(arguments.recipe, arguments.lock, arguments.source, arguments.output, arguments.version, arguments.epoch, arguments.evidence)
        else:
            result = replay_build(
                arguments.repository, arguments.commit, arguments.version, arguments.output_directory,
                recipe_path=arguments.recipe, recipe_sha256=arguments.recipe_sha256,
                expected_wheel_sha256=arguments.expected_wheel_sha256,
                expected_sdist_sha256=arguments.expected_sdist_sha256,
            )
            arguments.result.write_bytes(canonical_json_bytes(result))
    except (BuildRecipeError, OSError, ValueError) as exc:
        print(f"release-build: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
