+++
id = "SPEC-RLO-005"
type = "specification"
title = "Cross-platform publication rehearsal and divergence contract"
status = "approved"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-RLO-015", "REQ-RLO-016"]
+++

# Specification: Cross-platform publication rehearsal and divergence contract

## Scope

Add a repository-owned, credential-free rehearsal of the publication mechanics that runs on both the Linux and the Windows runner type, and a fail-closed check that the rehearsal still matches the publication orchestrator. `.github/workflows/publish-pypi.yml` is not modified. This contract is repository policy of `mmzen/se_harness`; it is not installed, packaged, or imposed on consumers.

## Actors and external systems

- Ordinary candidate integration triggers the rehearsal lane on pull requests and on pushes to `main`.
- A release owner may dispatch the rehearsal against a prepared release record before deciding whether to approve it.
- GitHub Actions provides the two runner types under `contents: read` only.
- The already-public released evaluator wheel is fetched over HTTPS as unauthenticated public data.
- No package index, tag, ref, release, environment, or Pages surface is contacted for writing.

## Inputs

- A candidate commit, defaulting to the checked-out `HEAD`.
- A mode: `candidate`, which rehearses the current candidate, or `release-record`, which rehearses a named `RLS-*` present in the repository.
- In `release-record` mode, one canonical `RLS-[A-Z0-9-]+-[0-9]{3}` identifier already committed to the repository.
- The publication orchestrator file, read as untrusted text for the divergence check.
- The data-only mechanic declaration.

## Outputs

- A machine-readable rehearsal result naming the platform, the mode, the candidate, and every mechanic with an outcome of `executed`, `failed`, or `excluded` plus a reason for anything not `executed`.
- A machine-readable divergence result listing each orchestrator mechanic as `covered`, `uncovered`, or `stale`, each excluded orchestrator job with the attribute that excluded it, and each step-level, command-level, and action-level finding with its direction.
- A rehearsal result that also states the inherited checkout condition — worktree cleanliness and line-ending conversion — because an inherited checkout changes what some mechanics can prove.
- A bounded human summary for the workflow run.
- No repository file, ref, tag, release, index object, deployment, or artifact lifecycle state.

## State model

1. **Unrehearsed:** no result exists for the candidate on a platform; no release-approval claim about that platform is supportable.
2. **Rehearsing:** derived trees exist under one canonical rehearsal root.
3. **Rehearsed-exact:** every required mechanic reported `executed` on both platforms, every mechanic that is not required on this run reported `excluded` with its reason, and both independent distribution sets compared byte-identical.
4. **Rehearsed-divergent:** the divergence check reported at least one `uncovered` or `stale` mechanic; the rehearsal result must not be read as coverage.
5. **Failed:** a mechanic reported `failed`; the platform, mechanic, and observed divergence are named.
6. **Torn-down:** every derived tree the rehearsal created is removed and the repository worktree is clean.

## Behavioral rules

### Mechanic inventory and coverage

1. Treat as a *mechanic* each distinct command the orchestrator's credential-free jobs invoke. Measured against the orchestrator at the candidate commit, that is the following twenty-two: release-record format validation, evaluator resolution, evaluator acquisition and hash proof, evaluator identity proof, predecessor-view qualification, distribution-policy validation, plan resolution, the bounded resolution-refusal document, candidate export, temporary-path identity establishment, pinned build-tool installation, complete-candidate qualification, the unit suite, the CLI smoke check, the deterministic build, sdist normalization, build determinism comparison, bundle assembly, bundle-manifest creation, build-manifest verification, bundle verification, and the recipe-bound build replay.
2. Classify an orchestrator job as credential-bearing when it declares any write permission, an `id-token` permission, no explicit `permissions` block at all, an `environment`, a secret or token in `env`, a step `env`, or a step `with`, or a step using an action that mutates external state. Exclusion is transitive: a job that consumes state produced by an excluded job runs after a credential has been used and is excluded too, naming the dependency as its excluding attribute. Every other job is credential-free.
3. Require rehearsal coverage for the mechanics of credential-free jobs only. Report every excluded job together with the attribute that excluded it, including an attribute inherited through `needs`; never omit it silently.
4. Add exactly one rehearsal-only mechanic, teardown, which the orchestrator does not perform because its runners are ephemeral. Declare it as rehearsal-only so it is never reported as orchestrator drift.
5. Drive the same underlying tools the orchestrator drives. Do not reimplement `normalize_sdist.py`, `create_release_bundle_manifest.py`, `publish_release.py`, `publish_dashboard.py`, `python -m build`, or any `harnessctl qualify` behavior.

### Platform neutrality

6. Resolve the virtual-environment interpreter and console-script paths from the running platform, using the `bin` layout on POSIX and the `Scripts` layout on Windows. Never hardcode either.
7. Perform every path conversion inside Python using path objects. Never invoke `cygpath`, and never require a POSIX shell utility such as `sha256sum` or `cmp` that is absent from a default Windows runner.
8. Canonicalize the rehearsal root before creating any virtual environment or exporting any tree, so an alias such as a Windows 8.3 short name or a symlinked POSIX parent resolves to the path the invoked tools will observe. Assert that the canonicalized root is a directory and fail otherwise.
9. Establish temporary-path identity for every child process by setting the platform's temporary-directory variables to the canonicalized rehearsal temporary root, and assert that a child process reports the same root the parent set.
10. Compute every digest with the Python standard library, and compare distribution bytes by reading them, so digest and comparison behavior is identical on both platforms.
11. Run the same shell on both platforms for lane orchestration, and keep all platform-conditional logic inside the rehearsal program rather than in workflow shell fragments.

### Determinism and verification

12. Export the candidate twice into two independent trees from the same commit, using the repository's own archive of that commit rather than the working tree.
13. Build each exported tree with the pinned build, `setuptools`, and `wheel` versions, assert exactly one wheel and one sdist per tree, and normalize each sdist with the candidate's own `normalize_sdist.py` at the candidate commit's own timestamp.
14. Compare the wheel and the normalized sdist of the two sets byte for byte and fail on any difference, reporting the first differing offset and both digests.
15. In `candidate` mode, derive the bundle manifest and plan from the first distribution set and verify the *second* set against it, so verification is a cross-check between independent builds rather than a self-comparison.
16. In `release-record` mode, derive the plan from the named record through the orchestrator's own resolution command and verify the assembled bundle against that record's bound distribution identity.
17. State in the result which mode produced the verification, because only `release-record` mode compares against an authorized release identity.

### Teardown

18. Create every derived tree under one canonical rehearsal root and nothing outside it.
19. Remove derived trees without following links: remove a `git` worktree through `git worktree remove`, and delete directory trees by unlinking links rather than recursing through their targets.
20. Assert after teardown that the rehearsal root is gone, that no path outside it was removed, and that `git status` reports the repository worktree clean and free of untracked residue.
21. Report teardown failure as a failed mechanic. Never leave residue silently and never delete a path the rehearsal did not create.

### Divergence check

22. Parse the orchestrator strictly and fail on a duplicate key, an unexpected structure, or an unclassifiable job. Rule 34 states which parser satisfies this.
23. Read the mechanic declaration as data only. Fail if it contains executable logic.
24. Report a credential-free orchestrator mechanic absent from the declaration as `uncovered`, and a declared mechanic no longer invoked by the orchestrator as `stale`. Fail on either.
25. Match mechanics by exact declared identity, never by name similarity or substring.
26. Confirm the orchestrator's credential-free jobs still declare the runner types the rehearsal claims to complement, and that the rehearsal lane declares both the Linux and the Windows runner type. Fail if either platform is missing.
27. Never edit either side, never weaken a comparison to make a change pass, and never downgrade a divergence to a warning.

### Authority boundary

28. Acquire no publication credential, request no protected environment, and use no repository token.
29. Create, move, or delete no ref, tag, release, index object, deployment, or environment approval.
30. Change no formal artifact lifecycle state, and treat every rehearsal result as derived operational evidence.
31. Change no portable `se_harness` module, managed template, managed validator, managed workflow, consumer workflow, consumer documentation, or `.engineering-harness.lock` entry.
32. Leave `.github/workflows/publish-pypi.yml` byte-unchanged.

### Divergence layers added during implementation

Rules 33 to 36 were added while implementing `WO-RLO-005`, each because a measurement showed that rules 22 to 27 alone leave a drift channel open. They extend the divergence check and weaken nothing above.

33. Fingerprint every credential-free orchestrator step by its declared name and by the SHA-256 of its `run` script normalized to LF. Fail on a step absent from the declaration, on a declared step whose digest no longer matches, and on a declared step the orchestrator no longer performs. Command-level coverage alone cannot see a changed argument, an added flag, or a reordered command inside a step that is already declared.
34. Read the orchestrator and the rehearsal lane with a bounded reader restricted to the Actions subset both files use, refusing a tab, a duplicate key, an unsupported construct, or an unexpected structure. Support an optional independent second parse that must agree about the job mapping, and fail when that cross-check is requested and the second parser is unavailable. Do not make the second parser a repository dependency, because the check must run from a bare interpreter.
35. Classify the action surface of every rehearsed job. An action that is neither declared infrastructure nor a declared external-state action is a divergence, and so is an action that is not pinned to a full forty-character commit, because a credential-free job can also gain a publication mechanic through a marketplace action rather than a shell command.
36. Declare a closed vocabulary of realization surfaces, and require every declared mechanic to name exactly one of them. Refuse a declaration that names a surface outside the vocabulary, so a mechanic cannot silently claim rehearsal coverage that no surface provides.

### Resolution subject added during implementation

Rule 37 was added for the same reason as rules 33 to 36: a measurement showed that the rules above do not say which subject a mechanic may be exercised against, and the mechanic that has no valid subject in `candidate` mode was reporting a failure of publication instead.

37. Exercise the predecessor-view qualification only against a subject whose committed bootstrap contract names the evaluator the run actually resolved. In `candidate` mode, compare the resolved evaluator identity with the subject record's declared predecessor evaluator identity and, when they differ or the record declares none, report the mechanic `excluded` with both measured identities rather than `failed`. In `release-record` mode never exclude it: a record under preparation must bind the governing evaluator, so a mismatch there is a defect in that record and must fail.

The accountable repository owner ruled on 2026-08-24 that `excluded` is the correct outcome here: on ordinary integration there is no valid subject, so reporting `excluded` with both measured identities is honest, and `release-record` mode still fails on a real mismatch, which is where the comparison is meaningful. Rule 37 must therefore not be satisfied by omitting the mechanic from the result, by reporting it `executed`, or by admitting an exclusion in `release-record` mode.

### Matrix-aware platform claims added during implementation

Rules 38 and 39 were added when `main` advanced during implementation and gave the orchestrator's `qualify` job a two-mode matrix. Rules 26 and 33 assume one runner label and one platform claim per job, which the matrix makes false: the same job now runs the legacy mechanics on `windows-2022` and the recipe-era mechanics on `ubuntu-latest`, gating its steps by mode. A per-job claim would state that both halves run on both platforms, which is the overstatement that `RC-060-11` is about.

38. Resolve a credential-free job's runner platforms from its matrix rather than from a single literal label. Enumerate its combinations from an `include` list or from plain axes crossed as a product, never from both together, refuse an `exclude` list and an empty matrix, and resolve a `runs-on` of the form `${{ matrix.<key> }}` against every combination. A job's platform families are the union over its combinations. Refuse any other runner expression instead of inferring a platform from it.
39. Claim orchestrator platforms per step, not per job, and derive each mechanic's expected platforms as the union over the declared steps of its own job that realize it. Evaluate a step's `if` gate against each combination over the grammar of `matrix.<key> == '<literal>'` and `!=` comparisons joined by `&&` and `||`; treat a gate that also reads a run-time context or a status function as able to hold, because the check may not decide a run-time value; and refuse a gate outside that grammar rather than guessing. Fail when a declared step's platforms differ from the measured ones, and fail when a declared step is gated out of every combination, because the orchestrator then performs it on no platform at all.

### Resolution subject added during implementation

Rule 40 was added in the same measurement: `main`'s new recipe-era half of `qualify` replays the bound build recipe, and that replay cannot be rehearsed on either runner type here.

40. Declare the recipe-bound build replay as an orchestrator mechanic and always report it `excluded` with a measured reason, in a fixed precedence: no eligible released distribution-schema-2 record with a bound recipe, then the rehearsal not running on the platform or without the container runtime the replay requires, then the boundary reason naming the repository's dedicated credential-free replay lane. Never omit it, and never report it `executed`. The replay pulls and runs an immutable `linux/amd64` container producer against a released record's bound recipe, so it is not platform-neutral under rules 6 to 11, has no valid subject on a candidate that no released schema-2 record binds, and is already exercised by a separate hosted lane.

## Error and recovery behavior

| Condition | Required behavior |
|---|---|
| Rehearsal root cannot be canonicalized or is not a directory | fail before creating any tree |
| Child process reports a different temporary root than the parent set | fail as a temporary-path identity divergence |
| Platform virtual-environment layout is absent | fail naming the expected layout and the platform |
| Exactly one wheel and one sdist are not produced | fail without assembling a bundle |
| The two distribution sets differ | fail reporting the first differing offset and both digests |
| Bundle or manifest verification fails | fail reporting the mode and the compared identities |
| A mechanic cannot run on a platform | fail; a skip is permitted only for a declared exclusion with a reported reason |
| Teardown leaves residue or would follow a link outside the root | fail without deleting outside the root |
| Orchestrator cannot be parsed or a job cannot be classified | fail the divergence check |
| Declaration contains executable logic | fail the divergence check |
| A mechanic is uncovered or stale | fail the divergence check naming the mechanic and direction |
| A credential-free step is undeclared, or its declared `run` digest no longer matches | fail the divergence check naming the job, the step, and both digests |
| A rehearsed job uses an unclassified action, or an action not pinned to a full commit | fail the divergence check naming the job, the step, and the action |
| An independent parser cross-check is requested and that parser is unavailable | fail the divergence check; never silently fall back to the bounded reader alone |
| The two parsers disagree about the job mapping | fail the divergence check naming every differing job |
| A declared mechanic names a realization surface outside the vocabulary | refuse the declaration before any comparison |
| Public evaluator download or its hash proof fails | fail the evaluator mechanics; other mechanics still report their own outcome |
| In `candidate` mode no committed record binds the resolved evaluator as its predecessor | report predecessor-view qualification `excluded`, naming the resolved evaluator identity and the record's own, and never report it `failed` for that reason |
| In `release-record` mode the named record binds a different evaluator than the run resolved | fail the mechanic; the record under preparation is the defect |
| A rehearsed job declares both matrix axes and an `include` list, an `exclude` list, or an empty matrix | refuse the workflow before any comparison; the combination set is not decidable |
| A rehearsed job's `runs-on` is an expression other than a resolvable `matrix` key | fail the divergence check naming the job and the expression |
| A step gate falls outside the comparison grammar | fail the divergence check naming the job, the step, and the gate |
| A declared step's platforms differ from its measured job-and-gate platforms | fail the divergence check naming the job, the step, and both platform sets |
| A declared step is gated out of every matrix combination | fail the divergence check; the orchestrator performs it on no platform |
| A declared mechanic's platforms differ from the union over its realizing steps | fail the divergence check naming the mechanic and both platform sets |
| A declaration step omits its platform claim, names an unknown platform family, or realizes no mechanic | refuse the declaration before any comparison |
| A declared orchestrator mechanic is realized by no declared step of its own job | refuse the declaration before any comparison |
| The recipe-bound build replay has no eligible subject, platform, or container runtime | report it `excluded` with the measured reason in the precedence rule 40 fixes, in both modes |

## Data and interface contracts

The mechanic declaration is a data-only mapping from a stable mechanic identifier to its orchestrator job, its orchestrator invocation, whether it is orchestrator-derived or rehearsal-only, the platforms on which the orchestrator performs it, and the realization surface that rehearses it. It additionally declares the orchestrator and lane paths, the required platforms, the external-state and infrastructure action sets, the shell trivia whose arguments carry no mechanic identity, the closed realization-surface vocabulary, and one entry per credential-free orchestrator step carrying that step's `run` digest, its own orchestrator platforms, and the mechanics it realizes. The declaration carries an explicit schema identifier, and the step platform claim required by rule 39 is a schema change: a declaration is refused when a step omits a required key, names a platform family outside the known set, or realizes no mechanic, and when a declared orchestrator mechanic is realized by no declared step of its own job. The step-to-mechanic link is therefore load-bearing rather than documentary, because rule 39 derives every mechanic's platform claim from it. The rehearsal result and divergence result are JSON documents carrying an explicit schema identifier, the platform, the mode, the candidate commit, the inherited checkout condition, and the per-mechanic outcomes. Both results declare that their authority is derived operational evidence and that no lifecycle transition occurred. Result documents are workflow artifacts and never formal repository authority.

## Security and privacy properties

The lane declares `contents: read` and nothing else. Candidate code runs only in jobs that hold no credential, matching the property `INT-RLO-001` already requires of publication. The evaluator wheel is unauthenticated public data whose digest is proven before installation. Orchestrator YAML, declaration content, downloaded bytes, subprocess output, and filesystem state are untrusted until structurally checked. No credential, token, or environment value is printed. Teardown never follows a link out of the rehearsal root, so a malicious or accidental link inside a derived tree cannot cause deletion elsewhere.

## Performance and capacity

The rehearsal performs a bounded, fixed sequence with no retry loop and no polling. It builds the candidate twice per platform and runs the unit suite once per platform, which is the dominant cost and is the same work publication performs on one platform. It adds no persistent service and retains only small result documents.

## Observability

Each platform reports a per-mechanic table with outcomes and reasons, the two distribution digests, the mode, and the teardown assertion result. The divergence check reports covered, uncovered, and stale mechanics and every excluded orchestrator job with its excluding attribute. Failure diagnostics name the platform, the mechanic, and the observed divergence without printing credentials.

## Compatibility and migration

Publication behavior, the single `release_record` input, and the `RLO-001` through `RLO-003` guarantees are unchanged. Existing release records, tags, branches, and published distributions are untouched. Because the rehearsal is a second lane, the divergence check is the compatibility mechanism: a later change to the orchestrator's credential-free surface fails the check until the declaration and the rehearsal are updated together.

## Examples and counterexamples

- Valid: the Windows lane proves evaluator identity through the `Scripts` layout, a mechanic publication performs only on Linux.
- Valid: the Linux lane exports, builds, normalizes, and verifies without `cygpath`, mechanics publication performs only on Windows.
- Valid: a child process reports the same temporary root the rehearsal set after canonicalizing a short-name alias.
- Valid: the divergence check fails because a new credential-free orchestrator step is undeclared.
- Valid: the divergence check reports `pages_build` as excluded because it uses actions that mutate external state.
- Valid: the divergence check reports `observe` as excluded although it holds no credential itself, because it depends on the excluded job `github_release`.
- Valid: the divergence check fails because an already-declared step gained a flag, so its `run` digest no longer matches while every command it invokes is still declared.
- Valid: `candidate` mode reports predecessor-view qualification as excluded because the governing evaluator `0.6.0` is not the predecessor evaluator `0.5.0` that the newest released record binds.
- Valid: a two-mode matrix job resolves to Linux and Windows, and a step gated to the legacy mode claims Windows alone while an ungated step in the same job claims both.
- Valid: the divergence check fails because an orchestrator step lost its mode gate, so it now runs on both platforms while the declaration still claims one.
- Valid: the recipe-bound build replay reports `excluded` naming the absent container runtime and the dedicated replay lane that does exercise it.
- Invalid: claim a matrix job's platforms for every step it contains, so a gated half of the job appears rehearsed on a platform it never runs on.
- Invalid: satisfy rule 39 by widening a step's declared platforms to the job's union, or by narrowing a mechanic's claim to one platform the declaration finds convenient.
- Invalid: skip a mechanic on one platform because it is inconvenient there.
- Invalid: report a mechanic `failed` because the rehearsal chose a subject the mechanic cannot accept.
- Invalid: satisfy the divergence check by editing the orchestrator or by matching a mechanic on a name prefix.
- Invalid: assert bundle verification against a plan derived from the same distribution set it verifies.
- Invalid: delete a path outside the rehearsal root, or leave a derived tree behind.
- Invalid: add a credential, environment, token, workflow input to the orchestrator, or any portable or consumer surface change.

## Explicitly unspecified decisions

The implementation agent may choose the rehearsal program's module layout and subcommand names, the mechanic identifier spelling, the result schema field names, the workflow file name and job names, step naming, and fixture organization. Whether the orchestrator is later refactored to share one implementation, which release records are rehearsed as a standing regression, hosted runner images beyond the two the orchestrator declares, and branch protection or required-check configuration remain owner-managed and outside this work.

## Approval

Approved by the accountable repository owner on 2026-08-24 through the statement `OK go for #111` together with the selected `Parallel lane + drift check` and `Fourth release-orchestration packet` designs. Implementation authority is limited to `WO-RLO-005` and grants no release, publication, deployment, or external action.

## Amendments during implementation

Implementing `WO-RLO-005` measured the orchestrator rather than describing it, and six statements above were wrong or incomplete as a result. Each amendment below is recorded with the measurement that forced it. No amendment weakens a rule, removes a failure mode, or widens the authority boundary, and no approved `statement` field changed.

The accountable repository owner accepted all seven amendments, `A1` through `A7`, on 2026-08-24 through the statement `Accept all seven`. That acceptance covers the amendments recorded in this section and the consequent entries in the state model, the outputs, the error and recovery table, and the examples; it authorizes no release, publication, deployment, push, or other external action.

Amendments `A8` and `A9` came later and from a different cause: `main` advanced under the open branch and changed the orchestrator itself, rather than a mismeasurement in this packet. They are **not** covered by the acceptance above and await the accountable owner's decision. Until that decision is taken, rules 38 to 40, declaration schema `v2`, and the twenty-second mechanic are implemented and measured but not owner-accepted, and this paragraph is the record of that gap. Nothing in either amendment changes the authority boundary, and neither is a substitute for accepting them.

| Amendment | What changed | Measurement that forced it |
|---|---|---|
| A1 | Rule 1 now names twenty-one mechanics instead of twenty, adding the bounded resolution-refusal document. | Classifying `.github/workflows/publish-pypi.yml` at the candidate commit found a twenty-first credential-free command in `resolve`, a `jq -n` invocation that emits the canonical release-result document for a refused resolution. Rule 24 would have reported it `uncovered` against the approved inventory. |
| A2 | Rule 2 adds an absent `permissions` block, step `env`, and step `with` as excluding attributes, and states that exclusion is transitive through `needs`. Rule 3 requires the inherited attribute to be reported. | Two measurements. The real orchestrator's `observe` job holds no credential of its own and would have been rehearsed, although it runs only after `github_release` has used one; it is now reported excluded as `depends on the excluded job github_release`. Separately, a test fixture whose jobs omitted `permissions` was classified credential-free, leaving no job to rehearse, which showed that silence about permissions is itself an excluding attribute. |
| A3 | Rule 22 no longer prescribes "a strict YAML load"; rule 34 states the parser contract instead. | The divergence check must run from a bare interpreter, and PyYAML is not a repository dependency (`pyproject.toml` declares none). A bounded reader restricted to the Actions subset satisfies rule 22's strictness, and an optional independent cross-check preserves the second opinion the original wording assumed. Both parsers were confirmed to agree about the 703-line orchestrator and about every fixture. |
| A4 | New rule 33 adds a per-step `run` fingerprint layer. | Command-level coverage under rules 24 and 25 is blind inside a declared step: adding a flag, changing an argument, or reordering commands leaves every command key already declared, so the check would have passed a changed orchestrator. Nine credential-free steps now carry a measured digest. |
| A5 | New rule 35 classifies and pins the action surface of rehearsed jobs. | A credential-free job can acquire a publication mechanic through a marketplace action instead of a shell command, and rules 22 to 27 inspected only `run` scripts. An unclassified action and an action not pinned to a full forty-character commit are now divergences. |
| A6 | New rule 36 requires a closed realization-surface vocabulary. | Declaring a per-mechanic realization freely allowed a mechanic to name a surface that rehearses nothing; the first draft of the declaration did exactly that. The vocabulary is now six surfaces, and a mechanic naming any other value is refused before comparison. |
| A7 | New rule 37 states which subject the predecessor-view qualification may be exercised against, and requires an exclusion with both measured evaluator identities when `candidate` mode has none. Two output statements and one state-model entry follow from it. | The first end-to-end rehearsal failed the mechanic with `PV001 evaluator wheel differs from the released RLS contract`. The same failure was then reproduced in a throwaway worktree at the merge-base `1431df5`, so it is not caused by this packet. Its cause was measured: `.engineering-harness.lock` is schema 3 and binds evaluator `0.6.0` (`2a952eb6…`), which the rehearsal installs, while the newest released record `RLS-SEH-012` binds predecessor evaluator `0.5.0` (`974ba2de…`) — and no released record in the repository binds `0.6.0`. A released record names the evaluator that qualified *it*, one release behind the lock that release then advanced, so on post-release integration `candidate` mode has no valid subject by construction. |
| A8 | New rules 38 and 39 resolve a job's platforms from its matrix and move the platform claim from the job to the step, deriving each mechanic's claim as the union over the declared steps that realize it. The declaration schema advances to `v2` with a required per-step platform claim and four new load-time refusals, and rule 26's per-job platform confirmation is now computed from rule 38. | Merging `main` into the branch changed the orchestrator: `qualify` gained `strategy.matrix.include` with a `legacy-schema-1` mode on `windows-2022` and a `recipe-schema-2` mode on `ubuntu-latest`, and `runs-on: ${{ matrix.os }}`. The divergence check refused it outright — `publication rehearsal: runs-on label has no known platform family: ${{ matrix.os }}` — which is the correct fail-closed behavior and not a repairable state. Six mechanics measurably run on both platforms now, four newly so, and every credential-free step of `qualify` carries a mode gate; a per-job claim would have stated that the Windows-only build half runs on Linux too. |
| A9 | Rule 1 now names twenty-two mechanics instead of twenty-one, and new rule 40 declares the recipe-bound build replay as always `excluded` with a measured reason in a fixed precedence. | The same merge added the step `Replay the exact bound recipe twice` to `qualify`, whose `python scripts/replay_release_build.py` command was `uncovered` against the approved inventory. Measuring the replay showed it cannot be rehearsed by this control: `repository_tools/release_build.replay_build` pulls and runs an immutable `linux/amd64` OCI producer through `docker pull --platform linux/amd64` and `docker run`, so `windows-2022` cannot run it at all; it requires a released distribution-schema-2 record with a bound recipe, and the repository has none; and `docker` is absent from the measuring host's `PATH`. `main` also added `.github/workflows/release-candidate-replay.yml`, a dedicated credential-free lane that does exercise it. Reporting the mechanic `excluded` with its measured reason follows rule 37's ruling, and unlike rule 37 it excludes in `release-record` mode too, because the platform obstacle is not a property of the subject. |

Three further facts belong on the record without amending a rule.

First, rule 20's teardown audit was unsatisfiable twice, in two different places, and only the second was found by running the rehearsal end to end. The containment helper was corrected early to compare inclusively. The audit that runs *after* removal still examined each deleted path by its parent, and the rehearsal root's own parent lies outside the root by construction, so the first complete run reported `teardown deleted a path outside the rehearsal root: C:/Users/mathi/rehearsal-inplace-1` after having removed the root correctly. The rule is unchanged; the audit now accepts exactly the root's own entry and audits every other deleted path by its parent, which is what rule 19 intends and what keeps a link's own target from deciding whether the link may be unlinked.

Second, rule 5's predecessor-view qualification requires a clean Git worktree, so rehearsing from a dirty inherited checkout fails it for a reason outside the rehearsal. This is a separate condition from the subject mismatch that amendment A7 records, and it was initially mistaken for it. The result now reports the inherited checkout condition so either cause is attributable rather than mysterious.

Third, the same inherited checkout decides the unit-suite mechanic. Rule 12 exports the build trees from the repository's archive of the commit, which is unaffected, but the orchestrator runs the unit suite in a `git worktree add` checkout and the rehearsal does the same under rule 5, so that checkout inherits `core.autocrlf`. On a Windows checkout that converts line endings, four tests asserting on exact bytes fail for that reason alone; the same commit is green in a `core.autocrlf=false` clone. The result now reports the inherited conversion setting alongside worktree cleanliness. No rule changes: the rehearsal is faithful to the orchestrator here, and the condition belongs to the checkout.
