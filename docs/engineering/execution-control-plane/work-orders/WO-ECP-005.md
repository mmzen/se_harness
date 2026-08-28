+++
id = "WO-ECP-005"
type = "work_order"
title = "One result schema and one rule selector"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The work removes a result schema and merges two rule selectors. Every later handoff, transition, verification-record, and release-record result is produced by this path, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow.py",
  "se_harness/workflow_result.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_contract.json",
  "se_harness/cli.py",
  "se_harness/provenance.py",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/agent-directive-surface/specifications/SPEC-ADS-001.md",
  "docs/engineering/agent-directive-surface/requirements/REQ-ADS-002.md",
  "docs/engineering/workflow-execution/specifications/SPEC-WEX-002.md",
  "docs/engineering/ci-pipeline/specifications/SPEC-CIP-001.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-010"]
specifications = ["SPEC-ECP-005"]
architecture = ["ARCH-ECP-001", "ADR-ECP-004"]
verification = ["VER-ECP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', in its amended form: REQ-ECP-010 only (schema 2 as the sole result, one rule selector, the contract handoff blocks removed, the three dated retirement amendments to SPEC-ADS-001, REQ-ADS-002 and SPEC-WEX-002, the focus_schema2 double validation, the golden result_sha256 test). The precondition engine is WO-ECP-009 and is not approved. Authorizes only the listed execution scope; start, completion, commit-bound verification and release are separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T12:14:43Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-28 by the accountable owner, 'start WO-ECP-005', after #238 merged the amended packet and the approvals. Execution is confined to the approved scope: schema 2 as the only result, one rule selector, the contract handoff blocks removed, the three dated retirement amendments, the focus_schema2 double validation, the golden result_sha256 test, notes and tests. The precondition engine is WO-ECP-009 and is not started."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-28T12:32:00Z"
decided_by = "engineering-owner"
reason = "Completed on 2026-08-28 on the owner's standing direction for this sequence, once the hosted lanes were green. The handoff checkpoint reads Completed under the released 0.7.1 evaluator outside the checkout with seventeen changed paths declared and completeness asserted. Delivered: schema 2 as the only result of focus, transition, capture-verification and prepare-release; the --result-schema option removed with either value an argument error; legacy_to_schema2, the schema-1 builder and renderers and _recommend deleted; one selector and one context builder in workflow_compliance.selected_result; the handoff blocks and handoff_fields removed from the workflow contract and its managed rendering with each rule keeping only done and current_lifecycle_state; focus validating once; the golden result_sha256 of the released 0.7.1 evaluator reproduced and pinned; dated retirement amendments to SPEC-ADS-001, REQ-ADS-002 and SPEC-WEX-002 and the SPEC-CIP-001 correction; tests and evidence. All thirteen hosted checks pass at f054a66, Windows legs included. ECP-KRN-008's per-predicate refusal labels are deferred to WO-ECP-009, disclosed. Completion is not verification."
+++

# Work Order: One result schema and one rule selector

Amended on 2026-08-28, before approval, on the review of issue #212: the
precondition engine (`REQ-ECP-009`, `ECP-KRN-004` to `ECP-KRN-009`) moves to
`WO-ECP-009`, so that a mechanical deletion and a contract-semantics change
are verified separately. This work order keeps `REQ-ECP-010`.

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-010`,
`SPEC-ECP-005`, `ARCH-ECP-001`, `ADR-ECP-004`, and `VER-ECP-005` are
separate acts by their owners and precede approval of this work order. This
work order is independent of the others; `WO-ECP-009` follows it.

## Objective

End every disagreement between `check` and `transition` on the same state.
Today there are two result envelopes, two rule engines, and three
precondition implementations (complexity audit P0-6,
`docs/notes/complexity-audit-2026-08.md:224-253`): schema 1 is still the
default on `transition`, `capture-verification`, and `prepare-release`;
`_recommend` and `select_rule` compute `successor_id` differently; the
gate contract's `transition` checkpoint is unreachable because
`check_workflow` refuses it (`se_harness/workflow_compliance.py:395`) while
`QUALITY_GATES.md` `QG-010` promises transitions recheck contract
predicates (the 2026-08 agentic execution review, section 3).

## In scope

- Schema 2 as the only result of `focus`, `check`, `transition`,
  `capture-verification`, and `prepare-release`; `--result-schema` removed
  with either value an argument error; `legacy_to_schema2`, the schema-1
  `_result`/`_handoff` builders and `workflow.render_*` deleted
  (`ECP-KRN-001`, `-002`, `-010`).
- `_recommend` and `_contract_match`/`_format_contract_value` deleted;
  `plan_transition`, `preparation_result` and `failed_result` build through
  `build_result` with `select_rule` over one context builder (`ECP-KRN-003`).
- The `handoff` block of every rule, `failure.handoff` and `handoff_fields`
  removed from `se_harness/workflow_contract.json` and the managed
  `WORKFLOW.json`; `WORKFLOW.md` and `OPERATING_CARD.md` no longer describe
  `--result-schema`; `tests/test_workflow_documentation_contract.py`
  retargeted.
- `focus_schema2` passing its validation report into `focus` so the
  validator runs once (issue #212, change 4).
- Transition failures labelled by the refusing check rather than a blanket
  `WEX201` (`ECP-KRN-008`), as far as the checks that exist before
  `WO-ECP-009` allow.
- `se_harness/provenance.py` rendering its results in schema 2 only.
- Dated retirement amendments to `SPEC-ADS-001` `ADS-NXT-002`, `REQ-ADS-002`
  and `SPEC-WEX-002`; the `[--result-schema 2]` correction in
  `SPEC-CIP-001`; `docs/notes/harnessctl-reference.md`.
- A golden `result_sha256` test: `select-work-order --field
  restitution-digest` on an unchanged fixture repository reads the same
  digest before and after (issue #212, criterion 3).
- Tests; work-order-keyed evidence.

## Out of scope

- The precondition engine, the `transition` checkpoint bindings and
  `QUALITY_GATES.*` (`WO-ECP-009`); authenticating decisions (`WO-ECP-004`);
  the delegation class (`WO-ECP-006`); the root managed `WORKFLOW.*` and
  `OPERATING_CARD.md` copies; any change to a gate predicate's identifier or
  meaning, to lifecycle states, or to decision rights; any lifecycle
  transition of any artifact; folding `focus` into `check` (#225).

## Authorized decision envelope

The implementation agent may decide how the shared context is built, the
argument-error wording, and test names. It may not change `result_sha256`'s
definition over the schema-2 block, touch `QUALITY_GATES.*` or
`_validate_preconditions`, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings;
  exercise the candidate `transition` only against temporary repositories.
- Root managed copies are not edited.
- LF line endings; assert bytes against blobs.
- Stage every deletion before any preflight or check run.

## Expected change surface

The workflow kernel's result path, the result renderer, the contract loader
and selector, the workflow contract and its managed rendering, the CLI
options, the provenance module's result path, three approved artifacts by
dated amendment, tests, evidence.

## Required verification

Execute the `VER-ECP-005` rows that name `REQ-ECP-010` plus the
repository-required checks; run the complete suite on Linux and Windows with
figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-005/`:
paired `check` and `transition` results per fixture, the mutated contract
copy and outcome, refusal diagnostics, per-platform test figures, and the
complete changed-path set.

## Stop and escalate conditions

Stop if any consumer of schema 1 is found outside tests and the
`harness-orient` `--help` guard, if `result_sha256` changes for an unchanged
repository, if the released evaluator refuses the edited workflow contract,
or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-005 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
