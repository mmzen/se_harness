+++
id = "REQ-DST-067"
type = "requirement"
title = "Render the designed Explorer from one self-contained document"
status = "approved"
owners = ["product-owner", "technical-owner", "security-owner"]
created = "2026-09-01"
updated = "2026-09-01"
statement = "WHEN Harness Explorer is opened from generated output, THE SYSTEM SHALL render the designed Overview, Lineage, Virtual Twin, Readiness, and record views from one self-contained HTML document that requests only same-origin, manifest-declared resources and names no remote location."
verification_method = "automated-test-and-browser-review"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-01T20:51:14Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-01 by selecting the presented option 'Approve, start, complete on green (Recommended)', after reviewing the designed Explorer against the complete repository bundle in the local design loop and instructing its integration as the canonical template. The owner also accepted, by selecting 'Accept now, next design round fixes it (Recommended)', the recorded deviation that the Lineage view prefetches every artifact detail until a following design round loads details for the selected spine only."
+++

# Requirement: Render the designed Explorer from one self-contained document

## Rationale

The Explorer is the surface through which a visitor judges whether a
repository's governance is real. The current page answers that question
poorly: its home page is counts and a decorative three-dimensional graph, its
Lineage view is a two-hop neighbourhood browser that cannot tell the story of
one change, and its only third-party dependency is a script fetched at runtime
from a public CDN under an accepted supply-chain risk (`ADR-DST-008`).

On 2026-09-01 the repository owner reviewed the designed replacement against
the complete 1,224-artifact bundle and instructed its integration as the
canonical template. The designed views answer the questions the product
exists for: whether the repository can be trusted now (coverage, closure, the
evaluator's own reading, release currency), whether governance is real
(attributed decisions, delegation under the gate, refusals on the record,
commit-bound proof), what is moving (lead time, work in flight), how one change
came to be (a stage pipeline and the decision trail of every record), and where
an artifact sits in the whole (the domain constellation). The redesign also
removes the CDN: every byte the page executes ships in the document.

The owner selected integration of the designed views as the canonical
template on 2026-09-01; the Readiness view is carried forward from the
previous template so no approved obligation lapses.

This requirement supersedes `REQ-DST-032`, whose obligation to load the pinned
3D renderer is withdrawn, and `REQ-DST-036`, whose zero-, one-, and two-hop
filter context is replaced by the designed lens and spine interactions.

## Behavior

- Trigger: a generated Explorer bundle is served over its supported static
  HTTP boundary and opened in a browser.
- Response: one document renders the five designed views and routes between
  them; every data request targets a same-origin path declared in the
  verified manifest; the document names no remote origin and declares a
  Content Security Policy without any remote source; the Readiness view keeps
  the G0-G5 gate observations, findings, provenance, and controlled outcomes
  the previous page presented.
- On failure: a missing, redirected, mismatched, or malformed resource leaves
  a visible, contained failure in the requesting view; the shell never
  substitutes data, widens its network boundary, or infers a decision.

## Assumptions and dependencies

- The integrity-addressed progressive bundle of `SPEC-DST-013` and the
  verified progressive access of `SPEC-DST-014` remain the data boundary.
- The designed views are retained as reviewable sources and rebuilt into the
  template by a deterministic build (`SPEC-DST-023`).
- Web Crypto and a same-origin static HTTP host are available, as today.

## Acceptance examples

### Example: the designed page on the real bundle

**Given** the SE Harness repository bundle generated at one revision,

**When** `index.html?view=overview` is opened over HTTP,

**Then** the headline strip shows the requirement-coverage, graph-integrity,
gate-reading, and release-currency figures computed from that bundle, and the
browser issues no request outside the page's origin.

### Example: a blocked or hostile host

**Given** a resource whose bytes differ from the manifest digest,

**When** a view requests it,

**Then** that view shows a contained failure with a retry, every other view
stays usable, and no remote fallback is attempted.

## Open decisions

None.
