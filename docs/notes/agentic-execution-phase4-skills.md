# Phase 4 writing-skill integration

<!-- Target expertise: 5/10. This is operator guidance, not authority. -->

This note explains the candidate `WO-AEX-008` skill and package integration.
It does not approve delegation, install or activate an evaluator, authorize
Git, decide assurance, release software, or permit external action. Formal
artifacts, current repository state, the managed lock, and the exact released
evaluator remain authoritative.

## What changed

The three explicit-only writing cores move from contract `1.0.x` and
`se-harness-skill-contract-v2` to major version `2.0.0` and
`se-harness-skill-contract-v3`:

| Skill | Evaluator interface | Requested Phase 4 operations | Terminal stop |
| --- | --- | --- | --- |
| `harness-draft-change` | `delegated-workflow execute` | delegated start, change-bundle apply, delegated completion | Git/action packet, then accountable draft review |
| `harness-execute-work-order` | `delegated-workflow execute` | delegated start, change-bundle apply, delegated completion | exact candidate-commit authorization |
| `harness-prepare-assurance` | `delegated-workflow prepare-vrec` | delegated VREC preparation | required Git commit or independent assurance decision |

`harness-orient` remains byte-identical on its v1 contract. The Phase 3
writing digests remain valid historical identities for repositories that have
not upgraded; they do not identify the Phase 4 procedures.

## Client boundary

Each v3 contract identifies:

- workflow schema `se-harness-workflow-v4`;
- request schema `se-harness-evaluator-client-request-v1`;
- result schema `se-harness-evaluator-client-result-v1`;
- the exact interface and underlying operation subset;
- evaluator ownership of bundle construction and target writing;
- `direct_target_writes: false`; and
- required canonical restitution.

The helper receives a closed argument vector, validates explicit activation,
the selected interface, delegation-evidence digest, state and path shape, and
the exact four-operation catalog. It then invokes one evaluator client. No
helper accepts a target-write callback. Local validation is defense in depth:
it cannot admit delegation, apply a bundle, transition lifecycle state, attest
completion, or validate its own result as authority.

Candidate bytes are produced only in the isolated proposed workspace. The
evaluator re-observes the target, resolves formal delegation, constructs the
bundle, admits the envelope, applies the transaction, validates receipts and
completion proof, and returns a decision packet. A provider's filesystem
permission never substitutes for those checks.

## Capability and compatibility

The portable compatibility floor remains 0.6.0; the contract does not select a
successor version. Capability is checked independently. Exact public 0.6.0 has
no `delegated-workflow` command, so these candidate v3 skills stop before any
effect when paired with that evaluator. This is the expected pre-activation
behavior, not a fallback to direct writing.

Phase 4 becomes usable in a repository only after all of these separately
governed steps:

1. complete commit-bound assurance of the candidate;
2. create and approve a successor release without changing this work order;
3. install the exact released evaluator outside the target;
4. explicitly apply the transactional repository upgrade; and
5. qualify a disposable target before considering self-hosting.

Copying a core, changing a lock, installing candidate source, or granting host
tools does not activate Phase 4.

## Host parity and stops

`.agents/skills/<name>` remains the only complete core. Codex uses the managed
explicit-only policy. Claude Code uses one same-named discovery adapter with
model invocation disabled; the adapter loads the canonical core and contains
no workflow, permissions, scripts, or second authority source.

Every client stops without a governed effect on missing capability, implicit
activation, invalid delegation, session conflict, direct-write mode, path
drift, incomplete proof, or failed restitution. Execute stops before Git.
Assurance preparation either requests the separately authorized exact commit
or returns an undecided ready VREC and stops for the assurance owner. Neither
path verifies the implementation or continues to release.

## Package qualification

The successor package inventory includes the observer, authority, bundle,
broker, runtime, delegated-workflow and skill-contract modules; managed JSON
contracts; all four canonical cores; three Codex policies; and four thin Claude
adapters. Source, wheel, fresh installation, init/adopt/upgrade, managed-lock,
customization-conflict, rollback, nested discovery, and explicit/implicit
activation tests bind those bytes. Candidate qualification is evidence for
later assurance only; it is not a release or activation decision.
