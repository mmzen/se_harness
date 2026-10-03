+++
id = "REQ-DST-062"
type = "requirement"
title = "Provide durable demonstrator topology headroom"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-10-03"
statement = "WHEN the SE Harness repository acceptance suite evaluates its compact Explorer topology, THE SYSTEM SHALL use a 4,194,304-byte UTF-8 acceptance target while continuing to report the exact observed size."
verification_method = ["test"]
verification_notes = "automated-performance-budget-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Provide durable demonstrator topology headroom

## Rationale

The 524,288-byte repository target was selected when the formal graph was materially smaller. Merged HUP and verification history now produce a valid 539-artifact, 1,944-relation topology of 525,689 bytes. The one-resource progressive design remains sound, but the current-repository acceptance test fails after ordinary governed growth.

A fourfold target provides meaningful headroom for the 0.5.1 recovery and continued governed evolution without returning artifact or evidence bodies to the topology resource.

## Preconditions and trigger

The deterministic progressive dashboard bundle has been generated for the SE Harness repository or an equivalent acceptance fixture, and the current-repository topology acceptance assertion is evaluated.

## Required response

- Compare the compact topology resource against exactly 4,194,304 UTF-8 bytes before compression.
- Report the actual topology bytes, configured target, resource role totals, and `topology_target_exceeded` observation.
- Keep target excess observational for general consumer generation while requiring the SE Harness repository acceptance fixture to remain at or below the target.
- Preserve deterministic serialization so identical accepted inputs and Git history produce identical bytes.

## Failure and boundary behavior

The SE Harness acceptance test fails when its topology exceeds 4,194,304 bytes. Consumer generation continues to report larger valid topology rather than misclassifying the formal graph as invalid. Exceeding this target does not weaken manifest size/digest verification or authorize silent truncation.

## Constraints

- The value is a repository acceptance target, not a universal consumer repository maximum and not an assurance score.
- Measurements remain uncompressed UTF-8 bytes.
- No topology field, relation, finding, readiness input, or provenance observation may be dropped to meet the target.
- The owner explicitly selected the increase from 2 MiB to 4 MiB on 2026-10-03 after the current-repository limit was exceeded. Topology sharding is deferred. A future need beyond 4 MiB requires a new capacity assessment and decision; this amendment authorizes no automatic increase.

## Acceptance examples

### Example: current merged repository

**Given** merged `main` produces a 525,689-byte compact topology,

**When** the updated acceptance suite evaluates it,

**Then** it passes against 4,194,304 bytes and reports both values.

### Example: future target excess

**Given** a future SE Harness topology exceeds 4,194,304 bytes,

**When** repository acceptance runs,

**Then** it fails explicitly without truncating data or invalidating the formal graph.

## Open decisions

The owner authorized exactly 4 MiB on 2026-10-03. Implementation may not choose a different value.

## Manual capacity revision — 2026-10-03

mmzen authorized the 4 MiB target and the bounded manual amendment after reviewing
the two-file correction and the affected definitions. This records the human's
exception to the selected 0.21.0 amendment procedure's unsupported-command stop;
it is not a revision operation performed by harnessctl. Lifecycle states,
original decision history and all noncapacity rules are preserved.

The exact accepted predecessor is the member `docs/engineering/harness-distribution/requirements/REQ-DST-062.md` of
[accepted-predecessors.zip](../evidence/WO-DST-028/accepted-predecessors.zip),
SHA-256 `483ffad85da1f4196ee5fa72e93d72a8844454abf04072b9a02a4c01ac851832`. The
[amendment manifest](../evidence/WO-DST-028/amendment.json) links both versions
and retains the owner's instruction. Earlier work keeps its original Git-bound
definitions and evidence.

The current target is 4,194,304 uncompressed UTF-8 bytes. Measurements and
0.5.0/0.5.1 rollout statements from the earlier amendment describe its historical
context. New work uses selected released 0.21.0 and the checks in VER-DST-030
under WO-DST-028. All other payload budgets, complete topology data, integrity
checks and publication boundaries remain unchanged. RLS-SEH-032's approved
candidate and archives are not amended.
