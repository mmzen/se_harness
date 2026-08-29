+++
id = "REQ-HUP-022"
type = "requirement"
title = "Adopt exact public 0.11.0 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN exact public se-harness 0.11.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.10.0 root, THE SYSTEM SHALL replace the managed root with 0.11.0's plan in one atomic transaction whose lock names 0.11.0 by version, payload digest and the published wheel's archive pair, and the files the 0.10.0 lock managed that 0.11.0 no longer ships SHALL leave the tree in the same work order."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-020 released and published on 2026-08-29; REL-SEH-022 observation window; WO-HUP-010 precedent; rehearsal of 2026-08-29 on a throwaway clone of main 896f8fa; issue #271"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.11.0, evaluator.version 0.11.0, archive_sha256 equal to the wheel bound in RLS-SEH-020, payload digest of the installation; replay reads every file unchanged; the 15 retired skill files absent from the tree"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T16:44:31Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-29 by the accountable owner, 'Approve and start WO-HUP-011', for the adoption of exact public 0.11.0 (RLS-SEH-020, released and published 2026-08-29) as the standard root the simple way, from the 0.10.0 lock aeb73cc7, with the explicit removal of the fifteen retired skill files the installer leaves behind (issue #271) and no verification-records directory in the work order's scope."
+++

# Requirement: Adopt exact public 0.11.0 as the standard root by the simple upgrade

## Rationale

`RLS-SEH-020` released 0.11.0 on 2026-08-29 and the publication observed
it installed from PyPI (PI001 to PI005). Its observation window
(`REL-SEH-022`) is this repository's own adoption: the `scope` and
`handoff` checkpoints that admit a work order's own records by
construction, the `harness-orient` core on `check`, and the root validator
without the `[agentic_delegation]` rule reach this repository only through
its root. The rehearsal of 2026-08-29 showed the simple upgrade works as it
did for 0.10.0 — and one thing it does not do: the installer plans from the
new managed set only, so the three skills 0.11.0 retired stay on disk,
unmanaged and invisible to `doctor` (issue #271). This adoption removes them
explicitly and says so.

## Acceptance examples

**Given** exact public 0.11.0 in an isolated environment outside the
checkout, installed from the wheel file whose SHA-256 equals
`ba26ab7be14321cdc26b69d59e2b894d544c3e7b529227de1f24ad9cd8f935c0`,
**when** `harnessctl upgrade . --apply` runs on the 0.10.0 root, **then**
the lock reads `tool_version 0.11.0`, `evaluator.version 0.11.0`,
`archive_sha256` equal to that digest, a payload digest of the installation,
46 managed files, and a second `upgrade .` reads 46 unchanged.

**Given** the moved root, **when** the tree is listed, **then**
`.agents/skills/` holds exactly `harness-operator-brief` and
`harness-orient` and `.claude/skills/` exactly `harness-orient`.
