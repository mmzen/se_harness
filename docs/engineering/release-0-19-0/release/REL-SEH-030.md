+++
id = "REL-SEH-030"
type = "release_contract"
title = "Release checker 0.19.0 with progressive instruction discovery"
status = "approved"
owners = ["release-owner", "assurance-owner"]
created = "2026-09-27"
updated = "2026-09-27"
previous_release_tag = "v0.18.0"

[relations]
gates = ["WO-DOC-016", "WO-ECP-039", "WO-HUP-019", "WO-HUP-020", "WO-IAR-013", "WO-IAR-014", "WO-IAR-015", "WO-IAR-016", "WO-IAR-017", "WO-IAR-018", "WO-IAR-019", "WO-PLG-023", "WO-PLG-025", "WO-RLS-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T17:46:14Z"
decided_by = "release-owner"
reason = "Human decision in this task: I approve. The user approves the reviewed REL-SEH-030 and WO-RLS-025 preparation package, including checker 0.19.0, plugin 0.2.0 inputs and the bounded delivery envelope. Codex applies that decision; this does not verify a candidate, release an RLS, merge, publish or adopt."
+++

# Checker 0.19.0 release contract

## Release unit

Release SE Harness 0.19.0 with the accepted instruction split, evaluator-owned
discovery, safe instruction migration and host delivery support. The explicit
gates select 13 completed work orders since 0.18.0 plus WO-RLS-025.
The [coverage table](../coverage.md) explains each member and the exclusions.
The first-parent trailer census is advisory; missing trailers need no repairs.

The preparation starts from merged commit
`fbc47dfdcff2b355ee973acb5be09bcdf7cefe78`. WO-RLS-025 adds the reviewed release
and plugin inputs. The final clean candidate C is the full commit recorded by
the build manifest and aggregate VREC. The human reviews that exact C with the
VREC before verification; the RLS must bind the same C. An accepted record is
never rebound after a source change. No final candidate is claimed here before
the preparation work is complete.

## Required evidence

1. All selected WOs are implemented. Their governing chains and required checks
   pass under the isolated released 0.18.0 evaluator.
2. Final integration is tested: the candidate suite, source qualification,
   distribution checks, installed package checks and predecessor upgrade
   rehearsals pass in the repository's existing Windows and Ubuntu lanes.
   Report skipped cases and the limits they leave.
3. Two fresh runs of the pinned Linux build recipe produce identical wheel and
   source archive bytes for C. Retain the recipe identity, toolchain, workflow
   run and schema-2 bundle manifest. Development wheels are not release builds.
4. One final-candidate VREC covers every selected WO and every required VER.
   Earlier verified records remain evidence of their original candidates.
   Current integration evidence must establish their combined result at C.
5. After the human verifies that VREC, prepare the ready RLS with version
   0.19.0, bind the permanent distribution manifest and pass the existing
   bound-record replay. Present its hashes and evidence to the release owner.

## Compatibility and claim limits

The delivered instruction structure has a compact root and conditional guides.
The selected evaluator remains the sole lifecycle authority. Existing root
0.18.0 files remain installed in this repository until a separate adoption.

Claim safe upgrade only for the exercised source-release and ownership cases.
An installation must satisfy the replacement-delivery checks before retirement
of its old entry. Customized or ambiguous inputs fail closed. Synthetic upgrade
receipts test installer transactions; they do not prove native host delivery.

Native evidence accepted in VREC-IAR-011 covers Windows Codex CLI
0.155.0-alpha.16.4 with its native app server and Claude Code 2.1.273, at startup
and after manual compaction. Preserve the recorded differences in switch,
failure and permission tests. This evidence does not establish desktop UI,
automatic threshold compaction, macOS or later host versions. Reuse it only
after comparing the delivered inputs with C; changed inputs need matching proof.

Owner-configured definition/WO exceptions and linked accepted-definition
revisions remain disclosed future capabilities. This release does not add
those evaluators or lifecycle commands.

## Plugin sequence

WO-RLS-025 proposes plugin version 0.2.0 for both hosts and adds the reviewed
delivery assets to the production plan. This contract accepts preparation of
those inputs. It does not claim that final plugin archives have been released.
After checker publication, assemble them using its released record and the
independently obtained public wheel, then inspect and test the actual outputs
before a separate publication decision. Preserve SPEC-PLG-001's published-wheel
boundary and SPEC-PLG-021's development route.

## Decisions and publication boundary

Contract approval selects this scope and these evidence expectations. WO
approval authorizes bounded execution. Human verification accepts one exact
aggregate VREC. Human release approval applies to one exact ready RLS.
Push/PR and read-only rehearsal authority is proposed in WO-RLS-025.
Merge, immutable publication, latest promotion and adoption remain separate.

Before any later latest promotion, complete one successful public observation
cycle: the publication workflow passes, both public distribution digests equal
the bound hashes, and installation from the public wheel passes its smoke check
in a clean environment. This is an event-based observation window; this
contract invents no elapsed-time soak claim. The release owner then explicitly
authorizes the latest and `last` marker updates.

## Failure and recovery

Stop at a failed required check. Correct only approved scope and retain the
original failure. A changed candidate requires a matching build and final
verification record. Before publication, a rejected candidate is not published.
After publication, preserve immutable bytes and use the existing resume path
for an interrupted exact release. A product defect requires a new version;
do not overwrite the published archive or move its immutable tag.
