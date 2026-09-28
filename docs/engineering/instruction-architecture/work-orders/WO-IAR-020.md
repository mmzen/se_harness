+++
id = "WO-IAR-020"
type = "work_order"
title = "Qualify active plugin instruction delivery"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Later discovery, adoption and assurance decisions rely on changed trusted content or retained host evidence. The human approved verification bound to the exact candidate commit."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/instruction-architecture/acceptance/plugin-adoption/",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-020/",
]

[relations]
implements = ["REQ-IAR-026"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-016"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T07:52:17Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve, you can start the work orders\". Approval covers the reviewed instruction-cleanup package and required commit-bound assurance. Legacy evaluator role engineering-owner records that human decision; Codex applies it. Reviewed SHA-256 4e575d54072d5d391ced30b566d7a3a5e6d427ca005a32290c608d4f310a9a54."
scope_paths = ["docs/engineering/instruction-architecture/acceptance/plugin-adoption/", "docs/engineering/instruction-architecture/work-orders/WO-IAR-020.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-020/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T07:53:47Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the selected work under mmzen's recorded approval and passing start checks."
+++

# Qualify active plugin instruction delivery

## Objective

Close finding F1 with evidence of which plugin the host loads and whether that
configuration delivers the current root at startup and after compaction.

## In scope and planned sequence

1. Inventory the actual Codex and Claude Code configuration read-only. Compare
   loaded skills and hooks with the exposed stale cache and compatible released
   package; record package identity, provenance and hashes.
2. Rehearse native events in isolated profiles and disposable repositories using
   the existing delivery demonstration. Record startup, compaction, repository
   switch and the failure cases in VER-IAR-016.
3. If repair is needed, prepare an exact adoption handoff: released package,
   source, target host/profile, action, expected effects, recovery and evidence.
   Present it for the external configuration authority before changing a real
   installation. No cache patch or candidate-source substitution is permitted.
4. After separately authorized repair, verify actual loading and repeat native
   events. Record the final qualification or exact remaining blocker.

## Out of scope

Changes to product hooks, evaluator code, root policy, real host configuration
or repository installation are not authorized by this WO. Selecting a missing
product fix requires a new bounded work order. No legacy guide is deleted.

## Authorized decision envelope

After approval, the agent may choose inspection tools, construct disposable
fixtures, execute the specified non-publishing demonstrations and retain the
results. An adoption handoff does not grant the authority it requests.
The read-only live inventory is not limited by repository path scope; any
durable repository output is limited to the declared acceptance/evidence paths.

## Dependencies and stop conditions

No dependency on the editorial correction is needed for initial inventory.
Use compatible released inputs. Stop the affected demonstration on missing
host capability or uncertain prior effects. An unavailable host or unresolved
adoption is a qualification gap, not a successful completion. Product retirement
may be developed in isolation; real repository cleanup waits for this evidence.

## Required verification and evidence

Apply VER-IAR-016. Keep actual native traces distinct from protocol tests and
older temporary demos. Record host/profile and repository identities without
credentials. Future retirement decisions rely on this evidence.

## Assurance and completion

The human repository owner, mmzen, confirmed commit-bound assurance as
`required`: later discovery, adoption and assurance decisions rely on changed
trusted content or retained host evidence. Verification must bind the exact
candidate commit. The recorded approval is: "I approve, you can start the work orders".

The evaluator records work authority through the explicit lifecycle transition.
This approval does not grant verification acceptance, release or real host
configuration authority beyond the decision envelope above.

After approval, use the repository-selected released evaluator for the exact
WO's start, scope and handoff checks. Retain actual findings and the complete
declared change set. Prepare a VREC through the supported command for the exact
clean candidate commit; only a human may accept it.

The completion report gives the WO ID, candidate commit, changed files, contract
criteria and observed evidence, unresolved limitations, retained evidence paths,
actual evaluator result and its next typed step. A passing preview is not an
applied transition. No accepted definition or history is rewritten by this WO.
