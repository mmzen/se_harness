+++
id = "SPEC-ECP-023"
type = "specification"
title = "Wave 2 primitives: process, front matter, integrity, closed sets, codes, and the wired contract tables"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Each shared primitive exists once in the package and is called everywhere it was copied, every recorded digest stays equal, and the four declarative contract tables replace their Python copies."

[relations]
specifies = ["REQ-ECP-034"]
+++

# Specification: Wave 2 primitives: process, front matter, integrity, closed sets, codes, and the wired contract tables

## In plain words

Three groups, each its own work order. The launcher and the parser; the
integrity primitives and the closed sets; the code registry and the four
contract tables read at run time.

## Scope

The package `se_harness/` and `repository_tools/`, which imports it. The
engine copies under `se_harness/engine/` stay for wave 3 (#378), because the
engine is not an import surface yet. The lane scripts under `scripts/` and
`.github/scripts/` stay standard-library only and are out of scope. Every
rule carries a keyword and an identifier a test can cite.

## Terms

- **Primitive.** One function or class that every caller of a family uses;
  a copy is any second implementation of the same behaviour.
- **Recorded digest.** A SHA-256 committed in a recipe, a lock, a record or
  an evidence binding, or pinned by a test.
- **Declarative section.** A table a contract JSON carries that a Python
  module also spells out today.
- **Contract copy.** A Python literal whose content equals a declarative
  section.

## Rules

**ECP-PRM-001.** `se_harness/_process.py` MUST provide `run(argv, ...)` and
`run_git(root, *args)` with a default timeout, `stdin=DEVNULL`, UTF-8
decoding and a bounded output.

**ECP-PRM-002.** Each launcher MUST catch `OSError` and `SubprocessError`
and raise the caller's exception class, passed as `error=`, with the
command named.

**ECP-PRM-003.** Every Git launch in the package and in `repository_tools`
MUST go through `run_git`; a launch site MAY override the timeout.

**ECP-PRM-004.** `se_harness/front_matter.py` MUST parse one artifact into
metadata and body, tolerating a BOM, CR and CRLF, with delimiters anchored
at line start.

**ECP-PRM-005.** Every front-matter read in the package and in
`repository_tools` MUST call that parser; a CRLF artifact MUST parse where
a copy refused it.

**ECP-PRM-006.** `integrity.py` MUST be the one home of `raw_sha256`,
`canonical_text_bytes`, `canonical_json_bytes`, `pretty_json_bytes`, the
duplicate-key hook and `atomic_write_bytes`.

**ECP-PRM-007.** `canonical_json_bytes` and `pretty_json_bytes` MUST take
`ensure_ascii` explicitly, so each caller keeps the bytes it wrote before.

**ECP-PRM-008.** `atomic_write_bytes` MUST write a sibling temporary file,
fsync it and replace the target; the three inline writers of
`workflow_compliance.py` MUST use it.

**ECP-PRM-009.** `repository_tools/json_bytes.py` MUST re-export the
integrity primitives, and `release_build.canonical_json_bytes` MUST be
renamed so recipe digests are unchanged.

**ECP-PRM-010.** Every inlined `\r\n` normalization in the package MUST
call `canonical_text_bytes`, so a lone `\r` canonicalizes the same way
everywhere.

**ECP-PRM-011.** One reader of `.engineering-harness.toml` MUST serve the
installer, the guard and the workflow, decoding `utf-8-sig`, and
`plan_transition` MUST read the policy once.

**ECP-PRM-012.** `workflow_contract.py` MUST be the only definition of the
checkpoint set and the definition-type set; `cli.py` and
`workflow_compliance.py` MUST import them.

**ECP-PRM-013.** `mode`, `action`, `checkpoint` and `phase` values MUST be
typed as `Literal` or `StrEnum` in the package.

**ECP-PRM-014.** One version grammar MUST serve both wheel-metadata parsers,
so `qualify public-install` and `qualify candidate-package` accept the same
wheels.

**ECP-PRM-015.** One subprocess environment builder MUST serve
`candidate_acceptance`, `release_qualification` and `upgrade_rehearsal`,
denying `PYTHONPATH` and user site the same way.

**ECP-PRM-016.** `se_harness/codes.py` MUST name every diagnostic code the
package raises as a constant, and no package module MAY spell a code as a
literal.

**ECP-PRM-017.** `CodedError(HarnessError)` MUST carry `code` and `message`,
and every coded refusal in the package MUST derive from it or expose the
same two attributes.

**ECP-PRM-018.** `repository_tools/diagnostic_code_index.py` MUST read the
package's codes from `codes.py` and MUST keep scanning the engine until
wave 3 moves it.

**ECP-PRM-019.** `gate_source.py` and `mutation_guard.py` MUST read the
delegated operations from `workflow_contract.json` `agentic_operations`, and
their contract copies MUST go.

**ECP-PRM-020.** `workflow_result.py` MUST read the schema-2 field set from
`restitution_fields`, and its contract copy MUST go.

**ECP-PRM-021.** The predicate aggregator MUST take its precedence from
`quality_gates_contract.json` `aggregation`, and its hard-coded order MUST
go.

**ECP-PRM-022.** The evaluator-evidence writer and the lock writer MUST hash
through `declared_digest` under the mode `hash_bound_classes.json` declares
for their paths.

**ECP-PRM-023.** A contract section that is read at run time MUST be
validated at load, and a missing or malformed section MUST refuse with one
code.

**ECP-PRM-024.** No recorded digest MAY change: recipes, locks, evidence
bindings, `CONTRACT_SHA256` and every digest pin in the suite MUST equal
`main`'s.

**ECP-PRM-025.** The contract JSON files and the candidate templates MUST
NOT change bytes under this specification.

**ECP-PRM-026.** Where an approved specification names a contract copy as
the operative table, it MUST receive a dated amendment record naming this
specification.

**ECP-PRM-027.** The duplication scan (`pylint --enable=duplicate-code`,
eight-line minimum) MUST report none of the seven cross-file blocks the
assessment recorded.

**ECP-PRM-028.** The suite's failure set MUST equal the baseline, and
`validate`, `doctor` and the hosted lanes MUST pass at every head.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| `git` is not on the path | `run_git` raises the caller's error naming the command; no traceback (ECP-PRM-002) | the caller's code |
| a launch exceeds its timeout | the same error names the timeout (ECP-PRM-002) | the caller's code |
| an artifact has a BOM or CRLF endings | the one parser reads it (ECP-PRM-004) | none |
| a contract section is missing or malformed | the loader refuses before any read (ECP-PRM-023) | `WEX-ECP-030` family |
| a code literal remains in a package module | the registry test names the module (ECP-PRM-016) | none |
| a recipe or lock digest differs from `main` | the release-qualification or hash-bound suite fails (ECP-PRM-024) | none |

## Examples

**Given** a CRLF checkout of this repository, **when** `harnessctl check`
reads a work order, **then** the front matter parses (ECP-PRM-005).

**Given** the candidate after group B, **when** `release_build` replays the
bound recipe of `RLS-SEH-025`, **then** the wheel digest is `a969d6ab…`
(ECP-PRM-009, ECP-PRM-024).

**Given** the candidate after group C, **when** `agentic_operations` loses
one entry in a throwaway copy, **then** the delegation gate refuses to load
(ECP-PRM-019, ECP-PRM-023).

**Given** the candidate after group C, **when** the code index regenerates,
**then** it equals the committed page and names no literal outside
`codes.py` and the engine (ECP-PRM-016, ECP-PRM-018).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ECP-034` | ECP-PRM-001, ECP-PRM-002, ECP-PRM-003, ECP-PRM-004, ECP-PRM-005, ECP-PRM-006, ECP-PRM-007, ECP-PRM-008, ECP-PRM-009, ECP-PRM-010, ECP-PRM-011, ECP-PRM-012, ECP-PRM-013, ECP-PRM-014, ECP-PRM-015, ECP-PRM-016, ECP-PRM-017, ECP-PRM-018, ECP-PRM-019, ECP-PRM-020, ECP-PRM-021, ECP-PRM-022, ECP-PRM-023, ECP-PRM-024, ECP-PRM-025, ECP-PRM-026, ECP-PRM-027, ECP-PRM-028 |

## Not decided here

- The default timeout and the output cap of `run`, provided every caller's
  current timeout is kept or raised.
- Which of the four version grammars serves both wheel parsers, provided the
  evidence names every wheel whose verdict changes.
- The exact `Literal` versus `StrEnum` choice per value set.
- Whether the three groups land as three pull requests or one stacked
  series; each work order is independent of the others.
