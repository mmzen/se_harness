# WO-PLG-006: assessment under the reconciled qualification criteria

Prepared 2026-09-12 by implementation-agent for independent assurance. This is a new assessment of retained observations under the definitions merged by PR #458. It does not rewrite the original reports or grant adapter qualification.

## Candidate and identity

The assessed implementation and definition snapshot is `2885712ad815e80eba601d9129759961d5797739`, after merging `0114707723f565bfdef85e8e74f7e0fef5f402a9` into PR #456. `assessment/candidate-inputs.json` binds the current definition digests, all source/package/recorded-loaded mappings, and all twelve canonical case records. The later VREC binds the complete implementation candidate containing this assessment; its preparation must recheck every relevant source and definition digest. Changes after that assessment require another assessment.

The retained live evidence uses source `fd2419f4c26b9ba4d4a97f85b7d2b08da72b8626` and package SHA-256 `f11d94139ad7e6194147c32a80a070f34f6761900a8c737aec354ec9b447d7f6`. Fresh Git-blob hashing confirms 23 source/package/recorded-loaded mappings. Source files are identical to the live assembly source revision. Original package and native-cache bytes were not reread on this machine: the comparison uses their immutable recorded inventories. No new archive, native installation, host call, profile expansion, or combined two-host assembly was produced.

The only assessed profile is **Claude Code 2.1.266, Windows, Python 3.14.6, released evaluator 0.16.0**, selected by DEC-PLG-002. Repository governance is evaluated separately with isolated released 0.17.0 on local Python 3.13.3.

## Qualification criteria

| VER-PLG-008 condition | Assessment and retained support |
| --- | --- |
| 1. Exact positive profile | The activation decision, recorded host/runtime identities, immutable package inventory and unchanged source identify only the profile above. |
| 2. Mandatory healthy paths and shared obligations | C01-C09 pass on their prescribed native or registered-command routes. `shared-component-coverage.json` also checks the unchanged shared session/tool handlers against verified VREC-PLG-005/006. No shared obligation is waived. |
| 3. Safe active production bindings | Production before-tool hooks remain synchronous with outer timeout 60s and the originally verified inner/startup/cleanup/output margins. C12 unsafe variants remain ineligible; actual execution is reported separately. |
| 4. Preserve negative observations | C10/C11 canonical records retain `fail` and their original false qualification values. The observed edit effects, target hashes, and missing refusal remain explicit. |
| 5. Applicable accepted deviation | DEC-PLG-006 concerns WO-PLG-006 and departs from SPEC-PLG-008#PLG-HOOK-002 for the specified local hook-loss conditions. Its disposition and revisit trigger remain unchanged. |
| 6. Explicit unavailable subcases | No unavailable C10/C11 subcase is admitted or used. |
| 7. Exact current assessment inputs | `assessment/candidate-inputs.json` binds the current definitions and evidence/source/package/recorded-loaded identities. The VREC must bind the final candidate and retain this assessment. |
| 8. Bounded claim and authority | The proposed assurance outcome is qualification with a documented local limitation only. Ordinary host permissions remain in force; passing local checks grants no external or lifecycle authority. |

## Case reading

| Cases | Result under the amended criteria |
| --- | --- |
| C01 | Retained native discovery resolves the expected packaged skills and active bindings. Package and recorded loaded identity match unchanged source. |
| C02 | Startup, resume and completed compaction restoration deliver complete verified context with absolute isolated interpreter arguments. Full receipts, not model acknowledgements, are the evidence. |
| C03 | The permitted mapped edit and out-of-scope refused edit are independently correlated with hook/tool results and target hashes. |
| C04 / C07 | Malformed/missing fields and excluded profiles are rejected on the approved registered-command route. These are not new native pending-edit observations. |
| C05 / C08 | Missing bindings/runtime and failed identity remain visibly unready. Logical failure at exit 0 is distinguished from a crash. |
| C06 | Supported argument transport and explicit unsupported-tool coverage remain separate from enforcement of shell/MCP effects. |
| C09 | Failed/interrupted/stalled evaluator children are cleaned up. Retained native denials in 2.764 / 2.608 / 36.106 seconds precede the host timeout; independently observed targets remain unchanged. |
| C10 | Failed enforcement: host timeout at 60.161 seconds, followed by the exact synthetic edit. No handler refusal or independent blocking control is inferred. |
| C11 | Failed enforcement: launch failure, missing output, invalid output, and binding removal after readiness, with actual edit effects and no required refusal. No unavailable C10/C11 subcase is admitted or used. |
| C12 | Unsafe asynchronous and insufficient-timeout bindings remain rejected. Both were actually exercised and allowed Write effects; the asynchronous check returned after the effect. |

## Verification and preservation

Six capture-assessment regression tests passed locally; all eight supported wire assessments were replayed on acceptance-06. The 11 runtime binding tests retain their original exact-profile results; they were not rerun on this machine. These local checks use Python 3.13.3 and do not replace the recorded native 3.14.6 profile observations.

Released integrity, released/candidate graph validation, candidate CLI help, review preflight, and release-distribution validation pass. Candidate-source doctor retains the six existing template differences from the released root; `candidate-doctor-skew.json` names them. No managed file, production adapter, shared handler, test source, accepted profile, or approved definition is changed by this continuation.

`assessment/historical-evidence-inventory.json` hashes all original evidence at the previous PR head. All canonical cases, prior reports, failed attempts and operator acceptance retain their committed bytes. Current machine checkpoint headers and the handoff result are refreshed by the released evaluator; their prior committed and checkout bytes are retained here. `packet-line-endings.json` records the LF-only header repair. The initial pre-merge checkpoint incorrectly included incoming main paths; its failed output and the corrected repository-integration/scope checks remain separate evidence.

## Assurance decision still required

The evidence supports presentation of this exact candidate for **qualification with a documented local limitation**. Enforcement qualification remains failed. The assurance owner must decide the candidate independently; this assessment records no VREC verification, merge, release or deployment decision.

DEC-PLG-006 retains the accepted reason: "I accept the hook failure as a documented local limitation". Revisit **before the first public plugin release, any supported host-profile expansion, or introduction of remote acceptance controls**. The deviation provides no waiver for healthy-path failure, wrong identity, scope errors, malformed actions, missing context, failed process cleanup or unsafe active configuration.

Unsupported shell/MCP effects, future availability, skill-ownership coexistence, combined-host packaging and independent protected-action controls remain outside this claim. The earlier Linux rehearsal failure and its unconfirmed cause remain in the original evidence; later success is not a waiver or a claimed cleanup repair.
