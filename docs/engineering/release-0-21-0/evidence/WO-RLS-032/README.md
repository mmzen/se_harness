# Plugin 0.2.4 qualification progress

Local qualification is implemented under WO-RLS-032; verification preparation
is the current next step. Marketplace publication has not occurred.

The current [contract assessment](contract-assessment.md) supersedes the progress
status below. DEC-RLS-002 is decided and RISK-RLS-002 is accepted. Both native
Codex work-to-delivery fixtures passed; Claude native and Codex Windows desktop
remain unverified. The earlier observations below are preserved as history.

## Historical progress snapshot before DEC-RLS-002

WO-RLS-032 is in progress. This evidence does not complete the work order,
prepare a ready VREC, verify the package or authorize marketplace publication.

The [continuation review](continuation-review.md) adds passing exact-package Codex
native observations and the pending decision DEC-RLS-002. Earlier failed attempts
remain below and in their original evidence.

## Exact inputs

- Approved plugin source: `4031f0fa4b5c4a95651bd928a110d8b2d94f9775`.
- Released governance: `66baa640eea3946bd041ac09e419e300fafef017`.
- Public evaluator: 0.21.0, RLS-SEH-031.
- Governing evaluator remains the separately installed 0.20.1.
- Marketplace identity SHA-256: `74f0854eadfbe962105d1aba9b594ff2f1697cd038cb27c1a01b802c1fb8d890`.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Public wheel and sdist hashes, isolated Windows install | Passed | [Public evaluator](public-evaluator.json) |
| Existing marketplace build and independent check | Passed | [Package qualification](package-qualification.json) |
| Claude native manifest validator | Passed | [Package qualification](package-qualification.json) |
| Exact-package adapter walkthrough, Windows | 41 steps passed | [Windows](portable-windows.json) |
| Exact-package adapter walkthrough, Linux | 41 steps passed | [Linux](portable-linux.json) |
| Codex fresh native profile | Pending: hook is untrusted | [Native observations](native-observations.json) |
| Claude fresh native profile | Pending: live OAuth request expired | [Native observations](native-observations.json) |
| Codex Windows desktop | Unverified | VER-IAR-021 remains required for this work |

The adapter walkthrough uses the existing resource acceptance runner. Its
assembly callback copies the independently checked release packages instead of
creating development packages. No product code or expected behavior changes.
These simulated-event checks establish adapter behavior, not native host support.
The original missing-cache and native-registration failures remain retained.

## Review and next action

The bounded change adds evidence and starts the approved work order. It changes
no runtime, instruction, template or source manifest. Existing assembly and test
tools are reused. All repository writes remain in the approved release domain.

Complete native authentication and hook trust in disposable profiles, then resume
the required matrix. Do not count a logged-in status as a successful live request.
Do not replace missing native or desktop evidence with the passing adapter tests.
DEC-RLS-001's accepted desktop risk for WO-RLS-031 supplies no waiver here.

No new verification record is prepared while these required checks are pending.
The [publication review](publication-review.md) identifies the exact package;
external authorization will be requested only after qualification and human verification.
