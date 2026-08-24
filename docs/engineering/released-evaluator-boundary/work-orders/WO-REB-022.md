+++
id = "WO-REB-022"
type = "work_order"
title = "Repair the junction-predicate capability rule on the pinned Python 3.11 lane"
status = "draft"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The defect this work order repairs refuses every interpreter at every evaluator-identity boundary on every supported lane below Python 3.12 off Windows, which is every lane the workflow pins. The repair therefore decides whether a released evaluator, a predecessor evaluator, or a candidate runtime may execute at all, and it widens the condition under which the junction check is treated as decided rather than unavailable. A defect in the repair would either keep the boundary unusable or accept a runtime that cannot classify a reparse point it can encounter. Verification must bind the exact implementation commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/evidence/WO-REB-022-junction-predicate-capability.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-024.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-011.md",
  "docs/engineering/released-evaluator-boundary/verification/VER-REB-010.md",
  "docs/engineering/released-evaluator-boundary/work-orders/WO-REB-022.md",
  "repository_tools/interpreter_safety.py",
  "se_harness/interpreter_safety.json",
  "se_harness/interpreter_safety.py",
  "tests/test_interpreter_safety.py",
]

[relations]
implements = ["REQ-REB-024"]
specifications = ["SPEC-REB-011"]
architecture = ["ARCH-REB-010", "ADR-REB-010"]
verification = ["VER-REB-010"]
+++

# Work Order: Repair the junction-predicate capability rule on the pinned Python 3.11 lane

## Lifecycle and authorization

This draft packet proposes a bounded repair of one defect in the rule implemented under `WO-REB-021`. It grants no execution or lifecycle authority while draft.

`WO-REB-021` is `implemented` and the work-order lifecycle admits only `verified` and `released` from that state, so the repair cannot be carried under it. This is a separate work order for that reason and not by preference. It does not reopen, amend, or contradict `WO-REB-021`'s implemented transition: the implementation that transition accepted is exactly the implementation this repair corrects, and the correction is recorded here rather than by editing that work order's retained evidence.

If the accountable owners approve this work order, a separate explicit start may authorize only the local implementation and qualification described here. Approval and start do not authorize a release, a tag, a publication, a deployment, a maintenance mutation, credential use, an external-policy change, or a root-evaluator adoption. GitHub issue #106's own boundary applies unchanged.

Pushing this branch and opening one pull request that carries this work order alone are authorized by the engineering owner in the same act that approves this packet. The `WO-REB-021` pull request is not to be reused: two work orders shall not share one diff.

## Defect

`SPEC-REB-011` rule 4 as amended gives the junction predicate two routes: `pathlib.Path.is_junction`, which exists from Python 3.12, and the reparse-point `stat` constants `FILE_ATTRIBUTE_REPARSE_POINT` and `IO_REPARSE_TAG_MOUNT_POINT`, which were intended to carry the predicate on Python 3.11. Where neither exists the rule refuses with `EPS011`.

The second route does not exist on the pinned lane. `FILE_ATTRIBUTE_REPARSE_POINT` is defined in the cross-platform `Lib/stat.py` and is present everywhere, but `IO_REPARSE_TAG_MOUNT_POINT` is published only by the `_stat` extension and only where the platform defines it. On Python 3.11 off Windows the runtime therefore has neither route, `link_classification_available()` returns false, and every registered boundary refuses every interpreter with `EPS011` before any identity is established.

The `ubuntu` lane of the hosted workflow, which pins `python-version: "3.11"`, measured this on the `WO-REB-021` candidate commit: 33 failures and 38 errors, every one of them traced to `EPS011 link_predicate` raised in `evaluate`. The Windows development lane cannot reach the defect, because on Windows both reparse constants are present at every supported version. `WO-REB-021`'s retained evidence disclosed exactly this as an open coverage gap: capability withdrawal proved the fallback logic, not the 3.11 runtime.

The defect is in the capability rule, not in the detection. A junction is a Windows reparse-point construct. On a platform whose stat result reports no reparse information, no path is a reparse point, so the predicate's answer is `False` by construction rather than unavailable — and `pathlib.Path.is_junction` returns exactly that answer for every path on such a platform from 3.12 onward. Refusing below 3.12 while accepting from 3.12, on the same platform, with the same detection power, protects nothing.

## Objective

Make the junction predicate decided on every supported runtime by distinguishing a runtime that cannot classify a reparse point it may encounter from a runtime that observes no reparse information at all, without introducing a platform-name conditional and without weakening any refusal.

## In scope

- Add a third named route to the junction predicate in both conforming loaders: the `os.stat_result` members through which a filesystem reports reparse information. Where the stat result carries neither member the predicate is decided and answers `False`; where it carries them and neither predicate route exists, `EPS011` still refuses.
- Amend `SPEC-REB-011` rule 4 to state the three routes and the narrowed `EPS011` condition, and restate the mechanical checks the rule's own drift text names.
- Amend `VER-REB-010`'s junction-predicate method row and refusal scenario 4 to match, in the same act, because they restate the same rule.
- Amend `REQ-REB-024` to state explicitly that a runtime observing no reparse information answers the predicate rather than disabling the check, and that the third route is a capability observation and not a platform test.
- Update the `EPS011` and `ISC016` summaries in the declaration to describe the narrowed condition. No case or corpus entry is added, removed, renumbered, or reordered.
- Extend the focused conformance tests so every combination of the three routes is constructable on either lane, so the pinned lane's own combination is covered on both, and so the absence of a platform name in the capability functions is asserted mechanically over the loader sources.
- Record the retained evidence, including the measured reproduction of the hosted failure and the measured repair.

## Out of scope

- Editing `WO-REB-021`, its retained evidence, or any lifecycle event either records.
- Changing `VREC-REB-017`. Its disposition is a separate governance decision recorded in that record.
- Any other case, boundary, recorded fact, refusal, or acceptance in the declared rule.
- The runtime-identity and evaluator-evidence schemas, the boundary registry, and the evaluation order.
- Raising `requires-python`, changing a pinned lane version, or adding a lane.
- The unresolved `main` conflict on the `WO-REB-021` pull request.

## Authorized decision envelope

After approval and explicit start, implementation may choose the name of the third route's constant and predicate function, the wording of the amended rule text beyond the required routes and condition, the wording of the two declaration summaries, and how the conformance tests construct each route combination.

It may not add, remove, renumber, or reorder a declared case or corpus identifier; turn an acceptance into a refusal or the reverse; add a per-boundary waiver; introduce a platform-name conditional in policy, in the declaration, or in the capability functions; make the declaration anything other than data; change the runtime-identity or evaluator-evidence schemas; make `repository_tools` import `se_harness` or the reverse; withdraw `EPS011` from the declared case list; leave the two loaders in disagreement; or touch an unlisted path.

## Constraints

- Python 3.11+ standard library only. `repository_tools` continues to import only the standard library and its own package.
- The two loaders remain mirrors, held in agreement by the existing cross-runtime conformance check.
- `EPS011` remains a declared refusal, reachable and tested. The repair narrows when it fires; it does not remove it.
- Every refusal present before this repair remains present. The only widened condition is the one the defect wrongly refused.
- Detection shall not depend on the platform name, in policy or in code. The third route is an observation of the runtime's own stat-result surface.
- The declaration stays data: no code, no platform conditional expressed as code, no waiver list.
- Re-measure rather than infer: the reproduction and the repair are both measured against the hosted lane's own failure, and the full suite is compared against the same four known Windows line-ending failures.
- The execution scope is a maximum allowlist. The evidence records the actual changed subset.

## Expected change surface

- One added constant and one added predicate function in each of the two loaders, and one narrowed condition in each.
- Two summary strings in the declaration.
- Rule 4 and one amendment section in `SPEC-REB-011`; one method row, one refusal scenario, and one amendment section in `VER-REB-010`; one clarifying paragraph and one amendment section in `REQ-REB-024`.
- One focused test module: the route-withdrawal helper, the corrected capability tests, and the added combination, regression, and platform-name-absence tests.
- The domain index and one retained evidence file.

## Required verification

- Reproduce the hosted failure locally before the repair, by withdrawing the three named routes to the pinned lane's profile and running the modules that failed there. Record the failure count and at least one verbatim failure that matches the hosted log.
- Prove the repair against the same simulated profile: the same modules pass, and the capability is reported as decided by the third route.
- Prove the whole capability decision table, both loaders, every combination of the three routes, on whichever lane runs the tests.
- Prove `EPS011` still refuses a real environment when reparse information is observable and neither predicate route exists, and that a runtime with no reparse surface accepts the same environment and derives the same environment root.
- Prove mechanically that no platform name appears in the capability functions of either loader.
- Prove the declared case list, evaluation order, boundary registry, corpus identifiers, and the bidirectional declaration comparison are unchanged.
- Run the focused module, the complete supported suite, graph validation, distribution validation, the portable-surface check, and the phase-appropriate preflight. Compare full-suite failure names against the four known line-ending failures; the delta shall be exactly the tests added here.
- Run the released-evaluator validation from a released-version environment outside the checkout, not the in-tree candidate CLI.
- Confirm on the hosted lane that the previously failing job passes, and record its identifier.

## Evidence to record

Retain, under `docs/engineering/released-evaluator-boundary/evidence/WO-REB-022-junction-predicate-capability.md`: the approved packet and preflight; the base commit; the hosted failure as measured, with the job identifier and a verbatim excerpt; the local reproduction under the simulated pinned-lane profile and the measured repair; the actual changed-path manifest; the capability decision table with the test-owned expectation; the before-and-after `EPS011` reachability proof; the platform-name-absence result; the unchanged case, order, registry, and corpus proofs; focused and full suite output with the baseline failure-name comparison; the amendment record for the specification, the verification contract, and the requirement; the relationship to `WO-REB-021` and to `VREC-REB-017`; the hosted re-run result; and the complete actions-not-performed statement.

## Stop and escalate conditions

- The third route cannot be expressed without naming a platform, or cannot be withdrawn and supplied by a conformance test on both lanes.
- The repair would remove `EPS011` from the declared case list, leave it unreachable, or make it untested.
- The repair would lose any refusal present before it, or would accept a path form the rule refused.
- The two loaders cannot be held in agreement, or the declaration would need a conditional expressed as code.
- The hosted lane still fails after the repair, or fails for a second unrelated cause.
- Another file, lifecycle policy change, historical mutation, released-byte change, or external action is required.

Retain the exact failure and request a bounded amendment. Do not absorb another defect and do not create a bypass.

## Completion report format

Report the defect as measured on the hosted lane; the three routes and the narrowed condition; the capability decision table; the actual changed paths; the reproduction and repair results under the simulated pinned-lane profile; the `EPS011` reachability proof; the platform-name-absence result; the unchanged-declaration proofs; focused, full-suite, graph, distribution, portable-surface, and preflight results with the baseline comparison; the amendment record; the evidence path; the hosted re-run result; residual risks; actions not performed; and one next accountable decision.
