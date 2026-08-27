+++
id = "WO-REB-029"
type = "work_order"
title = "Retire the predecessor-bootstrap rules from the consumer-installed validator"
status = "in_progress"
owners = ["engineering-owner", "repository-owner", "release-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The edited file is the validator every consumer repository installs, so the change reaches other repositories at the next release and cannot be withdrawn from the ones that adopt it. It also removes the only mechanical re-derivation of six closed release artifacts, whose digests are hash-bound history."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  ".github/workflows/pages-publication.yml",
  "tests/",
  "docs/engineering/released-evaluator-boundary/",
  "docs/notes/developing-se-harness.md",
]

[relations]
implements = ["REQ-REB-029"]
specifications = ["SPEC-REB-013", "SPEC-REB-014"]
architecture = ["ARCH-REB-012", "ADR-REB-012"]
verification = ["VER-REB-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T20:11:19Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the 3 draft artifacts', on the owner review of pull request #206. Authorizes only the scope stated: deleting the predecessor-bootstrap and predecessor-view rules from the candidate copy of the managed validator under templates/repository/standard/scripts/, amending ARCH-REB-009 and ADR-REB-009 to four typed operations, retiring REQ-REB-008 and REQ-REB-010 by dated amendment, renaming the retired temporary directory in the Pages lane, extending tests/test_predecessor_bootstrap_retirement.py, and the notes, packet index and evidence document. No byte of scripts/validate_engineering_artifacts.py, the root copy, and no byte of se_harness/hash_bound_classes.json. No change to REQ-REB-011, to the six closed 0.6.0 artifacts, or to any retained evidence under docs/engineering/release-0-6-0/. No superseded status on any retired definition, no promotable distribution, and no hash-bound digest changed. SPEC-REB-013 and SPEC-REB-014 both govern: SPEC-REB-013 keeps its force and is not amended, reopened or re-scoped, and SPEC-REB-014 adds only the managed-validator rules it excludes. Approval is not a start decision, not a verification decision and not a release decision; each is a separate accountable act."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T20:16:24Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-27 by the accountable owner, 'after approval is made, you can start the work', immediately after the approval of WO-REB-029, SPEC-REB-014 and VER-REB-013 on the owner review of pull request #206. Execution is confined to the approved scope and to the execution_scope paths. The approval envelope stands unchanged: no byte of scripts/validate_engineering_artifacts.py, no byte of se_harness/hash_bound_classes.json, no change to REQ-REB-011 or to the six closed 0.6.0 artifacts, no superseded status, no promotable distribution, no hash-bound digest changed. Completion, commit-bound verification and any release decision remain separate accountable acts."
+++

# Work Order: Retire the predecessor-bootstrap rules from the consumer-installed validator

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

Finish `REQ-REB-029`. `WO-REB-028` retired the predecessor-bootstrap machinery
from product code, the entry-point scripts, the qualification surface and the
release lanes, and its approval excluded both copies of the managed validator
in terms. That exclusion was deliberate and is recorded three times: in
`REQ-REB-029`'s approval, "REQ-REB-010 and REQ-REB-011 keep their force and
retire with the managed validator in a later work order"; in `SPEC-REB-013`'s,
"the hash-locked managed validator is not edited under this specification"; and
in `docs/notes/developing-se-harness.md`. This is that later work order.

Three things remain. The validator that consumer repositories install still
carries the rules, so `REQ-REB-029`'s measure of "zero code paths that read a
contract `[bootstrap]` tuple or construct a predecessor view" is not yet met.
`ARCH-REB-009` and `ADR-REB-009` still decide a `qualify` namespace of exactly
five typed operations, one of which no longer exists. And one temporary
directory in the Pages lane still carries the retired name.

## Governing artifacts

Both specifications are selected because both specify `REQ-REB-029`.
`SPEC-REB-013` keeps its force over this work order: its reserved error codes,
its retained-history rules and its preservation of `REQ-REB-011` all still
bind. What it does not do is authorize the managed-validator edit, which it
excludes in terms; `SPEC-REB-014` authorizes that and nothing else.
`SPEC-REB-013` is not amended, reopened or re-scoped here.

The selection is also the only shape the graph admits. `ARCH-REB-012`
addresses `REQ-REB-029`, so leaving it unselected is `W022`; it conforms to
`SPEC-REB-013`, so selecting it without `SPEC-REB-013` is `W021`. Measured
against the released 0.7.1 evaluator, this is the shape whose review preflight
reads PASS once the three draft artifacts are approved.

## In scope

1. **The candidate copy of the managed validator**,
   `templates/repository/standard/scripts/validate_engineering_artifacts.py`.
   Delete the three retired schema constants at lines 58 to 60, the three
   functions `_validated_release_bootstrap` (791 to 844),
   `_bootstrap_for_release_record` (854 to 921) and
   `_validate_predecessor_view_evidence` (1135 to 1457), the bootstrap-contract
   comparison inside the evaluator-evidence binding at 1062 to 1098, the
   at-most-one-approved-contract rule at 1940 to 1954, and the call sites at
   1991 to 1992 and 2115 to 2126.
2. **`ARCH-REB-009` and `ADR-REB-009`**, by dated amendment: the namespace has
   four typed operations, not five, and the predecessor-view service the
   architecture describes is gone. No frontmatter field changes.
3. **`REQ-REB-008` and `REQ-REB-010`**, by dated retirement amendment, for the
   reason and in the exact form `WO-REB-028` used for `REQ-REB-012` and
   `REQ-REB-015`: the definition families admit no `approved` to `superseded`
   transition. `REQ-REB-011` is not retired and its rule is not touched; only
   the predecessor-schema condition that referenced it goes.
4. **`.github/workflows/pages-publication.yml`**: rename
   `$RUNNER_TEMP/predecessor-view` to a neutral name in the six lines 174 to
   187, and drop the sentence of the comment at 166 to 168 that explains the
   retained path.
5. **Tests.** Absence cases for every deleted name in the candidate validator;
   a case pinning the retained fields of the six closed artifacts as inert
   data that no rule reads; the declared candidate exception in each test that
   pins a managed template byte-equal to its root copy; and an extension of
   `tests/test_predecessor_bootstrap_retirement.py` rather than a new module.
6. **The two notes and the packet index**, for the state after this change.
7. **Evidence** at
   `docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md`.

## Out of scope

- `scripts/validate_engineering_artifacts.py`, the root copy. It is the exact
  released 0.7.1 file and hash-locked. Not one byte of it changes here, and
  the deletion reaches this repository's own verdicts only when the root
  evaluator next advances.
- `se_harness/hash_bound_classes.json`, which still binds
  `preparation_view_evidence_sha256`. The digest stays bound; only the
  validator rule that re-derived it goes.
- The bytes of `REL-SEH-008`, `REL-SEH-009`, `REL-SEH-010`, `REL-SEH-011`,
  `RLS-SEH-009` and `RLS-SEH-012`, and every retained evidence file under
  `docs/engineering/release-0-6-0/`.
- `REQ-REB-011` and the rejected-succession rules of `SPEC-REB-005`.
- Any release, publication or adoption act. Applying the `superseded` status
  to any retired definition remains a separate owner decision.
- The `workflow_dispatch` rehearsal `VER-REB-012` requires. It is that
  contract's open gap and is not re-opened, re-scoped or discharged here.

## Authorized decision envelope

Approval authorizes the deletions, the four amendments, the rename, the tests,
the notes, the packet index and the evidence. It does not authorize editing the
root validator, changing any hash-bound digest, altering retained history,
setting a `superseded` status, building a promotable distribution, or making
the verification or release decision.

## Constraints

- No credential, network write, or root change of this repository.
- The candidate copy diverges from the root copy for the first time under this
  work order. Every test that pins the two byte-equal declares the exact
  expected difference; none is redirected away from the comparison.
- The full artifact graph validates with zero errors under both the candidate
  validator and the evaluator installed outside the checkout.
- Non-promotable ephemeral wheels outside the checkout are permitted for
  package acceptance; promotable distributions are not.

## Expected change surface

One managed template, one workflow, one test module, four definitions by
amendment, two notes, the packet index, three new packet artifacts and one
evidence document. Roughly 500 deleted lines in the validator.

## Required verification

`VER-REB-013`. The retained-history cases run against the six closed artifacts
with the candidate validator and with the evaluator outside the checkout; the
packaged case runs the validator as shipped inside an ephemeral non-promotable
wheel installed outside the checkout.

## Evidence to record

The measured deletion, both validator readings on the full graph, the six
closed artifacts read as inert data, the packaged-copy reading, the
template-versus-root divergence with each declared test exception, the four
amendments quoted, the suite result against a control at the same base, and
every disclosure and gap in one numbered section.

## Stop and escalate conditions

- Any error appears on the full graph, or any of the six closed artifacts stops
  validating.
- A retained digest fails to verify from the file it binds.
- Removing a rule turns out to also remove a rule `REQ-REB-011` still needs.
- A pinning test cannot express the divergence without weakening what it pins.

## Completion report format

The schema-2 result at the handoff checkpoint, the lifecycle state, the
accountable decision, one typed next step, and the disclosures verbatim.
