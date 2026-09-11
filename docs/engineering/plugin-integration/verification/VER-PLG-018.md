+++
id = "VER-PLG-018"
type = "verification"
title = "Preserve verified plugin work during integration"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[relations]
verifies = ["REQ-PLG-017", "REQ-PLG-018", "REQ-PLG-019", "REQ-PLG-020", "REQ-PLG-021"]
+++

# Verification Contract: Preserve verified plugin work during integration

## Independence

Expected imported bytes come from the source commits and reviewed plan, not from
the assembled candidate. Approval pins plan.json SHA-256
`68b59c5837e890396701e46f5e37cc391a3ebf91d9f71c736d27e50345155aaa`.
The verifier supplies this digest independently of the current file and checks
that the source commits remain available. The operator alone decides assurance.

This contract supplements VER-PLG-010, VER-PLG-011 and VER-PLG-012 for integration.
It does not replace their cases or broaden their host-coverage claims.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-017, REQ-PLG-018 | inspection, test | INT01–INT06 | The change skill and its boundaries survive; integration has its own approved scope. |
| REQ-PLG-019 | inspection, test | INT01–INT06 | Evidence and accountable decisions retain their exact source identities. |
| REQ-PLG-020, REQ-PLG-021 | inspection, test | INT01–INT06 | Orientation and explicit briefing retain their verified helpers, contracts and effect limits. |

## Acceptance scenarios

| Case | Action | Observable pass condition | Retain |
| --- | --- | --- | --- |
| INT01 — Input identity | Verify plan digest, base and source heads before assembly. Preview both merges. | Exact approved inputs; no conflict. Changed base/head/digest stops before assembly. | Input identities and merge preview. |
| INT02 — Import preservation | Run the new checker against the completed tree. | All 3,177 imported paths have their planned modes and blob IDs. Other baseline paths remain unchanged except integration-only paths. Every source head and original VREC candidate remains an ancestor. | Machine comparison, changed-path census. |
| INT03 — Decision and evidence history | Read imported WOs/VRECs and each VREC's evidence at its bound commit. | Record bytes match the plan: VREC007/009/010 verified, VREC008 ready; WO010/011/012/017 implemented. Bindings, sidecars and lifecycle events are preserved. Candidate-era receipts remain readable, including VREC007's older handoff header. | Record hashes, candidate evidence inventory. |
| INT04 — Independent failures | Tamper with disposable inputs, one at a time. | A changed payload/mode, unexpected path, missing ancestry, changed VREC or altered plan is rejected. Coordinated plan/payload tampering fails against the independently supplied approved digest. | Expected and observed failures. |
| INT05 — Combined checks | Run released 0.17.0 doctor, validate, review preflight and Git-derived WO018 scope checks; run existing hosted lanes. | Scope uses the actual integration PR base. Required checks pass for the identified final head/merge checkout. Both Windows/Linux upgrade rehearsals and integration-package verification pass. Git archive contains at most 10,000 total entries. Missing, stale, skipped or failed required results are not passes. | Commands, run/job IDs, tested commits, results and archive count. |
| INT06 — Candidate and governance | After completion, prepare VREC011 for clean committed candidate C under authorized preparation. Retain it at G; later record the operator's decision. | C is an ancestor of G; VREC011 binds C and selected integration evidence. It remains ready until the separate assurance decision. Final-head checks pass after governance changes. No existing record or external ref changes by inference. | Capture, readback, final-head checks. |

## Property and invariant tests

New `tests/plugin_integration/stack-integration/check.py` and its failure tests
implement INT01–INT04. The CLI accepts repository, candidate revision, plan path
and the independently approved plan digest as explicit arguments. It returns a
nonzero status on mismatch and changes no repository file or lifecycle state.
The verifier runs it; its own narration is not evidence of success.

## Static and architecture checks

No source or managed-file edits are admitted beyond the frozen imports.
No new requirement, specification or architecture is introduced. Imported
behavior remains governed by SPEC-PLG-010, SPEC-PLG-011 and SPEC-PLG-012.

## Security and privacy checks

No merge to main, tag, release, publishing, deployment, credential or host
activation operation is part of acceptance. Negative fixtures use synthetic inputs.

## Performance and resilience checks

Preserve source history through merge commits. Bound new retention by the
unchanged archive limit. A conflict or changed input requires an amended plan;
the checker cannot authorize its own exception.

## Manual assessments

Reuse verified component evidence where imported bytes match. Run combined
repository checks on Windows/Linux through existing hosted lanes. This grants
no additional live Codex/Claude or universal platform claim.

## Evidence retention

Retain a report, an indexed raw-results archive, candidate/plan identities and
actual lifecycle receipts under evidence/WO-PLG-018/. Record failed attempts
alongside corrected runs. Do not embed complete repository exports.

## Residual uncertainty

This draft reports no executed integration acceptance. A Git tree preview proves
only the observed merge shape. Prior component checks and verification decisions
do not prove the future integration candidate or authorize merging it.
