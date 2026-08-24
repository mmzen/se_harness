+++
id = "VER-HUP-004"
type = "verification"
title = "Verify portable version-independent governor succession"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
verifies = ["REQ-HUP-008", "REQ-HUP-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "quality-owner"
+++

# Verification Contract: Verify portable version-independent governor succession

## Independence

The transition resolver is repository-owned orchestration and is never an
evaluator. Authoritative target-root checks run from the independently
installed exact target release with checkout imports, user site, and
`PYTHONPATH` excluded.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-HUP-008 | resolver unit/fixture tests, exact identity checks, workflow contract, exact-target integration, hosted push and PR lanes | same-version and changed-version routing are deterministic; every trust/evidence mismatch fails; exact target validates complete root; checkout remains clean |
| REQ-HUP-009 | focused inspection test on canonical LF plus CRLF materialization, lock and origin negatives, complete suites | equality and governed drift are both role-safe; result is independent of checkout line endings; lock/origin failures remain blocking |

## Required positive cases

- Same version and canonical lock at base/target: deterministic not-applicable
  transition result; managed CI remains the validating gate.
- Synthetic N to N+1 and N+1 to N+2 fixtures: identical routing without source
  changes or version constants in workflow/resolver.
- Exact historical 0.5.0 to 0.6.0 declaration and evidence: target 0.6.0
  identity, doctor, and complete validation pass without a compatibility view.
- Pull-request, ordinary push, branch-creation push, and merge-push base
  selection produce one full suitable commit or fail closed.
- Equal canonical root/template bytes and divergent working-tree line endings
  preserve root lock integrity, distinct paths, and candidate semantics.
- Complete unit suites pass on Python 3.11 and the local default runtime.

## Required negative cases

- Zero, abbreviated, missing, ambiguous, non-ancestor, or shallow-history base.
- Missing, draft, rejected, duplicated, or mismatched upgrade work order.
- Wrong prior lock, target version, archive name/hash, payload hash, transaction
  evidence path/hash, runtime origin, entry point, templates, or interpreter.
- Hard-coded concrete governor constants in workflow or resolver.
- Checkout mutation, symlink/path escape, oversized output, malformed JSON,
  credential-bearing environment, `PYTHONPATH`, user site, or checkout import.
- Raw-byte inequality used as the only evaluator-role assertion.

## Repository gates

- Exact public 0.6.0 `doctor`, complete `validate`, `inspect`, dashboard, and
  workflow handoff.
- Checkout-source complete tests, release-distribution validation, workflow
  parsing, security/path scan, exact-scope audit, and `git diff --check`.
- Hosted Candidate source evidence and Governor transition assessment pass on
  both push and pull-request events for the exact corrected candidate.

## Evidence retention

Retain the resolver/workflow fixture matrix, exact command results, both full
suite summaries, target evaluator identity, hosted run URLs, checkout-clean
proof, and changed-path audit at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-004-verification.md`.
