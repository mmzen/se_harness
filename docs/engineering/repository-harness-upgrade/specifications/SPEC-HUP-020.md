+++
id = "SPEC-HUP-020"
type = "specification"
title = "Skill-provider changes in the governor-transition assessor"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-16"
updated = "2026-09-16"
contract = "The existing assessor accepts supported skill-provider changes with an unchanged evaluator and rejects unrelated lock drift."

[relations]
specifies = ["REQ-HUP-008", "REQ-HUP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T14:03:02Z"
decided_by = "technical-owner"
reason = "The owner approved this exact reviewed package with \"i approve\" on 2026-09-16, exercising the technical-owner decision for SPEC-HUP-020. Reviewed SHA-256 27e0357c5775bf78f1b3386ac9db52a02802be7dd9a79c36735bda870079b64d. This approves the definition or bounded execution scope; it records no assurance or external-delivery decision."
+++

# Skill-provider changes in the governor-transition assessor

## Scope and prospective applicability

PR #487 exposed an integration gap: plugin ownership uses lock schema 4, but
the repository-owned assessor accepts schema 3 only. The selected evaluator
remains 0.18.0. Changing the schema check alone would still fail the assessor's
same-version whole-lock comparison.

On approval, this addendum governs WO-HUP-020 and the behavior it delivers:

- SPEC-HUP-012 HUP-LSF-007 accepts supported schema-4 plugin ownership as well
  as schema 3. Its 2026-09-12 amendment's explicit exclusion of this assessor
  is replaced for this delivery. The same exclusion preserved in the
  SPEC-PLG-021 applicability table is replaced to that extent only.
- SPEC-HUP-004 state-selection step 2 also accepts the ownership-only
  difference defined below. Every other same-version lock difference retains
  its existing refusal. Changed evaluator versions retain the existing
  transition evidence and exact released evaluator qualification procedure.
- REQ-HUP-024's approved schema-4 exception now applies to this reader; its
  pre-3 floor, digest contract and preservation of historical evidence stand.

Earlier artifact bodies, approvals and verification records remain historical
facts. Drafting this addendum does not activate it. The responsibilities and
trust boundaries of ARCH-HUP-003 and ADR-HUP-001 remain applicable.

## Rules

**HUP-OWN-001.** Parse base and target locks as data. Accept schema 3 for
repository ownership and schema 4 with a skill_ownership object selecting
provider="plugin". Read previous schema-4 binding fields as permitted by
SPEC-PLG-021 PLG-KIS-012. Refuse unsupported schemas, invalid provider records,
configuration/version disagreement and unsupported hash contracts before
evaluation. Preserve duplicate-key rejection and bounded diagnostics.

**HUP-OWN-002.** An unchanged supported lock at the same selected version
produces the existing not_applicable observation, including schema-4 roots.
A schema-3/schema-4 provider switch at that version may also produce it only
when both evaluator identities are valid and equal, the hash contract is
unchanged, and the only parsed lock differences are schema, skill_ownership
and the disposable skill entries allowed by HUP-OWN-003. All other top-level
fields and file entries must remain equal. This is an ownership change, not
evidence of an evaluator upgrade or a passing managed-root check.

**HUP-OWN-003.** Use the existing catalogue at
se_harness/skill_ownership_contract.json from the trusted base Git revision
as data for the allowed skill entries. Do not maintain a second path list or
import candidate Python code. Missing or malformed catalogue data refuses the
ownership exception. Switching to plugin ownership removes the catalogued
seed entries; restoration reinstates ordinary seed entries. Missing old seed
entries remain permitted. The plugin lock contains none of those entries.
No managed or fragment hash change is excused by this exception, and target
catalogue edits cannot widen it. Provider records are not plugin package
identity evidence.

**HUP-OWN-004.** Continue rejecting same-version evaluator changes and
unrelated lock drift. Preserve the existing changed-version assessment,
trusted-base selection, exact release and transaction bindings, checkout
immutability, output envelope and credential boundary. Ordinary managed CI
continues to validate the selected released root. The assessor remains a
standard-library script invoked with python -S; no new workflow is needed.

## Examples and failure behavior

The PR #487 schema-3 to schema-4 switch, with identical 0.18.0 evaluator
identity and unrelated entries, passes planning with transition_required=false.
A later documentation-only PR on that schema-4 root also passes. Restoration
to repository skills with the same evaluator follows the same bounded rule.
Changing a payload digest, an unrelated file entry or an unsupported provider
fails before evaluator execution. An actual version upgrade still requires
its existing exact transition evidence.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-HUP-008 | HUP-OWN-002, HUP-OWN-003, HUP-OWN-004 |
| REQ-HUP-024 | HUP-OWN-001, HUP-OWN-003, HUP-OWN-004 |

## Design rationale

Keep one bounded comparison in the existing assessor and reuse the existing
catalogue. Accepting every same-version lock change would remove the existing
drift protection; a schema-only edit would leave the reported failure. This
adds only the supported ownership distinction. It introduces no migration
framework, runtime dependency, new architecture or new approval mechanism.
Private helper names and fixture organization remain implementation choices.
