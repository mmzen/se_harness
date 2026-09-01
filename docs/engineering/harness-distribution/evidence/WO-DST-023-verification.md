# WO-DST-023 verification evidence

Retained under `VER-DST-023` for the integration of the designed
self-contained Explorer as the canonical template. Measurements were taken
on Windows 11 at candidate revision `c065e3d` (origin/main) with the
released 0.12.0 evaluator in `C:/Users/mathi/se-harness-eval-0120` and the
candidate generator under `templates/repository/standard/scripts/`.

## Authorization

- 2026-09-01: the repository owner reviewed the designed export
  (`C:\Users\mathi\Desktop\output2`) against the complete bundle in the
  local design loop and instructed: integrate it, it replaces the existing
  `index.template.html`.
- 2026-09-01: the owner approved `REQ-DST-067`, `REQ-DST-068`,
  `SPEC-DST-023`, `VER-DST-023`, `ADR-DST-013`, `WO-DST-023` by selecting
  the presented option `Approve, start, complete on green (Recommended)` and
  accepted the Lineage prefetch deviation by selecting `Accept now, next
  design round fixes it (Recommended)`.

## Design-export identity (retained sources, LF bytes)

| Source | SHA-256 | Bytes |
| --- | --- | --- |
| `Graph.dc.html` | `b24cf42962c08f87471fc3daf29e616baea420e5dd947ff52057b1b1b9db553f` | 24,168 |
| `Lineage View.dc.html` | `80d17b50ec5d599d9cddf1d7d6754e282a5bb222ab51ae24eb1966320fe9417e` | 70,155 |
| `Overview.dc.html` | `60292f343313fac3b07feb5267a2f6cad09f5531a0bd27f43a454ff3f6b737ea` | 25,406 |
| `Record.dc.html` | `c192503d8bbdae46f17e3761b0dfd36f552be12977eb0afad4d2cd31394a773a` | 31,748 |
| `support.js` (component runtime) | `8fe7df74405f3c55f49b7249c74ea1397e65d07dea2b1bd3b4a489bec2e28cbe` | 69,150 |
| `styles.css` (design system) | `cf9fcf75ac84dfe7517177eb14acf5a20ca4410c55691ab9879c6af7b2168400` | 10,555 |
| `vendor/react.production.min.js` | `d949f1c3687aedadcedac85261865f29b17cd273997e7f6b2bfc53b2f9d4c4dd` | 10,751 |
| `vendor/react-dom.production.min.js` | `35f4f974f4b2bcd44da73963347f8952e341f83909e4498227d4e26b98f66f0d` | 131,835 |
| `shell/shell.html` | `9186a12e41ea38b4c0eae09c53b1d1ea40fd59f5795f9b76aa7d20e3ebe7a993` | 2,197 |
| `shell/explorer.js` | `7f4a6bb14a517a2df35fbe275c90a4af4ee6f4de8c61d3be40c52e398b83503f` | 30,170 |
| `shell/readiness.css` | `41c0eabcd983ab30a5ae4585baaabe3b38721ffe01e0d7017bf90f7a02a5d406` | 7,143 |

The vendored React builds were downloaded from the origins the runtime
names and match the subresource-integrity digests it declares:
`REACT_SRI = sha384-DGyLxAyjq0f9SPpVevD6IgztCFlnMF6oW/XQGmfe+IsZ8TqEiDrcHkMLKI6fiB/Z`,
`REACT_DOM_SRI = sha384-gTGxhz21lVGYNMcdJOyq01Edg0jhn/c22nsx0kyqP0TxaV5WVdsSH1fSDUf5YJj1`.
The build refuses a mismatch.

## Built template

- `templates/repository/standard/scripts/harness_explorer/index.template.html`:
  431,123 bytes, SHA-256
  `c21503567c7e15c5ca15f74ff36aeee78b96b503e3eb31fdb49601e18417ffe0`.
- `python -m repository_tools.explorer_design.build_explorer_template --check`:
  exit 0, "matches its sources".
- Invariants: one `__HARNESS_BOOTSTRAP_JSON__` marker; three `<script`
  elements; CSP
  `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'; img-src data:; connect-src 'self'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'`;
  URL-shaped literals limited to the five W3C namespace identifiers and
  React's error-decoder pointer; no `unpkg`, `googleapis`, `<link `,
  `<script src=`, `localStorage`, `sessionStorage`, `@import`.

## Generator

- `MAX_INDEX_BYTES` 262,144 -> 524,288; `metrics` object in the summary;
  `evaluator_evidence_path`/`evaluator_evidence_sha256` on verification and
  release records; scalar `distribution` on release records; compact
  topology rows carry `path` and, for release records, `version`,
  `released_at`, `distribution`; `repository.source_url` normalized to
  `https://github.com/mmzen/se_harness`.
- Real-repository metrics at `c065e3d` (before the packet was added):
  839 lifecycle events, 0 unattributed, 2 delegated transitions, 1
  delegated record (`WO-ECP-024`, `VREC-ECP-028`), 108 lead times (median
  0.62 h), 161/161 released work orders verified, latest release
  `RLS-SEH-021` 0.12.0 at `3dcde4b`, release arc `REL-SEH-023` -> release
  0.77 h. Nine of sixteen release records carry a distribution table.

## Bundle

- Final generation (packet approved, supersessions applied): PASS, 1,230
  artifacts, 4,573 relations, 0 errors; manifest
  `883420995ba658f6db0a028d6ac691000ea390dcb20ba1bdcebd55a35eaa4c32`;
  `index.html` 431,388 bytes; summary 5,209 bytes; topology 1,351,963
  bytes (target 2,097,152); 1,453 resources.
- Determinism: two generations into separate directories produced the
  identical manifest digest and byte-identical `index.html`; only
  `generation-summary.json` differed in its timing field, as documented.

## Tests

- `tests.test_dashboard_webui` + `tests.test_dashboard_publication` +
  `tests.test_harnessctl`: 79 tests, OK (2 skipped).
- Full suite `python scripts/run_tests.py` on the final tree: 1,176 tests,
  1 error, 26 skipped; the error is the known Windows baseline
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`.
  An earlier run also failed `test_public_onboarding...test_root_is_a_bounded_human_entry_point`
  (README at 201 lines); the README was trimmed to 199 lines and the test
  passes.
- Rewritten pins: the previous 3D/CDN template assertions, the
  candidate-equals-root generator equality, `new Option(v,v)`, and the
  two-script count. New tests: template invariants, build reproducibility,
  `_distribution_table`, `GITHUB_REMOTE`, `build_explorer_metrics` fixture,
  real-repository proof fields.

## Browser review (headless Edge, virtual time budget 40 s, HTTP on 127.0.0.1)

| View | Result |
| --- | --- |
| `?view=overview` | 312/312 coverage, 0 unresolved of 4,547 relations, gate reading with rule/gate versions, v0.12.0 currency with `3dcde4b` and wheel `639edbee`, 839 events / 0 unattributed, 2 transitions + 1 record with `VREC-ECP-028` and `WO-ECP-024` linked, 21 rejected / 11 superseded listed, 163 verified / 161/161, median lead time with n=108; no per-artifact request; console clean |
| `?view=lineage&artifact=WO-ECP-024` | six-stage board, spine lit, decision trail with the delegated acts and check-run references, `handoff` evidence rows, GitHub source link at `c065e3d`; console clean |
| `?view=graph&artifact=RLS-SEH-021` | constellation rendered on canvas, rail with commit `3dcde4b`, `VREC-SEH-021`, wheel `639edbee`, `Open in Lineage`; console clean |
| `?view=readiness` and `&subject=WO-ECP-024` | 215 subjects, G0-G5 rollups, subject view with gates, evidence rows, findings, provenance; console clean |

Network log (`--log-net-log`) for the Lineage release view: 1,235 same-origin
requests (manifest, summary, topology, artifact details) and no page request
to any other origin; the only non-local entries were Edge's own telemetry
endpoints. Screenshots at 1536x900 @2x replaced
`docs/images/harness-explorer-{overview,lineage,readiness}.png`.

## Recorded deviation

The designed Lineage view fetches every artifact detail when it opens
(1,224 requests, about 7 MB) against `SPEC-DST-014` rule 7. Accepted by the
owner for this integration and recorded in `SPEC-DST-023`; a following
design round loads details for the selected spine only (brief prepared).

## Governance

- Validation under the released evaluator after approval and supersessions:
  0 errors, 65 warnings, 0 advisories.
- `preflight --phase review`: PASS. `check --checkpoint handoff --from-git origin/main`:
  completed, decision required `DR-WO-COMPLETE`.
- Superseded: `REQ-DST-032`, `REQ-DST-036` (by `REQ-DST-067`);
  `SPEC-DST-008`, `SPEC-DST-010`, `SPEC-DST-011`, `SPEC-DST-012`,
  `SPEC-DST-016`, `SPEC-DST-017` (by `SPEC-DST-023`). Verification
  contracts `VER-DST-008/010/011/012/016/017` stay active because verified
  records bind them (`E010`). Amended by record: `SPEC-DST-013`,
  `VER-DST-013`, `SPEC-DST-014`, `VER-DST-014`, `ARCH-DST-008`,
  `ARCH-DST-009`; `ADR-DST-008` carries the 2026-09-01 reassessment.
- `git diff --check`: clean.

## Not performed

No change to root managed copies, the lock, the released evaluator, the
bundle verifier, the Pages workflow or its allowlist. No build, release,
publication, or deployment. The pull request is opened for the owner's
merge; commit-bound verification (`VREC`) follows separately.
