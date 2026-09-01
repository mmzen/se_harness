+++
id = "WO-DST-023"
type = "work_order"
title = "Integrate the designed self-contained Explorer as the canonical template"
status = "approved"
owners = ["engineering-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-09-01"
updated = "2026-09-01"

[assurance]
commit_bound_verification = "required"
rationale = "The change replaces the executable Explorer template, extends the generator's projection and budgets, and vendors third-party code that every generated dashboard and the public demonstration will execute; future release and publication decisions rely on its correctness and on the generator's determinism."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/harness_explorer/index.template.html",
  "templates/repository/standard/scripts/generate_harness_dashboard.py",
  "repository_tools/explorer_design/",
  "tests/test_dashboard_webui.py",
  "docs/engineering/harness-distribution/",
  "docs/notes/harness-dashboard-publication.md",
  "docs/images/",
  "README.md",
]

[relations]
implements = ["REQ-DST-067", "REQ-DST-068", "REQ-DST-055"]
specifications = ["SPEC-DST-023", "SPEC-DST-013", "SPEC-DST-014"]
architecture = ["ARCH-DST-008", "ADR-DST-013", "ADR-DST-008", "ARCH-DST-010", "ADR-DST-010"]
verification = ["VER-DST-023", "VER-DST-013", "VER-DST-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-01T20:51:14Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-01 by selecting the presented option 'Approve, start, complete on green (Recommended)', after reviewing the designed Explorer against the complete repository bundle in the local design loop and instructing its integration as the canonical template. The owner also accepted, by selecting 'Accept now, next design round fixes it (Recommended)', the recorded deviation that the Lineage view prefetches every artifact detail until a following design round loads details for the selected spine only."
+++

# Work Order: Integrate the designed self-contained Explorer as the canonical template

## Lifecycle

Drafted on 2026-09-01 after the repository owner reviewed the designed
Explorer against the complete repository bundle in the local design loop and
instructed: integrate it, it replaces the existing `index.template.html`.
Approval authorizes the bounded implementation below and nothing further.
Commit-bound verification is `required`: the work changes executable
presentation, the generator's projection, and vendored third-party code that
every generated dashboard and the public demonstration execute.

## Objective

Replace the canonical Explorer template with the designed self-contained
page, extend the candidate generator with the indicators and proof fields the
page presents, retire the runtime CDN, keep the G0-G5 Readiness view, and
leave every approved Explorer obligation either satisfied by the new page or
explicitly superseded, so that the 0.13.0 candidate ships the redesign and
this repository adopts it at its next root adoption.

## In scope

- Retain the design session's exported views verbatim under
  `repository_tools/explorer_design/sources/`, together with the component
  runtime, both React 18.3.1 production builds, and the design-system
  stylesheet, and add a deterministic, count-asserted build that produces
  the canonical template from them (`SPEC-DST-023` rules 1-6).
- Replace `templates/repository/standard/scripts/harness_explorer/index.template.html`
  with the built document: one bootstrap marker, three script elements, a
  Content Security Policy without any remote origin, the four designed
  views, the shell, and the Readiness view carried forward from the previous
  template.
- Extend `templates/repository/standard/scripts/generate_harness_dashboard.py`:
  raise `MAX_INDEX_BYTES` to 524,288; project `evaluator_evidence_path`,
  `evaluator_evidence_sha256`, and the scalar `[distribution]` table onto
  record details; carry `path`, and for release records `version`,
  `released_at`, and `distribution`, on compact topology rows; add the
  `metrics` object to the summary; add a normalized GitHub `source_url` to
  the repository descriptor.
- Rewrite the tests that pinned the previous canonical template and the
  candidate-equals-root generator parity; add tests for build
  reproducibility, the self-containment invariants, the metrics fixture, the
  distribution-table projection, and the remote normalization.
- After approval, supersede `REQ-DST-032` and `REQ-DST-036` by
  `REQ-DST-067` and the presentation contracts `SPEC-DST-008`,
  `SPEC-DST-010`, `SPEC-DST-011`, `SPEC-DST-012`, `SPEC-DST-016`,
  `SPEC-DST-017` by `SPEC-DST-023`; leave their verification contracts
  active, because verified records bind them (`E010`), so that the carried
  requirements are covered twice rather than not at all; amend
  `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-014`, `VER-DST-014`,
  `ARCH-DST-008`, and `ARCH-DST-009` by record; add the 2026-09-01
  reassessment to `ADR-DST-008`. The supersessions and the architecture
  relation changes wait for approval because the graph must stay valid for
  the approval transaction itself.
- Update the harness-distribution domain index, the dashboard publication
  note, and the README's Explorer section and screenshots so documentation
  describes the shipped page (`REQ-DST-060`).

## Out of scope

- Any change to the hash-locked root copies of the template and generator,
  the managed lock, or the released evaluator; the root adopts the redesign
  at the next release adoption.
- Any change to the bundle-v2 manifest contract, resource prefixes, the
  bundle verifier, the Pages publication workflow or its payload allowlist,
  `harness-dashboard-snapshot-v1`, validator rules, or lifecycle authority.
- A design round for the Readiness view; it is carried forward functionally
  and restyled with the design's tokens only.
- Building, releasing, publishing, or deploying anything; moving the public
  demonstration.

## Authorized decision envelope

The implementation agent may choose the build tool's module layout, the
patch-list wording, the shell's internal function names, the Readiness
view's markup, the test fixture values, and the screenshot viewport. It may
not change the designed views beyond the count-asserted patches that bind
them to the bundle contract, retire the CDN, route between views, and route
Overview indicators to the generator's metrics; may not embed artifact bodies
or evidence in the document; may not widen the Content Security Policy beyond
`'unsafe-inline'` and `'unsafe-eval'` on the page's own origin; may not
change any budget other than `MAX_INDEX_BYTES`; and may not alter a
requirement, specification, or record other than those enumerated above.

## Constraints

- Python 3.11+ standard library only in the generator and the build tool.
- Byte-deterministic template build and bundle generation; identical inputs
  produce identical bytes.
- Repository text stays inert: it reaches the page only as data rendered
  through text nodes or escaped interpolation, never through the component
  evaluation path.
- The vendored React builds must match the subresource-integrity digests the
  component runtime declares; the build refuses otherwise.
- The candidate template must build from its retained sources; a template
  edited by hand fails `--check`.

## Expected change surface

The canonical template and generator under `templates/repository/standard/`;
`repository_tools/explorer_design/` (build tool and sources); the dashboard
webui test module; the harness-distribution packet, supersessions, and
amendments listed above; the domain index; the publication note; the README
Explorer section and its three screenshots.

## Required verification

Execute `VER-DST-023` in full, plus the `VER-DST-013` and `VER-DST-014`
checks touched by the budget and history amendments: build reproducibility
(`--check`), the dashboard webui, publication, and harnessctl test modules,
the full Windows suite against its known baseline, twice-generated bundle
comparison, formal validation and start/review preflight under the released
evaluator, `git diff --check`, and a headless browser review of every view on
the real bundle with the console clean and the network trace limited to the
page's origin.

## Evidence to record

Retain under `docs/engineering/harness-distribution/evidence/WO-DST-023-verification.md`:
the design-export identity (file names and SHA-256 of every retained source),
the vendored React digests and their SRI match, the built template size and
SHA-256, exact commands and exit codes, test counts against the baseline,
twice-generated manifest digests, the headless review observations per view,
the CSP text, preflight results, deviations, and every action not performed.

## Stop and escalate conditions

Stop if a designed view needs a change outside the count-asserted patch list;
if the template exceeds 524,288 bytes; if a requirement other than
`REQ-DST-032` and `REQ-DST-036` turns out to be unsatisfied by the new page;
if the bundle verifier or the publication allowlist would need widening; or
if repository text could reach the component evaluation path.

## Completion report format

Report the template size and digest, the generator changes with their tests,
the supersession and amendment list, the compliance matrix outcome per
requirement, the browser review outcome per view, the retained evidence
path, and the explicit statement that root copies, lock, release, and
publication were not changed.
