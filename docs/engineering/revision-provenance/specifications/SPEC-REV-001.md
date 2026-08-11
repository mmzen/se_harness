+++
id = "SPEC-REV-001"
type = "specification"
title = "Commit-bound verification and release provenance"
status = "implemented"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-REV-001", "REQ-REV-002", "REQ-REV-003", "REQ-REV-004", "REQ-REV-005", "REQ-REV-006", "REQ-REV-007", "REQ-REV-008"]
+++

# Specification

## Formal records

`verification_record` uses `VREC-`, status `ready`, `verified`, or `released`, and requires `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, `evidence_paths`, `verifies_work_order`, and `conforms_to`.

`release_record` uses `RLS-`, status `ready` or `released`, and requires `version`, `commit`, `git_object_format`, `released_at`, `authorized_by`, `satisfies`, `includes_verification`, and `releases_work`.

Full commit values are lowercase hexadecimal with length 40 for `sha1` and 64 for `sha256`. Active verification records require `worktree_state = "clean"`, a 64-character lowercase snapshot SHA-256, and non-empty repository-contained evidence paths. Release and included verification commits and object formats must agree. Relation targets must have the specified formal artifact types.

## CLI

`capture-verification <root> --id VREC-nnn --work-order WO-nnn --verification VER-nnn --evidence <path> [--output <path>]` resolves a clean full `HEAD`, generates the current dashboard snapshot when absent, validates referenced IDs and evidence, and writes a `ready` Markdown record atomically. It never runs artifact-body commands or changes Git state.

`prepare-release <root> --id RLS-nnn --release-contract REL-nnn --verification-record VREC-nnn --work-order WO-nnn --version <value> --authorized-by <owner> [--tag <value>] [--output <path>]` reads a verified or ready verification record, copies its commit and object format, verifies consistent relations, and writes a `ready` record atomically. It does not create or verify a tag, authorize release, or publish.

Both commands refuse an existing output and contain output and evidence paths below the repository. ISO timestamps are UTC with a `Z` suffix. Generated records include human-readable bodies explaining that status transition remains an accountable decision.

## Dashboard

The snapshot includes structured `revision_provenance` entries for every parsed verification and release record: record ID, kind, declared commit, observed revision, match state (`exact`, `different`, or `not_assessable`), related work orders, and release version. Formal nodes and declared edges remain in the normal graph, enabling requirement-to-commit traversal.

Derived findings cover active verified work without a verification record, released work without a release record, declared commit mismatch, dirty active verification, and checkout drift. The observed repository revision is always labeled derived, never authoritative.

## Compatibility

Configuration schema becomes 2 for newly installed or safely upgraded unmodified configuration. Existing artifact types remain valid. The two new types are optional unless a repository chooses to retain a commit-bound verification or release instance. Upgrade follows the existing hash ownership rules.
