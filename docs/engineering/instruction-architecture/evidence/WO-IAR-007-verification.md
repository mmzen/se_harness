# WO-IAR-007 implementation and verification evidence

## Authority and scope

The repository owner approved `REQ-IAR-015`, `SPEC-IAR-007`, `ARCH-IAR-007`, `ADR-IAR-007`, `VER-IAR-007`, and `WO-IAR-007` on 2026-08-15 with the instruction `ok i approve`. The implementation remained within the approved first taxonomy increment: it added explanatory diagnostic planes without adding rules, commands, profiles, heuristics, evaluator selection, scores, or changed gate behavior.

## Baseline compatibility oracle

Before implementation, candidate-source validation reported:

- valid: `true`;
- artifacts: `316`;
- errors: `0`;
- warnings: `40`;
- warning codes: `W013 = 11`, `W014 = 14`, `W015 = 15`;
- JSON fields: `artifact_count`, `artifacts`, `error_count`, `errors`, `valid`, `warning_count`, and `warnings`.

The first focused taxonomy test failed at the intended seam because `TAXONOMY_VERSION` and the diagnostic plane contract did not yet exist.

## Delivered behavior

- Added the closed `se-harness-validation-taxonomy-v1` vocabulary: `structure`, `governance`, `policy`, and `maintenance`.
- Added an explicit validated plane to every diagnostic emission; an AST regression test rejects missing classifications.
- Preserved the existing errors and warnings collections, codes, paths, messages, validity rule, ordering basis, and exit behavior.
- Added additive JSON fields: `taxonomy`, `plane_counts`, and per-diagnostic `plane`.
- Added a compact human `Planes:` summary and visible plane labels without a score.
- Added concise authoritative wording to managed `QUALITY_GATES.md` and operator wording to `docs/notes/harnessctl-reference.md`.
- Synchronized the canonical validator and quality-gate policy, then refreshed their schema-2 lock hashes through the supported upgrade transaction.

## Rule-to-plane matrix

| Plane | Implemented rule families |
| --- | --- |
| `structure` | artifact discovery/parsing, common and type-specific field shape, IDs and prefixes, lifecycle vocabulary, required relation shape, target existence, self-reference, and typed targets |
| `governance` | active requirement coverage, architecture traceability, decision assessment and ADR coverage, VREC/RLS metadata and evidence, aggregate scope, supersession, commit agreement, and release gating |
| `policy` | configured `required_for_verified_work` coverage obligation |
| `maintenance` | `W013` canonical placement, `W014` legacy decision assessment, and `W015` legacy architecture relation advisories |

Classification is explicit at the emitting rule. It is not inferred from code ranges; `E010` can therefore represent either governance invariants or the configured policy obligation.

## Verification results

- Packet activation: formal validation passed with 316 artifacts, zero errors, and 40 pre-existing warnings; start preflight for `WO-IAR-007` passed with zero diagnostics.
- Focused compatibility and affected-domain suite: 89 tests passed with two expected skips before the final AST coverage addition.
- Complete Python 3.14.6 suite: 173 tests passed with three expected skips.
- Complete Python 3.11.9 suite: 173 tests passed with three expected skips.
- Managed upgrade: 33 entries, 31 unchanged and two protected self-hosting controls; apply refreshed the two intended lock hashes; the following plan was idempotent.
- Candidate-source `doctor`: passed with zero failures; root and canonical validator/quality-gate distribution copies matched and managed hashes were unchanged.
- Harness Explorer: generated twice with 316 artifacts, 1,152 relations, zero validator errors, 49 derived observations, and identical snapshot `4f98d14b0346557e32c232cac9af281f763559a7ce01dbd95d51946035a6457d`.
- Formal validation after implementation: `se-harness-validation-taxonomy-v1`, 316 artifacts, zero errors, and the same 40 warnings; all 40 warnings are in `maintenance`, with zero findings in the other three planes.
- Review preflight: `WO-IAR-007` was `implemented`, ready, and had zero diagnostics.
- CLI help, canonical byte parity, idempotent upgrade plan, and diff hygiene all exited zero.

## Changed components

- Formal packet and instruction-architecture index.
- Root and canonical `scripts/validate_engineering_artifacts.py`.
- Root and canonical `docs/engineering/QUALITY_GATES.md`.
- `docs/notes/harnessctl-reference.md`.
- `tests/test_validation_taxonomy.py`.
- `.engineering-harness.lock`.

## Deliberately unperformed work

No validation profile, inspection command, pending/orphan/aging heuristic, evaluator identity, policy-schema redesign, preflight or doctor semantic change, dashboard redesign, package version change, wheel, sdist, commit, push, pull request, VREC, release record, tag, publication, or deployment was produced. Building a package was not required to prove this standard-library reporting change and was not separately authorized; existing installer and package-data regression tests exercise the distribution surface.

## Residual risks

- Plane selection remains a reviewed design judgment; the taxonomy does not prove that the long-term boundary is ideal.
- Preflight currently translates validator diagnostics into its own diagnostic model and does not expose the new plane; changing that public contract is outside this packet.
- Harness Explorer remains behaviorally compatible but does not yet add plane-specific presentation.
- Evaluator identity and independent-governor behavior remain separate self-hosting concerns.
- Existing warnings remain non-blocking historical maintenance observations.
