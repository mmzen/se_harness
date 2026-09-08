+++
id = "VER-PLG-011"
type = "verification"
title = "Evidence skill using existing lifecycle procedures"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-019"]
+++

# Verification Contract: Evidence skill using existing lifecycle procedures

## Independence

Expected outcomes derive from SPEC-PLG-011 and selected requirements, never candidate output. The assurance owner reviews observations independently.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-019 | test, inspection | Cases 1–6; PLG-EVD-001–007 | Real results, authorized writes and exact candidate retained; preparation claims no accountable decision. |

## Acceptance scenarios

1. Retain actual successful and failed results, including the exact candidate.
2. Authorized VREC/RLS preparation leaves its later human decision pending.
3. Interrupted preparation inspects existing results before retry; unchanged valid authority adds no duplicate prompt.
4. A local hook pass or supplied owner name does not authorize merge/publication.
5. `check . --artifact WO-... --checkpoint handoff --from-git BASE` writes retained evidence; read-only preflight does not. Missing write authority stops the handoff operation.
6. Dirty-candidate capture fails. Successful required-assurance capture binds the earlier clean committed candidate; a later governance commit retains the VREC without rebinding it.

## Property and invariant tests

Assert refusals and prohibited effects directly. Check candidate and record commit identities independently.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Run instruction/helper fixtures on Windows and Linux with provided Python 3.11+ and released evaluator 0.16.0. Production host coverage belongs to VER-PLG-015.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-011/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
