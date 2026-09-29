+++
id = "REQ-PLG-041"
type = "requirement"
title = "Confirm the refreshed public marketplace before claiming completion"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "After authorized publication, actual public fresh-install and update observations on both hosts must match the verified package before current availability claims and overall delivery are marked complete."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner-approved marketplace and documentation correction plan, followed by the request to prepare its artifact package on 2026-09-28."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "product-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 578aa670f881c02f253592abb93726bfc0fe729c1e2b3d19398c14e1acd97fca; transition input SHA-256 578aa670f881c02f253592abb93726bfc0fe729c1e2b3d19398c14e1acd97fca. Legacy 0.19.0 role product-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
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
