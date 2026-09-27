+++
id = "ADR-IAR-011"
type = "adr"
title = "Use an injected entry with action-selected procedures"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"

[relations]
decides = ["ARCH-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "technical-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Use an injected entry with action-selected procedures

## Status

Proposed. This record formalizes the reviewed direction; no lifecycle approval
has been applied.

## Context and drivers

The review source has 58 headings, 31 main steps and about 21,900 whitespace
words. Injecting it in full burdens every task. A Markdown split alone does not
help if manifests and skills still require the whole policy collection.
AGENTS.md must return entirely to its repository owner.

## Considered options

1. Inject the full consolidated document. Simple distribution, but every task
   receives all procedures and maintenance detail. This misses the context goal.
2. Keep the managed AGENTS gate and split only the guides. This reuses current
   entry behavior, but misses owner-only AGENTS and automatic root delivery.
3. Inject one compact root and discover procedures from task triggers and
   evaluator-selected identifiers. This needs a versioned mapping, installer
   migration and host qualification, while preserving one lifecycle evaluator.

## Decision

Choose option 3. Use the 26-file allocation in SPEC-IAR-014. Keep always-applicable
rules in the root, detailed rules in one canonical guide, and exact prerequisites
at their action points. Use thin host adapters for the same repository content.
Treat advertised startup and compaction support as behavior that needs evidence.

## Consequences

Agents can see what to read without scanning every file. Owners regain AGENTS.md.
More files require link and coverage checks. Existing guide customizations and
recognized fragments need safe migration. Unsupported hosts require an explicit
limitation; restoring the old managed gate would contradict this decision.

Lifecycle rules and external-action authority do not move into adapters or prose.
The future release and this repository's adoption are separate governed actions.

## Validation

Use VER-IAR-014 for complete procedure coverage, actual reading sets, native host
traces, no duplicated lifecycle computation, and owner-content preservation.
