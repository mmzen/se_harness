+++
id = "ADR-DST-013"
type = "adr"
title = "Ship the designed Explorer as one self-contained document without a runtime CDN"
status = "draft"
owners = ["technical-owner", "security-owner", "product-owner"]
created = "2026-09-01"
updated = "2026-09-01"

[relations]
decides = ["ARCH-DST-008"]
+++

# ADR: Ship the designed Explorer as one self-contained document without a runtime CDN

## Status

Proposed.

## Context

`ADR-DST-008` kept `harness-dashboard-snapshot-v1` as the only persisted
Explorer boundary and, at the owner's explicit 2026-08-13 instruction,
preserved the original reviewed page with its `3d-force-graph` renderer
fetched from `unpkg.com` at runtime. That ADR records the accepted CDN risk
and names its reconsideration triggers: a security-sensitive or offline
deployment, a dependency-version change, or a renderer that needs no
dependency.

On 2026-09-01 the repository owner instructed the integration of a designed
replacement for the page. The design was produced in a separate design
session against briefs grounded in the real bundle, iterated in a local loop
against the complete repository, and reviewed by the owner. It renders the
topology on a hand-rolled canvas, needs no third-party renderer, and exposes
the value of the harness (coverage, attributed decisions, refusals, lead
time, proof) that the previous page did not. It runs on a small component
runtime that depends on React 18.3.1.

Two constraints frame the integration. The bundle verifier and the Pages
publication allowlist admit only JSON and text resources under fixed
prefixes, so scripts cannot ship as bundle resources without widening two
contracts and the public-payload policy. The generator caps `index.html` at
262,144 bytes, while the designed views, the runtime, and React together
exceed that.

## Decision drivers

- Remove the runtime CDN and its accepted supply-chain risk rather than
  renew it.
- Keep the bundle model, manifest verification, and the publication
  allowlist unchanged.
- Keep the designed views reviewable as the design session exported them,
  so a later design round is a diff, not a rewrite.
- Keep every approved Explorer obligation either satisfied or explicitly
  superseded; in particular keep the G0-G5 readiness observations.
- Preserve byte-deterministic generation and the light-bootstrap principle
  that no artifact body or evidence is embedded in the document.

## Considered options

1. Ship the runtime, React, and the view components as bundle resources
   under a new content-hashed prefix and load them from the shell. Rejected:
   it widens the bundle verifier, `SPEC-DST-013`'s manifest contract, and
   the repository's Pages allowlist for executable content, and it adds a
   `script-src 'self'` surface to the publication boundary.
2. Rewrite the designed views as plain scripts without the component runtime
   or React. Rejected: it discards the reviewed design as an artifact,
   makes every later design round a manual port, and would ship an
   unreviewed reimplementation under the design's name.
3. Inline the runtime, both React UMD builds, the design-system stylesheet,
   and the view components into one self-contained `index.html`, raise the
   shell budget from 256 KiB to 512 KiB, and drop every remote origin from
   the Content Security Policy. Selected.
4. Keep the previous page and add the designed views beside it. Rejected:
   two presentations of one model, double the pinned tests, and the CDN
   stays.

## Decision

Adopt option 3.

- The canonical template is built deterministically from retained sources
  under `repository_tools/explorer_design/`: the exported views verbatim,
  the component runtime, both React production builds verified against the
  subresource-integrity digests the runtime itself declares, the
  design-system stylesheet with its remote font import removed, and a shell
  that owns bootstrap reading, manifest-verified resource access, routing,
  in-memory preferences, and the Readiness view carried forward from the
  previous template. An explicit, count-asserted patch list binds the views
  to the bundle contract; any drift in a future export fails the build
  rather than silently shipping.
- The shell budget becomes 524,288 UTF-8 bytes. Summary, per-document, and
  total-content budgets are unchanged. No artifact body or evidence is
  embedded.
- The Content Security Policy names no remote origin:
  `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'
  'unsafe-eval'; img-src data:; connect-src 'self'; font-src 'none';
  base-uri 'none'; form-action 'none'; object-src 'none'`.
- The component runtime compiles each view's logic block with the `Function`
  constructor, which requires `'unsafe-eval'`. The only sources that reach
  that path are the template's own embedded component texts; repository
  text enters the page exclusively as data rendered through React text nodes
  and escaped interpolation. This exchanges remote executable code from a
  CDN for same-document evaluation of reviewed sources.
- `harness-dashboard-snapshot-v1` remains the only persisted boundary. The
  summary gains a derived `metrics` object and record details gain the
  proof fields their front matter already carries (`REQ-DST-068`); both are
  projections of the snapshot, not a second model.
- The exact `3d-force-graph` exception of `ADR-DST-008` is withdrawn. Its
  snapshot-boundary decision stands.

## Consequences

Positive: the page is offline-complete, the public demonstration makes no
third-party request, the supply-chain and observation risks of the CDN
disappear, the design remains a reviewable artifact, and future design
rounds integrate through one build.

Negative: the initial document grows from about 151 KB to about 431 KB
(roughly 100 KB compressed on Pages); the CSP gains `'unsafe-eval'`; the
page depends on React and a component runtime vendored into the repository
whose upgrades are governed changes; the designed Lineage board renders the
whole working set, which is large for this repository.

Operational: the root `scripts/harness_explorer/index.template.html` and the
root generator stay hash-locked to the released evaluator until the next
adoption; tests that pin the root copy keep passing until then, and the
adoption work order replaces them.

Security: repository content never reaches the evaluation path; the build
refuses any source or shell that names a remote origin other than the inert
XML namespace identifiers and React's error-message pointer; the runtime's
own CDN fallbacks are retired at build time.

Migration: consumer repositories receive the template through the ordinary
managed upgrade at the next release; customized templates are not
overwritten; historical generated dashboards are unchanged.

## Validation

`VER-DST-023` checks build reproducibility from sources, the single
bootstrap marker, exactly three script elements, the CSP text, the absence
of every remote origin, the 512 KiB budget, hostile-input escaping, the
generator's proof fields and metrics against fixtures and the real
repository, twice-generated byte identity, and a browser review of every
view on the real bundle with the network trace limited to same-origin
manifest-declared paths.
