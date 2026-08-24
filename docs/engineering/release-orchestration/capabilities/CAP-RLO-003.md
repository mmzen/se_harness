+++
id = "CAP-RLO-003"
type = "capability"
title = "Rehearse the credential-free last mile before release approval"
status = "approved"
owners = ["product-owner", "release-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
derives_from = ["INT-RLO-001"]
+++

# Capability: Rehearse the credential-free last mile before release approval

## Actor and need

A release owner needs to know that the mechanics of the last mile work on every runner platform the release uses *before* granting release authority, instead of discovering a platform defect while a partially published release is already public.

## Capability statement

`A release owner can exercise the complete credential-free portion of the publication path on every supported runner platform, at any candidate, without creating a tag, release, package, deployment, or lifecycle record.`

## Boundaries

- The rehearsal exercises only the portion of the last mile that requires no publication credential: candidate export, evaluator identity, candidate qualification, tests, deterministic build, sdist normalization, bundle assembly, bundle verification, and teardown.
- Tag creation, GitHub Release materialization, PyPI promotion, Pages deployment, and public-install observation remain outside the rehearsal and unchanged.
- The rehearsal is repository policy of `mmzen/se_harness`. It is not installed, packaged, or imposed on consumers.
- A rehearsal result is derived operational evidence. It does not approve, prepare, verify, or release anything, and it does not substitute for the qualification that runs inside an authorized release.

## Outcomes

- Every credential-free publication mechanic executes on both the Linux and the Windows runner type, not on one of the two.
- Virtual-environment layout, path conversion, temporary-path identity, and teardown behave identically on both platforms or fail visibly before release approval.
- A credential-free step added to, changed in, or removed from the publication orchestrator without matching rehearsal coverage fails a required check instead of reaching a release unexercised.
- The `RLO-001` through `RLO-003` publication guarantees, the single `release_record` input, and the portable boundary established by `ADR-RLO-002` remain unchanged.

## Candidate requirements

`REQ-RLO-013` defines the cross-platform credential-free rehearsal. `REQ-RLO-014` defines fail-closed detection of divergence between the publication orchestrator and that rehearsal.

## Approval

On 2026-08-24 the accountable repository owner stated `OK go for #111`, and selected `Parallel lane + drift check` and `Fourth release-orchestration packet` from the two presented design options. This approves this capability and its linked definition artifacts under the existing `INT-RLO-001` intent. It authorizes the packet and the bounded implementation in `WO-RLO-004`; it authorizes no release, publication, deployment, or external action.

## Amendments during implementation

Stated for owner acceptance or rejection. One outcome now says "added to, changed in, or removed from" where it said only "added to". The implemented drift check compares a digest of each credential-free step, so a change inside an already-declared step and the disappearance of a declared step both fail the required check. The narrower wording would have understated the capability that was built; the change adds no scope beyond `WO-RLO-004`.
