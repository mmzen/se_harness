+++
id = "SPEC-AEX-007"
type = "specification"
title = "Change-bundle and transactional effect-broker contract"
status = "approved"
owners = ["technical-owner", "security-owner", "repository-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-AEX-002", "REQ-AEX-004", "REQ-AEX-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# Specification: Change-bundle and transactional effect-broker contract

## Scope

This specification defines change-bundle v1, evaluator-owned bundle
construction, admission, transactional application, durable journaling,
rollback and recovery, receipt generation, and the initial supported regular-
file operation set.

The bundle is a transport manifest for proposed byte changes. It is not a work
order, delegation, status record, gate result, approval, or authority token.
Those facts remain canonical in their existing artifacts and are referenced by
digest.

This specification does not admit direct target writes by a worker, Git index
or ref mutation, mode changes, links, submodules, managed evaluator-policy
updates, credentials, network access, external actions, or parallel writers.

## Actors and external systems

- One worker edits an evaluator-created isolated session workspace.
- The exact released evaluator snapshots intended session changes and builds
  canonical bundle bytes.
- The effect broker validates the current envelope, stages target replacements,
  maintains a durable journal, applies target operations, validates result, and
  emits the receipt.
- The external evaluator runtime directory holds session objects, transaction
  journals, backups, and recovery markers outside the target checkout.

## Change-bundle v1 schema

Canonical JSON has exactly this semantic shape:

```json
{
  "schema": "se-harness-change-bundle-v1",
  "identity": {
    "work_order": "WO-AEX-000",
    "envelope_sha256": "<64 lowercase hex>",
    "repository_state_before": "<64 lowercase hex>"
  },
  "changes": [
    {
      "operation": "replace",
      "path": "path/to/file.txt",
      "before": {"sha256": "<digest>", "size": 123},
      "after": {
        "sha256": "<digest>",
        "size": 124,
        "object": "objects/<same digest>"
      }
    }
  ]
}
```

The object itself contains no `bundle_sha256`; its identity is SHA-256 over
`se-harness-canonical-json-v1` bytes. `changes` is a non-empty path-ordered
sequence with unique portable paths and at most 1,024 entries. Total after-
content is at most 64 MiB and one file at most 16 MiB in Phase 4.

Operation invariants are:

| Operation | `before` | `after` |
| --- | --- | --- |
| `create` | null; target must be absent | digest, size, object required |
| `replace` | digest and size required | digest, size, object required |
| `delete` | digest and size required | null |

An object path is derived from its digest and resolves only inside the
evaluator-owned session object store. Object bytes are regular files, immutable
after bundle construction, and independently rehashed before target apply.
Duplicate content may share one object.

The bundle intentionally does not repeat work-order title, prose, status,
owners, full execution scope, gates, delegation, decision rights, evidence
requirements, or lifecycle history. `work_order`, `envelope_sha256`, and
`repository_state_before` are foreign keys that prevent cross-context use.

## Inputs and outputs

Inputs are one valid current Phase 4 envelope, its stable observation, one
evaluator-created session workspace, an explicit intended-deletion set, current
managed-policy inventory, and the external runtime directory.

Bundle construction produces canonical bytes, bundle digest, immutable content
objects, a normalized proposed-path summary, and no target effect.

Successful apply produces changed target bytes and
`se-harness-effect-receipt-v1` containing:

- schema, operation ID, bundle digest, envelope digest and nonce digest;
- work-order and evaluator identities;
- canonical ordered entries with operation, path, before digest, after digest,
  and result;
- `state_before`, `state_after`, previous receipt digest, and transaction ID;
- started and completed UTC timestamps;
- journal terminal state `committed`; and
- normalized gate, deviation, and evidence bindings.

Receipt authority fields are prohibited. The receipt is immutable evidence.

## State model

```text
session_open
  -> bundle_constructed
  -> preflighted
  -> nonce_admitted
  -> journal_prepared
  -> targets_applying
  -> result_observed
  -> committed_receipt

bundle_constructed | preflighted -> rejected_without_target_write
journal_prepared | targets_applying -> rolled_back | recovery_required
recovery_required -> recovered_prior | recovered_result | human_recovery_stop
```

No new governed operation may begin while the target has a nonterminal journal.

## Broker algorithm

1. Acquire the exclusive target-session lock and complete or stop on any prior
   recovery journal.
2. Freshly observe the target and admit the exact envelope under
   `SPEC-AEX-006`.
3. Parse canonical bundle bytes and require identity equality with the envelope
   and observation.
4. Resolve every path using handle-aware containment. Reject `.git`, managed
   released-evaluator and governance surfaces, undeclared paths, links, reparse
   points, special files, submodules, case collisions, and parent conflicts.
5. Verify all `before` states and all immutable `after` objects.
6. Build all parent directories and same-filesystem temporary replacement files
   without altering a target path. Fsync files where the platform supports a
   reliable primitive.
7. Write a durable journal with the complete plan, prior-state backups,
   expected result, and recovery checksum; mark it `prepared`.
8. Apply operations in canonical path order using atomic single-path replace or
   rename primitives and update the journal after each step.
9. Re-observe the complete repository and require the exact expected resulting
   manifest and no unexplained change.
10. Write and validate the receipt, mark the journal committed, then release
    the lock. Retain or dispose recovery material according to managed policy.

Ordinary apply failure invokes reverse-order rollback and proves the live state
equals `state_before` before reporting `rolled_back`. Process or machine
interruption may expose an intermediate filesystem state; the durable journal
makes that condition explicit and blocks all governed continuation until the
evaluator deterministically restores the prior state or proves and finalizes
the complete result. Cross-file atomic visibility is not claimed.

## Behavioral rules

1. **AEX-BND-001:** The evaluator, not the worker or provider, constructs and
   canonicalizes the bundle from the isolated session delta.
2. **AEX-BND-002:** A bundle carries proposed bytes and foreign-key digests only;
   it carries no authority or duplicated mutable governance fact.
3. **AEX-BND-003:** The broker is the only Phase 4 component allowed to write a
   governed target path.
4. **AEX-BND-004:** Complete preflight precedes the first target-path change.
5. **AEX-BND-005:** Every path must be admitted independently by the work order,
   formal delegation, envelope, bundle, and managed deny policy.
6. **AEX-BND-006:** V1 supports regular-file create, replace, and delete only.
7. **AEX-BND-007:** Parent directory creation is permitted only when every new
   component is within admitted scope, absent at preflight, and a normal
   directory; empty evaluator-created parents are removed on rollback.
8. **AEX-BND-008:** Before and after content digests and sizes are verified at
   construction, preflight, apply, post-observation, and receipt validation as
   applicable.
9. **AEX-BND-009:** The envelope nonce is consumed once admission succeeds,
   including failed, rolled-back, or recovery-required transactions.
10. **AEX-BND-010:** A terminal committed receipt must link exact live before
    and after observations and the prior receipt when present.
11. **AEX-BND-011:** A nonterminal journal blocks new envelopes, effects,
    lifecycle completion, and assurance preparation.
12. **AEX-BND-012:** The broker never stages, commits, resets, cleans, switches,
    merges, rebases, tags, pushes, or otherwise mutates Git metadata.
13. **AEX-BND-013:** Diagnostics and journals contain paths, digests, sizes, and
    bounded status, not secret file bodies or hidden reasoning.
14. **AEX-BND-014:** Unsupported platform durability or containment primitives
    fail preflight; they are not silently downgraded.

## Managed deny policy

The initial deny policy always includes `.git/`, the external evaluator and
runtime directories, installed lock and evaluator-governance surfaces required
to prove the current evaluator, root managed workflow and authority files, and
any filesystem object not represented as a normal directory or regular file.

Candidate templates and candidate evaluator source may be changed only when an
approved work order lists their exact repository paths. The broker must still
refuse to overwrite the currently executing external evaluator payload.

## Error and recovery behavior

Stable codes distinguish malformed bundle, noncanonical order, unknown field,
resource bound, identity mismatch, stale before state, staged-object mismatch,
scope denial, managed denial, path ambiguity, unsupported object, lock conflict,
journal conflict, apply failure, rollback failure, recovery required, result
mismatch, and receipt failure.

Recovery first verifies journal integrity and every current target entry. It
chooses only a fully provable rollback or fully provable completion. Ambiguous
or damaged recovery material produces `human_recovery_stop`, preserves all
available material, names uncertain paths, and permits no further agentic or
lifecycle advancement.

## Security, privacy, and performance

- Open files without following links and recheck identity before replacement.
- Use exclusive creation for journals, objects, and temporary paths; reject
  preexisting unexpected entries.
- Never interpret content, paths, or bundle fields as shell, code, template,
  URL, credential, or provider instruction.
- Restrict runtime material to the invoking operator and remove secret-bearing
  content according to explicit retention policy.
- Apply complexity is linear in entries plus changed bytes. Bounds are checked
  before expensive copies and target effects.
- Evidence records bundle and object digests, entry counts and sizes, locks,
  preflight results, journal transitions, apply and rollback results, before and
  after observations, receipt digest, duration, deviations, and uncertainty.

## Compatibility and migration

- V1 is a new schema and changes no prior receipt or envelope schema.
- Existing command-driven mutations continue through their current released
  evaluator. They do not become bundle effects automatically.
- A successor release must install the broker externally before any real target
  uses it. Candidate-source self-execution is prohibited.
- A new operation kind, mode bit, directory delete, link, submodule, larger
  bound, cross-repository effect, or different canonicalization requires a new
  schema or approved compatible extension.

## Examples and counterexamples

### Example: no duplicated work-order scope

The bundle names `WO-AEX-006`, its envelope digest, current state digest, and
two path deltas. It does not repeat the work order's owners, status, path list,
gates, or delegation. The broker resolves those from authoritative current
artifacts.

### Counterexample: direct patch application

A worker invokes a general patch tool in the target checkout and later emits a
matching bundle. The receipt chain is invalid because the target changed before
admission; the observer stops and the direct write is never legitimized.

### Counterexample: crash presented as atomic success

The process stops after one of two target replacements. No success receipt is
issued. The nonterminal journal blocks continuation until recovery proves the
complete prior or intended state.

## Explicitly unspecified decisions

- Private implementation class and helper names.
- Backup compression and retention duration within the closed recovery policy.
- Whether session workspace materialization uses a full copy or a bounded
  overlay, provided target writes remain impossible before broker admission.
- Fixture subdivision within work-order scope.

These choices cannot change bundle bytes, supported operations, authority
resolution, target deny policy, receipt linkage, or recovery guarantees.
