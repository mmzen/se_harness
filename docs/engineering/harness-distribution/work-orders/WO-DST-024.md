+++
id = "WO-DST-024"
type = "work_order"
title = "Stop installing evaluator scripts into governed repositories"
status = "approved"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters what the wheel ships, what the installer writes into every governed repository, and how the evaluator locates the programs that produce its verdicts; the next release, every consumer upgrade and this repository's own root adoption rely on its correctness."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "pyproject.toml",
  "se_harness/",
  "templates/repository/standard/scripts/",
  "tests/",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/harness-distribution/",
]

[relations]
implements = ["REQ-DST-070"]
specifications = ["SPEC-DST-025"]
verification = ["VER-DST-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T14:49:42Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 by selecting the presented option 'Approve all four, do not start (Recommended)', after the packet was drafted at the owner's instruction to remove the evaluator content duplicated under scripts/ in two packets. This decision approves the artifact only; implementation of WO-DST-024 is not started by it."
+++

# Work Order: Stop installing evaluator scripts into governed repositories

## Lifecycle

Drafted on 2026-09-06 after the repository owner decided that the evaluator
content duplicated under `scripts/` creates confusion and must be removed, and
chose to do it in two packets: this one moves the evaluator scripts out of the
repository template and into the package; a later one folds them into
importable modules (complexity audit item #225). Every approval below is the
owner's; nothing here is approved by implication.

## Objective

Make the installed package the only home of the evaluator scripts, so that a
governed repository holds what the tool wrote for it and nothing of the tool
itself, and so that the next `upgrade --apply` removes the eight retired paths
from every existing installation through the existing leaving-set rule.

## In scope

- Move `validate_engineering_artifacts.py`, `generate_harness_dashboard.py`,
  `inspect_engineering_artifacts.py`, `artifact_layout_registry.py` and
  `harness_explorer/index.template.html` from `templates/repository/standard/scripts/`
  to one directory inside the `se_harness` package, declared as package data
  (`SPEC-DST-025` DST-ENG-001 to DST-ENG-003).
- Delete `select_harness_work_order.py`, `check_engineering_harness.sh` and
  `check_engineering_harness.ps1` (DST-ENG-008, DST-ENG-009).
- Remove the two `scripts` entries from `[tool.setuptools.data-files]`.
- Point the script resolver and every caller of the validator or generator
  (`cli.py`, `preflight.py`, `provenance.py`, `release_qualification.py`,
  `renumber.py`, and any other) at the package directory; keep the subprocess
  invocation form (DST-ENG-004 to DST-ENG-007).
- Correct hard-coded managed or required path lists that name `scripts/`
  (DST-ENG-010).
- Rewrite the tests that pin the template `scripts/` paths, the root-equals-
  template parity for these files, the wheel's file list and `doctor`'s
  `scripts/` checks; add the cases `VER-DST-025` names, including the
  upgrade-from-0.15.0 fixture and the decoy-copy resolver case.
- Update the installation note ("Two things are installed", the upgrade
  section's removal list) and the developing note's description of where the
  validator lives (DST-ENG-017).
- Add the packet's chain to the harness-distribution domain index and retain
  evidence under `docs/engineering/harness-distribution/evidence/`.

## Out of scope

- Any byte of this repository's hash-locked root `scripts/` files or its lock;
  they leave at the root adoption of the carrying release (DST-ENG-014).
- AGENTS.md, `SPEC-IAR-012`, and the three repository-owned lanes that run
  root scripts from a checkout or snapshot; DST-ENG-015 and DST-ENG-016 bind
  the adoption work order.
- Changing the scripts' internal form, output, exit codes or diagnostic codes;
  folding them into modules; reading templates through `importlib.resources`.
- Any change to the installer's leaving-set rule, the lock schema, the
  managed CI workflow, or the skills under `.agents/`.
- Building, releasing, publishing or adopting anything.

## Authorized decision envelope

The implementation agent may choose the name of the engine directory inside the
package, the shape of the upgrade fixture, the test module layout, and the
wording of the two notes. It may not add a `scripts/` path back to the template
set, widen the execution scope, touch the root footprint or the lock, or leave
a hard-coded `scripts/` path in the evaluator.

## Constraints

- Read `ENGINEERING_HARNESS.md` and run the review preflight with the released
  0.15.0 evaluator from its venv outside the checkout before completion.
- The candidate suite must pass on the hosted Linux lane; the local Windows
  suite is a control whose skips and known teardown flake are labelled.
- The Explorer generator's determinism test and the bundle byte budget stay
  green after the move.
- Keep the diff free of unrelated changes; `tests/` is admitted as a prefix
  because the footprint is pinned across many modules, and the completion
  report lists every test file touched.

## Expected change surface

`pyproject.toml`; the new package directory and the deleted template
directory; five evaluator modules that resolve or list script paths; on the
order of twenty test modules; two notes; this domain's index and evidence.

## Required verification

`VER-DST-025` in full: the manifest, init, wheel-content, resolver, parity,
upgrade and customized-copy tests; the retirement grep; the inspections;
scenarios A to C run from a wheel installed outside the checkout, with
outputs retained.

## Evidence to record

`docs/engineering/harness-distribution/evidence/WO-DST-024-verification.md`:
scenario outputs, wheel listing, upgrade plan, hosted test report link, local
control reading, the list of test files changed, and the review preflight
result.

## Stop and escalate conditions

- A caller of the scripts outside the expected set, or a consumer-facing path
  that cannot be served from the package, is found.
- The Explorer bundle budget or determinism test fails after the move.
- Any change would be needed to the root footprint, the lock, AGENTS.md or a
  managed file.
- The scope check reports a path outside `[execution_scope]`.

## Completion report format

State the engine directory chosen; list deleted and added paths; list test
files changed; give the wheel listing delta; give scenario A to C outcomes;
give the hosted lane result and the local control reading, each labelled;
state that the root footprint and lock are byte-identical to `main`; name the
adoption obligations DST-ENG-015 and DST-ENG-016 carried forward to the next
root-adoption work order.
