+++
id = "SPEC-DST-021"
type = "specification"
title = "Retire the repository-context scaffold and readiness gate"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-DST-065"]
+++

# Specification: Retire the repository-context scaffold and readiness gate

## Scope

This specification defines the installation, upgrade, readiness, and reporting behavior that satisfies `REQ-DST-065`. It covers the seed template, the lock entry, the preflight required-path and policy-path sets, the context parser and its diagnostic family, the preflight report payload, and the `init` guidance sequence.

It excludes the managed instruction router, the packaged instruction fragment, and the workflow procedure schema, which `SPEC-IAR-013` owns. It excludes this repository's own `AGENTS.md` owner region, which `SPEC-IAR-012` owns.

## Actors and external systems

- The repository owner, who runs installation and owns every seeded and owner-editable path.
- The standard installer, operating in `init`, `adopt`, and `upgrade` modes.
- The readiness evaluator, invoked as `preflight` for the `start` and `review` phases.
- The integrity evaluator, invoked as `doctor`.
- Downstream consumers of the machine-readable preflight payload.

## Inputs

- The template tree at `templates/repository/standard/`, enumerated by the installer.
- An existing `.engineering-harness.lock`, schema 1 or 2, possibly holding a `seed` entry for `docs/engineering/REPOSITORY_CONTEXT.md` with `state` of `present` or `removed`.
- The target repository worktree, which may or may not contain that path.
- A work-order identifier and phase for readiness evaluation.

## Outputs

- A regenerated lock with no entry for the retired path.
- A preflight report, rendered and machine-readable, carrying no repository-command block and no context diagnostic.
- Installation guidance naming the owner-controlled region of `AGENTS.md`.

## State model

Three repository states are recognized, and all three converge:

| Prior lock entry | File on disk | After upgrade |
|---|---|---|
| absent | absent | no entry, no file |
| `seed`/`present` | present | no entry, file byte-identical |
| `seed`/`present` | absent | no entry, no file |
| `seed`/`removed` | absent | no entry, no file |

Convergence is the invariant: the post-upgrade lock is identical across all four rows, so repeated upgrades are idempotent and no row is distinguishable afterwards.

## Behavioral rules

1. Delete `templates/repository/standard/docs/engineering/REPOSITORY_CONTEXT.md.seed`. The installer discovers seeds by the `.seed` suffix while enumerating the template tree, so removing the file removes the scaffold with no installer code change.
2. Do not add a replacement seed, template, or generated path for repository-local operational facts under any name.
3. Regenerate the lock from the current template item set, as the installer already does. The retired path receives no entry and no tombstone. Do not add a mechanism to retain one.
4. Never write, move, truncate, or delete an existing file at the retired path. An existing file becomes ordinary untracked owner content.
5. Remove `docs/engineering/REPOSITORY_CONTEXT.md` from `REQUIRED_PATHS`. Presence is no longer an installation check and no longer contributes an `I001` diagnostic.
6. Remove `docs/engineering/REPOSITORY_CONTEXT.md` from `POLICY_PATHS`. The reading manifest is otherwise unchanged and retains its existing order and de-duplication.
7. Remove the context parser and its constants: `CONTEXT_FIELDS`, `COMMAND_KEYS`, `UNRESOLVED_CONTEXT`, `_parse_context`, and the `context_path` construction and diagnostic extension in `run_preflight`.
8. Retire the entire `C` diagnostic family. `C001`, `C002`, `C003`, and `C004` are no longer emitted by any code path. Do not reuse the `C` prefix for an unrelated family in this change.
9. Remove `repository_commands` from `PreflightReport`, from `to_dict`, and from the rendered report. Do not emit the field as an empty object.
10. Advance the report schema to `se-harness-preflight-v2`. A consumer keying on `repository_commands` must fail against an unrecognized schema rather than read a silent default from a `v1` payload that no longer carries the field.
11. Retain every other diagnostic family unchanged: `I001`, `A001`, `W001` through `W004`, and `W011`.
12. Replace step 1 of the `init` guidance sequence so it directs the owner to record build, test, verification, ownership, and boundary facts in the owner-controlled region of `AGENTS.md`. Renumber the remaining steps without changing their content.
13. Preserve the existing seed machinery for every other seed. `docs/engineering/README.md` remains a seed with unchanged behavior, and the `present`/`removed` state vocabulary remains valid for it.
14. Preserve the transactional upgrade guarantee. If the lock cannot be written atomically, abort with no partial writes.

## Error and recovery behavior

- An upgrade that cannot enumerate the template tree, cannot write the lock atomically, or cannot identify the installed evaluator fails without retaining any file, per existing behavior.
- A worktree containing an unreadable file at the retired path is not an error, because the path is no longer read.
- A schema-1 lock upgrades through the existing compatibility path. The retired entry is simply absent from the regenerated map; no legacy-canonical comparison applies because no digest was ever recorded for a seed.
- Recovery from a partially applied upgrade is unchanged and is governed by the existing bounded-recovery behavior.

## Data and interface contracts

- `se-harness-preflight-v2` is the new report schema identifier. Its object differs from `v1` by the absence of `repository_commands` and by no other field.
- The lock `files` map contract is unchanged. Seed entries retain `{"mode": "seed", "state": "present"|"removed"}` for seeds that still ship.
- `REQUIRED_PATHS` and `POLICY_PATHS` remain ordered tuples of repository-relative POSIX paths.
- The retired diagnostic codes are a removal from a published surface and belong in the release migration note.

## Security and privacy properties

- Removing a parsed owner-authored file removes an untrusted-input surface from the readiness path. The retired parser read a repository-controlled file and echoed field values into the rendered report and the JSON payload; that echo path is withdrawn.
- No new file is read, written, or executed. No path escapes the target root.
- Withdrawing the presence gate does not weaken managed integrity, which never covered this path's content.

## Performance and capacity

One file read and its line scan are removed from every preflight invocation. No measurable capacity change is expected or required.

## Observability

- The rendered preflight report loses its repository-command section and gains nothing.
- `doctor` output loses one checked path.
- The upgrade change report shows no entry for the retired path, because the installer visits only current template items.

## Compatibility and migration

- Breaking. Release as a minor version with a migration note covering: the withdrawn seed, the retired `C` diagnostic family, the removed `repository_commands` field, and the report schema advance to `v2`.
- A repository whose preflight passes today continues to pass, whether it keeps or deletes its context file.
- A repository blocked today solely by unresolved context fields becomes ready without any owner action.
- Consumers parsing the preflight payload must handle `v2`. This is the only consumer-visible break.

## Examples and counterexamples

- Example: a fresh `init` produces a repository with no `docs/engineering/REPOSITORY_CONTEXT.md`, a lock with no entry for it, and a passing start preflight for an approved work order.
- Example: an `upgrade` of a repository whose context file holds owner facts leaves the file byte-identical and drops the lock entry.
- Counterexample: emitting `"repository_commands": {}` under schema `v1`. Rule 9 and rule 10 forbid it, because a consumer cannot distinguish a repository with no commands from a harness that stopped collecting them.
- Counterexample: shipping a smaller seed with only the five command fields. Rule 2 forbids it. Narrowing the scaffold is a different change and does not satisfy `REQ-DST-065`.
- Counterexample: deleting an owner's existing context file during upgrade "to complete the retirement". Rule 4 forbids it absolutely.

## Explicitly unspecified decisions

- The exact wording of the replacement `init` guidance step, subject to rule 12's required content.
- The internal ordering of the constant removals and whether the context parser is deleted in one edit or several.
- Test module names and placement, subject to `VER-DST-021`.
- The migration note's prose, subject to its required content.
