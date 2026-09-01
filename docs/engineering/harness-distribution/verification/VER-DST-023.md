+++
id = "VER-DST-023"
type = "verification"
title = "Verify the designed self-contained Explorer"
status = "draft"
owners = ["quality-owner", "security-owner"]
created = "2026-09-01"
updated = "2026-09-01"

[relations]
verifies = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-033", "REQ-DST-035", "REQ-DST-037", "REQ-DST-038", "REQ-DST-039", "REQ-DST-040", "REQ-DST-041", "REQ-DST-042", "REQ-DST-043", "REQ-DST-044", "REQ-DST-045", "REQ-DST-046", "REQ-DST-047", "REQ-DST-067", "REQ-DST-068"]
+++

# Verification Contract: Verify the designed self-contained Explorer

## Independence

Expected behaviour is derived from the requirements, from `SPEC-DST-023`,
from the unchanged bundle contracts `SPEC-DST-013` and `SPEC-DST-014`, and
from the owner's recorded decisions. The design export is untrusted
implementation input: its rendering is checked against the bundle, never
against itself. Browser review runs on the bundle generated from this
repository, over HTTP, with the network trace recorded.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-029`, `REQ-DST-031` | snapshot and bundle tests | real repository generated twice; fixture with a future artifact type | snapshot keys unchanged, no `metrics` in the snapshot, identical bytes across generations, unknown types rendered by name |
| `REQ-DST-030` | browser review | Overview, Lineage, Virtual Twin, Readiness, record panel | coverage, findings, gate states, provenance, supersession, evidence, and experiments remain reachable and named as recorded |
| `REQ-DST-033` | package and template tests | canonical template, package data, `--check` | one managed template, reproduced from its sources, shipped by the package |
| `REQ-DST-035` | browser review | Overview | headline strip states coverage without a per-requirement table; missing coverage lists the exact requirements |
| `REQ-DST-037` | static and browser check | revision display in every view | seven-character display with the complete revision available |
| `REQ-DST-038` | browser check | text filter with a value | one control clears only the filter and the view refreshes |
| `REQ-DST-039` | static check of stage palette and legend | six stages, status treatments | every category has a distinct stable colour and a text label |
| `REQ-DST-040` | browser review | select a work order, a requirement, a release record | six-stage board, lit spine, exact ids, status, relation direction |
| `REQ-DST-041` | browser check | select three artifacts, use the Lineage back and forward controls and the visit chips | earlier and later boards are restored in order; visits are labelled navigation, never lineage |
| `REQ-DST-042`, `REQ-DST-047` | browser review of the record panel | `WO-ECP-024`, `RLS-SEH-021`, `REQ-LRE-003`, a rejected and a superseded artifact | identity strip, type gloss, status, owners, decision trail with delegated acts distinct, proof block, absent fields omitted |
| `REQ-DST-043`, `REQ-DST-046` | hostile-fixture and browser check | bodies and evidence containing script and hostile markup | inert rendering, no network request, evidence text in place with the text-less row named and sized |
| `REQ-DST-044` | browser check | a requirement with an EARS statement | clauses distinguished, exact statement preserved |
| `REQ-DST-045` | browser check | relation list of a record | each resolved reference opens Lineage on that artifact |
| `REQ-DST-067` | static, build, and browser checks | template invariants, CSP, network trace | one document, three scripts, no remote origin, same-origin manifest-declared requests only, contained failures |
| `REQ-DST-068` | fixture and real-repository tests | metrics fixture, distribution table, evaluator fields, remote normalization | exact expected metrics, sorted lead times, scalar-only distribution, identical across generations |

## Acceptance scenarios

- Build the template from sources and confirm `--check` passes and the
  committed bytes equal the build.
- Generate the repository bundle twice and compare every manifest-declared
  path and byte.
- Open `?view=overview`, `?view=lineage&artifact=WO-ECP-024`,
  `?view=graph&artifact=RLS-SEH-021`, `?view=readiness`, and
  `?view=readiness&subject=WO-ECP-024` in a headless browser with a virtual
  time budget; record the rendered text, the console, and the request list.
- Click a node in the Virtual Twin and confirm the record panel loads that
  artifact, then open it in Lineage.
- Select a rejected release record and a superseded requirement; confirm the
  refusal reads as a recorded decision with its reason.
- Serve a resource with altered bytes and confirm the requesting view fails
  visibly with a retry while the others render.

## Property and invariant tests

- Exactly one bootstrap marker; exactly three `<script` occurrences; the
  bootstrap element is the only JSON script.
- The template's URL-shaped literals are exactly the XML namespace
  identifiers and React's error pointer; `unpkg`, `googleapis`, `<link `,
  `<script src=`, `localStorage`, and `sessionStorage` are absent.
- The CSP text equals the value in `SPEC-DST-023` rule 7.
- `MAX_INDEX_BYTES` is 524,288 in the generator and the build; the rendered
  document is at or below it; summary, per-document, and total budgets are
  unchanged.
- Hostile repository text in the bootstrap is escaped as before.
- `build_explorer_metrics` is a pure function of the snapshot: equal inputs
  give equal outputs, empty input gives zeros and nulls.

## Static and architecture checks

- `ARCH-DST-008` as amended and `ADR-DST-013` own the self-contained
  presentation boundary; `ARCH-DST-010`/`ADR-DST-010` continue to own the
  bundle model unchanged.
- The bundle verifier's resource contract and the publication allowlist are
  unchanged.
- No new remote dependency, workflow, storage, cookie, or telemetry.

## Security and privacy checks

- Confirm repository text reaches the page only through React text nodes or
  the shell's escaping, never through the component evaluation path.
- Confirm the vendored React builds match the runtime's declared SRI digests
  and that the runtime's CDN fallbacks are unreachable and retired.
- Scan the document for remote origins, storage, WebSocket, EventSource,
  `javascript:` and `data:text/html`.

## Performance and resilience checks

- Measure the document, summary, topology, and per-document sizes before
  compression; record the Overview's request count (no per-artifact fan-out
  when `metrics` is present).
- Repeat generation and transactional failure tests of `VER-DST-013`.

## Manual assessments

Review each view at desktop and narrow width for legibility, keyboard
reachability, visible focus, and explicit non-authority language; confirm the
Readiness view's gate posture, subject listing, evidence filters, findings,
provenance, and controlled outcomes match the previous page's semantics.

## Evidence retention

`docs/engineering/harness-distribution/evidence/WO-DST-023-verification.md`
retains source identities, digests, sizes, commands, exit codes, test counts,
manifest digests, browser observations, request lists, deviations, and the
actions not performed.

## Residual uncertainty

Headless review covers rendering and requests, not interaction latency on a
low-end device. The `'unsafe-eval'` allowance is mitigated by structure, not
by policy; a future change that routed repository text into a component
source would defeat it, which is why the build tool and this contract check
the sources rather than the page alone.
