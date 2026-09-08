+++
id = "VER-PLG-015"
type = "verification"
title = "Host qualification and measured workflow overhead"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-025", "REQ-PLG-026"]
+++

# Verification Contract: Host qualification and measured workflow overhead

## Independence

Expected outcomes derive from SPEC-PLG-015 and selected requirements, never candidate output. The assurance owner reviews observations independently.

DEC-PLG-005 blocks this contract's approval. Approval requires a positive qualification profile; a preview-only decision requires appropriate artifact disposition or amendment instead.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-025 | test, inspection | Cases 1, 2, 4, 5; PLG-QLF-001, 002, 006 | Every combination in the approved positive profile has passing reproducible evidence; missing coverage fails. |
| REQ-PLG-026 | test, inspection | Cases 3–5; PLG-QLF-003–006 | Measurements and conditions are complete; the approved positive profile's criteria are met. |

## Acceptance scenarios

1. Exercise every selected operation: setup, missing Python, sessions/compaction, authoring, work start, evidence, refusal, and maintenance.
2. Record exact host/platform/Python/plugin/evaluator versions and repeatable inputs.
3. Separate startup, each tool check, total duration and prompts; record cold/warm conditions and repetitions.
4. Missing coverage or samples remain visible; untested combinations gain no support claim.
5. A closed decision selecting preview-only cannot produce qualification acceptance; the governing artifacts require appropriate disposition or amendment.

## Property and invariant tests

Assert refusals and prohibited effects directly.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Exercise each Codex/Claude Code platform in DEC-PLG-005's approved positive profile. Record Python, host and released-evaluator identities, starting with evaluator 0.16.0 fixtures. Parser checks prove no host integration.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-015/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
