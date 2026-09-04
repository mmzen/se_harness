+++
id = "REQ-DST-069"
type = "requirement"
title = "Explain governed delegation through a concise public README"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN a reader opens the public README, THE SYSTEM SHALL explain governed agent delegation, the Virtual Twin vision, and a usable released-package starting path within 650 source words."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Repository owner review and publication request on 2026-09-04"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T20:43:53Z"
decided_by = "product-owner"
reason = "Record the repository owner approval of the complete reviewed README and explicit publication request on 2026-09-04."
+++

# Requirement: Explain governed delegation through a concise public README

## Rationale

The owner reviewed the complete replacement README, its branding, screenshots,
wording, and typography, then requested publication. The existing front page
requires too much reading before explaining what the harness is and why to use it.

## Required response

Explain the open source harness, bounded agent authority, independent verification,
human decisions, and the connected engineering chain. Distinguish current operation
from the vision in which the Virtual Twin drives code. Keep installation usable and
make deeper documentation discoverable. SPEC-DST-024 defines this presentation.

## Acceptance examples

**Given** a newcomer, **when** they read the opening and starting path, **then** they
can identify the product, the authority retained by humans, and how to initialize
or adopt a repository using the released package.

**Given** a proposed revision that presents automatic graph-to-code propagation as
already delivered, **when** its claims are reviewed, **then** it fails acceptance.

## Open decisions

None.
