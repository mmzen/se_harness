+++
id = "WO-IAR-018"
type = "work_order"
title = "Cover the preserved governance package in PR 489"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "not_required"
rationale = "Proposed for human approval: this work solely transports the already authorized VREC-IAR-009 verification decision and its preserved governing package. It changes no definition, implementation, evidence identity or assurance meaning. A change to those inputs requires separate scope and a new assurance classification."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/instruction-architecture/architecture/ARCH-IAR-011.md",
  "docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-011.md",
  "docs/engineering/instruction-architecture/capabilities/CAP-IAR-002.md",
  "docs/engineering/instruction-architecture/decisions/DEC-IAR-001.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-009-evaluator.json",
  "docs/engineering/instruction-architecture/proposals/progressive-discovery/APPLICABILITY.md",
  "docs/engineering/instruction-architecture/proposals/progressive-discovery/README.md",
  "docs/engineering/instruction-architecture/proposals/progressive-discovery/discovery-split-review-source.md",
  "docs/engineering/instruction-architecture/proposals/progressive-discovery/instruction-review-source.md",
  "docs/engineering/instruction-architecture/proposals/progressive-discovery/sources.json",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-022.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-023.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-024.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-025.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-026.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-027.md",
  "docs/engineering/instruction-architecture/specifications/SPEC-IAR-014.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-009.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-014.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-018.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-018/",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
verification = ["VER-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T09:31:13Z"
decided_by = "engineering-owner"
reason = "Human decision: I approve, answering the explicit request to approve the exact-path governance transport scope and proposed not_required assurance classification."
scope_paths = ["docs/engineering/instruction-architecture/architecture/ARCH-IAR-011.md", "docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-011.md", "docs/engineering/instruction-architecture/capabilities/CAP-IAR-002.md", "docs/engineering/instruction-architecture/decisions/DEC-IAR-001.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-009-evaluator.json", "docs/engineering/instruction-architecture/proposals/progressive-discovery/APPLICABILITY.md", "docs/engineering/instruction-architecture/proposals/progressive-discovery/README.md", "docs/engineering/instruction-architecture/proposals/progressive-discovery/discovery-split-review-source.md", "docs/engineering/instruction-architecture/proposals/progressive-discovery/instruction-review-source.md", "docs/engineering/instruction-architecture/proposals/progressive-discovery/sources.json", "docs/engineering/instruction-architecture/requirements/REQ-IAR-022.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-023.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-024.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-025.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-026.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-027.md", "docs/engineering/instruction-architecture/specifications/SPEC-IAR-014.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-009.md", "docs/engineering/instruction-architecture/verification/VER-IAR-014.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-018.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-018/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T09:31:36Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Execute the human-approved governance transport correction for PR 489, preserving every listed input and existing assurance decision."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-27T09:36:08Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed the approved transport correction: 19 governance inputs and 32 VREC evidence files preserved; released integrity, validation, selected handoff and combined PR check passed. No new assurance claim; WO-IAR-013 through WO-IAR-016 remain in progress."
+++

# Cover the preserved governance package in PR 489

## Objective

Make the already recorded governance package an explicit part of the combined
scope for PR #489. This proposal remains draft. Preparation does not approve it.

The released 0.18.0 check-pr rejects the first of 19 uncovered files,
ARCH-IAR-011.md. The implementation work orders cover product and test paths,
but omit the definition/proposal package and VREC-IAR-009 with its sidecar.
Those files already exist in the published branch at `a72c8262a134d0e07f78ca2fbfb16c1ecf610894`.

## In scope

Transport the 19 files listed below without changing their Git blob bytes,
formal meanings, decisions or evidence identities. Their original authoring,
definition approvals and verification decision retain their existing authority.
Approval of this work order authorizes their bounded inclusion in the PR; it
does not retroactively manufacture a decision or approve new definitions.

Add this work order to the PR declaration only after its approval. Retain the
scope inventory and actual released-evaluator results under evidence/WO-IAR-018/.
The only new repository content permitted is this work order and that evidence.

The line-ending test correction is separate execution under the existing
WO-IAR-013 approval. This work order grants no test or implementation scope.

## Preserved inputs

Baseline commit: `a72c8262a134d0e07f78ca2fbfb16c1ecf610894`.
Paths in this table are relative to `docs/engineering/instruction-architecture/`.
Hashes identify Git blob bytes, not platform-converted working-tree bytes.

| File | SHA-256 of Git blob |
| --- | --- |
| `architecture/ARCH-IAR-011.md` | `6c51056665858dc75c4baacf1b2ce3207ac5625e79ba56bce0211ee561adeed2` |
| `architecture/adr/ADR-IAR-011.md` | `30fbcb87e7eed8370b505b99d823b0f9f6cf494f929365202c39f05870c6ad42` |
| `capabilities/CAP-IAR-002.md` | `8e681d1d5114b7ea674251a98239bdad5beab1f135467737282c044497b192bd` |
| `decisions/DEC-IAR-001.md` | `2fcb7d6f5db780a3dcb0631aa791e283ac5172f9308a9703a16358d04e2e6aa7` |
| `evidence/VREC-IAR-009-evaluator.json` | `81dcc0fbfc44d1cbd3a0a78ac40ccd36159f5ac5ad2d08abc049bd914e63b38f` |
| `proposals/progressive-discovery/APPLICABILITY.md` | `5d5dad0b0a34e5e0c2119b881f263eeb0f6a69daf82a809af4c36f0f19e8ce79` |
| `proposals/progressive-discovery/README.md` | `e5a2bb0d29d27e597272dd54975b55432e8f3345a0e57ed2c1f99401455e42c2` |
| `proposals/progressive-discovery/discovery-split-review-source.md` | `881f561c8cfdfb4f8bdcd515475ee4e00cce750dcc60f4e3dd87764b4f36d2a0` |
| `proposals/progressive-discovery/instruction-review-source.md` | `4c210e7e0bb975c3b67cc673bf1986792a2ee46fc37eb5e6722769666d6ff300` |
| `proposals/progressive-discovery/sources.json` | `01f780efabfe86a3d19f39cde5c10529191b5dbebbed9aa5c889dfec989e5eb4` |
| `requirements/REQ-IAR-022.md` | `58446990ca0eadc3c4c655367f7dbe9749008aeddfe534d16867d8e63af6d969` |
| `requirements/REQ-IAR-023.md` | `5023bb77855fe400235680db215d97e3cc175a62a3d2e652ff15bb299af31fa1` |
| `requirements/REQ-IAR-024.md` | `70b8fad3597514932b6d2325a16bc409d213f61c6e51af150edd3f162f6c4690` |
| `requirements/REQ-IAR-025.md` | `23638188b364328ba4460516d4d0cbdef112280a762ee6aa315af6ef8b5b5066` |
| `requirements/REQ-IAR-026.md` | `b618ddacdce23d43e015fa1b5bb75edc4faf574bb45571bdc8847b75053615e8` |
| `requirements/REQ-IAR-027.md` | `846a7f01e7b891c3fb9a70c76e2eb1e843c00ecd29457eabb510583d45ebd282` |
| `specifications/SPEC-IAR-014.md` | `0a2070f45e4c2d280fb17c9ed3ffae70d93dd7fec0383b8806dc98c915c37e90` |
| `verification-records/VREC-IAR-009.md` | `007f49b9491b2696697d13453eeda63d3cb85a88c5e1200738ad586e64401cc6` |
| `verification/VER-IAR-014.md` | `158cd5044c5947578d450e7743e99eb97cb7b60970181e101d33322c5af05254` |

## Out of scope

No changes to these 19 files, accepted definitions, lifecycle history,
VREC-IAR-009, its candidate or evidence. No new verification or release record,
source/test changes, CI workflow changes, weakened gates, historical WO scope
edits, installed harness upgrade, host settings, merge, release or publication.
Unrelated files remain outside the combined PR scope.

## Authorized decision envelope

After human approval, use the released workflow to start, check and complete
only this transport work. Routine evidence and local commits follow the
approved execution procedure. Stop at implemented; this transport work adds
no new assurance claim. The proposed not_required classification relies on
preserving every listed input and the already recorded verification decision.

The existing user instruction to push and create PR #489 supplies its repository
delivery context. This draft neither supplies an approval nor marks that PR
ready. Any additional external action must remain within the actual user grant.

## Required verification

1. Compare each preserved input with the baseline Git blob and its SHA-256 above.
   The check must reject any changed byte after accounting for Git's checkout
   conversion. Also verify VREC-IAR-009's bound evidence using the evaluator.
2. Verify the complete PR diff against the combined paths of WO-IAR-013–018.
   Include this work order and its evidence. Report every uncovered path.
3. Run released doctor, graph validation and selected review preflight.
4. Run the required released scope and handoff checks for this work order.
5. Run check-pr with all six declared work orders and the actual main baseline.
   Retain failures from other selected work orders; do not replace their
   evidence or complete them as part of this transport work.

VER-IAR-014 remains the common verification contract. This transport check
addresses its PR-preparation case and preserved-source constraints only.
The Windows/LF test correction, native qualification and broader implementation
acceptance remain with WO-IAR-013–016. A path-coverage inspection alone is not
a passing check-pr result and does not establish full product verification.

## Evidence and completion

Retain exact commands, evaluator identity, exit codes, baseline/head commits,
path inventory, blob hashes and observed blockers under evidence/WO-IAR-018/.
Report the preserved package, actual check results, unchanged assurance meaning,
final lifecycle state and evaluator-selected next action. Do not mark this work
complete while any of its required checks fails or is missing.

## Stop conditions

Stop on a changed preserved input, additional path, missing approval, failed
integrity or required check. Semantic changes require a new bounded proposal.
An unrelated work order cannot supply coverage merely because its path prefix
is broad. Native qualification gaps and missing handoffs remain visible.
