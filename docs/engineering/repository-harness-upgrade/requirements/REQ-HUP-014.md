+++
id = "REQ-HUP-014"
type = "requirement"
title = "Adopt exact public 0.7.1 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN exact public se-harness 0.7.1 installed outside the checkout runs harnessctl upgrade --apply on this 0.6.0 standard root, THE SYSTEM SHALL replace the managed root with 0.7.1's reviewed plan in one atomic transaction whose lock names 0.7.1 by version and payload digest, with no packet."
verification_method = "automated-test"
priority = "must"
source = "REL-SEH-018 post-release observation window; owner direction of 2026-08-27 that the install process be simple"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.7.1, evaluator.version 0.7.1, archive pair null for an index install; replay reads every file unchanged"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T17:43:24Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', for the adoption of exact public 0.7.1 as the standard root the simple way (REQ-REB-027, REQ-REB-028 shipped by RLS-SEH-016): one command from an isolated index install outside the checkout, no packet, candidate moved to 0.8.0 with its scenario in the same change. Successor to the rejected WO-HUP-006. Measured before this transition over branch state 12e9e36 carrying unmoved main 23d5781: validate PASS at 986 artifacts, 0 errors under both the governing 0.6.0 root and public 0.7.1; doctor 0 FAIL; upgrade plan 61 files, 43 add or update, 18 unchanged."
+++

# Requirement: Adopt exact public 0.7.1 as the standard root by the simple upgrade

## Statement

WHEN exact public `se-harness` 0.7.1 installed outside the checkout runs
`harnessctl upgrade --apply` on this 0.6.0 standard root, THE SYSTEM SHALL
replace the managed root with 0.7.1's reviewed plan in one atomic transaction
whose lock names 0.7.1 by version and payload digest, with no packet.

## Rationale

`WO-REB-027` made the upgrade simple (`REQ-REB-027`, `REQ-REB-028`); 0.7.1
ships it (`RLS-SEH-016`). The rejected `WO-HUP-006` showed that the previous
packet-bound path could not be completed from an index install. This
requirement is that adoption, done the simple way, and it is the release's
acceptance test named in `REL-SEH-018`.

## Acceptance

- The applying runtime is 0.7.1 installed outside the checkout from the index
  (`pip install "se-harness==0.7.1"`), invoked in isolated mode.
- `upgrade .` lists the reviewed managed plan; `upgrade . --apply` succeeds
  without `--work-order` or any declaration; the lock's evaluator table reads
  `version 0.7.1`, the installed payload digest, and `null` for the archive
  pair; a second `upgrade .` reads every file unchanged.
