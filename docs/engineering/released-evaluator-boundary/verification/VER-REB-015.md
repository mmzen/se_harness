+++
id = "VER-REB-015"
type = "verification"
title = "Independent evidence for the typed-only acceptance path"
status = "draft"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
verifies = ["REQ-REB-031"]
+++

# Verification Contract: Independent evidence for the typed-only acceptance path

## Independence

Expected values derive from `REQ-REB-031` and the `REB-BFH-` rules of
`SPEC-REB-016`, never from the changed files. The workflow-conformance tests
read the workflow text; the facts tests drive
`repository_tools.evaluator_facts` against this repository's declared root
and against synthetic roots; the lane evidence is the pull request's own run.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-031` single path | test | workflow text, `candidate-package` job | exactly one acceptance invocation, the typed operation; no `accept-candidate`, no `qualify --help` probe, no dispatch |
| `REQ-REB-031` no legacy fact | test | `evaluator_facts.derive` on this root and on a synthetic root | no acceptance-contract attribute or output line; every other fact unchanged and equal to the lock's |
| `REQ-REB-031` no legacy retention | test | workflow text | no `candidate-package-legacy-bootstrap` artifact name; no `se-harness-functional-acceptance-v1` retention; no `RELEASED_ACCEPTANCE_CONTRACT_SHA256` |
| `REQ-REB-031` literal-free | existing test | `test_no_predecessor_literal_remains_in_the_repository_owned_workflows` | unchanged and passing |
| `REQ-REB-031` fail closed | existing tests | `PRE0nn` derivation failures | unchanged and passing |
| `SPEC-REB-016` tombstone unchanged | existing tests | `accept-candidate` refusal tests and note rows | unchanged and passing |
| `SPEC-REB-016` this repository | lane reading | the pull request's candidate-evidence run | `candidate-package` green with the typed result retained |

## Acceptance scenarios

1. Grep the workflow for `accept-candidate`, `qualify --help`,
   `RELEASED_ACCEPTANCE_CONTRACT_SHA256` and `legacy-bootstrap`: zero hits;
   the conformance test asserts the same and fails on reintroduction.
2. Derive facts on this repository (declared root 0.11.0): the fact set
   carries version, wheel, wheel digest and payload digest, and no
   acceptance-contract value in any form.
3. The pull request's `candidate-package` lane passes using only the typed
   operation.

## Evidence retention

Under `docs/engineering/released-evaluator-boundary/evidence/WO-REB-031/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the exact
released evaluator, se-harness 0.11.0, installed outside the checkout.

## Residual uncertainty

The lane proof shows the typed path on the current pinned verifier only; a
future root older than 0.7.0 cannot occur because the lock only moves
forward, and the floor decision of 2026-08-30 makes that irreversibility a
stated boundary rather than an assumption.
