# Repository-specific Agent Instructions

Owner-controlled. Read the managed harness gate at the end of this file first.

## Commands

- Setup: `python -m pip install -e .`
- Test: `python -m unittest discover -s tests -p "test_*.py"`
- Graph: `python scripts/validate_engineering_artifacts.py --root .`
- Also required: `python scripts/validate_release_distributions.py --root .`, `python -m se_harness --help`, `python -m se_harness doctor .`, and phase-appropriate `python -m se_harness preflight . --work-order WO-...`
- Lint or format: none is configured. Do not invent one as a required gate.
- Entry points: `se_harness/cli.py` and the `harnessctl` script declared in `pyproject.toml`.

`docs/engineering/REPOSITORY_CONTEXT.md` is repository-owned content carrying the same commands plus the release-build, release-binding, and publication sequences. Read it before any build, release, or publication step. Those sequences are not duplicated here.

## Do not edit these - they are hash-locked managed copies

`.engineering-harness.lock` is authoritative for ownership mode. Editing a managed path breaks `doctor` and the required CI check.

- `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, `.github/workflows/engineering-harness.yml`
- `docs/engineering/WORKFLOW.md`, `WORKFLOW.json`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `QUALITY_GATES.json`, `TRACEABILITY.md`
- every file in `docs/engineering/templates/`
- exactly these eight in `scripts/`: `validate_engineering_artifacts.py`, `generate_harness_dashboard.py`, `inspect_engineering_artifacts.py`, `select_harness_work_order.py`, `artifact_layout_registry.py`, `check_engineering_harness.sh`, `check_engineering_harness.ps1`, `harness_explorer/index.template.html`

The remaining files in `scripts/` are repository-owned and may change under an approved work order: `bind_release_distribution.py`, `check_portable_release_surface.py`, `create_release_bundle_manifest.py`, `normalize_sdist.py`, `validate_release_distributions.py`. Do not claim all of `scripts/` is managed; that would block the documented release-build path.

`AGENTS.md`, `CLAUDE.md`, and `.gitignore` are `fragment` mode: only the block between the `se-harness` begin and end markers is tracked. The rest of each file is owner content. Reproduce the tracked block byte-for-byte; `utf8-text-lf-v1` canonicalizes line endings only, so any other whitespace change breaks the digest.

## Candidate source versus released evaluator

This checkout is candidate source. Changes to the eight managed scripts and the managed policy documents belong in `templates/repository/standard/`. The root copies belong to the exact released version recorded in `.engineering-harness.toml`. They may match unchanged candidate templates and may lag later development; compare evaluator identities and bytes rather than assuming equality or difference.

Run the governing evaluator from outside the checkout:

    python -m venv ../se-harness-eval
    ../se-harness-eval/Scripts/python -m pip install "se-harness==0.6.0"
    ../se-harness-eval/Scripts/python -I -m se_harness doctor .

An in-tree `python -m se_harness doctor .` may report candidate-versus-released skew after post-release development. That is boundary evidence, not authorization to overwrite root managed files. External distribution metadata on the import path also makes candidate-source runtime identity fail with `RID018`.

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
at the procedure's checkpoint. Return the command's canonical human restitution
block verbatim. Do not append repository-wide inspection findings, analysis, a
second next step, or provider-specific workflow rules.
<!-- se-harness:end -->
