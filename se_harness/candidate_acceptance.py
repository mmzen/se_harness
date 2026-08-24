"""Released-verifier black-box acceptance for an exact candidate wheel."""

from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from se_harness import __version__
from se_harness.hash_bound import LOCK_RELATIVE
from se_harness.installer import HarnessError
from se_harness.runtime_identity import COMMIT_PATTERN, SHA256_PATTERN


ACCEPTANCE_SCHEMA = "se-harness-functional-acceptance-v1"
SCENARIO_IDS = (
    "installed-identity",
    "init",
    "adopt",
    "doctor",
    "validate",
    "dashboard",
    "safe-upgrade",
    "customized-content-refusal",
    "corrupted-integrity-refusal",
    "authority-denial",
)
CONTRACT_SHA256 = hashlib.sha256(
    json.dumps({"schema": ACCEPTANCE_SCHEMA, "scenarios": SCENARIO_IDS}, sort_keys=True).encode("utf-8")
).hexdigest()
MAX_CANDIDATE_WHEEL_BYTES = 100 * 1024 * 1024
MAX_SNAPSHOT_FILES = 20_000
MAX_SNAPSHOT_BYTES = 250 * 1024 * 1024
VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    outcome: str
    output_sha256: str


@dataclass(frozen=True)
class AcceptanceManifest:
    schema: str
    verifier_version: str
    verifier_wheel_sha256: str
    contract_sha256: str
    candidate_version: str
    candidate_commit: str
    candidate_wheel_sha256: str
    python_version: str
    scenarios: tuple[ScenarioResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "verifier": {
                "version": self.verifier_version,
                "wheel_sha256": self.verifier_wheel_sha256,
                "contract_sha256": self.contract_sha256,
            },
            "candidate": {
                "version": self.candidate_version,
                "commit": self.candidate_commit,
                "wheel_sha256": self.candidate_wheel_sha256,
            },
            "python": {"version": self.python_version},
            "scenarios": [asdict(item) for item in self.scenarios],
        }

    def canonical_bytes(self) -> bytes:
        return (json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n").encode("utf-8")


def _hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _wheel_version(path: Path, raw: bytes) -> str:
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
            if len(names) != 1:
                raise HarnessError("candidate wheel has ambiguous distribution metadata")
            metadata = archive.read(names[0]).decode("utf-8")
    except (OSError, UnicodeError, zipfile.BadZipFile) as exc:
        raise HarnessError(f"cannot inspect candidate wheel: {exc}") from exc
    names = [line.partition(":")[2].strip() for line in metadata.splitlines() if line.startswith("Name:")]
    versions = [line.partition(":")[2].strip() for line in metadata.splitlines() if line.startswith("Version:")]
    if len(names) != 1 or names[0].lower().replace("_", "-") != "se-harness" or len(versions) != 1:
        raise HarnessError("candidate wheel metadata does not identify one se-harness distribution")
    if VERSION_PATTERN.fullmatch(versions[0]) is None:
        raise HarnessError("candidate wheel version is invalid")
    expected = f"se_harness-{versions[0]}-py3-none-any.whl"
    if path.name != expected:
        raise HarnessError(f"candidate wheel filename must be {expected}")
    return versions[0]


def _environment() -> dict[str, str]:
    selected = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "HOME", "LANG", "LC_ALL"}
    }
    selected.update(
        {
            "PYTHONNOUSERSITE": "1",
            "PYTHONPATH": "",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_INPUT": "1",
        }
    )
    return selected


def _launcher(environment: Path, name: str) -> Path:
    candidates = (
        environment / "Scripts" / (name + ".exe"),
        environment / "Scripts" / name,
        environment / "bin" / name,
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise HarnessError(f"candidate environment has no {name} launcher")


def _normalize(value: str, temporary: Path, wheel: Path, checkout: Path | None) -> str:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    replacements = [(temporary, "<TEMP>"), (wheel, "<WHEEL>")]
    if checkout is not None:
        replacements.append((checkout, "<CHECKOUT>"))
    for path, label in replacements:
        representations: set[str] = set()
        for representation in {str(path), str(path.resolve())}:
            representations.add(representation)
            representations.add(representation.replace("\\", "/"))
            representations.add(json.dumps(representation)[1:-1])
        for representation in sorted(representations, key=len, reverse=True):
            normalized = normalized.replace(representation, label)
    return normalized.replace("\\", "/")


def _result(
    scenario_id: str,
    *,
    returncode: int,
    stdout: str,
    stderr: str,
    temporary: Path,
    wheel: Path,
    checkout: Path | None,
    expected_returncode: int = 0,
) -> ScenarioResult:
    canonical = json.dumps(
        {
            "returncode": returncode,
            "stdout": _normalize(stdout, temporary, wheel, checkout),
            "stderr": _normalize(stderr, temporary, wheel, checkout),
        },
        sort_keys=True,
    ).encode("utf-8")
    return ScenarioResult(
        scenario_id=scenario_id,
        outcome="passed" if returncode == expected_returncode else "failed",
        output_sha256=_hash(canonical),
    )


def _run(
    scenario_id: str,
    command: list[str],
    *,
    cwd: Path,
    temporary: Path,
    wheel: Path,
    checkout: Path | None,
    expected_returncode: int = 0,
) -> ScenarioResult:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=_environment(),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return _result(
        scenario_id,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        temporary=temporary,
        wheel=wheel,
        checkout=checkout,
        expected_returncode=expected_returncode,
    )


def _snapshot(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    excluded = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "target",
        "build",
        "dist",
        "__pycache__",
        ".pytest_cache",
    }
    result: dict[str, str] = {}
    total = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root)
        if any(part in excluded or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            raise HarnessError(f"candidate checkout snapshot contains a symbolic link: {relative.as_posix()}")
        if not path.is_file():
            continue
        if len(result) >= MAX_SNAPSHOT_FILES:
            raise HarnessError("candidate checkout snapshot exceeds the bounded file count")
        size = path.stat().st_size
        total += size
        if total > MAX_SNAPSHOT_BYTES:
            raise HarnessError("candidate checkout snapshot exceeds the bounded byte count")
        result[relative.as_posix()] = _hash(path.read_bytes())
    return result


def assess_candidate_wheel(
    wheel: Path,
    *,
    candidate_commit: str,
    candidate_wheel_sha256: str,
    verifier_wheel_sha256: str,
    checkout_root: Path | None = None,
) -> AcceptanceManifest:
    wheel = wheel.expanduser().resolve()
    if not wheel.is_file():
        raise HarnessError("candidate wheel does not exist")
    if COMMIT_PATTERN.fullmatch(candidate_commit) is None:
        raise HarnessError("candidate commit must be a full Git object ID")
    if SHA256_PATTERN.fullmatch(candidate_wheel_sha256) is None:
        raise HarnessError("candidate wheel SHA-256 must be lowercase and complete")
    if SHA256_PATTERN.fullmatch(verifier_wheel_sha256) is None:
        raise HarnessError("verifier wheel SHA-256 must be lowercase and complete")
    checkout = checkout_root.expanduser().resolve() if checkout_root is not None else None
    if checkout is not None and _within(Path(__file__), checkout):
        raise HarnessError("candidate checkout cannot supply the released acceptance runner")
    if wheel.stat().st_size > MAX_CANDIDATE_WHEEL_BYTES:
        raise HarnessError("candidate wheel exceeds the bounded archive size")
    wheel_bytes = wheel.read_bytes()
    candidate_digest = _hash(wheel_bytes)
    if candidate_digest != candidate_wheel_sha256:
        raise HarnessError("candidate wheel SHA-256 mismatch")
    candidate_version = _wheel_version(wheel, wheel_bytes)
    checkout_before = _snapshot(checkout) if checkout is not None else None
    with tempfile.TemporaryDirectory(prefix="se-harness-acceptance-") as temporary_name:
        temporary = Path(temporary_name).resolve()
        environment = temporary / "candidate-env"
        staged_wheel = temporary / "candidate-wheel" / wheel.name
        staged_wheel.parent.mkdir()
        staged_wheel.write_bytes(wheel_bytes)
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = _launcher(environment, "python")
        try:
            subprocess.run(
                [str(python), "-I", "-m", "pip", "install", "--no-deps", str(staged_wheel)],
                cwd=temporary,
                env=_environment(),
                capture_output=True,
                text=True,
                timeout=120,
                check=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise HarnessError(f"candidate wheel installation failed: {type(exc).__name__}") from exc
        harnessctl = _launcher(environment, "harnessctl")
        results: list[ScenarioResult] = []
        results.append(
            _run(
                "installed-identity",
                [
                    str(python),
                    "-I",
                    "-m",
                    "se_harness",
                    "identity",
                    "--role",
                    "candidate-package",
                    "--expected-version",
                    candidate_version,
                    "--expected-root",
                    str(environment),
                    "--candidate-commit",
                    candidate_commit,
                    "--entry-point",
                    str(harnessctl),
                    "--require-isolated-python",
                    "--require-entry-point",
                ]
                + (["--checkout-root", str(checkout)] if checkout is not None else []),
                cwd=temporary,
                temporary=temporary,
                wheel=wheel,
                checkout=checkout,
            )
        )
        initialized = temporary / "initialized"
        results.append(
            _run(
                "init",
                [str(harnessctl), "init", str(initialized), "--project-name", "Acceptance"],
                cwd=temporary,
                temporary=temporary,
                wheel=wheel,
                checkout=checkout,
            )
        )
        adopted = temporary / "adopted"
        adopted.mkdir()
        (adopted / "README.md").write_text("repository\n", encoding="utf-8")
        results.append(
            _run("adopt", [str(harnessctl), "adopt", str(adopted)], cwd=temporary, temporary=temporary, wheel=wheel, checkout=checkout)
        )
        for scenario, command in (
            ("doctor", [str(harnessctl), "doctor", str(initialized)]),
            ("validate", [str(harnessctl), "validate", str(initialized)]),
            ("dashboard", [str(harnessctl), "dashboard", str(initialized)]),
            ("safe-upgrade", [str(harnessctl), "upgrade", str(initialized), "--apply"]),
        ):
            results.append(
                _run(scenario, command, cwd=temporary, temporary=temporary, wheel=wheel, checkout=checkout)
            )
        customized = temporary / "customized"
        shutil.copytree(initialized, customized)
        customized_file = customized / "ENGINEERING_HARNESS.md"
        customized_file.write_bytes(customized_file.read_bytes() + b"\nRepository customization.\n")
        customized_before = _snapshot(customized)
        refusal = _run(
            "customized-content-refusal",
            [str(harnessctl), "upgrade", str(customized), "--apply"],
            cwd=temporary,
            temporary=temporary,
            wheel=wheel,
            checkout=checkout,
            expected_returncode=1,
        )
        if _snapshot(customized) != customized_before:
            refusal = ScenarioResult(refusal.scenario_id, "failed", refusal.output_sha256)
        results.append(refusal)
        corrupted = temporary / "corrupted"
        shutil.copytree(initialized, corrupted)
        lock_path = corrupted / LOCK_RELATIVE
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] = "0" * 64
        # Explicit LF: the lock is hash-bound text, so the writing platform must
        # not decide its bytes.
        lock_path.write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
        results.append(
            _run(
                "corrupted-integrity-refusal",
                [str(harnessctl), "doctor", str(corrupted)],
                cwd=temporary,
                temporary=temporary,
                wheel=wheel,
                checkout=checkout,
                expected_returncode=1,
            )
        )
        consumer_before = _snapshot(initialized)
        authority = _run(
            "authority-denial",
            [str(harnessctl), "approve", str(initialized)],
            cwd=temporary,
            temporary=temporary,
            wheel=wheel,
            checkout=checkout,
            expected_returncode=2,
        )
        if _snapshot(initialized) != consumer_before:
            authority = ScenarioResult(authority.scenario_id, "failed", authority.output_sha256)
        results.append(authority)
    if checkout is not None and _snapshot(checkout) != checkout_before:
        raise HarnessError("candidate acceptance modified the checkout")
    if tuple(item.scenario_id for item in results) != SCENARIO_IDS:
        raise HarnessError("candidate acceptance scenario set is incomplete")
    failed = [item.scenario_id for item in results if item.outcome != "passed"]
    if failed:
        raise HarnessError(f"candidate acceptance failed: {', '.join(failed)}")
    return AcceptanceManifest(
        schema=ACCEPTANCE_SCHEMA,
        verifier_version=__version__,
        verifier_wheel_sha256=verifier_wheel_sha256,
        contract_sha256=CONTRACT_SHA256,
        candidate_version=candidate_version,
        candidate_commit=candidate_commit,
        candidate_wheel_sha256=candidate_digest,
        python_version=platform.python_version(),
        scenarios=tuple(results),
    )


def write_acceptance_manifest(path: Path, manifest: AcceptanceManifest) -> None:
    destination = path.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(manifest.canonical_bytes())
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
