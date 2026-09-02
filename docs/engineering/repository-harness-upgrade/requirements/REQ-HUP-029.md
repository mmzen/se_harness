+++
id = "REQ-HUP-029"
type = "requirement"
title = "Adopt exact public 0.14.0 as the standard root by the simple upgrade"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN exact public se-harness 0.14.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.13.0 root, THE SYSTEM SHALL replace the managed root with 0.14.0's plan in one atomic transaction whose lock names 0.14.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-023 released and published on 2026-09-02; WO-HUP-014 precedent; rehearsal of 2026-09-02 on a throwaway clone of main 25c0ef9"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.14.0, evaluator.version 0.14.0, archive_sha256 equal to the wheel bound in RLS-SEH-023, payload digest of the installation; replay reads every file unchanged; no file leaves the managed set (measured)"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T11:42:30Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC' for WO-HUP-015: the adoption of exact public 0.14.0 (RLS-SEH-023, released and published 2026-09-02) as the standard root the simple way, from the 0.13.0 lock 9dfec5b4, rehearsed the same day on a throwaway clone of main 25c0ef9."
+++

# Requirement: Adopt exact public 0.14.0 as the standard root by the simple upgrade

## Rationale

`RLS-SEH-023` released 0.14.0 on 2026-09-02, a package that differs from
0.13.0 only by its version markers, cut so that its integration commit
carried the 0.13.0 root and the release-bound public demonstration rendered
the designed Explorer. Adopting it keeps this repository governed by the
latest published evaluator, which is the standing practice after every
release; it carries no behavioural change. The rehearsal of 2026-09-02
showed three managed files update, nothing leaves the managed set, and the
replay is a no-op.

## Behavior

- Trigger: exact public 0.14.0, isolated outside the checkout, runs
  `harnessctl upgrade . --apply` on the 0.13.0 root.
- Response: one atomic transaction writes the reviewed plan and a lock
  naming 0.14.0 by version, installed-payload digest and the published
  wheel's archive pair; a second `upgrade .` reads every file unchanged.
- On failure: the guard refuses, or the transaction writes nothing.

## Assumptions and dependencies

The wheel file is downloaded from PyPI and its SHA-256 compared with the
distribution table of `RLS-SEH-023` before installation.

## Acceptance examples

### Example: normal behavior

**Given** exact public 0.14.0 in an isolated environment outside the
checkout, installed from the wheel file whose SHA-256 equals
`70d438b501d374fec06f41e25571f674b3cd1f43178389e6e06b0269c92f4856`,

**When** `harnessctl upgrade . --apply` runs on the 0.13.0 root,

**Then** the lock reads `tool_version 0.14.0`, `evaluator.version 0.14.0`,
`archive_sha256` equal to that digest, payload
`25034dc72a6be582ebef3c6b9a733c6ab9b6dcd879b9fda162d4d3e131a04306`, 46
managed files, and a second `upgrade .` reads 46 unchanged.

### Example: failure behavior

**Given** a plan that reports a `customized`, `conflict` or unexpected
`remove` action,

**When** the operator reviews it,

**Then** the work order stops for amendment and nothing is written.
