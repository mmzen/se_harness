+++
id = "INT-HUP-004"
type = "intent"
title = "Adopt released se-harness 0.7.0 as the repository governor"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
+++

# Intent: Adopt released se-harness 0.7.0 as the repository governor

## Problem

The repository's standard root is governed by exact public 0.6.0 under a
schema-3 lock. `se-harness` 0.7.0 was published on 2026-08-27 (`RLS-SEH-015`,
tag `v0.7.0`, candidate `374554d`), and it carries the directive surface, the
authoring policy, the technical-communication route, the agent skills, the
`qualify` and `migrate` namespaces, and the release-unit predicate that this
repository already develops against. Until the root advances, every
lifecycle act is judged by an evaluator that predates the rules the graph is
written for, and `doctor` from the candidate reports skew on forty-six
managed files.

## Desired outcomes

- The root lock names exact public 0.7.0, installed from the wheel whose
  digest `RLS-SEH-015` binds, with its managed files, templates, policies and
  skills exactly as 0.7.0 distributes them.
- The complete graph validates under 0.7.0 with zero errors, directly and
  without any compatibility view.
- Every managed CI gate selects 0.7.0.
- Nothing else moves: product source and templates, versions, release
  records, tags, publication and Pages workflows, maintenance lines.

## Non-goals

Changing the candidate product beyond its development version identity;
re-releasing; retiring the `accept-candidate` bootstrap exception; acting on
the RC-070 issues; adopting a version other than exact public 0.7.0.

## Immutable identity

Wheel `se_harness-0.7.0-py3-none-any.whl`, SHA-256
`e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3`; installed
payload SHA-256
`26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9`
(`se-harness-installed-payload-v1`); GitHub Release `v0.7.0` and PyPI carry
the same wheel.

## Approval boundary

Approval of this packet authorizes drafting and review only. The transaction
runs under `WO-HUP-006` after its own approval and start; commit, push, pull
request, verification and merge stay separate acts.
