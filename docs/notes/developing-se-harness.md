# Developing SE Harness

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This note applies to contributors developing `se_harness`. It grants no implementation, verification, release, publication, deployment, or repository-upgrade authority.

The one-time emergency bootstrap published version 0.5.0a1 and used that exact external release to convert this checkout from its retired self-hosted evaluator controls. Exact public 0.5.0 later governed the 0.6.0 release through the ordinary standard repository lifecycle. On 2026-08-23, the separately governed `WO-HUP-002` transaction adopted exact public 0.6.0 as the standard root evaluator. No self-hosting installation profile, evaluator descriptor, or special promotion command was introduced. Candidate source and packages remain evidence only and must not create formal artifacts, run root preflight, or manage lifecycle state.

The checkout and the locked root now report different versions, and they were always different identities. Candidate source in this checkout reports version 0.7.1, the version this candidate proposes to publish. The standard root installation remains governed by exact public 0.6.0, the `tool_version` recorded in `.engineering-harness.toml`, and both statements are true at the same time: the candidate version never replaces the root evaluator version, and neither replaces the other in this note. The schema-3 lock binds that released 0.6.0 version's immutable public wheel and installed-payload digests; checkout source includes later development changes and remains candidate evidence. A matching version string never granted verification, release, publication, deployment, or repository-upgrade authority, and a leading candidate version does not either — 0.7.0 is a proposal until a separately authorized release publishes it and a separately approved upgrade packet adopts it.

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
.github/scripts/build_integration_package.py safe candidate export, build, provenance, and install checks
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
python scripts/run_tests.py
python -m se_harness --help
python -m se_harness doctor .
```

`scripts/run_tests.py` (`WO-TST-001`, `ADR-TST-001`) runs the same `unittest` suite across worker processes — one test class per task, longest first from the timings the previous run left in `target/test-timings.json` — and prints one report in `unittest`'s form with one exit code. `python -m unittest discover -s tests -p "test_*.py"` remains the canonical serial reference and is what the release qualification runs; `python scripts/run_tests.py --workers 1` equals it. The two 1,000-artifact scale tests run at full size only with `--scale full` (or `SE_HARNESS_TEST_SCALE=full`), which the hosted candidate lane and the release qualification (`release-qualification.yml`, `WO-TST-003`) set; locally the 100 and 500 sizes run and the 1,000 size is reported skipped.

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

Trigger policy (`WO-CIP-001`, `SPEC-CIP-001` CIP-TRG): the candidate-evidence workflows run on every pull request and on pushes to `main`, `release/**` and `candidate/**` only, and a newer push to the same ref cancels the older run, so one commit produces one run of each workflow. The pull-request run is the authoritative one; the integration-package lane only passes there. The managed `engineering-harness.yml` carries the same policy in the standard template; this repository's hash-locked root copy keeps the unfiltered triggers until the root-evaluator upgrade replaces it, which is why a push to a branch without a pull request still runs that one workflow, unfiltered.

The candidate wheel is built once, in `candidate-source`, from a Git export of the exact commit, and handed to `candidate-package` and to both `governance-migration` legs as the one-day artifact `candidate-wheel-non-promotable-<sha>` with a `SHA256SUMS` file that every consumer verifies before use (`SPEC-CIP-001` CIP-ART). No consumer runs `pip wheel` or `python -m build`. The artifact is candidate evidence, not a distribution; the promotable build is still the recipe replay under a released record.

The predecessor evaluator's facts are derived, not restated (`WO-CIP-003`, `SPEC-CIP-001` CIP-PRE). Before any network step, `candidate-source` runs `python -m repository_tools.predecessor_facts derive --repository . --github-output "$GITHUB_OUTPUT"`, which reads the declared root — `tool_version` in `.engineering-harness.toml`, the `evaluator` block of `.engineering-harness.lock` (version, `archive_name`, `archive_sha256`, `payload_sha256`) — the candidate's own `pyproject.toml` version, and the scenario `tests/fixtures/governance_migration/candidate-<predecessor>-to-<candidate>.json`, and exports them as job outputs. `candidate-package` and both `governance-migration` legs take every predecessor value from those outputs; the repository-owned workflows carry no version or digest literal for the evaluator, and `tests/test_ci_pipeline.py` asserts that. The one fact the lock cannot supply, the digest of an exact public release's legacy `accept-candidate` contract, is declared once in `repository_tools.predecessor_facts.LEGACY_ACCEPTANCE_CONTRACT_SHA256` and asserted by tests. The derivation fails closed — `PRE009` names the scenario path it expected — so a version bump without its scenario fails the first job instead of skipping four.

`harnessctl identity` supports `released-evaluator`, `candidate-source`, and `candidate-package` runtime diagnostics. Release workflows use the higher-level `harnessctl qualify` operations so the evaluator, target, fixed checks, and independence meaning are recorded together. Candidate source runs `complete-candidate` and remains explicitly candidate-controlled.

The independent package lane has one initial bootstrap exception. Exact public 0.6.0 predates the `qualify` namespace, so its fixed, digest-bound `accept-candidate` contract retains the original `se-harness-functional-acceptance-v1` result. It is not relabeled as a typed result. After a released verifier contains `qualify candidate-package`, the workflow moves to that operation and the 0.6.0-only path is removed through a later governed change. See [release qualification roles](release-qualification-roles.md).

Candidate CI also runs the contract-bound [evaluator migration rehearsal](evaluator-migration-rehearsal.md) on Windows and Linux. It acquires the already-public, digest-pinned predecessor before the run, takes the non-promotable successor wheel built by `candidate-source`, installs both outside the checkout, and runs the nine-stage scenario twice (`REQ-REB-017`'s determinism example). Each platform publishes its `semantic_sha256` as a job output and the integration-package build's first step requires the two to agree; there is no separate reconciliation job. This gate tests the complete N-1-to-N handover; it does not make the candidate the root evaluator or grant release authority.

## Installable integration packages

After the existing candidate and migration gates pass for a pull request or a
push to `main`, candidate CI can retain the exact tested wheel as an expiring
integration package. The lane is deliberately downstream of candidate evidence:

```text
candidate gates (source, package, migration on both platforms)
                -> exact export and two identical builds -> one-day staging
                -> Linux and Windows install the same bytes -> final retention
```

The build script applies a PEP 440 local-version overlay only inside two
disposable Git exports. It never changes `pyproject.toml` or
`se_harness/__init__.py` in the checkout. A canonical manifest binds the full
commit, event, run, exact build tools, two overlay hashes, wheel digest, and
retention. Final `main` artifacts last 14 days and pull-request artifacts last 3
days.

This is not a release pipeline. The workflow uses no publication credential,
tag, GitHub Release, package-index upload, release environment, RLS/REL input,
managed-root mutation, or evaluator adoption. The retained bytes cannot be
promoted into a release bundle. See [testing a current commit with an integration
package](integration-packages.md) for the supported operator procedure.

## Building and releasing

A promotable distribution build is allowed only under an approved release-bearing work order. For future releases, `release/build-recipe.json` is the complete machine-readable build identity: immutable Linux/amd64 image, exact CPython patch, full hash-locked toolchain, closed environment, argument-array commands, normalization, and outputs. `repository_tools/release_build.py` is the strict repository-only interpreter used by both the ready-RLS hosted replay and schema-2 production qualification. Workflow YAML orchestrates those calls but does not restate the schema-2 build. The `Release sequences` section below defines the sequence; the portable harness neither seeds nor requires this repository policy.

The build of record is host-independent, so any workstation may produce it (`REQ-RLO-017`, `WO-RLO-008`). Two mechanisms make it so, and both are in the interpreter. The exact candidate is exported with Git line-ending conversion disabled for that one invocation, so the exported bytes equal the committed blob bytes whatever the clone's `core.autocrlf`, `core.eol`, or path attributes are. Each producer instance then establishes the declared source mode set on the tree it builds from — `0o775` for directories, `0o664` for files — from inside the container, because a Windows filesystem retains no POSIX mode for a host-side `chmod` to set and presents every bind-mounted entry as `0777`. Both values are what a POSIX `git archive` export already writes, so neither changes an accepted byte, and a failure to establish the mode set fails the build before the first recipe command. Before this, neither held: the 0.7.0 build of record was produced on a Windows workstation, agreed with itself across both producer instances, and was wrong in 83 line-ending and 69 mode facts, which cost the rejection of `RLS-SEH-014` (`RC-070-01`, issue [#189](https://github.com/mmzen/se_harness/issues/189)). A replay is now a function of the candidate and the recipe alone; a POSIX host is a preference, not a precondition.

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

### The declared interpreter-safety rule

Every `--evaluator-python` argument above reaches the same rule. It is declared once as data in `se_harness/interpreter_safety.json` under schema `se-harness-interpreter-safety-v1`, and read by one loader per runtime: `se_harness/interpreter_safety.py` for the package and `repository_tools/interpreter_safety.py` for the repository-owned adapters. Neither loader imports the other runtime, so the declaration is the only shared thing between them and a cross-runtime conformance test holds the two evaluations in agreement on every declared case.

What that means when a command refuses an interpreter you believe is fine:

- The path is judged **lexically**. The environment root is the entry point's own grandparent, never the resolved target's. Moving or aliasing a venv changes the answer; where the target happens to live does not.
- The **only** link permitted is the interpreter itself, in the final position. Any link or Windows directory junction in an enclosing directory is refused. Junction detection is a predicate distinct from symbolic-link detection: it uses `pathlib.Path.is_junction` where the running Python has it, and the `stat` reparse-point attribute together with the mount-point reparse tag on Python 3.11, which predates that predicate. A runtime exposing neither route refuses rather than passing the check silently.
- An interpreter inside the candidate checkout is refused, and so is one whose resolved target lands inside it. That is the self-hosting boundary, not a path-hygiene rule; it is why the evaluator venv must live outside the clone.
- Refusal happens before any interpreter is spawned and before any target is validated. Refusal messages carry a case identifier and the subject, never the target's absolute path or environment content.

The boundary keeps its own diagnostic code — `RID004` and `RID006` for runtime identity, `MIG205` for governance migration — so an operator-facing message does not change shape. Reading `EPS...` in a detail string tells you which declared case fired.

One acceptance narrowed rather than widened: an interpreter sitting directly below a filesystem root has no derivable environment root and is now refused. No real virtual environment has that shape.

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

## Release sequences

Owner content moved here from the retired repository-context document under `WO-ADS-002`. It grants no authority; every step below runs only under the approved work order or release record it names.

- Candidate version bump: the candidate version and the governance-migration scenario are one fact recorded twice, so they move together. The `governance-migration` job of `.github/workflows/candidate-evidence.yml` builds its successor runtime from `GITHUB_SHA`, and `rehearse-migration` refuses any scenario whose declared successor differs from the version that runtime reports (`MIG211`, `SPEC-REB-008` rule 4). Raising `pyproject.toml` to a new version therefore requires, in the same change, a scenario under `tests/fixtures/governance_migration/` declaring that version as its successor. Write it with the canonical writer, never by hand: `python -m repository_tools.predecessor_facts write-scenario --repository . --template tests/fixtures/governance_migration/candidate-<previous pair>.json` re-points the template at the declared root's evaluator (from the lock) and the new candidate version (from `pyproject.toml`), recomputes the digests the contract checks, and writes `candidate-<predecessor>-to-<candidate>.json` in canonical bytes; writing the committed pair from the committed scenario reproduces it byte for byte. Nothing in the workflow changes: `candidate-source` derives the predecessor's version, wheel digest and the scenario path from the declared root and the candidate version (`repository_tools.predecessor_facts derive`) and fails closed, naming the expected path, when the scenario is missing, so the omission fails the first job on the pull request and `tests/test_ci_pipeline.py` and `tests/test_governance_migration.py` fail it on the workstation first. The refusal is correct behaviour and is never to be relieved by relaxing the comparison, which rule 15 forbids; the configuration is what changes.
- Release contract: the unit is one candidate commit (`WO-CIP-004`, `ADR-CIP-002`). Cut it from `main` (or from `candidate/<version>` when a fix to the release itself is needed), write `candidate_commit` and `previous_release_tag` into the contract, and paste the `gates` array `harnessctl release-unit . --from <tag> --to <commit> --toml` prints; `--contract REL-...` re-measures it and reports `E-CIP-001` on any difference, and the approval itself re-measures it: a release contract that names a `candidate_commit` cannot leave `draft` while its `gates` differ from the derivation (`QGP-G5P-RELEASE-UNIT`, `WO-CIP-005`); an untraced commit on the path needs `[release_unit] untraced_exemptions = ["<sha>"]` in the contract. A merge to `main` after the cut does not invalidate the contract; a commit on the first-parent path without a `Harness-Work-Order` trailer must be exempted explicitly (`--exempt <sha>`, and named in the contract with the reason) or the derivation fails.
- Build: under an approved release work order and after the exact candidate commit exists, run `python -m repository_tools.release_build replay --repository . --commit <full-candidate> --version <version> --output-directory <bundle-dir> --result <replay.json>`. The strict interpreter reads `release/build-recipe.json` and `release/build-toolchain.lock` from that candidate, launches two fresh instances of the digest-pinned Linux/amd64 producer, proves the exact CPython and complete hash-locked tool inventory, applies only the closed environment and argument arrays, normalizes the sdist, and requires byte-for-byte equality. Create retained binding evidence with `python scripts/create_release_bundle_manifest.py --repository . --commit <full-candidate> --version <version> --wheel <bundle-dir>/<wheel> --sdist <bundle-dir>/<sdist> --build-recipe release/build-recipe.json --output <bundle.json>`. Do not substitute native host commands for this recipe-era path. After the two producer runs the replay hands the workspace back to the calling user with one further run of the same pinned image (`chown -R <uid>:<gid> /workspace`, POSIX hosts only, `WO-RLO-007`): the producer writes as root inside the bind mount, and without the hand-back a hosted runner cannot tear the workspace down. The host this runs on does not enter the result (`WO-RLO-008`): the export disables Git line-ending conversion for its own invocation and each producer establishes the declared `0o775`/`0o664` source mode set inside the container, so a Windows workstation reproduces a bound record's exact bytes. Do not re-add a host restriction here; the two mechanisms are the obligation and are tested, and a note cannot fail a build.
- Release preparation: first run generic `harnessctl prepare-release ...` to create the ready RLS, then bind the retained schema-2 bundle with `python scripts/bind_release_distribution.py --repository . --release-record <RLS-path> --manifest <bundle.json>`. The binder changes only the repository-owned distribution table and fails atomically. Before the release decision, dispatch `.github/workflows/release-candidate-replay.yml` on the review ref with only `release_record=RLS-...`; it rebuilds twice from the already-bound recipe and hashes with read-only repository permission and retains technical evidence. Historical released schema-1 records remain valid as records, but they are never re-published: the release qualification is one definition, `.github/workflows/release-qualification.yml`, and it replays a bound schema-2 recipe only (`WO-CIP-002`, `SPEC-CIP-001` CIP-LEG 1). A new ready record cannot use schema 1. The publication rehearsal, `.github/workflows/publication-rehearsal.yml`, invokes that same definition on every pull request and push to `main`: in `candidate` mode it qualifies the commit and replays the commit's own recipe twice, and in `release-record` mode, when a ready or released schema-2 record exists (`publish_release.py select-rehearsal-record` chooses the newest, or a dispatch names one), it does what the release will do for that record. See [rehearsing the publication path](release-publication-rehearsal.md).
- Authorized last mile: after the RLS is `released` in `main`, dispatch `.github/workflows/publish-pypi.yml` from `main` with only `release_record=RLS-...`. Before privileged jobs, the workflow validates the complete committed governance graph with current semantics and, for a bound predecessor-bootstrap RLS, uses the standard predecessor-view qualification. It derives the candidate, governance commit, version, tag, recipe, files, hashes, and canonical `release/MAJOR.MINOR` maintenance line. The `qualify` job is a caller of `.github/workflows/release-qualification.yml` in `release-record` mode, so the release executes exactly the definition the rehearsal executed; there is no legacy leg. Only verified inert bytes cross into jobs that reconcile the exact GitHub tag and Release, maintenance line, PyPI state, Pages deployment, and public observation. The Pages deployment is a caller of `.github/workflows/pages-publication.yml`, the same definition the standalone `publish-dashboard-pages.yml` recovery workflow calls. The protected `pypi` environment remains a separate human decision.

This repository integrates reviewed work through branches and pull requests without one mandatory development-branch prefix. Every pull request subject to the installed workflow declares exactly one standalone `Harness-Work-Order: WO-...` field; branch naming does not substitute for that declaration or for approved scope. Repository release automation establishes `release/MAJOR.MINOR` from each authorized released candidate as the canonical maintenance line. Existing compatible lines may advance through separately governed maintenance work; automation never moves a conflicting ref. This local rule is not part of portable SE Harness or its consumer workflow.

## Advancing the root evaluator

Candidate success never changes the root evaluator. The current root is exact public 0.6.0 under a schema-3 identity lock. After a later SE Harness version is immutably published, maintainers install that exact release outside the checkout — an ordinary `pip install "se-harness==X"` is enough, from the index or from a wheel file — review `harnessctl upgrade .`, and run `harnessctl upgrade . --apply` (add `--evidence-output docs/engineering/<domain>/evidence/<name>.json` to retain the transaction evidence). The installed evaluator's version and installed-payload digest become the lock's identity; the archive digest is recorded when the installation carries one and `null` otherwise (`WO-REB-027`, `SPEC-REB-012`). No evaluator-upgrade packet and no wheel-file install are required any more. Which repository change is authorized is this repository's own policy: the changed managed files land under a normal work order. The standard upgrade transaction preserves repository-owned content and fails closed on customization or integrity ambiguity.

See the current [standard repository lifecycle guide](../engineering/self-hosting-boundary/SELF_HOSTING.md), the owner-controlled region of [`AGENTS.md`](../../AGENTS.md), and managed [`ENGINEERING_HARNESS.md`](../../ENGINEERING_HARNESS.md).
