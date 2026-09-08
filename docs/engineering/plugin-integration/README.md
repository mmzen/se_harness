# Native coding-agent plugin implementation packets

**16 small work packages, all proposed.** Each package has focused requirements, one specification, one verification contract, and one bounded work order. Two shared architecture decisions cover the significant boundaries. Five open decisions identify choices that still need an owner.

These artifacts develop the [plugin proposal](../../notes/plugin-installation-proposal-2026-09-06.md), [operation workflows](../../notes/plugin-operation-workflows-2026-09-06.md), and [16 scenarios](../../notes/plugin-scenarios/README.md). The notes and artifacts are reviewed together in [PR #416](https://github.com/mmzen/se_harness/pull/416), which incorporates the notes from PR #360 at `9e894e99`.

The notes and artifacts use main `560973cf`, with candidate source 0.17.0 and governing evaluator 0.16.0. Approved artifact contracts and the selected released evaluator govern implementation.

No implementation, approval, verification record, or release record is included. All definitions and work orders remain `draft`; the five decision records remain `open`. File creation and validation do not authorize work.

## Packages

Open a work order for its exact change scope. Its metadata selects the requirements, specification, verification contract, and applicable architecture.

| Work package | Requirements | Detailed contract and checks | Planned prerequisites |
| --- | --- | --- | --- |
| [01. Assemble plugin packages](work-orders/WO-PLG-001.md) | REQ-PLG-001–002 | [Specification](specifications/SPEC-PLG-001.md) · [Verification](verification/VER-PLG-001.md) | Can begin independently after approval. |
| [02. Check Python and prepare the environment](work-orders/WO-PLG-002.md) | REQ-PLG-003–005 | [Specification](specifications/SPEC-PLG-002.md) · [Verification](verification/VER-PLG-002.md) | Package contract and trusted wheel from 01. |
| [03. Prove Codex activation](work-orders/WO-PLG-003.md) | REQ-PLG-006 | [Specification](specifications/SPEC-PLG-003.md) · [Verification](verification/VER-PLG-003.md) | Disposable probe; no production adapter required. |
| [04. Prove Claude Code activation](work-orders/WO-PLG-004.md) | REQ-PLG-007 | [Specification](specifications/SPEC-PLG-004.md) · [Verification](verification/VER-PLG-004.md) | Disposable probe; no production adapter required. |
| [05. Register the Codex adapter](work-orders/WO-PLG-005.md) | REQ-PLG-008 | [Specification](specifications/SPEC-PLG-005.md) · [Verification](verification/VER-PLG-005.md) | 01, 02, 03, 07, 08 and shared skills; accepted route from DEC-PLG-001. |
| [06. Register the Claude Code adapter](work-orders/WO-PLG-006.md) | REQ-PLG-009 | [Specification](specifications/SPEC-PLG-006.md) · [Verification](verification/VER-PLG-006.md) | 01, 02, 04, 07, 08 and shared skills; accepted route from DEC-PLG-002. |
| [07. Deliver verified session context](work-orders/WO-PLG-007.md) | REQ-PLG-010–012 | [Specification](specifications/SPEC-PLG-007.md) · [Verification](verification/VER-PLG-007.md) | 02; protocol fixtures precede live adapter qualification. |
| [08. Check supported tool actions](work-orders/WO-PLG-008.md) | REQ-PLG-013–014 | [Specification](specifications/SPEC-PLG-008.md) · [Verification](verification/VER-PLG-008.md) | 02; protocol fixtures precede live adapter qualification. |
| [09. Connect repositories and select skill discovery](work-orders/WO-PLG-009.md) | REQ-PLG-015–016 | [Specification](specifications/SPEC-PLG-009.md) · [Verification](verification/VER-PLG-009.md) | 02; DEC-PLG-004. Its recommended migration needs separate evaluator work, release and root adoption; 0.16.0 does not provide it. |
| [10. Guide artifact and work-order changes](work-orders/WO-PLG-010.md) | REQ-PLG-017–018 | [Specification](specifications/SPEC-PLG-010.md) · [Verification](verification/VER-PLG-010.md) | 02; live integration follows the applicable adapter. |
| [11. Guide evidence and assurance handoffs](work-orders/WO-PLG-011.md) | REQ-PLG-019 | [Specification](specifications/SPEC-PLG-011.md) · [Verification](verification/VER-PLG-011.md) | 02 and the change workflow in 10. |
| [12. Adapt the two read-only skills](work-orders/WO-PLG-012.md) | REQ-PLG-020–021 | [Specification](specifications/SPEC-PLG-012.md) · [Verification](verification/VER-PLG-012.md) | 02; live coexistence follows 09. |
| [13. Repair and upgrade safely](work-orders/WO-PLG-013.md) | REQ-PLG-022–023 | [Specification](specifications/SPEC-PLG-013.md) · [Verification](verification/VER-PLG-013.md) | 02, 09, and the applicable adapter. |
| [14. Add optional read-only helpers](work-orders/WO-PLG-014.md) | REQ-PLG-024 | [Specification](specifications/SPEC-PLG-014.md) · [Verification](verification/VER-PLG-014.md) | Qualified host registration; main-agent fallback remains valid. |
| [15. Qualify workflows and measure cost](work-orders/WO-PLG-015.md) | REQ-PLG-025–026 | [Specification](specifications/SPEC-PLG-015.md) · [Verification](verification/VER-PLG-015.md) | Claimed features from 01–14; accepted qualification profile from DEC-PLG-005. |
| [16. Document qualified plugin installation](work-orders/WO-PLG-016.md) | REQ-PLG-027 | [Specification](specifications/SPEC-PLG-016.md) · [Verification](verification/VER-PLG-016.md) | 15; DEC-PLG-003 resolved. |

The prerequisites above are a delivery plan. The current graph has no work-order dependency relation, so this table does not create a new enforced gate. Each work order states its own constraints. Open decisions use the existing `blocks` relation.

The host probes can finish with a well-supported incompatibility finding. That result does not authorize the corresponding production adapter. Common scripts can be checked with protocol fixtures before host adapters exist; only later host tests establish live coverage.

## Shared architecture

| Boundary | Architecture | Proposed decision |
| --- | --- | --- |
| Provided Python, local environment, one released evaluator | [ARCH-PLG-001](architecture/ARCH-PLG-001.md) | [ADR-PLG-001](architecture/adr/ADR-PLG-001.md) |
| Host integration without lifecycle authority | [ARCH-PLG-002](architecture/ARCH-PLG-002.md) | [ADR-PLG-002](architecture/adr/ADR-PLG-002.md) |

No architecture or ADR is created merely to fill a slot in a package. Work orders select shared architecture only where it directly addresses their requirements.

## Decisions to resolve

| Open decision | Owner | Blocked definition and resulting work |
| --- | --- | --- |
| [DEC-PLG-001: Codex activation route](decisions/DEC-PLG-001.md) | Technical owner | SPEC-PLG-005, then production adapter work; the probe remains available for approval. |
| [DEC-PLG-002: Claude Code activation route](decisions/DEC-PLG-002.md) | Technical owner | SPEC-PLG-006, then production adapter work; the probe remains available for approval. |
| [DEC-PLG-003: Plugin-first public onboarding](decisions/DEC-PLG-003.md) | Product owner | REQ-PLG-027, then onboarding work until the PyPI-first contracts are reconciled. |
| [DEC-PLG-004: Skill discovery and ownership](decisions/DEC-PLG-004.md) | Technical owner | SPEC-PLG-009, then repository connection and migration. |
| [DEC-PLG-005: Qualification profile](decisions/DEC-PLG-005.md) | Assurance owner | VER-PLG-015, then qualification until configurations and acceptance limits are defined. |

Each decision blocks a definition owned by its named decision-maker. Work-order approval still needs the complete approved chain. A negative or preview option does not supply a positive route, amend another artifact, or authorize implementation.

## Existing artifacts reused

| Subject | Existing upstream chain | Boundary retained |
| --- | --- | --- |
| Installation and distribution | [CAP-DST-001](../harness-distribution/capabilities/CAP-DST-001.md) → [INT-DST-001](../harness-distribution/intent/INT-DST-001.md) | One standard harness; owner content and repository version selection are preserved. |
| Session instructions | [CAP-IAR-001](../instruction-architecture/capabilities/CAP-IAR-001.md) → [INT-IAR-001](../instruction-architecture/intent/INT-IAR-001.md) | Verified governance follows the existing managed route. |
| Workflow skills | [CAP-WEX-001](../workflow-execution/capabilities/CAP-WEX-001.md) → [INT-WEX-001](../workflow-execution/intent/INT-WEX-001.md) | The evaluator owns lifecycle legality; skills remain adapters. |

Existing evaluator identity, installation, authoring, evidence, decision, and delegation contracts remain unchanged. New requirements describe plugin behavior at those interfaces; they do not replace the engine's rules.

The current source has a unified `init` path; the released 0.16.0 evaluator retains the transitional `adopt` alias. Implementation must inspect the exact selected evaluator instead of copying older commands from the proposal.

Authenticated decisions remain separate work in [WO-ECP-004](../execution-control-plane/work-orders/WO-ECP-004.md), under [REQ-ECP-008](../execution-control-plane/requirements/REQ-ECP-008.md). That work order is still draft at this baseline. The repair of the README incident does not prove prevention. Plugin hooks do not close [issue #347](https://github.com/mmzen/se_harness/issues/347) or authorize remote effects.

## Review and delivery

Keep PR #416 as the umbrella review. Deliver definitions through the eleven groups below, with one selected work order per PR. The [full delivery plan](../../notes/plugin-definition-delivery-2026-09-08.md) gives every introduced identifier, exact scope ownership, approval conditions and the measured rehearsal.

| Introduction | Packets | Selected work order | Shared records introduced | Formal artifacts |
| --- | --- | --- | --- | ---: |
| D01 | 03 | [WO-PLG-003](work-orders/WO-PLG-003.md) | First index, glossary and delivery-note changes | 4 |
| D02 | 04 | [WO-PLG-004](work-orders/WO-PLG-004.md) | None | 4 |
| D03 | 01, 02 | [WO-PLG-001](work-orders/WO-PLG-001.md) | ARCH-PLG-001, ADR-PLG-001 | 13 |
| D04 | 05, 06, 07, 08, 14 | [WO-PLG-007](work-orders/WO-PLG-007.md) | ARCH-PLG-002, ADR-PLG-002, DEC-PLG-001, DEC-PLG-002 | 27 |
| D05 | 10 | [WO-PLG-010](work-orders/WO-PLG-010.md) | None | 5 |
| D06 | 11 | [WO-PLG-011](work-orders/WO-PLG-011.md) | None | 4 |
| D07 | 12 | [WO-PLG-012](work-orders/WO-PLG-012.md) | None | 5 |
| D08 | 09 | [WO-PLG-009](work-orders/WO-PLG-009.md) | DEC-PLG-004 | 6 |
| D09 | 13 | [WO-PLG-013](work-orders/WO-PLG-013.md) | None | 5 |
| D10 | 15 | [WO-PLG-015](work-orders/WO-PLG-015.md) | DEC-PLG-005 | 6 |
| D11 | 16 | [WO-PLG-016](work-orders/WO-PLG-016.md) | DEC-PLG-003 | 5 |

Each group contains every new artifact its metadata references, or relies on an earlier group.
The shared architecture links make D03 and D04 larger. Keeping complete packets and those links gives 13 and 27 artifacts respectively; the plan does not hide that review cost.
DEC-PLG-004 names WO-PLG-012, so D07 precedes D08.

All sixteen draft scopes now name their own definition files. Each selected introduction WO additionally names only its group's shared and peer records.
D01 owns the initial glossary, engineering index and exact delivery-note changes; every introduction selector owns the exact domain index path.
Each delivered index links only to artifacts already present. This complete umbrella index is not the D01 index.
D01 omits the proposal, operation-map and scenario links until those notes are delivered; its index links only its four probe records and the delivery note.

No broad carrier work order or whole-domain scope is created. There are 16 draft scope edits, no typed-relation changes, and no approved-artifact amendment records.
Definition carriage grants no permission to implement a sibling work order or approve its artifacts.

Approve each selected governing chain and work order before its definition PR becomes review-eligible.
After D01 and D02 integrate, the probes still need explicit starts, actual findings and the existing independent-assurance route.
D04 then needs positive host-route decisions and approval of its shared governing chain. A negative probe result can complete the investigation but cannot supply adapter authority.

The recommended DEC-PLG-004 migration is not available in released 0.16.0. Before affected repository connection, it needs a separate evaluator packet, approval, public release and root adoption.
WO-PLG-009 cannot implement that missing capability. A retain-repository or rejection choice requires the owner to amend or reject incompatible proposed scope.
D10 also waits for its qualification decision; D11 waits for onboarding reconciliation.

Shared setup changes run in this order: WO-PLG-002, WO-PLG-009, WO-PLG-013.
Rebase after the preceding integration and recheck the complete PR diff. This is an explicit sequencing constraint; no new work-order dependency mechanism is claimed.

The eleven cumulative scratch slices passed released-0.16 graph validation and Git-derived scope checks: zero errors, 44 baseline warnings, no advisories.
Every PLG record remained draft or open. These observations prove reference closure and path coverage only; they do not establish approval, review-preflight eligibility or a passing GitHub check.

Every implementation WO still requires commit-bound verification. Retained implementation evidence, a later VREC, its independent decision, and each integration remain separate work.
