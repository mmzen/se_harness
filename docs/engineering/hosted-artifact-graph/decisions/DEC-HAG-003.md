+++
id = "DEC-HAG-003"
type = "decision"
title = "Preserve the previous HAG handoff while binding the current snapshot"
status = "decided"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
kind = "question"
question = "Authorize the exact linked preservation amendment needed to rebind one live HAG handoff packet while preserving its original bytes?"
raised_by = "Codex"
recommendation = "bounded-manual-revision"
[[options]]
id = "bounded-manual-revision"
label = "Explicitly authorize the reviewed VER-HAG-004 linked revision and retain the old complete definition and handoff bytes."
[[options]]
id = "stop"
label = "Keep reconciliation pending without changing the accepted preservation definition or current packet."

[relations]
concerns = ["VER-HAG-004", "WO-HAG-006", "WO-HAG-005"]
blocks = ["WO-HAG-006"]

[disposition]
option = "bounded-manual-revision"
label = "Explicitly authorize the reviewed VER-HAG-004 linked revision and retain the old complete definition and handoff bytes."
decided_by = "mmzen"
decided_at = "2026-10-05T13:24:00Z"
reason = "Human mmzen answered \"I approve\" to SPEC-HAG-006, VER-HAG-005 and WO-HAG-006, required commit-bound verification, DEC-HAG-003 bounded-manual-revision of the exact VER-HAG-004 proposal, and ordinary draft PR #535 updates in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs. Review binding SHA-256 c9d4d84326b0e26d39519a1eadb91e216e4a6f01700213ec3c76a6854e55a649. This covers local implementation, checks, aggregate ready-record publication and later separately given verification-decision push. No verification acceptance, risk acceptance, retargeting, base-branch update, force push, merge, release or deployment. The exact manual amendment grants no general revision mechanism or gate waiver."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-05T13:24:00Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to SPEC-HAG-006, VER-HAG-005 and WO-HAG-006, required commit-bound verification, DEC-HAG-003 bounded-manual-revision of the exact VER-HAG-004 proposal, and ordinary draft PR #535 updates in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs. Review binding SHA-256 c9d4d84326b0e26d39519a1eadb91e216e4a6f01700213ec3c76a6854e55a649. This covers local implementation, checks, aggregate ready-record publication and later separately given verification-decision push. No verification acceptance, risk acceptance, retargeting, base-branch update, force push, merge, release or deployment. The exact manual amendment grants no general revision mechanism or gate waiver."
+++

# Preserve the previous HAG handoff while binding the current snapshot

## Facts

The revised definitions change WO-HAG-001's formal snapshot. Released check-pr
now refuses QGP-G4I-EVIDENCE and directs a supported evidence rebind. The current
VER-HAG-004 requires every earlier evidence blob to remain unchanged. Its
reviewed linked amendment permits only the one live packet to be rebound after
preserving its exact predecessor bytes. No other evidence exception is proposed.

## Exact proposed inputs

- Accepted VER-HAG-004 SHA-256: `a655e2a0ec03a31245a426ff9b38167825fcd6a34b92a405f0d47a714dcd8795`.
- Proposed replacement SHA-256: `574a4505a315a1eecc9f07f5c1c12ac04e6faca2f8a0843fbe193db73702c474`.
- Preserve the complete accepted version at `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-006/VER-HAG-004-accepted-before.txt`.
- Original handoff source commit: `64b4feb0cbaff06111876a1d4c0cc35a6c814415`.
- Original handoff SHA-256: `d109592865da42c88b176fe988492cb9643891aff29ac521d9434689ee7fcddf`.
- Preserve its complete bytes at `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-006/WO-HAG-001-handoff-before.txt`.

The complete replacement remains transient outside the repository until approved.
Applying it must leave lifecycle events unchanged and retain the actual human,
decision, date and both byte digests with the preserved version. No supported
generic amendment command is claimed. This is a proposed explicit human exception
for these exact bytes only; ordinary work approval does not silently grant it.

## Decision and effect

The accountable human may approve bounded-manual-revision or stop. Recording this
decision does not apply the amendment or rebind the packet. The supported released
evidence command must perform the later rebind; it does not run hosted tests.
No earlier VREC, candidate, acceptance, risk or release changes. All gates remain
required. The independent CI correction is governed by SPEC-HAG-006 and WO-HAG-006.
