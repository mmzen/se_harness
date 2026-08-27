+++
id = "SPEC-RLO-004"
type = "specification"
title = "Recipe-bound release build and replay contract"
status = "approved"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-27"

[relations]
specifies = ["REQ-RLO-013", "REQ-RLO-014", "REQ-RLO-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "engineering-owner"
+++

# Specification: Recipe-bound release build and replay contract

## Scope

Replace the current split identity—some facts in a release record and other facts handwritten in workflow YAML—with one repository-owned recipe that is bound by a new ready RLS and consumed by both hosted pre-release replay and production qualification.

This specification extends `SPEC-RLO-001` and respects the portable boundary in `SPEC-RLO-002`. It does not generalize build recipes into portable SE Harness, rewrite historical records, approve a release, or implement the Linux and Windows native rehearsal matrix in issue #111.

## Actors and external systems

- A release-work implementation actor uses the repository build interpreter to create accepted bytes and a bundle manifest.
- The repository binder attaches validated schema-2 distribution and recipe identity to one ready RLS.
- The quality owner reviews local and hosted replay evidence before an assurance or release decision.
- GitHub Actions provides a read-only hosted pre-release lane and the existing trust-separated publication workflow.
- A public immutable OCI registry supplies one digest-pinned Linux/amd64 producer image without credentials.
- The release owner retains the independent RLS decision; workflow success does not exercise it.

## Inputs

- One exact candidate commit and semantic version.
- Canonical candidate-tree file `release/build-recipe.json`.
- Canonical candidate-tree file `release/build-toolchain.lock` containing every installed Python build distribution with hashes.
- Exact accepted wheel and normalized-sdist bytes, or one ready RLS that already binds their names and hashes.
- For hosted pre-release replay, one `release_record` input and the hosting ref selected at dispatch.

No command accepts replacement platform, Python, tool, environment, epoch, normalization, command, filename, or expected-hash inputs when replaying an RLS.

## Outputs

- `se-harness-release-build-recipe/v1` canonical JSON in the candidate tree.
- `se-harness-release-bundle/v2` build manifest containing prior bundle fields plus the recipe schema, path, and SHA-256.
- Repository distribution schema 2 in the ready RLS with the same recipe binding.
- `se-harness-release-build-replay/v1` result containing resolved and observed identities, both build hashes, comparisons, and authority boundary.
- The existing exact wheel, normalized sdist, and `SHA256SUMS`; no additional public release asset is introduced by this work.

## State model

1. **Recipe declared:** canonical candidate bytes define one producer and build procedure.
2. **Candidate built:** the interpreter creates two independent outputs and proves internal equality.
3. **Bundle accepted:** exact hashes and recipe identity are retained in bundle schema 2.
4. **RLS bound:** the binder atomically writes distribution schema 2 to a ready RLS.
5. **Hosted replayed:** the read-only lane rebuilds from the RLS and retains exact or failed comparison evidence.
6. **Release eligible for decision:** technical replay is available for accountable review; no status changes automatically.
7. **Production replayed:** after a separate release decision, the existing publication qualifier consumes the same recipe before any privileged stage.

Historical schema-1 released records stay in a separate legacy replay state. A new ready record cannot enter that state.

## Behavioral rules

1. Recipe JSON must be UTF-8, LF-terminated, canonical key-sorted JSON with no duplicate keys and a bounded maximum size.
2. The exact recipe field set is closed and versioned. It contains `schema`, `producer`, `python`, `toolchain`, `environment`, `commands`, `normalization`, and `outputs`.
3. `producer` names one public OCI image by immutable digest plus exact `os = linux` and `architecture = amd64`. Floating tags, hosted-runner aliases, and host fallback are forbidden.
4. `python` names `CPython` and an exact three-part version. The interpreter must compare runtime implementation, version, pointer architecture, and platform with the recipe before installing tools or building.
5. `toolchain` binds the safe repository-relative lock path and raw SHA-256. The lock uses hash-required package entries for every direct and transitive Python distribution used to install or execute the build. The interpreter must compare the effective installed inventory with the declared inventory and reject extras or omissions.
6. `environment` has only fixed scalar values and declared derivations. `SOURCE_DATE_EPOCH` derives from the exact candidate commit timestamp. The producer starts with no host environment inheritance beyond the immutable image defaults; build subprocesses receive only the recipe allowlist and interpreter-required internal paths.
7. `commands` is an ordered array of typed steps. Each step declares an ID, argument array, working-directory token, and bounded path tokens. Shell strings, redirection, pipelines, command substitution, network commands, and arbitrary executables are forbidden.
8. The supported v1 steps install the locked toolchain, build wheel and raw sdist with `python -m build --wheel --sdist --no-isolation`, and normalize the raw sdist with the candidate-tree normalizer and recorded epoch. The repository interpreter, not workflow YAML, expands the bounded tokens.
9. `normalization` declares algorithm `se-harness-normalize-sdist/v1`, candidate path `scripts/normalize_sdist.py`, gzip level, archive format, member ordering, ownership, timestamp, PAX-header, and gzip-header expectations. The interpreter proves the declared path is present in the candidate tree.
10. `outputs` declares the version-derived universal wheel, normalized sdist, canonical two-line checksum file, and evidence schemas. Output directories must be fresh, outside the checkout, and contain no extra file.
11. The interpreter exports the exact candidate twice and launches two fresh producer instances. Reusing a tool environment, raw output, normalized output, cache, or source directory between A and B is forbidden.
12. Each producer instance may obtain only the digest-pinned image and hash-locked tool files. It receives no repository credential, publication credential, protected environment, secret, write token, or host build cache.
13. Bundle schema 2 contains all schema-1 identity fields plus `build_recipe_schema`, `build_recipe`, and `build_recipe_sha256`. The recipe path and bytes must resolve exactly at the candidate commit.
14. Distribution schema 2 contains the prior distribution fields plus the same three recipe fields. Binding requires bundle schema 2 and changes only that complete table in one ready RLS.
15. Repository validation accepts historical released schema-1 distribution records. It requires schema 2 for every recipe-era ready record and validates its candidate-tree recipe identity. No version-number allowlist or concrete-record exception defines the cutover.
16. The hosted pre-release workflow accepts one RLS ID, requires `status = ready`, derives every identity, runs with `contents: read`, and uploads only bounded replay evidence. It performs no lifecycle or external mutation.
17. The production qualifier uses the same interpreter for schema-2 records. Its existing legacy commands remain isolated and visibly selected only for historical released schema-1 records.
18. A replay passes only when build A equals build B byte-for-byte and both SHA-256 pairs equal the already bound RLS hashes. The interpreter never offers an update-expected mode during replay.
19. Workflow YAML may orchestrate checkout, artifact transport, and result upload, but must not restate producer, toolchain, environment, build, or normalization commands for schema-2 records.
20. Every error identifies the failed identity class and retains observed hashes when safe. Error handling must not leak environment contents, credentials, absolute host paths, or unbounded subprocess output.
21. Candidate export is host-independent. The interpreter exports the exact candidate with Git line-ending conversion disabled for that invocation, so the exported bytes equal the committed blob bytes in any clone. The source tree each producer instance builds from carries one declared mode set — `0o775` for directories and `0o664` for files — established from inside the producer boundary, because a non-POSIX host cannot retain a POSIX mode. No host platform, Git configuration, or filesystem fact reaches an accepted output.

## Error and recovery behavior

| Condition | Required behavior |
|---|---|
| Recipe absent or digest differs from candidate | fail before producer launch; no RLS write |
| Mutable image or wrong OS/architecture | fail recipe validation |
| Tool lock hash or installed inventory differs | fail before project build |
| Undeclared environment or command form | fail closed; do not execute the step |
| Build A and B differ | retain both hashes; fail |
| Builds agree but differ from accepted RLS | retain comparison; fail without updating RLS |
| Hosted producer cannot be acquired exactly | fail; no native-host fallback |
| Ready schema-1 record | fail forward-policy validation and require recipe-bound rebinding |
| Historical released schema-1 record | select labeled legacy publication replay without rewriting history |
| Exact schema-2 replay | retain pass evidence and make no formal or external change |
| Declared source mode set cannot be established inside the producer | fail before the first recipe command; no accepted output and no RLS write |

## Data and interface contracts

All JSON parsers reject duplicate keys, non-UTF-8 input, extra or missing fields, invalid scalar types, control characters, unsafe paths, and oversized documents. Paths are normalized repository-relative POSIX paths without absolute roots, `..`, backslashes, empty segments, or symlink escape.

Recipe and lock hashes identify raw canonical bytes. Candidate Git identity continues to use the repository object format. Output identity uses lowercase SHA-256. Command argument arrays are authoritative; rendered command text is observation only.

The build replay result records resolved recipe identity, image digest, observed OS/architecture, Python implementation/version, tool inventory, fixed/derived environment key names and non-secret values, normalized argument arrays, source manifest, both output hashes, expected output hashes, and exact comparisons. It does not retain the broader host environment.

## Security and privacy properties

- Candidate source, recipe, lock, archive members, JSON, paths, image metadata, tool packages, subprocess output, and RLS text are untrusted.
- Recipe parsing and RLS binding execute before candidate code.
- Candidate code and build backends execute only inside the no-credential producer.
- OCI and package identities are hash-pinned; no build credential or secret is introduced.
- Workflow expression values enter scripts through validated environment variables or argument boundaries.
- The interpreter uses argument arrays and bounded output capture, never a shell evaluation of recipe text.
- Privileged publication jobs continue to consume independently checked inert bytes and never execute the candidate or recipe.

## Performance and capacity

One replay launches two small producer instances and builds the repository twice. Recipe, lock, manifest, and result documents remain below 128 KiB each. Subprocess timeouts, output limits, and archive bounds are mandatory. Correctness does not depend on a cache; a cache may accelerate public immutable downloads only when every consumed byte is rehashed.

## Observability

Local and hosted results use the same replay schema and identify the exact candidate, RLS when present, recipe, toolchain, producer, and expected/observed hashes. GitHub retains the no-credential run and bounded result artifact. The result states that it is technical evidence and performs no verification or release decision.

## Compatibility and migration

- Do not edit `RLS-SEH-012` or any historical bundle, VREC, evidence, tag, or published byte.
- Distribution schema 1 and bundle schema 1 remain readable for already released history.
- Repository binder and documented preparation move forward to schema 2; new ready records require it.
- Portable `harnessctl`, standard release-record templates, consumer CI, and the packaged namespace remain format-neutral.
- Existing production publication retains a legacy branch for schema-1 replay while schema-2 uses the shared interpreter.
- Issue #111 may later add native Linux and Windows rehearsals. It must consume or compare against this same recipe and may not create another accepted-build identity.

## Examples and counterexamples

Valid: a ready RLS binds the exact candidate-tree recipe; hosted replay launches the declared OCI digest twice, proves the full tool inventory, and reproduces both accepted hashes.

Invalid: the RLS records only `SOURCE_DATE_EPOCH`, while workflow YAML chooses `windows-2022`, setup-python `3.11`, and three unconstrained packages.

Invalid: the recipe says `python:3.11`, `ubuntu-latest`, `setuptools>=68`, inherits all environment variables, or contains `python -m build && cp ...` as a string.

Valid legacy replay: the already released schema-1 `RLS-SEH-012` uses the isolated old path and is never described as recipe-bound.

## Explicitly unspecified decisions

The implementation agent may choose internal Python class and function names, temporary directory names, stable diagnostic codes, and test-fixture factoring. The initial exact OCI digest, CPython 3.11 patch, and locked package versions must preserve the currently qualified build contract and be explicit in the reviewed recipe; they are data under this specification, not a new architecture decision.

The agent may not change the recipe location, schemas, producer type, platform, complete-toolchain rule, environment closure, argument-array rule, two-build rule, new-record cutover, one-RLS hosted input, credential boundary, historical compatibility, or #111 scope boundary.

## Amendment record

**`REQ-RLO-017` coverage, rule 21, and one error row, accepted 2026-08-27 under `WO-RLO-008`.** As approved, this specification bound the producer platform, runtime, toolchain, environment, commands, normalization, and outputs, and said nothing about the bytes and modes of the source those commands build from. Rule 11 requires two independent exports and forbids shared state between them; it does not require either export to be independent of the host performing it.

`RC-070-01` (GitHub issue [#189](https://github.com/mmzen/se_harness/issues/189)) measured the consequence during the 0.7.0 release. The build of record was produced on a Windows workstation: `git archive` under `core.autocrlf=true` converted the exported text files, and the bind mount presented every entry to the producer as mode `0777`. Both builds were exported from the same host, so they agreed with each other and rule 18's internal comparison passed. 83 of 111 wheel entries carried CRLF and 69 were recorded executable. `RLS-SEH-014` was bound to those bytes and had to be rejected after hosted replay `33015517991` disagreed with them.

The amendment adds obligation and relaxes no pass condition. No rule is removed, renumbered, or reordered; no acceptance becomes a refusal or the reverse; no waiver is introduced; and the recipe field set, schemas, producer, toolchain, environment, command, and normalization contracts are untouched. The declared mode set is the set a POSIX export already produces, so no accepted byte of an existing record changes and the recipe digest every bound record names does not move.

This amendment was accepted at approval rather than during implementation, because `QG-G1-DEFINITION` requires the coverage to exist before `WO-RLO-008` is eligible. The accountable repository owner accepted it together with the companion `ARCH-RLO-004` and `VER-RLO-004` amendments, approved `REQ-RLO-017` and `WO-RLO-008`, and resolved that requirement's open decision by declining to retain a non-POSIX refusal, on 2026-08-27 over the framing recorded in `WO-RLO-008`.
