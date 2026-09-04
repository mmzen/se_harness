+++
id = "REQ-TCM-013"
type = "requirement"
title = "What derives from a capability is read from the graph"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN a capability is shown, THE EXPLORER SHALL show its ability, its plain words and the requirements that derive from it, read from the graph and not from a list in the body."
verification_method = ["test"]
priority = "must"
source = "docs/notes/assessment-capability-readability-2026-09-04.md: 30 capabilities list 79 requirement ids while 139 deriving requirements are unlisted and 8 lists match the graph; the owner's decision of 2026-09-04"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: What derives from a capability is read from the graph

## In plain words

Every requirement already records the capability it derives from, and the
validator checks it. The list at the end of a capability only repeats that
fact, and in 22 of 30 files it no longer matches. The list leaves the
template, and the Explorer shows the real list from the graph, beneath the
capability's ability sentence.

## Why

A section that can only repeat or contradict the graph is a second source
of truth, the same situation the `Open decisions` section was in. The
checklist asked for the list, the packets wrote it once, and nothing kept it
current. The graph is authoritative and already validated; showing it
where the reader looks removes the drift without asking anyone to maintain
a list.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A capability is created from the managed template | The template has no `Candidate requirements` or `Derived requirements` section | Not applicable |
| A capability record is opened in the Explorer | The ability appears first, the plain words beneath it, then the requirements that name the capability in `derives_from`, each linked, before the lifecycle events | A capability without an ability shows its title; a capability with no deriving requirement shows none |
| A capability draft still carries a legacy requirement list | The validator reports it as an advisory; the list is otherwise left alone | Validation still passes |

## Examples

### Normal

**Given** a capability with three requirements naming it in `derives_from`,

**When** its record is opened in the Explorer,

**Then** the three requirements are listed under the ability, and no list
in the body is needed to find them.

### Failure

**Given** a legacy capability whose body lists two requirement ids while
five derive from it,

**When** the Explorer shows it,

**Then** the five are listed from the graph, and the body's two stay as
retained prose.

## Open decisions

None.
