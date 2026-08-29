# Repository-specific Agent Instructions

Owner-controlled. Read the managed harness gate at the end of this file first.

## Commands

- Setup: `python -m pip install -e .`
- Test: `python scripts/run_tests.py` (parallel, same verdict); canonical serial reference `python -m unittest discover -s tests -p "test_*.py"`; `--scale full` or `SE_HARNESS_TEST_SCALE=full` for the 1,000-artifact scale tests
- Graph: `python scripts/validate_engineering_artifacts.py --root .`
- Also required: `python scripts/validate_release_distributions.py --root .`, `python -m se_harness --help`, `python -m se_harness doctor .`, and phase-appropriate `python -m se_harness preflight . --work-order WO-...`
- Lint or format: none is configured. Do not invent one as a required gate.
- Entry points: `se_harness/cli.py` and the `harnessctl` script declared in `pyproject.toml`.

The release-build, release-binding, and last-mile publication sequences are written once, in `docs/notes/developing-se-harness.md#release-sequences`. Read that section before any build, release, or publication step.

## Ungoverned paths

Changes confined to `docs/notes/`, `docs/rca/`, `docs/images/`, and the roadmap need a pull request and a reviewer, not a work order: no `Harness-Work-Order` line, the reason in the body, and the owner accepts the red managed check. Everything else changes under an approved work order.

## Scope of the managed obligations

`HRN-003`, the handoff rules, and the stop conditions bind an actor executing or reporting a lifecycle stage. Reading, analysis, and answering questions are unconstrained, provided no lifecycle state changes, no decision right is exercised, and no finding is presented as a formal result. `harnessctl focus` output without `--result-schema 2` is a compatibility projection, not restitution.

## Do not edit these - they are hash-locked managed copies

`.engineering-harness.lock` is authoritative for ownership mode; editing a managed path breaks `doctor` and the required CI check.

- `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, `.github/workflows/engineering-harness.yml`
- `docs/engineering/WORKFLOW.md`, `WORKFLOW.json`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `QUALITY_GATES.json`, `TRACEABILITY.md`, `ARTIFACT_AUTHORING.md`, `OPERATING_CARD.md`, `TECHNICAL_COMMUNICATION.md`
- every file in `docs/engineering/templates/`
- every file under `.agents/skills/` (`SKILL.md`, `skill-contract.json`, `openai.yaml`, `guard.py`, `check_scope.py`, `check_brief.py`, `orient.py`, `check_prepare.py`) and `.claude/skills/*/SKILL.md`
- exactly these eight in `scripts/`: `validate_engineering_artifacts.py`, `generate_harness_dashboard.py`, `inspect_engineering_artifacts.py`, `select_harness_work_order.py`, `artifact_layout_registry.py`, `check_engineering_harness.sh`, `check_engineering_harness.ps1`, `harness_explorer/index.template.html`

The remaining files in `scripts/` are repository-owned and may change under an approved work order: `bind_release_distribution.py`, `check_portable_release_surface.py`, `create_release_bundle_manifest.py`, `normalize_sdist.py`, `replay_release_build.py`, `validate_release_distributions.py`. Not all of `scripts/` is managed.

`AGENTS.md`, `CLAUDE.md`, and `.gitignore` are `fragment` mode: only the block between the `se-harness` markers is tracked; the rest is owner content. Reproduce the tracked block byte-for-byte; `utf8-text-lf-v1` canonicalizes line endings only, so any other whitespace change breaks the digest.

## Candidate source versus released evaluator

This checkout is candidate source. Changes to the eight managed scripts and the managed policy documents belong in `templates/repository/standard/`. The root copies belong to the exact released version in `.engineering-harness.toml`; they may match unchanged candidate templates or lag later development, so compare identities and bytes rather than assuming.

Run the governing evaluator from outside the checkout:

    python -m venv ../se-harness-eval
    ../se-harness-eval/Scripts/python -m pip install "se-harness==0.10.0"
    ../se-harness-eval/Scripts/python -I -m se_harness doctor .

An in-tree `python -m se_harness doctor .` may report candidate-versus-released skew after post-release development; that is boundary evidence, not authorization to overwrite root managed files. External distribution metadata on the import path makes candidate-source runtime identity fail with `RID018`.

The candidate CLI may lead the released one. Confirm commands against the isolated released evaluator before putting them in instructions its gate must satisfy.

## Traps

- Every pull-request body needs a standalone `Harness-Work-Order: WO-...` line. CI reads it from the stored event payload, so a later body edit leaves the check red until the next push.
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
suggested response's meaning. Exact-format consumers must use the direct
renderer. Do not add unrelated findings or provider-specific workflow rules.
<!-- se-harness:end -->
