+++
id = "VER-REB-013"
type = "verification"
title = "Consumer-installed validator retirement assurance"
status = "draft"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-REB-029"]
+++

# Verification Contract: Consumer-installed validator retirement assurance

## Independence

The graph readings run the exact public released evaluator from a virtual
environment outside the checkout with `-I`; the candidate checkout supplies the
tree under judgment and nothing else. The candidate-validator readings run the
edited file in this checkout and are labelled as candidate readings, never as
the governing verdict. The packaged reading runs the template as shipped inside
an ephemeral non-promotable wheel installed outside the checkout, never against
candidate source. Absence cases are static reads of the tree.

## Requirement-to-evidence matrix

`REQ-REB-029` is verified by the absence cases for the deleted names, the
inert-data cases on the six closed artifacts, the zero-error graph readings
from both validators, the packaged-copy case, and the preserved-rule case for
`REQ-REB-011`.

## Required cases

1. **Absence.** Every deleted constant, function and call site is absent from
   the candidate validator, by static read, named individually rather than by
   a single regular expression.
2. **Zero errors, candidate validator.** The full graph under the edited file.
3. **Zero errors, released evaluator.** The full graph under the evaluator
   outside the checkout, with the artifact, error and warning counts stated and
   compared to a control worktree at the same base.
4. **Inert data.** Each of `REL-SEH-008`, `REL-SEH-009`, `REL-SEH-010`,
   `REL-SEH-011`, `RLS-SEH-009` and `RLS-SEH-012` is byte-identical to its
   state before the change, still carries its retained fields, and validates
   with no rule reading them.
5. **Retained digests.** The three bindings are recomputed from the files
   themselves and match, under the suite, not under the validator.
6. **`REQ-REB-011` preserved.** A negative case shows a rejected record still
   cannot claim a version against a second ready or released successor, with
   the predecessor-schema condition gone.
7. **Packaged copy.** The template as shipped in an ephemeral non-promotable
   wheel contains none of the deleted names, and the wheel and its environment
   are deleted after the reading.
8. **Divergence declared.** Every test that pins a managed template byte-equal
   to its root copy names the exact expected difference; none is disabled,
   skipped or redirected.

## Acceptance scenarios

A repository with a retained `[bootstrap]` table validates clean. A repository
with none validates clean and unchanged. The six closed artifacts validate
clean and are not rewritten. A reader of `ARCH-REB-009` or `ADR-REB-009` finds
four typed operations and no predecessor-view service.

## Property and invariant tests

The count of `[bootstrap]` and `preparation_schema` occurrences under
`docs/engineering/release-0-6-0/` is unchanged. No new error code appears in
the taxonomy. `PV001` and `PV002` stay reserved and unused.

## Static and architecture checks

The four amendments are present, dated, and change no frontmatter field. The
root validator is byte-identical to its state before the change. The Pages lane
contains no occurrence of the retired name.

## Security and privacy checks

No credential, no network write, and no change of any hash-bound digest. The
deletion removes checks rather than adding a bypass, so the negative case is
that no artifact previously rejected by the validator becomes accepted for any
reason other than the removal of these named rules; the zero-error readings
before and after are compared artifact for artifact, not by total.

## Hosted evidence

The ordinary pull-request lanes, enumerated by run identifier per head commit,
with `validate`, both governance-migration platforms and both integration
package platforms named. No `workflow_dispatch` rehearsal is required by this
contract, and static review of the Pages lane rename is accepted as sufficient
evidence for a temporary directory name. `VER-REB-012`'s open dispatch
rehearsal is neither discharged nor re-scoped here.

## Evidence retention

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md`,
with the disclosures in one numbered section and each figure labelled with the
commit and the evaluator it was read under.
