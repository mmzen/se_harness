+++
id = "VER-PMI-001"
type = "verification"
title = "Verify portable managed-file integrity"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-PMI-001", "REQ-PMI-002", "REQ-PMI-003", "REQ-PMI-004", "REQ-PMI-005", "REQ-PMI-006", "REQ-PMI-007"]
+++

# Verification Contract: Verify portable managed-file integrity

## Independence

Verification derives expected hashes from the normative canonicalization rules and independent fixtures rather than calling the production helper to construct expected values. Temporary repositories isolate Git configuration, newline representation, locks, fragments, and upgrade state.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-PMI-001 | property and vector tests | UTF-8 LF, CRLF, CR, mixed endings, BOM, Unicode, final newline | equivalent terminators share the specified digest; every other content distinction remains |
| REQ-PMI-002 | command integration | schema-2 doctor on LF and CRLF targets | logically identical content passes; real edits fail with bounded reasons |
| REQ-PMI-003 | security regression | managed files, fragments, malformed markers, owner text | customization is preserved; only the valid block participates |
| REQ-PMI-004 | migration matrix | schema-1 exact, desired-canonical, ambiguous, invalid, interrupted | only proven-safe states migrate; ambiguous content and old evidence remain untouched |
| REQ-PMI-005 | architecture and integration | init, adopt, upgrade, lock writer, doctor | one shared semantic implementation produces identical decisions |
| REQ-PMI-006 | distribution end to end | self lock, canonical copies, wheel, fresh install, LF/CRLF checkout | every layer agrees and doctor passes; a stale fixture fails |
| REQ-PMI-007 | full regression and review | installation, path, symlink, provenance, authority | existing safety and compatibility tests pass with no new profile or authority mutation |

## Acceptance scenarios

The executable scenarios in `acceptance/portable-managed-integrity.feature` are the minimum public behavior contract.

## Property and invariant tests

- Replacing any combination of CRLF or CR terminators with LF does not change `utf8-text-lf-v1`.
- Changing any non-terminator byte changes the canonical digest except for cryptographic collision uncertainty.
- Final-newline presence remains significant.
- Canonicalization is idempotent.
- Lock JSON and file ordering are deterministic.
- Doctor never mutates files or locks.
- Failed or customized upgrades never partially replace content or lock evidence.

## Static and architecture checks

Search production code for raw managed-integrity SHA-256 call sites outside the shared component. Confirm installer, upgrade, doctor, full-file, and fragment flows delegate to it. Confirm source/canonical-template parity and no dependency inversion toward CLI, Git, or governance logic.

## Security and privacy checks

Exercise invalid UTF-8, malformed JSON, unsupported schema/mode/algorithm, malformed digest, escaping and absolute paths, symlink traversal, duplicate fragment markers, oversized bounded fixtures, and malicious-looking content. Diagnostics contain paths and reason codes but no target bodies or secrets.

## Performance and resilience checks

Hash the complete standard template and a bounded large text fixture. Verify linear completion, deterministic results, no network access, and atomic recovery from injected failure before lock replacement.

## Manual assessments

Review doctor and upgrade wording so operators can distinguish exact legacy evidence, canonical desired equality, required migration, and actual customization. Inspect the self-repository lock to confirm it was generated rather than hand-patched.

## Evidence retention

Retain exact commands, raw and canonical test vectors, test counts, doctor results before and after, migration matrix, changed-file parity, wheel hash and contents, fresh-install results, deviations, platform limitations, and residual risks in `docs/engineering/portable-managed-integrity/evidence/WO-PMI-001-verification.md`.

## Residual uncertainty

SHA-256 collision risk remains negligible rather than impossible. Legacy locks with ambiguous mismatches cannot be migrated automatically. Future binary-managed assets require a separate explicit mode and decision.
