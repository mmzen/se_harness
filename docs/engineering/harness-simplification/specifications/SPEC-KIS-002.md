+++
id = "SPEC-KIS-002"
type = "specification"
title = "Route one simplicity policy through ordinary authoring and review"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"

contract = "The existing authoring and review routes provide one generic simplicity policy without new workflow machinery."

[relations]
specifies = ["REQ-KIS-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "technical-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record technical-owner approval of SPEC-KIS-002 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."
+++

# Route one simplicity policy through ordinary authoring and review

## Rules

**KIS-DES-001.** The candidate ARTIFACT_AUTHORING.md owns the accepted shared wording
  and review questions. Judge simplicity against agreed needs, operating conditions and
  quality constraints, not project age, user count or a forbidden-mechanism list.
**KIS-DES-002.** Existing type checklists ask about necessary outcomes and promises,
  simpler adequate designs and the purpose of verification. A review-of-implemented-changes
  section challenges the specification as well as code. Material choices receive a short
  rationale in existing artifacts or review evidence, scaled to significance; trivial
  changes need no separate comparison document. Excessive approved obligations use the
  existing amendment route. Credible risk analysis can justify preventive measures.
**KIS-DES-003.** Relevant templates link to these checklists; unused verification sections
  are optional. Existing create-artifact checklist extraction supplies the questions.
  No new parser, mandatory KISS field, score, receipt, gate, state or CI job is added.
**KIS-DES-004.** The candidate router requires reading/applying the policy for authoring,
  design and review. Start and review manifests include the installed policy through the
  existing reading list. Existing AGENTS and CLAUDE router chains remain the entry paths.
**KIS-DES-005.** Common change skill instructions route drafting and definition review
  to the policy and implementation review to its final section. Evidence instructions
  retain relevant existing findings and rationale with normal evidence, without a second
  review. These common sources serve both host packages; they do not duplicate the rule.
**KIS-DES-006.** Ship candidate changes through the ordinary product release and explicit
  adoption path. Explain how editable policy/templates are selected for replacement.
  This patch does not upgrade this repository's installed 0.17.0 policies.

## Example and design choice

A displayed table's CSV export may need a direct operation. An agreed export of millions
of records with resumable downloads may justify background work. Either uses the same rule.
Neither case mandates a particular mechanism without its actual constraints.

Reuse the existing policy, checklist reader, router and reading list. A separate policy
service or automated complexity score would add maintenance without satisfying an unmet
need. No new component, dependency, trust boundary or significant architecture decision
is introduced; no separate architecture/ADR is required for these content and routing edits.

## Compatibility

Extend the authoring-policy route established by SPEC-AUT-001 and ordinary preflight
reading behavior. Preserve existing mechanical validation, authority and required quality
checks. This introduces human review guidance, not another conformance predicate.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-008 | KIS-DES-001, KIS-DES-002, KIS-DES-003, KIS-DES-004, KIS-DES-005, KIS-DES-006 |
