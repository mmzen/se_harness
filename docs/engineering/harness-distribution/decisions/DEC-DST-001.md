+++
id = "DEC-DST-001"
type = "decision"
title = "The fate of the configuration schema marker"
status = "decided"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
kind = "question"
question = "When the inert keys leave the installed configuration, does its schema marker go with them, advance to 3, or stay at 2?"
raised_by = "engineering-owner"
recommendation = "remove-marker"

[[options]]
id = "remove-marker"
label = "Remove `schema_version`, because nothing reads it and the lock already carries a schema and a tool version that the installer does read."

[[options]]
id = "advance-to-3"
label = "Keep the key and write 3, so that the number identifies the new shape of the file even though no code compares it."

[[options]]
id = "keep-at-2"
label = "Keep the key at 2 and change nothing else, accepting that two different key sets are both called schema 2."

[relations]
concerns = ["REQ-DST-071", "SPEC-DST-026"]
blocks = ["SPEC-DST-026"]

[disposition]
option = "remove-marker"
label = "Remove `schema_version`, because nothing reads it and the lock already carries a schema and a tool version that the installer does read."
decided_by = "technical-owner"
decided_at = "2026-09-07T18:41:17Z"
reason = "Disposed by the accountable repository owner on 2026-09-07 by selecting the presented option 'Remove it (Recommended)', after the owner's instruction to remove all unused configuration items. Nothing reads schema_version; the lock's schema and tool_version, which the installer does read on every upgrade, remain the only generation marker. SPEC-REV-001's compatibility sentence is amended by record and the installer test assertion is retired under WO-DST-025."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-07T18:41:17Z"
decided_by = "technical-owner"
reason = "Disposed by the accountable repository owner on 2026-09-07 by selecting the presented option 'Remove it (Recommended)', after the owner's instruction to remove all unused configuration items. Nothing reads schema_version; the lock's schema and tool_version, which the installer does read on every upgrade, remain the only generation marker. SPEC-REV-001's compatibility sentence is amended by record and the installer test assertion is retired under WO-DST-025."
+++

# Decision: The fate of the configuration schema marker

## Question

`.engineering-harness.toml` declares `schema_version = 2`. No code path reads
it. The complexity audit of 2026-08 recorded it as item P2-10, with the
finding that the lock is authoritative. `SPEC-REV-001` promises in its
compatibility paragraph that the configuration schema becomes 2 for a newly
installed or safely upgraded file, and one installer test asserts the line is
present. Two verified records quote the value as the state of this repository
at the time they were written; they are never rewritten.

Removing seven keys changes the shape of a published, hash-locked file. The
marker's fate decides whether the file keeps a number that no longer
identifies anything.

## Options

**remove-marker.** The configuration declares only what the harness reads, so
the requirement needs no exception. The lock keeps `schema` and `tool_version`,
and the installer already reads the lock on every upgrade, so a future
migration still has a handle. Costs: the compatibility sentence of
`SPEC-REV-001` is amended by record, and one test assertion is retired. It
forecloses using the configuration itself as a migration signal.

**advance-to-3.** The number moves with the shape, which is what a version
marker is for, and a future reader can tell a five-key file from a twelve-key
one without counting. Costs: the same amendment to `SPEC-REV-001`, one test
assertion changed rather than retired, and a key that the requirement must
name as a deliberate exception because nothing reads it.

**keep-at-2.** Nothing else to do. The cost is a false statement: two
different files both call themselves schema 2, and the next reader who trusts
the number is misled. It forecloses nothing, and it leaves the defect the
instruction was meant to close.

## Recommendation

`remove-marker`. The owner's instruction was to remove the configuration items
nothing uses, and this is one of them; the audit reached the same finding
independently. The lock, not the configuration, is where the harness already
records the generation of an installation, so nothing is lost by deleting a
second marker that no code consults.

## Disposition

Written by `harnessctl decide`; do not edit by hand.
