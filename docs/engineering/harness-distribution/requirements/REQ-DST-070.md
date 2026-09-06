+++
id = "REQ-DST-070"
type = "requirement"
title = "Install no evaluator script into a governed repository"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN THE INSTALLER writes or upgrades a standard installation, THE INSTALLER SHALL write no evaluator script into the target repository."
verification_method = ["test", "inspection"]
priority = "must"
source = "Repository owner decision on 2026-09-06 to remove the duplicated evaluator content from scripts/; complexity audit items #223 and #225"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T14:49:42Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 by selecting the presented option 'Approve all four, do not start (Recommended)', after the packet was drafted at the owner's instruction to remove the evaluator content duplicated under scripts/ in two packets. This decision approves the artifact only; implementation of WO-DST-024 is not started by it."
+++

# Requirement: Install no evaluator script into a governed repository

## In plain words

The programs the evaluator runs to judge a repository stay inside the
installed package. The tool stops copying them into the repositories it
governs.

## Why

Every governed repository carries hash-locked copies of the evaluator's
validator, Explorer generator and inspector. The governing lane never runs
them; the evaluator uses its installed copies. Readers and agents mistake the
copies for the engine. A governed repository should hold what the tool wrote
for it, not the tool.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A new standard installation is written | No file is created under the scripts directory; the lock records none | An installer defect |
| An upgrade reaches an installation holding the eight retired files | Unchanged copies and their lock entries are removed by the existing leaving-set rule | An edited copy blocks the upgrade as customized; nothing is written |
| The evaluator validates, inspects or renders a target | It runs the scripts inside its own package | A missing script is reported before the target is read |

## Examples

### Normal

**Given** an empty directory and the released package in a virtual
environment outside it,

**When** the operator initializes the directory,

**Then** it receives contracts, instructions, workflow and skills, its lock
lists no scripts path, and validation succeeds.

### Failure

**Given** an earlier installation whose owner edited the Explorer generator
copy,

**When** the operator applies an upgrade,

**Then** the plan reports the path as customized, the transaction refuses,
and repository and lock are unchanged.
