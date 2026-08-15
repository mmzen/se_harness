# Verification Evidence: WO-DOC-012

Date: 2026-08-15

## Authority and scope

The repository owner approved `REQ-DST-034`, `SPEC-DST-009`, `VER-DST-009`, and `WO-DOC-012` with `ok go for implementation`. The implementation is limited to reconciling current documentation contracts, four progressive notes, focused documentation assertions, the domain index, and this evidence. Runtime behavior, managed policy, historical evidence, VRECs, releases, and external state remain outside scope.

The implementation checkout already contained the committed `WO-IAR-008` and `WO-IAR-009` candidate plus an uncommitted ready `VREC-IAR-005`. That ready record was not edited, committed, transitioned, or treated as applicable to the descendant documentation candidate.

## Implemented correction

| Surface | Result |
| --- | --- |
| `REQ-DST-025` | Current ordinary human-facing command surface changed from five to six commands by adding `inspect`; gate and authority boundaries are explicit. |
| `SPEC-DST-007` | Command block and concise-root contract now distinguish `doctor`, gate-oriented `validate`, non-gating `inspect`, and visual `dashboard`; historical evidence remains separate. |
| `VER-DST-007` | Current assertions and reader scenarios now verify six commands and the validate/inspect distinction without rewriting original `WO-DOC-008` evidence. |
| `harness-overview.md` | Tier-0 automation boundary names inspection and explains that it cannot decide or perform the next step. |
| `harness-operational-phasing.md` | Execution/review phase and command table place inspection after validation and state their different exit/authority meanings. |
| `harness-installation-and-upgrades.md` | Post-install sequence includes inspection and warns that a successfully produced report may still show invalidity or attention. |
| `harness-lineage-example.md` | Practical agent sequence runs `validate`, `inspect`, then `dashboard`; suggestions remain bounded and non-executable. |
| `test_progressive_documentation.py` | Focused assertions protect the six-command active contract, all four note updates, CLI availability, and non-authority wording. |

The root README already satisfied the six-command concise contract and remained unchanged by `WO-DOC-012`: `159` physical lines and `9` level-two headings. `docs/notes/harnessctl-reference.md`, managed `QUALITY_GATES.md`, managed `WORKFLOW.md`, and their canonical copies were inspected and required no content change.

## Verification results

| Check | Result |
| --- | --- |
| Start and review preflight | PASS for `WO-DOC-012` in `in_progress` and final `implemented` states; the complete governing manifest was returned in both phases. |
| Focused public/progressive/instruction documentation tests | PASS: `44` tests. |
| Complete suite, Python 3.14.6 | PASS: `185` tests, `3` expected conditional Windows skips. |
| Complete suite, Python 3.11.9 | PASS: `185` tests, `3` expected conditional Windows skips. |
| Formal artifact validation | PASS: `334` artifacts, `0` errors, `40` pre-existing maintenance warnings; planes `structure E0/W0`, `governance E0/W0`, `policy E0/W0`, `maintenance E0/W40`. |
| Doctor | PASS: `82` passing checks and `11` classified historical `W013` placement warnings. |
| CLI help | PASS: `inspect` is present alongside the complete current command inventory. |
| Deterministic inspection | PASS in final `implemented` state: `se-harness-inspection-v1`, `334` artifacts, `90` retained findings, `36` bounded suggestions; two byte-identical JSON reports, SHA-256 `50d0033dc33d32c66d4cbd68dcc347ad249156a280c11ed1d445961b5184c58c`. |
| Deterministic Harness Explorer | PASS twice in final `implemented` state: `334` artifacts, `1190` relations, `0` errors, `61` warnings, snapshot `cedfeaf0e86f251f06e1d1ed253f351b0094018e5b914cdd54f2e049f70a685f`. |
| Managed documentation parity | PASS: root/canonical `QUALITY_GATES.md` SHA-256 `4fe82d19464bf6394b48c75abf27f9f0f6c6d7a0a10da26c1a02f00666cbed29`; root/canonical `WORKFLOW.md` SHA-256 `4f28168e37b83f062936691c40619ac20d367beb8207d594f4cf77f27c558003`. |
| Local links, expertise metadata, Markdown fences, placeholders, mojibake, and unsafe inline content | PASS through focused progressive and public-onboarding tests. |
| README budget and protected root | PASS: root README unchanged, `159` lines, `9` level-two headings. |
| Historical protected paths | PASS: no tracked file under an evidence, verification-records, or releases directory changed before this new work-order evidence was added. Existing untracked `VREC-IAR-005` remained separate. |
| Diff hygiene | PASS: no whitespace errors. |

## Behavioral and authority assessment

- `validate` remains the gate-oriented formal graph operation; documentation planes explain source rather than changing severity or exit behavior.
- `inspect` remains a derived read-only report. Successful report production may coexist with an invalid graph or attention findings.
- Suggestions identify possible accountable next steps but contain no executable command, set `automatic = false`, and establish no eligibility or authority.
- No runtime source, managed policy, canonical managed template, package version, workflow, schema, or consumer repository changed.
- No architecture or ADR was created because the correction preserves existing documentation responsibilities and introduces no architecturally significant requirement driver.
- Earlier `WO-DOC-008` evidence remains true for its exact candidate and was not rewritten.

## Deviations and residual uncertainty

The sandboxed shell did not expose the `py` launcher, so the supported Python 3.11.9 interpreter was invoked through its explicit installed path. The first unprivileged Explorer regeneration was denied access to its derived `target` staging directory; it was repeated with explicit filesystem permission and passed twice with the same snapshot. Neither condition changed repository source or verification semantics.

Automated checks establish command spelling, required distinctions, links, and protected boundaries. Reader comprehension remains a manual judgment; the reviewed wording keeps the 4/10 overview concise, the 5/10 installation route operational, and the 6/10-to-7/10 phasing and practical example progressively detailed.

## Candidate boundary

This evidence records completed implementation only. No candidate commit, VREC replacement, approval, push, pull-request update, merge, release, publication, or deployment is claimed. A later clean candidate must include the three IAR/DOC work orders and separate evidence, after which a newly prepared aggregate VREC must bind that exact descendant commit.
