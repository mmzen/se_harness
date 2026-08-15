+++
id = "VER-IAR-009"
type = "verification"
title = "Verify bounded deterministic inspection guidance"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-IAR-017"]
+++

# Verification Contract: Verify bounded deterministic inspection guidance

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `ok i approve` as the independent evidence contract for `REQ-IAR-017`.

## Independence

The expected catalog derives from `SPEC-IAR-009`, not from implementation constants. Controlled snapshots provide source queue entries and findings. Tests compare the complete public suggestion records and independently prove that unsupported sources do not receive advice.

## Required checks

| Concern | Method | Pass condition |
| --- | --- | --- |
| IAR-008 compatibility | artifact and contract assertions | the approved amendment removes conflicting broad exclusions while retaining the bans on free-form advice, new rule inference, and automatic remediation |
| JSON contract | exact structural assertions | every suggestion has only the specified fields and `automatic` is exactly `false` |
| queue catalog | one fixture per existing queue action class | source, subject, action, message, and accountable role match `SPEC-IAR-009` |
| finding catalog | one fixture per listed warning rule | each supported derived warning yields the specified bounded action and role |
| safe omission | validator, informational, and unknown-rule fixtures | source findings remain unchanged and no suggestion is emitted |
| source isolation | adversarial title, message, path, owner, and evidence values | those fields neither select nor construct guidance |
| preservation | baseline report comparison | removing additive suggestions yields the same validation, summary, queues, findings, ordering, and exit behavior as IAR-008 |
| deterministic JSON | repeated and permuted-source runs | byte-identical output and stable suggestion order |
| compact human output | repeated-rule fixture | guidance is grouped by source/action/role, subjects are bounded, authority is explicit, and no command or score appears |
| no execution or writes | patched process/filesystem calls and before/after inventories | suggestions invoke nothing and change no file, Git state, artifact, or lifecycle field |
| distribution | root/canonical, install, lock, and upgrade tests | the standard consumer installation and candidate source contain the same catalog and behavior |

## Security and boundary checks

- Include control characters, markup, shell metacharacters, path separators, and command-like text in every repository-controlled source field.
- Prove that catalog messages are static and only escaped artifact IDs may be substituted.
- Prove that no suggestion contains a command, generated repository path, target status, deadline, confidence, score, or URL.
- Confirm every human and JSON report retains the repository-local, derived, non-authoritative boundary.

## Aggregate candidate verification

The final candidate is expected to contain `WO-IAR-008` and `WO-IAR-009`. After both work orders are implemented with retained evidence, one aggregate verification record may list both work orders and both verification contracts against the same clean candidate commit. The aggregate record does not weaken either contract.

## Regression

Run focused suggestion and inspection tests, affected validator, Explorer, CLI, installer, integrity, package-data, documentation, and instruction-architecture tests, and the complete suite on Python 3.11 and the local supported runtime. Run formal validation, `doctor`, phase-appropriate preflight for both work orders, CLI help, canonical parity, managed-upgrade idempotence, and diff hygiene.

## Evidence retention

Retain catalog coverage, commands, runtimes, test counts, representative human and JSON output, deterministic hashes, hostile-input and no-write proof, changed paths, deviations, and residual risks under `docs/engineering/instruction-architecture/evidence/WO-IAR-009-verification.md`.

## Residual uncertainty

Deterministic guidance can show the intended decision path but cannot prove that an observation is substantively important or that an accountable owner will choose the correct outcome.
