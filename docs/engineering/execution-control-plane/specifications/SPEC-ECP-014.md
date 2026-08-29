+++
id = "SPEC-ECP-014"
type = "specification"
title = "The projection carries the execution context; next is an alias; accept-candidate is retired"
status = "draft"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-025"]
+++

# Specification: The projection carries the execution context; next is an alias; accept-candidate is retired

## Scope

Folds `next` into the checkpoint-less `check` projection (`ECP-ONE-001`)
with a one-release alias, and removes the `accept-candidate` subcommand. No
procedure step, gate, contract file, result schema or hash-locked root file
changes; the template `WORKFLOW.md` names the folded command.

## Terms

- **Projection:** `check` without `--checkpoint`, as `ECP-ONE-001` defines it.
- **Context:** the object `ECP-NXT-002` defines: `reading_manifest`,
  `governing`, `declared_paths`, `state`, `next`, `decision_required`.
- **Alias window:** the one release that ships with the deprecation notice.

## Behavioral rules

**ECP-CTX-001:** The projection's result carries the top-level `context`
object with exactly the members and values `ECP-NXT-002`, `ECP-NXT-003` and
`ECP-NXT-005` define; `operation.kind` stays `check` (`ECP-ONE-002`).

**ECP-CTX-002:** The projection's `--artifact` is optional: absent, the
single `in_progress` work order is selected, otherwise the result is
`blocked` with `WEX-ECP-001` naming the candidate count (`ECP-NXT-001`).
With a checkpoint `--artifact` remains required.

**ECP-CTX-003:** The projection's `result_sha256` is computed over the
canonical block with the `Context` section rendered after `Command or
response` (`ECP-NXT-007`); the human block renders that section.

**ECP-CTX-004:** `harnessctl next` remains for the alias window: it returns
bytes identical to the projection for the same arguments, the same
`operation.kind` and the same `result_sha256`, and prints one line on
standard error naming `harnessctl check` as the replacement; `next_step` in
`workflow.py` is deleted and the alias calls the projection.

**ECP-CTX-005:** Every corrective the product emits that named `harnessctl
next` names `harnessctl check` with the same arguments: the `WEX210`
corrective of a blocked `check --checkpoint start` names `harnessctl check .
--artifact ID` (`ECP-NXT-008` restated), and the response form names
`harnessctl check .`.

**ECP-CTX-006:** `harnessctl` has no `accept-candidate` subcommand: the
parser does not register it, `--help` does not list it, `_accept_candidate`
is deleted, and a pre-parse guard makes `harnessctl accept-candidate` exit
with status 2, empty standard output and one line on standard error naming
`harnessctl qualify candidate-package`. `qualify candidate-package`, the
`candidate_acceptance` module it uses and the candidate-evidence workflow
are unchanged.

**ECP-CTX-007:** The template `WORKFLOW.md` names `harnessctl check .
--artifact WO-...` where it named `next` (step 5 and the corrective-form
paragraph); `WORKFLOW.json` is unchanged. `docs/notes/harnessctl-reference.md`
folds the `next` synopsis into `check` and drops the `accept-candidate`
row and section; `harnessctl-check.md` says that `check` selects the default
artifact and carries the context and that `next` is an alias for one
release; `release-qualification-roles.md` says the alias is gone.

**ECP-CTX-008:** `SPEC-ECP-001` receives one amendment record restating
`ECP-NXT-001`, `ECP-NXT-004`, `ECP-NXT-007` and `ECP-NXT-008` against
`check`, with `next` as the alias for the window; no retained rule text is
edited.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-025 | ECP-CTX-001 to ECP-CTX-008 |

## Failure behaviour

Nothing new fails. A script on `accept-candidate` fails loudly at the guard;
a script on `next` keeps working through the window and reads the notice.

## Compatibility and migration

Consumer-visible: the projection's `result_sha256` changes for every
artifact because the block gains a section; no stored record binds a
projection digest (handoff and checkpoint results are unaffected).
`harnessctl check` with an explicit `--artifact` accepts every argument it
accepted. The `next` alias is removed by a later work order after the
window, as `WO-ECP-017` removed `focus`. The candidate-evidence workflow's
legacy branch stays as `SPEC-REB-012` rule 6 states it.
