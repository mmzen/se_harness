+++
id = "ADR-IAR-012"
type = "adr"
title = "Use the released wheel as the shared resource carrier"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
decides = ["ARCH-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 171e579f177c1bbd46f8c091d7c6ff63158a57299c78cfe7ffa7001a3957b842."
+++

# Use the released wheel as the shared resource carrier

## Status

Proposed for human review. Drafting records a concrete design choice, not approval.

## Context and drivers

The accepted proposal moves shared instructions and templates out of repositories.
Agents, headless CLI and CI still need the same pinned release. Existing wheels
already ship these assets and have payload-integrity checks.
The confirmed workflow installs the plugin once per host, then asks agents to
clone, carry out new or resumed work, and prepare authorized push/PR delivery.
Cycles repeat within a session or run in parallel. A clone can be below the host
session directory, so cwd discovery alone does not identify the active checkout.

## Considered options

| Option | Consequence |
| --- | --- |
| Copy all policy and templates into each host plugin | Simple initial move, but duplicates resources and leaves headless CI and older repository pins needing another distribution path. |
| Publish a separate resource archive | Independent content versioning, but adds release coordination and a resolver for a second distributable. No current need justifies this. |
| Use the released wheel and let plugins resolve it | Reuses existing identity and release machinery, supports CI directly and isolates repository release pins. Requires setup to retain side-by-side environments. |

## Proposed decision

Use the released wheel as the sole resource carrier. The plugin installs or
locates that wheel in external private storage and delivers its instructions.
Keep host adapter versions separate from the repository's governing release.
Do not bundle a second independently editable policy edition in the plugin.

## Session selection

Keep the existing cwd discovery route for sessions started in a checkout. Add a
short shared bootstrap and one activation helper for a checkout selected later.
Store that selection in a small local record keyed by host and session. The agent
uses the path from its actual clone or existing-work selection; the human need
not repeat it. Restore and validate it at compaction and resume. Exact command
names and record encoding remain bounded implementation choices.

A cwd-only solution is smaller but does not satisfy the confirmed clone-after-
startup workflow. Scanning child directories cannot select reliably when several
checkouts exist. A global last-used path would mix parallel sessions. The chosen
local record adds persistence and atomic update handling without adding policy
copies, repository files, a registry service or a new host-wide setting.

The bootstrap is adapter guidance for locating released instructions. Lifecycle
policy and templates still come exclusively from the selected released wheel.

## Consequences

The plugin gives the user access to the full instruction material while the
checkout holds only selection and project records. CI uses the same resources.
Cached installs work offline; a new release needs explicit setup. Older supported
layouts require a compatibility path. Release availability and integrity checks
remain prerequisites; no newest-version fallback is permitted.
The session record must be validated as a locator and kept separate from formal
authority. Setup must protect environments used by concurrent sessions. Native
qualification must cover the actual host identity and private-data route; a
synthetic event containing a convenient identity is insufficient evidence.

## Validation

Verify packaged-resource parity, cloning after startup, immediate activation,
session recovery, simultaneous repository pins, plugin update without adoption,
native startup/compaction and plugin-free CI. The separate
applicability decision controls the boundary with accepted historical contracts.
