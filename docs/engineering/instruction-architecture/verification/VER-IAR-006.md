+++
id = "VER-IAR-006"
type = "verification"
title = "Verify artifact catalog authority and applicability consistency"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-IAR-014"]
+++

# Verification Contract: Verify artifact catalog authority and applicability consistency

## Independence

Verification derives expected artifact membership from the canonical layout registry and expected semantics from the approved requirement, specification, architecture, and ADR. Tests may inspect documentation structure but must not accept implementation wording as the oracle for applicability.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-IAR-014` | catalog membership test | canonical registry versus authoritative catalog | Every canonical standard type appears exactly once; missing, duplicate, and unsupported entries fail deterministically. |
| `REQ-IAR-014` | responsibility inspection | router, traceability, workflow, notes, and templates | Traceability owns the catalog; router links directly; other documents cross-reference or retain focused responsibilities without a second normative catalog. |
| `REQ-IAR-014` | applicability matrix | work orders with routine and architecturally significant requirements | No-applicable-architecture omission passes; applicable omission, irrelevant selection, and missing required ADR coverage fail. |
| `REQ-IAR-014` | distribution and upgrade tests | root, standard template, wheel, fresh install, adopt, and upgrade | Managed copies and packaged data agree; customized content is protected; no formal artifact is rewritten. |
| `REQ-IAR-014` | human review | catalog entries and examples | Objective, required-when, omission/reuse, owner, relations, and lifecycle references are understandable and consistent for all types. |

## Catalog tests

- Parse only the bounded authoritative catalog section, not incidental type names elsewhere in the document.
- Compare against `ARTIFACT_DIRECTORIES` and `ARTIFACT_PREFIXES`.
- Reject duplicate rows, unknown canonical-looking entries, missing required columns, and type/prefix mismatch.
- Confirm evidence, acceptance scenarios, source, commits, dashboards, tickets, and conversations are identified as non-formal material rather than catalog types.
- Confirm the test is insensitive to line endings and deterministic across supported runtimes.

## Work-order architecture matrix

1. No architecture addresses any implemented requirement and the work order omits `architecture`: pass.
2. No architecture applies and the work order declares an empty `architecture` list: fail as malformed relation data.
3. Active architecture addresses an implemented requirement and is omitted: fail.
4. All applicable architecture is selected and every shared specification is selected: pass.
5. Selected architecture has no relevant conforming specification: fail.
6. Selected architecture is `adr_required` and no deciding ADR is selected: fail.
7. Selected architecture has accepted `no_significant_decision` and no ADR is selected: pass.
8. Historical completed work orders and commit-bound records remain unchanged and valid under their compatibility rules.

Exercise both formal validator and start/review preflight text and JSON where applicable.

## Routing and documentation review

- Confirm `ENGINEERING_HARNESS.md` directly routes purpose, applicability, reuse, and relation questions to `TRACEABILITY.md` without copying the table.
- Confirm the Tier-0 overview and UML/model note use relative links to the catalog and retain their declared non-authoritative status.
- Confirm `WORKFLOW.md` continues to own sequence and lifecycle transitions and `DECISION_RIGHTS.md` continues to own accountability.
- Confirm the template index owns canonical locations and templates provide prompts without contradicting conditional applicability.
- Confirm the catalog is readable by an operator without source inspection and sufficiently precise for an agent to stop rather than infer.

## Managed distribution and upgrade checks

- Compare root managed files with `templates/repository/standard/` where parity is required.
- Run candidate-source transactional upgrade and prove idempotence.
- Verify schema-2 lock hashes and line-ending canonicalization.
- Build an explicitly non-promotable ephemeral wheel from a clean Git export only when the approved work order permits it.
- Install into a fresh Python 3.11 environment outside the checkout; run `init`, `doctor`, `validate`, and relevant preflight fixtures.
- Confirm customized managed policy blocks replacement without partial writes.

## Security and resilience

Exercise malformed Markdown rows, deceptive type names, duplicate prefixes, Unicode, CRLF/LF variation, oversized cell content, malformed TOML relations, unknown targets, and injection-shaped values. No documentation or artifact value may be executed or shell-interpolated.

## Regression

Run focused instruction-architecture, progressive-documentation, artifact-authoring, validator, preflight, installer, integrity, dashboard, provenance, and self-hosting tests plus the complete unit suite on Python 3.11 and the local supported runtime. Run `doctor`, formal graph validation, CLI help, deterministic dashboard generation, phase-appropriate preflight, and diff hygiene.

## Evidence retention

Retain commands, runtimes, test counts, catalog/type matrix, routing inspection, architecture applicability fixtures and diagnostics, managed parity, upgrade outcomes, package identity if built, changed paths, deviations, and residual risk under `docs/engineering/instruction-architecture/evidence/WO-IAR-006-verification.md`.

## Residual uncertainty

Structural checks cannot prove that an artifact description is semantically sufficient or that an author truthfully reused an existing artifact. Accountable owners must review the catalog and challenge suspicious applicability or reuse claims.
