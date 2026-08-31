+++
id = "SPEC-ECP-017"
type = "specification"
title = "The handoff check self-binds its packet and closes the change set over its own write"
status = "draft"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
specifies = ["REQ-ECP-028"]
+++

# Specification: The handoff check self-binds its packet and closes the change set over its own write

## Scope

Changes only the Git-derived handoff checkpoint of `harnessctl check`: the
evaluator rebinds an existing packet header and includes the retained result
path in the evaluated change set. The `evidence` command, the retained-result
rules, the `scope` checkpoint, the declared change-set forms, every contract
file and the result schema are unchanged.

## Terms

- **Current formal snapshot:** the digest `formal_snapshot_digest` computes
  over every formal artifact's line-ending-canonical bytes for this run.
- **Retained result path:** `DOMAIN/evidence/WO-ID/handoff.json`, the path a
  completed Git-derived handoff check writes (`ECP-PRB-002`, amended).
- **Self-binding run:** a `check --checkpoint handoff --from-git BASE`
  invocation selecting a work order.

## Behavioral rules

**ECP-SBH-001:** Before any predicate is evaluated, a self-binding run whose
packet exists with a machine header naming the selected work order and the
`handoff` checkpoint, and whose `formal_snapshot_sha256` differs from the
current formal snapshot, rewrites only the header: `formal_snapshot_sha256`
to the current snapshot and `rebound_at` to the run's UTC time at second
precision. The body is preserved byte for byte and the write is staged and
atomic, exactly as `harnessctl evidence` writes it. A packet already bound
to the current snapshot is not touched.

**ECP-SBH-002:** A missing packet is not created, and a packet without a
machine header at byte offset 0 is not touched: `QGP-G4I-EVIDENCE` keeps
reporting `not_assessable` with `harnessctl evidence` as the corrective
command for the first, and the one-release legacy grace (`W-ECP-002`) keeps
reading the second.

**ECP-SBH-003:** The `evidence` command's refusals hold unchanged on the
self-binding path: a header naming another artifact or checkpoint refuses
with `WEX-ECP-010`, and a `.gitattributes` rule that would convert the
packet's line endings refuses with `WEX-ECP-011`; nothing is written on
either refusal.

**ECP-SBH-004:** The evaluated change set of a self-binding run is the
Git-derived set united with the retained result path, whether or not that
file exists yet. The change set of the run that first retains the result
therefore equals the change set of any repeated run over the unchanged
tree, and `result_sha256` is stable from the first completed run.

**ECP-SBH-005:** A header rewrite is reported in the result's
`mutation.writes` with the packet path and the two header fields it moved,
beside the retained result's existing entry. `mutation.writes` is outside
the canonical restitution block, so neither entry perturbs
`result_sha256`.

**ECP-SBH-006:** Every other path through `check` stays read-only: the
declared change-set forms (`--changed-path`, `--changes-complete`,
`--change-manifest`) neither rebind nor extend the change set, and the
`scope`, `start`, `pre-action` and `transition` checkpoints write nothing
(`ECP-SCP-004` unchanged).

## Failure behaviour

A refused rebind (`WEX-ECP-010`, `WEX-ECP-011`) blocks the check before
predicate evaluation with the refusing code, and the packet keeps its prior
bytes. A blocked evaluation after a successful rebind retains no result,
exactly as today; the rebound header persists, because it states a fact
about the current tree that the next run re-verifies.

## Consequence for operators

One run of `check --checkpoint handoff --from-git BASE` is the declared
result: the digest it prints is the one `pr-body` emits and CI compares.
The second confirmation run and the manual `harnessctl evidence` re-bind
after each merge from the base branch are retired. The root evaluator
governing this repository keeps the released two-run behaviour until the
next root adoption.

## Open decisions

None.
