# Verification assessment: repository adoption of 0.22.0

The repository and CI select released evaluator **0.22.0**. Development source
is **0.22.1**, which is not published. The complete implementation tested here
is `9c290cce29176c4d4c3bbcdef9919c02c7b658f5`. The original comparison base is `b9821e3a3ef3f821f36cc92da7fa4ce900f7e750`.
The later candidate commit adds only retained evidence and completion records.
This assessment prepares human verification; it does not supply that decision.

## Requirements and checks

| Requirement / contract check | Result and evidence |
| --- | --- |
| REQ-REB-027: exact released evaluator and ordinary upgrade | Pass. RLS-SEH-032 supplies the wheel and payload identities. Identity, doctor, released-root qualification, actual installer transaction and repeat preview pass. See ../WO-HUP-028/implementation-checks.json and implementation-raw.zip there. |
| REQ-IAR-031: owner preservation and external resources | Pass. The installer changes only configuration and lock. Protected tracked bytes, including AGENTS.md, remain intact; no instruction copies are added. Resource lookup and direct session activation select 0.22.0. The 12-file adoption diff matches the reviewed patch exactly. See ../WO-HUP-028/implementation-report.md and raw archive. |
| REQ-IAR-031: CI, source versions and guidance | Pass locally. CI selects the exact public 0.22.0 wheel; both source declarations are 0.22.1; derivation has no PRE008. The seven owner documents agree with this state. The original 127-test focused adoption run passes with two skips; the final full suite covers those tests again. |
| REQ-REB-027: release decision identity | Pass. The original checker fails the named-human case. The reviewed correction accepts matching named-human and legacy identities and rejects missing, blank, non-string or mismatched identities. All 35 predecessor tests pass, with two platform skips. See review.md, prototype-results.json and this directory's implementation-raw.zip. |
| VER-HUP-024: real predecessor plan and assessment | Pass on the actual combined implementation. Both commands select the unchanged RLS-SEH-032 and WO-HUP-028 upgrade transaction against the original trusted base. Identity, doctor and validation pass. See corrected-predecessor-plan.json and corrected-predecessor-assessment.json in this directory's raw archive. |
| VER-HUP-005: actual CI upgrade helper rehearsal | Pass. The trusted baseline export upgrades from 0.21.0 to public 0.22.0 and returns the expected canonical lock. See upgrade-handover-1/ inside ../WO-HUP-028/implementation-raw.zip. |
| Both contracts: full checks | Pass locally: 1,262 tests, 22 skips; zero validation errors, 61 existing warnings. Distribution checks passed for 22 records; CLI help passed. See both implementation-checks.json files and raw archives. |
| Both contracts: handoff and capture | Evaluator results are retained with the handoff packets and generated VREC. These results remain separate from this substantive assessment. |
| Hosted source/package, predecessor, Linux/Windows upgrade and integration checks | Pending review publication. They must pass before merge. |

## Diff review and simplicity

The adoption uses the released installer and existing resource layout. Owner
edits update only the approved version and guidance references. The correction
compares the two existing release decision fields and adds three test methods;
it introduces no identity registry, new role, or lifecycle rule. The trusted-base,
unique-release, version, tag, archive and transaction checks remain intact.
Historical RLS-SEH-032 and its evidence are unchanged. A matching identity string
does not by itself authenticate a human; the trusted release boundary remains.

No unresolved implementation defect was found in the reviewed scope. The final
checks exercise the correction and all source tests. Earlier successful identity,
installer and resource observations still apply because those inputs are unchanged.
The full candidate will be captured after completion and evidence retention.

## Failures and limits

The original real predecessor assessment failed on its obsolete literal
release-owner assumption; WO-HUP-029 resolves it. The earlier full-suite runner
overrode a fixture's line-ending configuration and failed one test. The retry
uses that fixture's normal configuration and passes. Preparation argument and
line-ending failures are preserved in the earlier raw archive. No failed attempt
was rewritten or converted into a pass.

The 22 skips remain visible. The 61 existing graph warnings are not acceptance
or risk decisions. Claude Code and Codex Windows desktop were not tested.
Direct session activation proves selection and resource resolution, not native
startup or compaction. The host plugin and authentication are unchanged. Hosted
checks, human verification and merge remain separate pending actions.
