+++
id = "WO-PLG-017"
type = "work_order"
title = "Portable retention of evidence-skill test output"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[assurance]
commit_bound_verification = "required"
rationale = "Later assurance depends on complete, readable retained evidence after its storage paths change."
decided_by = "engineering-owner"

[delegation]
class = "execution"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/acceptance/linux-replay-attempt1/native-products/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/acceptance/linux-replay-attempt2/native-products/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/native/",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/native-path-map.json",
  "docs/engineering/plugin-integration/evidence/WO-PLG-011/README.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-017/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-017.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-010.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-010-evaluator.json",
  "docs/engineering/plugin-integration/README.md",
  "tests/plugin_integration/evidence-skill/check_retention_paths.py",
]

[relations]
implements = ["REQ-PLG-019"]
specifications = ["SPEC-PLG-011"]
verification = ["VER-PLG-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T21:12:46Z"
decided_by = "engineering-owner"
reason = "The operator explicitly answered \"Approve WO-PLG-017 and authorize the repair\" to the reviewed PR #447 proposal on 2026-09-10. Record DR-REMEDIATION-SCOPE and DR-WO-SELECT under engineering-owner for only WO-PLG-017. Approval of its execution delegation permits the bounded delegated route after the approved class exists at the configured base and the live exact-head required check succeeds. It does not approve an aggregate VREC, assurance, supersession, integration or merge."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T21:21:16Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at ed19676fd2af8b9754f74cbc6bc8664a92d2f803 (check-run 103052409603, source github-checks)."
+++

# Work Order: Portable retention of evidence-skill test output

## Lifecycle

The operator approved this remediation and authorized the delegated repair on
2026-09-10. The released evaluator recorded only draft-to-approved. Start and
completion remain subject to the configured-base and live-check requirements.
No repair has started. This approval does not authorize assurance, supersession,
integration, or preparation of an aggregate verification record.

## Objective

Make the WO-PLG-011 evidence checkout work on the existing Windows CI runner
without changing any observed test payload or weakening CI.

## In scope

Relocate the 55 native-product captures in the exact [path plan](../evidence/WO-PLG-017/path-plan.json)
to shallow numbered paths. Retain a one-to-one original-path/new-path/size/SHA-256
map and a short explanation in the WO-PLG-011 evidence index. Add a focused
retention checker and record the repair's own acceptance evidence.

The existing REQ/SPEC/VER chain is reused because observed-result retention and
decision separation are unchanged. These repair checks supplement the existing
contract; they do not alter its pass conditions or the skill's behavior.

## Out of scope

Skill or evaluator behavior, CI configuration, managed roots, WO-PLG-012 content,
historical result rewriting, or any existing VREC/RLS mutation. Do not rewrite old logs or
manifests to pretend their original paths were different. Their bytes remain
interpretable through the new map. No new successful acceptance claim is inferred
from moving a file.

## Authorized decision envelope

After approval and start, implement only the declared relocation, its checker and
evidence. Proposed paths and original hashes are fixed by path-plan.json. Stop
for a new scope decision if another path or behavior needs changing.

## Constraints

Preserve C=e9418644e22497e622b706cb228f0cd8b36f3b5b and
G=7fe82c95823503e54d2e35e00d8c409a6dd4b065 as ancestors. No amend/rebase.
VREC-PLG-008, its sidecar and all 95 directly selected evidence files remain
unchanged except the separately identified explanatory evidence index. The
record continues to bind the original index at C, never the later explanation.
Before moving files, resolve and check both paths stay in this checkout and
match the approved map. Verify bytes before removing an old working-tree copy.

## Expected change surface

Only execution_scope paths. No payload has moved in this definition proposal.
The longest affected repository-relative path falls from 235 to 72 characters.
Original selected evidence and its interpretation stay visible in Git history.

## Required verification

- Reconcile all 55 original and relocated files one-to-one against the exact
  base: same count, bytes, sizes and SHA-256; original source manifests unchanged.
- Check every tracked path fits the observed Windows checkout root with a
  conservative full-path budget of 250 characters. Keep this a repair acceptance
  check, not a claim about every possible user-chosen checkout root.
- Perform a fresh Windows checkout with core.longpaths=false, then run the
  existing Windows upgrade rehearsal and its dependent integration jobs.
- Confirm Linux can read/reconcile the retained replay inputs. Re-run behavior
  cases only if bytes or relevant implementation changed.
- Run repository-required source/distribution/help/doctor checks, released
  integrity/graph/review-preflight and Git-derived scope/handoff checks.

## Evidence to record

Retain failed CI logs, approved map, exact before/after hashes, checkout logs,
runner identity, repair checker results, live CI outcomes and limitations under
evidence/WO-PLG-017. Keep paths short. Missing/skipped checks are not passes.

## Stop and escalate conditions

Stop on identity, graph, scope or required-check failure; missing or altered
payloads; a failed count/hash reconciliation; or a needed historical mutation.
Completion and later verification preparation remain separate.

## Completion report format

Report the repaired layout, byte/count reconciliation, actual Windows and Linux
outcomes, unchanged historical records, and the next accountable decision.
VREC-PLG-010 and its evaluator sidecar are reserved for later preparation;
their paths grant no decision. An aggregate replacement VREC covering
WO-PLG-011 and this repair needs explicit preparation authority and exact clean
candidate/evidence inputs before capture. Delegated
execution only permits single-WO capture. VREC-PLG-008 stays ready until its
assurance owner separately decides it; supersession needs an eligible verified
successor. Do not treat this draft as either decision.
