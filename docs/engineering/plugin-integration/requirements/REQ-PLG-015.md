+++
id = "REQ-PLG-015"
type = "requirement"
title = "Connect and maintain a project with existing tools"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "WHEN the owner requests project connection or maintenance, THE PLUGIN SHALL use the existing setup and released installer operations with a compatible checker while preserving the explicitly selected repository version."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner-directed KISS amendment, 2026-09-14; existing PR #416 identifier"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:05:14Z"
decided_by = "requirements-steward"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."
+++

# Connect and maintain a project with existing tools

## In plain words

Help the user connect a new or existing project and repair its checker without a
second installation system. A plugin update does not silently upgrade the project.

## Acceptance

The instructions name the target, selected wheel/checker and requested operation.
They cover initialization, switching an existing project to plugin skills, repair
and an explicitly requested upgrade through commands supported by that checker.
Setup reuses the one private environment. After any failure, report the actual
error and a useful retry; do not require a replacement environment or repair receipt.
A missing prerequisite stops only the operation needing it. Development acceptance
uses a disposable project and is clearly distinguished from a live migration.
