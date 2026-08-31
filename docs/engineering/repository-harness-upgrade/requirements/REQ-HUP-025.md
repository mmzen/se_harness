+++
id = "REQ-HUP-025"
type = "requirement"
title = "Adopt exact public 0.12.0 as the standard root by the simple upgrade"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"
statement = "WHEN exact public se-harness 0.12.0 installed outside the checkout runs harnessctl upgrade --apply on this 0.11.0 root, THE SYSTEM SHALL replace the managed root with 0.12.0's plan in one atomic transaction whose lock names 0.12.0 by version, payload digest and the published wheel's archive pair."
verification_method = ["test"]
priority = "must"
source = "RLS-SEH-021 released and published on 2026-08-31; REL-SEH-023 observation window; WO-HUP-011 precedent; rehearsal of 2026-08-31 on a throwaway clone of main 63889f7; issue #284"
measure = "one command from the isolated environment; lock schema 3, tool_version 0.12.0, evaluator.version 0.12.0, archive_sha256 equal to the wheel bound in RLS-SEH-021, payload digest of the installation; replay reads every file unchanged; no file leaves the managed set (measured), and a leaving file would be removed by the installer's own remove action (WO-DST-022)"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Adopt exact public 0.12.0 as the standard root by the simple upgrade

## Rationale

`RLS-SEH-021` released 0.12.0 on 2026-08-31 and the publication observed it
installed from PyPI. Its observation window (`REL-SEH-023`) is this
repository's own adoption: the advisory class in the gate's own count, the
managed lane reading the live pull-request body, the self-binding handoff
check, the evaluator-evidence and lock-schema floors, and the delegation
class reach this repository only through its root. The rehearsal of
2026-08-31 showed the simple upgrade works as it did for 0.11.0 — and this
time nothing leaves the managed set, and the installer's own `remove`
action (`WO-DST-022`, the fix for issue #271) would handle it if it did.

## Acceptance examples

**Given** exact public 0.12.0 in an isolated environment outside the
checkout, installed from the wheel file whose SHA-256 equals
`639edbeed4bdca7c9e21a5eb2afc3b9fc993ddb3f66177eec962f1646a545811`,
**when** `harnessctl upgrade . --apply` runs on the 0.11.0 root, **then**
the lock reads `tool_version 0.12.0`, `evaluator.version 0.12.0`,
`archive_sha256` equal to that digest, a payload digest of the
installation, 46 managed files, and a second `upgrade .` reads 46
unchanged.
