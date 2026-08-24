+++
id = "SPEC-REB-010"
type = "specification"
title = "Role-specific release qualification commands and results"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-REB-020", "REQ-REB-021", "REQ-REB-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "technical-owner"
+++

# Specification: Role-specific release qualification commands and results

## Scope

This specification defines a new public `harnessctl qualify` namespace with five closed subcommands. It converts release qualification from caller-assembled validator paths into named operations whose evaluator, target, checks, provenance, and independence semantics are fixed by the command contract.

It also defines one canonical result schema and the workflow migration required by issue #109 / RCA `RC-060-09`. It does not change lifecycle policy, compatibility-view contents, release authority, product version, root managed bytes, or public distribution state.

## Public command surface

The CLI shall expose these forms:

```text
harnessctl qualify released-root ROOT [--output PATH] [--json]
harnessctl qualify predecessor-view ROOT --release-record ID --evaluator-python PATH [--output PATH] [--view-output PATH] [--json]
harnessctl qualify complete-candidate ROOT --candidate-commit COMMIT [--output PATH] [--json]
harnessctl qualify candidate-package --candidate-wheel PATH --candidate-commit COMMIT --candidate-wheel-sha256 SHA256 --verifier-wheel-sha256 SHA256 [--checkout-root PATH] [--output PATH] [--json]
harnessctl qualify public-install ROOT --release-record ID --public-wheel PATH --public-wheel-sha256 SHA256 --payload-sha256 SHA256 [--output PATH] [--json]
```

Subcommands have independent parsers. Unsupported options, missing role inputs, options from another role, and trailing arguments fail during parsing. There is no `--role`, `--validator`, or arbitrary `--script` escape hatch.

`--output` is optional. When supplied, it names one new evidence file outside the inspected repository. Existing files are not overwritten. `--json` writes the canonical result to standard output; without it, standard output is a concise human rendering of the same result. When both are supplied, the same canonical result is written atomically to `--output` and rendered to standard output.

## Common execution contract

1. Resolve paths without following an untrusted repository into evaluator code.
2. Parse the role-specific governed inputs needed to establish expected identity.
3. Inspect the running distribution, interpreter isolation, entry point, package payload, and checkout separation before importing or executing repository-controlled Python.
4. Compare runtime and target identity with the role contract. Any mismatch terminates the operation.
5. Execute the fixed checks for that role in their specified isolation boundary.
6. Construct one canonical result from independently collected identities and check outcomes.
7. Write an evidence file atomically only when requested. A failing result may be retained, but it can never contain `passed = true`.
8. Exit zero exactly when the canonical result has `passed = true`; otherwise exit non-zero.

Every operation is read-only with respect to the inspected repository, Git refs, governance artifacts, environments, credentials, and external systems. It performs no network access. A temporary directory outside the target may be created and removed for isolated checks.

## Operation contracts

### `released-root`

- Running role: exact installed released evaluator.
- Target: a repository root with `.engineering-harness.lock` whose evaluator version, archive digest, and installed-payload digest match the running distribution.
- Required checks: isolated runtime identity, lock ownership, managed-file doctor, complete engineering-graph validation, and no-change proof for the target worktree.
- Independence: `released-evaluator` with respect to repository-controlled candidate code.
- Prohibited: a candidate checkout/archive target, an unlocked root, an external validator path, or importing target package code.

### `predecessor-view`

- Coordinator: the current successor CLI.
- External evaluator: the interpreter located by `--evaluator-python`; its expected version, archive digest, payload digest, and allowed entry point are derived from the governed release/predecessor transition inputs, not caller overrides.
- Target: a deterministic, contract-bound read-only view derived from `ROOT` for `--release-record` by the shared predecessor-view service. The result records source commit, release-record identity, view manifest schema, included-path digest, excluded-path digest, and view-tree digest.
- Required checks: successor input validation, exact external predecessor identity, deterministic view construction, view-manifest replay, predecessor doctor/validation through the approved predecessor entry point, and source/view no-change proofs.
- Independence: `external-predecessor`; the predecessor interpreter imports no successor/candidate package or repository module.
- Prohibited: caller-selected omissions, diagnostic allowlists, arbitrary scripts, view mutation after hashing, or describing a partial view as complete successor validation.

An immediate predecessor that predates `harnessctl qualify` may be invoked through its exact documented doctor/validator entry points by this coordinator only after external identity and view binding pass. This compatibility adapter is versioned and tested; it is not an untyped workflow escape hatch.

### `complete-candidate`

- Running role: candidate-source or candidate-package runtime bound to `--candidate-commit`.
- Target: the complete candidate checkout at `ROOT`.
- Required checks: candidate runtime identity, exact Git commit and clean tracked tree, candidate managed-template doctor where applicable, complete current engineering-graph validation, focused/full candidate contract checks selected by the workflow, and no-change proof.
- Independence: `candidate-controlled` in all output and retained evidence.
- Prohibited: claiming released-verifier assurance or using the result as predecessor/root compatibility evidence.

### `candidate-package`

- Running role: exact installed released verifier, isolated from the candidate checkout and candidate wheel.
- Target: a candidate wheel bound to the supplied commit and declared candidate digest.
- Required checks: released-verifier runtime and wheel identity, candidate wheel digest/name/version/metadata, safe archive structure, payload manifest, isolated installation, candidate installed runtime identity, disposable-repository smoke/doctor/validation, candidate acceptance contract, and cleanup/no-change proof.
- Independence: `released-verifier` for checks performed by the verifier. Candidate self-check output inside the disposable environment is nested and labelled candidate-controlled.
- Prohibited: adding the candidate wheel or checkout to the verifier interpreter's import path, executing candidate modules in the verifier process, or using a verifier digest that does not match the running released environment.

The existing `harnessctl accept-candidate` command may remain for one compatibility cycle as a thin alias to this handler. It must use the same parser validation, result schema, implementation, diagnostics, and exit semantics.

#### Initial 0.6.0 bootstrap exception

Public `se-harness==0.6.0` predates the `qualify` namespace but already owns the hardened `se-harness-functional-acceptance-v1` candidate contract. Until a released verifier containing this specification is available, candidate-package automation may invoke only that immutable distribution's existing `accept-candidate` command. Before invocation it shall independently bind the installed version, archive digest, installed-payload digest, entry point, isolation, candidate wheel digest, and candidate commit to the governed values.

The retained 0.6.0 output remains legacy bootstrap evidence. It shall preserve its original schema, shall not be wrapped or relabeled as `se-harness-release-qualification-v1`, and shall not claim that public 0.6.0 implemented `qualify candidate-package`. Any different verifier version, digest, scenario contract, executable, schema, or role fails closed. This exception adds no public option or sixth operation and expires when a released verifier exposes the typed command.

### `public-install`

- Running role: the exact clean environment installed from `--public-wheel`.
- Target: that installed distribution plus the released repository inputs identified by `ROOT` and `--release-record`.
- Expected identity: released version and distribution digests are taken from the immutable released record/manifest and must equal the supplied wheel digest, supplied payload digest, installed package identity, and runtime entry point.
- Required checks: wheel digest and archive structure, installed payload identity, version/entry-point identity, public CLI help/smoke surface, installed template/resource availability, released-record binding, and no source-checkout contamination.
- Independence: `public-install-observation`; it proves public bytes and installed behavior, not candidate acceptance or predecessor governance.
- Prohibited: downloading the artifact, accepting an unreleased record, importing the source checkout, or rewriting the installed environment.

Network acquisition and index provenance remain workflow responsibilities before this command. The command verifies only the already acquired exact wheel and installed environment.

## Canonical result

The result schema identifier is `se-harness-release-qualification-v1`. Its top-level object contains exactly:

- `schema`;
- `operation`;
- `passed`;
- `independence`;
- `evaluator`;
- `target`;
- `checks`;
- `authority`.

`evaluator` contains role, distribution/version, runtime payload/archive digests when available, entry-point kind, isolation flags, and a stable identity digest. `target` contains a fixed `kind`, role-specific immutable identities, and a stable target digest. `checks` is an ordered array of objects containing `id`, `passed`, `subject`, and a bounded deterministic message. `authority` is the constant `evidence-only; no lifecycle or external action authorized`.

Absolute environment paths may appear in interactive diagnostics only when needed to repair a local invocation; canonical retained JSON replaces them with role-relative subjects and stable digests. Secrets and unrelated environment contents never appear.

Decision-bearing fields exclude completion time, run ID, workstation path, temporary directory, and nondeterministic command output. Workflows may record hosted run identity in a separate evidence envelope.

## Workflow contract

Repository-owned automation shall map qualification claims as follows:

| Workflow purpose | Required operation | Required runtime |
| --- | --- | --- |
| released root health | `released-root` | evaluator matching target root lock |
| predecessor transition/publication preparation | `predecessor-view` | successor coordinator plus exact external predecessor |
| full candidate source/package self-check | `complete-candidate` | exact candidate runtime |
| independent candidate distribution assessment | `candidate-package` | exact released verifier isolated from candidate |
| post-publication installed smoke | `public-install` | clean exact public installation |

Candidate, predecessor-assessment, release, and publication workflows shall retain the canonical role result or its digest, except that the initial exact-public-0.6.0 candidate-package lane retains its distinct legacy bootstrap result. Workflow conformance tests inspect executable commands, environment selection, provenance inputs, artifact names, and the exact bootstrap identity; matching step prose alone is insufficient.

The candidate template for `.github/workflows/engineering-harness.yml` shall use the appropriate typed operations. The root installed `.github/workflows/engineering-harness.yml` remains unchanged and continues to run the exact 0.6 released workflow until a later upgrade transaction.

## Error and recovery behavior

Errors use stable role-prefixed identifiers grouped as parser, evaluator identity, target identity, trust-boundary, check, output, and no-change failures. The first identity or trust-boundary failure prevents substantive checks whose meaning would be invalid. Independent cleanup and no-change checks still run where safe.

A failed operation does not retry with a lower-level command, another interpreter, a different view, relaxed omissions, accepted diagnostics, or candidate code. Recovery requires correcting the invocation or governed inputs and running the same operation again.

## Security and privacy properties

- Treat wheels, archives, repositories, locks, manifests, release records, view manifests, entry points, Git metadata, and environment locations as untrusted.
- Reject archive traversal, symlink/hardlink escapes, duplicate members, case-colliding paths, invalid UTF-8 where text is required, malformed digests, ambiguous installed distributions, and import-path contamination.
- Spawn external evaluators with isolated Python, a minimal explicit environment, no `PYTHONPATH`, disabled user site, fixed working directory, and argument arrays without shell interpolation.
- Never import candidate/successor code into a released verifier or external predecessor process.
- Never echo tokens, credentials, package-index configuration, or arbitrary file contents.

## Performance and capacity

Qualification may be slower than a raw validator because identity and isolation checks are mandatory. Each operation runs its fixed expensive validation at most once per invocation, streams bounded subprocess output, and uses bounded hashing. Correctness and provenance take precedence over optimizing release-lane duration.

## Observability

Human output begins with the operation, independence class, evaluator identity summary, target identity summary, and final pass/fail. Failures name the stable check ID and subject. Workflows upload the canonical JSON using names containing the operation and candidate/release identity.

## Compatibility and migration

- Low-level commands remain supported for diagnostics and non-release consumers, but repository-owned release workflows stop treating their output as qualification evidence.
- `accept-candidate` is a temporary compatibility alias, not a sixth role.
- Immutable public 0.6.0 is a separately identified bootstrap predecessor of that alias: only its exact legacy acceptance result may be retained until the first typed released verifier exists, and that result is never represented as canonical qualification output.
- Exact pre-command predecessors are supported only through the contract-bound adapter inside `predecessor-view`.
- Existing released evidence and historical workflows are not rewritten.
- Root managed bytes and root lock stay unchanged until separately approved adoption.

## Explicitly unspecified decisions

Implementation may choose internal dataclass names, module-private helper boundaries, subprocess buffering, temporary-directory naming, and exact human formatting. It may not change the five operations, their trust boundaries, required identities, independence classifications, result fields, workflow mapping, or failure semantics without an approved amendment.
