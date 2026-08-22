+++
id = "SPEC-REB-007"
type = "specification"
title = "Publication predecessor-view validation contract"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
specifies = ["REQ-REB-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T17:29:44Z"
decided_by = "technical-owner"
+++

# Specification: Publication predecessor-view validation contract

## Scope

This specification defines one repository-owned, read-only adapter for publication gates that must combine complete current validation with exact predecessor validation of the already governed two-omission view. It applies to the initial release resolver, release-bound Pages build, and standalone Pages recovery validation points.

## Actors and external systems

- Trusted main supplies publication policy, released RLS, view/evaluator evidence, and current validator.
- Git supplies exact commit, tree, blob, sparse-worktree, and clean-state identity.
- External released 0.5.0 supplies `doctor` and `validate` observations only.
- Existing publication resolvers validate RLS history, tag, evaluator binding, and distribution.
- Privileged GitHub, maintenance, PyPI, and Pages jobs remain downstream and separate.

## Inputs

One clean committed repository, selected released RLS ID, external evaluator interpreter and entry point, and its already downloaded exact wheel. Every path, metadata value, Git object, evidence byte, process output, and environment value is untrusted until checked.

## Outputs

Canonical JSON identifies governance commit/tree, selected RLS/candidate/version, exact omitted descriptors and sparse digest, complete-graph counts, predecessor-view counts, commands, and a zero-source-change result. It contains no credential or host-specific persistent path.

## State model

```text
trusted main + released RLS
  -> resolve and replay canonical RLS/view/evaluator bindings
  -> validate complete graph with current semantics
  -> derive exact two-path view at governance commit
  -> run isolated predecessor doctor + validate in view
  -> prove complete source unchanged and revalidate
  -> allow existing privileged jobs
```

## Behavioral rules

1. Select the RLS by exact canonical ID and require `status = "released"`.
2. Derive the rejected pair from current typed relations, then require equality with the RLS-bound preparation-view descriptors and canonical sparse digest.
3. Create the view only from the exact clean HEAD and local Git objects; accept no caller-supplied omission or sparse pattern.
4. Candidate validation runs on the complete source before and after predecessor execution.
5. Predecessor commands run externally with isolated environment, no credential variables, and the view as their only checkout root.
6. Require predecessor `doctor` success and a valid `validate --json` report with zero errors.
7. Prove the view omits exactly two tracked paths and source status/tree/history bytes remain unchanged.
8. Plan and execution are read-only; output may be written only to an explicitly bounded path outside artifact discovery.
9. All three publication validation points use the same adapter and semantics.
10. Any failure prevents every downstream privileged job and supports safe idempotent retry after correction.

## Error and recovery behavior

Fail on dirty state, non-HEAD input, unsupported object format, changed sidecar or history, wrong RLS/version/candidate, unsafe path, Git configuration substitution, runtime contamination, timeout, malformed JSON, nonzero predecessor report, checkout mutation, or cleanup ambiguity. The only recovery is correction followed by a fresh complete transaction.

## Data and interface contracts

The CLI accepts `--repository`, `--release-record`, `--evaluator-python`, `--evaluator-entry-point`, `--evaluator-wheel`, optional `--output`, and `--json`. Its closed JSON schema uses canonical UTF-8/LF and sorted set-like values. Caller input cannot name omitted paths or expected errors.

## Security and privacy properties

Credential-bearing environment variables are removed from child processes. The adapter rejects linked/escaped repositories and tools, alternate Git state, evidence substitution, and unexpected files. It never contacts a network or performs Git writes outside its temporary isolated clone/worktree metadata.

## Performance and capacity

Execution is bounded by existing artifact/evidence limits and process timeouts. It performs two complete candidate validations and one predecessor `doctor`/`validate` pair per publication validation point.

## Observability

Human output distinguishes complete-current validation from predecessor-view validation. Retained JSON records exact identities and counts without claiming that 0.5.0 parsed omitted history.

## Compatibility and migration

This is repository publication tooling only. It does not alter the packaged candidate, portable templates, managed root, formal history, tag, RLS, distribution, public interfaces, or consumer behavior.

## Examples and counterexamples

- Conforming: current main validates completely; 0.5.0 validates a view omitting only exact rejected `REL-SEH-008` and `RLS-SEH-009`.
- Non-conforming: ignore E009/E010 while continuing publication.
- Non-conforming: delete or move rejected history, or run predecessor against an arbitrary caller-supplied sparse view.
- Non-conforming: skip complete-current validation because the predecessor view passed.

## Explicitly unspecified decisions

Temporary names, internal dataclasses, and workflow step labels are delegated. Trust direction, exact omissions, three call sites, canonical evidence replay, and fail-closed behavior are fixed.
