+++
id = "REQ-HUP-016"
type = "requirement"
title = "Adopt exact public 0.8.0 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
statement = "WHEN exact public se-harness 0.8.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.7.1 root, THE SYSTEM SHALL replace the managed root with 0.8.0's plan in one atomic transaction whose lock names 0.8.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "REL-SEH-019 post-release observation window; RLS-SEH-017 released and published on 2026-08-28; WO-HUP-007 precedent"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.8.0, evaluator.version 0.8.0, archive_sha256 equal to the wheel bound in RLS-SEH-017, payload digest of the installation; replay reads every file unchanged"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T17:04:46Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'Approve and start', for the adoption of exact public 0.8.0 (RLS-SEH-017, released and published 2026-08-28) as the standard root the simple way: one command from an isolated wheel-file install outside the checkout whose digest equals the record's bound wheel, no packet, candidate moved to 0.9.0 in the same change. Measured before this transition over branch state 5a2475f carrying unmoved main 2628627: validate PASS at 0 errors under both the governing 0.7.1 root and public 0.8.0; rehearsal on a throwaway export: plan 61 files, 9 update, 52 unchanged, no customization or conflict; 0.8.0 doctor 0 FAIL after apply; nine test modules pinned."
+++

# Requirement: Adopt exact public 0.8.0 as the standard root by the simple upgrade

## Statement

WHEN exact public `se-harness` 0.8.0 installed outside the checkout runs
`harnessctl upgrade --apply` on this 0.7.1 standard root, THE SYSTEM SHALL
replace the managed root with 0.8.0's reviewed plan in one atomic transaction
whose lock names 0.8.0 by version, installed-payload digest and the published
wheel's archive pair.

## Rationale

`RLS-SEH-017` released 0.8.0 on 2026-08-28 and `publish-pypi.yml` run
33191433505 published it: tag `v0.8.0` and `release/0.8` at candidate
`884b769`, PyPI wheel `e08aab8a…` and sdist `2d2c237e…` equal to the record's
bound digests. `REL-SEH-019`'s observation window names this adoption as the
release's acceptance in the wild, and it is what lets the retained stage
machine of issue #210 be deleted afterwards. `WO-HUP-007` established the
simple path from an index install with a `null` archive pair; that `null`
later blocked `prepare-release` (`MG004`) until a same-version refresh from a
wheel-file install wrote the pair (`REL-SEH-019` amendment). This adoption
therefore installs from the wheel file whose digest equals the published
one, so the lock carries the archive pair from the start.

## Acceptance

- The applying runtime is 0.8.0 installed outside the checkout from the wheel
  file downloaded from PyPI, whose SHA-256 is re-measured equal to
  `RLS-SEH-017`'s bound `e08aab8a96c156f9e5edf99b9a28aad96c7cffe5b18c262a2598a6b6873fadeb`,
  invoked in isolated mode.
- `upgrade .` lists the reviewed managed plan; `upgrade . --apply` succeeds
  without `--work-order` or any declaration; the lock's evaluator table reads
  `version 0.8.0`, the installed payload digest, `archive_name
  se_harness-0.8.0-py3-none-any.whl` and that archive digest; a second
  `upgrade .` reads every file unchanged.
