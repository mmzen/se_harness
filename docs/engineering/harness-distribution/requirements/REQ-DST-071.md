+++
id = "REQ-DST-071"
type = "requirement"
title = "Declare no configuration key that nothing reads"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHEN THE INSTALLER writes or upgrades a standard installation, THE INSTALLER SHALL declare no configuration key that changes no harness behaviour."
verification_method = ["test", "inspection"]
priority = "must"
source = "Repository owner instruction on 2026-09-07 to remove all unused configuration items; complexity audit 2026-08 item P2-10"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T18:41:35Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-07 by selecting the presented option 'Approve and start immediately', after the owner instructed that all unused configuration items be removed and DEC-DST-001 was disposed as remove-marker. Seven of the twelve keys in the installed configuration have no reader anywhere in the evaluator; the packet removes them from the standard template, pins the installed key set with its reader inventory, and amends the two definitions whose prose names a removed key."
+++

# Requirement: Declare no configuration key that nothing reads

## In plain words

The installed configuration offers seven settings that nothing in the tool
reads, and they are removed. Five keys remain, each with a reader, and an
upgrade takes the seven out of existing installations.

## Why

A hash-locked file is a promise. An owner who sets `require_clean_worktree` to
false expects a rule to relax, and nothing relaxes. The integrity check then
defends those misleading bytes on every run. Seven of the twelve keys shipped
in the founding template and never gained a reader.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A standard installation is written | The file declares five keys, each read by a named part of the harness | An installer defect |
| An upgrade reaches an installation holding the removed keys | The unmodified file is rewritten without them, and the project name and installation date survive | An edited file blocks the upgrade as customized |
| A target still carries a removed key | It loads as before, because an unknown key was never an error | A new refusal would break installations |

## Examples

### Normal

**Given** an empty directory and the released package installed outside it,

**When** the operator initializes the directory,

**Then** the configuration holds two tables and five keys, and validation and
the dashboard succeed.

### Failure

**Given** an installation whose owner added a configuration line,

**When** the operator applies an upgrade,

**Then** the plan reports the path as customized, the transaction refuses, and
file and lock are unchanged.
