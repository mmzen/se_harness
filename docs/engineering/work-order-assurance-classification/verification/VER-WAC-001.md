+++
id = "VER-WAC-001"
type = "verification"
title = "Verify explicit work-order assurance applicability"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-WAC-001", "REQ-WAC-002", "REQ-WAC-003", "REQ-WAC-004", "REQ-WAC-005"]
+++

# Verification Contract: Verify explicit work-order assurance applicability

## Independence

Fixtures derive expected classifications, lifecycle states, VREC eligibility, and authority boundaries from `SPEC-WAC-001`, not from implementation helper constants. Tests enumerate aggregate subjects and legacy exceptions explicitly.

## Requirement-to-evidence matrix

| Concern | Method | Pass condition |
| --- | --- | --- |
| metadata shape | absent, scalar, partial, unknown-key, invalid-value, blank, and valid tables | exact valid contract accepted; malformed present data rejected deterministically |
| actionable lifecycle | draft, approved, in-progress, implemented, verified, released, rejected, and superseded work orders | actionable work requires declaration; completed legacy omission remains compatible |
| decision protection | required/not-required rationale and role cases | missing fields fail; no evidence, release, or authority rule is bypassed |
| preflight | start/review fixtures and real packet | classification is displayed; selected missing or invalid declaration fails read-only |
| pending assurance | implemented required work across absent and VREC-state matrix | only no active ready/verified/released coverage enters `assurance_pending` |
| aggregate coverage | several work orders and one aggregate ready VREC | pending subjects disappear and one assurance review remains |
| non-required and legacy | governance-only and completed-legacy fixtures | no false pending assurance or inferred exemption |
| deterministic output | repeated JSON and human inspection | stable ordering, counts, grouping, schema version, escaping, and messages |
| authority | negative command and transition assertions | no classification, VREC, status, release, commit, or push occurs automatically |
| distribution | canonical/root parity, lock, package, fresh install, upgrade | consumers receive consistent template, validator, preflight, inspection, and policy behavior without work-order overwrite |
| regression | supported Python and complete repository suites | existing lifecycle, provenance, dashboard, self-hosting, and CLI behavior passes |

## Acceptance scenarios

1. An approved required work order passes start preflight, reaches implemented with retained evidence, and appears under assurance pending until a ready VREC covers it.
2. An implemented non-required governance work order does not appear pending and still satisfies ordinary verification and evidence expectations.
3. A completed legacy work order without the table remains valid, but explicit preflight selection requires classification.
4. A ready aggregate VREC replaces several pending items with one accountable assurance-review decision.

## Property and invariant tests

- Queue membership depends only on explicit classification, exact lifecycle, and direct active VREC coverage.
- Suggestions are sorted, non-automatic, and contain no shell command, URL, generated ID, or inferred aggregate scope.
- Captured VREC and release semantics remain byte-for-byte unchanged outside intentionally updated documentation or tests.

## Static and architecture checks

Check one canonical field vocabulary, one queue implementation, versioned JSON schema, root/canonical managed parity, no date/title/path heuristic, and no circular dependency from inspection into provenance capture.

## Security and privacy checks

Exercise control characters, Unicode, oversized values, unknown keys, and terminal rendering. Confirm decision-role text is not presented as authenticated identity.

## Manual assessments

Review the rule examples and current repository classifications to confirm that assurance-bearing changes are distinguished from work that only records or transports an already authorized governance decision.

## Evidence retention

Retain exact changed paths, validator and preflight matrices, inspection before/after reports, deterministic hashes, managed reconciliation, package/install/upgrade results, supported-Python suites, full regression, deviations, and residual risk under `docs/engineering/work-order-assurance-classification/evidence/WO-WAC-001-verification.md`.

## Residual uncertainty

Automation cannot prove that a human rationale is honest or that the named role maps to the person acting. Accountable review and repository access controls remain necessary.
