+++
id = "WO-ECP-032"
type = "work_order"
title = "Wave 2, group B: the integrity primitives, the closed sets and the two grammars"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "This group touches every function that produces or compares a digest, a canonical byte form or an atomic write; that no recorded digest moved is a fact every later release and adoption relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/integrity.py",
  "se_harness/artifact_layout.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/cli.py",
  "se_harness/evaluator_evidence.py",
  "se_harness/evaluator_identity.py",
  "se_harness/github_ci.py",
  "se_harness/hash_bound.py",
  "se_harness/installer.py",
  "se_harness/interpreter_safety.py",
  "se_harness/mutation_guard.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/runtime_identity.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "repository_tools/json_bytes.py",
  "repository_tools/release_build.py",
  "repository_tools/release_distribution.py",
  "repository_tools/upgrade_rehearsal.py",
  "repository_tools/evaluator_facts.py",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-034.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-023.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-025.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-032.md",
]

[relations]
implements = ["REQ-ECP-034"]
specifications = ["SPEC-ECP-023"]
verification = ["VER-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T09:17:17Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #395, #396 and #397 and their summary were presented: wave 2 of the code health assessment of 2026-09-07 (issue #377) with the owner decision of issue #381 item 4, one primitive per family and the four contract tables read at run time. Approval of a definition authorizes no work. WO-ECP-032 carries no delegation class: its start, completion and record preparation are the engineering owner's explicit decisions."
+++

# Work Order: Wave 2, group B: the integrity primitives, the closed sets and the two grammars

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-PRM-006` to `ECP-PRM-015` of `SPEC-ECP-023`: `integrity.py`
as the one home of the digest, canonical-bytes, JSON, duplicate-key and
atomic-write primitives, re-exported to the repository tools; one
configuration reader; the checkpoint and definition-type sets exported from
the contract module only; typed value sets; one version grammar for both
wheel parsers; one subprocess environment builder.

## In scope

- `integrity.py`: `canonical_json_bytes(value, *, ensure_ascii)`,
  `pretty_json_bytes(value, *, ensure_ascii)`, the one duplicate-key hook,
  `atomic_write_bytes` with fsync; `raw_sha256` and `canonical_text_bytes`
  as they are.
- The sites measured on 2026-09-08 on `main` at `9d5a22da`: fifteen
  `hashlib.sha256` copies, eleven `sort_keys=True` serializers with
  `ensure_ascii=True` in the package and `False` in the tools, eleven
  `object_pairs_hook` definitions, the three inline `.tmp` writers of
  `workflow_compliance.py` and the writers of `installer.py`,
  `provenance.py`, `artifact_layout.py` and `workflow.py`, seventeen
  inlined `\r\n` replacements in the package and tools.
- `repository_tools/json_bytes.py` re-exporting the primitives;
  `release_build.canonical_json_bytes` renamed, its bytes unchanged, so the
  recipe digests of every bound record hold.
- One `.engineering-harness.toml` reader for `installer.py`,
  `mutation_guard.py` and `workflow.py`; `plan_transition` reads it once.
- `workflow_contract.CHECKPOINTS` and `DEFINITION_TYPES` imported by
  `cli.py` and `workflow_compliance.py`; `Literal` or `StrEnum` for
  `mode`, `action`, `checkpoint` and `phase`.
- One version grammar for `candidate_acceptance._wheel_version` and the
  `release_qualification` wheel parser; the evidence names every fixture
  wheel whose verdict changes.
- One environment builder for `candidate_acceptance.py`,
  `release_qualification.py` and `upgrade_rehearsal.py`.
- Tests at the boundary, the digest comparisons, the domain index, this
  work order's evidence packet and its record.

## Out of scope

- The engine's copies (wave 3, #378); the lane scripts.
- The launcher and the parser (`WO-ECP-031`); the codes registry and the
  contract tables (`WO-ECP-033`).
- Any byte a caller writes today, other than a lone `\r` now canonicalized
  where a copy dropped only `\r\n`.

## Expected change surface

About two hundred lines out of eighteen package modules and five tool
modules, one new function family in `integrity.py`, the boundary tests, this
packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-032/`: the five
greps before and after, the recipe replay digests against `RLS-SEH-025`, the
`CONTRACT_SHA256` reading, the scan readings, the suite reading, `validate`
and `doctor` readings.

## Authorized decision envelope

The order of edits inside the group; helper names beyond those the
specification fixes; whether the group lands as one commit or several.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- No contract JSON byte and no candidate template byte changes
  (`ECP-PRM-025`); no engine file changes (wave 3, #378).
- Every recorded digest equals `main`'s before completion (`ECP-PRM-024`).
- The scan readings before and after go in the evidence packet.
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Required verification

Execute `VER-ECP-025` in full for this group; repository-required checks;
the pull request's lanes; the handoff check; a verification record bound to
the candidate commit.

## Stop and escalate conditions

A recorded digest that differs from `main`; a suite failure beyond the
baseline that a consolidation explains: two copies disagreed and a caller
depended on the difference, stop and report; a need to change a contract
JSON byte; any managed or engine path in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
