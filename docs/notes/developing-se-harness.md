# Developing SE Harness

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This note applies to contributors developing `se_harness`. It grants no implementation, verification, release, publication, deployment, or repository-upgrade authority.

The one-time emergency bootstrap published version 0.5.0a1 and used that exact external release to convert this checkout from its retired self-hosted evaluator controls. Exact public 0.5.0 later governed the 0.6.0 release through the ordinary standard repository lifecycle. On 2026-08-23, the separately governed `WO-HUP-002` transaction adopted exact public 0.6.0 as the standard root evaluator. No self-hosting installation profile, evaluator descriptor, or special promotion command was introduced. Candidate source and packages remain evidence only and must not create formal artifacts, run root preflight, or manage lifecycle state.

The checkout and the locked root both report version 0.6.0, but they are different identities. The schema-3 lock binds the immutable public wheel and installed-payload digests; checkout source includes later development changes and remains candidate evidence. A matching version string does not grant verification, release, publication, deployment, or repository-upgrade authority.

## Development environment

SE Harness requires Python 3.11 or later and has no runtime dependencies outside the standard library. From a trusted source checkout, install candidate source into a dedicated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m se_harness --version
```

`python -m pip install .` performs a non-editable source install. Neither form is released proof; both are candidate development inputs.

## Repository structure

```text
se_harness/                              CLI and safe installation control plane
templates/repository/standard/           one canonical repository installation
scripts/                                 portable validation, Explorer, CI selection, release support
repository_tools/                        non-packaged distribution and publication policy
release/                                 canonical repository build recipe and hash-locked toolchain
tests/                                   installer, provenance, identity, package, and regression tests
docs/notes/                              non-authoritative human explanations
docs/engineering/                        self-governing formal artifact graph and evidence
.engineering-harness.toml                exact released root evaluator version and repository policy
.github/workflows/engineering-harness.yml exact released standard evaluator workflow
.github/workflows/candidate-evidence.yml  repository-owned source and package evidence
.github/workflows/predecessor-evaluator-assessment.yml transitional released-0.5 view evidence
.github/workflows/publish-pypi.yml        one-input release orchestrator
.github/workflows/release-candidate-replay.yml ready-RLS no-credential build replay
.github/workflows/publish-dashboard-pages.yml release-bound Explorer recovery
```

The root validator and Explorer sources remain managed by the selected released installation. Candidate templates may evolve without overwriting root managed files before the candidate is published.

## Ordinary development checks

Use the commands confirmed by the owner-controlled region of `AGENTS.md`:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python scripts/validate_release_distributions.py --root .
python -m unittest discover -s tests -p "test_*.py"
python -m se_harness --help
python -m se_harness doctor .
```

Run phase-appropriate work-order preflight and focused checks required by the governing verification contract. No formatter or linter is currently declared as a repository gate.

Generated dashboards, bytecode, environments, raw build output, normalized distributions, and disposable acceptance repositories are derived and must not become formal authority.

## Evaluator and candidate evidence

CI separates three identities without creating a second repository lifecycle:

| Plane | Origin | Purpose | Authority |
| --- | --- | --- | --- |
| Released evaluator | exact version recorded by the standard root installation, installed outside the checkout | root doctor, preflight, validation, and Explorer | evidence only; lifecycle authority remains human |
| Candidate source | reviewed checkout at `GITHUB_SHA` | full source regression and graph checks | evidence only |
| Candidate package | wheel built from an exact Git export and installed in a fresh environment | installed-origin, archive, init/adopt/upgrade, and package behavior | evidence only |

The standard managed workflow owns the released-evaluator lane. `.github/workflows/candidate-evidence.yml` owns candidate source and package jobs. Each job identifies its origin and proves it did not mutate the checkout. Passing candidate jobs cannot approve work, verify a VREC, release an RLS, publish, or update the root installation.

`harnessctl identity` supports `released-evaluator`, `candidate-source`, and `candidate-package` runtime diagnostics. Release workflows use the higher-level `harnessctl qualify` operations so the evaluator, target, fixed checks, and independence meaning are recorded together. Candidate source runs `complete-candidate` and remains explicitly candidate-controlled.

The independent package lane has one initial bootstrap exception. Exact public 0.6.0 predates the `qualify` namespace, so its fixed, digest-bound `accept-candidate` contract retains the original `se-harness-functional-acceptance-v1` result. It is not relabeled as a typed result. After a released verifier contains `qualify candidate-package`, the workflow moves to that operation and the 0.6.0-only path is removed through a later governed change. See [release qualification roles](release-qualification-roles.md).

Candidate CI also runs the contract-bound [evaluator migration rehearsal](evaluator-migration-rehearsal.md) on Windows and Linux. It acquires the already-public, digest-pinned predecessor before the run, builds a non-promotable successor from the exact candidate commit, installs both outside the checkout, and runs the nine-stage scenario twice. This gate tests the complete N-1-to-N handover; it does not make the candidate the root evaluator or grant release authority.

## Building and releasing

A promotable distribution build is allowed only under an approved release-bearing work order. For future releases, `release/build-recipe.json` is the complete machine-readable build identity: immutable Linux/amd64 image, exact CPython patch, full hash-locked toolchain, closed environment, argument-array commands, normalization, and outputs. `repository_tools/release_build.py` is the strict repository-only interpreter used by both the ready-RLS hosted replay and schema-2 production qualification. Workflow YAML orchestrates those calls but does not restate the schema-2 build. The owner-authored `docs/engineering/REPOSITORY_CONTEXT.md` defines the sequence; the portable harness neither seeds nor requires this repository policy.

Build success is evidence, not release authorization:

```text
clean candidate C -> exact recipe build A/B -> schema-2 bundle -> ready VREC -> human verification
                                                              -> generic ready RLS -> bind recipe + hashes
                                                                                   -> hosted exact replay
                                                                                   -> human release decision
                                                              -> one-input authorized publication
```

The tag selects C, not the later governance commit containing the released record. Recipe replay uses the already-bound expected hashes and has no update-expected mode. Historical released schema-1 records keep their labeled legacy rebuild; new ready records require recipe-bearing schema 2. Publication and Pages workflows validate their complete governance snapshots with current semantics and use an evidence-bound predecessor-compatible view when retained rejected history requires it. No `harnessctl` or recipe command commits, pushes, tags, creates a GitHub Release, publishes, deploys, or exercises accountable authority.

### Historical one-release predecessor bootstrap

Version 0.6.0 was the first candidate that required canonical evaluator evidence on a ready release record while this repository was governed by a schema-2 lock and released 0.5.0. The approved `se-harness-release-bootstrap-v1` contract bridged only that transition. Released 0.5.0 prepared and validated the RLS; candidate code merely recorded and rechecked an observation of that external evaluator.

If the complete graph contains one exact rejected predecessor-bootstrap RLS and its exact rejected declaring contract, released 0.5.0 cannot parse that newer terminal status. Under a separately approved successor contract, use the repository-owned adapter to rehearse an exact compatibility view:

```powershell
python scripts/prepare_predecessor_release.py `
  --repository . `
  --release-record RLS-... `
  --release-contract REL-... `
  --verification-record VREC-... `
  --work-order WO-... `
  --version 0.6.0 `
  --authorized-by release-owner `
  --tag v0.6.0 `
  --evaluator-python <external-env>/Scripts/python.exe `
  --evaluator-entry-point <external-env>/Scripts/harnessctl.exe `
  --evaluator-wheel <downloaded-public-wheel> `
  --json
```

Plan mode validates the complete graph with candidate source, derives the rejected pair from its closed relations, creates a temporary clone detached at the exact clean governance commit, and gives released 0.5.0 a sparse view omitting only those two paths. It verifies the generated ready RLS but leaves the source repository unchanged. The canonical `se-harness-predecessor-preparation-view-v1` evidence binds the source commit/tree, omitted paths/blob/raw hashes, sparse rules, external evaluator, exact predecessor command, candidate/VREC/work scope, and generated-output digest.

Adding `--apply` exclusively creates only the predecessor-generated RLS and its preparation-view sidecar, with source rechecks around each write and rollback on failure. It does not hide rejected history from candidate validation: the complete graph retains both rejected artifacts, and only `ready` or `released` RLS records claim a version. Multiple active records for one version still fail. This adapter is specific to the exact schema-2 predecessor-bootstrap boundary; it is not a general validation-error filter and it never approves, verifies, releases, commits, tags, publishes, deploys, changes the root, or uses credentials.

The same derived view supported a separate hosted predecessor assessment without pretending that released 0.5.0 understood the complete graph. During the 0.6.0 release, the unchanged managed workflow remained visibly failed at its exact full-checkout `E009`. The candidate-owned assessment required a clean exact commit and a valid complete-graph candidate report, proved the exact external wheel/runtime and old lock, accepted only that one legacy diagnostic, and then required released 0.5.0 `doctor`, `validate`, and dashboard generation to pass in the two-omission view:

```powershell
python scripts/assess_predecessor_evaluator.py `
  --repository . `
  --candidate-commit <exact-full-HEAD> `
  --release-contract REL-SEH-010 `
  --evaluator-python <external-env>/Scripts/python.exe `
  --evaluator-entry-point <external-env>/Scripts/harnessctl.exe `
  --evaluator-wheel <downloaded-public-wheel> `
  --output <external-runner-directory>/predecessor-assessment.json `
  --json
```

Plan mode performs the complete assessment but creates no evidence file. Adding `--apply` exclusively creates canonical `se-harness-predecessor-assessment-view-v1` JSON at the named external path. The JSON binds the complete candidate report, exact legacy refusal, both omitted Git/raw identities, sparse rules, isolated evaluator payload, fixed view commands, graph counts, and dashboard tree. The dashboard digest retains every generated file while normalizing only the released generator's factual run-time `generated_at` and `elapsed_ms` fields; all semantic bundle bytes remain hash-bound. The adapter rejects publication credential signals, arbitrary omissions or expected-error input, linked or in-checkout output, collision, diagnostic drift, candidate drift, and any source mutation. It has no lifecycle, commit, push, tag, publication, deployment, maintenance, policy, or root-upgrade effect.

The publication gate uses a separate read-only adapter after the RLS is released. Operators normally do not invoke it manually; the initial release resolver, release-bound Pages build, and standalone Pages recovery all call the same command. A local evidence replay uses:

```powershell
python scripts/validate_predecessor_publication_view.py `
  --repository <clean-governance-checkout> `
  --release-record RLS-SEH-012 `
  --evaluator-python <external-env>/Scripts/python.exe `
  --evaluator-entry-point <external-env>/Scripts/harnessctl.exe `
  --evaluator-wheel <downloaded-public-wheel> `
  --output <external-runner-directory>/predecessor-publication-view.json `
  --json
```

The adapter requires a clean committed checkout, a released RLS, canonical preparation/evaluator sidecars, unchanged rejected-history blobs, and the exact external wheel/runtime. It validates the complete graph before and after, derives the two omissions without caller input, requires released `doctor` and JSON `validate` to pass in a detached temporary view at governance `HEAD`, proves cleanup and zero source change, and emits canonical `se-harness-predecessor-publication-view-v1` JSON only at the named external path. Passing is a technical prerequisite, not publication authority; the adapter has no credentials, network, lifecycle, Git-ref, maintenance, publication, deployment, policy, or root-upgrade effect.

On POSIX, supply the virtual environment's lexical `bin/python` path rather than its resolved system-interpreter target. The adapter permits only that terminal interpreter link, derives evaluator identity from the virtual-environment root, and continues to reject linked parent directories, entry points, wheels, and source-checkout paths. A standard Windows `Scripts/python.exe` remains an ordinary-file path under the same contract.

After a separately authorized predecessor `prepare-release` has created the exact contract-named ready RLS, the repository-only binder can first produce a read-only plan:

```powershell
python scripts/bind_release_bootstrap.py `
  --repository . `
  --release-record docs/engineering/<domain>/releases/RLS-...md `
  --release-contract docs/engineering/<domain>/release/REL-...md `
  --evaluator-python <external-env>/Scripts/python.exe `
  --evaluator-entry-point <external-env>/Scripts/harnessctl.exe `
  --evaluator-wheel <downloaded-public-wheel> `
  --json
```

Adding `--apply` is a separate explicit mutation. It exclusively creates one canonical evaluator-evidence sidecar and atomically adds only `preparation_schema`, `evaluator_evidence_path`, and `evaluator_evidence_sha256` to the ready RLS. The command rejects any contract, lock, wheel, runtime-origin, candidate, verification, work-set, path, or existing-byte mismatch. Candidate validation then replays the complete graph, including the retained rejected pair and both sidecars. It never creates or transitions an RLS, changes the root, commits, pushes, tags, publishes, deploys, or uses credentials.

The versioned Git rule `docs/engineering/**/evidence/*.json text eol=lf` preserves the canonical sidecar bytes and bound raw SHA-256 under supported Windows and non-Windows checkout configurations. Validators do not normalize evidence before hashing; changed, noncanonical, or CRLF worktree bytes still fail.

Ordinary ready RLS records now use the complete schema-3 evaluator identity in the current lock. The predecessor-bootstrap rules above remain a historical description of the 0.6.0 release and retained terminal records; they are not needed for ordinary complete-graph evaluation by the 0.6.0 root. A rejected contract cannot bind, prepare, release, publish, or authorize credentials, and only `ready` or `released` records are active version claims. Adopting public 0.6.0 remained separate from publication and was later performed through `WO-HUP-002`.

## Advancing the root evaluator

Candidate success never changes the root evaluator. The current root is exact public 0.6.0 under a schema-3 identity lock. After a later SE Harness version is immutably published, maintainers select it under a separate approved repository-upgrade work order, install that exact release outside the checkout, review ordinary `harnessctl upgrade`, and authorize `--apply` only when the plan is safe. The standard upgrade transaction preserves repository-owned content and fails closed on customization or integrity ambiguity.

See the current [standard repository lifecycle guide](../engineering/self-hosting-boundary/SELF_HOSTING.md), the owner-controlled region of [`AGENTS.md`](../../AGENTS.md), and managed [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md).
