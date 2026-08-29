# The delegation class

<!-- Target expertise: 4/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Non-authoritative note. The rules are `REQ-ECP-011` and `SPEC-ECP-006`
> (`ECP-DLG-001` to `ECP-DLG-010`); the decision-right catalog is
> `docs/engineering/DECISION_RIGHTS.md` (`DR-015`).

## What it is

A work order can say that its three mechanical decisions — start it, mark it
implemented, prepare its verification record — may be taken by a non-human
actor, as long as the pull request's required check is green for the exact
commit the actor stands on. Everything else stays a human decision: approving
definitions and work orders, verifying records, releasing, selecting work,
and merging.

The class is one table in the work order's front matter:

```toml
[delegation]
class = "execution"
```

Approving a work order that carries the table *is* the act of delegating. The
evaluator reads the class from the **base** of the pull request, so a branch
cannot add the table to itself and gain the rights.

## What the actor does

Nothing new. The actor keeps running `harnessctl check --artifact WO-…` and
does what the restitution says:

- `decision_required` names `delegated-executor` and `command_or_response`
  is a **command** — the gate is green and the decision is the actor's; it
  runs the command (`transition … --decision WO-…=delegated-executor --apply`,
  or `capture-verification … --owner delegated-executor`).
- `decision_required` names `delegated-executor` and `command_or_response`
  is a **response** naming the check, the head and the conclusion — the gate
  is not green; the actor waits for or repairs the check. There is nothing
  for a human to decide here.
- `decision_required` names a human role, or is `null` — as today: the actor
  hands off.

The lifecycle event the delegated route writes carries the class, the
check-run id and the head sha, so anyone reading the work order later sees
exactly what unlocked the decision.

## What the evaluator checks, in order

1. The decision right is one of `DR-WO-START`, `DR-WO-COMPLETE`,
   `DR-VREC-PREPARE`; any other right for the `delegated-executor` role is
   `WEX-ECP-022`.
2. The work order declares the class and carries it at the base of the pull
   request (`git merge-base HEAD <base_ref>`); otherwise `WEX-ECP-022`.
3. The gate: the required check's conclusion for the candidate head, read
   from the configured source by commit id; anything but `success` — a
   failure, a pending run, a missing check, an unknown head, a source error
   — is `WEX-ECP-040` naming the head and the conclusion observed. No
   request-side flag, environment variable, token or actor name is consulted.
4. For `DR-WO-COMPLETE`, the same handoff gate the human decision passes:
   the change set must be inside `[execution_scope].paths`
   (`QGP-G4I-PATHS`) before the CI gate is read.

## Configuring the gate

The gate source is owner content in `.engineering-harness.delegation.toml`,
beside the managed `.engineering-harness.toml` and never inside it (the
managed file is hash-locked; editing it reads as customization):

```toml
[delegation]
gate_source = "github-checks"   # or "local-file" for tests and rehearsals
check_name = "validate"         # the required check's name
repository = "owner/name"       # optional; derived from origin when absent
base_ref = "origin/main"        # where the class is read from
# local_file = "gate.json"      # {"sha": ..., "conclusion": ..., "check_run_id": ...}
```

`github-checks` reads `GET /repos/{repository}/commits/{sha}/check-runs`
filtered by `check_name`, with `GITHUB_TOKEN` from the environment when
present. `local-file` exists for tests and rehearsals; used elsewhere it
prints `W-ECP-005` on every read.

## The one step the harness cannot take

The class makes the evaluator refuse; it does not make GitHub refuse. A
branch-protection rule on the default branch that requires the managed check
is what turns the boundary into prevention rather than reporting, and only
the repository owner can set it.

## Where it came from

`ADR-ECP-002` chose to enforce scope at the Git boundary instead of through
the Phase 4 broker; `WO-ECP-006` removed the broker and kept the journaled
apply; `WO-ECP-018` added this class; the shared journaled write path
(`REQ-ECP-017`) follows.
