+++
id = "WO-RSK-003"
type = "work_order"
title = "Amend the risk-artifact skill definitions to the delegated execution model"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes three approved definitions that specify and verify how a portable skill may raise a risk. Every later assurance decision about the risk artifact reads them, and the later verification record covering WO-RSK-002 must be measured against the amended text rather than the approved one. A defect here would leave the shipped delegated behaviour specified as a direct skill effect that the contract parser refuses to represent."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/risk-management/README.md",
  "docs/engineering/risk-management/evidence/WO-RSK-003-delegated-skill-amendments.md",
  "docs/engineering/risk-management/requirements/REQ-RSK-007.md",
  "docs/engineering/risk-management/specifications/SPEC-RSK-002.md",
  "docs/engineering/risk-management/verification/VER-RSK-002.md",
  "docs/engineering/risk-management/work-orders/WO-RSK-003.md",
]

[relations]
implements = ["REQ-RSK-007"]
specifications = ["SPEC-RSK-002"]
verification = ["VER-RSK-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:55:16Z"
decided_by = "engineering-owner"
reason = "Accountable engineering-owner approval of a bounded, documentation-only amendment of three approved definitions of the risk artifact's skill integration. REQ-RSK-007, SPEC-RSK-002 and VER-RSK-002 were approved on 2026-08-25 against the schema-v2 skill surface, which main's delegated execution model replaced; under _parse_v3_contract the design they specify is unrepresentable, since SKC036 requires client.target_writer 'evaluator' and SKC038 requires effects.permitted to equal the closed profile and 'direct-target-write' to be prohibited. The amendment changes the mechanism named in the definitions and no obligation: both skills still cause a risk to be raised without a scope decision, no skill disposes, and the register still reaches the assurance packet. Scope is three definitions, the domain README, the work order and one evidence file; no executable behaviour, managed policy, contract, fixture, test, note or verification record is in scope. Authorizes no start, no release, no tag, no publication, no deployment, no maintenance mutation, no credential use, no external-policy change, no root-evaluator adoption, and decides no verification record."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T16:57:13Z"
decided_by = "engineering-owner"
reason = "Explicit start of the authorized amendment of REQ-RSK-007, SPEC-RSK-002 and VER-RSK-002 only, on the engineering owner's instruction \"Start\", after a PASS start preflight from the released 0.6.0 evaluator. Authorizes editing the six paths in the execution scope and nothing else. Authorizes no release, tag, publication, deployment, maintenance mutation, credential use, external-policy change, root-evaluator adoption, or verification-record decision, and it does not authorize superseding or re-pointing VREC-RSK-002, which is verified and has no outgoing lifecycle edge."
+++

# Work Order: Amend the risk-artifact skill definitions to the delegated execution model

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them. This is governance-only work and stops at
`implemented` unless an eligible commit-bound record explicitly covers it.

Commit-bound verification is `required` because the scope is definitions. The
template permits `not_required` only for work that solely records or transports
an already authorized decision, and this work order transports none: it changes
what `REQ-RSK-007`, `SPEC-RSK-002` and `VER-RSK-002` require, specify and
verify.

## Objective

Make the three approved definitions of the risk artifact's skill integration
describe the behaviour that is actually deliverable and actually delivered.

`REQ-RSK-007`, `SPEC-RSK-002` and `VER-RSK-002` were approved on 2026-08-25
against the schema-v2 skill surface, in which a portable skill wrote governed
targets itself and could therefore carry a `risk-raise` effect class and invoke
a `raise-risk` evaluator operation from its own effect plan. `WO-AEX-006`,
`WO-AEX-007` and `WO-AEX-008` replaced that surface with the schema-v3 closed
contracts of the delegated execution model, in which the evaluator owns every
governed-target write. Under `_parse_v3_contract` a direct `risk-raise` effect
is not merely discouraged, it is unrepresentable: `SKC036` requires
`client.direct_target_writes` false and `client.target_writer` `"evaluator"`,
and `SKC038` requires `effects.permitted` to equal the closed profile exactly
and requires `"direct-target-write"` among the prohibitions.

The substance the requirement asked for is delivered by other means and is
unaffected by this amendment: `harness-draft-change` and
`harness-execute-work-order` can still cause a risk to be raised without a
scope decision, because the standing scope exception of `REQ-RSK-006` admits a
new `identified` or `raised` risk path inside the evaluator's brokered change
bundle under the existing `draft-create` and `implementation-write` effect
classes; `harness-prepare-assurance` carries the register; and no skill has any
disposition effect. Only the mechanism named in the definitions changed.

## In scope

- `REQ-RSK-007`: the third bullet of the required response, its failure and
  boundary behaviour sentence about a disposal attempt where that sentence
  names a mechanism, and the failure-behaviour acceptance example, which is
  written against an effect plan that admits `raise-risk`.
- `SPEC-RSK-002`: rule `RSK2-SKL-001`, and rule `RSK2-SKL-003`, which advances
  the wrong versions and names a fixture file that no longer exists.
- `VER-RSK-002`: the `RSK2-SKL-001/002` matrix row and acceptance scenario 2.
- One `## Amendment record` section per amended artifact, in the form
  established by `REQ-REB-024`, `SPEC-REB-011` and `VER-REB-010` under
  `WO-REB-022`: what changed, why, measured, and an explicit statement of what
  stands verbatim.
- The domain README index entry for this work order.
- Work-order-keyed evidence.

## Out of scope

- Any change to `REQ-RSK-007`'s `statement` field, which is satisfied as
  written: the two skills do let a risk be raised, and the record of that fact
  does not depend on which component performs the write.
- `RSK2-SKL-002`, which is delivered exactly as approved.
- `RSK2-GRD-001`, `RSK2-DOC-001` and `RSK2-AMD-001..003`, all delivered as
  approved.
- `WO-RSK-002` and its execution scope, its retained evidence, `SPEC-RSK-001`,
  `REQ-RSK-001..006`, `VER-RSK-001`, `CAP-RSK-001`, `INT-RSK-001`,
  `ARCH-RSK-001` and `ADR-RSK-001`.
- Every verification record. `VREC-RSK-002` is verified and cannot be corrected
  or re-pointed, and it cannot be superseded either: `docs/engineering/WORKFLOW.json`
  gives the verification-record family no transition out of `verified`, and the
  supersession packet governs only a `ready` record. It stands as the accountable
  verified fact about commit `2d64df0`. A later record covering this work order
  and `WO-RSK-002` at a shared clean candidate commit is an ordinary additional
  record, and is a separate governance act taken outside any work order because a
  record cannot contain the hash of its own commit.
- Any executable behaviour, managed policy, contract, fixture, test or note. No
  path outside `docs/engineering/risk-management/` changes.

## Authorized decision envelope

Wording, sentence order, and the placement of each amendment record within its
artifact. Not: which rule is amended, the semantics of any amended rule, the
approved status of any artifact, any `statement` field, any lifecycle event, or
any path outside scope.

## Constraints

Amend in place and append an amendment record; do not rewrite history and do not
delete the approved wording's meaning where it still holds. Change no
frontmatter: `status`, `owners`, `created`, `updated`, `statement`,
`verification_method`, the relations and the `lifecycle_events` array of each
amended artifact stay exactly as approved, as they did in `WO-REB-022`. Use the
exact external released evaluator recorded in `.engineering-harness.toml` for
identity, integrity, graph, focus, and preflight.

## Expected change surface

Three definitions, the domain README, this work order, and one evidence file.

## Required verification

Execute `VER-RSK-002` completely plus the repository-required checks; full suite
on Windows and Linux against an independently captured baseline; released
evaluator `validate` with no new error and no lost warning; `doctor`; graph and
distribution validation; review preflight; handoff check with the complete
changed-path set.

## Evidence to record

`docs/engineering/risk-management/evidence/WO-RSK-003-delegated-skill-amendments.md`,
recording the `SKC036` and `SKC038` refusals verbatim from
`se_harness/skill_contract.py`, the closed `ALLOWED_EFFECTS` sets of both
helpers, the delivered contract versions and required operations, and the
before-and-after text of every amended statement.

## Stop and escalate conditions

Stop if an amendment would relax a pass condition, remove a refusal, change a
`statement` field, or require a path outside scope. Stop if the delivered
behaviour turns out to satisfy an approved rule as written, since then the rule
needs no amendment and the disclosure was wrong.

## Completion report format

The `harnessctl check . --artifact WO-RSK-003 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
