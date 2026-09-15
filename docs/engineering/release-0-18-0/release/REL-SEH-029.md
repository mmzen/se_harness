+++
id = "REL-SEH-029"
type = "release_contract"
title = "Release checker 0.18.0 with the accepted KISS and plugin support changes"
status = "approved"
owners = ["release-owner", "assurance-owner"]
created = "2026-09-15"
updated = "2026-09-15"

[relations]
gates = [
  "WO-AUT-006",
  "WO-CIP-008",
  "WO-CIP-009",
  "WO-CIP-010",
  "WO-DST-027",
  "WO-ECP-037",
  "WO-ECP-038",
  "WO-HUP-018",
  "WO-KIS-001",
  "WO-KIS-002",
  "WO-KIS-003",
  "WO-KIS-004",
  "WO-KIS-005",
  "WO-KIS-006",
  "WO-KIS-007",
  "WO-KIS-008",
  "WO-KIS-009",
  "WO-PLG-001",
  "WO-PLG-002",
  "WO-PLG-003",
  "WO-PLG-004",
  "WO-PLG-005",
  "WO-PLG-006",
  "WO-PLG-007",
  "WO-PLG-008",
  "WO-PLG-009",
  "WO-PLG-010",
  "WO-PLG-011",
  "WO-PLG-012",
  "WO-PLG-016",
  "WO-PLG-017",
  "WO-PLG-018",
  "WO-PLG-019",
  "WO-PLG-020",
  "WO-PLG-021",
  "WO-PLG-022",
  "WO-RLO-009",
  "WO-TCM-011",
  "WO-RLS-024",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T06:00:55Z"
decided_by = "release-owner"
reason = "The owner selected release preparation through the delegated route on 2026-09-15. Record the bounded release-preparation scope: checker 0.18.0, the 38 completed changes plus WO-RLS-024, and plugin 0.1.0 assembly inputs. Use existing checks and the accepted KISS amendments. This selects the contract for preparation and does not verify, release, publish or adopt the resulting candidate."
+++

# Checker 0.18.0 release contract

## Scope

Release the 0.18.0 checker and standard templates containing the accepted KISS
changes, ordinary delegated execution and plugin ownership support. The gates
select the 38 completed changes since v0.17.0 plus WO-RLS-024. The
[coverage table](../evidence/WO-RLS-024/coverage.md) explains membership and
reuses one existing evidence path for each work order. Historical claims remain
bound to their original candidates. The final aggregate record binds the
selected integration candidate.

This contract uses the existing explicit work-order list. The trailer census is
an inventory aid: five completed members were found through artifact/Git review
and two already-released members were excluded. No history repair, exemption
registry or per-member evidence copy is required.

## Acceptance

1. The isolated released 0.17.0 evaluator accepts graph, integrity, selected
   preflight and implementation handoff. Each gate member is implemented when
   aggregate verification is prepared.
2. The full candidate test suite passes. Existing package acceptance proves
   installation and the 0.17.0-to-0.18.0 upgrade in its Windows and Ubuntu
   environments; retain actual skips and limits. Existing source qualification,
   distribution validation and help checks pass.
3. The existing pinned Linux recipe produces matching wheel and source archive
   bytes in two runs. Retain the exact candidate, workflow run and bundle
   manifest. Native development wheels cannot be promoted as this release build.
4. One final aggregate verification record covers all gates and their declared
   verification contracts on that candidate. Reuse historical evidence in its
   stated scope and add current integration evidence; apply the accepted KISS
   amendments to current behavior. Removed hooks, locks and historical host
   matrices do not return as release gates.
5. After accountable verification, prepare the release record, bind the build
   manifest and run the existing ready-record replay. Accountable release and
   external publication are subsequent decisions.

## Plugin sequence and limits

The candidate also fixes the first plugin version at 0.1.0 and supplies
release/plugin-assembly.json for both hosts. This is preparation of the release
inputs. The checker release does not claim publication or acceptance of final
plugin archives. After checker publication, the existing builder consumes its
released record and independently identified public wheel unchanged. Assemble,
inspect and test those actual outputs before any plugin publication claim.
SPEC-PLG-021 preserves this sequence. No extra publication workflow is added.

Existing Windows evidence covers native skill discovery, direct checker use,
connection, repair and upgrade in disposable projects. It does not establish
model-driven sessions, desktop installation or macOS support. Repeat only the
checks needed for the actual final archives; retain these claim limits.

## Recovery

If qualification fails, retain the failure and fix only the selected scope; a
new source candidate needs matching build evidence. Before publication, stop at
the failed stage. If publication is interrupted after a release decision, use
the existing resume procedure for that exact release. Do not replace published
bytes. A discovered post-release defect is corrected in a new version.
