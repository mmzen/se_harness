+++
id = "REQ-IAR-016"
type = "requirement"
title = "Inspect repository attention without creating authority"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN an operator requests repository inspection, SE Harness SHALL produce a deterministic read-only attention report from existing validation, lifecycle, and Explorer observations without changing gates or exercising accountable authority."
verification_method = "Automated command, projection, determinism, no-write, distribution, and regression tests"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Inspect repository attention without creating authority

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `go for implementation` as part of the complete `IAR-008` packet. Clarified on 2026-08-15 through the separately governed `IAR-009` approval `ok i approve`: the original exclusion concerns free-form recommendations and automatic remediation, not the closed non-authoritative suggestion projection defined by `REQ-IAR-017` and `SPEC-IAR-009`.

## Problem

`harnessctl validate` answers whether the formal graph satisfies current rules, while Harness Explorer exposes lifecycle and consistency observations visually. An operator who needs a concise terminal answer must currently interpret validator output, generate the dashboard, and manually combine artifact states with derived findings.

The recently implemented assessment planes clarify validation findings but intentionally add no inspection command. A first inspection capability should make existing information actionable without becoming another validator or inventing ambiguous heuristics.

## Required outcome

`harnessctl inspect [TARGET]` produces one deterministic, read-only report that:

- states whether formal validation passed and summarizes the existing assessment planes;
- identifies artifacts awaiting an accountable decision through status `ready`;
- identifies incomplete definitions through status `draft`;
- identifies authorized or active work orders through status `approved` or `in_progress`;
- surfaces existing validator and Harness Explorer findings, including current orphan, stale, evidence, provenance, and maintenance observations;
- distinguishes derived observation from approval, verification, release, and policy authority.

## Acceptance criteria

1. The command supports concise human output and deterministic JSON.
2. Inspection reuses the existing validator and Explorer snapshot projection; it does not duplicate their graph parser or finding rules.
3. Queue membership follows declared artifact type and lifecycle status, with no natural-language inference.
4. Existing finding rule IDs, severity, authority, messages, paths, and artifact references remain unchanged.
5. The command writes no repository or derived-output file and performs no lifecycle transition.
6. Inspection completion is not a validation gate: the report carries formal validity, while `harnessctl validate` retains authoritative pass/fail exit behavior.
7. Repository-controlled execution and derived authority are explicit; the report does not claim independent-governor assurance.
8. No health score, aging deadline, new orphan rule, new policy rule, free-form recommendation, or automatic remediation is introduced. Structured non-authoritative suggestions require their own approved requirement, specification, verification contract, and work order.

## Deferred questions

New orphan semantics, aging thresholds, repository-configurable inspection policy, remediation commands, interactive filtering, and independent evaluator identity remain separately governed follow-on work.

## Authority boundary

Inspection reports observations. It cannot approve an artifact, authorize work, verify a candidate, supersede a record, release software, or waive a validation finding.
