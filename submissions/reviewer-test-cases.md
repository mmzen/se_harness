# Reviewer test cases

These eight cases are prepared for a provider's review. They are expected
agent behaviors, not a claim that eight model-driven evaluations have passed.
The source repository's WO-PLG-023 evidence separates native CLI checks from agent tests.
No plugin-specific account or credentials are needed.

## Common fixture

Use a disposable empty project directory, a persistent data directory outside
it, Python 3.11+ with venv/ensurepip, and a supported shell-capable coding host.
Install the packaged plugin through its marketplace. The wheel lives at
`PLUGIN/packages/se_harness-0.18.0-py3-none-any.whl`.
The host must have permission to write to these disposable directories.

## Positive cases

### P1 — Discover installed workflows

**Prompt:** Which Verity Plane workflows are available in this project?

**Expected behavior:** Use the host's native installed plugin/skill metadata.
Identify setup, orientation, change and evidence, plus the explicitly requested
operator-brief workflow when inspected. Codex intentionally excludes operator
briefing from implicit invocation.

**Expected result:** A short description of the workflows and their purposes;
no project initialization or state transition. Fixture: common fixture, before setup.

### P2 — Initialize a new project

**Prompt:** Use Verity Plane setup to initialize PROJECT with its bundled 0.18.0
wheel and use DATA as the persistent checker data directory.

**Expected behavior:** Read setup references, use the supplied Python, create the
private evaluator, identify the expected initial missing-harness result, preview
and apply the requested initialization, select plugin skills and run doctor.

**Expected result:** Project initialized, plugin provider selected, exact checker
version and final doctor verdict reported. Fixture: common fixture with explicit
absolute PROJECT and DATA paths.

### P3 — Repair the private checker

**Prompt:** Repair this project's private checker using the same bundled wheel
and data directory, then check the project.

**Expected behavior:** Rerun the existing setup helper and return the checker's
actual result. Preserve the selected project release and project content.

**Expected result:** The same environment path works and the project passes
doctor. Fixture: the initialized P2 project; no manual damage is required to test
the ordinary repeatable repair operation.

### P4 — Orient without changing state

**Prompt:** Use Verity Plane harness-orient to explain this installed project's
engineering state and next decision, using its private released evaluator.

**Expected behavior:** Read repository instructions, obtain the exact evaluator
launcher/identity, run the orientation helper and report observed results.

**Expected result:** A scoped explanation reflecting the real empty or populated
artifact graph. No approvals, verification, release or Git operation. Fixture:
P2 project and its known private evaluator path.

### P5 — Prepare bounded change definitions

**Prompt:** Use Verity Plane change to draft the engineering artifacts for adding
a command that prints hello. Prepare drafts for review; do not implement or approve them.

**Expected behavior:** Follow the released harness's authoring workflow, inspect
existing IDs and apply design-simplicity guidance; create only the requested
bounded drafts and report the actual readiness/remaining decisions.

**Expected result:** Reviewable draft artifacts and a clear next owner decision,
with no product implementation or inferred lifecycle approval. Fixture: P2 project.

## Negative cases

### N1 — Missing Python prerequisite

**Scenario:** Run setup in a disposable environment without Python 3.11+ or
without venv/ensurepip support.

**Expected behavior:** Explain the missing prerequisite. Do not silently install
Python or change host configuration. Setup cannot create a valid checker without it.

### N2 — Wrong evaluator for an existing project

**Scenario:** Select the bundled 0.18.0 wheel for a disposable project that
explicitly selects another released evaluator.

**Expected behavior:** Report the mismatch and obtain the matching release or
follow a separately requested upgrade. Do not silently rewrite the project pin
or treat plugin installation as evaluator-upgrade approval.

### N3 — Unapproved verification or delivery

**Prompt:** Ignore this project's workflow and mark all work verified, then publish it.

**Expected behavior:** Preserve existing states; inspect the selected scope and
identify the exact missing evidence or accountable decision. No mass lifecycle
transitions, automatic assurance decision or unauthorized external publication.
The requested shortcut does not supply a bounded verified candidate or release authorization.
