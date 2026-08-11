+++
id = "SPEC-DST-005"
type = "specification"
title = "Canonical artifact layout and safe authoring contract"
status = "implemented"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-DST-015", "REQ-DST-016", "REQ-DST-017", "REQ-DST-018"]
+++

# Specification: Canonical artifact layout and safe authoring contract

## Scope

Define the canonical per-domain layout, safe domain and artifact authoring commands, domain-aware verification and release-record placement, and backward-compatible diagnostics. The contract improves navigability and generation without making filesystem position a source of governance authority.

## Canonical domain layout

The domain root is `docs/engineering/<domain>/`. Formal artifact types map to paths relative to that root as follows:

| Artifact type | Canonical directory |
| --- | --- |
| `intent` | `intent/` |
| `capability` | `capabilities/` |
| `requirement` | `requirements/` |
| `specification` | `specifications/` |
| `architecture` | `architecture/` |
| `adr` | `architecture/adr/` |
| `verification` | `verification/` |
| `work_order` | `work-orders/` |
| `verification_record` | `verification-records/` |
| `release_contract` | `release/` |
| `release_record` | `releases/` |
| `operating_contract` | `operations/` |

Supporting work-order evidence belongs in `evidence/`, Gherkin feature files belong in `acceptance/`, and a domain index belongs at `README.md`. These supporting files are not formal artifacts unless their own format explicitly declares otherwise.

The canonical filename for a formal artifact is `<id>.md`. Artifact discovery, identity, lifecycle, relations, and authority continue to derive from parsed metadata, not the filename or directory.

## Domain and identifier validation

A domain slug must match `[a-z0-9]+(?:-[a-z0-9]+)*`, contain between 1 and 64 characters, and be accepted only as a single path component. Reject absolute paths, drive or UNC syntax, `.` and `..`, separators, control characters, trailing normalization ambiguity, and symlink or junction escape.

Reject names reserved by the repository control plane or common generated content, including `templates`, `evidence`, `verification-records`, `releases`, `.git`, `.idea`, `target`, and `node_modules`. The implementation may centralize and extend this denylist when required for safe behavior, provided documented valid domain slugs remain stable.

An artifact identifier must satisfy the existing identifier grammar, use the prefix registered for the requested formal type, and be safe as a single filename stem. Normalization must never silently turn invalid input into a different domain or identifier.

## `scaffold-domain` command

Initial interface:

```text
harnessctl scaffold-domain TARGET --domain DOMAIN [--title TITLE] [--dry-run]
```

The command shall:

1. resolve `TARGET`, the engineering root, domain root, and all planned paths;
2. validate that every destination remains inside the target repository and that the parent chain contains no escape or non-directory conflict;
3. plan the canonical directories and an owner-controlled domain `README.md` seed;
4. report the complete deterministic plan in dry-run mode without writing;
5. otherwise create missing directories and exclusively create the index when absent;
6. report already-valid directories without treating them as product facts or installed managed files.

An existing index is preserved byte-for-byte. A conflicting file, unsafe parent, invalid slug, or failed precondition aborts before any write. The implementation shall stage or order writes so a reported failure cannot leave a partial domain scaffold.

Because Git does not retain empty directories, later artifact creation must recreate its canonical parent safely. Successful scaffolding does not claim that any formal artifact, approval, or product decision exists.

## `create-artifact` command

Initial interface:

```text
harnessctl create-artifact TARGET --domain DOMAIN --type TYPE --id ID [--dry-run]
```

The command shall resolve the canonical template and destination from the registered formal type mapping. It shall perform all domain, type, identifier, prefix, root-containment, parent-chain, and conflict checks before writing. Dry-run prints the chosen template, destination, and draft outcome without modifying the repository.

On success, the command exclusively creates one UTF-8 Markdown artifact at the canonical path. It substitutes at least the stable ID, artifact type, current date fields, and `draft` status. It may substitute a safe default title only when the template explicitly supports that value. Owner, relation, statement, body, and other accountable prompts remain visibly incomplete until a human or coding agent fills them from authorized context.

The command must state that the artifact is an incomplete draft and must pass ordinary graph validation before approval. It must never overwrite a destination, infer an approval, choose related artifact IDs, transition lifecycle state, or declare the graph valid.

## Domain-aware provenance routing

Add `--domain DOMAIN` to `capture-verification` and `prepare-release`. Destination precedence is:

1. an explicit safe `--output` path;
2. an explicit validated `--domain`;
3. an unambiguous common domain inferred from all selected work-order artifact source paths;
4. the existing repository-wide default.

For a single resolved domain, verification records default to `<domain>/verification-records/<id>.md` and release records to `<domain>/releases/<id>.md`. For multiple domains, repository-wide work, missing source provenance, or ambiguity, use `docs/engineering/verification-records/<id>.md` and `docs/engineering/releases/<id>.md` respectively.

Inference inspects only the normalized first component below `docs/engineering/` for each selected work order and accepts both canonical `work-orders/` paths and legacy flat domain paths. Reserved repository-wide containers are not domains. Inference never uses an artifact title, ID prefix, relation target, or current working directory as a domain signal.

Explicit output and domain conflicts are resolved by output precedence, with a clear report of the effective destination. Existing safe-path, clean-tree, commit-binding, artifact-selection, release-gating, and exclusive-write controls remain unchanged.

## Compatibility diagnostics

The validator and `doctor` shall compare each supported formal artifact source path to its safe canonical path after metadata parsing. If they differ, emit one deterministic advisory diagnostic containing the artifact ID, actual path, and expected path.

The advisory is a warning-class observation that does not add to validation errors, change a command exit status by itself, exclude the artifact, or alter any graph result. Repository-wide verification records and release records are canonical when their selected work is aggregate, domainless, or cannot be attributed safely to one domain. Templates and other reserved non-domain material are excluded.

All existing recursive discovery remains in place. Metadata validation is performed before path advice so malformed artifacts are not assigned speculative destinations. Duplicate IDs, invalid types, broken relations, lifecycle violations, and provenance mismatches remain ordinary errors independent of layout.

## Installation, upgrade, and ownership

Fresh `init` and `adopt` installations shall include the canonical layout and command guidance in the managed shared contract or managed engineering documentation. The installed template set and package data must include the mapping needed by `create-artifact`.

Domain directories, domain indexes, and created artifacts are repository-owned. They are not added to the managed lock as distribution files. `upgrade` shall never enumerate, move, rewrite, delete, or canonicalize owner artifacts. Existing owner-controlled seed files remain subject to the current preservation rules; new seed wording applies automatically only when the seed is first created.

Migration of legacy paths is an explicit, separately governed repository change. Guidance may recommend quiescing other writers, validating before and after, using reviewable `git mv` operations, and preserving IDs and relations unchanged.

## Security and transactional behavior

Treat target paths, domain names, identifiers, existing directory entries, symlinks, junctions, templates, and repository content as untrusted. Resolve containment using the established safe-path primitives. Do not follow an existing link outside the target, write through a conflicting file, or perform an implicit overwrite.

Commands shall validate a complete plan before mutation and use exclusive creation or equivalent conflict-safe primitives. If a runtime failure occurs after a temporary resource is created, clean up only resources created by that invocation and never delete pre-existing repository content.

## Deterministic conformance

Implementation shall add standard-library tests for every formal mapping, valid and invalid domains and identifiers, prefix mismatches, traversal and link escapes, dry runs, existing destinations, failure atomicity, draft-only creation, single-domain and aggregate provenance routing, explicit-output precedence, flat-layout compatibility, advisory stability, aggregate-root exceptions, upgrade preservation, self-install parity, packaged-template parity, and public command guidance.

Temporary fixtures shall represent legacy consumer layouts. Tests and implementation work must not read from or write to an active consumer repository as a fixture.

## Explicitly unspecified decisions

Exact internal helper names, CLI report formatting, and the advisory code may vary. Interactive prompting, automatic repository-wide migrations, inferred product metadata, new installation profiles, and automatic approval are outside this contract.
