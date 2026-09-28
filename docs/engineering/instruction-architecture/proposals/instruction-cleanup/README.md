# Instruction cleanup implementation proposal

Status: **WO-IAR-021 and WO-IAR-023 implemented; verification preparation selected**.
WO-IAR-022 is approved and waits for verified instruction corrections.
The repository remains governed by its selected released evaluator, **0.19.0**.
Candidate source is 0.20.0; this proposal does not release or adopt it.

The [reassessment](../../../../notes/instruction-reassessment-2026-09-28/README.md)
found that the instruction split works, but stale consumers and references still
weaken discovery. The proposed outcome is a usable current instruction path in
the active host, precise references in shipped content, and safe retirement of
obsolete default entry points.

## Recommended sequence

| Stage | Work order | Deliverable | Verification | Dependency |
| --- | --- | --- | --- | --- |
| 1 | [WO-IAR-020](../../work-orders/WO-IAR-020.md) — Qualify active plugin instruction delivery | Active-package inventory and fresh native startup/compaction evidence for Codex and Claude Code. If adoption is needed, an exact repair handoff precedes any real profile change. | [VER-IAR-016](../../verification/VER-IAR-016.md) | Approved; real host adoption remains separately authorized. |
| 2 | [WO-IAR-021](../../work-orders/WO-IAR-021.md) — Correct instruction references and context guidance | Correct source templates, Explorer descriptions, provider references and reading guidance, with focused regression checks. | [VER-IAR-015](../../verification/VER-IAR-015.md) | Approved and started independently of stage 1. |
| 3 | [WO-IAR-022](../../work-orders/WO-IAR-022.md) — Stop shipping obsolete guide pointers safely | Future fresh installations omit the six pointers. Upgrades preserve owner content and supported legacy migration. | [VER-IAR-017](../../verification/VER-IAR-017.md) | DEC-IAR-002 now selects product-wide retirement. Definitions and WO are approved; use verified stage 2 as the implementation base. |
| 4 | Later release package | Published, verified release containing stages 2 and 3. | Exact combined candidate coverage and release contract/record. | Select the version and prepare separate release artifacts when the implementation is verified. No new release ID is invented now. |
| 5 | Later repository adoption work order | Adopt that exact release; remove reviewed stock pointers from this repository only when current consumers no longer need them. | Native evidence from stage 1, exact file hashes, installer preview/apply, owner-byte checks and post-adoption readiness. | Published release, passing native qualification and separate adoption authority. |

Stage 1 does not authorize product-hook changes or real profile updates. A stale
loaded plugin may need adoption rather than a code fix. That distinction must be
settled before claiming F1 resolved. A proposed repair is an intermediate result;
complete qualification still needs actual post-adoption native traces.

The dependencies above are planning and contractual conditions. No unsupported
`depends_on` relation or new automatic lifecycle rule is introduced. The evaluator
continues to compute legality and the next action.

## Findings assigned to work

| Finding | Proposed disposition | Artifact |
| --- | --- | --- |
| F1 — exposed plugin cache differs from current source | Identify what the host actually loads. Qualify released inputs and prepare an exact adoption handoff if needed. Keep native and simulated evidence distinct. | WO-IAR-020 / VER-IAR-016 |
| F2 — generated WO uses a missing old approval anchor | Point to AUTHORITY.md#authority-from-work-approval; request actual human assurance identity. Preserve evaluator rights and history. | WO-IAR-021 / VER-IAR-015 |
| F3 — obsolete README, Explorer and PR-guide references | Update shipped source and generated surfaces. Preserve historical descriptions as historical records. | WO-IAR-021 / VER-IAR-015 |
| F4 — EXECUTE_WORK implies unconditional rereading | Clarify reuse of current material retained in context and rereading of changed/lost prerequisites. Preserve formal inputs and fresh lifecycle checks. | WO-IAR-021 / VER-IAR-015 |
| F5 — limited delivery-envelope margin | Add complete-envelope and oversize checks, including a declared long path. Keep the root's invariants; report actual units and limits. | WO-IAR-021 / VER-IAR-015 |
| F6 — unclear external-action provider prerequisite | Give the applicable control a clear owner and conditional route in both skills and the procedure. Preserve its meaning. | WO-IAR-021 / VER-IAR-015 |
| F7 — navigation duplication | Simplify excess formatting and references only in touched files. **Defer removing the CONTINUE index:** SPEC-IAR-014 explicitly requires it. | Bounded subset in WO-IAR-021; index removal requires a later accepted-definition change. |
| F8 — separate outcome/scope confirmation turns | Permit one exchange covering both when clear; retain both confirmations and clarify material ambiguity. | WO-IAR-021 / VER-IAR-015 |
| Six legacy human-guide pointers | Stop generating them for new installations, preserve existing owner files on upgrade, and remove eligible repository copies only through later adoption. | REQ-IAR-028 / SPEC-IAR-015 / WO-IAR-022 / VER-IAR-017; choice in DEC-IAR-002 |

## Definitions reused unchanged

The approved [INT-IAR-001](../../intent/INT-IAR-001.md) and
[CAP-IAR-002](../../capabilities/CAP-IAR-002.md) already define the intended ability.
There is no new intent or duplicated capability.

| Accepted record | Use in this package |
| --- | --- |
| [REQ-IAR-022](../../requirements/REQ-IAR-022.md) | Compact root and complete delivery-envelope review. |
| [REQ-IAR-023](../../requirements/REQ-IAR-023.md) | Current-action instructions and exact prerequisite references. |
| [REQ-IAR-026](../../requirements/REQ-IAR-026.md) | Current repository context at native startup and compaction. |
| [REQ-IAR-027](../../requirements/REQ-IAR-027.md) | Preserved instruction meaning, complete migration and measured reading cost. |
| [SPEC-IAR-014](../../specifications/SPEC-IAR-014.md) | Governing discovery contract; its approved meaning is unchanged. |
| [ARCH-IAR-011](../../architecture/ARCH-IAR-011.md) and [ADR-IAR-011](../../architecture/adr/ADR-IAR-011.md) | Existing entry, evaluator and host boundaries, selected where their addressed requirements apply. |

Completed WOs IAR-013 through IAR-019 remain historical authority for their own
work. Their completed scope does not authorize this correction. The old broad
VER-IAR-014 remains unchanged; the new contracts give each proposed WO concrete,
bounded evidence criteria.

## New formal artifacts

| Artifact | State | Purpose |
| --- | --- | --- |
| [REQ-IAR-028](../../requirements/REQ-IAR-028.md) | approved | Safe retirement behavior and owner-content acceptance conditions. |
| [SPEC-IAR-015](../../specifications/SPEC-IAR-015.md) | approved | Exact six-path set, current consumers, preservation, legacy migration, cleanup conditions and failure behavior. Supplements SPEC-IAR-014. |
| [VER-IAR-015](../../verification/VER-IAR-015.md) | approved | References, protected meaning, full delivery envelope and six task-reading traces. |
| [VER-IAR-016](../../verification/VER-IAR-016.md) | approved | Actual loaded package and native events on each claimed host. |
| [VER-IAR-017](../../verification/VER-IAR-017.md) | approved | Fresh install, packaging, supported upgrades, owner bytes, refusal and retry. |
| [WO-IAR-020](../../work-orders/WO-IAR-020.md), [WO-IAR-021](../../work-orders/WO-IAR-021.md), [WO-IAR-022](../../work-orders/WO-IAR-022.md) | 020 in progress; 021 implemented; 022 approved | Separately bounded execution scopes and decision envelopes. |
| [DEC-IAR-002](../../decisions/DEC-IAR-002.md) | decided | Product-wide retirement selected by the requesting repository owner. |

Typed metadata links provide the formal traceability: the new requirement derives
from CAP-IAR-002; SPEC-IAR-015 specifies it; VER-IAR-017 verifies it; WO-IAR-022
selects those records and the reused migration requirement. DEC-IAR-002's scope
choice is now resolved; it does not approve the four related records. The table is a review
index, not an additional source of authority.

## Selected retirement scope

The owner selected **product-wide retirement** in DEC-IAR-002. New repositories should not
receive obsolete entry points. This adds packaging and migration testing; it
avoids carrying the same cleanup into every future installation.

The supplied answer was “For DEC-IAR-012: product wide retirement.” There is no
DEC-IAR-012 in this repository. DEC-IAR-002 is the unique presented retirement
decision with that option. The released evaluator recorded its disposition as
`product-wide`, retaining the supplied answer verbatim. Its required
`repository-owner` label represents the human requester, not the applying agent.

The six paths are under `docs/engineering/`:

- `OPERATING_CARD.md`
- `DECISION_RIGHTS.md`
- `QUALITY_GATES.md`
- `WORKFLOW.md`
- `TRACEABILITY.md`
- `TECHNICAL_COMMUNICATION.md`

Keep `ARTIFACT_AUTHORING.md`, `WORKFLOW.json`, `QUALITY_GATES.json`, the current
root and harness collection, owner instructions, historical evidence and supported
old-release adapters. The six pointers total only 210 words; this is chiefly a
discoverability improvement, not a large startup-context saving.

Use the existing seed ownership boundary. Current stock pointers and owner
content survive upgrades; an absent seed stays absent. Recognized older full
guides still follow their accepted, version-conditioned migration. Customized
legacy content needs an explicit owner plan. Removing source templates must not
silently break that older migration path. No new deletion CLI is proposed.

## Verification and risks

The human confirmed **required commit-bound verification** for each WO. Expected results come
from requirements and specifications, not candidate output. Source changes are
tested in isolated candidate environments; real repository lifecycle operations
continue through the selected released evaluator.

| Risk | Required response |
| --- | --- |
| Cache inspection is mistaken for active loading | WO-IAR-020 records actual host/package selection and native events. Unavailable or stale inputs remain a qualification gap. |
| A path edit weakens a decision or provider control | WO-IAR-021 preserves the rule and stops for review if its meaning must change. |
| Removing templates loses owner content or old-release support | WO-IAR-022 proves byte preservation and supported upgrade behavior before completion. |
| Word-count improvement hides a missing prerequisite | VER-IAR-015 checks six complete reading paths and reports formal inputs separately. Scores are editorial, not gates. |

The six reading paths are new drafting, resumed execution, verification decision,
PR preparation, failed-check recovery and evaluator setup. Count unique instruction
words including COMMUNICATION.md and all required reference sections. Do not claim
token savings or native delivery from a file-size or protocol measurement.

## Execution and review status

The human approved the reviewed package with “I approve, you can start the work
orders.” The selected 0.19.0 evaluator applied the five definition approvals and
three WO approvals. Actual human mmzen and the exact decision are retained in
the reasons; the evaluator's legacy role labels do not replace that identity.
WO-IAR-020 and WO-IAR-021 passed start checks. WO-IAR-021 and the separate
WO-IAR-023 correction subsequently passed complete combined-scope handoff and
were transitioned to `implemented` by the evaluator. WO-IAR-020 remains in
progress; no native-qualification completion is claimed.

Full testing exposed two test assumptions outside WO-IAR-021's paths. The human
separately approved [WO-IAR-023](../../work-orders/WO-IAR-023.md), required
commit-bound assurance and the legacy approval encoding. It is now implemented.
The reviewed [test correction](test-correction.patch) is applied; its
[isolated review](test-correction-review.json) preserves the pre-approval probe.

The current source correction and its evidence are described in
[the implementation review](../../evidence/WO-IAR-021/review.md).
[WO-IAR-023 evidence](../../evidence/WO-IAR-023/review.md) explains the two test
changes and the pre-existing CRLF fixture failure. Original failing results are
retained beside corrected checks. The initial proposal remains in Git at
d243f792ffb9cfda4929a0eaeb5b4db16f88220f.

WO-IAR-020 found both real hosts still select plugin 0.1.0. Isolated Codex
startup and compaction passed with the 0.2.0 package. Claude delivered the full
startup root, but its isolated OAuth login expired before the model response;
compaction remains unverified. The
[adoption handoff](../../acceptance/plugin-adoption/README.md) names exact
replacement inputs and remaining authority. Real profiles remain unchanged.

WO-IAR-022 has not started. No compatibility pointer is removed. No human
verification, release or repository adoption is inferred from the approvals.
The PR remains a draft while these stages are assessed.
