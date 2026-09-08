+++
id = "REQ-DST-073"
type = "requirement"
title = "Mark the managed gitignore block with comment markers"
status = "draft"
owners = ["product-owner", "technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE INSTALLER SHALL write the managed block of .gitignore between comment-line markers, as it already does for .gitattributes."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #380 (code health assessment 2026-09-07, section 4): installer._block at se_harness/installer.py lines 147 to 151 and the root .gitignore lines 10 and 15 at main a68caf70"
measure = "the installed .gitignore's markers begin with #; an upgrade rewrites HTML-comment markers to # markers with every byte outside the block unchanged"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Mark the managed gitignore block with comment markers

## In plain words

The installer marks its block in the ignore file with HTML comments, which
the ignore file treats as two patterns. Comment lines mark it instead.

## Why

In gitignore syntax a line is a pattern unless it starts with a hash. Every
installation therefore ignores two literal names that never exist, and a
reader of the file meets two lines that mean nothing there. The attributes
file already uses hash markers, and the block reader already accepts both
forms, so the change is the writer's alone.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the installer writes the ignore file | the block sits between `# se-harness:begin` and `# se-harness:end` | the block is between HTML comments |
| an upgrade meets a block between HTML comments | it rewrites the block with hash markers and keeps every byte outside it | owner lines move or the block is duplicated |

## Examples

### Normal

**Given** an empty directory,

**When** the installer initializes it,

**Then** the ignore file's managed block opens with a hash-marked line and
Git reports no pattern for the marker text.

### Failure

**Given** a repository initialized by released 0.16.0, whose block is between
HTML comments,

**When** the candidate's upgrade is applied,

**Then** the block carries hash markers, the owner lines are byte-identical,
and the health check passes; anything else fails the upgrade test.
