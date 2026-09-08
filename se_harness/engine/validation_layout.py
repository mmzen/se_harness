"""The layout seam: the canonical-location pass, alone or inside a full run.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from se_harness.artifact_layout import (
    ARTIFACT_DIRECTORIES,
    ARTIFACT_PREFIXES,
    ID_PATTERN,
    artifact_domain_from_relative_path,
    canonical_artifact_relative_path,
    common_artifact_domain,
    repository_record_relative_path,
)
from se_harness.codes import W013
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    display_path,
    load_artifacts,
    relation_targets,
)


def validate_canonical_layout(
    artifacts: list[Artifact],
    repository_root: Path,
    artifact_root: Path,
    errors: list[Diagnostic],
) -> list[Diagnostic]:
    canonical_root = repository_root / "docs" / "engineering"
    if artifact_root.resolve() != canonical_root.resolve():
        return []

    invalid_paths = {item.path for item in errors}
    id_counts = Counter(artifact.artifact_id for artifact in artifacts)
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>" and id_counts[artifact.artifact_id] == 1
    }
    warnings: list[Diagnostic] = []

    for artifact in artifacts:
        actual = display_path(artifact.path, repository_root)
        artifact_type = artifact.artifact_type
        artifact_id = artifact.artifact_id
        if (
            actual in invalid_paths
            or artifact_type not in ARTIFACT_DIRECTORIES
            or id_counts[artifact_id] != 1
            or ID_PATTERN.fullmatch(artifact_id) is None
            or not artifact_id.startswith(ARTIFACT_PREFIXES[artifact_type])
        ):
            continue

        if artifact_type in {"verification_record", "release_record"}:
            relation = "verifies_work_order" if artifact_type == "verification_record" else "releases_work"
            work_order_ids = sorted(relation_targets(artifact, relation))
            work_order_paths: list[str] = []
            complete = bool(work_order_ids)
            for work_order_id in work_order_ids:
                work_order = catalog.get(work_order_id)
                if work_order is None or work_order.artifact_type != "work_order":
                    complete = False
                    break
                work_order_paths.append(display_path(work_order.path, repository_root))
            if not complete:
                continue
            domain = common_artifact_domain(work_order_paths)
            expected = repository_record_relative_path(artifact_type, artifact_id, domain)
        else:
            domain = artifact_domain_from_relative_path(actual)
            if domain is None:
                continue
            expected = canonical_artifact_relative_path(domain, artifact_type, artifact_id)

        expected_text = expected.as_posix()
        if actual != expected_text:
            warnings.append(
                Diagnostic(
                    actual,
                    W013,
                    f"artifact '{artifact_id}' is valid outside its canonical location; expected '{expected_text}'",
                    "maintenance",
                )
            )
    return sorted(set(warnings))


def canonical_layout_diagnostics(repository_root: Path, artifact_root: Path | None = None) -> list[Diagnostic]:
    """The canonical-location warnings alone (ECP-ENG-012): the artifacts are loaded and the
    layout pass runs; the graph passes do not. Parse errors exclude their files as in a full run."""

    repository_root = repository_root.resolve()
    selected_artifact_root = (artifact_root or repository_root / "docs" / "engineering").resolve()
    if not selected_artifact_root.exists():
        return []
    artifacts, parse_errors = load_artifacts(selected_artifact_root, repository_root)
    return validate_canonical_layout(artifacts, repository_root, selected_artifact_root, list(parse_errors))
