+++
id = "VER-ADS-001"
type = "verification"
title = "Independent evidence for an enforced, bounded, consistent directive surface"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-ADS-001", "REQ-ADS-002", "REQ-ADS-003", "REQ-ADS-004", "REQ-ADS-005", "REQ-ADS-006"]
+++

# Verification Contract: Independent evidence for an enforced, bounded, consistent directive surface

## Independence

Expected behaviour derives from the six requirements, `SPEC-ADS-001`,
`ARCH-ADS-001`, and the accepted outcome of `ADR-ADS-001`. Tests compare
rendered bytes, contract fields, manifests, diagnostics, digests, and CI
outcomes against fixtures written from the specification, never from candidate
output. Reviewers assess the router wording from the requirement, not from the
template.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ADS-001` distinct corrective step | contract loader tests, renderer tests, conformance test over every predicate | each predicate blocked in isolation; contract missing a corrective; corrective equal to evaluated command | no rendered `Command or response` equals the evaluated command; loader fails with `WEX-ADS-001`; escalation names a `DR-` role |
| `REQ-ADS-002` one step, one dialect | resolver equality test over every state in the state table; CLI default test | every WO/VREC/RLS state at one snapshot; `--result-schema 1` | `focus` and `check` render identical `Next` and `Command or response`; schema 2 is default; schema 1 carries `WEX-ADS-002` |
| `REQ-ADS-003` manifest and card | preflight manifest test; installer rendering test; card conformance test | start and review phases; card regenerated from contracts; contract mutated | manifest is closed and complete; card is `managed`, at most 3072 bytes, byte-equal to regeneration; mutation fails conformance |
| `REQ-ADS-004` trap diagnostics | fixture body with `\r`; temporary repository with orphaned `ready` VREC; non-Git target | trailer CRLF; VREC candidate rebased away; no `.git` | `W-ADS-001` with offset; `W-ADS-002` with record, commit, routes; `not_assessable` outside Git; exit status unchanged |
| `REQ-ADS-005` digest | JSON result test; canonicalisation test; CI selector test | LF/CRLF/trailing-space variants of one block; matching and edited PR bodies; absent trailer | one digest across variants; mismatch fails naming both digests and snapshot; absence passes |
| `REQ-ADS-006` router scope | template rendering test; blinded review | rendered router; three reviewers given the paragraph and four scenarios | heading and paragraph present verbatim; reviewers classify all four scenarios as intended |

## Acceptance scenarios

### Scenario 1: no self-loop anywhere

For every workflow rule and every predicate it names, block that predicate
alone and render. Assert the corrective command differs from the evaluated
command or is an escalation.

### Scenario 2: focus equals check

For every state in the state table, build a minimal repository, run both
commands with `--json`, and assert equal `next` and `command_or_response`.

### Scenario 3: manifest is the read

Run start preflight on an approved work order. Assert the manifest equals the
closed set in `ADS-RDM-001` and that the rendered router names the manifest
and card.

### Scenario 4: card conformance

Regenerate the card from the installed contracts and compare bytes. Add one
transition to a copy of `WORKFLOW.json` and assert the conformance test fails
naming it.

### Scenario 5: CRLF trailer

Supply a body whose trailer line ends `\r\n`. Assert `W-ADS-001` with the byte
offset and that the work-order selection still succeeds.

### Scenario 6: orphaned ready record

Create a `ready` VREC bound to a commit, rebase the branch so the commit is
unreachable, run review preflight. Assert `W-ADS-002`.

### Scenario 7: digest round trip

Render `check --json`, write the block into a PR body with the trailer, run
the CI selector at the same snapshot. Assert pass. Edit one word. Assert fail.

### Scenario 8: scope paragraph

Render the router from the template. Assert the heading and paragraph bytes.
Independent reviewers read the paragraph and classify: a repository review
(unconstrained), a transition inside an answer (stop conditions apply), a
finding labelled as formal (forbidden), a question about a work order
(unconstrained). All four must be classified as intended.

## Pass criteria

All deterministic tests pass on Linux and Windows. Scenario 8 has zero
misclassifications. The installed and packaged `WORKFLOW.json` remain
byte-identical. No lifecycle state, gate predicate, or decision right changed.
