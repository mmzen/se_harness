+++
id = "REQ-AUT-006"
type = "requirement"
title = "Slim the requirement template and link acceptance examples to the acceptance directory"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN the standard harness installs the requirement template, THE SYSTEM SHALL provide a body of Rationale, Behavior (trigger, response, on failure), Assumptions and dependencies, Acceptance examples, and Open decisions, SHALL show the five statement shapes and the optional attributes, and SHALL point executable scenarios to acceptance/<REQ-ID>.feature for a verification contract to name."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "requirements-steward"
+++

# Requirement: Slim the requirement template and link acceptance examples to the acceptance directory

## Rationale

"Preconditions and trigger" restates the `WHEN` clause and "Required
response" restates the `SHALL` clause; they are the most-skipped sections.
"Constraints" invites design detail that belongs in the specification.
Acceptance examples exist in 152 requirements and are connected to nothing,
while the layout reserves `acceptance/` for Gherkin scenarios.

## Preconditions and trigger

Installation or upgrade of the standard template set; `create-artifact
--type requirement`.

## Required response

- Template body: `## Rationale`, `## Behavior` with sub-bullets trigger /
  response / on failure, `## Assumptions and dependencies`,
  `## Acceptance examples` (one normal, one failure, Given/When/Then),
  `## Open decisions`.
- A sentence pointing executable scenarios to `acceptance/<REQ-ID>.feature`
  and stating that the verification contract names them.
- Existing requirements keep their headings; no migration.

## Failure and boundary behavior

None beyond template rendering; `create-artifact` still requires the
template's `id`, `status`, `created`, and `updated` lines.

## Constraints

Six headings, not nine; the template stays under 2,500 bytes.

## Acceptance examples

### Example: normal behavior

**Given** a fresh installation

**When** the requirement template is read

**Then** it carries exactly the six headings and the five shapes.

### Example: failure behavior

**Given** a requirement body with the old nine headings

**When** validated

**Then** no diagnostic.

## Open decisions

None.
