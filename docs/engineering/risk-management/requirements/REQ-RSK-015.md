+++
id = "REQ-RSK-015"
type = "requirement"
title = "Recording a risk never widens a work order's authorized scope"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHILE a work order is in progress, THE SCOPE CHECK SHALL admit a new risk file of the work order's domain as an authorized changed path."
verification_method = ["test"]
priority = "must"
source = "PR #156 REQ-RSK-006, retired with its branch; SPEC-ECP rules behind QGP-G4I-PATHS, which otherwise reads a new file outside the declared paths as a scope failure"
measure = "the scope and handoff checks pass with one added risk file that no declared path admits; a second changed file outside scope still fails"

[relations]
derives_from = ["CAP-RSK-010"]
+++

# Requirement: Recording a risk never widens a work order's authorized scope

## In plain words

Someone who notices a threat mid-execution can write it down without breaking
the scope check. Only the risk file is admitted, and nothing else.

## Why

A threat is most often seen while the work is being done, by the person doing
it. If writing it down fails the scope check, it will not be written down. The
admission is narrow on purpose: one new file, in the domain's risk directory, and
never an existing file.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| an in-progress work order adds one risk file in its domain | the scope check admits the path | none |
| the change also touches a path outside scope | that path still fails the scope check | the checkpoint reports the offending path |
| the change edits an existing risk file | the edit is not admitted by this rule | the path fails unless a declared path admits it |

## Examples

### Normal

**Given** an in-progress work order whose paths do not include the risk
directory,

**When** its change set adds one risk file in that domain,

**Then** the scope checkpoint passes.

### Failure

**Given** the same change set with one unrelated source file added,

**When** the scope checkpoint runs,

**Then** it fails and names the unrelated file only.
