# Repository Context for se_harness

> Repository-owned after installation. This context helps engineering agents operate the repository, but it is not approved product intent, a requirement, architecture approval, or release authority.

## Purpose

- Repository purpose: distribute one reusable, repository-native software-engineering harness with formal traceability, local validation, Harness Explorer, and safe lifecycle commands.
- Primary users or operators: repository owners, engineers, coding agents, assurance owners, release owners, and service owners adopting or maintaining the harness.
- Accountable repository owners: the `product-owner` and `engineering-owner` roles named by the applicable formal artifacts.

## Commands

- Setup: `python -m pip install -e .`
- Build: under an approved release work order, run `python -m build --wheel --sdist --no-isolation --outdir <raw-output> .`, then create the final sdist with `python scripts/normalize_sdist.py <raw-sdist> <release-sdist> --epoch <candidate-commit-unix-timestamp>`.
- Test: `python -m unittest discover -s tests -p "test_*.py"`
- Lint or format: no formatter or linter command is currently defined; do not invent one as a required gate.
- Additional required verification: `python scripts/validate_engineering_artifacts.py --root .`, `python -m se_harness --help`, `python -m se_harness doctor .`, and phase-appropriate `python -m se_harness preflight . --work-order WO-...`

## Architecture

- Entry points: `se_harness/cli.py` and the `harnessctl` script declared in `pyproject.toml`.
- Major components and responsibilities: `se_harness/` is the safe control plane, including runtime identity and read-only preflight; `templates/repository/standard/` is the one canonical consumer installation; `.self-hosting/governor.toml` selects the exact released governor for this implementation repository; `.github/workflows/engineering-harness.yml` separates governor, candidate-source, and candidate-package gates; `scripts/` validates, selects structured CI work orders, renders the local Explorer, and contains repository release-build support; `tests/` verifies installer, upgrade, diagnostics, instruction routing, preflight, CI, provenance, and deterministic distribution behavior; `docs/engineering/` contains the governing artifact graph.
- External services or dependencies: Python 3.11 or later is the only runtime dependency. Runtime behavior uses the standard library and installed repositories do not require an external service. Package building uses the separately provisioned build environment declared by `pyproject.toml`.

## Repository constraints

- Generated paths: `target/harness-dashboard/`, Python bytecode, build metadata, raw and normalized distribution artifacts, self-hosting virtual environments, disposable acceptance repositories, and temporary files are derived and must not become formal authority.
- Restricted or sensitive paths: preserve `.git/`, `.engineering-harness.lock`, managed `se-harness` marker blocks, and repository-owned content outside those blocks.
- Files requiring specialized review: changes to installer ownership modes, safe path handling, lock behavior, canonical templates, runtime identity, the governor descriptor, self-hosting CI, artifact validation, provenance rules, or release archive normalization require deterministic boundary and failure tests.
- Local conventions not captured elsewhere: maintain exactly one consumer installation; keep the released governor isolated from candidate source and candidate packages; treat target content as untrusted; preserve customizations; never infer product authority; and do not commit, tag, push, publish, verify, or release without separately authorized work and accountable human action.

## Git workflow context

This repository integrates reviewed work through branches and pull requests, but it does not currently declare one mandatory branch-prefix or release-branch scheme in this owner context. Every pull request subject to the installed workflow declares exactly one standalone `Harness-Work-Order: WO-...` field; branch naming does not substitute for that declaration or for approved scope.

The non-authoritative [`docs/notes/harness-branching-model.md`](../notes/harness-branching-model.md) presents one illustrative trunk-based model through a compact lifecycle example and a detailed example with short-lived work branches, later governance commits, and supported `release/x.y` maintenance lines. It is a teaching aid, not repository policy or a universal SE Harness rule. Hosting controls such as branch protection, required checks, and merge permissions remain owner-managed external configuration.

## Maintenance

Review this file when commands, boundaries, ownership, or repository structure change. Put product decisions and approvals in the formal artifact chain under `docs/engineering/`, not in this context file.
