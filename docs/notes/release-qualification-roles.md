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

## The five operations

| Operation | Evaluator | Target | Meaning of a pass | Independence |
| --- | --- | --- | --- | --- |
| `released-root` | exact released evaluator named by the root lock | installed repository root | managed files and complete graph agree with their owning evaluator | `released-evaluator` |
| `predecessor-view` | exact external predecessor selected by governed release evidence | deterministic predecessor-compatible view | the immutable predecessor accepts only the view it is able and authorized to parse | `external-predecessor` |
| `complete-candidate` | candidate code | complete candidate checkout at one commit | the candidate accepts its own full current graph | `candidate-controlled` |
| `candidate-package` | exact released verifier | exact candidate wheel bound to a commit | the released verifier's fixed black-box contract accepts the installed candidate | `released-verifier` |
| `public-install` | exact package installed from the public wheel | released record, acquired wheel, installed payload, and CLI | the public bytes and installed behavior agree with the released distribution | `public-install-observation` |

These claims are deliberately separate. A successful `complete-candidate` result cannot be renamed into independent package evidence. A successful public installation cannot prove predecessor compatibility or root ownership.

## Typical workflow order

```text
candidate checkout
  -> complete-candidate
  -> build candidate wheel
  -> candidate-package
  -> accountable verification and release decisions
  -> predecessor-view during release/publication preparation where required
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

## Initial public-0.6.0 bootstrap

Public 0.6.0 already contains the hardened `accept-candidate` contract, but it was released before `harnessctl qualify` existed. Immutable released bytes cannot contain a future command.

For the first deployment only, candidate-package CI therefore:

1. downloads exact public 0.6.0;
2. verifies its fixed wheel and installed-payload SHA-256 values;
3. verifies its isolated interpreter and entry point;
4. invokes only its existing `accept-candidate` command;
5. binds the exact candidate wheel digest and commit; and
6. retains the original `se-harness-functional-acceptance-v1` result under a clearly named legacy-bootstrap artifact.

That output is not relabeled as `se-harness-release-qualification-v1`. Another verifier version, digest, command, contract, schema, or artifact label fails the workflow. Once a released verifier exposes `qualify candidate-package`, the workflow must move to the typed operation and a later governed change removes the bootstrap path.

Newly built versions keep `accept-candidate` only as a one-cycle alias to the typed handler. That alias is different from immutable public 0.6.0's historical command.

## Diagnostic commands

`doctor`, `validate`, and `identity` remain useful low-level diagnostics. A typed handler may use them internally, and a workflow may retain additional diagnostic output. Their output alone is not role-bound release qualification because it does not establish the complete evaluator/target/independence contract.

## Root/template adoption boundary

The candidate managed-workflow template uses `qualify released-root`, so a future governed repository upgrade installs the role-specific health check. The currently installed root workflow remains owned by its existing public 0.6.0 lock and is not edited by this change. Template drift is expected until a separately authorized upgrade adopts the new released bytes.
