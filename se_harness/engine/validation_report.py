"""The report seam: the validation report and its human rendering.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from se_harness.engine.validation_core import Artifact, Diagnostic, TAXONOMY_VERSION, VALIDATION_PLANES


@dataclass
class ValidationReport:
    artifacts: list[Artifact]
    errors: list[Diagnostic]
    warnings: list[Diagnostic]
    # SPEC-AUT-002 AUT-ADV-001: the advisory class, apart from errors and warnings.
    advisories: list[Diagnostic] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def to_dict(self, root: Path) -> dict[str, Any]:
        def relative(path: Path) -> str:
            try:
                return path.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                return path.as_posix()

        plane_counts = {
            plane: {
                "errors": sum(item.plane == plane for item in self.errors),
                "warnings": sum(item.plane == plane for item in self.warnings),
            }
            for plane in VALIDATION_PLANES
        }
        return {
            "taxonomy": TAXONOMY_VERSION,
            "valid": self.valid,
            "artifact_count": len(self.artifacts),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "advisory_count": len(self.advisories),
            "errors": [asdict(item) for item in sorted(self.errors)],
            "warnings": [asdict(item) for item in sorted(self.warnings)],
            "advisories": [asdict(item) for item in sorted(self.advisories)],
            "plane_counts": plane_counts,
            "artifacts": [
                {
                    "id": artifact.artifact_id,
                    "type": artifact.artifact_type,
                    "status": artifact.status,
                    "path": relative(artifact.path),
                }
                for artifact in sorted(self.artifacts, key=lambda item: (item.artifact_id, item.path.as_posix()))
            ],
        }


def render_human(report: ValidationReport, *, show_advisories: bool = False) -> str:
    status = "PASS" if report.valid else "FAIL"
    plane_summary = " | ".join(
        f"{plane} E{sum(item.plane == plane for item in report.errors)}/W{sum(item.plane == plane for item in report.warnings)}"
        for plane in VALIDATION_PLANES
    )
    lines = [
        f"Engineering artifact validation: {status}",
        f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)} | Advisories: {len(report.advisories)}",
        f"Planes: {plane_summary}",
    ]
    if report.errors:
        lines.append("")
        lines.append("Errors:")
        for diagnostic in sorted(report.errors):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    if report.warnings:
        lines.append("")
        lines.append("Warnings:")
        for diagnostic in sorted(report.warnings):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    if show_advisories and report.advisories:
        lines.append("")
        lines.append("Advisories:")
        for diagnostic in sorted(report.advisories):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    return "\n".join(lines)
