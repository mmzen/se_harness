+++
id = "VER-PLG-016"
type = "verification"
title = "Truthful released installation guidance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-027"]
+++

# Verification Contract: Truthful released installation guidance

## Independence

Expected outcomes derive from SPEC-PLG-016 and selected requirements, never candidate output. The assurance owner reviews observations independently.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-027 | test, inspection | Cases 1–4; PLG-DOC-001–006 | Commands, prerequisites and activation claims match the qualified release; future behavior remains prospective. |

## Acceptance scenarios

1. An operator follows the qualified release route with provided Python and observes setup/activation separately.
2. Missing Python produces install/provide guidance and no repository initialization.
3. Unavailable releases and untested hosts remain prospective or unsupported.
4. Version mismatch, recovery and local-hook authority limits match the released behavior.

## Property and invariant tests

Assert refusals and prohibited effects directly.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Rehearse the qualified release route on its accepted host/platform matrix. Record host, Python and exact released-evaluator versions. Use evaluator 0.16.0 for baseline documentation checks.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-016/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
