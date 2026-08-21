"""Bounded runtime-identity evidence for released evaluators and candidates."""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import re
import shutil
import site
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from se_harness import __version__
from se_harness.evaluator_identity import (
    EvaluatorIdentityError,
    installed_evaluator_identity,
)
from se_harness.installer import HarnessError, template_root


IDENTITY_SCHEMA = "se-harness-runtime-identity-v3"
ROLES = {"released-evaluator", "candidate-source", "candidate-package"}
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, order=True)
class IdentityDiagnostic:
    code: str
    subject: str
    message: str


@dataclass(frozen=True)
class RuntimeIdentity:
    schema: str
    passed: bool
    role: str
    python_executable: str
    python_version: str
    harness_version: str
    module_origin: str
    distribution_origin: str
    template_origin: str
    entry_point_origin: str | None
    expected_root: str
    checkout_root: str | None
    candidate_commit: str | None
    evaluator_payload_manifest: str | None
    evaluator_payload_sha256: str | None
    evaluator_archive_name: str | None
    evaluator_archive_sha256: str | None
    evaluator_wheel_sha256: str | None
    isolated_python: bool
    user_site_enabled: bool
    pythonpath_present: bool
    diagnostics: tuple[IdentityDiagnostic, ...]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["diagnostics"] = [asdict(item) for item in self.diagnostics]
        return value


def _resolved(path: Path) -> Path:
    try:
        return path.expanduser().resolve(strict=True)
    except OSError:
        return path.expanduser().resolve(strict=False)


def _absolute(path: Path) -> Path:
    """Return a normalized absolute path without resolving its final symlink."""

    return Path(os.path.abspath(path.expanduser()))


def _within(path: Path, boundary: Path) -> bool:
    try:
        _resolved(path).relative_to(_resolved(boundary))
    except ValueError:
        return False
    return True


def _lexically_within(path: Path, boundary: Path) -> bool:
    """Check launcher placement without following a normal virtualenv symlink."""

    try:
        _absolute(path).relative_to(_absolute(boundary))
    except ValueError:
        return False
    return True


def _distribution_root() -> Path:
    try:
        return _resolved(Path(importlib.metadata.distribution("se-harness").locate_file("")))
    except importlib.metadata.PackageNotFoundError:
        return _resolved(Path(__file__).parent.parent)


def _effective_search_paths() -> tuple[Path, ...]:
    paths: set[Path] = set()
    for value in sys.path:
        if not isinstance(value, str):
            continue
        candidate = Path.cwd() if value == "" else Path(value)
        paths.add(_resolved(candidate))
    return tuple(sorted(paths, key=lambda item: os.path.normcase(str(item))))


def inspect_runtime_identity(
    *,
    role: str,
    expected_version: str,
    expected_root: Path,
    checkout_root: Path | None = None,
    candidate_commit: str | None = None,
    evaluator_payload_sha256: str | None = None,
    evaluator_wheel_sha256: str | None = None,
    entry_point: Path | None = None,
    require_isolated_python: bool = False,
    require_entry_point: bool = False,
) -> RuntimeIdentity:
    """Inspect and verify one declared runtime role without exposing environment data."""

    diagnostics: list[IdentityDiagnostic] = []
    expected = _resolved(expected_root)
    checkout = _resolved(checkout_root) if checkout_root is not None else None
    module = _resolved(Path(__file__))
    distribution = _distribution_root()
    templates = _resolved(template_root())
    executable = _absolute(Path(sys.executable))
    runtime_prefix = _resolved(Path(sys.prefix))
    discovered_entry_point = shutil.which("harnessctl") or shutil.which("harnessctl.exe")
    resolved_entry_point = (
        _resolved(entry_point)
        if entry_point is not None
        else (_resolved(Path(discovered_entry_point)) if discovered_entry_point else None)
    )
    isolated = bool(getattr(sys.flags, "isolated", 0))
    user_site_enabled = bool(site.ENABLE_USER_SITE)
    pythonpath_present = bool(os.environ.get("PYTHONPATH"))
    installed_payload_manifest: str | None = None
    installed_payload_sha256: str | None = None
    installed_archive_name: str | None = None
    installed_archive_sha256: str | None = None

    if role not in ROLES:
        diagnostics.append(IdentityDiagnostic("RID001", "role", "unsupported runtime role"))
    if __version__ != expected_version:
        diagnostics.append(
            IdentityDiagnostic(
                "RID002",
                "harness_version",
                f"resolved {__version__!r}; expected {expected_version!r}",
            )
        )
    if pythonpath_present:
        diagnostics.append(
            IdentityDiagnostic("RID008", "PYTHONPATH", "runtime inherited PYTHONPATH")
        )
    if user_site_enabled:
        diagnostics.append(
            IdentityDiagnostic("RID009", "user_site", "runtime enables user site-packages")
        )
    for label, path in (("module_origin", module), ("template_origin", templates)):
        if not _within(path, expected):
            diagnostics.append(
                IdentityDiagnostic("RID003", label, "origin is outside the expected runtime root")
            )

    if role in {"released-evaluator", "candidate-package"}:
        if runtime_prefix != expected:
            diagnostics.append(
                IdentityDiagnostic("RID004", "runtime_prefix", "runtime prefix differs from the expected environment")
            )
        if not _lexically_within(executable, expected):
            diagnostics.append(
                IdentityDiagnostic("RID004", "python_executable", "virtualenv launcher is outside its environment")
            )
        if not _within(distribution, expected):
            diagnostics.append(
                IdentityDiagnostic("RID004", "distribution_origin", "installed-runtime path is outside its environment")
            )
        if checkout is None:
            diagnostics.append(IdentityDiagnostic("RID005", "checkout_root", "checkout boundary is required"))
        else:
            for label, path in (
                ("module_origin", module),
                ("distribution_origin", distribution),
                ("template_origin", templates),
            ):
                if _within(path, checkout):
                    diagnostics.append(
                        IdentityDiagnostic("RID006", label, "installed runtime resolves inside the checkout")
                    )
            if _lexically_within(executable, checkout):
                diagnostics.append(
                    IdentityDiagnostic("RID006", "python_executable", "installed runtime launcher is inside the checkout")
                )
            contaminated = [path for path in _effective_search_paths() if _within(path, checkout)]
            if contaminated:
                diagnostics.append(
                    IdentityDiagnostic("RID007", "sys.path", "effective import search contains the checkout")
                )
        if resolved_entry_point is not None and not _within(resolved_entry_point, expected):
            diagnostics.append(
                IdentityDiagnostic("RID010", "entry_point_origin", "harnessctl resolves outside the environment")
            )
        if require_entry_point and resolved_entry_point is None:
            diagnostics.append(
                IdentityDiagnostic("RID011", "entry_point_origin", "harnessctl entry point is unavailable")
            )

    if role == "candidate-source":
        if checkout is None:
            diagnostics.append(IdentityDiagnostic("RID005", "checkout_root", "checkout boundary is required"))
        elif expected != checkout:
            diagnostics.append(
                IdentityDiagnostic("RID012", "expected_root", "candidate source root must equal the checkout root")
            )
        if not _within(distribution, expected):
            diagnostics.append(
                IdentityDiagnostic("RID018", "distribution_origin", "source distribution metadata resolves outside the checkout")
            )

    if role == "released-evaluator":
        try:
            evaluator = installed_evaluator_identity()
        except EvaluatorIdentityError as exc:
            diagnostics.append(
                IdentityDiagnostic("RID019", "evaluator_payload", f"installed payload identity failed: {exc}")
            )
        else:
            installed_payload_manifest = evaluator.payload_manifest
            installed_payload_sha256 = evaluator.payload_sha256
            installed_archive_name = evaluator.archive_name
            installed_archive_sha256 = evaluator.archive_sha256
        if evaluator_payload_sha256 is not None:
            if SHA256_PATTERN.fullmatch(evaluator_payload_sha256) is None:
                diagnostics.append(
                    IdentityDiagnostic(
                        "RID020",
                        "evaluator_payload_sha256",
                        "the expected payload digest must be a lowercase SHA-256",
                    )
                )
            elif installed_payload_sha256 != evaluator_payload_sha256:
                diagnostics.append(
                    IdentityDiagnostic(
                        "RID021",
                        "evaluator_payload_sha256",
                        "installed payload digest differs from the expected evaluator payload",
                    )
                )
        if evaluator_wheel_sha256 is not None and SHA256_PATTERN.fullmatch(evaluator_wheel_sha256) is None:
            diagnostics.append(
                IdentityDiagnostic("RID013", "evaluator_wheel_sha256", "the optional digest must be a lowercase SHA-256")
            )
        elif evaluator_wheel_sha256 is not None and installed_archive_sha256 != evaluator_wheel_sha256:
            diagnostics.append(
                IdentityDiagnostic(
                    "RID022",
                    "evaluator_wheel_sha256",
                    "installed PEP 610 archive digest differs from the expected evaluator wheel",
                )
            )
        if candidate_commit is not None:
            diagnostics.append(
                IdentityDiagnostic("RID014", "candidate_commit", "released evaluator identity cannot claim a candidate commit")
            )
    elif role in {"candidate-source", "candidate-package"}:
        if candidate_commit is None or COMMIT_PATTERN.fullmatch(candidate_commit) is None:
            diagnostics.append(
                IdentityDiagnostic("RID015", "candidate_commit", "a full lowercase candidate commit is required")
            )
        if evaluator_wheel_sha256 is not None:
            diagnostics.append(
                IdentityDiagnostic("RID016", "evaluator_wheel_sha256", "candidate identity cannot claim a released evaluator digest")
            )
        if evaluator_payload_sha256 is not None:
            diagnostics.append(
                IdentityDiagnostic("RID023", "evaluator_payload_sha256", "candidate identity cannot claim a released evaluator payload")
            )

    if require_isolated_python and not isolated:
        diagnostics.append(
            IdentityDiagnostic("RID017", "isolated_python", "Python isolated mode is required")
        )

    ordered = tuple(sorted(set(diagnostics)))
    return RuntimeIdentity(
        schema=IDENTITY_SCHEMA,
        passed=not ordered,
        role=role,
        python_executable=str(executable),
        python_version=platform.python_version(),
        harness_version=__version__,
        module_origin=str(module),
        distribution_origin=str(distribution),
        template_origin=str(templates),
        entry_point_origin=str(resolved_entry_point) if resolved_entry_point is not None else None,
        expected_root=str(expected),
        checkout_root=str(checkout) if checkout is not None else None,
        candidate_commit=candidate_commit,
        evaluator_payload_manifest=installed_payload_manifest,
        evaluator_payload_sha256=installed_payload_sha256,
        evaluator_archive_name=installed_archive_name,
        evaluator_archive_sha256=installed_archive_sha256,
        evaluator_wheel_sha256=evaluator_wheel_sha256,
        isolated_python=isolated,
        user_site_enabled=user_site_enabled,
        pythonpath_present=pythonpath_present,
        diagnostics=ordered,
    )


def render_runtime_identity(identity: RuntimeIdentity) -> str:
    return json.dumps(identity.to_dict(), indent=2, sort_keys=True)


def assert_runtime_identity(**kwargs: object) -> RuntimeIdentity:
    identity = inspect_runtime_identity(**kwargs)  # type: ignore[arg-type]
    if identity.diagnostics:
        details = "; ".join(f"{item.code} {item.subject}: {item.message}" for item in identity.diagnostics)
        raise HarnessError(f"runtime identity mismatch: {details}")
    return identity
