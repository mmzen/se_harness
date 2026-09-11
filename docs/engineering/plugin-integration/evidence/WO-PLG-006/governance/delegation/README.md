# WO-PLG-006: delegated execution preparation

The operator selected this work order and the execution delegation class on
2026-09-11. The released evaluator records approval separately. The requested
start, completion and ready-record preparation remain subject to DR-015.
Verification of the result and merge are separate human decisions.

## What this packet changes

- Add the requested execution delegation to the existing work order.
- Reserve VREC-PLG-013 and its evaluator sidecar as exact future output paths.
- Correct the obsolete description of the specification as blocked/unapproved.

The implementation scope and approved requirements, specification, architecture,
verification contract and compatibility decision remain in force. No adapter code
or verification record is created by this packet.

## Implementation preparation

The available shared skills are `setup`, `change`, `evidence`, `harness-orient`
and `harness-operator-brief`. Qualify an explicit selection in an already
initialized disposable repository. Repository connection and ownership migration
from WO-PLG-009 are separate work.

An initialized repository may still contain managed copies of retained skills.
C01 must not claim compatible activation of overlapping skills before a
supported ownership-migration route exists.

DEC-PLG-002 accepts Claude Code 2.1.266 on Windows with Python 3.14.6 and evaluator
0.16.0. New host acceptance must use that recorded profile or obtain a separate
technical decision. Repository governance is evaluated by released 0.17.0;
that does not establish a new supported plugin profile.

Implement the native manifest and inline shell bindings in this WO's host
directory. Reuse the unchanged shared session/tool handlers. Put focused tests,
disposable assembly fixtures and acceptance runners in its existing test scope.
The package builder's companion-host fixture must be explicitly inert; it cannot
establish support for the other host.

VER-PLG-006 requires C01-C12, including real-host timeout, startup failure,
denial and independently observed target effects. A missing or failed check is
not a passing qualification. Shared-code repairs or broader profiles require
separate authority.

## Start boundary

Integrate this approval/delegation packet into `main` first. Then refresh the base
and obtain a successful required GitHub `validate` check for the implementation
head. Only then may `delegated-executor` start the selected work order.
Branch-only delegation is insufficient; there is no fallback to a human actor.

## Observed governance result

The released 0.17.0 evaluator applied work-order approval. The work order is **approved**, with implementation still not started. Review preflight passes. The retained delegated-start preview refuses the branch-only class with `WEX-ECP-022`; no transition to `in_progress` was applied.

`validation-summary.json` records the definition checks. The approval and start-preview JSON files retain the original evaluator results.
