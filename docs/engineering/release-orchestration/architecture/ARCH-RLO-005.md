+++
id = "ARCH-RLO-005"
type = "architecture"
title = "Credential-free rehearsal lane with a checked equivalence seam"
status = "approved"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-RLO-015", "REQ-RLO-016"]
conforms_to = ["SPEC-RLO-005"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "deployment-or-operating-model", "material-alternatives", "cross-cutting-policy", "responsibility-or-dependency-direction"]
rationale = "The change decides whether the release orchestrator is refactored into a shared implementation or left unchanged behind a checked equivalence seam, which fixes the trust model of every future pre-release assurance claim and the risk carried by the live release path."
assessed_by = "engineering-owner"
+++

# Architecture: Credential-free rehearsal lane with a checked equivalence seam

## Context and scope

`.github/workflows/publish-pypi.yml` performs the last mile as one credentialed transaction. Its credential-free work is split across `resolve` on `ubuntu-latest` and `qualify` on `windows-2022`, so half the mechanics run only on Linux and half only on Windows. Neither half is exercised on the other platform before a release. This architecture adds a second, credential-free lane that exercises the whole credential-free surface on both platforms, and one seam that fails closed when the two lanes stop matching. It changes no publication behavior.

## Components and responsibilities

- A repository-owned rehearsal program under `.github/scripts/` owns platform-neutral orchestration: canonical root resolution, virtual-environment layout selection, temporary-path identity, candidate export, invocation of the same underlying tools publication invokes, byte comparison, and link-safe teardown.
- A data-only mechanic declaration owns the mapping from orchestrator mechanic to rehearsal coverage, the digest of each credential-free orchestrator step, and the closed vocabulary of realization surfaces. It carries no logic, so it cannot satisfy itself.
- A repository-owned rehearsal workflow owns the two-platform matrix, `contents: read` only, the pull-request and `main` triggers, and the release-owner dispatch input.
- The divergence checker owns strict parsing of the orchestrator, job classification by declared attributes and by dependency on an excluded job, step-digest and action-surface comparison, and the covered/uncovered/stale verdict.
- A bounded workflow reader, vendored inside the rehearsal program, owns parsing the Actions subset both workflow files use, so the checker adds no repository dependency. An independent second parser is a cross-check the checker may request, never a requirement it depends on.
- Repository tests own the negative matrix: platform layout, alias canonicalization, temporary-path identity, determinism failure, verification failure, teardown refusal, classification, and both divergence directions.
- `.github/workflows/publish-pypi.yml`, portable `se_harness`, managed templates, the managed validator, and consumer surfaces own nothing here and are unchanged.

## Dependency direction

The rehearsal depends on the orchestrator: it reads the orchestrator's declared mechanics and reproduces them. The orchestrator depends on nothing in the rehearsal. Both depend on the same repository release tooling. Portable SE Harness depends on neither. Nothing in the rehearsal is imported by, packaged with, or installed into a consumer.

## Data and control flow

`candidate commit -> canonical rehearsal root -> platform layout and temporary identity -> candidate exported twice -> pinned build tools -> qualification, unit suite, CLI smoke -> two deterministic builds -> normalized sdists -> byte comparison -> bundle assembled -> manifest and bundle verified across the two independent sets -> link-safe teardown -> per-platform result`

In parallel: `orchestrator YAML -> bounded parse (optionally cross-checked) -> job classification -> transitive exclusion through needs -> credential-free step set -> step digests, command keys, action surface -> compare with data-only declaration -> covered/uncovered/stale verdict`

## Trust boundaries

- The rehearsal lane holds `contents: read` and no token, secret, environment, or write permission, so candidate code executes with no credential at all.
- The public evaluator wheel crosses an untrusted boundary and is hash-proven before installation.
- Orchestrator YAML, declaration data, subprocess output, and filesystem state are untrusted until structurally checked.
- The rehearsal root is the only writable derived region; teardown never crosses out of it, and links inside it are unlinked rather than followed.
- The rehearsal produces no formal authority, so a green result cannot be mistaken for verification, approval, or release.

## Required patterns

- Platform capability resolved from the running platform, never hardcoded, never shelled out to a platform-specific utility.
- Canonicalize-then-use for every root path, before any environment creation or export.
- Assert-what-you-set for temporary-path identity: the parent sets it, a child reports it back, and the two are compared.
- Cross-check between independent builds rather than self-comparison.
- Data-only declaration compared by exact identity.
- Digest-what-you-declare: a declared step carries the digest of the script it declares, so a change inside the step is a divergence even when every command it invokes is still declared.
- Closed vocabularies: a mechanic's realization surface and a job's action surface are both drawn from declared sets, and a value outside the set is refused rather than accepted as new.
- Fail-closed classification: an unclassifiable job fails rather than defaulting to excluded or included, an absent permission block excludes rather than permits, and exclusion propagates to every dependent job.
- Report-every-exclusion, so a shrinking rehearsal surface is visible instead of silent.
- Link-safe teardown with a post-condition assertion.

## Prohibited patterns

- Editing `.github/workflows/publish-pypi.yml`, its input surface, its permissions, or its behavior.
- Reimplementing normalization, manifest, plan, verification, or qualification logic instead of invoking it.
- `cygpath`, `sha256sum`, `cmp`, or any other utility absent from a default runner of either platform.
- Hardcoded `bin/` or `Scripts/` paths, or a platform branch expressed in workflow shell rather than in the program.
- Silent skips, name-similarity matching, warning-level divergence, or a declaration that computes anything.
- Any credential, token, environment, ref, tag, release, index, or deployment action.
- Any change to portable code, managed files, the lock, or consumer surfaces.

## Quality attributes

- Safety: the strongest available property is that the lane cannot publish, because it holds no credential and no write permission.
- Fidelity: the rehearsal invokes the same tools publication invokes, so only the shell glue differs — and the glue is precisely what is being made portable.
- Honesty: the result declares its mode, and states that only `release-record` mode compares against an authorized release identity.
- Fail-closed drift detection: the seam converts silent divergence into a red required check.
- Reproducibility: an engineer can run the rehearsal locally on one platform and reproduce a hosted failure.
- Bounded blast radius: nothing in this change can alter the release transaction, because the release transaction is not touched.

## Accepted architectural weakness

Equivalence is checked, not structural. Two lanes exist, so they can differ in a way the checker does not model. The checker compares the mechanic set, the declared platforms, each credential-free step's script digest, the command keys inside those steps, and the action surface of those jobs. Within a step, therefore, an argument change, an added flag, and a reordering are all caught, because the digest covers the script's exact bytes after line-ending normalization.

What remains unproven is equivalence of *sequence and environment* between the two lanes. The rehearsal program decides its own order of mechanics and its own environment shape; the checker does not prove that order matches the orchestrator's step and job order, nor that a mechanic the rehearsal drives with the same command sees the same surrounding state the orchestrator gives it. A drift of that kind — the orchestrator moving a step between jobs, or changing what an earlier step leaves behind — passes every comparison the checker makes, because the checker's unit is a step's script rather than the pipeline that reaches it. `ADR-RLO-005` records why the owner accepted this weakness instead of refactoring the live release path, and what would change the decision.

## Conformance checks

- Strictly parse both workflows and assert the rehearsal lane declares both runner types and `contents: read` only, and that the orchestrator is byte-unchanged against its merge-base content.
- Exercise the negative matrix on the real platform where possible and through injected platform state otherwise: absent layout, alias root, temporary-identity mismatch, non-deterministic build, failed verification, teardown residue, link escape attempt, unclassifiable job, uncovered mechanic, stale mechanic, executable declaration.
- Assert the declaration is data only.
- Inspect changed paths, the built wheel inventory, and the standard template inventory to prove the portable and consumer boundary is unchanged.
- Validate the formal graph with no new structural, governance, or policy errors.

## Related ADRs

`ADR-RLO-005` decides the parallel lane with a checked equivalence seam over refactoring the orchestrator into a shared implementation.

## Approval

Approved by the accountable repository owner on 2026-08-24 through the statement `OK go for #111` together with the selected `Parallel lane + drift check` design.

## Amendments during implementation

Stated for owner acceptance or rejection. Nothing below changes the decided structure: one unchanged orchestrator, one credential-free lane, one checked seam.

- **The seam has three layers, not one.** *Components and responsibilities* and *Data and control flow* now name the step-digest and action-surface layers and the vendored bounded reader. Implementation showed the mechanic-set comparison alone leaves two channels open: a change inside a step that keeps every command key, and a mechanic arriving through a marketplace action rather than a shell command.
- **The accepted weakness is smaller and differently shaped.** The original text accepted that "identical commands invoked with different arguments, or an ordering difference between mechanics" could pass. Step digests close the argument case and the within-step ordering case outright, so keeping that sentence would have overstated the risk the owner accepted. What is genuinely unproven is sequence-and-environment equivalence between the two lanes, and the section now says so instead. This narrows the accepted weakness; it does not add one.
- **Parsing is vendored.** The checker parses with a bounded reader restricted to the Actions subset rather than a general YAML library, because `pyproject.toml` declares no dependencies and a drift check that fails to import is a drift check that does not run. The independent cross-check remains available and was confirmed to agree about the 703-line orchestrator and every fixture, so the strictness the original text assumed is measured rather than asserted.
