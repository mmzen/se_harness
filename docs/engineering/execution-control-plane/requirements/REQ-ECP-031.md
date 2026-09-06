+++
id = "REQ-ECP-031"
type = "requirement"
title = "One command installs the harness into any target"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN an operator requests installation of the harness into a target, THE INSTALLER SHALL offer one command, init, whose behaviour follows the target's content."
verification_method = ["test", "inspection"]
priority = "should"
source = "functional assessment of 2026-08-30 (section 4.1, adopt being init plus a report; the table Simplify, combine, clarify, remove: combine adopt into init); the owner's request of 2026-09-05 to merge init and adopt as a single command"
measure = "harnessctl --help lists init and no adopt; init on an absent or empty target plans the same files as the previous init; init on a target with content plans the same files as the previous adopt, including docs/engineering/ADOPTION_REPORT.md; harnessctl adopt exits 2 with argparse's usage error"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: One command installs the harness into any target

## In plain words

Two commands install the harness today, and they are the same operation
underneath. After this change there is one command, `init`, which reads the
folder and does the right thing.

## Why

The functional assessment of 2026-08-30 found that the adopt command is
the init command plus a report. Both names run the same installer; the only
differences are a refusal of non-empty folders and an inventory report. The
tool can see whether the folder is empty, so the operator should not have
to say so.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| init on an absent or empty target | the complete standard harness, as today; no adoption report | a conflicting file refuses every write, as today |
| init on a target with content | existing files kept, managed fragments integrated, the adoption report written, as adopt does today | a conflicting file refuses every write, exit 1, as today |
| the adopt command | refused by the parser as an unknown command, exit 2 | none; the replacement is documented, not printed |

## Examples

### Normal

**Given** a Rust project with its own agent instructions and no harness,

**When** init runs on it,

**Then** the exit status is 0, the owner's instructions stay above the
managed fragment, the lock is written, and the adoption report names Rust.

### Failure

**Given** the same project,

**When** the adopt command runs on it,

**Then** the exit status is 2, standard output is empty and standard error
carries the parser's usage error.
