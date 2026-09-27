+++
id = "CAP-IAR-002"
type = "capability"
title = "Discover harness instructions for the current action"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
ability = "An agent can discover and use the instructions needed for its current action at startup, after compaction, and while continuing governed work."

[relations]
derives_from = ["INT-IAR-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "repository-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Discover harness instructions for the current action

## Actor and need

An agent entering a repository, resuming after compaction, or moving to another
engineering action needs the governing rules and exact next reading location.
The repository owner needs AGENTS.md to contain only owner instructions.

The agent receives a compact harness entry, opens the current procedure, and
reads its required references when their conditions apply. The evaluator still
decides lifecycle legality and the next action.

## Boundary

This is a proposed successor delivery model under INT-IAR-001. It does not
reuse CAP-IAR-001's requirement to route the harness through AGENTS.md.
It does not approve implementation or activate a new installed contract.
The related requirements define observable behavior; SPEC-IAR-014 defines the split.
