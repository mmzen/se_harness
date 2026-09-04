+++
id = "REQ-xxx"
type = "requirement"
title = "<Observable obligation>"
status = "draft"
owners = ["<product/domain owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
# One obligation per requirement; split on "and SHALL". At most 30 words.
# Name the concrete component when one exists (THE VALIDATOR, THE INSTALLER);
# keep THE SYSTEM for an obligation that spans components. Pick one shape:
#   THE SYSTEM SHALL <response>.                          (always)
#   WHEN <event>, THE SYSTEM SHALL <response>.            (event)
#   WHILE <state>, THE SYSTEM SHALL <response>.           (state)
#   IF <unwanted condition>, THEN THE SYSTEM SHALL <response>.   (unwanted)
#   WHERE <feature is present>, THE SYSTEM SHALL <response>.     (optional feature)
statement = "WHEN <event>, THE SYSTEM SHALL <observable response>."
verification_method = ["test"]
priority = "must"
source = "<stakeholder, standard clause, incident, or artifact ID>"
measure = "<value and unit, for a quality requirement>"

[relations]
derives_from = ["CAP-xxx"]
+++

# Requirement: <title>

## In plain words

<One or two sentences a newcomer understands. A project term used here is
defined in this repository's own glossary, `docs/notes/glossary.md`, which
this repository writes.>

## Why

<At most five sentences. Why the obligation exists, not what it does. How
it is met belongs in the specification that specifies this requirement.>

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| <the observable condition or event; "always" for an invariant> | <what the reader can check> | <what happens when the response cannot be given> |

## Examples

### Normal

**Given** ...

**When** ...

**Then** ...

### Failure

**Given** ...

**When** ...

**Then** ...
