+++
id = "CAP-ECP-003"
type = "capability"
title = "The shipped product carries only machinery a consumer repository needs"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-27"
updated = "2026-10-17"

[relations]
derives_from = ["INT-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "product-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Capability: The shipped product carries only machinery a consumer repository needs

## Selected WO-ECP-007 revision

This revision applies only to remaining work under WO-ECP-007. The [preserved accepted version](../evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/CAP-ECP-003.txt) has complete-file SHA-256 `7688ca3c641dd84312d304c688f67d86e075cd25b9498e89064a36b161473d37` and Git blob `c661f2c22356d86bd41840b814d8be331de7afb6` at commit `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38`. The [activation receipt](../evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json) records the actual human authority and before/after identities. Without that recorded authority this replacement does not govern work. Original lifecycle events remain unchanged; this is not a native evaluator revision event. Earlier completed work and evidence retain their original definition meaning. Retained historical problem descriptions are context, not claims about current code. Unrelated skills and capabilities retain their existing obligations.

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
a repository with only selection files, select Git evidence integration (or an
equivalent owner rule), commit, and pass doctor. The distributed product has no
repository-specific record exception in executable code, templates or scripts.
Its skills invoke the evaluator they describe, its multi-file writes are
journaled with rollback, and its CLI and public API expose no autonomy-envelope
apparatus.`

## Boundaries

The capability bounds what is distributed. It does not change the released
evaluator boundary, the mutation guard, the hash-bound class mechanism as
such, or the identity layers; it removes declarations that hold only in this
repository. It does not decide whether this repository keeps private tooling
under `repository_tools/` for its own releases; it decides that such tooling
is not the product. It retires skills rather than rewriting them; a skill
returns to the template when it invokes the evaluator for real. Nothing here
rewrites a verified or released record; legacy unbound release records follow the accepted evaluator-evidence floor
under SPEC-LRE-002. Do not restore the retired declaration mechanism.

## Outcomes

- A fresh consumer repository: minimal `init`, explicit Git evidence setup, commit, `doctor` exits 0 with no
  failed check, on Linux and Windows, from the released wheel.
- Executable product code, templates and generated UI carry no repository-specific
  artifact-ID exception. Historical documentation references are not executable policy.
  Historical unbound releases follow SPEC-LRE-002 without an ID list.
- The distributed template carries no skill whose script cannot invoke the
  evaluator for the operation its `SKILL.md` describes.
- The product CLI and public Python API expose no envelope, nonce, lifetime,
  or revocation interface; the second execution model is gone.
- Every harness-owned multi-file write goes through one journaled apply with
  rollback and a human-recovery stop, so the crash-safety Phase 4 built is
  kept where the harness itself writes.

## Candidate requirements

`REQ-ECP-012`, `REQ-ECP-013`, `REQ-ECP-014`, `REQ-ECP-017`, `REQ-ECP-018`.
