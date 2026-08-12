+++
id = "REQ-DST-024"
type = "requirement"
title = "Concise human-facing root README"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a human reader opens the repository root README, THE SYSTEM SHALL present the essential SE Harness value, safe starting path, authority boundary, current limitations, and deeper-documentation routes in no more than 200 physical lines."
verification_method = "automated-test-and-reader-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Concise human-facing root README

## Rationale

The current 523-line README combines public onboarding, an agent operating manual, governance reference, release procedure, installed-file inventory, and contributor instructions. This makes the most important human information difficult to identify and duplicates material now available in progressive notes and managed policy.

## Preconditions and trigger

A human repository owner, evaluator, adopter, or contributor opens `README.md` from GitHub, PyPI, or a source checkout.

## Required response

The README gives the reader a clear reason to use SE Harness, a safe route to install or adopt it, the small human-operable inspection surface, the human/agent authority model, known material limitations, and obvious links for details.

The 200-line ceiling is a maintainability guard, not permission to omit required safety boundaries. Details exceeding that information budget move to linked notes or remain in authoritative engineering policy.

## Failure and boundary behavior

The README must not become a second managed workflow or command manual. Concision must not hide that automation cannot approve, verify, release, publish, or deploy.

## Constraints

- Preserve `Target expertise: 6/10`.
- Keep GitHub and PyPI Markdown compatibility.
- Keep the public installation source, package version example, project links, and renderer-independent meaning.
- Count physical UTF-8 text lines deterministically in focused tests.

## Acceptance examples

### Example: first-time evaluator

**Given** a reader has not inspected source code,

**When** they scan the README,

**Then** they can explain the harness value, the first repository action, who retains authority, and where to learn more.

### Example: detail is needed

**Given** a reader needs command flags, provenance timing, or self-hosting detail,

**When** they follow the relevant README link,

**Then** the detail is available in an expertise-labeled note or authoritative policy rather than duplicated in the root page.

## Open decisions

Exact prose and section lengths within the 200-line ceiling remain delegated to implementation under `SPEC-DST-007`.
