+++
id = "REQ-ECP-010"
type = "requirement"
title = "One result schema and one rule selector"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL render every workflow result of `focus`, `check`, `transition`, `capture-verification`, and `prepare-release` in result schema 2 from one shared rule selector."
verification_method = ["test"]
priority = "must"
source = "complexity audit P0-6"

[relations]
derives_from = ["CAP-ECP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: One result schema and one rule selector

## Rationale

Two result envelopes exist with a lossy projection between them, and `--result-
schema` defaults to 2 on `focus` but to 1 on `transition`, `capture-
verification`, and `prepare-release` (se_harness/cli.py:999, :1042, :1241,
:1323; docs/notes/complexity-audit-2026-08.md:226-233). `_recommend` and
`select_rule` are two rule engines over the same table computing `successor_id`
differently (se_harness/workflow.py:355-399;
se_harness/workflow_contract.py:554-595). `result_sha256` binds only schema 2
and `legacy_to_schema2` has no test importer (docs/notes/complexity-
audit-2026-08.md:243-245). The audit's P0-6 verdict is to consolidate; nothing
is lost because the evaluator is version-pinned.

## Behavior

- Trigger: always: any of the five commands emits a result.
- Response: the result is a schema-2 block with `result_sha256`; the `next`
  field of every command is computed by `select_rule` over one context builder;
  the CLI has no `--result-schema` option and no schema-1 renderer.
- On failure: a command that cannot build a schema-2 block fails closed with a
  coded predicate; it never emits a schema-1 block.

## Assumptions and dependencies

- The template CI already consumes only `check --json`, which is schema 2
  (docs/notes/complexity-audit-2026-08.md:244-245).
- `harnessctl next` (REQ-ECP-001) is a sixth consumer of the same selector.
- Removing schema 1 is a documented CLI change in the release notes and the
  managed `WORKFLOW.md`.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-010.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` is `implemented` with a ready record.

**When** `harnessctl transition . --artifact WO-X-004 --to verified --json` runs
without `--apply`.

**Then** the output is a schema-2 block carrying `result_sha256`, and its `next`
equals the `next` that `focus` and `check` compute for the same state.

### Example: failure behavior

**Given** an actor passes `--result-schema 1` to `capture-verification`.

**When** the command runs.

**Then** the CLI rejects the unknown option; no result is emitted.

## Open decisions

None.
