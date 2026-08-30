# Phase 4 change bundles and transactional effects

> Historical record from 2026-08-25, at `45b259b`. Kept for the decision trail; it describes the tool as it was then. The `delegated-workflow` command and the three retired writing skills it describes were replaced by the [delegation class](../delegation-class.md) and the journaled apply.

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

This guide explains the `WO-AEX-006` candidate implementation. Formal meaning
comes from `SPEC-AEX-007`, the selected work order, and the target repository's
exact released evaluator. Candidate source cannot use these APIs to authorize
its own construction.

## What the bundle contains

`se-harness-change-bundle-v1` is a transport manifest for proposed bytes. Its
identity contains only three foreign keys:

- the selected work-order ID;
- the exact envelope digest; and
- the exact repository-state-before digest.

Each ordered entry describes one regular-file `create`, `replace`, or `delete`.
Content is addressed as `objects/<sha256>` in the evaluator-owned external
object store. The bundle does not copy work-order prose, owners, status, scope,
delegation, decision rights, gates, evidence requirements, or lifecycle
history. The broker resolves those current facts at admission time.

`se_harness.change_bundle.construct_change_bundle` compares an
evaluator-owned baseline with a proposed isolated workspace. Removed files
must also appear in the explicit intended-deletion set. It writes immutable,
deduplicated content objects externally and returns canonical bytes plus their
SHA-256 identity. It never writes the target repository.

## How a target effect runs

`se_harness.effect_broker.apply_change_bundle` is the sole Phase 4 target-file
writer. In order, it:

1. proves released-evaluator mutation authority for
   `change-bundle-apply`;
2. acquires the repository session's OS-backed single-writer lock;
3. resolves any older journal before accepting new work;
4. freshly observes the repository and consumes the envelope nonce through the
   existing live-admission API;
5. checks the bundle foreign keys, every path scope, the managed deny policy,
   every before state, and every content object;
6. takes a complete regular-file manifest, re-observes after preflight, and
   rejects drift;
7. stores prior bytes and a checksum-bound recovery plan in the external
   runtime directory before creating any target parent or temporary file;
8. applies entries in UTF-8 path order with one-path replacement primitives;
9. compares the complete result with the planned manifest and a fresh live
   observation; and
10. returns canonical `se-harness-effect-receipt-v1` evidence after the journal
    reaches `committed`.

The receipt links the bundle, envelope, nonce digest, evaluator, work order,
ordered effects, state before and after, prior receipt, transaction, gates,
deviations, and evidence. It deliberately has no approval or authority field.

## Failure and restart behavior

An ordinary exception after the durable journal runs reverse rollback and
compares the complete target manifest with the prior manifest. A successful
rollback consumes the nonce as failed and archives a `rolled-back` journal.

An actual process exit releases the operating-system locks but leaves the
session identity, nonce record, recovery objects, and nonterminal journal. A
new evaluator process may resume only that journal-bound session. Recovery
validates the journal's closed field set and checksum before examining target
paths. It either proves and archives the completed result, restores and proves
the exact prior result, or records `human-recovery-stop`.

Missing, corrupt, aliased, or ambiguous recovery material never triggers a
guess. It retains the journal, records recovery-required state, names uncertain
paths, and blocks another session.

## Deliberate limits

The canonical bundle is limited to 1 MiB, 1,024 changes, 16 MiB per proposed
file, and 64 MiB of proposed bytes in total. The external recovery journal has
a separate 4 MiB canonical limit because it carries the complete mutation plan,
prior/result manifests, and rollback bookkeeping. Ordinary canonical documents
retain the 1 MiB default.

The candidate supports regular file bytes only. It does not change file modes,
directories as governed objects, links, junctions, reparse points, hard links,
submodules, Git metadata, root managed evaluator/governance files, credentials,
network services, releases, deployments, or other external systems. It claims
atomic replacement for one path, not instantaneous visibility of a whole
multi-file bundle.

The implementation is not active in a real target. Activation requires a
successor released evaluator, external installation, independent commit-bound
verification, and a separately governed disposable pilot.
