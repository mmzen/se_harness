+++
id = "VER-RLO-004"
type = "verification"
title = "Verify complete recipe binding and exact hosted replay"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-27"

[relations]
verifies = ["REQ-RLO-013", "REQ-RLO-014", "REQ-RLO-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:01:04Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Verify complete recipe binding and exact hosted replay

## Independence

Verification derives expected fields and failure cases from `REQ-RLO-013`, `REQ-RLO-014`, `REQ-RLO-017`, and `SPEC-RLO-004`, not from production parser constants. Schema fixtures independently enumerate required and forbidden fields. Hosted evidence must be produced after the exact candidate commit and must compare against already accepted RLS hashes; the replay cannot generate its own expected values.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-013 | canonical schema matrix | complete recipe, each missing/extra/duplicate/wrong-type field, size and encoding bounds | only the exact canonical v1 shape passes; all failures occur before candidate execution |
| REQ-RLO-013 | producer identity matrix | immutable/mutable images, OS, architecture, CPython patch, pointer width, observed image identity | only exact declared and observed Linux/amd64 OCI and CPython identities pass |
| REQ-RLO-013 | toolchain and environment matrix | complete direct/transitive lock, altered hash, omitted/extra package, inherited/undeclared variables | exact lock and installed inventory pass; drift fails before project build |
| REQ-RLO-013 | command and normalization matrix | argument arrays, tokens, working directories, shell strings, arbitrary executable, altered normalizer contract | only closed supported steps execute; unsafe or drifting forms fail without output |
| REQ-RLO-013 | bundle/RLS binding | matching and mismatching candidate, version, source, epoch, recipe, filenames, hashes; injected atomic-write failure | schema 2 binds exactly once; replay is idempotent; every failure leaves the RLS unchanged |
| REQ-RLO-013 | compatibility and product boundary | released schema 1, new ready schema 1, built wheel, initialized/upgraded consumer | released history remains valid; new ready schema 1 is refused; no repository recipe policy reaches portable surfaces |
| REQ-RLO-014 | local exact replay | two clean candidate exports and producers using one accepted schema-2 manifest | A equals B and both wheel/sdist hashes equal the accepted values; result binds all identities |
| REQ-RLO-014 | hosted pre-release replay | exact candidate commit, ready RLS, one dispatch input, retained result | hosted no-credential lane reproduces both accepted bytes and retains exact pass evidence before release decision |
| REQ-RLO-014 | hosted failure replay | changed recipe/tool/environment/normalizer/output hash and unavailable producer | each run fails without RLS edit, hash update, lifecycle transition, credential, or external mutation |
| REQ-RLO-014 | production-policy conformance | schema-2 and historical schema-1 workflow paths | schema 2 uses only the shared interpreter; schema 1 is isolated and labeled legacy; privileged jobs execute neither path |
| REQ-RLO-017 | export byte matrix | export from clones with `core.autocrlf` false, true, and input, a clone with `core.eol=crlf`, and a path carrying a `text eol=lf` attribute | every exported file equals its committed blob bytes in every clone |
| REQ-RLO-017 | source mode matrix | POSIX export, non-POSIX bind-mount presentation, and an incoming tree already carrying wrong modes | the tree the producer builds from carries `0o775` directories and `0o664` files in every case; failure to establish it fails before the first recipe command |
| REQ-RLO-017 | host-independence rebuild | full replay of `RLS-SEH-015` on a POSIX host and on a Windows host, plus the negative control with the mode response removed | both hosts reproduce the bound wheel and sdist identities; the negative control reproduces neither |

## Acceptance scenarios

1. Build an exact candidate twice with the reviewed canonical recipe and retain the accepted bundle-v2 manifest outside the checkout.
2. Prepare one synthetic or phase-appropriate ready RLS and atomically bind its schema-2 distribution without changing core fields or status.
3. Replay the RLS locally in two fresh producers and compare both outputs with the accepted hashes.
4. Commit the exact candidate separately from later governance/evidence, dispatch the hosted pre-release lane on the review ref, and retain its candidate/RLS/recipe-bound result.
5. Repeat with one controlled mismatch in each identity class and prove no expected-value update or external action occurs.
6. Resolve historical `RLS-SEH-012` through the schema-1 compatibility path and prove its bytes and metadata remain unchanged.
7. Replay an already released recipe-bound record from a non-POSIX host and from a POSIX host and prove both reach the bound identities, then remove each half of the host-independence response in turn and prove each removal breaks the reproduction.

## Property and invariant tests

- Canonical recipe bytes have one SHA-256 identity across LF checkouts.
- Every accepted path is safe, candidate-relative where required, and symlink-contained.
- All required recipe fields are present exactly once and all unknown fields fail.
- Every installed build distribution appears exactly once in the hash-locked inventory; no undeclared distribution is tolerated.
- Build subprocess environments equal the declared allowlist plus documented interpreter-internal paths.
- Recipe text never reaches a shell evaluator.
- Builds A and B share no mutable source, tool, cache, raw-output, normalized-output, or temporary directory.
- Replay expected hashes are immutable inputs and never become outputs or writable fields.
- Bundle and RLS recipe identities are equal and resolve to candidate-tree bytes.
- Exported candidate bytes equal committed blob bytes independently of clone configuration.
- The source tree a producer builds from carries the declared mode set independently of host filesystem mode semantics.
- Technical evidence performs no lifecycle or external action.

## Static and architecture checks

Confirm one repository parser/interpreter implementation is imported by manifest creation, distribution binding/validation, hosted pre-release replay, and schema-2 production qualification. Confirm schema-2 workflow YAML contains no `python -m build`, tool installation list, environment recipe, or direct normalizer invocation. Confirm all workflow actions are full-SHA pinned, the pre-release lane accepts one RLS input, and no portable package or managed consumer path imports repository recipe code.

## Security and privacy checks

Exercise duplicate JSON keys, oversized input, invalid UTF-8, control characters, absolute/traversal/backslash/symlink paths, mutable image references, malicious tokens, executable substitution, newline and option injection, hostile archive members, environment injection, subprocess timeout, output flooding, tool hash mismatch, extra files, and cleanup failure. Inspect hosted permissions, environments, secret references, checkout credential persistence, OCI mounts, caches, and uploaded artifacts.

## Performance and resilience checks

Measure two clean builds without correctness-dependent cache. Prove bounded JSON, logs, archive sizes, subprocess time, and cleanup. Inject failure before producer start, during tool installation, during each build, during normalization, during comparison, and during evidence write; no partial accepted bundle or RLS mutation may survive.

## Manual assessments

- Review the exact OCI digest, CPython patch, and full lock inventory against the current qualified toolchain.
- Review declared environment values for completeness and absence of secrets or host identity.
- Review command arrays and normalizer fields against actual invoked arguments.
- Review the workflow job/permission/environment matrix and schema-1 isolation.
- Review the final diff against issue #110 and confirm native Linux/Windows rehearsal remains issue #111.

## Evidence retention

`REQ-RLO-017` evidence is retained under `docs/engineering/release-orchestration/evidence/WO-RLO-008/`: the export-byte and source-mode readings, both host replays of `RLS-SEH-015` with their observed identities, the negative control, and the host-versus-container mode readings that decide where the mode response belongs. A reading taken before the commit under assurance is an analysis measurement and is re-taken at that commit.

Retain under `docs/engineering/release-orchestration/evidence/WO-RLO-004-verification.md`: candidate and governance commits, exact recipe/lock/image/package hashes, schema matrices, local build A/B identities, accepted hashes, hosted run URL and retained result digest, workflow permission analysis, historical compatibility result, package/consumer boundary observations, focused and full test commands/counts, formal validation, deviations, residual risks, and all unperformed lifecycle/external actions.

## Residual uncertainty

Public registries may stop serving already pinned image or package bytes. That is an availability failure, not permission to substitute bytes. Native host-runner path parity, virtual environments, shell behavior, and cleanup across Linux and Windows remain for issue #111.

The declared source mode set is flat, and that is correct only while no committed blob carries the executable bit. Every blob at the 0.7.0 candidate is mode `100644`, so the flat set is currently exact, but nothing in this contract detects the day that changes. A committed executable file would be silently demoted. `REQ-RLO-017` records the constraint; closing it with a check is not in this contract's coverage.

## Amendment record

**`REQ-RLO-017` coverage, three matrix rows, acceptance scenario 7, two property bullets, and one evidence-retention paragraph, accepted 2026-08-27 under `WO-RLO-008`.** This contract's coverage of the recipe replay was complete for declared identity classes and silent about the source input those classes are compared through. Its local and hosted replay rows compare outputs against accepted hashes, which is exactly the comparison that does catch a host-dependent export — but only after a first build has already been accepted with the fault in it. No row exercised the export or the source modes directly, so no reading available before acceptance could distinguish a correct build from the one bound to `RLS-SEH-014`.

The rows and scenario added above close that gap, and scenario 7's negative control is the part that matters: removing each half of the response in turn is what proves each half is load-bearing rather than defensive.

The amendment adds obligation and relaxes no pass condition. No row is removed, renumbered, or reordered; no pass condition is weakened; no waiver is introduced; and the independence rule stands — the new rows derive their expected values from the committed tree and from already bound record identities, never from the code under test.

Accepted at approval rather than during implementation, because `QG-G1-DEFINITION` requires the coverage to exist before `WO-RLO-008` is eligible. The accountable repository owner accepted it with the companion `SPEC-RLO-004` and `ARCH-RLO-004` amendments on 2026-08-27 over the framing recorded in `WO-RLO-008`.
