+++
id = "INT-IAR-001"
type = "intent"
title = "Make harness instructions simple, adaptable, and enforceable"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make harness instructions simple, adaptable, and enforceable

## Problem

The installed instruction route currently repeats navigation and policy across `AGENTS.md`, `ENGINEERING_HARNESS.md`, and `docs/engineering/README.md`, while focused managed files such as `WORKFLOW.md` are reached only through a secondary index. Ownership is also difficult to infer: some files must be safely customized by a repository owner, while other files must remain managed and integrity-protected. The result is avoidable reading, apparent orphaning, ambiguous precedence, and an enforcement boundary that depends too heavily on agents following prose.

## Desired outcome

A new or existing repository receives one tool-neutral harness entry route, retains its repository-specific agent instructions, exposes focused policy exactly where it is needed, and blocks implementation readiness when the installed harness, repository context, artifact graph, or selected work authorization is invalid. Required CI evaluates the repository with a checker that is independent from the candidate changes.

## Success indicators

- Supported agent entry files converge on one managed router without duplicating its instructions.
- Repository-owned content survives installation and upgrade byte-for-byte outside managed fragments.
- Every managed policy module is directly discoverable from the router and has an explicit decision point.
- One read-only command reports whether a selected approved work order is ready for implementation and lists its complete governing chain.
- A candidate change cannot make a required check pass merely by changing its checked-in validator or workflow payload.
- Human approval, verification, and release authority remain distinct from instructions and automation.

## Authority boundary

This intent authorizes no implementation, file migration, work-order approval, verification transition, commit, push, pull request, release, tag, publication, or deployment.
