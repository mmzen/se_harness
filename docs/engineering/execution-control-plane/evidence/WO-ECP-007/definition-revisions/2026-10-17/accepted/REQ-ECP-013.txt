+++
id = "REQ-ECP-013"
type = "requirement"
title = "No product code names this repository's records"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL ship no product code, template, or installed script that names an artifact identifier of the SE Harness repository's own releases."
verification_method = ["analysis", "test"]
priority = "must"
source = "complexity audit P1-2"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: No product code names this repository's records

## Rationale

Six `RLS-SEH-*` identifiers of this repository's own releases are hard-coded in
generic code: `se_harness/legacy_release_evidence.py:30-36`, the template
validator at `:73-78` and `:1755-1830`,
`.github/scripts/publish_dashboard.py:76`, `se_harness/installer.py:495-520`,
and `se_harness/cli.py:149-176` (docs/notes/complexity-audit-2026-08.md:259).
`predecessor_assessment.py:44-49` hard-codes an expected error at `RLS-
SEH-009.md` (docs/notes/complexity-audit-2026-08.md:144-146). SPEC-LRE-001 rule
14 keeps two implementations equal by fixture. A consumer's evaluator should
carry no knowledge of which records SE Harness itself released; the same records
stay exempt through the specification's own declaration mechanism (rule 5).

## Behavior

- Trigger: always: an invariant over the packaged surface.
- Response: no file under the wheel's packaged surface, the distributed template
  tree, or the installed scripts contains an identifier matching
  `[A-Z]+-SEH-[0-9]+`; the exemptions the identifiers encoded today are
  expressed as data in this repository's own artifacts.
- On failure: the portable-surface check fails the pull request that introduces
  such an identifier and names the file and line.

## Assumptions and dependencies

- `check_portable_release_surface.py` (or its successor) is the test that
  scans the packaged surface, and it runs on every pull request.
- The legacy-release-evidence declaration mechanism, rules 1 to 10 of
  SPEC-LRE-001, stays; only the constant set goes
  (docs/notes/complexity-audit-2026-08.md:356-358).
- Historical records `RLS-SEH-001` to `RLS-SEH-017` remain tracked and
  hash-bound; nothing rewrites them.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-013.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** the packaged surface is built from a candidate commit.

**When** the surface check scans every packaged, template, and installed-script
file for `-SEH-` identifiers.

**Then** zero matches; the six formerly exempt records still validate as legacy
through the data declaration.

### Example: failure behavior

**Given** a pull request adds `RLS-SEH-018` to `se_harness/installer.py`.

**When** the surface check runs on the pull request.

**Then** the check fails and names `se_harness/installer.py` with the line.

## Open decisions

None.
