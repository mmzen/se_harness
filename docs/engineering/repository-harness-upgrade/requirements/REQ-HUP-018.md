+++
id = "REQ-HUP-018"
type = "requirement"
title = "Adopt exact public 0.9.0 as the standard root by the simple upgrade"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN exact public se-harness 0.9.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.8.0 root, THE SYSTEM SHALL replace the managed root with 0.9.0's plan in one atomic transaction whose lock names 0.9.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-018 released and published on 2026-08-28; WO-HUP-008 precedent; rehearsal of 2026-08-29 on a throwaway clone of main 7291602"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.9.0, evaluator.version 0.9.0, archive_sha256 equal to the wheel bound in RLS-SEH-018, payload digest of the installation; replay reads every file unchanged"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Adopt exact public 0.9.0 as the standard root by the simple upgrade

## Statement

WHEN exact public `se-harness` 0.9.0 installed outside the checkout runs
`harnessctl upgrade --apply` on this 0.8.0 standard root, THE SYSTEM SHALL
replace the managed root with 0.9.0's reviewed plan in one atomic transaction
whose lock names 0.9.0 by version, installed-payload digest and the published
wheel's archive pair.

## Rationale

`RLS-SEH-018` released 0.9.0 on 2026-08-28 from candidate `8adfe1b`, binding
wheel `c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364`
and sdist `da80ef01…`; PyPI serves that wheel with the same digest. This
repository's root still runs exact public 0.8.0 (`WO-HUP-008`), so the
managed workflow it installs lacks the unconditional pull-request scope gate
that `WO-ECP-003` shipped in 0.9.0. `WO-HUP-008` established the path this
adoption repeats verbatim: one `upgrade --apply` from a wheel-file install
outside the checkout whose digest equals the record's bound wheel, so the
lock carries the archive pair from the start and `prepare-release` never
meets `MG004`.

## Acceptance

- The applying runtime is 0.9.0 installed outside the checkout from the wheel
  file downloaded from PyPI, whose SHA-256 is re-measured equal to
  `RLS-SEH-018`'s bound `c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364`,
  invoked in isolated mode.
- `upgrade .` lists the reviewed managed plan; `upgrade . --apply` succeeds
  without `--work-order` or any declaration; the lock's evaluator table reads
  `version 0.9.0`, the installed payload digest, `archive_name
  se_harness-0.9.0-py3-none-any.whl` and that archive digest; a second
  `upgrade .` reads every file unchanged.
