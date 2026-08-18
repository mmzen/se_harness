+++
id = "INT-RLO-001"
type = "intent"
title = "Make authorized releases reproducible and routine"
status = "approved"
owners = ["product-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
+++

# Intent: Make authorized releases reproducible and routine

## Problem

After a released release record is merged, publishing SE Harness still requires a maintainer to reconstruct verified distributions, copy version and hash values between commands, create and check the tag and GitHub Release, approve and observe PyPI promotion, and separately recover or replay the public demonstration. The steps are individually controlled, but their manual composition is long and susceptible to transcription errors, incomplete external state, and inconsistent recovery. The `v0.4.1` release demonstrated the issue: package publication succeeded, while the release-triggered Pages build could not deploy because its tag ref conflicted with the main-only environment policy.

## Desired outcomes

- One accountable operator selects one released `RLS-*` already integrated into `main`.
- Automation derives every version, tag, commit, distribution, and hash identity from that record and its verified evidence.
- Credential-free qualification is separated from GitHub, PyPI, and Pages credential boundaries.
- Exact matching prior state permits a safe replay; missing, partial, ambiguous, or mismatched state stops visibly.
- GitHub Release, PyPI, Pages, public-install, and provenance observations are summarized as one release transaction without granting lifecycle authority.

## Actors and stakeholders

- The release owner authorizes the release record and initiates publication.
- The quality owner relies on reproducible candidate and public-install evidence.
- The security owner relies on least-privilege GitHub, PyPI OIDC, and Pages boundaries.
- The service owner operates PyPI and the demonstration channel.
- Engineers and coding agents maintain the workflow and deterministic checks but do not exercise accountable release or environment-approval rights.
- Consumers receive the released wheel and source distribution.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Operator-supplied release identity fields | release record, tag, two hashes, and governance identity across several commands | one released RLS ID | each release |
| Manual artifact reconstruction or hash transcription after RLS merge | required | zero | each release |
| Credential-bearing jobs that execute candidate code | zero by policy | zero | every run |
| Exact successful rerun behavior | manual diagnosis | automatic verification and bounded continuation | every replay |
| Package and demonstration result visibility | separate runs and manual checks | one linked transaction summary | every release |

## Non-goals

- Automatically preparing, approving, verifying, releasing, merging, or amending an RLS.
- General-purpose release automation for repositories that consume SE Harness.
- Removing the protected PyPI environment decision or treating workflow execution as release authority.
- Repairing a defective candidate, overwriting PyPI, moving a tag, or deleting mismatched external state.
- Adding another installation profile, runtime dependency, package format, prerelease channel, or package index.

## Principles and immutable constraints

- A workflow may act only on a released RLS committed to trusted `main` history.
- The tag always targets the RLS candidate commit; the demonstration uses the immutable main-history governance commit containing that released RLS.
- Release identity is derived once and transported as machine-readable data, never re-entered between stages.
- Candidate code and build tools run without publication credentials.
- PyPI receives exact GitHub Release assets without checkout, rebuild, stored credentials, or duplicate suppression.
- External immutable state is verified or created; it is never silently replaced.
- Automation reports observations and outcomes but performs no formal lifecycle transition.

## Approval

On 2026-08-18, after reviewing the complete release-orchestration packet, the accountable repository owner stated `ok, go implement`. This approves `INT-RLO-001`, `CAP-RLO-001`, `REQ-RLO-001` through `REQ-RLO-008`, `SPEC-RLO-001`, `ARCH-RLO-001`, `ADR-RLO-001`, `VER-RLO-001`, and authorizes the bounded implementation in `WO-RLO-001`. It does not authorize any production release, publication, deployment, or governance transition outside that work order.

## Risks and assumptions

- GitHub, PyPI, and Pages remain externally administered dependencies whose configuration can drift.
- PyPI currently binds Trusted Publishers to a top-level workflow filename and does not accept a reusable workflow as that identity. The design must preserve or deliberately migrate that external identity.
- A released RLS currently lacks machine-readable distribution hashes; schema and preparation support must be added without invalidating historical release records.
- A failure after an immutable external write can require human disposition even when the orchestrator itself is replay-safe.
