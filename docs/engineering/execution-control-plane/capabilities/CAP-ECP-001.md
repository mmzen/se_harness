+++
id = "CAP-ECP-001"
type = "capability"
title = "An agent obtains its complete execution context in one call and works against a Git-derived, enforced change set"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
derives_from = ["INT-ECP-001"]
+++

# Capability: An agent obtains its complete execution context in one call and works against a Git-derived, enforced change set

## Actor and need

A coding agent executing a work order under the managed harness, on any
host. Today it composes its context from three commands and inference
(`focus`, `preflight`, and a `check` invocation it must choose), reads a
twelve-file manifest of about 12.4k tokens of which 30% is repository-generic,
recites the changed-path set by hand (twenty-two paths on `WO-REB-027`),
authors its own evidence prose, allocates identifiers by inspecting the
current tree only, and types the pull-request trailer that CI relies on
(2026-08 agentic execution review, sections 3 and 6). The agent needs the
harness to hold that state and to derive the change set from the one source
it cannot misreport, the Git difference.

Engineering, assurance, and release owners need the restitution an agent
returns to prove which paths changed, not only which fields were rendered
(`se_harness/workflow_result.py:174-207`). CI needs to enforce scope on every
pull request rather than only when a trailer is volunteered
(`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`).

## Capability statement

`A coding agent can obtain, in one evaluator call, the selected artifact and
its state, the governing chain, the declared execution scope, the phase
reading set, the exact next command, and any pending decision, and can then
hand off work whose change set the harness derives from Git, whose evidence
packet and identifiers the harness writes, and whose scope the pull-request
gate enforces on every pull-request event.`

## Boundaries

The capability computes, derives, writes packets, and enforces at the
pull-request gate. It does not approve, start, complete, verify, or release
anything; it does not select a work order for the agent; it does not change
what a state means or who decides it; it does not provide a session store or
multi-agent orchestration. Enforcement holds for changes that reach `main`
through a pull request; a repository that merges without pull requests is
outside the guarantee. The reading set stays the router and the card plus
what the call returns; the owner narrative in `AGENTS.md` is not part of the
mandatory read.

## Outcomes

- The state an agent carries in its context shrinks to the work-order
  identifier; selection, scope, snapshot digest, next command, and record
  identifiers are returned or written by the harness.
- The live `WEX210` self-loop (review section 3, failure and retry) cannot
  occur, because the next command is returned rather than inferred.
- A change set is complete by construction, including untracked files, and
  its sorted paths are inside the restitution digest, so identical digests
  cannot cover different change sets.
- Handoff evidence survives a merge on an unrelated chain, because the
  snapshot it binds covers the governing chain and dependencies only
  (review section 5, weakness 16).
- Any path outside the declared scope fails the required pull-request check,
  whether or not the agent typed a trailer.
- The mandatory reading set for a phase drops the owner narrative and
  carries a generated command block of at most 2048 bytes.

## Candidate requirements

`REQ-ECP-001`, `REQ-ECP-002`, `REQ-ECP-003`, `REQ-ECP-004`, `REQ-ECP-005`,
`REQ-ECP-006`, `REQ-ECP-007`, `REQ-ECP-015`, `REQ-ECP-016`.
