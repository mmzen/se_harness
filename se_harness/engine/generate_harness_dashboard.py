#!/usr/bin/env python3
"""Generate a deterministic static engineering-harness dashboard bundle.

The generator reuses the repository validator as the authoritative parser and
validation core. It adds read-only graph projection, coverage, impact support,
derived consistency findings, readiness evidence, controlled experiment import,
and a progressively loaded viewer. A module of the ``se_harness.engine`` package
(SPEC-ECP-024 ECP-ENG-001), runnable as ``python -m se_harness.engine.generate_harness_dashboard``.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from se_harness.engine.validate_engineering_artifacts import ValidationReport, validate_repository
# ECP-ENG-007, ECP-ENG-008: the package definitions the generator reads, importable here for its readers.
from se_harness.engine.validate_engineering_artifacts import coverage_rows, specification_rules  # noqa: F401
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES  # noqa: F401

# The seams of this module (SPEC-ECP-024 ECP-ENG-018): every public name stays importable here.
from se_harness.engine.dashboard_snapshot import (  # noqa: F401
    ACTIVE_WORK_ORDER_STATUSES,
    ALLOWED_EVIDENCE_SUFFIXES,
    ContentBudget,
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_EXPERIMENT_ROOT,
    DEFAULT_OUTPUT_ROOT,
    EXPERIMENT_MEASURES,
    EXPERIMENT_SCHEMA,
    FINDING_RULES_VERSION,
    GITHUB_REMOTE,
    GenerationError,
    INACTIVE_GOVERNING_STATUSES,
    MAX_CONTENT_DOCUMENT_BYTES,
    MAX_CONTENT_TOTAL_BYTES,
    MAX_EXPERIMENT_BYTES,
    QUALITY_GATES_VERSION,
    SEVERITY_ORDER,
    SNAPSHOT_SCHEMA,
    TEMPORAL_REASSESSMENT_INACTIVE_STATUSES,
    TEMPORAL_REASSESSMENT_RELATIONS,
    TEMPORAL_REASSESSMENT_WORK_ORDER_STATUSES,
    WORK_ORDER_RELATIONS,
    build_architecture_transitive_relations,
    build_coverage,
    build_declared_relations,
    build_evidence_documents,
    build_findings,
    build_readiness,
    build_revision_provenance,
    build_snapshot,
    discover_evidence,
    distribution_table,
    git_commit_availability,
    git_object_format,
    git_revision,
    git_source_url,
    import_experiments,
    is_within,
    normalize_artifacts,
    normalize_diagnostics,
    project_evidence_document,
    repository_relative,
    resolve_artifact_root,
    resolve_output_root,
    resolve_repository_root,
    text_list,
    text_value,
)
from se_harness.engine.dashboard_bundle import (  # noqa: F401
    ARTIFACT_RESOURCE_SCHEMA,
    BOOTSTRAP_SCHEMA,
    BUNDLE_SCHEMA,
    MAX_SUMMARY_BYTES,
    READINESS_RESOURCE_SCHEMA,
    SUMMARY_RESOURCE_SCHEMA,
    TOPOLOGY_ACCEPTANCE_BYTES,
    TOPOLOGY_RESOURCE_SCHEMA,
    build_dashboard_bundle,
    build_explorer_metrics,
    render_dashboard,
    serialize_compact_json,
    serialize_json,
    sha256_text,
    topology_target_exceeded,
    verify_serialized_bundle,
    write_output_transactionally,
)


GENERATION_SCHEMA = "harness-dashboard-generation-v2"
MAX_INDEX_BYTES = 524_288


def generate_snapshot(
    repository_root: Path,
    artifact_root: Path | None = None,
) -> tuple[dict[str, Any], ValidationReport, Path]:
    resolved_repository = resolve_repository_root(repository_root)
    resolved_artifacts = resolve_artifact_root(resolved_repository, artifact_root)
    report = validate_repository(resolved_repository, resolved_artifacts)
    return build_snapshot(resolved_repository, resolved_artifacts, report), report, resolved_artifacts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic static engineering-harness dashboard bundle."
    )
    parser.add_argument("--root", type=Path, required=True, help="Repository root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory; default: target/harness-dashboard below --root.",
    )
    return parser


def _display_output(output_root: Path, repository_root: Path) -> str:
    if is_within(output_root, repository_root):
        return output_root.relative_to(repository_root).as_posix()
    return "<explicit-external-output>"


def generate_bundle(
    repository_root: Path,
    artifact_root: Path | None = None,
    output: Path | None = None,
    *,
    report: ValidationReport | None = None,
    started: float | None = None,
) -> tuple[ValidationReport, dict[str, Any], dict[str, Any]]:
    """Validate once (or take the caller's report, ECP-ENG-011), build the snapshot and the
    bundle, and write the output transactionally; return the report, the snapshot and the
    generation summary. `main` prints from them; provenance takes the manifest digest."""

    started = time.perf_counter() if started is None else started
    repository_root = resolve_repository_root(repository_root)
    artifact_root = resolve_artifact_root(repository_root, artifact_root)
    output_root = resolve_output_root(repository_root, artifact_root, output)

    def validate_output() -> None:
        if resolve_output_root(repository_root, artifact_root, output) != output_root:
            raise GenerationError("output root changed during generation")
    if report is None:
        report = validate_repository(repository_root, artifact_root)
    snapshot = build_snapshot(repository_root, artifact_root, report)
    bootstrap, manifest, resource_files, bundle_observations = build_dashboard_bundle(snapshot)
    manifest_text = serialize_json(manifest)
    dashboard_text = render_dashboard(bootstrap)
    dashboard_bytes = len(dashboard_text.encode("utf-8"))
    if dashboard_bytes > MAX_INDEX_BYTES:
        raise GenerationError(
            f"dashboard index exceeds {MAX_INDEX_BYTES} UTF-8 bytes"
        )
    content_records = [
        artifact["content"]
        for artifact in snapshot["artifacts"]
        if isinstance(artifact.get("content"), dict)
    ] + list(snapshot.get("evidence_documents", []))
    outcome = "generated-valid" if report.valid else "generated-invalid"
    summary = {
        "schema": GENERATION_SCHEMA,
        "outcome": outcome,
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "repository_revision": snapshot["repository"]["revision"],
        "artifact_count": len(snapshot["artifacts"]),
        "relation_count": len(snapshot["relations"]),
        "validator_error_count": len(report.errors),
        "warning_count": sum(1 for item in snapshot["findings"] if item["severity"] == "warning"),
        "content_document_count": sum(1 for item in content_records if item.get("state") == "included"),
        "content_omitted_count": sum(1 for item in content_records if item.get("state") == "omitted"),
        "content_projected_bytes": sum(
            int(item.get("bytes") or 0)
            for item in content_records
            if item.get("state") == "included"
        ),
        "output": _display_output(output_root, repository_root),
        "bundle_schema": BUNDLE_SCHEMA,
        "manifest_sha256": sha256_text(manifest_text),
        "dashboard_sha256": sha256_text(dashboard_text),
        "dashboard_bytes": dashboard_bytes,
        "manifest_bytes": len(manifest_text.encode("utf-8")),
        "resource_count": bundle_observations["resource_count"],
        "resource_bytes": bundle_observations["resource_bytes"],
        "resource_role_counts": bundle_observations["role_counts"],
        "resource_role_bytes": bundle_observations["role_bytes"],
        "largest_resource": bundle_observations["largest_resource"],
        "topology_acceptance_bytes": TOPOLOGY_ACCEPTANCE_BYTES,
        "topology_target_exceeded": bundle_observations["topology_target_exceeded"],
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
    }
    summary["output_bytes_excluding_summary"] = (
        dashboard_bytes
        + len(manifest_text.encode("utf-8"))
        + int(bundle_observations["resource_bytes"])
    )
    write_output_transactionally(
        output_root,
        {
            "dashboard-manifest.json": manifest_text,
            "generation-summary.json": serialize_json(summary),
            "index.html": dashboard_text,
            **resource_files,
        },
        validate_output=validate_output,
    )
    return report, snapshot, summary


def main(argv: Iterable[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        report, snapshot, summary = generate_bundle(args.root, None, args.output, started=started)
        label = "PASS" if report.valid else "INVALID"
        print(
            "Harness Explorer generation: "
            f"{label} | Artifacts: {len(snapshot['artifacts'])} | "
            f"Relations: {len(snapshot['relations'])} | "
            f"Errors: {len(report.errors)} | "
            f"Warnings: {summary['warning_count']} | "
            f"Output: {summary['output']} | "
            f"Manifest: {summary['manifest_sha256']}"
        )
        for diagnostic in report.errors:
            print(f"[{diagnostic.code}] {diagnostic.path}: {diagnostic.message}", file=sys.stderr)
        return 0 if report.valid else 1
    except (GenerationError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Harness Explorer generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
