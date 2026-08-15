+++
id = "VER-IAR-008"
type = "verification"
title = "Verify read-only deterministic repository inspection"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-IAR-016"]
+++

# Verification Contract: Verify read-only deterministic repository inspection

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `go for implementation` as the independent evidence contract for `REQ-IAR-016`.

## Independence

Expected queue membership derives from controlled artifact types and lifecycle states, not from implementation helpers. Existing validator fixtures and Explorer snapshot/finding tests remain the oracle for diagnostic and finding identity. Filesystem snapshots prove the command is read-only.

## Requirement-to-evidence matrix

| Concern | Method | Pass condition |
| --- | --- | --- |
| command contract | CLI parser and subprocess tests | `inspect [TARGET] [--json]` is available from source and installed entry points |
| reuse boundary | static architecture test and patched-call test | inspection calls the existing snapshot API and defines no duplicate validation or finding rule catalog |
| decision queue | controlled lifecycle fixture | every and only `ready` artifact appears with the specified mechanical action class |
| definition queue | controlled lifecycle fixture | every and only `draft` artifact appears |
| active-work queue | controlled work-order fixture | every and only approved or in-progress work orders appear with the correct action class |
| findings | existing validator and Explorer fixtures | rule, severity, authority, message, artifacts, paths, and evidence are preserved |
| invalid graph | malformed/invalid graph fixture | report is produced, formal validity is false, blocking findings remain visible, and inspection exits zero |
| operational failure | missing script, unsafe target, and unreadable/malformed input fixtures | concise nonzero failure with no partial write |
| JSON | golden structural assertions | schema, producer, authority, counts, planes, queues, sorting, UTF-8, and final newline are deterministic |
| human output | golden semantic assertions | counts, queues, finding IDs, validity, and authority boundary are visible with no score |
| no writes | before/after repository inventory and content hashes | no file, directory, lock, artifact, or Git state changes |
| compatibility | validator, dashboard, CLI, installer, integrity, and package tests | existing commands and snapshot schema remain unchanged |

## Security and boundary checks

- Exercise titles, paths, messages, and owners containing control-like characters and markup.
- Exercise target and script path escape attempts through the existing launcher boundary.
- Confirm inspection never executes repository content beyond the managed repository script selected by the established command architecture.
- Confirm output says `repository-local` and `derived`; no independent assurance claim appears.

## Regression

Run focused inspection tests, affected validator/Explorer/CLI/installer/integrity/documentation tests, and the complete suite on Python 3.11 and the local supported runtime. Run formal validation, `doctor`, start and review preflight, canonical parity, managed-upgrade idempotence, CLI help, and diff hygiene.

## Evidence retention

Retain commands, runtimes, test counts, representative human and JSON output, deterministic hashes, no-write proof, changed paths, deviations, and residual risks under `docs/engineering/instruction-architecture/evidence/WO-IAR-008-verification.md`.

## Residual uncertainty

The report can make existing observations easier to see but cannot prove their usefulness, eliminate noisy Explorer heuristics, or determine whether a human decision is substantively correct.
