# Verification evidence for WO-DST-017

## Authority and boundary

This local evidence records the implementation and checks authorized when the repository owner supplied the replacement Explorer template, confirmed that removal of the literal five-question strip was intentional, approved revision of the formal specification and verification contract, and instructed `ok go implement` on 2026-08-18. It supports an `implemented` work-order state only. After this evidence was first reported, the owner separately authorized the exact candidate commit, preparation of a ready verification record, branch push, and pull-request creation. This evidence is not itself commit-bound verification and does not approve a VREC transition, merge, release, publication, deployment, or governor promotion.

Work occurred only in the fresh clone at `C:/Users/mathi/.codex/visualizations/2026/08/18/01a01358-1d5a-7801-b15e-8b99a665cf02/se_harness-dashboard-integration`, on branch `codex/WO-DST-017-dashboard-template` from remote `main` commit `cbdb46f9d7077c8812e77663391aae0e3eab4a1f`. The occupied checkout at `C:/Users/mathi/RustroverProjects/se_harness` was not used or modified.

## Source intake, final bytes, and deviation

- The supplied `C:/Users/mathi/Downloads/index.template.html` had raw SHA-256 `5b52939838a9c91d04689814ba8523e8fca627111704dde9e4da31faf02a8368` at intake.
- The supplied content was normalized to repository line endings and integrated into both managed template copies. Browser review exposed one presentation defect in that input: the four-column State Lens was retained after the lens moved into a narrow side panel, causing label overlap at 1440 x 900.
- The only source-to-final deviation is the scoped local CSS rule `[data-od-id=graph-lens-summary] .lens{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:16px}`. It changes no data, script, URL, authority, or browser-state behavior and has a focused regression assertion.
- Final active and canonical template bytes are equal at SHA-256 `bc1af59acb409fd6960bbc6ca3cf1585d70d419a7a92933602304c8e6163b1d3`.
- The schema-2 lock was changed only through `harnessctl upgrade`; its template digest is the same `bc1af59acb409fd6960bbc6ca3cf1585d70d419a7a92933602304c8e6163b1d3`. Final lock-file SHA-256 is `f612267fa2ffec5a9c1b8ae2bbec3e698a803dd1555524e5b92ab654c9799377`.
- The literal five-question strip and all five question phrases are absent. Overview, Lineage, Readiness, artifact detail, Relations, Evidence, findings, provenance, and controlled outcomes remain represented by their existing routes and hooks.
- The final static presentation includes `DERIVED · READ-ONLY`, the statement that no approval, verification, or release decision is inferred, `Explorer gate groupings`, `NAVIGATION LABELS · NOT POLICY`, and the statement that managed `QUALITY_GATES.md` owns gate meaning and grants no authority.

## Preserved browser, security, and data contracts

- The two inline script bodies are byte-equivalent to pre-change `main`; their combined comparison SHA-256 is `65ed0d6e45882880238b4a32cd007523c83728a9a77807cbb126a250c8eb411c`.
- The CSP is unchanged: `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline' https://unpkg.com; img-src data:; connect-src 'self'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'`.
- The external URL set is unchanged and retains only the CSP source plus exact runtime asset `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js`.
- Progressive schema constants are unchanged: bundle, bootstrap, summary, topology, readiness, artifact, and snapshot schemas remain at their prior versions. The final template contains exactly one `__HARNESS_BOOTSTRAP_JSON__` marker.
- No generator, CLI, Python module, dependency, workflow, governor descriptor, architecture, ADR, package metadata, telemetry, storage, cookie, form, or hosted-service change was made.
- The unchanged focused suite retains hostile closing-script/markup/Unicode input, bounded graph and Lineage, verified-resource integrity, retry, stale-request containment, CSP, DOM-hook, URL, provenance, semantic-state, focus, and fallback assertions.

## Managed distribution and formal checks

- Start preflight passed for the approved `WO-DST-017` packet with `INT-DST-001`, `CAP-DST-001`, requirements `REQ-DST-030/032/033/035/047`, specifications `SPEC-DST-008/010/012/016`, `ARCH-DST-008`, `ADR-DST-008`, and `VER-DST-016`.
- The pre-apply upgrade plan identified exactly `scripts/harness_explorer/index.template.html` for update and protected the two self-hosting controls. Apply completed transactionally. After the scoped CSS correction, the same bounded update was applied again; the final idempotence plan reported 32 unchanged managed files and no update.
- The complete regression suite exercises transactional/idempotent upgrades, customized and ambiguous upgrade refusal, installation parity, schema-two locks, hostile/corrupted resources, progressive loading, and self-hosting boundaries.
- Final root `harnessctl doctor` and `git diff --check` pass. Formal validation passes for 451 artifacts with structure, governance, and policy at E0/W0; its 44 maintenance warnings are existing compatibility/location notices outside this packet.

## Automated and deterministic evidence

- `python -B -m unittest discover -s tests -p "test_dashboard_webui.py"`: 19 tests passed in 3.341 seconds.
- The ordinary full-suite invocation found one environment-only `RID018` because the host Python exposes installed `se-harness 0.4.0` distribution metadata outside the fresh 0.4.1 source checkout. The isolated failing file passed all 24 tests with site packages disabled.
- `python -S -B -m unittest discover -s tests -p "test_*.py"`: all 232 tests passed in 67.121 seconds; 3 environment-dependent tests skipped. This removes the unrelated globally installed distribution from source-identity discovery while retaining the checkout under test.
- Two final real-repository generations each produced 451 artifacts, 1660 relations, 537 files, 0 errors, and 44 existing warnings. Both retained manifest SHA-256 `7bd77494a58f6a222e67d7e4c0e30b1a029bb9046a55710b016d74f241d1aeae` and dashboard SHA-256 `2bf216f9b1854d0f6342b043d3414f93bfda858cf467972ecb37980b711001a4`.
- Every generated file matched between the two runs except `generation-summary.json`, whose documented observational timestamp, elapsed time, and output path differ. Manifest, index, content, artifact, topology, readiness, and summary resources were identical.

## Browser and responsive evidence

- The generated real-repository dashboard was served only on loopback and inspected in the Codex in-app browser. At 1440 x 900, 900 x 900, and 390 x 844, document scroll width equaled the usable client width; no page-level horizontal overflow occurred.
- Wide review initially identified the supplied State Lens overlap. After the scoped two-column correction, its seven items rendered legibly. At medium width the queue and lens stacked into one 758.7-pixel column. At narrow width all three named navigation buttons remained semantically exposed, the bottom navigation remained available, and the two-column metric/lens presentation stayed within the 375-pixel client width.
- Semantic browser actions opened Overview, Lineage, and Readiness; Lineage exposed navigation history; the search value `WO-DST-017` narrowed the graph to one match and Clear restored the empty filter; Readiness exposed the gate title, policy badge, policy-owner note, subject selector, and derived decision-boundary summary.
- Normal wide/narrow/medium runs produced no browser console warning or error. Accessible names and visible focus styling were observed on navigation/search controls, and the focused tests retain explicit `:focus-visible` and accessible-name assertions. The in-app automation's synthetic Tab injection did not advance focus reliably, so a complete independent physical-keyboard traversal remains residual manual review uncertainty rather than a claimed observation.
- In a disposable generated copy, only `GRAPH_SOURCE` was changed to a CSP-disallowed unavailable host. The browser displayed `Interactive 3D topology unavailable`, retained the 451-artifact metric, and kept Overview, Lineage, Readiness, provenance, and outcomes available. Readiness still opened and exposed `Explorer gate groupings`. The sole console warning was the expected `3D graph library failed to load` containment signal.

## Residual risk and unperformed actions

The optional pinned CDN remains an accepted external availability risk. Representative rendering cannot prove comprehension for every repository size, browser, display, assistive technology, or physical keyboard. The literal prompts are intentionally absent; discoverability now depends on the three named routes and semantic sections approved by `SPEC-DST-016`.

No promotable distribution was built. At candidate-evidence capture time, hosted CI, a physical-keyboard/assistive-technology session, commit creation, push, pull request, VREC preparation or transition, release, tag, publication, deployment, and governor promotion had not been performed. The owner's later bounded authorization permits the candidate commit, ready VREC preparation, branch push, and pull-request creation to follow the repository workflow; all other listed actions remain unperformed and unauthorized.
