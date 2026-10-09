# Review: correct the drafting qualification cases

## Decision requested

Approve the four exact linked revisions below and explicitly authorize their
bounded manual application under **WO-HAG-011**. Then continue the listed
instruction-discovery corrections and revised qualification under its existing
path scope, required commit-bound verification and PR #543 publication grant.

This is a proposal. The accepted files are unchanged, WO-HAG-011 is still
`in_progress`, and the implementation has not been verified. Your "Ok go"
authorized preparing and publishing this review. No test criterion has changed.

## Why this correction is needed

The original request asks for an intent about already-defined greeting behavior.
Claude's drafts made unsupported absence claims and used an acceptance test as
an operational success measure. Codex correctly disclosed the missing operational
measure. A blocked draft is useful negative evidence but cannot establish faster
successful authoring. See the [recorded assessment](../efficiency-assessment.md).

The fixture already has both REQ-P3-900 and VER-P3-900. The positive case therefore
explicitly requests an alternative verification-contract draft as an authoring
exercise. It does not pretend that a requirement or verification plan is missing.
Existing records remain immutable; the agent must author its own new contract.

## Proposed cases

| Case | Requested work | Passing result |
| --- | --- | --- |
| EFF-04A: missing input | Keep the original one-intent request | Acknowledge existing definitions, report the missing operational measure, and avoid invented facts. An explicitly incomplete draft or precise stop is allowed. |
| EFF-04B: positive authoring | Draft one alternative verification contract for REQ-P3-900 | An independently reviewed draft with the correct requirement link, expected result, usable check, pass condition and evidence plan. Planned checks are not reported as executed tests. |

Retain one fresh negative attempt per host. For the positive case, run Claude
once; if correct and unassisted, repeat twice on the same candidate and then run
Codex once. All attempts, failures and candidate changes remain visible. This is
six required native observations if the first positive attempt succeeds. An
incorrect attempt does not count toward the required successful repetitions.

The positive goals remain **under 180 seconds**, **at most 15 native calls** and
**under 40,000 peak input-context tokens**. Report them separately from correctness.
The new task gets its own baseline. Do not claim its results are a same-task
improvement over Opus10. Report negative-case costs separately; an honest stop
does not establish faster completed authoring. No old failure is relabeled.

## Small discovery corrections

Use existing features and released text:

1. Link checklists by full type names, such as `intent` and `verification`.
2. For 0.22.1's duplicate `CONTINUE.md#continue-selected-work`, read its unique
   `#procedure` parent. It contains the exact current step. A read-only check
   confirmed that this works today, while the ambiguous selector still fails.
3. Require applicable instruction reading before the native task's first
   explanation. This explicit fixture setup makes no automatic startup claim.

The implementation uses the already-approved plugin Markdown references and
native/resource test paths. It adds no selector API, service behavior, schema,
dependency or instruction registry. It changes no released resource bytes or
host permissions. Existing refusal and uncertain-write behavior remains required.

## Exact files for review

The [patch](proposed.patch) shows all changes. The [binding](review-binding.json)
records complete before/after SHA-256 values. Proposed `.txt` copies are review
evidence, not active formal artifacts or an installed policy.

| Record | Accepted bytes | Proposed bytes |
| --- | --- | --- |
| `REQ-HAG-014` | [REQ-HAG-014.accepted.txt](REQ-HAG-014.accepted.txt) | [REQ-HAG-014.proposed.txt](REQ-HAG-014.proposed.txt) |
| `SPEC-HAG-008` | [SPEC-HAG-008.accepted.txt](SPEC-HAG-008.accepted.txt) | [SPEC-HAG-008.proposed.txt](SPEC-HAG-008.proposed.txt) |
| `VER-HAG-008` | [VER-HAG-008.accepted.txt](VER-HAG-008.accepted.txt) | [VER-HAG-008.proposed.txt](VER-HAG-008.proposed.txt) |
| `WO-HAG-011` | [WO-HAG-011.accepted.txt](WO-HAG-011.accepted.txt) | [WO-HAG-011.proposed.txt](WO-HAG-011.proposed.txt) |

REQ-HAG-014's measurement wording changes. SPEC-HAG-008 separates the historical
diagnostic from the positive case. VER-HAG-008 states the two cases, actual task,
independent assessment and repetition rules. WO-HAG-011 records their effect on
subsequent work. Its paths, assurance, owners, state and all past lifecycle events
stay unchanged. The existing full VER-HAG-007 / WO-HAG-009/010 qualification remains
required. INT-HAG-002, CAP-HAG-002 and the hosted architecture are unchanged.

## Exact activation requested

The released [AMEND_DEFINITIONS.md procedure](https://github.com/mmzen/se_harness/blob/v0.22.1/templates/repository/standard/docs/engineering/harness/AMEND_DEFINITIONS.md)
says:

> This release has no supported command and relation for creating and activating this linked definition revision.

The installed [change skill](https://github.com/mmzen/se_harness/blob/v0.22.1/plugins/verity-plane/common/skills/change/SKILL.md)
routes amendments through that released procedure. The proposal cannot activate
itself. The requested authorization is a one-time instruction to use this exact
manual linked revision, not a claim that the missing evaluator capability exists:

1. Compare the current files with every accepted digest in review-binding.json.
   Stop if any file changed after this review.
2. Preserve the linked accepted Git-blob bytes, already included here.
3. Apply only the four proposed byte sequences identified by the binding.
4. Record mmzen's actual decision, activation time, before/after digests, selected
   work and effect in `activation.json`. Preserve existing lifecycle events; add
   no invented transition or typed relation. The four revisions link that record.
5. Validate and recheck the affected work through released 0.22.1 before continuing.
   Required gates and human verification still apply; do not replay WO approval
   or start. If activation or a check fails, stop the affected work and retain it.

This authorization does not accept failed results, change lifecycle rules,
accept risks, install a host plugin, release software or authorize merge. The
ordinary review push remains to `codex/hosted-agent-qualification`, targeting
`main` in PR #543. Human verification of the eventual exact candidate is separate.

## Checks performed on this proposal

- All four accepted files match the exact Git blobs at the review base and remain
  unchanged in the working checkout.
- Complete proposed metadata preserves owners, states, relationships, assurance,
  path scope and past lifecycle events. Only the date and stated requirement
  measure change in metadata; the patch shows the body changes.
- In a disposable checkout, released 0.22.1 validated the complete proposed graph:
  **1,991 artifacts, zero errors, 63 existing warnings**. Review preflight was ready,
  with no diagnostics or skew. These checks establish shape, not amendment authority.
- The existing section reader rejects the duplicate heading and returns the full
  unique Procedure section with canonical source identity. No new API is needed.
- No implementation edit or new native trial was performed for this proposal.

Exact checks are retained in [proposal-checks.zip](proposal-checks.zip). Historical
test evidence remains byte-for-byte unchanged. The current draft PR's qualification
gate remains blocked until the required work and evidence are complete.
