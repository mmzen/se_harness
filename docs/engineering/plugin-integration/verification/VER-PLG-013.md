+++
id = "VER-PLG-013"
type = "verification"
title = "Fresh repair and explicit repository upgrade"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-022", "REQ-PLG-023"]
+++

# Verification Contract: Fresh repair and explicit repository upgrade

## Independence

Expected outcomes derive from SPEC-PLG-013 and selected requirements, never candidate output. The assurance owner reviews observations independently.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-022 | test, inspection | Cases 1, 2; PLG-MNT-001–004 | Only verified fresh environments become active; failure preserves previous selection. |
| REQ-PLG-023 | test, inspection | Cases 3, 4; PLG-MNT-005, 006 | Repository version changes require the authorized existing installer procedure. |

## Acceptance scenarios

1. Provided Python prepares an empty replacement before selecting it.
2. Missing Python, install failure and identity mismatch preserve the previous usable selection.
3. Plugin update/removal leaves the project lock and governance unchanged.
4. Authorized upgrade preserves owner content and refuses conflicts.

## Property and invariant tests

Assert refusals and prohibited effects directly.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Run instruction/helper fixtures on Windows and Linux with provided Python 3.11+ and released evaluator 0.16.0. Production host coverage belongs to VER-PLG-015.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-013/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
