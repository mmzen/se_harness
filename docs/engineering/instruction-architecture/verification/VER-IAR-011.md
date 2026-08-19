+++
id = "VER-IAR-011"
type = "verification"
title = "Verify stage-aware agent lifecycle handoffs"
status = "approved"
owners = ["quality-owner", "assurance-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
verifies = ["REQ-IAR-019"]
+++

# Verification Contract: Verify stage-aware agent lifecycle handoffs

## Lifecycle

Approved on 2026-08-19 through the repository owner's instruction `ok go implement` as the independent evidence contract for `REQ-IAR-019`.

## Independence

Verification reads fresh-install outputs, managed policy files, README examples, and upgrade results rather than importing wording or stage tables from an implementation helper. Expected semantic fields, lifecycle boundaries, accountable roles, and positive and negative examples derive directly from `REQ-IAR-019` and `SPEC-IAR-011`.

Automated tests can prove that the managed guidance is present, consistently distributed, and preserves existing boundaries. They cannot prove that every external language model will follow prose correctly; accountable semantic review remains required.

## Requirement-to-evidence matrix

| Requirement concern | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| mandatory handoff fields | fresh-install router/workflow assertions | installed standard target | all six semantic fields and the conditional alternative rule are discoverable through the managed route |
| stage awareness | focused workflow assertions | draft definition, approved WO, implemented work, clean candidate, ready/verified VREC, ready/released RLS | each state has one bounded primary recommendation and correct accountable role |
| actual identity guidance | exact prose and README assertions | illustrative WO/VREC/RLS/commit handoffs | guidance requires actual known IDs and forbids fabricated values |
| authority separation | positive and negative wording checks | approval, verification, release, tag, publication, and deployment cases | recommendations name required authority and never imply that the action occurred |
| failure and stop behavior | focused policy and example assertions | failed preflight, damaged managed content, missing authority, out-of-scope remediation | state remains unchanged and the handoff recommends bounded remediation or escalation |
| multiple valid paths | README and workflow assertions | verified candidate | primary recommendation and PR/release alternatives expose their distinct authorities |
| responsibility split | router/workflow/agent-gate tests | installed managed route | router states the invariant, workflow owns stage procedure, and AGENTS remains thin |
| Inspector separation | existing inspection contract and regression tests | `harnessctl inspect` human and JSON output | schema, suggestion catalog, `automatic = false`, and no-executable-command boundary remain unchanged |
| public example | bounded README tests | `What this looks like in practice` | examples demonstrate stage-aware responses without exceeding the public entry constraints |
| managed upgrade | unchanged, customized, ambiguous, and damaged fixtures | normal upgrade plan/apply | unchanged content updates transactionally; blocked cases retain no-partial-write behavior |
| integrity and graph | doctor, validation, preflight, parity, and lock checks | self-hosted repository and fresh target | managed content, canonical templates, lock entries, and formal graph agree |

## Acceptance scenarios

1. A draft definition packet handoff recommends accountable review and offers a suggested response containing the actual work-order ID.
2. An approved work-order handoff recommends start preflight and implementation of only the authorized scope.
3. An implemented-work handoff recommends review checks and a separately authorized clean candidate commit.
4. A clean candidate handoff recommends preparing a ready VREC without claiming verification.
5. A ready-VREC handoff names the assurance owner and no automated verification command.
6. A verified-candidate handoff presents pull-request and separately authorized release paths distinctly.
7. A ready-RLS handoff names the release owner and leaves tag and publication actions unperformed.
8. A failed check reports unchanged state and one remediation or escalation path.
9. A multi-stage authorized turn summarizes completed stages and recommends only from the final state reached.
10. Unknown state, ID, or command data is reported as unavailable rather than fabricated.

## Property and invariant tests

- Every listed lifecycle boundary has a recommendation and accountable role.
- Every recommendation that can change repository or external state states whether separate authority is required.
- The router contains the reporting invariant but omits ordered capture, transition, release, and tagging sequences owned by workflow.
- The managed agent gate has exactly one harness destination and does not duplicate the handoff body.
- No test treats successful checks, conversational wording, or a suggested response as lifecycle authority.

## Static and architecture checks

- Confirm root and canonical router/workflow content are synchronized through the supported managed process.
- Confirm package data still includes every changed managed template.
- Confirm `.engineering-harness.lock` uses schema-2 canonical hashes for the changed managed files.
- Confirm `ARCH-IAR-002` and `ADR-IAR-002` remain historical design precedent and are not rewritten merely to implement this packet.
- Confirm no new architecture relation is required unless accountable technical review identifies a new significant structural decision before approval.

## Security and privacy checks

- Examples contain no real credentials, tokens, private URLs, or unsafe shell interpolation.
- Suggested commands use controlled illustrative IDs and do not execute untrusted repository prose.
- Failure examples do not bypass managed integrity, preflight, formal validation, or authority checks.
- Inspector suggestions remain non-executable and automatic action remains false.

## Performance and resilience checks

- Repeated installation and upgrade planning remain deterministic.
- Interrupted or blocked upgrade fixtures retain existing transactional recovery and no-partial-write behavior.
- Full tests pass on Python 3.11 and the local supported runtime without a new runtime dependency.

## Manual assessments

- Accountable reviewers judge whether each stage recommendation is substantively correct and whether the named role matches `DECISION_RIGHTS.md`.
- Reviewers confirm that exact commands are offered only where managed workflow defines a safe command.
- Reviewers confirm that suggested responses cannot be mistaken for decisions already exercised.
- Reviewers confirm the README remains concise and understandable without the formal artifact context.

## Evidence retention

Retain focused and full commands, runtimes, test counts, installed router/workflow excerpts, README assertions, upgrade and lock results, validation and preflight outputs, changed paths, diff hygiene, deviations, and residual risks under `docs/engineering/instruction-architecture/evidence/WO-IAR-011-verification.md`.

## Residual uncertainty

Static instruction tests cannot establish universal coding-agent compliance, correct human judgment, or host-specific permission. Suggested user responses may still be misunderstood outside their surrounding authority wording. Those limits require human review and do not justify automatic actions or machine-readable CLI expansion in this packet.
