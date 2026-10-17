+++
id = "REQ-ECP-013"
type = "requirement"
title = "No product code names this repository's records"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-10-17"
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

## Selected WO-ECP-007 revision

This revision applies only to remaining work under WO-ECP-007. The [preserved accepted version](../evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/REQ-ECP-013.txt) has complete-file SHA-256 `3c7d41ea28442d16bad05a3e24fe76824102a244e7641d689acf8f0c5d9cdb15` and Git blob `595905cb2717bdf986b5fab07bea868fe4ae9eac` at commit `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38`. The [activation receipt](../evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json) records the actual human authority and before/after identities. Without that recorded authority this replacement does not govern work. Original lifecycle events remain unchanged; this is not a native evaluator revision event. Earlier completed work and evidence retain their original definition meaning. Retained historical problem descriptions are context, not claims about current code. Unrelated skills and capabilities retain their existing obligations.

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

- Executable implementation, machine policy, templates and generated executable
  UI shipped with the evaluator must contain no repository-specific artifact-ID
  literal matching [A-Z]+-SEH-[0-9]+. Treat equivalent records equally when only
  their IDs differ; use their declared type, state and relations.
- Extend the existing portable-surface check over the actual built wheel. A
  forbidden literal reports its member path and source location and fails the check.
- Historical prose, release documentation and package-description metadata may
  reference real records. That permission does not cover executable exceptions.
  User artifacts and data loaded at runtime are not packaged implementation.
- Preserve historical records and the accepted SPEC-LRE-002 evidence floor.
  No legacy declaration mechanism or hard-coded compatibility set is restored.

## Assumptions and dependencies

Reuse scripts/check_portable_release_surface.py and its current CI callers.
Inspect source and generated wheel members; generated embedded JavaScript is in
scope. Repository-only design exports and tests do not ship and remain separate.
Keep all historical artifacts and evidence unchanged. SPEC-LRE-002 governs legacy
unbound release records; SPEC-LRE-001 rules 1 to 16 are retired.

## Acceptance examples

- Equivalent verified records, including the formerly special-cased ID and a
  different ID, receive equivalent viewer selection treatment under the same graph.
- A clean generated UI and built wheel pass the boundary check.
- A forbidden literal introduced into a Python implementation member or embedded
  JavaScript in generated HTML fails with the affected member identified.
- Documentation/package-description links remain allowed and existing package
  safety checks still fail their original negative controls.
- No released historical artifact or evidence byte changes.

## Open decisions

None.
