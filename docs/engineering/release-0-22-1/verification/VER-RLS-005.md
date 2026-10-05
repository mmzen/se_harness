+++
id = "VER-RLS-005"
type = "verification"
title = "Verify release documentation independently of public delivery"
status = "draft"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020"]
+++

# Verify release documentation independently of public delivery

## Independence

Expected facts come from the accepted release contract, VREC-SEH-033 and its exact
candidate, DEC-RLS-009/RISK-RLS-007, retained 0.2.5 public observations and provider
readback. Agreement between edited documents is not evidence. Keep evaluator
0.22.0 as governor outside the checkout. This verification covers source guidance;
it does not qualify changed packages or replace VER-RLS-038 public-route tests.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-RLO-019 | Inspect the six reviewed files, independent identity/qualification receipts and existing source/composed link tests. | Version and support statements match their named evidence; historical 0.2.5 results remain dated; no claimed 0.2.6 public test without a receipt; links resolve in the correct context. |
| REQ-RLO-020 | Inspect qualification, authorization, delivery and omission language; compare complete Git and payload digests. | Documents distinguish the stages, retain accepted desktop uncertainty, route live status to the RLS and separate observations, and make no premature completion/adoption/service claim. |

## Checks and pass criteria

On Windows, run the existing refresh-guidance and progressive-documentation tests,
the repository test runner, distribution checks and CLI help smoke check. They must
exit zero; retain actual counts and skips. Validate with released 0.22.0 and perform
the required scope, handoff and candidate checks. No new test framework or executable
change is needed. Linux product qualification remains the already verified release
evidence; this Markdown correction does not claim another Linux package run.

Review both source link resolution and the original staged README context. Preserve
the staged archives and inventories byte-for-byte. Explain the embedded preparation
snapshot and direct users to the source guide/public identity for later status.
Check the frozen-plan implementation permits the exact separate documentation commit
and hashes; do not insert a future or invented commit. The later complete plan must
reference this independent verification before claiming documentation ready.

## Retention and remaining work

Retain the review, raw command results, input/output digests and failed attempts under
evidence/WO-RLS-044/. Capture a separate verification record at the exact clean
documentation commit and obtain mmzen's human decision. Preserve VREC-SEH-033 and its
candidate. No public publication, fresh/update test, desktop pass, release decision
or hosted-service verification is supplied by these checks.
