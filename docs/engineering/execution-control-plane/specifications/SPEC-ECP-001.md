+++
id = "SPEC-ECP-001"
type = "specification"
title = "The next command, Git-derived change sets, the chain-scoped snapshot, and the trimmed manifest"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
specifies = ["REQ-ECP-001", "REQ-ECP-002", "REQ-ECP-015", "REQ-ECP-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Specification: The next command, Git-derived change sets, the chain-scoped snapshot, and the trimmed manifest

## Scope

This specification defines four contracts over the existing workflow kernel:
a `next` command that projects the complete execution context in one schema-2
result; a `--from-git BASE` change-set source for `check`; a snapshot digest
scoped to the selected artifact's governing chain; and a reading manifest that
carries a generated command block in place of the `AGENTS.md` owner narrative.
It changes no lifecycle state, decision right, or artifact schema. Today the
next step is emitted only after an operation, `focus` gives the decision step
and not the `check` invocation, and no `next` command exists
(`docs/notes/agentic-execution-review-2026-08.md`, section 7, first row).
Changed paths are agent-typed and never compared to `git diff`
(`se_harness/workflow_compliance.py:142-152`, `:316-322`).

## Actors and external systems

- A coding agent runs `next`, `check --from-git`, and `preflight`.
- Git supplies the difference between a base and the working tree and the
  set of untracked, non-ignored files.
- The released evaluator computes every value; the in-tree CLI may run
  read-only projections under the existing read-only rule.
- The managed CI workflow consumes `--from-git` at the pull-request head
  (`SPEC-ECP-003`).

## Terms

- **Execution context:** the tuple (selected artifact, state, governing chain,
  declared execution scope, phase reading manifest, next command, decision
  required) that a fresh agent needs before acting.
- **Base:** any Git revision expression accepted by `git rev-parse --verify`.
- **Change set:** the sorted, normalised, unique relative-path set fed to the
  `QGP-G4I-*` scope predicates.
- **Governing chain:** the closure returned by `project_scope`
  (`se_harness/workflow.py:304`) for the selected artifact: governing ids plus
  dependencies.
- **Formal snapshot digest:** `formal_snapshot_digest`
  (`se_harness/workflow_compliance.py:185`), today computed over every
  validated artifact.
- **Owner region:** the region of `AGENTS.md` outside the managed block.

## Behavioral rules

### The next command

**ECP-NXT-001:** `harnessctl next REPOSITORY [--artifact ID]` returns one
`se-harness-workflow-result-v2` result with `operation.kind = "next"`; when
`--artifact` is absent and exactly one work order is `in_progress`, that work
order is selected, otherwise the result is `blocked` with
`WEX-ECP-001` naming the candidate count.

**ECP-NXT-002:** The result carries an additive top-level `context` object
with exactly these members: `reading_manifest` (ordered list of repository
relative paths), `governing` (the governing chain ids), `declared_paths` (the
normalised `[execution_scope].paths`), `state` (`{"status": STATUS,
"family": FAMILY}` of the selected artifact), `next` (`{"argv": [...],
"procedure_id": ..., "step_id": ...}`), and `decision_required` (`null` or
the schema-2 decision object).

**ECP-NXT-003:** `context.next.argv` equals the argv that
`select_current_step` (`se_harness/workflow_procedures.py:132`) returns for
the rule that `select_rule` (`se_harness/workflow_contract.py:558`) selects at
the current formal snapshot, with every `{artifact_id}` parameter substituted;
`next` holds no private mapping.

**ECP-NXT-004:** For the same selected artifact and snapshot, `context.next.
argv`, `restitution.next`, and `restitution.command_or_response` of `next`
are byte-identical to those of `focus` and of `check` without a
checkpoint-specific argument (`ADS-NXT-003` extended to `next`).

**ECP-NXT-005:** `context.reading_manifest` equals the `reading_manifest`
that `run_preflight` (`se_harness/preflight.py:321`) emits for the phase
implied by the state: `start` for `approved` and `in_progress`, `review` for
`implemented` and later.

**ECP-NXT-006:** `next` writes nothing, requires no prior command, and
succeeds from a clean checkout with only the released evaluator resolvable
from the lock.

**ECP-NXT-007:** `result_sha256` of a `next` result is computed over the
canonical block bytes with the `context` object rendered as an ordered
`Context` section after `Command or response`, so two contexts with different
manifests or scopes never share a digest.

**ECP-NXT-008:** The `WEX210` corrective on a blocked `check --checkpoint
start` for an `implemented` work order names `harnessctl next . --artifact
{artifact_id}`, never the evaluated command (reproduced self-loop,
`docs/notes/agentic-execution-review-2026-08.md`, section 3, "Failure and
retry").

### Git-derived change sets

**ECP-CHG-001:** `check` accepts `--from-git BASE`; it is mutually exclusive
with `--changed-path`, `--changes-complete`, and `--change-manifest`, and
supplying both is `WEX-ECP-002`.

**ECP-CHG-002:** With `--from-git BASE`, the change set is the union of
`git diff --name-only BASE` against the working tree (renamed paths
contribute both names) and `git ls-files --others --exclude-standard`, each
member passed through `normalize_path`
(`se_harness/workflow_compliance.py:71`) and deduplicated by `_unique_paths`
(`:95`).

**ECP-CHG-003:** A `--from-git` change set sets `change_set_complete = true`
and `scope.change_set.source = "git"` in the result; an arguments-sourced set
keeps `source = "arguments"` (`se_harness/workflow_compliance.py:152`).

**ECP-CHG-004:** `--from-git` outside a Git checkout, with a base that
`git rev-parse --verify` rejects, or when either Git command exits non-zero,
blocks with `WEX-ECP-003` naming the base and the Git exit status; no
predicate is evaluated as `pass`.

**ECP-CHG-005:** A change-set member that escapes the repository after
resolution fails with the existing `WEX200`
(`se_harness/workflow_compliance.py:156-165`); the Git source does not bypass
`_validate_changed_targets`.

**ECP-CHG-006:** The schema-2 `scope.changed_paths` list carries the
Git-derived set unchanged, so `result_sha256` binds it (`ECP-DIG-001`).

**ECP-CHG-007** (amendment of 2026-08-28 under `WO-ECP-001`, on the
engineering owner's decision): the selected work order's own artifact path is
admitted to its execution scope by construction when `QGP-G4I-PATHS` is
evaluated, whatever the change-set source. Only `transition` writes that
file, and it is in every Git diff after the work order's own approval and
start, so a rule that scope-checked it would refuse every real work order
under `--from-git`. `scope.declared_paths` in the result continues to carry
only the declared `[execution_scope].paths`.

### Chain-scoped snapshot

**ECP-SNP-001:** `review_evidence_available` binds evidence to
`chain_snapshot_sha256`: `formal_snapshot_digest` evaluated over the selected
artifact and the artifacts in `scope.governing` and `scope.dependencies`
only, in id order.

**ECP-SNP-002:** The schema-2 `compliance` object carries both
`formal_snapshot_sha256` (unchanged, whole tree) and
`chain_snapshot_sha256`; only the latter is compared to an evidence packet.

**ECP-SNP-003:** An artifact edit outside the chain changes
`formal_snapshot_sha256` and leaves `chain_snapshot_sha256` unchanged; a
conformance test asserts both facts on one fixture.

**ECP-SNP-004:** An evidence packet whose header carries only the legacy
whole-tree digest is accepted for one release when that digest equals the
current `formal_snapshot_sha256`, with warning `W-ECP-001`.

### Trimmed reading manifest

**ECP-MAN-001:** The phase reading manifest lists `AGENTS.md` only through the
generated file `docs/engineering/AGENTS_COMMANDS.md`, a managed file rendered
by the installer from the managed block's command list and managed-path list.

**ECP-MAN-002:** `AGENTS_COMMANDS.md` is at most 2048 bytes of UTF-8; the
installer refuses to render a larger block with `WEX-ECP-004`, and a
conformance test regenerates and compares bytes.

**ECP-MAN-003:** The owner narrative of `AGENTS.md` appears in no reading
manifest; `preflight` lists it under `routed_policies`, which carries no
reading obligation (`ADS-RDM-003`).

**ECP-MAN-004:** The manifest stays closed as `ADS-RDM-001` defines it, with
`AGENTS_COMMANDS.md` replacing the owner-region command file.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-001 | ECP-NXT-001 to ECP-NXT-008 |
| REQ-ECP-002 | ECP-CHG-001 to ECP-CHG-006 |
| REQ-ECP-015 | ECP-MAN-001 to ECP-MAN-004 |
| REQ-ECP-016 | ECP-SNP-001 to ECP-SNP-004 |

## Inputs and outputs

Inputs: `next REPOSITORY [--artifact ID] [--json]`; `check ...
--from-git BASE`; the existing `preflight` arguments. Outputs: schema-2
results with the additive `context` object, `scope.change_set.source`, and
`compliance.chain_snapshot_sha256`; the managed file
`docs/engineering/AGENTS_COMMANDS.md`. Example `context` value:

```json
{
  "reading_manifest": ["ENGINEERING_HARNESS.md",
    "docs/engineering/OPERATING_CARD.md",
    "docs/engineering/AGENTS_COMMANDS.md",
    "docs/engineering/execution-control-plane/work-orders/WO-ECP-001.md"],
  "governing": ["CAP-ECP-001", "INT-ECP-001", "REQ-ECP-001", "REQ-ECP-002"],
  "declared_paths": ["se_harness/cli.py", "tests/"],
  "state": {"status": "in_progress", "family": "work_order"},
  "next": {"argv": ["harnessctl", "check", ".", "--artifact", "WO-ECP-001",
    "--checkpoint", "handoff", "--from-git", "origin/main"],
    "procedure_id": "PROC-WO-IMPLEMENT", "step_id": "STEP-WO-IMPLEMENT-CHECK"},
  "decision_required": null
}
```

## Failure behaviour

Every rule fails closed. `WEX-ECP-001` (ambiguous selection), `WEX-ECP-002`
(conflicting change-set sources), `WEX-ECP-003` (Git unavailable or base
unresolvable), and `WEX-ECP-004` (command block over budget) are `blocked`
outcomes with exit status 1; none creates, changes, or infers lifecycle
state. `W-ECP-001` is a governance warning that changes no exit status.

## Compatibility and migration

Schema 2 is extended additively; `schema` stays
`se-harness-workflow-result-v2`. `--changed-path` and `--changes-complete`
remain accepted for one release after `--from-git` ships and are removed with
the following minor version. Installed `WORKFLOW.json`, `WORKFLOW.md`, and
`OPERATING_CARD.md` regenerate on the next governor upgrade because the
corrective forms and the state table gain `next`. `AGENTS_COMMANDS.md` is a
new managed file installed by `upgrade`. Legacy whole-tree evidence bindings
are accepted for one release (`ECP-SNP-004`).

## Explicitly unspecified decisions

- The ordering of `reading_manifest` beyond "router, card, command block,
  then the selected chain".
- Whether `next` caches the validation result between the manifest and the
  step resolution.
- The exact rendering of the `Context` section in the human block, provided
  it is deterministic and covered by the digest.
- The Git executable resolution strategy, provided it is the one shared Git
  wrapper the kernel already uses.

## Amendment record

**`ECP-SNP-001`'s digest hashes line-ending-canonical bytes, proposed
2026-08-29 under `WO-ECP-014` (issue #256; `SPEC-ECP-010`).** The rule names
`formal_snapshot_digest` as the function that binds evidence to a snapshot;
that function hashed each artifact's raw bytes, so a Windows checkout under
`core.autocrlf=true` computed a different snapshot from the LF checkout of
the managed workflow, and a packet bound there could never pass
`QGP-G4I-EVIDENCE` hosted (pull request #253 at `61840f3`). The amendment
makes the function hash `utf8-text-lf-v1` canonical bytes, the rule the
managed-file lock already uses; on an LF tree the digest is unchanged, so no
stored packet header or verification record moves. The chain-scoped digest
this rule defines inherits the byte rule when it is implemented. Nothing
else in this specification changes.
