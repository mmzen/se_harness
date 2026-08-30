# Phase 4 delegated workflow coordination

> Historical record from 2026-08-25, at `71efd2a`. Kept for the decision trail; it describes the tool as it was then. The `delegated-workflow` command and the three retired writing skills it describes were replaced by the [delegation class](../delegation-class.md) and the journaled apply.

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

This note explains the candidate `WO-AEX-007` coordinator. It does not approve
a delegation, authorize a Git or external action, verify a VREC, release an
evaluator, or activate Phase 4. Formal authority remains in approved artifacts,
the managed workflow, current repository state, and the exact released
evaluator.

## Closed operation surface

Workflow v4 activates exactly four coordinator operations:

| Operation | Current work-order state | Delegated right | Result |
| --- | --- | --- | --- |
| `delegated-work-order-start` | `approved` | `DR-WO-START` | `in_progress` plus a start lifecycle proof |
| `change-bundle-apply` | `in_progress` | started-work execution only | one broker receipt and new live-state anchor |
| `delegated-work-order-complete` | `in_progress` | `DR-WO-COMPLETE` | `implemented` plus a completion lifecycle proof |
| `delegated-vrec-prepare` | `implemented` | `DR-VREC-PREPARE` | a ready, undecided VREC and assurance packet |

`DR-RLS-PREPARE`, assurance decisions, release decisions, delivery, Git,
credentials, network access, child delegation, parallel writers, publication,
deployment, and other external actions are not activated.

## Coordinator sequence

For each operation, the coordinator independently resolves the current formal
delegation. A previous success creates no standing authority.

```text
mutation guard + current managed operation
                  |
                  v
stable live observation + formal delegation + current gates
                  |
                  v
short-lived envelope + external session + fresh nonce admission
                  |
                  v
existing lifecycle engine or separately guarded effect broker
                  |
                  v
fresh observation + exact paths + retained receipt/evidence
                  |
                  v
one governed continuation or accountable stop
```

The envelope path scope includes both the requested target paths and the
formally required evidence paths because envelope v2 requires evidence
containment. That does not widen the bundle effect: the coordinator separately
requires the evaluator-built bundle's `proposed_paths` to equal the requested
write set exactly, and the broker applies only those entries.

## Lifecycle proof, not another schema

Start, completion, and VREC preparation use existing canonical documents. A
`LifecycleProof` is an in-memory composition of:

- one `se-harness-execution-receipt-v1`;
- its `se-harness-autonomy-envelope-v2`;
- the exact before observation; and
- the exact after observation.

The composition avoids copying work-order fields into a new artifact. It lets
the next operation independently verify the receipt's envelope digest,
evaluator, repository, work order, lifecycle states, state digests, and prior
receipt anchor. CLI output retains all four documents; `prepare-vrec` requires
the complete completion proof rather than accepting a receipt by itself.

Effect proofs similarly retain the broker receipt and its before/after
observations. Completion requires an uninterrupted start-to-effect chain, a
fresh matching terminal observation, exact live Git changes, successful test
operations, passing gates, verified evidence digests, explicit deviations and
residual uncertainty, and no active effect journal.

## Commit-bound assurance stop

Completion never creates a commit. When commit-bound verification is required
and the exact completed candidate is still dirty, VREC preparation revalidates
the completion proof and live state, checks that no runtime recovery/session
conflict exists, and returns the managed `PROC-CANDIDATE-COMMIT` packet. The
packet requests only authorization to create the exact candidate commit.

After that separately authorized commit exists, preparation requires a clean
worktree and proves that repository, evaluator, governance, and regular-file
content still match the completed candidate while Git `HEAD` has changed. It
then delegates to the existing provenance writer, creates one `ready` VREC and
evaluator-evidence file, and projects the managed `DR-VREC-DECIDE` packet with
complete reject and supersede alternatives. It records no `verified_at`,
`verified_by`, pass, fail, waiver, or assurance lifecycle event.

## Failure and recovery behavior

Missing, altered, skipped, or foreign proof links; stale live state; failed or
not-assessable gates; unsuccessful tests; invalid evidence; undeclared paths;
wrong evaluator/delegate; active journals; and runtime conflicts stop before
the next governed mutation.

Receipt shapes are prevalidated before lifecycle writes. If a lifecycle or
VREC write occurred but its post-state cannot be proved, the coordinator marks
external runtime recovery as required and closes the session. Later sessions
remain blocked until accountable recovery acknowledges canonical state. The
coordinator does not reverse an illegal lifecycle edge, guess at restoration,
or label an uncertain result complete.

## Interfaces and activation boundary

The Python API is `se_harness.delegated_workflow`. The CLI surface is
`harnessctl delegated-workflow {catalog,execute,prepare-vrec}`; exact options
are listed in the [`harnessctl` reference](../harnessctl-reference.md).

The implementation is candidate source stacked on the independently verified
`WO-AEX-006` commits. It must still receive commit-bound independent assurance,
candidate-package qualification, a separately governed successor release,
external installation, and disposable pilot evidence before it can govern a
real target. It must not govern its own construction.
