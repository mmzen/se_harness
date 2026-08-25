+++
id = "SPEC-ADS-001"
type = "specification"
title = "Failure rendering, next-step resolution, reading manifest, trap diagnostics, restitution digest, and router scope"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-ADS-001", "REQ-ADS-002", "REQ-ADS-003", "REQ-ADS-004", "REQ-ADS-005", "REQ-ADS-006"]
+++

# Specification: Failure rendering, next-step resolution, reading manifest, trap diagnostics, restitution digest, and router scope

## Scope

This specification defines six bounded contracts over the existing workflow
result, preflight, diagnostics, CI, and router surfaces. It changes no
lifecycle state, decision right, gate predicate, traceability relation, or
artifact schema. Every rule is a rendering, resolution, diagnostic, or
verification behaviour of the released evaluator or the managed CI workflow.

## Actors and external systems

- A coding agent runs `focus`, `check`, and `preflight` and returns restitution.
- Accountable owners read restitution and decide; nothing here decides for them.
- The released evaluator renders, resolves, and warns.
- The managed CI workflow recomputes a declared restitution digest.
- Git supplies ancestry for `W-ADS-002`.

## Terms

- **Corrective form:** the argument array declared for a predicate in
  `WORKFLOW.json` that, when supplied, can move that predicate from `fail` or
  `not_assessable` toward `pass`.
- **Operating card:** `docs/engineering/OPERATING_CARD.md`, a managed file
  rendered from the machine contracts.
- **Canonical block bytes:** the schema-2 human block, UTF-8, LF line endings,
  no trailing whitespace on any line, one trailing LF.

## Behavioral rules

### Failure rendering

**ADS-RST-001:** Every predicate in `WORKFLOW.json` steps of kind `command`
declares `corrective` as either `{"kind": "command", "arguments": [...]}` or
`{"kind": "escalation", "decision_right": "DR-..."}`. Contract loading fails
with `WEX-ADS-001` when a predicate lacks it.

**ADS-RST-002:** On a `blocked` or `failed` outcome, the renderer selects the
first failing predicate in `QG-009` order and renders its corrective form under
`Next` and `Command or response`. A corrective command whose argument array
equals the evaluated array is a conformance failure.

**ADS-RST-003:** Corrective arguments may contain placeholders of the form
`<changed-path>` and `<evidence-path>`; the renderer never substitutes guessed
values.

### Next-step resolution

**ADS-NXT-001:** `focus` and `check` call one shared resolver that takes the
selected artifact, its state, and the formal snapshot and returns the ordered
workflow rule and bound step. Neither command holds a private mapping.

**ADS-NXT-002:** `focus` renders `--result-schema 2` by default. Passing
`--result-schema 1` renders the legacy block preceded by `WEX-ADS-002: schema 1
is not restitution`.

**ADS-NXT-003:** For the same selected artifact and snapshot, and with no
checkpoint-specific argument to `check`, the `Next` and `Command or response`
values of `focus` and `check` are byte-identical.

### Reading manifest and operating card

**ADS-RDM-001:** The preflight reading manifest for a phase is closed: the
router, the operating card, the selected work order, every artifact it selects
through `implements`, `specifications`, `architecture`, and `verification`, and
the owner-region command file. Nothing else is mandatory.

**ADS-RDM-002:** The installer renders `docs/engineering/OPERATING_CARD.md`
from `WORKFLOW.json` and `QUALITY_GATES.json` in mode `managed`. Content, in
order: state table; nine restitution headings; stop conditions; managed trap
list. Size is at most 3072 bytes of UTF-8. A conformance test regenerates it
and compares bytes.

**ADS-RDM-003:** The router's reading instruction reads: "Before acting on a
lifecycle stage, read every file in the phase reading manifest emitted by
`harnessctl preflight` and `docs/engineering/OPERATING_CARD.md`. The routed
policies below are reference for humans and for the evaluator; an agent is not
required to read them to act."

### Trap diagnostics

**ADS-DGN-001:** `W-ADS-001` fires when a pull-request body supplied by
`--pull-request-body` or read by the CI selector contains `\r` within the
`Harness-Work-Order` line. It reports the byte offset and one exact fix.

**ADS-DGN-002:** `W-ADS-002` fires in `preflight --phase review` and
`check --checkpoint handoff` when a `ready` verification record's
`candidate_commit` is not an ancestor of `HEAD`. It reports the record, the
commit, and the three legal routes. Outside a Git checkout it is
`not_assessable`.

**ADS-DGN-003:** Both diagnostics are `governance` plane warnings and change no
exit status of an otherwise passing run.

### Restitution digest

**ADS-DIG-001:** `se-harness-workflow-result-v2` gains `result_sha256`: the
lowercase SHA-256 of the canonical block bytes. The schema version is unchanged.

**ADS-DIG-002:** The pull-request template offers an optional standalone line
`Harness-Restitution: <sha256>`.

**ADS-DIG-003:** When that line is present, the managed CI workflow runs the
bound `check` for the declared work order at the checkout's formal snapshot and
compares. Mismatch is a failed required check naming both digests and the
snapshot. Absence is not a failure.

### Router scope

**ADS-SCP-001:** The router carries, before the global invariants, the heading
`Scope of these obligations` and this paragraph: "`HRN-003`, the lifecycle
restitution rules, and the stop conditions bind an actor executing or
reporting a lifecycle stage. Reading, analysis, and answering questions are
unconstrained, provided no lifecycle state changes, no decision right is
exercised, and no finding is presented as a formal result."

## Inputs and outputs

Inputs are the existing command arguments plus `--pull-request-body <file>` on
`check`. Outputs are the existing human and JSON results plus the field,
diagnostics, and file named above.

## Failure behaviour

Every rule fails closed: a missing corrective form blocks contract loading; a
stale card fails conformance; a mismatched digest fails CI. No rule creates,
changes, or infers lifecycle state.
