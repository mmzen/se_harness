+++
id = "REQ-PLG-041"
type = "requirement"
title = "Confirm the refreshed public marketplace before claiming completion"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "After authorized publication, actual public fresh-install and update observations on both hosts must match the verified package before current availability claims and overall delivery are marked complete."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner-approved marketplace and documentation correction plan, followed by the request to prepare its artifact package on 2026-09-28."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Confirm the refreshed public marketplace before claiming completion

## Need and applicability

Local qualification cannot establish that a user receives the same plugin from
the public ref. This requirement governs confirmation of the distinct 0.2.1
delivery after its separately authorized publication.

## Required outcome

Retain observations from `https://github.com/mmzen/se_harness#plugin-marketplace`
for both fresh installation and update on Codex and Claude Code. Reconcile current
availability claims only after these observations match the verified package.

## Acceptance

- The public commit preserves the preceding branch history and contains the
  accepted complete distribution. Source commit, plugin version, evaluator wheel
  and installed-content digests match the retained qualification identities.
- On each claimed host, a disposable fresh profile installs from the actual
  public ref; another profile starts with public 0.1.0 and follows the documented
  update route. Both actively load 0.2.1 with evaluator 0.19.0.
- Native startup and compaction are observed after public installation. Cache
  presence, a reported version, local paths and fixture output alone cannot pass.
- Public README and guide claims identify the observed pair, source and support
  limits. A failed or unavailable observation leaves that claim pending.
- The existing release-delivery checker reports complete only with matching,
  retained evidence for all five surfaces, including explicit unchanged reviews
  for the evaluator and release markers. Missing proof leaves delivery incomplete.

This requirement does not authorize publication, marker changes, provider
submission, a new evaluator release or changes to real user profiles.
