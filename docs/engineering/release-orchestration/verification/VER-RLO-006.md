+++
id = "VER-RLO-006"
type = "verification"
title = "Verify release discovery separates artifacts from evidence"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[relations]
verifies = ["REQ-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-11T12:57:17Z"
decided_by = "assurance-owner"
reason = "The operator stated on 2026-09-11: I approve both artifacts and authorize implementation. This records assurance-owner approval of the verification contract reviewed in PR 452 at 553c7badf6f742c092b0b2d284f95e2e4ca60428; no candidate assurance or release decision."
+++

# Verification Contract: Verify release discovery separates artifacts from evidence

## Independence

Expected artifact membership follows the canonical validator's existing path
rules. Expected release identities come from committed fixture records and
the frozen incident tree, never from the repaired resolver's output.
An assurance owner separately assesses the resulting commit-bound record.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-001; SPEC-RLO-001 rules 3–5 | test, inspection | DISC01–DISC07 | Only real artifacts determine the unique released record and its unchanged candidate, evidence and main-history identity. |

## Acceptance scenarios

| Case | Action | Observable pass condition |
| --- | --- | --- |
| DISC01 — Path boundary | Exercise path inputs for each excluded directory: `templates`, `evidence`, `.git`, `.idea`, `target`, `node_modules`. Commit representable fixtures with valid and malformed Markdown, nested paths and ordinary lookalike names. | Excluded content is not parsed as artifacts. Normal artifact paths remain eligible. Membership matches the existing validator; no substring or ID-prefix exclusion. |
| DISC02 — Real duplicates | Put copied VREC, WO and RLS IDs in retained evidence, then put duplicate IDs in two eligible artifact paths. | Evidence copies do not collide. Genuine duplicate catalog IDs and ambiguous live RLS selection still refuse. Malformed eligible front matter still refuses. |
| DISC03 — History | Place a matching released RLS copy in evidence before its real integration, then change that evidence after integration. Exercise tree, record-search and changed-path discovery. | Both release and Pages resolvers return the real record's first main-history integration. Evidence cannot introduce, replace or move it. The rehearsal selector ignores evidence-only ready/released records. |
| DISC04 — Explicit evidence | Resolve an eligible release with its bound evaluator sidecar under `evidence/`; separately remove or corrupt the sidecar. | The valid binding resolves. Missing or invalid bound evidence still refuses. Directory exclusion grants no bypass of evidence validation. |
| DISC05 — Incident replay | Use trusted-main tree `fb6f60d5069706e8ae0ca69d1263285cbb904f45` and selected `RLS-SEH-026`. Run original and repaired discovery, then the repaired full resolver. | Original code reproduces the recorded `VREC-EVD-001` duplicate refusal. Repaired catalog membership equals canonical discovery on that tree, and full resolution returns identities independently read from its real RLS/VREC records. Preserve all original evidence bytes. |
| DISC06 — Revision isolation | Modify uncommitted working-tree artifacts while resolving the frozen trusted-main revision. Repeat the existing publication and CI-policy suites. | Working-tree edits cannot change the release plan. Existing main-ref, candidate, first-parent, binding and permission checks still pass. |
| DISC07 — Candidate acceptance | Run governance, preservation, archive and hosted checks for the repair candidate and final governance head. | Required checks pass on their identified commits; historical engineering bytes and modes are unchanged; every tested archive has at most 10,000 entries. |

## Property and invariant tests

Use disposable Git repositories to exercise real history and metadata parsing.
Supply expected path membership independently of the candidate helper. Include
an ID beginning with `VREC-EVD-` at an eligible path: the incident's ID prefix
must not become an exclusion rule. A filename containing `evidence` is not an
excluded directory. Use path-level cases for entries Git cannot safely store
in a working tree, such as a nested `.git` directory.

## Static and architecture checks

Inspect all callers of the three discovery helpers and the rehearsal selector.
Preserve ARCH-RLO-001 and ADR-RLO-001 trust separation. Diff against the baseline
must contain only WO-RLO-009 paths. No CI definition or portable validator edit.

## Security and privacy checks

Perform read-only resolution and disposable local tests without publication
credentials. No live tag, GitHub Release, PyPI or Pages mutation is an acceptance
step. Explicit evidence reads retain their existing digest and path checks.

## Performance and resilience checks

Filter excluded paths before metadata parsing. Retain elapsed time and parsed
path counts for the frozen-tree replay; do not add a broad benchmark suite.
Repeated reads of the same committed tree must produce the same identities.

## Manual assessments

The assurance owner reviews genuine-duplicate refusal, historical-byte
preservation and the complete DISC05 resolver result before verification.
The release-record rehearsal executes the PR checkout's resolver against
trusted-main records. Retain both commit identities so its result proves the
repaired code saw the incident's retained snapshots.

## Evidence retention

Store commands, outputs, runtime versions, commit identities, hashes and case
results below `docs/engineering/release-orchestration/evidence/WO-RLO-009/`.
Bundle raw results to respect the existing archive-entry limit. Record the
governing evaluator as isolated released 0.17.0, outside the source checkout.

Run focused tests and DISC05 on Windows and Linux. Run released doctor,
validate, review preflight and Git-derived scope checks; obtain existing
hosted required checks for the identified final head and merge checkout.
Record any unavailable platform or failed check as a gap, never as a pass.

## Residual uncertainty

These checks verify artifact discovery and release resolution. They do not
qualify a new software release or prove live publication service behavior.
