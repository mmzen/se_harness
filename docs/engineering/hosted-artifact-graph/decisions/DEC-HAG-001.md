+++
id = "DEC-HAG-001"
type = "decision"
title = "Released evaluator support for standalone sandbox draft admission"
status = "open"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
kind = "question"
question = "How should the hosted adapter satisfy incomplete-draft and relationship-type admission when released evaluator 0.22.0 exposes no complete standalone draft-admission result?"
raised_by = "Codex"
recommendation = "extend-evaluator"

[[options]]
id = "extend-evaluator"
label = "Prepare a bounded evaluator extension and qualify a released version before changing the hosted evaluator pin."

[[options]]
id = "amend-adapter"
label = "Prepare an explicit hosted-contract amendment permitting service-side structural draft admission while retaining released lifecycle evaluation."

[[options]]
id = "stop"
label = "Stop the dependent hosted authoring work and retain the completed Phase 1 material."

[relations]
concerns = ["REQ-HAG-004", "REQ-HAG-007", "SPEC-HAG-002", "SPEC-HAG-003", "VER-HAG-001", "WO-HAG-001"]
blocks = ["WO-HAG-001"]
+++

# Released evaluator support for standalone sandbox draft admission

## Observed facts

HAG-API-003 requires the selected released evaluator to support legitimate
incomplete drafts while refusing malformed content and prohibited relation
types. It directs the implementer to stop and propose a contract amendment if
the release cannot express the classification without inventing policy.
WO-HAG-001 contains the matching stop condition. This decision concerns that
dependency; it does not reopen the user's completed package approval.

The isolated 0.22.0 evaluator was run against the complete public reference
commit `82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`. Observations are retained in
`../evidence/WO-HAG-001/phase1-evaluator-feasibility.json`:

- The 1,909-artifact reference validates. WO-RLS-038 context resolves its expected
  12 governing artifacts and 11 declared paths.
- Released `create-artifact` writes an incomplete requirement with template
  relation `derives_from = ["CAP-xxx"]`. Full validation then reports E006 for
  that placeholder; an empty relation reports E005.
- A real CAP-IAR-002 target passes full validation. The existing release record
  RLS-SEH-001 also passes as a derives_from target, without an error. Using this
  result as the entire admission decision would violate the SC-06 refusal.
- Missing targets, duplicate TOML and ID/type mismatches are rejected.
- Review preflight for the actual selected WO-RLS-038 passes for either new
  draft. Its typed checks cover the selected governing chain, which excludes
  this new unlinked requirement. This does not supply standalone admission.

The first Windows archive converted LF to CRLF. Git-blob comparison caught it;
export with `git -c core.autocrlf=false` corrected it. Every formal source byte
now matches Git, and key validation/context/admission cases reproduce the same
gap on exact bytes. Earlier observations remain retained.

## Options

### extend-evaluator — recommended

Prepare a separate bounded checker change with an explicit standalone
draft-admission contract. Reuse one definition of typed links for preflight and
draft admission. Distinguish authoring incompleteness from malformed TOML,
unknown supplied targets, identity/type mismatches and prohibited endpoints.
Return structured findings; a pass grants no human decision right. Preserve
ordinary repository validation and existing approval gates unless their own
reviewed contracts select a change.

Inspected implementation seams are `se_harness/engine/validation_architecture.py`,
`se_harness/engine/validation_evidence.py`, `se_harness/preflight.py`,
`se_harness/cli.py`, existing artifact-authoring/validation tests, and the matching
released command/authoring documentation. The corrective work order must name
its exact final paths and acceptance cases. WO-HAG-001 does not authorize the
additional checker paths.

Required cases: generated incomplete template, empty authoring link, valid
capability link, existing release-record link, missing non-template target,
duplicate TOML, ID/type mismatch, and unchanged approval/preflight behavior.
Qualify the actual package and release it through the existing process before
proposing the hosted evaluator-identity amendment. Candidate code must not
silently become the hosted or repository governor. This route costs a checker
release but preserves one source of evaluation policy.

### amend-adapter

Prepare a linked hosted-contract amendment explicitly assigning structural
draft checks to the service. Specify the rule source, allowed incompleteness,
version binding and tests proving that service checks cannot grant lifecycle
authority. Keep 0.22.0 for context and applicable workflow checks. This avoids
waiting for a checker release but adds a second structural-rule implementation
and its drift/qualification burden. This boundary change is not accepted here.

### stop

Leave the selected work incomplete and preserve contracts, fixtures and
observations. Do not claim the twelve-step sandbox or VER-HAG-001 complete.

## Recommendation

Choose `extend-evaluator`: the missing standalone result belongs in the same
released evaluator that owns the rules. The accountable human chooses the
correction path under DR-DECISION-DISPOSE. Affected definitions and work scope
then follow their existing procedures. This proposal grants no publication,
deployment, release acceptance or risk acceptance.

RISK-HAG-001 remains raised independently. Cypher stays in the sandbox contract.
WO-HAG-001 remains in_progress; its dependent command adapter and completion
claim wait for this decision. No disposition has been supplied or applied.
