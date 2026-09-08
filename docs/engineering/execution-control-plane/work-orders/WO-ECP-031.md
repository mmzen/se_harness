+++
id = "WO-ECP-031"
type = "work_order"
title = "Wave 2, group A: one process launcher and one front-matter parser"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "Every command launches Git or parses front matter through the code this group replaces; that the one launcher and the one parser behave as the copies did, except where a copy was wrong, is a fact later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/_process.py",
  "se_harness/front_matter.py",
  "se_harness/artifact_layout.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/cli.py",
  "se_harness/gate_source.py",
  "se_harness/hash_bound.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/release_unit.py",
  "se_harness/risks.py",
  "se_harness/decisions.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "repository_tools/release_build.py",
  "repository_tools/release_distribution.py",
  "repository_tools/upgrade_rehearsal.py",
  "repository_tools/evaluator_facts.py",
  "docs/notes/diagnostic-codes.md",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-034.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-023.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-025.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-031.md",
]

[relations]
implements = ["REQ-ECP-034"]
specifications = ["SPEC-ECP-023"]
verification = ["VER-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T09:16:54Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #395, #396 and #397 and their summary were presented: wave 2 of the code health assessment of 2026-09-07 (issue #377) with the owner decision of issue #381 item 4, one primitive per family and the four contract tables read at run time. Approval of a definition authorizes no work. WO-ECP-031 carries no delegation class: its start, completion and record preparation are the engineering owner's explicit decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T09:38:40Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-08, given with the words 'start the work orders' for the three wave 2 work orders after the packet pull requests #395, #396 and #397 merged. Start preflight PASS. Executes on wo/ecp-031-process-front-matter; groups B and C follow in sequence because the three groups edit overlapping modules."
+++

# Work Order: Wave 2, group A: one process launcher and one front-matter parser

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-PRM-001` to `ECP-PRM-005` of `SPEC-ECP-023`: one process
launcher in `se_harness/_process.py` behind every Git launch of the package
and the repository tools, and one front-matter parser in
`se_harness/front_matter.py` behind every front-matter read, with each
caller keeping its exception type and its timeout or a longer one.

## In scope

- `se_harness/_process.py`: `run` and `run_git` with a default timeout,
  `stdin=DEVNULL`, UTF-8 decoding with replacement, an output cap, the
  `(OSError, SubprocessError)` catch and the `error=` class parameter.
- The launch sites measured on 2026-09-08 on `main` at `9d5a22da`:
  `artifact_layout.py`, `candidate_acceptance.py` (two), `cli.py` (the
  engine launcher), `gate_source.py`, `hash_bound.py`, `preflight.py`,
  `provenance.py`, `release_qualification.py`, `release_unit.py`,
  `workflow_compliance.py` (two); `repository_tools/release_build.py`
  (two), `release_distribution.py`, `upgrade_rehearsal.py` (two). Timeouts
  read `{5, 30, 60, 120, 300, 600}` and named constants today; none is
  lowered.
- `se_harness/front_matter.py`: one parser returning metadata and body,
  BOM-tolerant, CR and CRLF normalized, delimiters anchored at line start.
- The parser sites: `artifact_layout.py`, `gate_source.py` (the unanchored
  split), `hash_bound.py`, `provenance.py`, `release_qualification.py`,
  `workflow.py`, `risks.py`, `decisions.py`, `workflow_compliance.py`
  (the LF-only delimiter matches), `repository_tools/evaluator_facts.py`
  (the copy that fails on CRLF).
- Tests for both primitives at the boundary: `git` absent, timeout, output
  over the cap; BOM, CRLF, lone CR, unanchored `+++` in a body.
- The diagnostic-code page if a message text moves; the domain index; this
  work order's evidence packet and its record.

## Out of scope

- The engine's four launches and its parser in `se_harness/engine/`
  (wave 3, #378); the lane scripts under `scripts/` and `.github/scripts/`.
- The integrity primitives, closed sets and grammars (`WO-ECP-032`); the
  codes registry and the contract tables (`WO-ECP-033`).
- Any behaviour a caller can reach today, other than a CRLF artifact
  parsing where a copy refused it and a missing `git` refusing with a code
  where one copy raised a traceback.

## Expected change surface

Two new package modules of about two hundred lines together, about thirty
call sites edited across fifteen modules, the boundary tests, this packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-031/`: the
`subprocess.run` and `"+++"` greps before and after, the scan readings, the
suite reading, `validate` and `doctor` readings.

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
