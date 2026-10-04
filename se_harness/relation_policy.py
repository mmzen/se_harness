"""Declared source/relation/endpoint contract shared by all graph readers."""
from types import MappingProxyType

from se_harness.artifact_layout import ARTIFACT_PREFIXES
from se_harness.codes import E006, E011, W_AUT_024

ALL_ARTIFACT_TYPES = frozenset(ARTIFACT_PREFIXES)
RELATION_TARGET_TYPES = MappingProxyType({
    ('capability', 'derives_from'): frozenset({'intent'}),
    ('requirement', 'derives_from'): frozenset({'capability'}),
    ('specification', 'specifies'): frozenset({'requirement'}),
    ('architecture', 'addresses'): frozenset({'requirement'}),
    ('architecture', 'conforms_to'): frozenset({'specification'}),
    ('adr', 'decides'): frozenset({'architecture'}),
    ('verification', 'verifies'): frozenset({'requirement'}),
    ('work_order', 'implements'): frozenset({'requirement'}),
    ('work_order', 'specifications'): frozenset({'specification'}),
    ('work_order', 'architecture'): frozenset({'architecture', 'adr'}),
    ('work_order', 'verification'): frozenset({'verification'}),
    ('verification_record', 'verifies_work_order'): frozenset({'work_order'}),
    ('verification_record', 'conforms_to'): frozenset({'verification'}),
    ('verification_record', 'superseded_by'): frozenset({'verification_record'}),
    ('release_contract', 'gates'): frozenset({'work_order'}),
    ('release_record', 'satisfies'): frozenset({'release_contract'}),
    ('release_record', 'includes_verification'): frozenset({'verification_record'}),
    ('release_record', 'releases_work'): frozenset({'work_order'}),
    ('operating_contract', 'assures'): frozenset({'requirement'}),
    ('decision', 'concerns'): ALL_ARTIFACT_TYPES,
    ('decision', 'blocks'): frozenset({'requirement', 'specification', 'verification', 'architecture', 'adr', 'work_order'}),
    ('decision', 'produces'): frozenset({'requirement', 'specification', 'verification', 'architecture', 'adr', 'work_order'}),
    ('risk', 'threatens'): ALL_ARTIFACT_TYPES,
    ('risk', 'mitigated_by'): frozenset({'work_order'}),
    ('risk', 'avoided_by'): frozenset({'adr', 'decision'}),
})

REQUIRED_RELATIONS = MappingProxyType({
    'capability': ('derives_from',), 'requirement': ('derives_from',),
    'specification': ('specifies',), 'adr': ('decides',), 'verification': ('verifies',),
    'work_order': ('implements', 'specifications', 'verification'),
    'release_contract': ('gates',), 'verification_record': ('verifies_work_order', 'conforms_to'),
    'release_record': ('satisfies', 'includes_verification', 'releases_work'),
    'operating_contract': ('assures',), 'decision': ('concerns', 'blocks'),
})


def relation_findings(artifact, catalog, path, *, template_relations=None):
    """Classify each edge before rendering, with exact canonical draft slots only.

    Ordinary validation supplies no template. The draft reader supplies only the
    selected type's evaluator-owned template, after checking selection and state.
    """
    errors, incomplete = [], []
    relations = artifact.metadata.get('relations', {})
    if not isinstance(relations, dict):
        return errors, incomplete  # The common metadata predicate reports the table shape.
    for relation, targets in sorted(relations.items()):
        detail = {'path': path, 'plane': 'structure', 'field': 'relations.' + relation, 'relation': relation}

        def error(code, message, **extra):
            errors.append({**detail, 'code': code, 'message': message, **extra})

        allowed = RELATION_TARGET_TYPES.get((artifact.artifact_type, relation))
        if allowed is None:
            error(E011, f"type '{artifact.artifact_type}' does not declare relation '{relation}'")
        if not isinstance(targets, list):
            error(E006, f"relation '{relation}' must be an array of artifact IDs")
            continue
        for index, target in enumerate(targets):
            endpoint = {'index': index, 'target': target}
            if not isinstance(target, str) or not target.strip():
                error(E006, f"relation '{relation}' contains a non-string or empty target", **endpoint)
            elif allowed is not None and template_relations is not None and target in template_relations.get(relation, ()):
                incomplete.append({**detail, **endpoint, 'code': W_AUT_024,
                                   'message': 'Canonical relation slot is unfinished.'})
            elif target == artifact.artifact_id:
                error(E006, f"artifact '{artifact.artifact_id}' must not reference itself via '{relation}'", **endpoint)
            elif target not in catalog:
                error(E006, f"artifact '{artifact.artifact_id}' relation '{relation}' references unknown target '{target}'", **endpoint)
            elif allowed is not None and catalog[target].artifact_type not in allowed:
                target_type = catalog[target].artifact_type
                expected = ', '.join(sorted(allowed))
                error(E011, f"relation '{relation}' target '{target}' must have type {expected}, found {target_type}",
                      **endpoint, target_type=target_type, allowed_types=sorted(allowed))
    return errors, incomplete
