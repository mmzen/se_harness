+++
id = "REQ-HBI-003"
type = "requirement"
title = "Assess an empty template-region class as vacuously declared, not as a failure"
status = "approved"
owners = ["repository-owner", "security-owner", "quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
statement = "IF a template-region hash-bound class covers no tracked path in the repository under assessment, THEN THE SYSTEM SHALL report the class declared with zero covered paths while still requiring its attribute rule to be present in the managed region."
verification_method = ["test"]
priority = "must"
source = "Repository issue #207; complexity audit finding P0-1 in docs/notes/complexity-audit-2026-08.md"

[relations]
derives_from = ["CAP-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T10:18:43Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I accept SPEC-HBI-001/VER-HBI-001 and I approve WO-HBI-005', for repository issue #207. The template-region empty-pattern case is assessed as vacuously declared while the attribute rule stays required."
+++

# Requirement: Assess an empty template-region class as vacuously declared, not as a failure

## Rationale

A `template`-region class is a promise about files a repository will hold
later. `evaluator-evidence` covers `docs/engineering/**/evidence/*.json`, and a
repository holds no such file until its first verification record is captured.
`SPEC-HBI-001` rule 9 today treats "pattern matches no tracked path" as a
fail-closed condition for every class, so `hash-bound-class-declared` fails in
every freshly installed repository between its first commit and its first
assurance cycle. That window is exactly when a new adopter runs `doctor` to learn
whether the installation is sound, and the answer it receives is wrong.

Fail-closed is the right property for a `repository`-region class: its owner
declared it for paths they know exist, so an empty match is a stale declaration.
It is the wrong property for a `template`-region class, because the evaluator,
not the owner, decided the pattern, and the absence of a file is not a defect the
owner can act on. What must still fail closed is the thing the owner *can* break:
the attribute rule's presence in the managed block. That obligation is unchanged
and is assessed independently by `hash-bound-attribute-effective`.

## Behavior

- Trigger: `doctor` assesses a Git working tree in which a `template`-region
  class's patterns match no tracked path.
- Response: `hash-bound-class-declared` passes for that class and its detail
  states the class and `0 tracked paths` explicitly, so a reviewer can
  distinguish a vacuous class from a covered one; `hash-bound-attribute-effective`
  still fails when the class's required attribute rule is absent from the
  managed region.
- On failure: a `repository`-region class whose patterns match no tracked path
  continues to fail `hash-bound-class-declared` naming the pattern, exactly as
  today.

## Assumptions and dependencies

- Region membership is declared per class in the shipped declaration
  (`SPEC-HBI-001` rule 1) and is the only input that distinguishes the two
  behaviors.
- `hash-bound-attribute-effective` assesses rule presence per region
  (`SPEC-HBI-001` rule 10) independently of whether any tracked path is covered,
  so relaxing the declared check cannot hide a missing rule.

## Acceptance examples

### Example: normal behavior

**Given** a repository created by `harnessctl init` with one commit and no
`VREC`, so `docs/engineering/**/evidence/*.json` matches nothing,

**When** `harnessctl doctor` runs,

**Then** `hash-bound-class-declared` passes with a detail naming
`evaluator-evidence` and `0 tracked paths`, `hash-bound-attribute-effective`
passes, and the exit status is 0.

### Example: failure behavior

**Given** the same repository with the `docs/engineering/**/evidence/*.json`
line removed from the managed `.gitattributes` block,

**When** `harnessctl doctor` runs,

**Then** `hash-bound-attribute-effective` fails naming `evaluator-evidence` and
the missing region, and the exit status is non-zero.

**Given** a declaration carrying a `repository`-region class whose pattern
matches no tracked path,

**When** the assessment runs,

**Then** `hash-bound-class-declared` fails naming that pattern and
`matches no tracked path`.

## Open decisions

None.
