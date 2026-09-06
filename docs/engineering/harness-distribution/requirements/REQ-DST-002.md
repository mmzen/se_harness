+++
id = "REQ-DST-002"
type = "requirement"
title = "Initialize and adopt without destructive replacement"
status = "implemented"
owners = ["engineering-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN init or adopt is requested, THE SYSTEM SHALL plan all changes before writing, stop on ordinary-file conflicts, and integrate bounded managed blocks into existing agent and ignore files."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

Initialization accepts an absent or empty target. Adoption accepts an existing repository. Both reject unsafe paths and symlinked destinations and avoid partial writes when conflicts are known.


## Amendment record

**The statement's trigger is amended, proposed 2026-09-06 under `WO-ECP-026` (`SPEC-ECP-020` `ECP-INS-002`, `ECP-INS-003`).** Where the statement and the body read `init` or `adopt`, one command, `init`, is requested; its behaviour on an absent or empty target is the former initialization and on a target with content the former adoption. The obligation (plan before writing, stop on conflicts, integrate bounded blocks) is unchanged.
