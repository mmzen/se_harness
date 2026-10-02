# Plugin 0.2.4 qualification assessment

## Decision and scope

Human mmzen accepted DEC-RLS-002 with the response “I accept”. Released evaluator
0.20.1 recorded the decision and accepted RISK-RLS-002. The decision applies only
to WO-RLS-032 and the exact plugin 0.2.4 assembly below. Claude native qualification
and Codex Windows desktop remain **unverified**, not passed.

This assessment covers package qualification and its verification preparation.
Marketplace publication, public installation/update tests, moving release markers
and repository adoption remain separate actions. Overall delivery is incomplete.

## Exact inputs

- Product source: `4031f0fa4b5c4a95651bd928a110d8b2d94f9775`.
- Released governance: `66baa640eea3946bd041ac09e419e300fafef017`.
- Evaluator release: RLS-SEH-031, version 0.21.0.
- Public wheel SHA-256: `13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789`.
- Package identity SHA-256: `74f0854eadfbe962105d1aba9b594ff2f1697cd038cb27c1a01b802c1fb8d890`.
- Complete change baseline: `66baa640eea3946bd041ac09e419e300fafef017`.

The governing evaluator for the product checkout remains 0.20.1. The released
0.21.0 evaluator is the system under test in disposable fixtures. No adoption
occurred. [Public readback](public-evaluator.json), [assembly](package-qualification.json)
and the [independent recheck](package-recheck.json) bind these exact bytes.

## VER-RLS-031

| Requirement | Assessment | Evidence and limits |
| --- | --- | --- |
| REQ-PLG-002: shared package assembly | Passed | Builder and independent checker agree on both trees, inventories and archives. Both contain the exact public wheel and shared source assets. Claude manifest validation and native Codex installation/file comparison passed. No Python runtime or separate policy edition was added. |
| REQ-IAR-030: delivery and recovery | Codex CLI/app-server and portable checks passed; two host gaps remain unverified under DEC-RLS-002 | Native entry digests, host versions, sessions, startup, manual/automatic compaction, resume, parallel selection and workflow observations are retained below. No simulated event or CLI result is described as desktop evidence. |
| REQ-RLO-018: delivery handoff | Inputs explicit; external actions pending | publication-review.md identifies the source, wheel, archives, package and observed old marketplace parent. delivery-plan.json carries the five surfaces forward. WO-RLS-033 retains public fresh/update and current-documentation obligations. |

## VER-IAR-021

| Criterion | Assessment | Evidence |
| --- | --- | --- |
| Bootstrap and activation after cloning | Passed on native Codex CLI/app-server; Claude unverified under DEC-RLS-002 | codex-native-current.json retains native bootstrap before cloning, actual session ID, clone, activation and full entry identity. Repository instruction copies are absent in the successor fixture. |
| Native delivery and recovery | Passed on Codex CLI/app-server; Claude and Codex Windows desktop unverified under DEC-RLS-002 | codex-native-current.json retains manual and actual automatic compaction, resume and full entry comparisons. Helpers and simulated callbacks are not native proof. |
| Two release selections | Passed on Codex CLI/app-server and portable adapters | codex-native-boundaries.json shows native 0.20.0/0.21.0 selections after installing the exact 0.2.4 package. portable-windows.json and portable-linux.json assess both adapters. The workflow repeats on both releases. |
| Parallel sessions and setup | Passed for native Codex session isolation and portable setup controls; Claude native unverified | Native interleaved sessions stay independent. Windows/Linux adapter walkthroughs cover distinct release environments and controlled same-identity setup contention. Existing activation/setup regression tests cover atomic replacement and partial-environment refusal. |
| Selection failure and switching | Passed for observed native Codex boundaries and portable failure cases; Claude native unverified | Native switch/clear preserves the other session; missing checkout refuses and recovers. Adapter traces retain corrupt-record refusal, failed activation preserving valid selection, and independent unselected sessions. Atomic replacement is covered by unchanged regression tests. |
| Offline and unavailable resources | Passed in portable checks | Both 41-step runs disable package-index access, reuse cached resources, reject altered resources and a missing ready marker, and preserve repository content during delivery. These are adapter observations, not additional native-host claims. |
| Repeated work and delivery handoff | Passed on native Codex CLI/app-server; Claude native unverified | cli-workflow.json and cli-workflow-traces.json retain new drafts, approved/resumed execution, exact-byte tests, scope/handoff/completion, clean local candidates and exact push/PR authority boundaries on both releases. Local fixture remotes remain empty. |
| Packaging and ownership | Passed | Assembly inventories and independent checks cover both packages. Native installation compares exact files and restores the prior disposable-profile plugin. Session records stay outside fixtures and package contents. Real credentials and settings are unchanged. |

The native Codex tests use new sessions and fixtures in an existing disposable
profile with native trust already recorded for the same hook hash. No hook-trust
bypass was used. The initial completely fresh profile's untrusted-hook result
remains in native-observations.json. Successful later runs do not erase it.

## Source tests and capture

The product source, plugin assets, tests and instructions are unchanged from the
verified release candidate. source-comparison.json records that comparison.
VREC-SEH-031 retains the prior exact-candidate Windows/Linux full-scale runs:
1,215 tests, with 21 Windows and two Linux skips. Those are reused results, not
new runs claimed by this work.

Verification capture reruns the existing delivery, activation, simple-plugin and
package-assembly suites from the clean qualification candidate. Its generated
evaluator evidence records the actual test command, output and verdict. It also
binds the retained evidence files and the capture driver's source digest.

## Failures and accepted uncertainty

Original failed setup, registration, hook-trust, authentication and workflow
attempts remain retained with later corrections. Claude produced a bootstrap
callback before its authenticated request failed; this does not establish the
complete native matrix. Historical Claude comparisons support risk assessment
only because their wheel archive and packaging differ.

The accepted risk is undetected host-specific delivery, selection or recovery
failure on the two unverified routes. Revisit before the next plugin release,
before claiming either route is verified, or before adoption relying on either
route, whichever comes first. Keep normal authentication and hook-trust controls.
DEC-RLS-002 does not waive WO-RLS-033's public-route tests.

## Implementation review

This change uses existing release assembly, native drivers, fixture procedures
and capture tools. Product code, manifests, accepted definitions and the selected
installation are unchanged. Repository additions are the required decision and
evidence within the approved release domain. Transient drivers and disposable
fixtures remain outside the repository; their observed source and results are
retained where needed to assess the evidence. No new runtime or framework was added.

Human verification is still required after a ready VREC is prepared. That verdict
will not by itself authorize the marketplace write. The old public parent must
be read again before proposing and applying the separately authorized ordinary
descendant update.
