+++
id = "VER-RCA-001"
type = "verification"
title = "Verify RCA completeness, evidence, and non-authority"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
verifies = ["REQ-RCA-001", "REQ-RCA-002", "REQ-RCA-003"]
+++

# Verification Contract: Verify RCA completeness, evidence, and non-authority

## Independence

Acceptance is derived from `INT-RCA-001`, the three requirements, `SPEC-RCA-001`, `ARCH-RCA-001`, immutable Git and public release identities, and the restored standard-repository rules. Verification must not accept a claim merely because it appears in the authored RCA, prior conversation, candidate code, or a successful workflow.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-RCA-001` | deterministic heading/path inspection and accountable content review | exact RCA path, one H1, required sections, root-cause statement, five whys, completed/recommended separation | exactly one canonical RCA is complete, concise, causal, blameless, and free of unresolved material decisions |
| `REQ-RCA-002` | commit/API/hash reconciliation and semantic review | every exact commit and Actions run in `SPEC-RCA-001`, GitHub release, PyPI release, wheel/sdist hashes, attestation observation | every enumerated identity is exact and each technical observation remains distinct from lifecycle authority |
| `REQ-RCA-003` | graph validation, front-matter scan, changed-path inspection, link review | `docs/rca/`, this formal domain, issue #81, repository index, final diff | RCA has no formal identity; issue and RCA cross-reference; no preventive implementation or prohibited surface is changed |

## Acceptance scenarios

- A maintainer can identify the primary cause without reconstructing the event from conversation history.
- A reviewer can follow every release and CI link and match the final distribution hashes.
- A reviewer cannot reasonably read the RCA as retroactive authorization or as permission for issue #81 actions.
- Changed-path inspection shows only the RCA, this governing packet, its evidence, and the bounded repository index update.

## Property and invariant tests

- Exactly one RCA file matches the specified date and slug.
- The RCA has exactly one H1 and contains every required H2 concept.
- No `+++` formal front-matter delimiter, `status =`, or formal artifact declaration appears in the RCA.
- All enumerated commits are 40 lowercase hexadecimal characters; hashes are 64 lowercase hexadecimal characters.
- The root remains pinned to released `0.5.0a1`, and no candidate role is described as governing the root.
- No changed path is under `se_harness/`, `templates/`, `.github/workflows/`, `.self-hosting/`, package metadata, or release records.

## Static and architecture checks

- Run released-evaluator `harnessctl validate` and phase-appropriate preflight.
- Confirm `ARCH-RCA-001` addresses only the non-authority boundary requirement, conforms to the selected specification, and has an accepted `no_significant_decision` assessment before approval.
- Inspect typed relation coverage across intent, capability, requirements, specification, architecture, verification, and work order.
- Confirm the repository index identifies the new domain without describing `se_harness` as specially self-governing.

## Security and privacy checks

- Scan the RCA and evidence for credentials, private tokens, environment approval payloads, local user paths, and unnecessary logs.
- Confirm every external link uses HTTPS and no active HTML, remote image, script, or embedded executable content is introduced.
- Treat fetched public metadata as untrusted and reconcile exact identity fields before recording results.

## Performance and resilience checks

No runtime performance behavior applies. Confirm the RCA remains usable as a standalone Markdown file when external services are unavailable, with exact identities still sufficient for later reconciliation.

## Manual assessments

- Product/repository owner: confirm the problem, impact, desired outcome, and root cause are accurate and blameless.
- Technical owner: accept or reject the no-significant-decision assessment and boundary description.
- Quality/security owner: confirm evidence sufficiency, authority semantics, supply-chain claims, and residual uncertainty.
- Engineering owner: confirm the diff remains inside `WO-RCA-001` and issue #81 actions remain unimplemented.

## Evidence retention

Record evaluator identity, start/review preflight manifests, graph validation, exact changed paths, heading/front-matter checks, commit and public API reconciliation, hash and attestation observations, link results, secret/path scan, Markdown whitespace review, accountable manual assessments, residual uncertainty, and every unperformed external action under `docs/engineering/root-cause-analysis/evidence/WO-RCA-001-verification.md`.

## Residual uncertainty

An RCA necessarily contains causal analysis and cannot be proven solely by automation. Public service availability and mutable presentation URLs may change even where immutable identities remain valid. Independent accountable review, exact identities, explicit uncertainty, and the non-authority boundary constrain but do not eliminate these limits.
