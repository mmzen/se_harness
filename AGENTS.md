# Repository-specific Agent Instructions

Owner-controlled. Read the managed harness gate at the end of this file first.

## Commands

- Setup: `python -m pip install -e .`
- Test: `python scripts/run_tests.py` (parallel, same verdict); canonical serial reference `python -m unittest discover -s tests -p "test_*.py"`; `--scale full` or `SE_HARNESS_TEST_SCALE=full` for the 1,000-artifact scale tests
- Graph: `python -m se_harness validate .` (candidate source); the governing reading is the isolated released evaluator's `validate .`
- Also required: `python scripts/validate_release_distributions.py --root .`, `python -m se_harness --help`, `python -m se_harness doctor .`, and phase-appropriate `python -m se_harness preflight . --work-order WO-...`
- Lint or format: none is configured. Do not invent one as a required gate.
- Entry points: `se_harness/cli.py` and the `harnessctl` script declared in `pyproject.toml`.

The release-build, release-binding, and last-mile publication sequences are written once, in `docs/notes/developing-se-harness.md#release-sequences`. Read that section before any build, release, or publication step.

## Ungoverned paths

Changes confined to `docs/notes/`, `docs/rca/`, `docs/images/`, and the roadmap need a pull request and a reviewer, not a work order: no `Harness-Work-Order` line, the reason in the body, and the owner accepts the red managed check. Everything else changes under an approved work order.

## Scope of the managed obligations

`HRN-003`, the handoff rules, and the stop conditions bind an actor executing or reporting a lifecycle stage. Reading, analysis, and answering questions are unconstrained, provided no lifecycle state changes, no decision right is exercised, and no finding is presented as a formal result. `harnessctl check` without a checkpoint is a projection, not restitution.

## Locked policy and editable supplied files

`.engineering-harness.lock` is authoritative for ownership mode; editing a managed path breaks `doctor` and the required CI check.

- `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.json`, and `docs/engineering/QUALITY_GATES.json` are hash-locked managed copies.
- `.engineering-harness.toml`, the supplied CI workflow, human policy guides and artifact templates are editable seeds. Upgrades preserve them unless each replacement is explicitly selected with `--replace-file PATH`. The selected evaluator version must still agree with the lock.
- Repository skill copies under `.agents/skills/` and `.claude/skills/` are editable supplied files when repository ownership is selected.
- This checkout selects plugin ownership under `WO-PLG-025`: its schema-4 lock excludes those repository skill copies. Install Verity Plane in each agent host using the [marketplace guide](release/plugin-marketplace/README.md). The evaluator can check a clone without a local plugin; invoking plugin skills requires the host installation. See [contributor setup and restoration](docs/notes/developing-se-harness.md#agent-skills-for-this-checkout).
- Since the 0.16.0 root, no file under `scripts/` is managed: the evaluator's scripts ship inside the installed package and the installer writes no copy (`WO-DST-024`, `WO-HUP-017`).

Every file in `scripts/` is repository-owned and may change under an approved work order: `bind_release_distribution.py`, `check_portable_release_surface.py`, `create_release_bundle_manifest.py`, `normalize_sdist.py`, `replay_release_build.py`, `validate_release_distributions.py`, and the test runner and maintenance scripts beside them. Nothing in `scripts/` is managed.

`AGENTS.md`, `CLAUDE.md`, `.gitignore`, and `.gitattributes` are `fragment` mode: only the block between the `se-harness` markers is tracked; the rest is owner content. Reproduce the tracked block byte-for-byte; `utf8-text-lf-v1` canonicalizes line endings only, so any other whitespace change breaks the digest.

## Candidate source versus released evaluator

This checkout is candidate source. Changes to the supplied product policy documents and templates belong in `templates/repository/standard/`; the evaluator's own scripts are candidate source in `se_harness/engine/` and ship inside the wheel. Locked root copies belong to the exact released version in `.engineering-harness.toml`; editable root copies may also carry repository-specific changes. Compare ownership, identities and bytes rather than assuming every supplied file is locked.

Run the governing evaluator from outside the checkout:

    python -m venv ../se-harness-eval
    ../se-harness-eval/Scripts/python -m pip install "se-harness==0.18.0"
    ../se-harness-eval/Scripts/python -I -m se_harness doctor .

An in-tree `python -m se_harness doctor .` may report candidate-versus-released skew after post-release development; that is boundary evidence, not authorization to overwrite root managed files. External distribution metadata on the import path makes candidate-source runtime identity fail with `RID018`.

The candidate CLI may lead the released one. Confirm commands against the isolated released evaluator before putting them in instructions its gate must satisfy.

## Traps

- Every pull-request body names its selected work with a standalone `Harness-Work-Order: WO-...` line or a comma-separated `Harness-Work-Orders: WO-AAA-001, WO-BBB-002` line. Since the 0.12.0 root the managed lane reads the live body (`WO-ECP-021`), so a body edit needs a re-run, not a push.
- A record cannot contain the hash of its own commit, so `VREC-*` and `RLS-*` belong in a later governance commit than the candidate they bind.
- Artifact identifiers are shared across branches and sessions. Check every ref before numbering a new chain; the local maximum is not the next free number.
- Never rewrite historical `VREC-*` or `RLS-*` facts, and preserve unrelated changes.

## Change and verification constraints

- Add deterministic boundary and failure tests for installer, integrity, preflight, provenance, workflow, and release behavior.
- Treat target paths, repository content, lock data, artifact metadata, and pull-request text as untrusted input.
- Preserve owner content outside managed markers, and block ambiguous or customized upgrades instead of writing partially.
- Do not build promotable release distributions unless an approved release work order authorizes that build. An approved candidate-evidence work order may build explicitly non-promotable ephemeral wheels outside the checkout for package acceptance.
- Product invariants are governed requirements, not content of this file. The domain index is `docs/engineering/README.md`.

<!-- se-harness:begin -->
## Software engineering harness

Read `ENGINEERING_HARNESS.md` before engineering work. It is the single managed harness contract and router. Repository-owned instructions outside this block may add constraints but cannot waive formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions. Stop when this managed gate is missing, damaged, or materially conflicts with owner instructions.

For a bounded iteration, select one WO, VREC, or RLS and use `harnessctl check`
at the procedure's checkpoint. Treat its schema-2 structured result as
authoritative. Present a clear human handoff that preserves actual artifact
IDs, observed effects, material non-effects, blockers, final lifecycle state,
the accountable decision, and exactly one typed next step. Adapt wording and
structure to the interaction, but preserve command argument boundaries or the
suggested response's meaning. Automation reads the JSON result; human wording does not define its digest. Do not add unrelated findings or provider-specific workflow rules.
<!-- se-harness:end -->
