+++
id = "REQ-HUP-027"
type = "requirement"
title = "Adopt exact public 0.13.0 as the standard root by the simple upgrade"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN exact public se-harness 0.13.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.12.0 root, THE SYSTEM SHALL replace the managed root with 0.13.0's plan in one atomic transaction whose lock names 0.13.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-022 released and published on 2026-09-02; REL-SEH-024 observation window; WO-HUP-013 precedent; rehearsal of 2026-09-02 on a throwaway clone of main 09aa69f"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.13.0, evaluator.version 0.13.0, archive_sha256 equal to the wheel bound in RLS-SEH-022, payload digest of the installation; replay reads every file unchanged; no file leaves the managed set (measured)"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Adopt exact public 0.13.0 as the standard root by the simple upgrade

## Rationale

`RLS-SEH-022` released 0.13.0 on 2026-09-02 and the publication observed it
served from PyPI with the record's digests. Its observation window
(`REL-SEH-024`) is this repository's own adoption: the designed
self-contained Explorer reaches this repository's generated dashboard, and
the public demonstration, only through its root. The rehearsal of
2026-09-02 showed the simple upgrade works as it did for 0.12.0: five
managed files update, nothing leaves the managed set, and the replay is a
no-op.

## Behavior

- Trigger: exact public 0.13.0, isolated outside the checkout, runs
  `harnessctl upgrade . --apply` on the 0.12.0 root.
- Response: one atomic transaction writes the reviewed plan and a lock
  naming 0.13.0 by version, installed-payload digest and the published
  wheel's archive pair; a second `upgrade .` reads every file unchanged.
- On failure: the guard refuses, or the transaction writes nothing.

## Assumptions and dependencies

The wheel file is downloaded from PyPI and its SHA-256 compared with the
distribution table of `RLS-SEH-022` before installation; the installer's
managed set is the one 0.13.0 declares.

## Acceptance examples

### Example: normal behavior

**Given** exact public 0.13.0 in an isolated environment outside the
checkout, installed from the wheel file whose SHA-256 equals
`1bbf3b747b7ebbb07fd3fd975e87e3c11049e7a6a8e1377e3d35099f4fe862ae`,

**When** `harnessctl upgrade . --apply` runs on the 0.12.0 root,

**Then** the lock reads `tool_version 0.13.0`, `evaluator.version 0.13.0`,
`archive_sha256` equal to that digest, payload
`9b4cdb5f2148683f3ceaad868e64b1b4ebefbadcac49cf4cd1feccd954540bfe`, 46
managed files, and a second `upgrade .` reads 46 unchanged.

### Example: failure behavior

**Given** a plan that reports a `customized`, `conflict` or unexpected
`remove` action,

**When** the operator reviews it,

**Then** the work order stops for amendment and nothing is written.
