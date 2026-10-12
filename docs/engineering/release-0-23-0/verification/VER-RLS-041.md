+++
id = "VER-RLS-041"
type = "verification"
title = "Confirm all public 0.23.0 delivery surfaces"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020", "REQ-RLO-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 ea87d111791b983d6347c6ea5c864b81200f8ff38fdb7fa83ba6dbac8a27b661."
+++

# Confirm all public 0.23.0 delivery surfaces

## Independence

Use the frozen approved plan and bound RLS/package identities as expected values.
Independently read public state after authorized delivery. A command exit alone
does not prove that users can obtain the intended payload.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-RLO-019 | GitHub/PyPI downloads, clean evaluator install, both CLI marketplace fresh/update routes, documentation and Pages readback | Public identities match the frozen plan. Update begins at actual public plugin 0.2.6. Tagged sandbox source and guide match the declared private-source delivery. |
| REQ-RLO-020 | Existing five-surface completion check and retained observations | Every required surface passes; absent, failed or deferred results remain explicit and prevent complete delivery. |
| REQ-RLO-023 | Publisher/resolver results, recovery observations and ref readbacks | Only approved bytes are published, marketplace advances as an ordinary descendant, and release/0.23, v0.23.0, latest and last match the exact plan. |

## Procedure and retention

After the exact complete-release grant, run the existing trusted-main resolver
and publisher. Confirm the public wheel equals the qualified bundle before
marketplace promotion. Inspect uncertain effects before retrying. Use temporary
profiles for fresh/update tests; do not update the user's actual host profiles.

Keep version tags and payloads immutable. Verify demonstration provenance at
https://mmzen.github.io/se_harness/. No public service, authenticated graph
authority or production-readiness claim is part of this delivery.

Retain actual commands, observations, identities and failures under
evidence/WO-RLS-047/. The frozen plan names permitted receipt paths before its
approval. Prepare separate commit-bound verification of public observations and
status documentation; it is not a prerequisite of its own public delivery.
