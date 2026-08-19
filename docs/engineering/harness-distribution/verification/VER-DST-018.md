+++
id = "VER-DST-018"
type = "verification"
title = "Verify bounded documentation-state consistency"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
verifies = ["REQ-DST-060"]
+++

# Verification Contract: Verify bounded documentation-state consistency

## Independence

Expected facts derive from current validator behavior, canonical authoring guidance, the exact governor descriptor, formal VREC/RLS metadata, and repository directory structure. Verification must not infer truth from the edited explanatory prose or treat passing prose assertions as lifecycle authority.

On 2026-08-19, the accountable owner approved this evidence contract under its original identifier `VER-DST-017` with `REQ-DST-060`, the specification then identified as `SPEC-DST-017`, and `WO-DOC-013`. After current `main` independently assigned both `017` identifiers to another packet, the owner approved renumbering the unchanged contracts to `SPEC-DST-018` and `VER-DST-018`. Approval defines required evidence; it does not judge the later implementation or create a VREC.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-DST-060` | focused tests, formal validation, managed-integrity doctor, static fact comparison, and manual diff review | README limitation, engineering index, self-hosting identity, three domain status summaries, exact referenced records | every current-state statement matches its authoritative bounded source; no formal state or behavior changes |

## Acceptance scenarios

- Confirm the validator requires work-order `architecture` only when the relation is present and the README no longer claims otherwise.
- Confirm the README still reports the unresolved G0-G5 policy/Explorer mismatch.
- Confirm every audited missing engineering directory is present in the root engineering index.
- Confirm the self-hosting summary matches governor version 0.3.0 and `RLS-SEH-005`.
- Confirm the evidence-keying, work-order-assurance, and release-orchestration summaries match the named VREC/RLS statuses and do not overclaim release or publication.

## Property and invariant tests

- Formal artifact metadata outside this new packet remains byte-for-byte unchanged.
- The selected governor descriptor, package version, managed templates, workflows, and lock remain unchanged.
- Every new factual artifact ID resolves uniquely in formal validation.
- Repeated validation and focused tests produce equivalent outcomes.

## Static and architecture checks

- Run `python -m unittest tests.test_public_onboarding` and any focused documentation tests affected by the edits.
- Run the complete unit suite.
- Run formal artifact validation, release-distribution validation, CLI help, and `doctor`.
- Run start and review preflight for `WO-DOC-013` at their phase-appropriate times.
- Review the final diff for the exact authorized documentation and test surface.

## Security and privacy checks

Confirm no secret, credential, environment dump, private URL, unsafe Markdown/HTML, executable content, or untrusted file body is introduced.

## Performance and resilience checks

No runtime performance behavior changes. Confirm the complete suite remains within its ordinary execution envelope and that the correction introduces no new dependency or external availability requirement.

## Manual assessments

Review the corrected prose for tense, authority boundaries, historical accuracy, and distinction between verified coverage, release, publication, and governor promotion. Confirm navigation descriptions are concise and the public README remains a bounded entry point.

## Evidence retention

Retain exact changed paths, authoritative source lines, preflight manifests, commands and exit codes, focused and full test counts, validation and doctor summaries, local-link observations, diff review, residual risks, and unperformed external actions at `docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md`.

## Residual uncertainty

Static checks cannot prove reader comprehension or future external rendering. Future lifecycle transitions and governor promotions can make present-tense narratives stale again; preventing all such drift requires separately authorized broader automation.
