+++
id = "ADR-IAR-008"
type = "adr"
title = "Project existing validation and Explorer observations into inspection"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
decides = ["ARCH-IAR-008"]
+++

# ADR: Project existing validation and Explorer observations into inspection

## Status

Accepted on 2026-08-15 through the repository owner's instruction `go for implementation`.

## Context

Operators need a practical terminal view of repository attention. Validation already owns gate findings and assessment planes, while Harness Explorer owns additional derived consistency observations and lifecycle context. A new command could either reuse those facts or introduce another interpretation layer.

## Decision drivers

- Keep one formal validator and one set of Explorer finding rules.
- Make the command useful before inventing configurable inspection policy.
- Preserve a clear boundary between observation and accountable authority.
- Keep output deterministic, testable, offline, and Python 3.11+ standard-library-only.
- Avoid presenting repository-local execution as independent governor assurance.

## Considered options

1. Add pending, orphan, and maintenance heuristics directly to `validate`. Rejected because optional operational attention would become entangled with gate semantics.
2. Implement a separate inspection parser and rule engine. Rejected because it would duplicate artifact interpretation and allow validator, Explorer, and inspection to disagree.
3. Make the CLI scrape generated dashboard HTML. Rejected because presentation markup is not a stable data interface and dashboard generation writes derived files.
4. Reuse the in-memory Explorer snapshot, preserve its validator diagnostics and derived findings, and add only mechanical lifecycle queues and renderers. Preferred because it is read-only, consistent, and bounded.

## Decision

Choose option 4. `inspect` obtains the existing snapshot without writing dashboard output. It preserves existing diagnostics and findings, derives only explicitly specified status-based queues, and renders a compact human report or versioned JSON.

Inspection exits zero when a report is successfully produced, even if that report embeds failed formal validation or attention items. This prevents the observational command from becoming a second gate; `validate` remains the command whose exit status expresses graph validity.

The report explicitly labels itself derived and repository-local. Future independent-governor inspection or new finding semantics require separate authority.

## Consequences

- Validator and Explorer changes automatically become visible to inspection through their existing contracts.
- Snapshot compatibility becomes an explicit dependency tested by inspection.
- Human and agent users receive one terminal attention view without generating HTML.
- Some current Explorer observations may be noisy; inspection preserves them rather than silently redefining them.
- The first increment cannot apply repository-specific thresholds or remediation.

## Rejected implications

This decision does not authorize a health score, new validation rule, new orphan definition, aging policy, automatic lifecycle transition, dashboard rewrite, released-governor promotion, or resolution of GitHub issue #46.
