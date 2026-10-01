+++
id = "VER-RLO-009"
type = "verification"
title = "Verify maintenance-release publication provenance"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T06:47:33Z"
decided_by = "mmzen"
reason = "Human mmzen: Ok i approve corrections. Applies the expressly approved two-issue publication correction under WO-RLO-012 and VER-RLO-009, authored to record that instruction; required commit-bound assurance applies to changed publisher checks. No claim of earlier review of these newly authored files. The verified 0.20.1 candidate, release decision and existing evidence remain preserved; only the missing tag binding is corrected. Verification acceptance and external actions remain separate."
+++

# Verify maintenance-release publication provenance

## Independence

Expected identities come from the original RLS-SEH-030, VREC-SEH-030 and
immutable candidate b9af631b850c495eace9807361ed3ec3e36a10b2, not the repaired
resolver output. Fixture expectations follow the same release binding rules.
The public 0.20.0 evaluator runs outside the checkout for governed checks.
Repository source tests are implementation evidence, not lifecycle authority.

## Requirement-to-evidence matrix

| Requirement | Method | Cases and pass criteria |
| --- | --- | --- |
| REQ-RLO-001; SPEC-RLO-001 rules 3-5 | test | PUB01: both resolvers select the first complete matching released binding when the tag is corrected after release. Later unrelated commits do not change it. Missing or conflicting tags and duplicate real records still fail. |
| REQ-RLO-001; SPEC-RLO-001 rules 3-5 | test | PUB02: a maintenance record matches its exact candidate lock although integration uses another valid lock. Both resolvers preserve its candidate and evidence digest. Evidence matching neither lock, corrupt or missing evidence, invalid lock shape and missing candidate proof still fail. Existing normal and historical replay tests pass. |
| REQ-RLO-001 | inspection, test | PUB03: RLS-SEH-030 differs only by its tag line. Existing candidate, VREC and evidence bytes are unchanged. The original two failures remain retained. |
| REQ-RLO-001 | demonstration | PUB04: run the real publication resolver against a disposable local main ref containing the correction. It returns v0.20.1, the original full candidate and all original distribution/evaluator digests. No remote write or release tag is created. |
| REQ-RLO-001 | test, inspection | PUB05: the focused publication suites and canonical full local unit suite pass on Windows; released evaluator validation, scope and handoff pass. Documentation explicitly records --tag and the before-dispatch resolver check. CI remains a separate integration check. |

## Inputs and commands

Use the correction branch derived from a0e91f65f7ead24a14d9a9c65d54ee9b05e9b7e0.
Run python -m unittest tests.test_dashboard_publication tests.test_release_orchestration
and python scripts/run_tests.py. Run publish_release.py resolve in a disposable
Git clone of the committed correction, with refs/heads/main pointing to that
local correction commit. This local ref is rehearsal input, not merged authority.
Use the selected released evaluator's validate, scope and handoff commands.

## Evidence retention and decision

Retain full commands and observed results under evidence/WO-RLO-012/.
Failed attempts remain visible. Compare the original record SHA-256
3768876259e5c1c2b1ffd507d5da3feb484c269b437e296429c6282eb8e04934
and evaluator evidence SHA-256
3d06ef9adf5b4bcb9bd9d9d93ae6ea13f35ec4f0ca9ab8338586e48254d39713.
Bind the final evidence to one clean correction commit using the supported
capture command. Human mmzen makes the separate assurance decision. No hosted
test, public publication, merge or native plugin test is claimed by this contract.
