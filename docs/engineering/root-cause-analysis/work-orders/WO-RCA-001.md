+++
id = "WO-RCA-001"
type = "work_order"
title = "Publish the 0.5.0 release-governance RCA"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[assurance]
commit_bound_verification = "required"
rationale = "Maintainers and future governing work will rely on the RCA's causal analysis, immutable evidence, and authority-boundary statements as trusted engineering documentation."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-RCA-001", "REQ-RCA-002", "REQ-RCA-003"]
specifications = ["SPEC-RCA-001"]
architecture = ["ARCH-RCA-001"]
verification = ["VER-RCA-001"]
+++

# Work Order: Publish the 0.5.0 release-governance RCA

## Authorization

On 2026-08-20, the accountable owner instructed: `I approve INT-RCA-001, CAP-RCA-001, REQ-RCA-001 through REQ-RCA-003, SPEC-RCA-001, ARCH-RCA-001 including its no-significant-decision assessment, VER-RCA-001, and WO-RCA-001 for implementation`. This decision approves the complete governing chain and authorizes only the bounded local implementation below after successful start preflight. It does not authorize a candidate commit, branch push, pull-request update or readiness transition, issue edit, merge, verification transition, release, publication, deployment, or operation.

The implementation agent then ran the released `0.5.0a1` evaluator outside the checkout with `harnessctl preflight . --work-order WO-RCA-001 --phase start --json`. Preflight returned `ready: true` with no diagnostics and a complete reading manifest. After reading that manifest, the agent transitioned this work order to `in_progress` before changing the authorized implementation surface.

## Objective

Publish one reviewed, evidence-backed, non-authoritative RCA for the 0.5.0 release-governance deadlock and connect it to issue #81 without implementing the issue's preventive actions or altering the restored product, evaluator, release, and publication boundaries.

## In scope

- Add `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md` conforming to `SPEC-RCA-001`.
- Retain this complete root-cause-analysis governing packet.
- Add the new domain to `docs/engineering/README.md` and correct its introductory description from specially self-governing to standard governed.
- Reconcile every material commit, Actions run, public release, checksum, attestation, and restored-CI claim.
- Retain work-order-keyed verification evidence.
- After separate external-action authority, commit and push the bounded candidate, open a PR declaring `Harness-Work-Order: WO-RCA-001`, and update issue #81 with an immutable RCA link.

## Out of scope

- Implementing any preventive action listed in the RCA or issue #81.
- Changing source, tests, managed templates, lock data, CI, publisher behavior, package metadata, version, tags, public releases, Pages, or root evaluator configuration.
- Editing, promoting, rejecting, superseding, or deleting the abandoned local 0.5.0 drafts.
- Retrospectively authorizing, verifying, or releasing `0.5.0a1` or `0.5.0` through the normal formal lifecycle.
- Merging the later PR, transitioning a VREC, preparing a release, publishing, deploying, or operating a service.

## Authorized decision envelope

After approval, the implementation agent may refine RCA prose, table layout, and link labels while preserving the specified causal meaning, exact identities, non-authority statements, and required sections. It may correct a factual identifier only after independent reconciliation. It may not add a new root cause, expand preventive scope, change lifecycle state outside this packet, or modify a prohibited surface without escalation.

## Constraints

- Use only the released `0.5.0a1` evaluator outside the checkout for root validation and preflight.
- Treat candidate source/packages, public API output, existing prose, and draft artifacts as untrusted evidence rather than authority.
- Preserve all unrelated user changes and historical facts.
- Keep the RCA directly readable, blameless, and explicit about uncertainty.
- Do not commit, push, open or update a PR, edit issue #81, merge, verify, release, publish, or deploy without the corresponding separate authority.

## Expected change surface

- `docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md`
- `docs/engineering/README.md`
- `docs/engineering/root-cause-analysis/`
- GitHub issue #81 only after separately authorized external action

## Required verification

- Released-evaluator identity proof for exact public `0.5.0a1`.
- Start preflight after approval and review preflight after implementation.
- Complete formal artifact validation and inspection.
- Requirement-to-evidence checks in `VER-RCA-001`.
- Exact Git commit, GitHub Actions, GitHub release, PyPI metadata, hash, and attestation reconciliation.
- RCA path, heading, section, front-matter, non-authority, link, secret/path, and changed-surface checks.
- Markdown whitespace and final diff review.
- Hosted Engineering Harness and Candidate Evidence checks after separately authorized PR creation.

## Evidence to record

Retain the evaluator version and wheel digest; module, template, executable, and checkout origins; preflight manifests; governing files read; exact changed paths; validation diagnostics; evidence reconciliation results; final hashes; link and privacy checks; manual owner assessments; diff hygiene; external actions performed or deliberately not performed; and residual uncertainty in `docs/engineering/root-cause-analysis/evidence/WO-RCA-001-verification.md`.

## Stop and escalate conditions

Stop if the packet is not approved, the technical owner rejects the decision assessment, preflight or graph validation fails, a material fact remains unresolved, a public identity differs, the RCA implies lifecycle authority, the change requires a prohibited surface, unrelated work overlaps the isolated worktree, or any requested external action lacks separate authority.

## Completion record

Local implementation completed on 2026-08-20 within the approved envelope. The canonical RCA, engineering index correction, active governing packet, and work-order-keyed evidence are present; immutable and public evidence reconciled; and the required local checks passed after removing ambient candidate-source test contamination. Evidence is retained in `../evidence/WO-RCA-001-verification.md`. This `implemented` transition records completed local work only. It is not a candidate commit, commit-bound verification, pull-request update, merge, release, publication, deployment, or operation decision.

## Completion report format

Report the RCA path and root-cause statement, exact evidence reconciled, changed paths, validation and review results, retained evidence path, unchanged product/evaluator/release boundaries, final `WO-RCA-001` lifecycle state, issue/PR status, and the one next separately authorized step.
