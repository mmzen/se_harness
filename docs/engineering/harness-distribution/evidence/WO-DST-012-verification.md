# WO-DST-012 implementation and verification evidence

## Authority and boundary

On 2026-08-16 the repository owner explicitly authorized implementation of `WO-DST-012` with `go for implementation`. The approved work order classifies commit-bound verification as required. This evidence records candidate implementation checks only; it does not create a candidate commit, transition a VREC, open or update a pull request, authorize release, update the public demonstrator, publish a package, or deploy software.

Start preflight passed with `REQ-DST-040`, `REQ-DST-041`, `SPEC-DST-011`, `VER-DST-011`, and `WO-DST-012` approved. The work order then moved to `in_progress`. The implementation stayed inside the browser presentation, canonical snapshot, managed distribution, and accepted CDN boundaries documented by the packet.

## Implemented mapping

- `REQ-DST-040`: replaced the free-positioned two-hop/nine-card Lineage layout with six stable conceptual groups and exact formal-type sublanes. Unknown types remain visible under `Other`; missing types use `Unknown type`. Cards retain exact ID, title, type, lifecycle state, and selected/direct/second-level scope text.
- Depth 1 retains the selected artifact and every resolved direct neighbor without a direct-neighbor cap. Depth 2 adds at most 100 deterministic non-direct artifacts, with visible and omitted counts. Traversal is iterative, sorted, cycle-safe, and missing targets are not synthesized.
- Every resolved relation inside the visible scope remains in the board relation set. Directional connectors preserve source, target, relation name, and declared/derived authority. Relations incident to the selected artifact are emphasized and labeled; all relations remain available through the authoritative Relations tab. Unresolved direct targets are reported explicitly.
- `REQ-DST-041`: added in-memory Navigation history with Back, Forward, visited-ID controls, Return to initial, current/disabled/unavailable states, forward-branch truncation, no consecutive duplicate, a 20-visit sliding-window bound, and an accessible discarded-history announcement. External Explorer entry resets history and depth; internal card/detail selection appends. Every history render adjusts only the history list's horizontal scroll position as needed to reveal the current visit fully; it does not reassign focus or scroll the page or board.
- The history region explicitly states that visits are not formal lineage. No URL, browser-history, storage, cookie, network, canonical-snapshot, evidence, or repository persistence was added.
- Desktop uses a deterministic horizontally scrollable board. At narrow width, the same six labeled groups stack, connector geometry is hidden, and the Relations tab remains the complete non-geometric route.

The Overview topology, `harness-dashboard-snapshot-v1`, generator, validator, inspection, readiness, formal artifacts, revision provenance, CLI, exact `3d-force-graph@1.79.0` URL, CSP, fallback boundary, public Pages workflow, and release behavior are unchanged.

## Managed distribution transaction

The reusable source changed at `templates/repository/standard/scripts/harness_explorer/index.template.html`. Candidate `harnessctl upgrade .` planned one managed update while protecting `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`. Explicit `upgrade . --apply` updated `scripts/harness_explorer/index.template.html` and only its schema-2 lock digest. A second plan reported no update and 32 unchanged managed files.

The canonical template initially retained mixed historical CRLF/LF bytes while the supported updater emitted normalized LF. The canonical file was mechanically normalized to LF so the raw managed parity promise is exact. Canonical template, active template, and lock SHA-256 are all:

`cdae72ccc98ee0bf9f42fc29d0e12248d0be2dbb08dda574029a2b64db3d9b3c`

No protected self-hosting control, generator, workflow, package metadata, dependency, runtime URL, or other managed file changed.

## Automated checks

| Check | Result |
| --- | --- |
| Focused `tests.test_dashboard_webui` | PASS - 13 tests |
| Complete `unittest` discovery | PASS - 221 tests, 3 existing skips; final replay completed in 72.500 seconds |
| `harnessctl validate .` | PASS - 405 artifacts, 0 errors, 42 existing maintenance warnings |
| `harnessctl doctor .` | PASS - required files, managed Explorer template, lock, and self-hosting controls valid; existing location warnings remain non-blocking |
| Candidate-source start preflight | PASS - `WO-DST-012` approved |
| Candidate-source review preflight | PASS - `WO-DST-012` implemented with retained evidence |
| Managed upgrade replay | PASS - protected controls plus 32 unchanged managed files; no update |
| `python -m se_harness --help` | PASS - public command surface unchanged |
| Final dashboard generation twice | PASS - identical snapshot SHA-256 `a3e1edba3e367b9bc9738979b04aaa107f669600ba7278b15551316ce416e70d` |
| `harnessctl inspect .` | PASS - no active work; `WO-DST-012` is the sole assurance-pending work order |
| `git diff --check` | PASS |

Focused assertions cover the fixed group/type map, exact depth options, complete direct-scope construction, 100-node second-level budget, stable relation direction and authority, unknown types, unresolved-target reporting, removal of the rank/nine-card/zoom contract, exact history controls, branch truncation, the 20-entry bound, minimum horizontal current-visit reveal without `scrollIntoView`, Return to initial, non-persistence, canonical/active parity, and the unchanged Overview CDN boundary.

## Browser interaction and responsive review

The generated 405-artifact dashboard was served only on temporary localhost and inspected in the in-app browser. The JavaScript loaded and executed successfully, the existing 3D Overview remained available, and browser logs contained no warning or error. Temporary tabs and local servers were closed after review.

- Initial Lineage showed `INT-AGR-001` plus its direct capability in the `Purpose` group. All six conceptual group headings and exact-type sublanes were present in stable order.
- Selecting `CAP-AGR-001` produced 10 visible artifacts, 9 complete direct neighbors, and 9 resolved relations. Exact type, status, ID, title, and scope text remained visible.
- The sequence `INT-AGR-001 -> CAP-AGR-001 -> REQ-AGR-001`, Back, Forward, Back, then `REQ-AGR-002` produced the expected branched history `INT-AGR-001`, `CAP-AGR-001`, `REQ-AGR-002`, with Forward disabled.
- Depth 2 from `REQ-AGR-002` produced 31 cards: 1 selected, 6 direct, and 24 second-level, with 95 resolved relations and exactly 6 selected-artifact relation labels.
- Depth 2 from `CAP-DST-001` produced 107 cards: 1 selected, 42 complete direct, and 64 second-level, with 391 resolved relations. This exercised a dense multi-lane distribution graph without direct-neighbor omission or browser error.
- Twenty-four additional alternating visits retained exactly 20 entries and reported 5 discarded older visits. The current rightmost chip was fully visible with list `scrollLeft` 1786 while the document stayed horizontally fixed. Selecting the oldest retained visit moved only the history list to `scrollLeft` 0; Forward and Back kept their selected chips fully visible and focus on the replacement history control.
- In a separate session that did not revisit its initial artifact, 24 visits retained exactly 20 entries and reported 4 discarded visits. Return to initial appended the aged-out initial artifact through the ordinary bound, retained 20 entries, reported 5 discarded visits, selected the exact initial artifact, and revealed it fully at the right edge with list `scrollLeft` approximately 1829 while document horizontal scroll remained zero and selected-card focus was preserved.
- Opening `WO-AGR-001` from Readiness reset the session to one history entry and depth 1. Internal card selection continued to append instead of reset.
- At the default 1265-pixel browser width, document scroll width equaled viewport width; the board owned its horizontal overflow. At the narrow breakpoint, client and document scroll widths were both 375 pixels, all six groups stacked, 19 current cards remained available, connectors were hidden, history controls used the responsive grid, and the Relations tab remained visible.
- Buttons use native semantics, programmatic names, visible focus rules, and explicit disabled/current states. Selected-card rerender restored focus to the new card and history navigation restored it to the current visit. The browser test surface did not synthesize native click activation from injected Enter/Space even for the pre-existing Overview button, so activation equivalence is grounded in native-button construction and the shared click path rather than claimed from that unsupported injection.

Two consecutive dashboard generations before completion-state recording produced identical canonical snapshot SHA-256:

`37b32ed07c6fc5e665a4f7068ae1ed4fe85ebaa8ab8c2b334ceb83ac76ce8557`

After the work order moved to `implemented` and retained evidence was present, two further consecutive generations produced the identical final canonical snapshot SHA-256:

`a3e1edba3e367b9bc9738979b04aaa107f669600ba7278b15551316ce416e70d`

The digest change from the earlier generation is expected: the formal work-order status moved from `in_progress` to `implemented` and the evidence path became part of the repository snapshot. Repeating the completed state was byte-stable.

## Governor separation observation

Local preflight, tests, validation, doctor, managed upgrade, generation, and browser review used the editable candidate environment. They are candidate-source implementation evidence, not independent released-governor verification. `doctor` identified the selected released governor as v0.3.0 with digest `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`; this work did not change or execute a governor transition.

Independent exact-commit acceptance remains unavailable until a candidate commit exists. CI and a later commit-bound VREC decision remain required and are not claimed here.

## Deviations and residual risk

No approved product or architecture deviation was required. Very dense direct neighborhoods intentionally remain complete and can require vertical and horizontal scrolling. Relation connectors can overlap in dense boards; selected-relation emphasis, exact labels, scope counts, stacked narrow fallback, Related artifacts, and the authoritative Relations tab constrain but do not eliminate that usability risk.

The optional Overview topology retains the previously accepted CDN availability and supply-chain risk. The Lineage board itself uses only embedded data and local code. The 42 validator warnings are the repository's existing maintenance observations and are unrelated to this work.

The standalone `node` executable was not installed in the shell environment, so no separate Node syntax command was claimed. Actual Chromium page load, interactions, responsive layout, and empty browser error logs supplied the executable JavaScript check.

## External actions not performed

No commit, push, pull request, VREC, release record, tag, GitHub Release, PyPI publication, public-demonstrator update, or deployment was performed.
