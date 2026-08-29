+++
id = "REQ-HUP-020"
type = "requirement"
title = "Adopt exact public 0.10.0 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN exact public se-harness 0.10.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.9.0 root, THE SYSTEM SHALL replace the managed root with 0.10.0's plan in one atomic transaction whose lock names 0.10.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-019 released and published on 2026-08-29; REL-SEH-021 observation window; WO-HUP-009 precedent; rehearsal of 2026-08-29 on a throwaway clone of main 47f67de"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.10.0, evaluator.version 0.10.0, archive_sha256 equal to the wheel bound in RLS-SEH-019, payload digest of the installation; replay reads every file unchanged"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T10:40:48Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'Approve and start WO-HUP-010', for the adoption of exact public 0.10.0 (RLS-SEH-019, released and published 2026-08-29) as the standard root the simple way: one command from an isolated wheel-file install outside the checkout whose digest equals the record's bound wheel, no packet, candidate moved to 0.11.0 in the same change. Measured before this transition over branch state d2e210c carrying unmoved main 47f67de: validate PASS at 0 errors under the governing 0.9.0 root and under public 0.10.0; rehearsal on a throwaway clone: plan 61 files, 6 update, 55 unchanged, no customization or conflict; 0.10.0 doctor 0 FAIL and released-root 143/143 after apply; the full suite on the moved root differs from the same-commit control by three tests, all resolved by owner content, the candidate version and one test literal."
+++

# Requirement: Adopt exact public 0.10.0 as the standard root by the simple upgrade

## Statement

WHEN exact public `se-harness` 0.10.0 installed outside the checkout runs
`harnessctl upgrade --apply` on this 0.9.0 standard root, THE SYSTEM SHALL
replace the managed root with 0.10.0's reviewed plan in one atomic
transaction whose lock names 0.10.0 by version, installed-payload digest and
the published wheel's archive pair.

## Rationale

`RLS-SEH-019` released 0.10.0 on 2026-08-29 from candidate `69ee77a`,
binding wheel `e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3`;
PyPI serves that wheel with the same digest. `REL-SEH-021`'s observation
window names this adoption as the release's acceptance in the wild: it is
what puts the state-independent pull-request gate (`WO-ECP-013`) on this
repository's own lanes, lets its Windows checkout run `evidence` and
`check` from the released evaluator (`WO-ECP-012`), and binds evidence
packets on any checkout (`WO-ECP-014`). `WO-HUP-009` established the path
this adoption repeats verbatim.

## Acceptance

- The applying runtime is 0.10.0 installed outside the checkout from the
  wheel file downloaded from PyPI, whose SHA-256 is re-measured equal to
  `RLS-SEH-019`'s bound `e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3`,
  invoked in isolated mode.
- `upgrade .` lists the reviewed managed plan; `upgrade . --apply` succeeds
  without `--work-order` or any declaration; the lock's evaluator table reads
  `version 0.10.0`, the installed payload digest, `archive_name
  se_harness-0.10.0-py3-none-any.whl` and that archive digest; a second
  `upgrade .` reads every file unchanged.
