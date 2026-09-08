+++
id = "VER-PLG-012"
type = "verification"
title = "Retained orientation and explicit operator briefing"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-020", "REQ-PLG-021"]
+++

# Verification Contract: Retained orientation and explicit operator briefing

## Independence

Expected outcomes derive from SPEC-PLG-012 and selected requirements, never candidate output. The assurance owner reviews observations independently.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-020 | test, inspection | Cases 1, 4; PLG-RO-001, 002, 005, 006 | Existing orientation procedure and zero mutation are preserved. |
| REQ-PLG-021 | test, inspection | Cases 2–4; PLG-RO-003–006 | Explicit invocation, protected text and bounded-source contract remain unchanged. |

## Acceptance scenarios

1. Orient with valid/invalid identities; optional projection and explicitly requested preflight retain current behavior.
2. Implicit briefing stays inactive; valid explicit input produces existing schemas.
3. Wrong digest, malformed spans and missing required current state refuse briefing.
4. File, lifecycle, network and credential effect sentinels remain empty.

## Property and invariant tests

Assert refusals and prohibited effects directly.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Run instruction/helper fixtures on Windows and Linux with provided Python 3.11+ and released evaluator 0.16.0. Production host coverage belongs to VER-PLG-015. Isolated retained-skill checks need no live migration.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-012/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
