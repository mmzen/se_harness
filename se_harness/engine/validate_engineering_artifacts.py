#!/usr/bin/env python3
"""Validate specification-driven engineering artifacts.

A module of the ``se_harness.engine`` package (SPEC-ECP-024 ECP-ENG-001): it reads
the layout tables from ``se_harness.artifact_layout`` and runs in-process for every
governance command, or as ``python -m se_harness.engine.validate_engineering_artifacts``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - version guard
    raise SystemExit("Python 3.11 or later is required (missing tomllib).") from exc


from se_harness.codes import E001

# The seams of this module (SPEC-ECP-024 ECP-ENG-017): every public name stays importable here.
from se_harness.engine.validation_core import (  # noqa: F401
    Artifact,
    Diagnostic,
    EXCLUDED_DIRECTORY_NAMES,
    ISO_DATE_PATTERN,
    TAXONOMY_VERSION,
    TYPE_PREFIX,
    VALIDATION_PLANES,
    add_error,
    discover_candidate_files,
    display_path,
    duplicate_strings,
    load_artifacts,
    load_revision_policy,
    parse_formal_artifact,
    relation_targets,
    require_non_empty_string,
    require_non_empty_string_list,
)
from se_harness.engine.validation_report import ValidationReport, render_human  # noqa: F401
from se_harness.engine.validation_lifecycle import (  # noqa: F401
    ACTIVE_COVERAGE_STATUSES,
    LifecycleStatePolicy,
    WORKFLOW_LIFECYCLES,
    WORKFLOW_TRANSITIONS,
    active_record_status,
    grants_authority,
    lifecycle_family,
    reserves_version,
    validate_common_metadata,
    validate_lifecycle_events,
)
from se_harness.engine.validation_authoring import (  # noqa: F401
    authoring_advisories,
    AUTHORING_BODY_LIMIT,
    AUTHORING_CODE_IDENTIFIER_LIMIT,
    AUTHORING_NAMED_SUBJECT,
    AUTHORING_OPENERS,
    AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT,
    AUTHORING_SENTENCE_LIMIT,
    AUTHORING_STATEMENT_LIMIT,
    AUTHORING_WHY_SENTENCE_LIMIT,
    AUTHORING_WHY_WORD_LIMIT,
    CAPABILITY_ABILITY_LIMIT,
    CAPABILITY_BODY_LIMIT,
    CAPABILITY_CODE_IDENTIFIER_LIMIT,
    CAPABILITY_NEED_SENTENCE_LIMIT,
    CAPABILITY_NEED_WORD_LIMIT,
    INTENT_BODY_LIMIT,
    INTENT_CODE_IDENTIFIER_LIMIT,
    INTENT_OUTCOME_LIMIT,
    INTENT_PROBLEM_SENTENCE_LIMIT,
    INTENT_PROBLEM_WORD_LIMIT,
    REQUIREMENT_PRIORITIES,
    RULE_IDENTIFIER,
    SPECIFICATION_CONTRACT_LIMIT,
    SPECIFICATION_KEYWORDS,
    SPECIFICATION_LEGACY_HEADINGS,
    SPECIFICATION_PROSE_LIMIT,
    SPECIFICATION_RULE_LIMIT,
    SPECIFICATION_RULE_SECTIONS,
    SPECIFICATION_UNBUDGETED_SECTIONS,
    VERIFICATION_METHODS,
    coverage_rows,
    sentences,
    specification_rules,
    validate_authoring,
)
from se_harness.engine.validation_evidence import (  # noqa: F401
    EVIDENCE_MESSAGES,
    EVIDENCE_WORK_ORDER_PATTERN,
    GIT_COMMIT_PATTERNS,
    SHA256_PATTERN,
    evidence_path_is_keyed_to,
    evidence_work_order_keys,
    validate_type_specific_metadata,
)
from se_harness.engine.validation_revision import (  # noqa: F401
    validate_operating_contract_readiness,
    validate_revision_consistency,
)
from se_harness.engine.validation_architecture import (  # noqa: F401
    RELATION_TARGET_TYPES,
    architecture_traceability_state,
    validate_architecture_traceability,
    validate_relations,
    validate_requirement_coverage,
)
from se_harness.engine.validation_decisions import (  # noqa: F401
    DECISION_ASSESSMENT_OUTCOMES,
    DECISION_KINDS,
    DECISION_TERMINAL,
    DECISION_TRIGGERS,
    DEVIATION_OPTIONS,
    MAX_ASSESSMENT_RATIONALE_LENGTH,
    MAX_ASSESSOR_LENGTH,
    MAX_ASSURANCE_DECIDER_LENGTH,
    MAX_ASSURANCE_RATIONALE_LENGTH,
    RISK_CATEGORIES,
    RISK_DISPOSED,
    RISK_MEASUREMENT_RANGE,
    RISK_OPTION_TARGETS,
    RISK_REQUIRED_FIELDS,
    RISK_STAGES,
    RISK_TERMINAL,
    WORK_ORDER_ASSURANCE_FIELDS,
    WORK_ORDER_ASSURANCE_VALUES,
    decision_assessment_state,
    standing_deviations,
    validate_decision_assessments,
    validate_decisions,
    validate_risks,
    validate_work_order_assurance,
    validate_work_order_delegation,
    validate_work_order_execution_scope,
    work_order_assurance_state,
)
from se_harness.engine.validation_layout import canonical_layout_diagnostics, validate_canonical_layout  # noqa: F401

# ECP-ENG-004 to ECP-ENG-008: the package definitions the engine reads, importable here for its readers.
from se_harness.artifact_layout import (  # noqa: F401
    ARTIFACT_DIRECTORIES,
    ARTIFACT_PREFIXES,
    ID_PATTERN,
    canonical_artifact_relative_path,
    repository_record_relative_path,
)
from se_harness.evaluator_evidence import validate_evaluator_evidence  # noqa: F401
from se_harness.front_matter import body_sections  # noqa: F401
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES, LifecycleState, load_lifecycle_registry  # noqa: F401



def validate_repository(repository_root: Path, artifact_root: Path | None = None) -> ValidationReport:
    repository_root = repository_root.resolve()
    selected_artifact_root = (artifact_root or repository_root / "docs" / "engineering").resolve()
    revision_policy = load_revision_policy(repository_root)

    artifacts, parse_errors = load_artifacts(selected_artifact_root, repository_root)
    errors = list(parse_errors)

    assessment_warnings: list[Diagnostic] = []
    traceability_warnings: list[Diagnostic] = []
    authoring_warnings: list[Diagnostic] = []
    decision_warnings: list[Diagnostic] = []
    if not selected_artifact_root.exists():
        errors.append(
            Diagnostic(
                display_path(selected_artifact_root, repository_root),
                E001,
                "artifact root does not exist",
                "structure",
            )
        )
    else:
        errors.extend(validate_common_metadata(artifacts, repository_root))
        errors.extend(validate_lifecycle_events(artifacts, repository_root))
        errors.extend(validate_type_specific_metadata(artifacts, repository_root))
        authoring_errors, authoring_warnings, authoring_advisories = validate_authoring(artifacts, repository_root)
        errors.extend(authoring_errors)
        errors.extend(validate_relations(artifacts, repository_root))
        traceability_errors, traceability_warnings = validate_architecture_traceability(
            artifacts,
            repository_root,
        )
        errors.extend(traceability_errors)
        assessment_errors, assessment_warnings = validate_decision_assessments(
            artifacts,
            repository_root,
        )
        errors.extend(assessment_errors)
        errors.extend(validate_work_order_assurance(artifacts, repository_root))
        errors.extend(validate_work_order_execution_scope(artifacts, repository_root))
        errors.extend(validate_work_order_delegation(artifacts, repository_root))
        decision_errors, decision_warnings = validate_decisions(artifacts, repository_root)
        errors.extend(decision_errors)
        risk_errors, risk_warnings = validate_risks(artifacts, repository_root)
        errors.extend(risk_errors)
        decision_warnings.extend(risk_warnings)
        errors.extend(
            validate_revision_consistency(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(
            validate_operating_contract_readiness(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(validate_requirement_coverage(artifacts, repository_root))

    warnings = [
        *assessment_warnings,
        *traceability_warnings,
        *authoring_warnings,
        *decision_warnings,
        *validate_canonical_layout(artifacts, repository_root, selected_artifact_root, errors),
    ]
    return ValidationReport(
        artifacts=artifacts,
        errors=sorted(set(errors)),
        warnings=sorted(set(warnings)),
        advisories=sorted(set(authoring_advisories)),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate engineering artifact identity, relations, and coverage.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory).")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit a machine-readable JSON report.")
    parser.add_argument(
        "--advisories", action="store_true", dest="show_advisories",
        help="List the authoring advisories (W-AUT-*) after the warnings; the JSON report always carries them.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    repository_root = args.root.resolve()
    artifact_root = None
    if artifact_root is not None and not artifact_root.is_absolute():
        artifact_root = repository_root / artifact_root

    report = validate_repository(repository_root, artifact_root)
    if args.as_json:
        print(json.dumps(report.to_dict(repository_root), indent=2, sort_keys=True))
    else:
        print(render_human(report, show_advisories=args.show_advisories))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
