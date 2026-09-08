# Deliver the plugin definitions in eleven closed groups

<!-- Target expertise: 3.5/10. This score describes the knowledge expected from the reader. -->

This is the definition-delivery plan for the 16 implementation packets in [PR #416](https://github.com/mmzen/se_harness/pull/416).
The baseline is main `560973cf`: candidate source 0.17.0, governing evaluator 0.16.0.
All current PLG records remain draft or open. This plan approves nothing.

## Why split delivery this way

The managed PR workflow selects one work order and checks the whole Git diff against its scope.
It does not combine several work orders' scopes. A passing graph check alone does not make a draft packet eligible for merge.

The umbrella PR remains a place to review the full proposal.
Actual definition delivery uses the groups below, each with one selected work order and exact file paths.
The 16 implementation work orders remain separate.

A closed group contains every new artifact referenced by its metadata, or relies on one introduced earlier.
It does not require all referenced artifacts to be approved merely to exist.
Approval eligibility is a separate check.

## Exact introduction groups

Ranges are inclusive. Every identifier below belongs to the PLG domain.
The selected WO's `[execution_scope].paths` lists the exact files; no whole-domain directory permission is added.

| Group | Selected WO | Records first introduced | Artifacts |
| --- | --- | --- | ---: |
| D01 | WO-PLG-003 | REQ-PLG-006; SPEC/VER/WO-PLG-003 | 4 |
| D02 | WO-PLG-004 | REQ-PLG-007; SPEC/VER/WO-PLG-004 | 4 |
| D03 | WO-PLG-001 | REQ-PLG-001–005; SPEC/VER/WO-PLG-001–002; ARCH-PLG-001; ADR-PLG-001 | 13 |
| D04 | WO-PLG-007 | REQ-PLG-008–014 and REQ-PLG-024; SPEC/VER/WO-PLG-005–008 and SPEC/VER/WO-PLG-014; ARCH-PLG-002; ADR-PLG-002; DEC-PLG-001–002 | 27 |
| D05 | WO-PLG-010 | REQ-PLG-017–018; SPEC/VER/WO-PLG-010 | 5 |
| D06 | WO-PLG-011 | REQ-PLG-019; SPEC/VER/WO-PLG-011 | 4 |
| D07 | WO-PLG-012 | REQ-PLG-020–021; SPEC/VER/WO-PLG-012 | 5 |
| D08 | WO-PLG-009 | REQ-PLG-015–016; SPEC/VER/WO-PLG-009; DEC-PLG-004 | 6 |
| D09 | WO-PLG-013 | REQ-PLG-022–023; SPEC/VER/WO-PLG-013 | 5 |
| D10 | WO-PLG-015 | REQ-PLG-025–026; SPEC/VER/WO-PLG-015; DEC-PLG-005 | 6 |
| D11 | WO-PLG-016 | REQ-PLG-027; SPEC/VER/WO-PLG-016; DEC-PLG-003 | 5 |

For example, `SPEC/VER/WO-PLG-003` means three files: SPEC-PLG-003, VER-PLG-003 and WO-PLG-003.
There are 84 formal artifacts in total: 27 REQs, 16 SPECs, 16 VERs, 16 WOs, two ARCHs, two ADRs and five DECs.

All paths start at `docs/engineering/plugin-integration/`.
REQs, SPECs, VERs, WOs and DECs use `requirements/`, `specifications/`, `verification/`, `work-orders/` and `decisions/`.
ARCHs use `architecture/`; ADRs use `architecture/adr/`. Each filename is its full identifier plus `.md`.

D01 also carries the one-time changes to `GLOSSARY.md`, `docs/engineering/README.md`, and this exact delivery-note file.
Each selected introduction WO owns the exact domain `README.md` path for its slice update.
The slice index links only to already introduced files. Do not copy the complete umbrella index into D01.
In D01, link only the four probe artifacts and this delivery note. Omit the full proposal, operation map and scenario links until those notes exist on the delivery branch. Check every local link before submitting each slice.

Other notes may be delivered separately under the repository's existing notes-only exception.
This delivery note is explicitly in D01's scope; remaining proposal notes are not silently added to that diff.

## Why the shared groups are larger

ARCH-PLG-001 refers to assembly and setup requirements and to both specifications.
D03 therefore introduces the two complete packets and their shared architecture together.

ARCH-PLG-002 refers to both host adapters, both hooks and optional helpers.
Its two host decisions also refer to the probe and adapter work orders.
D04 keeps those five packets and their shared records together, after both probes exist.

This 27-artifact group is the cost of preserving complete packets and the current shared architecture.
It is not a claim that 27 is the smallest possible graph.
Smaller introductions would require partial packets, redesigned architecture boundaries, or temporary relation changes with later amendments.

The review suggested separating shared handlers from native adapters. That is a plausible design boundary, but the extra records have a cost:

| Option | Largest affected introductions | Total introduction groups | Total artifacts |
| --- | --- | ---: | ---: |
| Current shared architecture | One group of 27 | 11 | 84 |
| Separate handlers and native adapters | Two groups of 13 and 16 | 12 | 86 |

The alternative adds one ARCH and one ADR. A finer split into 14 or 15 groups needs three or four additional ARCH/ADR pairs respectively. Retain the current proposal for the probes; before approving ARCH-PLG-002, use their findings to decide whether independent handler delivery justifies the two-boundary split. No approval or typed-relation change is implied by this comparison.

DEC-PLG-004 names WO-PLG-012, so D07 precedes D08.
Each decision arrives with the definition it blocks.
Neither probe carries unrelated architecture records or all five decisions.

The chosen route changes 16 draft WO scopes, creates no additional work order, and changes no typed relation.
There are zero approved-artifact amendment records and zero remove/restore cycles for architecture relations.
Only each group's named records are introduced through its selected WO; the other WOs retain their own implementation boundaries.

## Approval and implementation must be interleaved

D01 and D02 first need their named requirement, specification and verification approvals, followed by the engineering owner's WO approval.
Their definition PRs may then be reviewed and integrated under explicit repository-owner authority.

| Owner | Codex probe | Claude Code probe |
| --- | --- | --- |
| Requirements steward | REQ-PLG-006 | REQ-PLG-007 |
| Technical owner | SPEC-PLG-003 | SPEC-PLG-004 |
| Assurance owner | VER-PLG-003 | VER-PLG-004 |
| Engineering owner | WO-PLG-003 | WO-PLG-004 |

Read-only start and review preflights on main `560973cf` plus these drafts report those four inactive records for each probe, with no upstream or identity blocker. This is a readiness diagnosis, not approval. After actual decisions and definition integration, rerun the current preflight and obtain the separate start decision.

Afterward, the owner can start the probes.
Each probe needs actual retained results, completion and independent assurance through the existing workflow.
An evidenced incompatibility can complete a probe; it cannot authorize an adapter.

D03 similarly needs its complete governing chain approved before its definition PR is eligible.
Assembly and environment implementation remain separate work orders with separate starts.

D04 is not eligible merely because its references resolve.
The probe findings must support positive host-route choices in DEC-PLG-001 and DEC-PLG-002.
The technical owner must resolve the blocked specifications and shared architecture; required VER approvals and the selected WO approval follow.
Excluding a host requires a corresponding scope or artifact decision before continuing this proposed group.

The same rule applies later:

- D08 waits for an available ownership-compatible route and the decisions governing SPEC-PLG-009.
- D10 waits for the assurance owner's positive qualification profile and VER-PLG-015 approval.
- D11 waits for the product owner's reconciliation of plugin-first and current PyPI-first onboarding.

A selected introduction WO does not approve its sibling work orders.
Their later approvals and implementation PRs use their own exact definition and implementation paths.
Adding a path never grants a definition decision or permission to change approved meaning.

After each real integration, rebase the next delivery onto the new base.
Run review preflight and the full Git-derived scope check again.
The scratch results below do not replace those readings.

## The setup dependency must stay visible

The released 0.16.0 evaluator does not supply the plugin ownership migration recommended by DEC-PLG-004.
That choice needs separate evaluator work, owner approval, a public release, and adoption of that released evaluator before the affected connection can proceed.
WO-PLG-009 explicitly excludes implementing that missing core capability.

Choosing to retain repository skills does not implement the proposed migration.
The owner must amend or reject incompatible scope rather than treat a decided DEC as successful delivery.

The shared setup entry changes in this order: WO-PLG-002, WO-PLG-009, then WO-PLG-013.
The reference pages separate environment, repository and maintenance instructions.
Rebase and recheck after each preceding integration; do not edit the shared entry concurrently.

The order is a stated prerequisite, not a new work-order dependency relation.
The existing Git-diff gate enforces each selected WO's declared paths. It does not infer completion dependencies from this table.

## Rehearsal and its limits

On 2026-09-08, the revised draft scopes were rehearsed against main `560973cf` in disposable local repositories.
The artifacts came from the working proposal based on merge `1ed43d38`; no lifecycle state was changed.

For each row, the fixture introduced exactly that group's records and its assigned index changes.
The cumulative index linked only to records already present.
A separate scratch Git history represented the preceding delivery base.
No original repository ref was changed or pushed.

The external released 0.16.0 evaluator ran these commands:

```powershell
& $envPython -I -m se_harness validate $slice --json
& $envPython -I -m se_harness check $slice --artifact $selectedWO --checkpoint scope --from-git $priorCommit --json
```

Here, `$envPython` is the verified interpreter outside the fixture; `$slice` is the disposable repository.
The subprocess clears inherited PYTHONPATH and resolves the installed entry point through its environment's Scripts directory.
`$priorCommit` is the actual preceding scratch commit, and `$selectedWO` comes from the introduction table.

| Group | Cumulative PLG artifacts | Actual changed paths | Graph errors | Scope result |
| --- | ---: | ---: | ---: | --- |
| D01 | 4 | 8 | 0 | completed |
| D02 | 8 | 5 | 0 | completed |
| D03 | 21 | 14 | 0 | completed |
| D04 | 48 | 28 | 0 | completed |
| D05 | 53 | 6 | 0 | completed |
| D06 | 57 | 5 | 0 | completed |
| D07 | 62 | 6 | 0 | completed |
| D08 | 68 | 7 | 0 | completed |
| D09 | 73 | 6 | 0 | completed |
| D10 | 79 | 7 | 0 | completed |
| D11 | 84 | 6 | 0 | completed |

Every graph reading retained the 44 baseline location warnings and reported no authoring advisories.
Each scope reading passed the three scope predicates: declared scope, complete change set and all changed paths within scope.
Local scratch scripts and raw outputs were retained outside the repository under `work/plugin-packet-validation/definition-delivery-git/`.

These are graph and diff-scope observations only.
Draft WOs and unapproved governing chains remain ineligible for review preflight.
No passing GitHub check, host qualification, implementation evidence, VREC, approval or merge is claimed.

The controlling sources are [the managed PR workflow](../../.github/workflows/engineering-harness.yml),
[workflow order](../engineering/WORKFLOW.md), [decision rights](../engineering/DECISION_RIGHTS.md),
and [the state-independent scope contract](../engineering/execution-control-plane/specifications/SPEC-ECP-009.md).
