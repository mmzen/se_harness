+++
id = "ADR-RLO-003"
type = "adr"
title = "Automatic repository maintenance-line reconciliation"
status = "approved"
owners = ["release-owner", "engineering-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
decides = ["ARCH-RLO-003"]
+++

# ADR: Automatic repository maintenance-line reconciliation

## Status

Accepted.

## Context

The SE Harness repository promises a trunk-based model with `release/x.y` branches for supported lines, while its repository-specific release workflow does not create them. Manual creation is easy to omit or base incorrectly. The correction must not leak repository branching policy into the portable governance product.

## Decision drivers

- Complete the repository's deterministic one-input release last mile.
- Preserve `main` as the normal integration and new-line release source.
- Preserve one maintenance branch across all patches in a minor line.
- Make reruns safe after partial external success.
- Never rewrite mutable history automatically.
- Keep consumer installation and governance behavior unchanged.

## Considered options

1. Keep branch creation as a documented manual step.
2. Add an operator-supplied branch name or `create_branch` input.
3. Create `release/MAJOR.MINOR.PATCH` for every release.
4. Automatically derive `release/MAJOR.MINOR`, create it at the candidate if absent, and otherwise require candidate containment without moving it.
5. Move the capability into `harnessctl` or the managed consumer workflow.

## Decision

Choose option 4 inside `.github/workflows/publish-pypi.yml` and, if useful for testability, repository-owned `.github` helper code. Run it after the tag and GitHub Release are exact. Reuse the existing job-scoped GitHub token and contents-write permission. Treat an equal or descendant branch tip as replay-compatible; fail closed on unrelated or behind history. Do not add workflow inputs and never update an existing ref.

This is explicitly a policy of `mmzen/se_harness`, not a governance-tool capability or consumer requirement.

## Consequences

- Positive: each release deterministically establishes its maintenance line without another operator command.
- Positive: exact reruns and advanced maintenance branches are accepted without mutation.
- Positive: the portable/product boundary established by `ADR-RLO-002` remains intact.
- Negative: every new release line is treated as supported until repository policy is changed.
- Negative: a conflicting pre-existing canonical branch blocks downstream promotion and requires human disposition.
- Operational: historical per-patch branch names are untouched; canonical lines begin with later releases or separate authorized administration.
- Security: no new credential exists, but the existing contents-write stage gains one bounded mutable-ref operation.
- Migration: no consumer or package upgrade behavior changes.

## Validation

Test deterministic derivation, create, compatible replay, advanced-line replay, conflict refusal, concurrent creation, malformed responses, permissions, ordering, one-input preservation, and absence of portable-file changes. A non-production fixture or static API harness supplies write-path evidence; implementation verification must not create a real branch or release.

## Approval

Accepted by the accountable repository owner on 2026-08-19 through the statement `go implement` as part of the complete RLO-003 packet.
