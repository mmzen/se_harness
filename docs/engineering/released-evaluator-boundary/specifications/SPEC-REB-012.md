+++
id = "SPEC-REB-012"
type = "specification"
title = "Simple evaluator upgrade contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-REB-027", "REQ-REB-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T15:20:02Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', on the owner's direction that the evaluator upgrade must be simple: the MG007 work-order packet and the MG004 and RID022 archive-digest requirements are retired, the installed evaluator's version and payload digest are its identity, index installs pass the managed lane, and the candidate-evidence lane selects the acceptance operation by the verifier's capability. REQ-REB-005 is superseded under WO-REB-027."
+++

# Specification: Simple evaluator upgrade contract

## Scope

`harnessctl upgrade` and the identity proofs it and the managed workflow rely
on, when the installed released evaluator is newer than the standard root's
lock. Replaces the packet model of `SPEC-REB-002` rule 1 for upgrades; the
conflict rules, runbook and recovery rules of that specification stay.

## Inputs

- A standard root with a schema-3 lock (or the legacy schema-2 lock that
  `MG002` already routes to an upgrade).
- A released evaluator installed outside the checkout by any means — an
  index install (`pip install se-harness==X`) or a wheel file — and run with
  `-I`.
- Optional `--evidence-output <repository-relative .json>`.

## Outputs

The reviewed managed files and the schema-3 lock naming the installed
evaluator's version, payload digest and, when recorded, archive digest; the
evaluator-transition evidence when requested; `identity`,
`qualify released-root` and `doctor` results.

## State model

`root at version A` → `plan` (read-only) → `apply` → `root at version B`, in
one transaction; a plan with `customized` or `conflict` entries stops before
the write, as today.

## Behavioral rules

1. **Identity.** `installed_evaluator_identity()` yields the version, the
   installed-payload digest, and the archive name and digest only when the
   installation recorded them. No caller treats a missing archive digest as
   an error (`REQ-REB-028`).
2. **Guard.** `require_mutation_authority(..., allow_upgrade_transition=True)`
   proves the target evaluator's identity by version and payload; `MG004` is
   raised only when the evaluator cannot identify itself at all. `MG007` and
   the `[evaluator_upgrade]` packet, `upgrade_authorization` and the
   `--work-order` option are retired; the code values stay reserved and are
   never reused for another meaning.
3. **Apply.** `--apply` writes the reviewed plan and the lock atomically; the
   lock's `evaluator.archive_sha256` is the recorded digest or `null`.
4. **Evidence.** With `--evidence-output`, the transaction writes the same
   canonical `se-harness-evaluator-upgrade-evidence-v1` document as today
   minus the packet fields (`authorization_path`, `authorized_by`,
   `work_order` become `null`); without it, nothing is written and the human
   output says so.
5. **Root qualification.** `qualify released-root` and the managed
   `engineering-harness.yml` template pass on an index install; `RR001`
   compares the archive digest only when the lock and the installation both
   carry one.
6. **Candidate acceptance.** The repository-owned candidate-evidence lane
   uses `qualify candidate-package` when the released verifier carries the
   `qualify` namespace and the legacy `accept-candidate` bootstrap otherwise;
   the assertions match the operation that ran.
7. **Policy.** Which repository change is authorized is repository policy —
   a normal work order over the changed files — and not a tool gate.
8. **Determinism.** Same inputs, same plan, same lock bytes, same evidence.

## Error and recovery behavior

Customization, conflict, an unreadable lock, a target evaluator that cannot
prove its identity, a payload or recorded-archive mismatch, or a partial
write stop the transaction and leave the pre-write state.

## Compatibility and migration

Repositories on a schema-3 lock upgrade with `pip install se-harness==X`
outside the checkout and `harnessctl upgrade . --apply`. Historical
`[evaluator_upgrade]` tables in retained work orders are unknown tables to
the validator and stay as history. The `.engineering-harness.lock` schema is
unchanged; `archive_sha256` was already optional in it.

## Examples and counterexamples

- Valid: index-installed 0.7.1 upgrades a 0.6.0 root with one command; the
  lock records `archive_sha256 = null`; the managed lane passes.
- Valid: wheel-file-installed 0.7.1 does the same and records the digest.
- Invalid: a payload digest that does not match the installed files
  (`RID021`); a recorded archive digest that differs (`RID022`).
- Invalid: a candidate checkout run as the evaluator (`RID018` as today).

## Explicitly unspecified decisions

Whether a future release records the archive digest for index installs
through pip's `--require-hashes` metadata; the repository's own work-order
policy for root changes.
