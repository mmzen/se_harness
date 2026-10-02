+++
id = "VER-RLS-031"
type = "verification"
title = "Qualify plugin 0.2.4 with public evaluator 0.21.0"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 3b580cf1ba9d26b6abfca6c7fba4a9d1a1e390bfbddd270b21a0acb753f3252b; transition-input SHA256 3b580cf1ba9d26b6abfca6c7fba4a9d1a1e390bfbddd270b21a0acb753f3252b. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
+++

# Qualify plugin 0.2.4 with public evaluator 0.21.0

## Independence

Use SPEC-PLG-001, SPEC-IAR-016 and SPEC-RLO-006. Expected wheel identity comes
from the released v0.21.0 RLS and independent public download. Expected source
comes from the approved committed plugin manifests and assembly plan.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-002 | test, inspection | Existing builder/checker, inventories and both native host validators | Both 0.2.4 outputs contain identical shared assets and the exact public 0.21.0 wheel; no Python runtime or independent policy copy is added. |
| REQ-IAR-030 | demonstration, test | Disposable native profiles and resource acceptance | Exact installed package supports bootstrap, activation, startup, manual/automatic compaction, resume and independent selections under VER-IAR-021. Record actual host versions and complete entry identity. |
| REQ-RLO-018 | inspection | Delivery plan and public-handoff inputs | Qualified package identity, source, wheel, claimed hosts and expected old marketplace parent are explicit. Public routes remain pending under WO-RLS-033. |

## Procedure and evidence

Require the released evaluator wheel to be independently public before invoking
the existing marketplace build/check commands. Assemble from one committed source
and released governance revision. Recheck the entire generated tree and archives.
Use fresh disposable profiles, existing authorized authentication and cached
resources for offline checks. Preserve user credentials and real profile settings.
Apply VER-IAR-021's identity/recovery requirements to these exact package bytes.
Do not substitute helper output for native host events or CLI for desktop evidence.

Retain actual identities, commands, tree digests, native traces, failures and the
publication review under evidence/WO-RLS-032/. Prepare one commit-bound VREC for
this work and both declared contracts. Human verification precedes the marketplace
write. Recheck the remote parent immediately before ordinary descendant publication.

## Residual uncertainty

Local qualification proves no public install/update result. Missing required
desktop evidence stays pending. Public qualification and current claims are
assessed by VER-RLS-032 after the authorized marketplace action.
