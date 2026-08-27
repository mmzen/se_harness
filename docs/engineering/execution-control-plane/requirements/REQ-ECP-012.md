+++
id = "REQ-ECP-012"
type = "requirement"
title = "A fresh consumer repository passes doctor"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN a consumer runs `harnessctl init`, commits the result, and runs `harnessctl doctor`, THE SYSTEM SHALL exit 0 with no failed check."
verification_method = ["test", "demonstration"]
priority = "must"
source = "complexity audit P0-1"

[relations]
derives_from = ["CAP-ECP-003"]
+++

# Requirement: A fresh consumer repository passes doctor

## Rationale

`init`, a commit, then `doctor` exits 1 in every fresh repository:
`hash_bound_classes.json` declares the class `governance-migration-protocol`
over `se_harness/governance_migration*.py`, files that exist only in this
repository, and the managed `.gitattributes` fragment pins them
(se_harness/hash_bound_classes.json:19-32;
templates/repository/standard/gitattributes.fragment:4-6;
se_harness/hash_bound.py:454-457, :485-499). Reproduced in-tree: `doctor` prints
`FAIL hash-bound-class-declared` and `FAIL hash-bound-attribute-effective`, and
the 0.7.1 wheel carries identical bytes (docs/notes/complexity-
audit-2026-08.md:97-116). The acceptance lane is structurally blind to it
(docs/notes/complexity-audit-2026-08.md:112-115). A green `init` followed by a
red `doctor` breaks portability for the primary audience.

## Behavior

- Trigger: in an empty Git repository, `harnessctl init .` runs, the result is
  committed, and `harnessctl doctor .` runs with the same released evaluator.
- Response: `doctor` exits 0, every check reads `PASS` or an explicit
  informational status, and no hash-bound class fails for a pattern that matches
  no tracked path in the consumer.
- On failure: a real installation fault (a missing managed file, a modified
  hash-bound byte) still fails `doctor`; the obligation removes only failures
  caused by this repository's own files.

## Assumptions and dependencies

- The `governance-migration-protocol` class and the three fragment lines are
  removed from the product; this repository pins its own LF bytes outside the
  managed block.
- The `evaluator-evidence` pattern is informational until the consumer's
  first verification record exists.
- The candidate-acceptance lane runs `git init` and commits in its target so
  this scenario is exercised in CI on Linux and Windows.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-012.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** an empty directory with `git init` done and the released evaluator
installed outside it.

**When** `harnessctl init .`, `git add -A`, `git commit`, then `harnessctl
doctor .` run.

**Then** `doctor` exits 0 and its output contains no line beginning `FAIL`.

### Example: failure behavior

**Given** the same repository, and the consumer then edits one byte of a hash-
locked managed script.

**When** `harnessctl doctor .` runs.

**Then** `doctor` exits 1 and the failing check names that script, not any file
of the SE Harness repository.

## Open decisions

None.
