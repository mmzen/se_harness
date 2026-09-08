+++
id = "VER-PLG-014"
type = "verification"
title = "Optional helpers with enforced read-only boundaries"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-024"]
+++

# Verification Contract: Optional helpers with enforced read-only boundaries

## Independence

Expected outcomes derive from SPEC-PLG-014 and selected requirements, never candidate output. The assurance owner reviews observations independently.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-024 | test, inspection | Cases 1–4; PLG-HLP-001–006 | Scoped read-only findings and enforced prohibitions hold; unsupported hosts delegate nothing. |

## Acceptance scenarios

1. Bounded investigation returns sources and uncertainty; unrelated findings do not become blockers.
2. Host controls deny file mutation, privileged tools, credential access and publication.
3. Unsupported registration/restrictions select the main-agent fallback.
4. Findings cannot approve a VREC or replace the assurance owner.

## Property and invariant tests

Assert refusals and prohibited effects directly.

## Static and architecture checks

Compare declared paths, command arguments and permission boundaries.

## Security and privacy checks

Use disposable fixtures; retain no credentials.

## Performance and resilience checks

Record interruptions; overhead acceptance belongs to SPEC-PLG-015.

## Manual assessments

Record tested Codex/Claude Code versions on Windows/Linux using released evaluator 0.16.0. Demonstrate restrictions or the no-delegation fallback; unsupported combinations gain no support claim.

## Evidence retention

Retain commands, inputs, outcomes and failures under `docs/engineering/plugin-integration/evidence/WO-PLG-014/`. This draft claims no execution or passing result.

## Residual uncertainty

Untested combinations remain unqualified. Assurance remains a separate decision.
