# WO-DST-018 implementation and verification evidence

Date: 2026-08-19

This file retains implementation evidence for `WO-DST-018`. It is not a verification record, approval, release record, publication decision, or deployment authorization.

## Authorization and scope

- The repository owner supplied `C:/Users/mathi/Downloads/index.template.html` and instructed the agent to integrate it.
- The owner authorized a 256 KiB generated `index.html` limit, recorded as 262,144 UTF-8 bytes, and controlled same-document fragments plus browser History API state.
- Browser review of the exact intake found two defects: a fresh Lineage fragment was replaced by the default artifact before topology initialization, and malformed percent encoding stopped dashboard initialization.
- The agent stopped without editing the template and requested permission for only those two corrections. The owner answered `yes OK`.
- No other supplied CSS, markup, copy, interaction, schema, URL, dependency, storage, network, workflow, governor, release, publication, or deployment behavior was changed.

## Intake, final identity, and authorized delta

| Item | UTF-8/raw bytes | SHA-256 |
| --- | ---: | --- |
| Supplied intake | 153,493 | `6b6881a095fac417c358548342eb31737c58b9bf6345cf632b066f8aa53f470a` |
| Final canonical template | 153,839 | `f7aa922075fbc343f6ad8d61526323dc611f567ed8eb562c67b2e19194d2cc48` |
| Final active template | 153,839 | `f7aa922075fbc343f6ad8d61526323dc611f567ed8eb562c67b2e19194d2cc48` |

`git diff --no-index` between the intake and final canonical template showed only the authorized route delta:

1. apply the requested fragment before Lineage rendering can replace it with the default artifact;
2. add non-throwing route-component decoding, reduce malformed Lineage to `#overview`, reduce malformed Readiness subject routing to `#readiness`, and reduce an unknown resolved Lineage request to the safe current artifact route.

The final canonical and active template bytes are identical. The two generators both declare `MAX_INDEX_BYTES = 262_144` and match under the schema-2 `utf8-text-lf-v1` managed representation.

## Formal packet and preflight

- Added `SPEC-DST-017`, `VER-DST-017`, and `WO-DST-018` and revised the selected routing/size requirement, specification, verification, and domain-index wording.
- Start command: `python -B -m se_harness preflight . --work-order WO-DST-018`.
- Result: PASS, phase `start`, work order `approved`, commit-bound verification `required`, decided by `repository-owner`.
- The complete returned manifest was read before implementation.
- Formal validation: PASS, 481 artifacts, 0 errors, 44 pre-existing maintenance warnings; structure, governance, and policy planes had no warnings.

## Managed upgrade and customization boundary

The first upgrade plan proposed only:

- `scripts/generate_harness_dashboard.py` — update;
- `scripts/harness_explorer/index.template.html` — update;
- `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` — protected.

`python -B -m se_harness upgrade . --apply` updated the two ordinary managed files and the schema-2 lock. A second plan reported 32 unchanged ordinary files and only the two protected files. The final lock records:

- generator digest `48cc8e1bbb8c72ed8f808baa2504923d55708d110a0d7de8d39fce090bf0d429` under the managed representation;
- template digest `f7aa922075fbc343f6ad8d61526323dc611f567ed8eb562c67b2e19194d2cc48`.

`python -B -m unittest tests.test_harnessctl.HarnessCtlTests.test_upgrade_plan_is_read_only_and_apply_preserves_customized_file` passed: 1 test, 0 failures. The complete suite also exercised schema-1 ambiguity, schema-2 newline equivalence, protected drift, and upgrade transaction behavior.

## Automated verification

| Check | Result |
| --- | --- |
| `python -B -m unittest tests.test_dashboard_webui` | PASS, 19 tests |
| clean source environment: `python -B -m unittest discover -s tests -p "test_*.py"` | PASS, 252 tests, 3 skipped, Python 3.14.6 |
| `python -B scripts/validate_engineering_artifacts.py --root .` | PASS, 481 artifacts, 0 errors, 44 maintenance warnings |
| `python -B scripts/validate_release_distributions.py --root .` | PASS, 0 distribution-bearing records |
| `python -B -m se_harness --help` | PASS |
| `python -B -m se_harness doctor .` | PASS for every required, distribution, managed, lock, Python, and governor check; 15 historical-placement warnings remained |
| `git diff --check` | PASS; Git printed only configured LF-to-CRLF working-tree notices |

No formatter or linter command is defined by the repository, so none was invented. No promotable distribution build was run because this is not an approved release work order.

## Deterministic generation and budgets

The active and canonical generators each rendered the repository into separate external work directories.

- Both reported the same manifest SHA-256. The exact digest is deliberately not embedded here because this evidence is itself a generated evidence resource; embedding that digest would create a self-reference and change the next manifest.
- Recursive path/size/hash comparison showed all canonical bundle files identical.
- Only `generation-summary.json` differed in its documented noncanonical `generated_at` and `elapsed_ms` fields; the summaries were identical after removing those fields.
- Generated `index.html`: 154,075 bytes, limit 262,144.
- Summary resource: 706 bytes, limit 262,144.
- Topology resource: 477,645 bytes, repository target 524,288.
- Projected content remained below the 16,777,216-byte limit; 565 documents were represented and 0 were omitted.
- Bundle: 481 artifacts, 1,815 relations, 568 resources, 0 validator errors, 44 maintenance warnings.

## Static security and interface checks

- Bootstrap markers: 1.
- Script elements: 2; style elements: 1.
- Script Subresource Integrity attributes: 0. The local `data-integrity` presentation attribute remains distinct.
- CSP remains `default-src 'none'`, inline local style/script, exact `https://unpkg.com` script origin, same-origin connect, data-only images, and no fonts/base/forms/objects.
- The exact graph asset remains `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js`; no other runtime origin was added.
- Static scans found no local/session storage, cookies, WebSocket, EventSource, beacon, service worker, or `eval` surface.

## Browser verification

The generated bundle was served from a disposable Python standard-library HTTP server and inspected in fresh browser tabs.

- Overview initialized as a verified bundle with 481 artifacts and the progressive request sequence `index -> manifest -> summary -> topology`.
- Readiness data was requested only after entering Readiness.
- Fresh `#lineage/REQ-DST-055` selected exactly `REQ-DST-055` and started `1 of 1 retained visits`.
- Visiting `SPEC-DST-013` produced `2 of 2 retained visits`; reloading `#lineage/SPEC-DST-013` selected that artifact and reset the trail to `1 of 1`.
- Fresh malformed `#lineage/%E0%A4%A` reduced to `#overview` and the verified bundle initialized.
- Unknown `#lineage/NOT-A-REAL-ID` reduced to the safe default artifact route.
- Valid `#readiness/subject/WO-DST-018` opened exactly that subject; malformed Readiness subject encoding reduced to `#readiness` and initialized safely.
- Overview/Readiness navigation produced History API entries; browser Back restored `#overview` and Forward restored `#readiness`.
- Desktop, 800 × 900, and 390 × 844 layouts remained usable. The mobile layout exposed bottom navigation, readable one-column gate figures, and no observed clipped control. A focused navigation button had a clear non-color outline.
- A disposable generated-output fixture changed only the graph source to a CSP-blocked local URL. The page displayed `Interactive 3D topology unavailable`, retained repository metrics, and kept the Readiness view and its 84 subjects usable. This fixture did not change repository source.

## Deviations and residual observations

- The generation summary is intentionally noncanonical and contains timing fields; canonical resource determinism passed and normalized summaries matched.
- The browser automation binding visibly focused ordinary buttons but did not synthesize their native Enter/Space activation during this run. The controls are native buttons, the focused state was visible, click behavior passed, and the focused contract suite passed; this retained observation is not an accessibility certification.
- At a wide desktop width, the supplied Readiness gate grid exposes its `--border` background across unused cells in the final row as a large gray rectangle. This is a presentation artifact in the supplied design, does not hide evidence or controls, and was not changed because the owner authorized only the two route corrections. A later visual adjustment requires explicit owner permission.
- The accepted CDN availability and supply-chain risks in `ADR-DST-008` remain. The failure fallback passed locally.
- SHA-256 verifies resources relative to the trusted generated shell; it does not authenticate an attacker able to replace the entire hosted bundle.

## Candidate commit authorization and excluded external actions

At verification closeout no commit had yet been created. The repository owner subsequently instructed `OK: commit the clean candidate under WO-DST-018.` This evidence is included in that authorized candidate and intentionally cannot contain the hash of its own commit; a later commit-bound VREC must bind the exact candidate hash. No push, branch or pull-request mutation, tag, VREC preparation or transition, release preparation or transition, package build, publication, GitHub Pages deployment, external message, governor promotion, or production operation was authorized or performed.
