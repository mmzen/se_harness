# Bounded evaluator recovery runbook

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Maintainer-only recovery guidance. This document is not standing authorization. It does not authorize a release, publication, tag, deployment, lifecycle transition, or evaluator upgrade.

## 1. Applicability

Use this runbook only when the repository owner, release owner, security owner, and engineering owner have recorded that the normal released-evaluator path is deadlocked and cannot restore the standard lifecycle. Ordinary upgrade, release, or CI failures do not qualify. Stop when the normal path remains usable.

The declaration must name the observed deadlock, affected repository, bounded recovery objective, accountable owners, time window, and actions that remain prohibited. Link the factual 0.5.0 incident analysis as precedent, not as reusable authority.

## 2. Decision rights

The recorded declaration may permit maintainers to prepare and review a bounded technical recovery. It cannot grant product approval, commit-bound verification, release approval, production credential access, publication, tag creation, deployment, artifact disposition, or root adoption. Each external action still needs immediate action-time authority from its normal accountable owner and protected environment.

Technical output is evidence, not retrospective authorization. Never describe an emergency action as having been authorized earlier than it was.

## 3. Prerequisites

- Preserve the operational repository and current standard lock as read-only evidence.
- Record the exact failing normal controls and the last known released evaluator identity.
- Confirm that one full candidate commit and one exact distribution can be selected without a mutable ref.
- Prepare an isolated build/acquisition directory, fresh external evaluator environment, rollback snapshot location, and evidence directory.
- Require security and release-owner review before any real credential-bearing step.

Create the external evaluator environment with an ordinary `python -m venv` outside the operational checkout, and refer to it afterwards by its own lexical entry point — `bin/python` on POSIX, `Scripts/python.exe` on Windows. The declared interpreter-safety rule derives the environment root from that lexical path, so a recovery directory reached through a symbolic link or a Windows directory junction is refused even though the interpreter behind it is correct. Under time pressure that reads as an unrelated tooling failure; place the environment on a real path instead of relaxing the check.

Stop on ambiguous source, digest disagreement, candidate checkout imports, expanded product scope, unavailable protected publishing, or any request to weaken identity checks.

## 4. Immutable selection

Select one full Git object ID. Record the object format, tree identity, reachability basis, and archive digest before building or acquiring anything. Do not use a branch, pull-request head, tag without verified dereference, abbreviated commit, newest attempt, or conversational “current” candidate.

Select one exact distribution filename and SHA-256. Multiple plausible candidates or competing chains stop for accountable disposition; tooling must not choose a winner.

## 5. Isolated acquisition or build

Use a clean detached worktree or immutable source archive outside the evaluator environment. Build without importing the operational checkout. Record tool versions, file list, wheel digest, and candidate commit. Candidate output remains non-authoritative until a separately authorized publication and public-install proof complete.

For rehearsal only, use the synthetic local archive and simulated publication implemented by `harnessctl rehearse-recovery`. It performs no network operation.

## 6. Credential boundary

A real publication requires short-lived GitHub OIDC Trusted Publishing, least permissions, protected-environment approval, and a separate action-time release-owner decision. Long-lived tokens, copied credentials, local credential files, broad workflow permissions, and credentials made available before digest verification are prohibited.

The rehearsal refuses recognized publication credential signals. Never add an option that suppresses that refusal.

## 7. Public-install proof

After separately authorized real publication, download public bytes into a fresh directory, independently reconcile the selected SHA-256, and install those exact bytes in a fresh external environment. Prove version, archive name and digest, installed payload digest, normalized origins, entry point, isolated interpreter, disabled user site, absent `PYTHONPATH`, and checkout exclusion.

The interpreter facts in that proof are the ones runtime identity now records: whether the entry point is itself a symbolic link, the position class of its resolved target relative to the expected and checkout roots, and the target's SHA-256. Read them with the platform in mind. A POSIX recovery environment normally reports the entry point as a link and its target as `outside-declared-roots`, because `bin/python` points at the system interpreter; that is the accepted shape, not a finding. A Windows `Scripts\python.exe` normally reports no link and `within-expected-root`. What fails the proof on either platform is a target inside the operational checkout, because that would mean the recovery evaluator is backed by candidate bytes.

An index version string, local wheel, editable install, source checkout, or same-version import is not public-install proof.

## 8. Bounded root transaction

Prepare a distinct approved or in-progress evaluator-upgrade work order containing `[evaluator_upgrade]` with schema `se-harness-evaluator-upgrade-v1`, `scope = "standard-root-only"`, the exact prior lock SHA-256, target version/payload/archive identity, `publication = "immutable"`, and the accountable authorizer.

Review `harnessctl upgrade REPOSITORY` before apply. A real transition then uses the exact external target evaluator and a work-order-keyed path:

```text
harnessctl upgrade REPOSITORY --apply --work-order WO-... --evidence-output docs/engineering/DOMAIN/evidence/WO-...-evaluator-upgrade.json
```

This command is illustrative syntax, not authority to execute it. The transaction rechecks the plan, validates the old lock and target evaluator against the approved packet, atomically updates managed files plus lock and evidence, proves no-op replay, and restores its pre-write snapshot on failure.

## 9. Restoration

Recovery is incomplete until all of the following are true:

- standard config and schema-3 lock select the exact public evaluator;
- the normal released-evaluator workflow, candidate-evidence workflow, and publisher are restored;
- temporary publisher, recovery workflow, alternate profile, descriptor, and bootstrap paths are absent;
- product release records and candidate versions were not changed by root adoption;
- ordinary upgrade replay is a no-op.

## 10. Verification

Run `doctor`, artifact validation, inspection, dashboard generation, supported-runtime tests, active-surface scanning, and hosted checks from the correct external released evaluator. Retain exact commands, exit codes, evaluator evidence, lock identities, changed paths, no-op result, and workflow results. Commit-bound assurance remains a separate VREC decision.

Before any real recovery, rehearse with an empty directory outside the operational repository:

```text
harnessctl rehearse-recovery DISPOSABLE_OUTPUT --repository REPOSITORY --candidate-commit FULL_COMMIT --target-version SYNTHETIC_VERSION
```

Review `rehearsal-report.json`. It must show candidate-contamination rejection, stale/mismatched-identity rejection, non-automatic conflict stop, exact interrupted-transaction rollback, restored workflows/invariants, and every external action as false.

## 11. Rollback

Before root mutation, retain the exact prior config, lock, managed-path snapshot, evaluator archive identity, and restoration command review. Any write or postcondition failure must restore the complete snapshot. If restoration is incomplete, stop all further action, preserve both states, and escalate to the repository and security owners; do not retry with broader permissions or candidate code.

After a successful but later-disputed transition, rollback is a new separately approved standard-root transaction selecting an exact previously published evaluator. It is not an unreviewed file copy.

## 12. Evidence retention

Retain the declaration, owners, immutable commit, archive and payload hashes, acquisition/build transcript, public-install evidence, prior lock hash, reviewed plan, changed paths, transaction record, rollback observation, no-op replay, doctor/validation/inspection/dashboard results, runtime matrix, hosted checks, credential and permission review, absence scan, and every action not performed. Use work-order-keyed repository paths and normalized facts without usernames, home paths, tokens, or environment dumps.

## 13. Incident follow-up

Create a factual, non-authoritative incident record after recovery. Record what happened, when authority was obtained, technical deviations, incomplete stages, and residual risks. Preventive changes require ordinary intent-through-work-order governance. Emergency activity is not retroactively normalized and does not become a reusable profile.

## 14. Explicit prohibitions

- No candidate source or locally built wheel acts as the released evaluator.
- No mutable ref, automatic newest-chain selection, lifecycle mutation, deletion, rejection, or supersession.
- No product release and evaluator adoption in one inferred transaction.
- No long-lived credential, unprotected publisher, broad permission, hidden network mutation, tag, release, or deployment in rehearsal.
- No alternate recovery installation profile or permanent bypass.
- No real command execution merely because this runbook or a green rehearsal exists.
