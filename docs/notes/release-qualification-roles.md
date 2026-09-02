# Release qualification roles

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operating guidance. Qualification results are technical evidence. They do not approve work, verify a VREC, release an RLS, publish, deploy, or upgrade a repository root.

## Why the roles exist

A validator can be correct and still be used in the wrong place. During release 0.6.0, similar commands were run by different versions of SE Harness against roots, complete candidates, compatibility views, built wheels, and public installations. A pass or failure did not clearly state which relationship had been tested.

`harnessctl qualify` makes that relationship part of the command. Each operation fixes:

- who evaluates;
- what is evaluated;
- which identity must be proven first;
- which checks run;
- whether the result is independent; and
- which result schema is retained.

## The four operations

| Operation | Evaluator | Target | Meaning of a pass | Independence |
| --- | --- | --- | --- | --- |
| `released-root` | exact released evaluator named by the root lock | installed repository root | managed files and complete graph agree with their owning evaluator | `released-evaluator` |
| `complete-candidate` | candidate code | complete candidate checkout at one commit | the candidate accepts its own full current graph | `candidate-controlled` |
| `candidate-package` | exact released verifier | exact candidate wheel bound to a commit | the released verifier's fixed black-box contract accepts the installed candidate | `released-verifier` |
| `public-install` | exact package installed from the public wheel | released record, acquired wheel, installed payload, and CLI | the public bytes and installed behavior agree with the released distribution | `public-install-observation` |

These claims are deliberately separate. A successful `complete-candidate` result cannot be renamed into independent package evidence. A successful public installation cannot prove root ownership.

A fifth operation, `predecessor-view`, once qualified a deterministic predecessor-compatible view against an exact external predecessor evaluator. It existed only for the 0.5.0→0.6.0 handover and was retired under `WO-REB-028` (`ADR-REB-012`, amending `ADR-REB-009`); the retained 0.6.0 results remain valid history. Predecessor-to-successor agreement is now shown by the real upgrade rehearsal (`repository_tools/upgrade_rehearsal.py`, `WO-ECP-010`), not by a `qualify` operation.

## Typical workflow order

```text
candidate checkout
  -> complete-candidate
  -> build candidate wheel
  -> candidate-package
  -> accountable verification and release decisions
  -> publish exact released bytes
  -> public-install
  -> later, separately governed released-root adoption
```

The order does not make transitions automatic. Accountable owners still review the applicable formal evidence and make each lifecycle or external-action decision separately.

## Canonical results

The typed operations emit `se-harness-release-qualification-v1`. A result includes:

- the operation and completion state;
- overall pass or failure;
- the fixed independence classification;
- stable evaluator and target identities;
- ordered fixed checks; and
- an explicit statement that the result grants no lifecycle or external-action authority.

An optional `--output` must name a new file outside the inspected repository. Existing evidence is never overwritten. The same result is rendered as JSON with `--json` or as concise human text without it.

## The retired public-0.6.0 bootstrap

Public 0.6.0 was released before `harnessctl qualify` existed, so the very first deployment accepted the candidate through 0.6.0's own digest-bound `accept-candidate` contract and retained that `se-harness-functional-acceptance-v1` result under a clearly named legacy-bootstrap artifact. That path expired by its own terms once a released verifier exposed the typed command (0.7.0 did), and `WO-REB-031` removed it: candidate-package CI now runs `qualify candidate-package` unconditionally and retains only the canonical `se-harness-release-qualification-v1` result. The retained bootstrap evidence of those first runs stays valid as history and is never relabeled.

Newly built versions kept `accept-candidate` only as a one-cycle alias to the typed handler; that alias was removed after 0.11.0 (`WO-ECP-019`) and the command now exits with status 2 naming `qualify candidate-package`.

## Diagnostic commands

`doctor`, `validate`, and `identity` remain useful low-level diagnostics. A typed handler may use them internally, and a workflow may retain additional diagnostic output. Their output alone is not role-bound release qualification because it does not establish the complete evaluator/target/independence contract.

## Root/template adoption boundary

The managed-workflow template uses `qualify released-root`, and this repository's installed root workflow has run it since the root adopted exact public 0.7.1 (`WO-HUP-007`); every later root adoption, through `WO-HUP-015` and exact public 0.14.0, carried it forward. A candidate template may still lead the installed root: that drift is expected until a separately authorized upgrade adopts the new released bytes, and the installed root workflow is never edited by a candidate change.
