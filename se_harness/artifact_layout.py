"""Canonical artifact layout and conflict-safe domain authoring."""

from __future__ import annotations

import os
import re
import stat
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from se_harness import mutation_guard
from se_harness.installer import HarnessError, ensure_target, safe_destination


ARTIFACT_DIRECTORIES: dict[str, tuple[str, ...]] = {
    "intent": ("intent",),
    "capability": ("capabilities",),
    "requirement": ("requirements",),
    "specification": ("specifications",),
    "architecture": ("architecture",),
    "adr": ("architecture", "adr"),
    "verification": ("verification",),
    "work_order": ("work-orders",),
    "verification_record": ("verification-records",),
    "release_contract": ("release",),
    "release_record": ("releases",),
    "operating_contract": ("operations",),
}

ARTIFACT_PREFIXES = {
    "intent": "INT-",
    "capability": "CAP-",
    "requirement": "REQ-",
    "specification": "SPEC-",
    "architecture": "ARCH-",
    "adr": "ADR-",
    "verification": "VER-",
    "work_order": "WO-",
    "verification_record": "VREC-",
    "release_contract": "REL-",
    "release_record": "RLS-",
    "operating_contract": "OPS-",
}

ARTIFACT_TEMPLATES = {
    "intent": "INTENT.template.md",
    "capability": "CAPABILITY.template.md",
    "requirement": "REQUIREMENT.template.md",
    "specification": "SPECIFICATION.template.md",
    "architecture": "ARCHITECTURE.template.md",
    "adr": "ADR.template.md",
    "verification": "VERIFICATION.template.md",
    "work_order": "WORK_ORDER.template.md",
    "verification_record": "VERIFICATION_RECORD.template.md",
    "release_contract": "RELEASE_CONTRACT.template.md",
    "release_record": "RELEASE_RECORD.template.md",
    "operating_contract": "OPERATING_CONTRACT.template.md",
}

SUPPORTING_DIRECTORIES = ("evidence", "acceptance")
DOMAIN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]*-\d{3}$")
TITLE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._()/-]{0,127}$")

# These names either identify repository-wide containers, canonical type
# directories, or common implementation output and therefore cannot be safely
# interpreted as a product/domain slug in the first component below the
# engineering root.
RESERVED_DOMAINS = frozenset(
    {
        ".agents",
        ".codex",
        ".git",
        ".idea",
        "acceptance",
        "architecture",
        "capabilities",
        "evidence",
        "experiments",
        "intent",
        "node_modules",
        "operations",
        "release",
        "releases",
        "requirements",
        "specifications",
        "target",
        "templates",
        "verification",
        "verification-records",
        "work-orders",
    }
)


@dataclass(frozen=True)
class AuthoringChange:
    action: str
    path: str


def validate_domain(value: str) -> str:
    if not isinstance(value, str) or len(value) > 64 or DOMAIN_PATTERN.fullmatch(value) is None:
        raise HarnessError("domain must use 1-64 lowercase ASCII letters, numbers, and single hyphens")
    if value in RESERVED_DOMAINS:
        raise HarnessError(f"domain name is reserved: {value}")
    return value


def validate_artifact_type(value: str) -> str:
    if value not in ARTIFACT_DIRECTORIES:
        supported = ", ".join(sorted(ARTIFACT_DIRECTORIES))
        raise HarnessError(f"unsupported artifact type '{value}'; choose one of: {supported}")
    return value


def validate_artifact_id(value: str, artifact_type: str) -> str:
    selected_type = validate_artifact_type(artifact_type)
    prefix = ARTIFACT_PREFIXES[selected_type]
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None or not value.startswith(prefix):
        raise HarnessError(f"artifact ID must use the {prefix} prefix and a three-digit suffix")
    return value


def canonical_artifact_relative_path(domain: str, artifact_type: str, artifact_id: str) -> Path:
    selected_domain = validate_domain(domain)
    selected_type = validate_artifact_type(artifact_type)
    selected_id = validate_artifact_id(artifact_id, selected_type)
    return Path("docs") / "engineering" / selected_domain / Path(*ARTIFACT_DIRECTORIES[selected_type]) / f"{selected_id}.md"


def repository_record_relative_path(artifact_type: str, artifact_id: str, domain: str | None) -> Path:
    selected_type = validate_artifact_type(artifact_type)
    selected_id = validate_artifact_id(artifact_id, selected_type)
    if selected_type not in {"verification_record", "release_record"}:
        raise HarnessError("repository-wide record routing supports only verification and release records")
    if domain is not None:
        return canonical_artifact_relative_path(domain, selected_type, selected_id)
    return Path("docs") / "engineering" / Path(*ARTIFACT_DIRECTORIES[selected_type]) / f"{selected_id}.md"


def artifact_domain_from_relative_path(value: str | Path) -> str | None:
    raw = Path(value)
    if raw.is_absolute() or "\\" in str(value):
        return None
    parts = raw.parts
    if len(parts) < 4 or parts[:2] != ("docs", "engineering"):
        return None
    candidate = parts[2]
    try:
        return validate_domain(candidate)
    except HarnessError:
        return None


def common_artifact_domain(paths: list[str | Path]) -> str | None:
    if not paths:
        return None
    domains = [artifact_domain_from_relative_path(path) for path in paths]
    if any(domain is None for domain in domains):
        return None
    unique = set(domains)
    return next(iter(unique)) if len(unique) == 1 else None


def canonical_directory_paths() -> tuple[tuple[str, ...], ...]:
    paths = set(ARTIFACT_DIRECTORIES.values())
    paths.update((name,) for name in SUPPORTING_DIRECTORIES)
    return tuple(sorted(paths, key=lambda item: (len(item), item)))


def _is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _validate_existing_chain(root: Path, relative: Path, *, final_kind: str) -> Path:
    destination = safe_destination(root, relative)
    probe = root
    for index, part in enumerate(relative.parts):
        probe = probe / part
        if not probe.exists() and not _is_link_like(probe):
            continue
        if _is_link_like(probe):
            raise HarnessError(f"refusing to traverse a linked path: {probe}")
        is_final = index == len(relative.parts) - 1
        if not is_final and not probe.is_dir():
            raise HarnessError(f"path parent is not a directory: {probe}")
        if is_final and final_kind == "directory" and not probe.is_dir():
            raise HarnessError(f"domain path conflicts with a file: {probe}")
        if is_final and final_kind == "file" and probe.exists() and not probe.is_file():
            raise HarnessError(f"artifact path conflicts with a directory: {probe}")
    return destination


def _atomic_create(path: Path, content: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_name, path)
        except FileExistsError as exc:
            raise HarnessError(f"destination already exists: {path}") from exc
        except OSError as exc:
            raise HarnessError(f"cannot create destination atomically: {exc}") from exc
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def _rollback_directories(paths: list[Path]) -> None:
    for path in reversed(paths):
        try:
            path.rmdir()
        except OSError:
            # Remove only empty directories created by this invocation. A
            # concurrent writer's content is never deleted.
            pass


def _validate_installed_templates(root: Path) -> Path:
    relative = Path("docs") / "engineering" / "templates"
    templates = _validate_existing_chain(root, relative, final_kind="directory")
    if not templates.is_dir():
        raise HarnessError("the target does not contain installed engineering artifact templates")
    return templates


def scaffold_domain(
    repository: Path,
    *,
    domain: str,
    title: str | None,
    dry_run: bool,
) -> list[AuthoringChange]:
    root = ensure_target(repository, must_exist=True)
    _validate_installed_templates(root)
    selected_domain = validate_domain(domain)
    selected_title = title if title is not None else selected_domain.replace("-", " ").title()
    if TITLE_PATTERN.fullmatch(selected_title) is None:
        raise HarnessError("domain title must use 1-128 safe single-line letters, numbers, spaces, or ._()/-")

    domain_relative = Path("docs") / "engineering" / selected_domain
    _validate_existing_chain(root, domain_relative, final_kind="directory")
    directory_relatives = [domain_relative / Path(*parts) for parts in canonical_directory_paths()]
    for relative in [domain_relative, *directory_relatives]:
        _validate_existing_chain(root, relative, final_kind="directory")
    index_relative = domain_relative / "README.md"
    index = _validate_existing_chain(root, index_relative, final_kind="file")

    changes = [
        AuthoringChange("present" if (root / relative).is_dir() else "create", relative.as_posix())
        for relative in [domain_relative, *directory_relatives]
    ]
    changes.append(AuthoringChange("present" if index.is_file() else "create", index_relative.as_posix()))
    if dry_run:
        return changes

    mutation_guard.require_mutation_authority(root, operation="scaffold-domain")
    created_directories: list[Path] = []
    try:
        for relative in [domain_relative, *directory_relatives]:
            destination = root / relative
            if destination.is_dir():
                continue
            destination.mkdir()
            created_directories.append(destination)
        if not index.exists():
            content = (
                f"# {selected_title} Engineering Domain\n\n"
                "> Repository-owned index. Formal artifact authority comes from TOML metadata, "
                "typed relations, and lifecycle state—not this directory or index.\n\n"
                "Use the canonical type directories below and retain domain-specific navigation or "
                "instructions here.\n"
            ).encode("utf-8")
            _atomic_create(index, content)
    except (OSError, HarnessError) as exc:
        _rollback_directories(created_directories)
        if isinstance(exc, HarnessError):
            raise
        raise HarnessError(f"cannot scaffold domain safely: {exc}") from exc
    return changes


def _render_draft(template: str, artifact_type: str, artifact_id: str) -> bytes:
    normalized = template.replace("\r\n", "\n").replace("\r", "\n")
    expected_type = re.search(r'^type = "([^"]+)"$', normalized, flags=re.MULTILINE)
    if expected_type is None or expected_type.group(1) != artifact_type:
        raise HarnessError(f"canonical template type does not match requested type: {artifact_type}")
    rendered, id_count = re.subn(r'^id = "[^"]+"$', f'id = "{artifact_id}"', normalized, count=1, flags=re.MULTILINE)
    rendered, status_count = re.subn(r'^status = "[^"]+"$', 'status = "draft"', rendered, count=1, flags=re.MULTILINE)
    today = date.today().isoformat()
    rendered, created_count = re.subn(r'^created = "[^"]+"$', f'created = "{today}"', rendered, count=1, flags=re.MULTILINE)
    rendered, updated_count = re.subn(r'^updated = "[^"]+"$', f'updated = "{today}"', rendered, count=1, flags=re.MULTILINE)
    if id_count != 1 or status_count != 1 or created_count != 1 or updated_count != 1:
        raise HarnessError("canonical template is missing required id, status, created, or updated metadata")
    return rendered.encode("utf-8")


def authoring_checklist(repository: Path, artifact_type: str) -> list[str]:
    """Return the installed authoring policy's checklist bullets for one artifact type (AUT-POL-003)."""

    root = ensure_target(repository, must_exist=True)
    policy = _validate_existing_chain(root, Path("docs") / "engineering" / "ARTIFACT_AUTHORING.md", final_kind="file")
    if not policy.is_file():
        return []
    try:
        lines = policy.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    except (OSError, UnicodeError):
        return []
    bullets: list[str] = []
    in_type = False
    in_checklist = False
    for line in lines:
        if line.startswith("## "):
            in_type = line[3:].strip() == artifact_type
            in_checklist = False
            continue
        if line.startswith("### "):
            in_checklist = in_type and line[4:].strip() == "Checklist"
            continue
        if in_checklist and line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets


def _existing_artifact_path(root: Path, artifact_id: str) -> Path | None:
    artifact_root = root / "docs" / "engineering"
    if not artifact_root.is_dir():
        return None
    declaration = re.compile(rf'^id = "{re.escape(artifact_id)}"$', flags=re.MULTILINE)
    for path in sorted(artifact_root.rglob("*.md"), key=lambda item: item.as_posix()):
        try:
            relative_parts = path.relative_to(artifact_root).parts
        except ValueError:
            continue
        if any(part in {"templates", "evidence", ".git", ".idea", "target", "node_modules"} for part in relative_parts[:-1]):
            continue
        if _is_link_like(path) or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        if text.startswith("+++\n") and declaration.search(text.partition("\n+++\n")[0]):
            return path
    return None


def create_artifact(
    repository: Path,
    *,
    domain: str,
    artifact_type: str,
    artifact_id: str,
    dry_run: bool,
) -> AuthoringChange:
    root = ensure_target(repository, must_exist=True)
    _validate_installed_templates(root)
    selected_type = validate_artifact_type(artifact_type)
    selected_id = validate_artifact_id(artifact_id, selected_type)
    destination_relative = canonical_artifact_relative_path(domain, selected_type, selected_id)
    destination = _validate_existing_chain(root, destination_relative, final_kind="file")
    if destination.exists():
        raise HarnessError(f"artifact destination already exists: {destination_relative.as_posix()}")
    existing = _existing_artifact_path(root, selected_id)
    if existing is not None:
        raise HarnessError(f"artifact ID already exists: {selected_id} at {existing.relative_to(root).as_posix()}")

    template_relative = Path("docs") / "engineering" / "templates" / ARTIFACT_TEMPLATES[selected_type]
    template_path = _validate_existing_chain(root, template_relative, final_kind="file")
    if not template_path.is_file():
        raise HarnessError(f"canonical artifact template is missing: {template_relative.as_posix()}")
    try:
        content = _render_draft(template_path.read_text(encoding="utf-8-sig"), selected_type, selected_id)
    except (OSError, UnicodeError) as exc:
        raise HarnessError(f"cannot read canonical artifact template: {exc}") from exc

    parent_relative = destination_relative.parent
    _validate_existing_chain(root, parent_relative, final_kind="directory")
    change = AuthoringChange("create", destination_relative.as_posix())
    if dry_run:
        return change

    mutation_guard.require_mutation_authority(root, operation="create-artifact")
    missing: list[Path] = []
    probe = root
    for part in parent_relative.parts:
        probe = probe / part
        if not probe.exists():
            missing.append(probe)
    created_directories: list[Path] = []
    try:
        for directory in missing:
            directory.mkdir()
            created_directories.append(directory)
        _atomic_create(destination, content)
    except (OSError, HarnessError) as exc:
        _rollback_directories(created_directories)
        if isinstance(exc, HarnessError):
            raise
        raise HarnessError(f"cannot create artifact safely: {exc}") from exc
    return change
