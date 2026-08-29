+++
id = "WO-ECP-008"
type = "work_order"
title = "Retire stubbed skills, trim the manifest, scope the handoff snapshot"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the shipped skill set, the preflight reading manifest every agent receives, and the snapshot digest that binds handoff evidence. Later handoff and verification decisions rely on exact candidate behaviour, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/AGENTS.md.fragment",
  "se_harness/preflight.py",
  "se_harness/workflow_compliance.py",
  "docs/notes/agentic-execution-skills-mvp.md",
  "docs/notes/agentic-execution-host-adapters.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-015", "REQ-ECP-016"]
specifications = ["SPEC-ECP-001"]
architecture = ["ARCH-ECP-001", "ADR-ECP-001"]
verification = ["VER-ECP-001"]
+++

# Work Order: Retire stubbed skills, trim the manifest, scope the handoff snapshot

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-014`,
`REQ-ECP-015`, `REQ-ECP-016`, `SPEC-ECP-001`, `SPEC-ECP-007`,
`ARCH-ECP-001`, `ADR-ECP-001`, `VER-ECP-001`, and `VER-ECP-007` are
separate acts by their owners and precede approval of this work order.
This work order follows `WO-ECP-001`, whose `next` result carries the
manifest this work order trims.

## Objective

Cut the mandatory read to what the harness can stand behind. Today the
three writing skills inject a stub client and print
`"evaluator_invoked": false` while their `SKILL.md` says they invoke the
evaluator
(`templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`;
the 2026-08 agentic execution review, section 3); the manifest lists the
whole of `AGENTS.md`, of which 79% is owner narrative
(`se_harness/preflight.py:53-57`; review section 6); and the formal
snapshot digest moves on any artifact edit, so a merge elsewhere
invalidates every branch's handoff evidence (review section 5, weaknesses
6 and 16).

## In scope

Revised 2026-08-29, before any lifecycle event: the retirement of the three
stubbed writing skills (`REQ-ECP-014`, `ECP-SKL-*`) moved to `WO-ECP-006`,
which removes the command those skills name; this work order keeps the
manifest and snapshot items.

- `READING_PATHS` replacing the whole-file `AGENTS.md` entry with the
  generated command block bounded to 2048 bytes; the
  `AGENTS.md.fragment` rendering that block; preflight failing on an
  oversize block, per `ECP-MAN-*`.
- `review_evidence_available` binding to a digest computed over the
  selected artifact, its governing chain, and its declared dependencies
  only, per `ECP-SNP-*`.
- The two notes updated to describe what remains.
- Tests; work-order-keyed evidence.

## Out of scope

- The `next` command and Git-derived change sets (`WO-ECP-001`); evidence
  authoring (`WO-ECP-002`); the root `AGENTS.md`, `CLAUDE.md`, and
  `.agents/`/`.claude/` copies (the template copies are edited); the
  operating card and router; any change to lifecycle states, gate
  predicates, decision rights; any lifecycle transition of any artifact.

## Authorized decision envelope

The implementation agent may decide the block's internal layout within the
byte bound, the dependency-closure traversal order, the packaging check's
diagnostic code, and test names. It may not keep a stubbed skill in the
wheel, list any narrative byte in the manifest, include artifacts outside
the chain closure in the digest, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings.
- Root managed copies are not edited.
- LF line endings; assert bytes against blobs.
- Stage every skill deletion before any preflight or check run;
  `hash_bound.assess` reads index-tracked paths and the skills are
  hash-locked.

## Expected change surface

Two template skill trees (three skills removed), one owner-region fragment,
the preflight manifest, the compliance module's snapshot digest, the
installer's packaging check, two notes, tests, evidence.

## Required verification

Execute `VER-ECP-001` for `REQ-ECP-015` and `REQ-ECP-016` (Scenarios 6 to 8
and the corresponding property, static, and security checks) and
`VER-ECP-007` for `REQ-ECP-014` (Scenarios 5 and 6 and the corresponding
checks), plus the repository-required checks; run the complete suite on
Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-008/`:
the manifest listings for both phases, the block byte count, both digests
from the chain-scope scenario, the subprocess trace of the retained skill,
the wheel `RECORD`, per-platform test figures, and the complete
changed-path set.

## Stop and escalate conditions

Stop if the command block cannot carry every managed command under 2048
bytes, if the chain closure cannot be enumerated from the graph without a
new traceability edge, if the released evaluator refuses the trimmed
manifest at review preflight, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-008 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
