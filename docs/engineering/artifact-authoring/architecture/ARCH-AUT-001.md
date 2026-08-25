+++
id = "ARCH-AUT-001"
type = "architecture"
title = "Authoring rules as a managed policy consumed by tools, with mechanical checks in the validator and gates"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[decision_assessment]
outcome = "adr_required"
triggers = ["cross-cutting-policy", "public-interface-or-protocol", "material-alternatives"]
rationale = "The proposal adds one managed cross-cutting policy, changes a public artifact schema (verification_method becomes an array; three attributes), adds an evaluator to the closed set, and chooses policy-plus-validator over per-type skills. Material alternatives exist. An ADR is required before this architecture can be approved."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-AUT-001", "REQ-AUT-002", "REQ-AUT-003", "REQ-AUT-004", "REQ-AUT-005", "REQ-AUT-006"]
conforms_to = ["SPEC-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "technical-owner"
+++

# Architecture: Authoring rules as a managed policy consumed by tools, with mechanical checks in the validator and gates

## Context and scope

Authoring quality must be discoverable on every route (skill, CLI, editor),
integrity-protected, and enforced where it can be. The architecture assigns
the judgement rules to one policy and the mechanical rules to the validator
and two gates, and leaves the drafting procedure where it is.

## Components and responsibilities

### Managed authoring policy
Owns the per-type checklists and guidance. Does not own lifecycle, rights,
gates, or relations.

### Requirement template
Owns the shape: five openers, attributes, six headings, the `acceptance/` link.

### Validator
Owns `W-AUT-001..004`, `E-AUT-001..002`, attribute validation, and the
vocabulary. Reads no policy text.

### Quality gates and compliance
Own `authoring_ready` and its two predicates.

### `create-artifact`
Prints the installed policy's checklist for the created type.

### `harness-draft-change`
Applies the policy; no other change.

## Dependency direction

```text
formal artifacts + machine contracts + workflow/decision/gate/traceability policies
        |
ARTIFACT_AUTHORING.md (checklists, guidance)
        |                 \
templates            create-artifact / harness-draft-change (consumers)
        |
validator + gates (mechanical rules only; independent of policy text)
```

## Trust and failure boundaries

Policy text is managed and hash-locked; a consumer cannot alter it. The
validator's rules are code, not policy text, so a policy edit cannot weaken
a check. Warnings are signals; errors and predicates fail closed.

## Quality attributes

One owner per rule; no restatement; bounded reading (the checklist is
printed once, at creation); compatibility (warnings for existing artifacts,
migration for the vocabulary).
