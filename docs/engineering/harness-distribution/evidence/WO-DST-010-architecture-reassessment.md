# WO-DST-010 architecture-reassessment evidence

## Scope and authority

On 2026-08-16, the repository owner selected the recommended reassessment of the three `W-HEX-003` observations and authorized `WO-DST-010`. When updating the source architectures truthfully exposed two downstream observations from their deciding ADRs, the owner explicitly instructed `yes go`, authorizing a bounded ADR reaffirmation and correction of the obsolete command list in `ADR-DST-007`.

The work does not change product behavior, requirements, specifications, relations, inspection logic, lifecycle rules, selected ADR options, accepted risks, verification contracts, or historical evidence. Commit, push, pull request, VREC transition, release, publication, and deployment remain separate decisions.

## Original observations and dependency revisions

Before reassessment, inspection reported exactly three `W-HEX-003` observations:

- `ARCH-DST-007` dated 2026-08-12 depended through `addresses` on `REQ-DST-025`, revised 2026-08-15;
- `ARCH-DST-007` dated 2026-08-12 depended through `conforms_to` on `SPEC-DST-007`, revised 2026-08-15; and
- `ARCH-DST-008` dated 2026-08-13 depended through `conforms_to` on `SPEC-DST-008`, revised 2026-08-15.

The first two target revisions documented the already implemented read-only, non-gating `inspect` command and distinguished it from `validate` and `dashboard`. The third removed the redundant `templates/webui/` handoff and established the standard-distribution Explorer template as the sole reusable source.

## Accountable conclusions

`ARCH-DST-007` already assigns concise public guidance to the README and progressive operational detail to notes and reference documentation. Adding `inspect` to that existing human surface does not alter a component, dependency direction, authority source, trust boundary, required pattern, prohibited pattern, or quality attribute. Its architecture remains applicable.

`ARCH-DST-008` already separates the canonical snapshot, static renderer, browser presentation, and managed distribution copies. Removing a redundant design-source directory strengthens that boundary without changing data flow, DOM safety, the external CDN trust boundary, fallback behavior, accessibility obligations, or accepted supply-chain risk. The ambiguous source-copy sentence now names the canonical standard-distribution template and active managed root copy.

Dating those architecture reassessments exposed two truthful downstream `ADR.decides -> ARCH` observations. `ADR-DST-007` and `ADR-DST-008` were therefore reaffirmed on the same date. Their selected options, outcomes, consequences, and accepted risks remain unchanged. `ADR-DST-007`'s list of public commands was corrected from five commands to the implemented six by adding `inspect`; this aligns the decision record with the already governed behavior rather than introducing it.

## Changed paths

- `docs/engineering/harness-distribution/README.md`
- `docs/engineering/harness-distribution/architecture/ARCH-DST-007.md`
- `docs/engineering/harness-distribution/architecture/ARCH-DST-008.md`
- `docs/engineering/harness-distribution/architecture/adr/ADR-DST-007.md`
- `docs/engineering/harness-distribution/architecture/adr/ADR-DST-008.md`
- `docs/engineering/harness-distribution/work-orders/WO-DST-010.md`
- `docs/engineering/harness-distribution/evidence/WO-DST-010-architecture-reassessment.md`

## Verification results

| Check | Result |
| --- | --- |
| Original inspection baseline | Three `W-HEX-003` observations for the two source architectures. |
| Post-reassessment inspection | PASS: zero `W-HEX-003` observations; no rule suppression or target-date change. |
| Formal artifact validation | PASS: 361 artifacts, 0 errors, 40 classified maintenance warnings. |
| Focused documentation, Explorer, and inspection tests | PASS: 35 tests. |
| Managed-integrity doctor | PASS: required, distribution, managed, lock, and self-hosting checks passed; 11 existing `W013` location advisories remain. |
| Start and review preflight | PASS: start preflight passed while the work order was approved; review preflight passed while it was implemented and selected the complete governing chain. |
| Deterministic inspection | PASS: two consecutive JSON inspections were byte-identical after PowerShell capture, with 361 artifacts, 1,306 relations, 40 existing warnings, zero `W-HEX-003` findings, and SHA-256 `379d94ee6f400b49060c550ecb84dd17ff0418e5db6f805a18645b3e8aa31392`. |
| Diff hygiene and path boundary | PASS: `git diff --check` reported no errors and the diff is limited to the seven declared paths. |

The remaining 40 warnings are pre-existing legacy architecture and canonical-location maintenance observations outside this work order. No active `W-HEX-003` observation remains.

One review-preflight invocation initially supplied the work-order path and returned the expected `invalid work-order ID` diagnostic. The command was corrected to the required artifact ID, `WO-DST-010`, and passed. The failed read-only invocation did not modify the candidate and is not treated as verification evidence.

## Authority boundary

This evidence demonstrates implementation and retained review evidence for `WO-DST-010`; it is not an assurance decision. It does not verify a candidate commit, transition a VREC, authorize release, or grant any external action.
