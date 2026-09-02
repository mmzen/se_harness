+++
id = "SPEC-ECP-014"
type = "specification"
title = "The projection carries the execution context; next is an alias; accept-candidate is retired"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:39:39Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-29 with the words 'Approve and start WO-ECP-019': ECP-CTX-001 to ECP-CTX-008; the candidate-evidence workflow's legacy branch stays as SPEC-REB-012 rule 6 states it, and the next alias is removed by a later work order after one release ships the notice."
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
- **Alias window:** the one release that was to ship the deprecation
  notice; closed before opening by `WO-ECP-020`.

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

**ECP-CTX-004:** `harnessctl` has no `next` subcommand: the parser does
not register it, `--help` does not list it, `_next` and its notice are
deleted, and a pre-parse guard makes `harnessctl next` exit with status 2,
empty standard output and one line on standard error naming `harnessctl
check [--artifact ID]` as the replacement; `next_step` in `workflow.py` is
deleted. (Amended under `WO-ECP-020`; the rule first kept `next` as a
byte-identical alias for one release.)

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
folds the `next` synopsis into `check` and drops the `next` row, the
`accept-candidate` row and section; `harnessctl-check.md` says that `check` selects the default
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
a script on `next` fails loudly at its guard the same way.

## Compatibility and migration

Consumer-visible: the projection's `result_sha256` changes for every
artifact because the block gains a section; no stored record binds a
projection digest (handoff and checkpoint results are unaffected).
`harnessctl check` with an explicit `--artifact` accepts every argument it
accepted. The `next` alias is removed in the same release by `WO-ECP-020`;
no release ships it. The candidate-evidence workflow's
legacy branch stays as `SPEC-REB-012` rule 6 states it.

## Amendment record

**`ECP-CTX-004` is the refusal, not the alias, proposed 2026-08-29 under
`WO-ECP-020`.** The rule kept `next` for one release as a byte-identical
alias with a notice; the owner's decision of 2026-08-29 removes it before
the release after 0.11.0 is built (see the record on `REQ-ECP-025`). The
rule is restated in place as the guard, mirroring `ECP-RMV-002` for
`focus` and `ECP-CTX-006` for `accept-candidate`; `ECP-CTX-007` drops the
reference's `next` row with the synopsis, the term "alias window" and the
failure and compatibility paragraphs read accordingly. Nothing else in
this specification changes.

**The guards of `ECP-CTX-004` and `ECP-CTX-006` are closed, proposed 2026-09-02 under `WO-ECP-025` (`SPEC-ECP-019` `ECP-TMB-001`, `ECP-TMB-002`).** `harnessctl` still has no `next` and no `accept-candidate` subcommand; the pre-parse guards that named the replacements left `main()` three releases after the removals shipped, and argparse refuses both names with its usage error and exit status 2. `ECP-CTX-005` and `ECP-CTX-007` are unchanged.
