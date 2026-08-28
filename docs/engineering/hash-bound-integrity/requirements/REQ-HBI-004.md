+++
id = "REQ-HBI-004"
type = "requirement"
title = "Ship no hash-bound class or managed byte rule that only the harness's own repository can satisfy"
status = "draft"
owners = ["repository-owner", "security-owner", "quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL declare in the shipped class table and the canonical template fragment only hash-bound patterns that an installed consumer repository can satisfy from its own tracked content."
verification_method = ["test", "inspection"]
priority = "must"
source = "Repository issue #207; complexity audit finding P0-1 in docs/notes/complexity-audit-2026-08.md; VER-HBI-001 acceptance scenario 7"

[relations]
derives_from = ["CAP-HBI-001"]
+++

# Requirement: Ship no hash-bound class or managed byte rule that only the harness's own repository can satisfy

## Rationale

The class table in `se_harness/hash_bound_classes.json` and the fragment in
`templates/repository/standard/gitattributes.fragment` travel inside the wheel
and are installed into every consumer. Since `WO-HBI-001` they have carried
`governance-migration-protocol`, whose patterns name
`se_harness/governance_migration*.py`,
`se_harness/governance_migration_contract.json` and
`tests/fixtures/governance_migration/*.json`. Those paths exist in exactly one
repository: this one. In any other, the class fails
`hash-bound-class-declared` because nothing matches, and fails
`hash-bound-attribute-effective` because the fragment installs its rules into
the managed region while the class is declared `repository`-region.

`VER-HBI-001` scenario 7 already states the property this requirement makes
explicit — a consumer "inherits the `template` classes and none of this
repository's `repository`-region rules" — but no test derives the expectation
from the shipped surface, so the divergence was pinned as known
(`test_candidate_fragment_promotion_of_repository_patterns_is_pinned`) rather
than refused.

This repository's own byte pin for the migration-protocol files is not lost by
the change: the owner-controlled region of the root `.gitattributes` already
carries the same three rules, and `governance_migration_contract.py` computes
`implementation_sha256` with its own `sha256_bytes` rather than through
`hash_bound.resolve_mode`, so no product code path resolves the class.

## Behavior

- Trigger: always; assessed statically against candidate source.
- Response: every pattern in every class of the shipped declaration, and every
  rule in the canonical fragment, is satisfiable by an installed consumer:
  it names a path under the artifact root, a managed file, or another path the
  installer itself writes. No pattern names `se_harness/`, `tests/`,
  `repository_tools/` or any other path that exists only in candidate source.
- On failure: a static test over `templates/repository/standard/` and
  `hash_bound_classes.json` fails naming the offending pattern, and a fresh
  consumer installation's `doctor` is not required to pass.

## Assumptions and dependencies

- The `template` / `repository` region distinction of `SPEC-HBI-001` rule 10
  remains the mechanism by which this repository declares its own
  repository-only classes: in owner-controlled `.gitattributes` content, never
  in the shipped table or fragment.
- A binding recorded only in harness data rather than in a governed artifact
  (`implementation_sha256`) is declared in `unbound_digest_fields` with its
  reason, so `hash-bound-class-declared` still refuses any unclaimed digest
  field.

## Acceptance examples

### Example: normal behavior

**Given** the shipped declaration and the canonical fragment as built from
candidate source,

**When** the static portability test enumerates every pattern and rule,

**Then** none begins with `se_harness/`, `tests/` or `repository_tools/`, and a
repository created by `harnessctl init` followed by one commit passes
`harnessctl doctor` with exit status 0 on Linux and Windows.

### Example: failure behavior

**Given** a class added to the shipped declaration with the pattern
`tests/fixtures/example/*.json`,

**When** the static portability test runs,

**Then** it fails naming that pattern and the file that declares it.

## Open decisions

None.
