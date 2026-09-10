+++
id = "SPEC-DST-028"
type = "specification"
title = "Issue #433 managed-template leftovers: the retired relation in the traceability policy, the completion decider in the work-order template"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
contract = "The managed traceability policy calls the retired architecture relation refused, and the work-order template says who decides completion by default and under delegation."

[relations]
specifies = ["REQ-DST-076", "REQ-DST-077"]
+++

# Specification: Issue #433 managed-template leftovers: the retired relation in the traceability policy, the completion decider in the work-order template

## In plain words

Two sentences in the files the harness ships to every repository fell behind
the code. One rule is rewritten and one empty heading gets guidance; this
repository's own copies follow at the next root adoption.

## Scope

The standard templates `TRACEABILITY.md` and `WORK_ORDER.template.md`, one
note, and the tests that pin them and their parity with the released root.
The two `ci-pipeline` definitions of issue #433 are `SPEC-CIP-004`'s. The
root copies are `docs/engineering/TRACEABILITY.md` and
`docs/engineering/templates/WORK_ORDER.template.md`, hash-locked and taken at
the root adoption of the carrying release.

## Terms

- **Parity test.** The test in `tests/test_artifact_catalog.py` that compares
  each released root policy copy with its candidate template, modulo the
  candidate changes it declares.

## Rules

**DST-TPL-001.** `TRC-008` of the template `TRACEABILITY.md` MUST state that
`ARCH.constrains` is retired and that a validator refuses every such relation
with `E016`, whatever the architecture's status.

**DST-TPL-002.** `TRC-008` MUST name `addresses` and `conforms_to` as the only
form and MUST NOT promise the classification of a historical relation or a
migration report.

**DST-TPL-003.** `TRC-008` MUST keep its sentence that installation and
upgrade never rewrite repository-owned artifacts, and no other line of the
template MAY change.

**DST-TPL-004.** The "Completion report format" heading of
`WORK_ORDER.template.md` MUST carry guidance naming who decides completion:
the engineering owner, or the `delegated-executor` under
`[delegation] class = "execution"` while the required check is `success`.

**DST-TPL-005.** `docs/notes/harness-uml-model.md` MUST say the relation is
retired and refused, not that older completed artifacts may still carry it.

**DST-TPL-006.** `tests/test_artifact_catalog.py` MUST declare the two
template changes as candidate exceptions against the released root and take
its equality branch once a root carries them.

**DST-TPL-007.** Tests MUST pin DST-TPL-001 to DST-TPL-005: the words retired,
refuses and `E016` in the rule, the absence of `compatibility-only` and
`MAY classify`, the template guidance, the note.

**DST-TPL-008.** This work MUST NOT change a root managed byte, the lock, or
any existing work order; the corpus keeps its completion sentences as records
of their time.

**DST-TPL-009.** The root-adoption work order of the carrying release MUST
take both template changes into `docs/engineering/TRACEABILITY.md` and
`docs/engineering/templates/WORK_ORDER.template.md`.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| the template rule still says compatibility-only or promises a migration report | the template test fails naming the phrase | test failure |
| the completion report heading has nothing under it, or names one decider only | the template test fails naming the heading | test failure |
| the released root and the candidate template differ outside the two declared changes | the parity test fails with the differing lines | test failure |
| a root carrying both changes is adopted | the parity test takes its equality branch and passes | none |
| the note still says older artifacts may carry the relation | the note test fails naming the sentence | test failure |

## Examples

**Given** the candidate template, **when** `TRC-008` is read, **then** it says
`ARCH.constrains` is retired, refused with `E016` whatever the architecture's
status, and that `addresses` and `conforms_to` are the only form (DST-TPL-001,
DST-TPL-002).

**Given** a work order drafted from the candidate template, **when** its
completion section is read, **then** the guidance names the engineering owner
and the `delegated-executor` under the execution class (DST-TPL-004).

**Given** this repository under the 0.17.0 root, **when** the parity test
runs, **then** it strips the two declared changes from the candidate copies
and finds them equal to the root copies (DST-TPL-006).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-DST-076` | DST-TPL-001, DST-TPL-002, DST-TPL-003, DST-TPL-005, DST-TPL-006, DST-TPL-007, DST-TPL-008, DST-TPL-009 |
| `REQ-DST-077` | DST-TPL-004, DST-TPL-006, DST-TPL-007, DST-TPL-008, DST-TPL-009 |

## Not decided here

- The exact wording of the rewritten rule and of the template guidance,
  within the rules above.
- Where the new tests live: beside the existing template tests or in a
  module of their own.
- Whether the root-adoption work order also drops other lines; DST-TPL-009
  binds only the two changes.
