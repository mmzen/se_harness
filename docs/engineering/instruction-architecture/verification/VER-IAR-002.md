+++
id = "VER-IAR-002"
type = "verification"
title = "Verify managed policy responsibility separation"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-IAR-010"]
+++

# Verification Contract: Verify managed policy responsibility separation

## Independence

Verification evaluates the externally visible responsibility and upgrade invariants in `REQ-IAR-010`, not an implementation-selected exact paragraph alone. Automated assertions are complemented by human semantic inspection so shorter wording cannot silently weaken authority or provenance.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-IAR-010` | focused content tests | canonical router and fresh-install output | Required invariants and direct routes are present; duplicated ordered procedure is absent. |
| `REQ-IAR-010` | upgrade tests | unchanged, customized, damaged, and repeated-upgrade fixtures | Safe content upgrades; ambiguous content is preserved; failures make no partial writes; repetition is idempotent. |
| `REQ-IAR-010` | parity and integrity checks | canonical template, self-hosted copy, and schema-2 lock | Supported self-upgrade produces exact managed parity and `doctor` reports no integrity failure. |
| `REQ-IAR-010` | human inspection | router plus four focused policies | No provenance, authority, gate, traceability, or lifecycle obligation is lost or assigned ambiguously. |

## Acceptance scenarios

- An agent reaches concise verification and release invariants and can directly locate the complete ordered workflow.
- A fresh installation receives the refined router and unchanged focused policies.
- An unchanged prior installation upgrades transactionally to the refined router.
- A customized or malformed router produces the existing fail-closed conflict with no write.

## Property and invariant tests

- Assert the canonical and installed router retain exact-candidate, later-governance-commit, decision-right, and no-external-action meanings.
- Assert the old procedural sentence beginning with candidate-commit sequencing is absent from the router.
- Assert `WORKFLOW.md` still contains `capture-verification`, the assurance transition, `prepare-release`, aggregate coverage, release transition, and separate tagging guidance.
- Assert the router still links all four focused policy modules directly.
- Assert deterministic and idempotent plan/apply behavior for the managed-template update.

## Static and architecture checks

- Run formal artifact validation and inspect relation coverage.
- Run `doctor`, phase-appropriate preflight, CLI help, and deterministic dashboard generation.
- Compare canonical standard installation, self-hosted operational files, and lock entries through existing parity checks.
- Confirm no policy-module body, command implementation, artifact schema, or historical record changed outside the authorized surface.

## Security and privacy checks

Re-run managed-marker, customized-content, lock-integrity, and no-partial-write upgrade cases. Confirm no new shell interpolation, network behavior, external side effect, or authority transition is introduced.

## Performance and resilience checks

Run the full unit suite on Python 3.11 and the local supported runtime. No dedicated performance threshold is required for a bounded managed-text change.

## Manual assessments

- Compare router and workflow side by side and confirm ordered procedure has one owner.
- Confirm the concise wording remains sufficient to stop an agent from treating preparation as approval or from binding a record to its own governance commit.
- Confirm repository-owner documents remain non-authoritative and historical IAR artifacts remain unchanged.

## Evidence retention

Retain exact commands, runtimes, focused and full-suite results, changed paths, upgrade fixture outcomes, integrity and parity results, deterministic dashboard snapshots, inspection conclusions, deviations, and residual risks under `WO-IAR-002`.

## Residual uncertainty

Structural and textual checks cannot prove an actor followed the route or interpreted concise prose correctly. Accountable review remains necessary to assess semantic completeness.
