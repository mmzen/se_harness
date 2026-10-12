# Native hosted lifecycle qualification — verification assessment

## Result and scope

WO-HAG-009 and WO-HAG-010 deliver native Windows Codex CLI/Claude Code
qualification and the corrected hosted setup route. Both hosts pass NQ-01
through NQ-05 under VER-HAG-007. The actual candidate will be the clean commit
named by VREC-HAG-006, containing completed work orders and this retained
evidence. No real human verification is inferred from these observations.

## Requirement assessment

| Governing requirement | Observed result | Evidence |
| --- | --- | --- |
| REQ-HAG-011: lifecycle rehearsal with Git authority preserved | PASS for NQ-01/02/03/05 on both hosts. Agents followed the hosted route, authored definitions, completed synthetic work and prepared/assessed test VREC/RLS records. Original imported records and real host/repository boundaries are preserved. | final44-result native archives: instruction-read-trace, independent-assessment, boundary comparisons, requests, responses and replay |
| REQ-HAG-012: complete atomic effects and safe retry | PASS for NQ-03/04 on both hosts. Out-of-scope and stale operations are refused. A lost reply is recovered by its operation key; identical retry returns the original receipt and changed input under that key is refused. Twelve accepted operations per host independently replay. | Native archives: exact operation inputs/outputs, receipt lookup and replay/assessment.json |
| REQ-HAG-013: provenance and reproducible export | PASS for NQ-02/05 on both hosts. Two Claude and four Codex exports reconstruct exact files and retained Git history; synthetic VREC/RLS candidate bindings remain unchanged. | Native archives: exports, replay commands/results, original-file comparisons and component tuples |
| WO-HAG-010: hosted selection before local activation | PASS in the final native runs. The original two-file correction, preserved local route, rebuilt packages, activation tests and earlier failed trials remain retained. | WO-HAG-010/execution-support.zip and the final native instruction-read traces |

## Exact source and checks

Native qualification ran candidate `2f6ecb1433ef98cf643e0f604ed2c4258a2261e2`,
using released governor 0.22.1, candidate client 0.22.2 and plugins 0.2.7. Exact
wheel, image, dependency and fixture identities are in
[consolidation.json](consolidation.json). That index verifies 1,374 members in
eight retained archives and records byte-equivalence limits for earlier service
qualification. It does not claim equal archive/image identities where they differ.

The final verification candidate adds documentation status, retained check
results and work-order completion to the published consolidation. No native
service, client, instruction package or test-driver source changes. The new
documentation only links observed results and distinguishes historical reports.
Prior verification records and archived native run evidence are preserved
byte-for-byte. The supported handoff rebind and its previous packet are retained.

Supporting source checks pass 1,339 tests with 24 skips, distribution validation
and CLI smoke. Exact commands/runtime and the original long-path failures plus
successful process-local retry remain in the IPK local-check archive. The later
CI capacity correction and Windows/Linux package qualification were verified
separately by mmzen in VREC-IPK-002. Final clean-candidate source, distribution,
CLI and validation checks are also required during committed-candidate capture.
The generated verification record will retain their actual command and result;
full command outputs will be retained with verification preparation. Capture
must fail if a required check fails. No new native session is claimed. Refreshed
released scope, handoff and completion results are in completion-checks.zip.

## Limits and separate work

Codex's seven-tool MCP parity includes five tools from the original run and two
from a separate read-only session at the same fixed final baseline. The observer
initially watched old directories. Four delayed comparisons returned stale HTTP
409 and remain unmatched; the supplement supplies the missing parity evidence
without graph mutation or lifecycle assistance. All native command failures and
recovered errors remain visible. No corrective prompts, operator workflow
mutations or hidden scripted completion supplied the required lifecycle result.

WO-HAG-011 retains two focused Claude drafting failures under VER-HAG-008:
omitted known evaluator version and contradictory readiness/type-check claims.
Its efficiency targets are unmet. This record assesses only WO-HAG-009/010 and
VER-HAG-007; it neither verifies WO-HAG-011 nor waives a criterion. PR #543 stays
draft while that separate work remains unfinished.

Desktop, automatic startup/compaction/resume, public installation, production
operation, authentication/database ACL implementation and real Git authority
cutover are excluded. RISK-HAG-001 and RISK-HAG-002 remain raised. Acceptance
of this result does not accept those risks or authorize merge/release/deployment.
Synthetic actor decisions and test VREC/RLS records do not verify this candidate.
