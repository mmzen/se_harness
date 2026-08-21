# Migration note: the repository-context scaffold is withdrawn

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

This note describes a breaking change prepared under `WO-DST-021` and `REQ-DST-065`. It applies to the next release that carries the change; the exact version increment is a separate release decision and is not asserted here. This note is human-readable guidance and grants no approval, verification, or release authority.

## What changed

Repository-local operational facts now belong in the owner-controlled region of `AGENTS.md`. The harness no longer scaffolds, tracks, requires, parses, or reports a repository-context document.

| Surface | Before | After |
| --- | --- | --- |
| Installed seed | `docs/engineering/REPOSITORY_CONTEXT.md` was seeded on `init`, `adopt`, and upgrade | no seed; the path is never written |
| Lock | a `seed` entry with `present` or `removed` state | no entry and no tombstone |
| `doctor` and `preflight` required files | the path was a required installed file | the path is not checked |
| Readiness gate | diagnostics `C001`, `C002`, `C003`, and `C004` | the whole `C` family is retired and emitted by no code path |
| Preflight payload | carried a `repository_commands` object parsed from that file | the field is removed and is not emitted as an empty object |
| Preflight schema | `se-harness-preflight-v1` | `se-harness-preflight-v2` |
| Managed router `HRN-002` | named the repository-context document | names the owner-controlled region of `AGENTS.md` |
| Router routing table | routed repository facts to that document | routes them to the owner-controlled region of `AGENTS.md` |
| Router stop conditions | stopped when repository context was incomplete | that condition is removed; every other stop condition is retained |
| Workflow reference steps | a reference step could declare a `CTX-ACT-*` action identifier | that form is withdrawn and rejected before resolution |
| `init` guidance step 1 | directed the owner to complete the context document | directs the owner to record build, test, verification, ownership, and boundary facts in the owner-controlled region of `AGENTS.md` |

## What is not changed

- **An existing file at `docs/engineering/REPOSITORY_CONTEXT.md` is never written, moved, truncated, or deleted.** It becomes ordinary untracked owner content. Keep it, rewrite it, or remove it yourself; the harness has no opinion and reports nothing about it.
- The packaged `AGENTS.md` and `CLAUDE.md` fragments are unchanged, so the single managed destination and every tracked-block digest are unchanged.
- Every other seed keeps its behavior. `docs/engineering/README.md` remains a seed, and the `present`/`removed` state vocabulary remains valid for it.
- No other diagnostic family changes. `I001`, `A001`, `W001` through `W004`, and `W011` are retained.
- The upgrade transaction is unchanged: a customized or ambiguous managed file still blocks apply without a partial write.

## What you need to do

1. **Move your operational facts.** Put setup, build, test, lint-or-format, required-verification, entry-point, ownership, and boundary facts into the owner-controlled region of `AGENTS.md`, outside the `<!-- se-harness:begin -->` and `<!-- se-harness:end -->` markers. That region is owner content: the harness preserves it, never parses it, and never hashes it.
2. **Run the upgrade as usual.** `harnessctl upgrade <repository>` then, after owner authorization, `--apply`. The regenerated lock simply has no entry for the retired path. Upgrading a repository that had already deleted the seed produces the same lock as one that had not, so no ordering or cleanup step is needed.
3. **Stop relying on the readiness gate for context completeness.** A repository that was previously blocked only by unresolved context fields becomes ready with no owner action. If you want completeness enforced, state it as a governed requirement with its own verification contract, not as a scaffold field.
4. **Update any consumer of the preflight JSON payload.** A reader keyed on `repository_commands` must fail against the unrecognized `se-harness-preflight-v2` schema string rather than read a silent default. Check the `schema` value before reading fields.
5. **Update any tooling keyed on the `C` diagnostic codes.** They are no longer emitted. The `C` prefix is not reused for an unrelated family in this change.
6. **Check your workflow contracts for the withdrawn reference form.** A reference step declaring a `CTX-ACT-*` action identifier now fails conformance with a diagnostic naming the withdrawn form. A reference step declares exactly one `procedure_id`. This form had no use in the shipped or candidate contracts, so no ordinary repository is expected to be affected.

## Why

A harness-tracked scaffold implied that the harness could gate the quality of repository-local facts it does not own and cannot evaluate. It could only check that placeholder text had been replaced. The cost was a second always-loaded file, a parser over repository-authored text whose values were echoed into a report, and a readiness gate that blocked work for a reason outside harness authority. Routing those facts to the region an owner already controls removes the file, the parser, the gate, and the payload field without losing anything the harness could actually assure.

See [installation and safe upgrades](harness-installation-and-upgrades.md) for the upgrade transaction itself, and the [`harnessctl` command reference](harnessctl-reference.md) for command actors and side effects.
