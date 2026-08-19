+++
id = "VER-RLO-003"
type = "verification"
title = "Verify repository maintenance-line reconciliation"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
verifies = ["REQ-RLO-012"]
+++

# Verification Contract: Verify repository maintenance-line reconciliation

## Independence

Verification derives expected branch names and state transitions from controlled release fixtures rather than calling implementation derivation. Workflow structure is parsed independently. Production GitHub refs, tags, releases, packages, and Pages are not mutated as implementation evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-012 | workflow policy, isolated state fixtures, boundary inspection | absent, equal, descendant, behind, diverged, concurrent-create, malformed/API failure, one-input and portable-surface checks | canonical line is created once or accepted unchanged only when it contains the candidate; conflicts fail unchanged; no portable behavior changes |

## Acceptance scenarios

Executable scenarios are retained in `acceptance/maintenance-line-reconciliation.feature` and mapped to automated tests in retained evidence.

## Property and invariant tests

- `MAJOR.MINOR.PATCH` always derives exactly `release/MAJOR.MINOR`.
- No operator input controls the branch name.
- An absent ref is created at exactly the candidate.
- Any existing compatible ref receives zero update/delete calls.
- Any incompatible or malformed state receives zero mutation calls.
- Replaying the same successful transaction is idempotent.
- The candidate must be equal to or an ancestor of the existing tip.

## Static and architecture checks

- Strict YAML parsing confirms exactly one required `release_record` input.
- The reconciliation step follows exact GitHub Release verification and precedes successful completion of the GitHub stage.
- Only the existing GitHub job has contents-write authority; no action, secret, PAT, environment, or candidate checkout is added.
- Changed-path and package/template inspection confirm no `se_harness/`, `templates/repository/standard/`, managed consumer workflow, validator, or lock mutation.
- The domain model validates with no new structural, governance, or policy errors.

## Security and privacy checks

Treat version, commit IDs, API JSON, ref types, comparison state, and concurrency outcomes as untrusted. Verify structural JSON generation, full commit validation, derived safe refs, fail-closed unknown states, and absence of credential output.

## Performance and resilience checks

Bound API calls per reconciliation, prohibit polling loops, simulate lookup/create/compare failures, and prove a later exact replay can continue after partial GitHub success.

## Manual assessments

- The repository owner confirms automatic establishment of every new `MAJOR.MINOR` line is the intended local support policy.
- The release owner confirms the one-input operator flow remains simpler than a separate branch action.
- The technical owner confirms the portable boundary from `ADR-RLO-002` is unchanged.

## Evidence retention

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-003-verification.md` with changed paths, fixture/state matrix, exact workflow assertions, test commands and counts, formal validation, portable-surface inventory, warnings, residual risks, and explicit production actions not performed.

## Residual uncertainty

Fixture and static tests cannot prove future GitHub API availability, branch-rule configuration, or repository administrator policy. The first separately authorized production release after merge is the operational confirmation; a refusal remains safe and replayable.

## Approval

Approved as an independent evidence contract by the accountable repository owner on 2026-08-19 through the statement `go implement`. This does not verify an implementation candidate.
