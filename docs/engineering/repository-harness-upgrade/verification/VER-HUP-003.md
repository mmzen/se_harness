+++
id = "VER-HUP-003"
type = "verification"
title = "Verify post-adoption self-hosting compatibility"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
verifies = ["REQ-HUP-007"]
+++

# Verification Contract: Verify post-adoption self-hosting compatibility

## Independence and authority

The immutable public 0.6.0 environment remains the only root governor. Source
tests may import checkout code as an explicitly labelled candidate-source lane,
but cannot validate, mutate, or authorize the installed root.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
|---|---|---|
| REQ-HUP-007 | exact diff review | only the eight implementation paths and HUP-003 governance/evidence paths change beyond the already retained HUP-002 surface |
| REQ-HUP-007 | focused regression | all ten previously failing test IDs pass without changing production validator or canonical template bytes |
| REQ-HUP-007 | complete source suite | 452 tests pass with only the seven declared platform skips, unless discovery legitimately adds tests |
| REQ-HUP-007 | released-root gates | identity, doctor, validate, preflight, inspect, dashboard, distribution validation, and no-op upgrade remain passing |

## Required assertions

- Installed/package equality is exact for the adopted 0.6.0 policies and is not
  used as proof that runtime roles share an origin.
- Released-evaluator origins remain external and candidate-source origins remain
  inside the checkout.
- Fragment-managed hashes remain unchanged when owner content changes.
- `REPOSITORY_CONTEXT.md` remains byte-identical and absent from the lock.
- Temporary release fixtures carry canonical evaluator evidence matching their
  schema-3 lock; missing or corrupt evidence tests continue to fail closed.
- The predecessor-assessment workflow remains pinned, read-only, credential
  free, and unchanged.
- No credential, network, publisher, release, deployment, issue, or Git-history
  action occurs.

## Security and regression checks

Review the complete diff for relaxed negative assertions. Scan retained evidence
for host paths and secrets. Run `git diff --check` and prove no change under
`se_harness/`, `templates/repository/standard/`, managed root content, release
records, package metadata, repository release tools, publisher, or Pages paths.

## Evidence retention

Retain `WO-HUP-003-verification.md` with focused and complete-suite counts,
fixture evidence identities, owner-region size, role origins, scope audit,
governor gates, warnings, and every unperformed external or lifecycle action.
