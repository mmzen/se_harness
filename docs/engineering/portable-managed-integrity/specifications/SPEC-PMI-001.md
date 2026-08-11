+++
id = "SPEC-PMI-001"
type = "specification"
title = "Portable managed-file digest and lock migration contract"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-PMI-001", "REQ-PMI-002", "REQ-PMI-003", "REQ-PMI-004", "REQ-PMI-005", "REQ-PMI-006", "REQ-PMI-007"]
+++

# Specification: Portable managed-file digest and lock migration contract

## Scope

Define canonical integrity for all current UTF-8 managed files and managed fragments, an explicit schema-2 lock, conservative schema-1 compatibility, and consistent behavior across init, adopt, upgrade, doctor, source verification, and packaged installation.

## Actors and external systems

- Repository operators invoke `harnessctl` commands.
- Git and filesystems may present LF, CRLF, or CR line endings.
- The harness distribution supplies canonical rendered text templates.
- Assurance and release owners consume diagnostics but retain lifecycle authority.

No network service participates in hashing or migration.

## Inputs

- Target root and contained managed paths.
- Management mode: `managed`, `fragment`, `seed`, or `generated`.
- Raw target bytes and, for fragments, the uniquely delimited managed block.
- Rendered desired standard-template bytes.
- `.engineering-harness.lock` schema, tool version, modes, paths, and digests.

## Outputs

- Deterministic SHA-256 digests and comparison classifications.
- A schema-2 lock after successful init, adopt, or applied safe upgrade.
- Doctor results identifying unchanged, legacy-compatible, customized, missing, or malformed entries without file bodies.
- Upgrade actions that preserve customized content and either migrate safe entries or retain legacy evidence.

## State model

### Schema 1: legacy raw-byte evidence

Absence of a hash-mode declaration selects the historical schema-1 behavior: complete managed files hash exact bytes, while fragments reproduce the former extraction rule that normalized CRLF to LF before hashing. Schema-1 evidence is never silently reinterpreted as schema-2 canonical evidence.

### Schema 2: canonical UTF-8 text evidence

The lock declares:

```json
{
  "schema": 2,
  "hash_algorithm": "sha256",
  "hash_mode": "utf8-text-lf-v1",
  "tool_version": "<version>",
  "files": {}
}
```

Every hashed `managed` or `fragment` entry uses the declared canonical mode. `seed` entries continue to record presence state rather than a managed digest. The schema reserves future entry-level modes but this change introduces no binary-managed mode.

## Behavioral rules

1. `utf8-text-lf-v1` validates strict UTF-8, converts every CRLF sequence to LF, converts each remaining CR to LF, preserves every other code point and the presence or absence of a final newline, re-encodes UTF-8, and computes lowercase SHA-256.
2. Canonicalization applies to the complete rendered bytes for `managed` entries and only to the extracted block bytes for `fragment` entries. Owner text outside a fragment is never included.
3. Init and adopt write schema 2 and compute every digest through the shared integrity component after the target content has been written successfully.
4. Doctor reading schema 2 computes the recorded canonical mode and fails missing, malformed, invalid-text, unsupported-mode, or digest-mismatched entries.
5. Doctor reading schema 1 first accepts the historical entry digest, including former fragment CRLF handling. If that evidence differs but the current tracked content is canonically identical to the currently rendered desired template or fragment, it may report a passing `legacy canonical match` advisory recommending upgrade. It remains read-only.
6. Upgrade reading schema 2 uses canonical comparison for old-versus-current and current-versus-desired classifications. Newline representation alone never yields `customized` or an unnecessary rewrite.
7. Upgrade reading schema 1 accepts an exact legacy raw match. It may also treat current content canonically identical to desired content as safe and unchanged. Any other mismatch remains customized; its file and old entry are preserved.
8. After a fully successful applied init, adopt, or upgrade, the lock writer emits one complete schema-2 lock atomically. A failure before replacement leaves the previous lock intact.
9. Unsupported schema numbers, algorithms, modes, malformed digests, duplicate paths, escaping paths, invalid fragments, and invalid UTF-8 fail closed with bounded diagnostics.
10. All callers use one shared implementation for canonicalization, digesting, schema interpretation, and comparisons. CLI surfaces do not maintain independent hash rules.
11. The self-repository lock is regenerated through the same supported lock writer or an equivalently tested deterministic entry point; hand-entered digests are prohibited.
12. Integrity commands never execute target content, print content bodies, change Git state, or grant verification or release authority.

## Error and recovery behavior

Planning and doctor are read-only. Applied operations validate the complete plan before mutation and use existing atomic-write semantics. Customized or ambiguous legacy entries remain untouched with their prior evidence. Operators recover by reviewing customization, adopting desired content explicitly, and rerunning a safe upgrade; they do not edit digest values to suppress diagnostics.

## Data and interface contracts

Existing CLI command names and required arguments do not change. The lock is deterministic JSON with sorted file keys, a final newline, schema 2, SHA-256, and `utf8-text-lf-v1`. Diagnostics add mode-aware reason text but preserve bounded exit-code behavior.

## Security and privacy properties

- SHA-256 strength is unchanged.
- Only line terminators are canonicalized.
- Strict UTF-8 prevents ambiguous byte interpretation.
- Paths remain repository-contained and symlink-safe.
- File bodies, credentials, and unrelated owner content are never emitted.
- Canonical equivalence cannot authorize overwrite when desired-content equality is absent.

## Performance and capacity

Hashing remains linear in tracked bytes with bounded memory appropriate to the existing template-sized files. No network access, background service, cache, or concurrency is required.

## Observability

Doctor and upgrade-plan output identify lock schema/mode and distinguish exact legacy match, canonical match, customized content, missing content, malformed evidence, and unsupported mode. Tests and retained evidence record both raw and canonical digests for diagnostic fixtures.

## Compatibility and migration

- Schema-1 locks remain readable.
- Exact legacy matches behave as before.
- Safe canonical equality to the current desired template enables migration without content rewrite.
- Ambiguous legacy mismatches remain manual review.
- Existing standard installation, templates, provenance commands, and record formats remain compatible.
- Schema-2 writers become the only source of new locks after adoption.

## Examples and counterexamples

- LF `a\nb\n`, CRLF `a\r\nb\r\n`, and CR `a\rb\r` are canonically equal.
- `a\nb` and `a\nb\n` are not equal because final-newline presence is content.
- Two spaces and one space are not equal.
- Unicode NFC and NFD forms are not normalized and remain different.
- A legacy mismatch is not declared newline-only merely because canonicalizing the current bytes changes its digest.

## Explicitly unspecified decisions

The implementation agent may choose module and helper names, internal result types, and exact advisory phrasing. It may not alter schema names, canonicalization semantics, safe-migration proof, or authority boundaries without an approved artifact change.
