+++
id = "VER-ECP-001"
type = "verification"
title = "Independent evidence for the next command, Git-derived change sets, the trimmed manifest, and the chain-scoped snapshot"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-ECP-001", "REQ-ECP-002", "REQ-ECP-015", "REQ-ECP-016"]
+++

# Verification Contract: Independent evidence for the next command, Git-derived change sets, the trimmed manifest, and the chain-scoped snapshot

## Independence

Expected behaviour derives from the four requirement statements and the
`ECP-NXT-`, `ECP-CHG-`, `ECP-MAN-`, and `ECP-SNP-` rules of `SPEC-ECP-001`,
read against `ARCH-ECP-001` and the proposed outcome of `ADR-ECP-001`.
Fixtures (temporary repositories, expected JSON results, expected manifests,
expected digests) are written from the requirement text before any candidate
run. No expected value is copied from candidate output. The Git differences
used as oracles are produced by `git diff --name-only` and
`git ls-files --others --exclude-standard` run by the test, never by the code
under test. Identity, graph, focus, and preflight readings come from the exact
released evaluator, se-harness 0.7.1, installed outside the checkout; the
candidate is exercised only through its own test suite and, for read-only
commands, the in-tree module.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-001` one call returns the complete context | test: `next --json` over every work-order, VREC, and RLS state in the state table; equality against `focus --json`, `preflight --json`, and `select_current_step` | temporary repository per state; explicit `--artifact` and default selection; no selectable artifact | one schema-2 result carries `selected` (id and status), `governing_chain`, `execution_scope.paths`, `reading_manifest`, `next.command_or_response` with a concrete argv, and `decision_required`; each field equals the corresponding output of the composed commands at the same snapshot; the no-selection case is a blocked result with an escalation, never an exception |
| `REQ-ECP-002` change set derived from Git | test: `check --from-git <base>` against a hand-built working tree | modified tracked file; deleted tracked file; renamed file; untracked file; ignored file; path outside scope; `<base>` not a commit | derived set equals `diff(base, worktree) + untracked - ignored` with the deletion and both rename sides present; `QGP-G4I-PATHS` fails on the outside path; an unresolvable base is a fail-closed `not_assessable` naming the base; `--from-git` combined with `--changed-path` is refused |
| `REQ-ECP-015` generated command block, not the narrative | test: `preflight --phase start --json` manifest; byte measurement of the emitted block | owner region carrying 6,000 bytes of narrative plus the managed command block; block grown past 2048 bytes | the manifest names the generated command block and no other part of `AGENTS.md`; the block is at most 2048 bytes; the oversize block fails preflight with a coded diagnostic and a byte count |
| `REQ-ECP-016` chain-scoped snapshot | test: `review_evidence_available` digest; edit outside the chain; edit inside the chain | evidence bound at snapshot S; an unrelated domain's requirement edited; a governing requirement edited | the digest after the unrelated edit equals S and the predicate stays `pass`; the digest after the chain edit differs from S and the predicate fails naming both digests; the digest covers the selected artifact, its governing chain, and its declared dependencies only, as enumerated by the test from the graph |

## Acceptance scenarios

### Scenario 1: next equals the composition it replaces

For every state in the state table, build a minimal repository and run
`next --json`, `focus --json`, and `preflight --json` at the same snapshot.
Assert the projected fields are equal field by field and that
`next.command_or_response` is never the command that was just evaluated.

### Scenario 2: next on the state that self-looped

Reproduce the implemented work order that today returns `WEX210` with
"rerun the same command" as the corrective (the 2026-08 agentic execution
review, `docs/notes/agentic-execution-review-2026-08.md:143-148`). Assert
`next` returns `pre-action --procedure PROC-DELIVERY-SELECT` and no
`WEX210`.

### Scenario 3: Git is the change set

Modify, delete, rename, add untracked, and add ignored files in a temporary
repository whose work order scopes only some of them. Run
`check --artifact WO --checkpoint handoff --from-git <base>`. Assert the
derived set and assert `QGP-G4I-PATHS` fails on the out-of-scope path with
`WEX201` naming it.

### Scenario 4: failure path, unresolvable base

Run `check --from-git no-such-ref`. Assert the result is blocked,
`QGP-G4I-COMPLETE` is `not_assessable`, the diagnostic names the ref, and no
gate reports `pass`.

### Scenario 5: failure path, mixed declaration

Run `check --from-git HEAD --changed-path x`. Assert refusal with one coded
diagnostic and no gate evaluation.

### Scenario 6: manifest excludes the narrative

Render the owner region with a 6,000-byte narrative and the managed block.
Run start preflight. Assert the manifest entry for `AGENTS.md` is the block
only, its byte count is at most 2048, and no narrative byte is listed.

### Scenario 7: failure path, oversize block

Grow the block to 2049 bytes. Assert preflight fails with the byte count.

### Scenario 8: merge elsewhere does not invalidate handoff evidence

Bind evidence to a work order, then edit a requirement in a different domain.
Assert `review_evidence_available` still passes. Edit the work order's own
governing requirement. Assert it fails and names both digests.

## Property and invariant tests

- For random subsets of a fixture tree, the derived change set is a pure
  function of `(base, worktree)`: two runs yield equal sorted sets.
- The chain-scoped digest is invariant under edits to any artifact outside
  the enumerated chain and dependency closure, and sensitive to every
  artifact inside it (one edit per member, each must move the digest).
- `next` is idempotent: two consecutive runs without intervening edits yield
  byte-identical JSON.

## Static and architecture checks

- `grep -n "rerun the same command" se_harness/workflow_contract.json templates/repository/standard/docs/engineering/WORKFLOW.json`
  returns nothing (today it matches; review section 3, `WORKFLOW.json:83`).
- `READING_PATHS` in `se_harness/preflight.py` contains no whole-file
  `AGENTS.md` entry (today it does, `se_harness/preflight.py:53-57`).
- `next` has one implementation and calls `select_rule`; no second rule
  table is introduced.

## Security and privacy checks

- The derived change set never includes paths outside the repository root;
  a symlink pointing outside is reported, not followed.
- `next` performs no write; a read-only filesystem yields the same result.

## Performance and resilience checks

- `next` on this repository completes within twice the wall time of `focus`
  at the same snapshot, measured on both platforms and recorded.

## Manual assessments

None beyond the reviewer reading of Scenario 2's rendered corrective.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/<WO-ID>/`: the
commands, per-scenario JSON results, the fixture trees as listings, the
measured byte counts, both digests of Scenario 8, and per-platform test
figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows with figures labelled
per platform. Graph, focus, preflight, and integrity readings are taken with
the exact released evaluator, se-harness 0.7.1, installed outside the
checkout. No lifecycle state, gate predicate, or decision right is changed by
the work this contract covers.

## Residual uncertainty

Rename detection depends on Git's similarity heuristic; the test pins
`--find-renames` behaviour to what the rule states and records the Git
version. The 2048-byte bound is a requirement figure and is not re-derived
here.
