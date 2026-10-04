"""Read-only, selected-draft admissibility (SPEC-HAG-004).

This is a snapshot query. Authentication, immutable-base comparisons and version
guards belong to its caller; no result is an approval or a mutation receipt.
"""
from collections import Counter
from dataclasses import asdict
from datetime import date
import json
import math
from pathlib import Path
import re

from se_harness.artifact_layout import ARTIFACT_TEMPLATES
from se_harness.codes import E002, E003, E_AUT_003, E_AUT_004, E_AUT_005, W_AUT_024
from se_harness.engine.validation_core import display_path, load_artifacts, parse_formal_artifact
from se_harness.engine.validation_lifecycle import validate_common_metadata
from se_harness.engine.validation_evidence import validate_type_specific_fields
from se_harness.engine.validation_authoring import validate_authoring
from se_harness.engine.validation_decisions import (
    DECISION_ASSESSMENT_OUTCOMES, DECISION_TRIGGERS, WORK_ORDER_ASSURANCE_VALUES,
    MAX_ASSESSMENT_RATIONALE_LENGTH, MAX_ASSESSOR_LENGTH,
    MAX_ASSURANCE_RATIONALE_LENGTH, MAX_ASSURANCE_DECIDER_LENGTH,
    _execution_scope_path_issue, validate_work_order_delegation,
)
from se_harness.engine.validate_engineering_artifacts import validate_artifact_catalog
from se_harness.installer import HarnessError, ensure_target, template_root
from se_harness.relation_policy import REQUIRED_RELATIONS, relation_findings

SUPPORTED_TYPES = frozenset({
    'intent', 'capability', 'requirement', 'specification', 'architecture',
    'adr', 'verification', 'work_order', 'release_contract', 'operating_contract',
})
PROTECTED_FIELDS = frozenset({'id', 'type', 'status', 'created', 'updated',
                              'lifecycle_events', 'disposition'})
PLACEHOLDER = re.compile(r'<[^>\n]+>|\b[A-Z]+-xxx\b')


def _finding(path, code, message, **detail):
    return {'path': path, 'code': code, 'message': message, 'plane': 'structure', **detail}


def _canonical_slots(template):
    """Only whole values at exact metadata fields from this evaluator's template."""
    slots = {}

    def visit(value, field):
        if isinstance(value, dict):
            for key, child in value.items():
                visit(child, field + '.' + key if field else key)
        elif isinstance(value, list):
            for child in value:
                visit(child, field)  # An array element occupies its named field.
        elif isinstance(value, str) and PLACEHOLDER.search(value):
            slots.setdefault(field, set()).add(value)

    for key, value in template.metadata.items():
        if key not in PROTECTED_FIELDS and key != 'relations':
            visit(value, key)
    return slots


def _metadata_findings(artifact, template, path):
    errors, incomplete = [], []
    slots = _canonical_slots(template)

    def is_slot(field, value):
        return isinstance(value, str) and value in slots.get(field, ())

    def error(field, message):
        errors.append(_finding(path, E_AUT_005, message, field=field))

    def visit(value, field):
        if isinstance(value, dict):
            for key, child in sorted(value.items()):
                visit(child, field + '.' + key if field else key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                if is_slot(field, child):
                    incomplete.append(_finding(path, W_AUT_024, 'Canonical authoring slot is unfinished.', field=field, index=index))
        elif is_slot(field, value):
            incomplete.append(_finding(path, W_AUT_024, 'Canonical authoring slot is unfinished.', field=field))

    for key, value in sorted(artifact.metadata.items()):
        if key not in PROTECTED_FIELDS and key != 'relations':
            visit(value, key)

    for key in ('created', 'updated'):
        value = artifact.metadata.get(key)
        if isinstance(value, str):
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(_finding(path, E002, 'Date must be a valid calendar date in YYYY-MM-DD.', field=key))

    # These tables have canonical slots that ordinary readiness predicates do
    # not permit. Check their supplied values individually, using shared enums
    # and path predicates; never remove readiness diagnostics after the fact.
    for name, kind in (('assurance', 'work_order'), ('execution_scope', 'work_order'),
                       ('decision_assessment', 'architecture')):
        if name not in artifact.metadata:
            if name == 'decision_assessment' and artifact.artifact_type == kind:
                error(name, 'Architecture decision assessment is required.')
            continue
        table = artifact.metadata[name]
        if artifact.artifact_type != kind:
            error(name, f'{name} is allowed only on {kind}.')
            continue
        canonical = template.metadata[name]
        if not isinstance(table, dict) or set(table) != set(canonical):
            error(name, f'{name} must contain exactly the declared fields: {", ".join(sorted(canonical))}.')
            continue
        for key, value in table.items():
            field = name + '.' + key
            if isinstance(canonical[key], str):
                if not isinstance(value, str) or not value.strip():
                    error(field, 'Field must be non-empty text.')
                elif not is_slot(field, value):
                    allowed = (WORK_ORDER_ASSURANCE_VALUES if key == 'commit_bound_verification'
                               else DECISION_ASSESSMENT_OUTCOMES if key == 'outcome' else None)
                    if allowed is not None and value.strip() not in allowed:
                        error(field, 'Value must be one of: ' + ', '.join(sorted(allowed)))
                    limit = ({'rationale': MAX_ASSURANCE_RATIONALE_LENGTH, 'decided_by': MAX_ASSURANCE_DECIDER_LENGTH}
                             if name == 'assurance' else
                             {'rationale': MAX_ASSESSMENT_RATIONALE_LENGTH, 'assessed_by': MAX_ASSESSOR_LENGTH}).get(key)
                    if limit is not None and len(value.strip()) > limit:
                        error(field, f'Field exceeds {limit} characters.')
            elif not isinstance(value, list):
                error(field, 'Field must be an array.')
            else:
                seen = set()
                if key == 'paths' and not value:
                    error(field, 'Execution paths must be non-empty.')
                for item in value:
                    if not isinstance(item, str) or not item.strip():
                        error(field, 'Array contains a non-string or blank value.')
                        continue
                    normalized = item.casefold() if key == 'paths' else item.strip()
                    if normalized in seen:
                        error(field, 'Array contains a duplicate or ambiguous value.')
                    seen.add(normalized)
                    if is_slot(field, item):
                        continue
                    if key == 'paths':
                        issue = _execution_scope_path_issue(item)
                        if issue:
                            error(field, issue)
                    elif item.strip() not in DECISION_TRIGGERS:
                        error(field, 'Unknown decision trigger.')
        if name == 'decision_assessment':
            outcome, triggers = table.get('outcome'), table.get('triggers')
            if outcome == 'adr_required' and triggers == []:
                error(name + '.triggers', 'adr_required must declare at least one trigger.')
            if outcome == 'no_significant_decision' and isinstance(triggers, list) and triggers:
                error(name + '.triggers', 'no_significant_decision must not declare triggers.')

    if artifact.artifact_type == 'release_contract':
        for field in ('candidate_commit', 'previous_release_tag'):
            value = artifact.metadata.get(field)
            if value is not None and not is_slot(field, value):
                if not isinstance(value, str) or not value.strip():
                    error(field, 'Field must be non-empty text.')
                elif field == 'candidate_commit' and re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', value) is None:
                    error(field, 'Candidate must be a full Git commit ID.')

    for token in sorted(set(PLACEHOLDER.findall(template.body))):
        if token in artifact.body:
            incomplete.append(_finding(path, W_AUT_024, 'Canonical body placeholder is unfinished.', field='body', placeholder=token))
    return errors, incomplete


def validate_draft(repository_root: Path, artifact_id: str) -> dict:
    """Evaluate one supported draft against one complete caller-supplied catalog."""
    root = ensure_target(repository_root, must_exist=True)
    artifact_root = root / 'docs/engineering'
    artifacts, parse_errors = load_artifacts(artifact_root, root)
    errors = [asdict(e) for e in parse_errors]
    incomplete, background = [], []
    counts = Counter(a.artifact_id for a in artifacts if a.artifact_id != '<unknown>')
    for artifact in artifacts:
        if counts[artifact.artifact_id] > 1:
            errors.append(_finding(display_path(artifact.path, root), E003, 'Duplicate artifact ID prevents an unambiguous catalog.',
                                   field='id', artifact_id=artifact.artifact_id))
    selected = [a for a in artifacts if a.artifact_id == artifact_id]
    selection = {'id': artifact_id, 'type': None, 'status': None, 'path': None}
    if len(selected) != 1:
        errors.append(_finding('docs/engineering', E_AUT_003, 'Selection must resolve exactly one artifact.', field='id', matches=len(selected)))
    else:
        artifact = selected[0]
        path = display_path(artifact.path, root)
        selection.update(type=artifact.artifact_type, status=artifact.status, path=path)
        if artifact.artifact_type not in SUPPORTED_TYPES:
            errors.append(_finding(path, E_AUT_003, 'Selected type does not support draft validation.', field='type'))
        else:
            errors.extend(asdict(e) for e in validate_common_metadata([artifact], root))
            if artifact.status != 'draft':
                errors.append(_finding(path, E_AUT_004, 'Selected artifact must be in draft.', field='status'))
            for field in ('lifecycle_events', 'disposition'):
                if field in artifact.metadata:
                    errors.append(_finding(path, E_AUT_004, 'Draft must not contain lifecycle history or disposition.', field=field))
            if artifact.status == 'draft' and not any(f in artifact.metadata for f in ('lifecycle_events', 'disposition')):
                template_path = template_root() / 'docs/engineering/templates' / ARTIFACT_TEMPLATES[artifact.artifact_type]
                template, parse_error = parse_formal_artifact(template_path, template_path.parent)
                if template is None or parse_error:
                    raise HarnessError('Canonical evaluator template cannot be parsed: ' + str(template_path))
                errors.extend(asdict(e) for e in validate_type_specific_fields([artifact], root))
                errors.extend(asdict(e) for e in validate_work_order_delegation([artifact], root))
                authoring_errors, _, _ = validate_authoring(artifacts, root)
                errors.extend(asdict(e) for e in authoring_errors if e.path == path)
                metadata_errors, incomplete = _metadata_findings(artifact, template, path)
                errors.extend(metadata_errors)
                catalog = {a.artifact_id: a for a in artifacts if counts[a.artifact_id] == 1}
                edge_errors, edge_slots = relation_findings(artifact, catalog, path, template_relations=template.relations)
                errors.extend(edge_errors)
                incomplete.extend(edge_slots)
                required = set(REQUIRED_RELATIONS.get(artifact.artifact_type, ())) | set(template.relations)
                for relation in sorted(required):
                    if relation not in artifact.relations or artifact.relations[relation] == []:
                        incomplete.append(_finding(path, W_AUT_024, 'Required authoring relation is unfinished.',
                                                   field='relations.' + relation, relation=relation))

    # Full normal findings remain visible for unselected records. Catalog blockers
    # above apply globally; no diagnostic plane/code is suppressed to admit a draft.
    report = validate_artifact_catalog(root, artifact_root, artifacts, parse_errors)
    for severity, findings in (('error', report.errors), ('warning', report.warnings), ('advisory', report.advisories)):
        background.extend({**asdict(f), 'severity': severity} for f in findings if f.path != selection['path'])

    def stable(items):
        # TOML has dates as well as JSON primitives, including in malformed targets.
        def json_value(value):
            if isinstance(value, dict):
                return {key: json_value(child) for key, child in value.items()}
            if isinstance(value, list):
                return [json_value(child) for child in value]
            if isinstance(value, float) and not math.isfinite(value):
                return {'type': 'float', 'value': str(value)}
            if value is None or isinstance(value, (str, int, float, bool)):
                return value
            return {'type': type(value).__name__, 'value': str(value)}

        encoded = {json.dumps(json_value(f), sort_keys=True, allow_nan=False) for f in items}
        return [json.loads(item) for item in sorted(encoded)]

    return {'schema': 'se-harness-draft-validation-v1', 'selection': selection,
            'admissible': not errors, 'errors': stable(errors),
            'incomplete': stable(incomplete), 'background': stable(background)}


def render_human(result):
    selection = result['selection']
    lines = [f"Draft {selection['id']}: {'admissible' if result['admissible'] else 'refused'}",
             f"Selection: {selection['type']} / {selection['status']} / {selection['path']}"]
    for group in ('errors', 'incomplete', 'background'):
        lines.append(f'{group}: {len(result[group])}')
        for finding in result[group]:
            lines.append('  ' + json.dumps(finding, sort_keys=True, ensure_ascii=True))
    return '\n'.join(lines)
