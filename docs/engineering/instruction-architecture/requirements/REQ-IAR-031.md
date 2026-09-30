+++
id = "REQ-IAR-031"
type = "requirement"
title = "Install and migrate with minimal repository writes"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
statement = "Installation writes only portable selection files and selected integrations; migration preserves owner content and formal history."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Human mmzen accepted the external-resource proposal and requested its artifacts, explicitly applying KIS principles, on 2026-09-30."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 3a6d75fd2981d85563f1501727a26d9718360ae76a03df0548d7423d9ffaf1d0."
+++

# Install and migrate with minimal repository writes

## Why

Repository owners need a complete usable harness without maintaining copied
generic instructions, templates or example files.

## Behavior

A fresh installation creates the configuration and lock only unless the owner
selects a repository integration. Keep caches, evaluators and instruction bundles
outside the checkout. Create formal artifacts only when requested. Existing
customized files and historical records remain owner content.

## Acceptance

- The default fresh-install diff contains exactly .engineering-harness.toml and
  .engineering-harness.lock. No root guide, policy collection, template directory,
  local skill, glossary, example artifact or empty domain is created.
- Requested CI and Git integration writes are individually disclosed by preview;
  required byte-preservation attributes remain enforced when evidence is stored.
- Migration first validates the replacement resources and instruction delivery.
  Recognized managed copies can then retire; editable seeds require explicit
  owner selection. Customized, ambiguous or linked destinations stop the affected
  migration before partial writes. Retry after interruption is safe.
- Historical artifacts, evidence and owner files preserve their bytes. Current
  documentation explains the new route; historical references retain provenance.
- Two independent repeated installations produce the same applicable file set;
  a repeat against the same selection changes nothing.
