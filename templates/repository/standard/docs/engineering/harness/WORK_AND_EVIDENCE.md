# Work and evidence

## Links from work orders (WO)

A work order (WO) selects the definitions and verification contracts (VER) that govern
its execution. Links to requirements (REQ) alone are not enough.

| Source → target | Relation | Meaning and coverage |
| --- | --- | --- |
| Work order (WO) → Requirement (REQ) | `implements` | Names every requirement (REQ) in the authorized work scope. |
| Work order (WO) → Specification (SPEC) | `specifications` | Names the specifications (SPEC) governing those requirements (REQ). |
| Work order (WO) → Architecture (ARCH) or Architecture decision (ADR) | `architecture` | Names every applicable architecture (ARCH) and every required architecture decision (ADR). |
| Work order (WO) → Verification contract (VER) | `verification` | Names the verification contracts (VER) for the work. |

For example, a work order (WO) can declare these links in its metadata. The IDs
below are examples, not records created by this document.

```toml
[relations]
implements = ["REQ-EXAMPLE-001"]
specifications = ["SPEC-EXAMPLE-001"]
verification = ["VER-EXAMPLE-001"]
```

The referenced requirement (REQ) must also link back to a capability (CAP) and intent (INT).
Add architecture (ARCH) links when architecture (ARCH) applies; do not invent them just to
fill a field.

## Links for verification, release, and operation

| Source → target | Relation | Meaning and coverage |
| --- | --- | --- |
| Verification record (VREC) → Work order (WO) | `verifies_work_order` | Names one or more work orders (WO) assessed at one exact candidate commit. |
| Verification record (VREC) → Verification contract (VER) | `conforms_to` | Names every verification contract (VER) required by those work orders (WO). |
| Verification record (VREC) → Verification record (VREC) | `superseded_by` | A superseded record names exactly one distinct eligible successor. |
| Release contract (REL) → Work order (WO) | `gates` | Names every work order (WO) the release contract (REL) permits the release to include. |
| Release record (RLS) → Release contract (REL) | `satisfies` | Names exactly one applicable release contract (REL). |
| Release record (RLS) → Verification record (VREC) | `includes_verification` | Names one or more eligible verification records (VREC) at the release's candidate commit. |
| Release record (RLS) → Work order (WO) | `releases_work` | Names exactly the combined set of work orders (WO) covered by the included verification records (VREC). |
| Operating contract (OPS) → Requirement (REQ) | `assures` | Names every requirement (REQ) covered by a continuing operational assurance claim. |

A verification contract (VER) defines what to check. A verification record
(VREC) binds the evidence and work to an exact result for a later decision.
Likewise, a release contract (REL) defines the permitted release, while a
release record (RLS) binds a particular release candidate and its decision.

## Complete work scope

Every requirement (REQ) selected by a work order (WO)
MUST link back to active capabilities (CAP) and intents (INT). It MUST also
have selected active specifications (SPEC) and verification contracts (VER).
Reuse existing artifacts where their scope applies.

A work order should cover one complete bounded outcome, including its
foreseeable tests, documentation and retained evidence. Use exact file paths
by default. Use a narrow existing component directory when the affected
files belong to that component. A matching directory does not authorize
unrelated behavior.

Prepare this scope through
[Draft work orders](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements).
Do not split predictable supporting changes into extra work orders merely
because they use different file types. A genuine expansion after approval
still needs the applicable human decision; preserve the approved history.

## Generated outputs

Existing scope rules admit the selected work order's own file, records that
directly verify or release that work order, and those records' declared
evaluator-evidence paths. This does not admit those records' parent directories.
The selected work order's own packet directory is also already admitted by
the existing scope rules; the planning report identifies that separate rule.

List other planned evidence, review and log destinations explicitly in the
work order's scope unless an existing rule covers them. A neighboring file
or a record linked only to another work order is not automatically admitted.
The conditional rule for recording risks during execution remains unchanged;
it is not a blanket admission of future files during preparation.

If a future record's ID is not allocated, mark its destination as unresolved
and explain the relationship rule expected to cover it. Do not create a
record or invent an ID to complete the plan. Once the evaluator prepares
the record, assess its actual returned record and evidence paths. An
unresolved destination is not an already covered file.

## Assurance classification

Each work order (WO) in `approved` or
`in_progress` MUST set `assurance.commit_bound_verification` to `required`
or `not_required`.

Use `required` when later decisions depend on the correctness of changes to
code, required checks, CI configuration, harness policy, artifact definitions,
or their links. These are examples of “changed trusted state”: information or
behavior that others will rely on when accepting, releasing, or operating the
result.

For example, a work order (WO) changes the code that validates artifact links.
A later release decision relies on that validation being correct. The work
order (WO) therefore needs verification tied to its exact candidate commit.

Use `not_required` only when the work solely records or transports a
verification, release, supersession, publication, or deployment decision
that an authorized human has already made. It does not make a new decision
or change the definitions, implementation, or evidence behind that decision.

For example, a work order (WO) commits an already authorized release decision
in a release record (RLS), with no change to the released code, scope, or
supporting evidence. The work records the decision; it does not reassess the
release.

A work order (WO) that combines both kinds of work MUST be split or classified
`required`. `not_required` removes the obligation to prepare a new
verification record (VREC) for that work; it does not remove required checks
or the links to verification contracts (VER).

## Verification coverage

A verification record (VREC) MUST bind one or more
work orders (WO), all their declared verification contracts (VER), retained
evidence, and one exact clean candidate commit. Preparing a verification
record (VREC) does not change its state to `verified`.

## Successor coverage

A verification record (VREC) in `superseded`
keeps its original commit, evidence, work orders (WO), and verification
contracts (VER) unchanged. Its successor MUST be a different verification record (VREC) in
`verified` or `released`, covering every original work order (WO).
A verification record (VREC) in `superseded` MUST NOT qualify a release.

## Release coverage

A release record (RLS) MUST bind one release contract
(REL), one exact candidate commit, and eligible verification records (VREC)
at that same commit. Its released-work set MUST equal the combined set of
work orders (WO) covered by those verification records (VREC). Governance
work is included only when the release record (RLS) explicitly includes
verification records (VREC) that provide eligible coverage for that work.
A related record or dashboard cannot add work to a release.

This model describes the readable record structure. This release's
`prepare-release` procedure is narrower: it requires one final verification
record covering the complete released-work set. When earlier records cover
separate parts, prepare and verify a record for the exact combined candidate
through [Verify the outcome](VERIFY_OUTCOME.md#procedure) before using that release procedure. Do not
assemble or edit a release record by hand to bypass the preparation checks.

## Operational coverage

An active operating contract (OPS) assurance claim
requires an active requirement (REQ) and at least one completed work order
(WO) implementing it. When verified provenance is required, at least one such
work order (WO) MUST be covered by a verification record (VREC) in
`verified` or `released`. Those links alone neither approve the operating
contract (OPS) nor prove continuing conformance.
