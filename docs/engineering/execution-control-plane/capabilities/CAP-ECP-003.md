+++
id = "CAP-ECP-003"
type = "capability"
title = "The shipped product carries only machinery a consumer repository needs"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
derives_from = ["INT-ECP-001"]
+++

# Capability: The shipped product carries only machinery a consumer repository needs

## Actor and need

A consumer repository owner who installs the released evaluator and runs
`harnessctl init`, and the coding agents who then work in that repository.
Today `init`, a commit, and `doctor` exit 1 in every fresh repository,
because `se_harness/hash_bound_classes.json:19-32` and
`templates/repository/standard/gitattributes.fragment:4-6` declare a
hash-bound class for files that exist only in this repository (complexity
audit P0-1; the 0.7.1 wheel carries identical bytes). Six `RLS-SEH-*`
identifiers of this repository's own releases are hard-coded in three
generic files (audit P1-2). `qualify predecessor-view` in the wheel imports
`repository_tools`, which is not packaged (2026-08 agentic execution review,
section 5, weakness 5).

The same consumer receives Phase 4 delegated execution, 8,766 lines and 39%
of the package, reachable through `harnessctl delegated-workflow` and never
run on a real work order; its envelope carries a nonce ledger, a five-minute
lifetime, revocation, and a retry ordinal for a token that never leaves the
process that minted it (`se_harness/cli.py:1259-1304`; audit P0-5, P1-3).
Three shipped writing skills inject a stub client and print
`"evaluator_invoked": false` while their `SKILL.md` says they invoke the
evaluator (`.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`).
A frontier agent must recognise a second execution model and ignore it.

What the consumer does need from that stratum is the crash-safe part: the
journaled apply with rollback and a `human-recovery-stop`
(`se_harness/effect_broker.py:1029-1160`; `tests/test_effect_broker.py:308-344`),
applied to the harness's own multi-file writes.

## Capability statement

`A consumer repository owner can install the released evaluator, initialise
a repository, commit, and pass doctor, and can rely on a distributed product
whose code, templates, and scripts name no record of this repository's
releases, whose skills invoke the evaluator they describe, whose multi-file
writes are journaled with rollback, and whose CLI and public API expose no
autonomy-envelope apparatus.`

## Boundaries

The capability bounds what is distributed. It does not change the released
evaluator boundary, the mutation guard, the hash-bound class mechanism as
such, or the identity layers; it removes declarations that hold only in this
repository. It does not decide whether this repository keeps private tooling
under `repository_tools/` for its own releases; it decides that such tooling
is not the product. It retires skills rather than rewriting them; a skill
returns to the template when it invokes the evaluator for real. Nothing here
rewrites a verified or released record; the records that today are exempt by
identifier stay exempt through data.

## Outcomes

- A fresh consumer repository: `init`, commit, `doctor` exits 0 with no
  failed check, on Linux and Windows, from the released wheel.
- No product code, template, or installed script names an `RLS-SEH-*`
  identifier; the same records stay exempt through the specification's own
  rule.
- The distributed template carries no skill whose script cannot invoke the
  evaluator for the operation its `SKILL.md` describes.
- The product CLI and public Python API expose no envelope, nonce, lifetime,
  or revocation interface; the second execution model is gone.
- Every harness-owned multi-file write goes through one journaled apply with
  rollback and a human-recovery stop, so the crash-safety Phase 4 built is
  kept where the harness itself writes.

## Candidate requirements

`REQ-ECP-012`, `REQ-ECP-013`, `REQ-ECP-014`, `REQ-ECP-017`, `REQ-ECP-018`.
