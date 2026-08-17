+++
id = "REQ-DST-048"
type = "requirement"
title = "Open Explorer through a lightweight bootstrap"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a generated Harness Explorer is opened over its supported static HTTP boundary, THE SYSTEM SHALL present its application shell and bounded repository summary without embedding artifact bodies or retained-evidence content in the HTML document."
verification_method = "automated-test-and-browser-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Open Explorer through a lightweight bootstrap

## Rationale

The current generated `index.html` is approximately 2.68 MB because it embeds the complete repository snapshot. The reusable UI template is only about 103 KB. A reader should see repository identity, validation state, aggregate metrics, and navigation promptly without first downloading and parsing every artifact and evidence body.

## Preconditions and trigger

This applies to every newly generated dashboard bundle served from GitHub Pages or another supported static HTTP origin. Historical generated pages remain historical outputs.

## Required response

- Keep executable UI structure, local styles, local scripts, and a small integrity bootstrap in `index.html`.
- Load a bounded repository summary as data rather than embedding the complete snapshot.
- Exclude artifact-body Markdown and retained-evidence bodies from both the HTML and initial summary.
- Render explicit loading, unavailable, and integrity-failure states without implying repository invalidity or assurance failure.

## Failure and boundary behavior

If bootstrap or summary data cannot be verified and loaded, the shell remains usable enough to identify the failed resource and observed revision when known. It must not display stale, partial, or invented repository facts as current.

## Constraints

- The browser must not read the source repository at runtime.
- No API, database, application server, telemetry, or new runtime network origin is introduced.
- Opening the generated HTML directly through `file://` is not a supported progressive-data transport.

## Acceptance examples

### Example: normal opening

**Given** a valid generated bundle is served from a static HTTP origin,

**When** a reader opens `index.html`,

**Then** the shell and repository summary become readable before topology, artifact bodies, or evidence content are requested.

### Example: missing summary

**Given** the declared summary resource is missing,

**When** Explorer starts,

**Then** it reports a bounded summary-loading failure and does not treat absent data as a valid empty repository.

## Open decisions

None when approved.
