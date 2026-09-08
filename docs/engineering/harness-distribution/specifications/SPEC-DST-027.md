+++
id = "SPEC-DST-027"
type = "specification"
title = "Wave 5 managed template hygiene: the workflow's failure surface, header and pins, the gitignore markers, the environment inventory"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The managed workflow fails with the evaluator's own refusal, pins its actions and describes what it runs; the gitignore block uses comment markers; every environment variable read is specified."

[relations]
specifies = ["REQ-DST-072", "REQ-DST-073", "REQ-DST-074", "REQ-DST-075"]
+++

# Specification: Wave 5 managed template hygiene: the workflow's failure surface, header and pins, the gitignore markers, the environment inventory

## In plain words

One work order over the standard template and the installer: the managed
workflow surfaces refusals, says what it runs and pins what it uses. The
ignore file gets markers Git ignores, and the one undocumented environment
variable is written down.

## Scope

The managed template `engineering-harness.yml`, the installer's fragment
writer, the tests that pin them, and one amendment record on `SPEC-ECP-006`.
This repository's hash-locked root copies change only at the root adoption
of the carrying release. The repository-owned workflows are `SPEC-CIP-003`'s.

## Terms

- **Result file.** The JSON the scope or handoff check writes to stdout,
  which the managed workflow redirects to a file and reads.
- **Marker pair.** The two lines that open and close a managed block in a
  fragment-mode file: HTML comments, or hash-prefixed lines.

## Rules

**DST-MWF-001.** The two `check … --json` steps of the template MUST capture
the check's exit status and stderr instead of appending `|| true`.

**DST-MWF-002.** When the result file is empty or not JSON, the step MUST
print the captured stderr and fail with the check's exit status, never with
a decoder traceback.

**DST-MWF-003.** When the result file parses, the steps MUST evaluate it
exactly as today: `QGP-G4I-PATHS`, the outcome, the blockers and the declared
restitution digest.

**DST-MWF-004.** The template's header comment MUST name only steps the file
runs: evaluator install, live body read, work-order selection, review
preflight, scope and handoff check, released-root qualification, Explorer
generation and upload.

**DST-MWF-005.** Every `uses:` in the template MUST pin a full commit digest
with the exact tag in a trailing comment, the form `SPEC-CIP-003` CIP-ONE-006
fixes for the repository-owned workflows.

**DST-MWF-006.** `installer._block` MUST write the `.gitignore` block between
`# se-harness:begin` and `# se-harness:end`; the HTML-comment pair remains for
`AGENTS.md` and `CLAUDE.md`.

**DST-MWF-007.** `_extract_block` MUST keep accepting both marker pairs, so an
upgrade of a `.gitignore` written with HTML comments rewrites the block with
hash markers and preserves every byte outside it.

**DST-MWF-008.** That upgrade MUST classify the rewrite through the existing
fragment rule, with no new installer mode and no owner-content loss.

**DST-MWF-009.** `SPEC-ECP-006` MUST be amended by record: the test rehearsal
`ECP-DLG-004` exempts is a process with `SE_HARNESS_REHEARSAL=1` in its
environment, read by `gate_source.load_configuration`.

**DST-MWF-010.** `docs/notes/delegation-class.md` MUST name the variable
beside its `local-file` sentence.

**DST-MWF-011.** A test MUST pin the inventory of environment names read under
`se_harness/`, two today, and assert that each occurs in a specification
under `docs/engineering/`.

**DST-MWF-012.** Tests MUST pin rules 001 to 008: header versus steps, the
reader on an empty result, the pin form, the markers, and the rewrite of an
older fixture.

**DST-MWF-013.** This work MUST NOT change this repository's hash-locked root
`engineering-harness.yml`, the root `.gitignore` block, the lock or any other
root managed byte.

**DST-MWF-014.** The root-adoption work order of the carrying release MUST
take the new template and the hash-marked block into the root; it MAY drop
the root `.gitignore` lines duplicating the fragment.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| the check refuses with nothing on stdout | the step prints the refusal and exits with the check's status | the check's own code, such as `MG005` or `RID002` |
| the check writes a result that does not complete | as today: blockers printed, step fails | `outcome` and `blocked_by` |
| a header names a step the file lacks | the header test fails naming the step | test failure |
| a `uses:` line lacks the pin form | the pin test fails naming the line | test failure |
| an upgrade meets a `.gitignore` with both marker pairs | `_extract_block` refuses as duplicated markers, nothing written | `HarnessError` |
| a module reads a variable no specification names | the inventory test fails naming it | test failure |

## Examples

**Given** a consumer whose evaluator refuses the scope check with `MG005`,
**when** the managed lane runs, **then** the log ends with the `MG005`
message and the step fails (DST-MWF-001, DST-MWF-002).

**Given** a repository initialized by released 0.16.0, **when** the
candidate's `upgrade --apply` runs, **then** its `.gitignore` block carries
hash markers and the owner lines are unchanged (DST-MWF-007, DST-MWF-008).

**Given** the amended `SPEC-ECP-006`, **when** the inventory test runs,
**then** `SE_HARNESS_REHEARSAL` and `GITHUB_TOKEN` each occur in a
specification (DST-MWF-009, DST-MWF-011).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-DST-072` | DST-MWF-001, DST-MWF-002, DST-MWF-003, DST-MWF-012, DST-MWF-013, DST-MWF-014 |
| `REQ-DST-073` | DST-MWF-006, DST-MWF-007, DST-MWF-008, DST-MWF-012, DST-MWF-013, DST-MWF-014 |
| `REQ-DST-074` | DST-MWF-004, DST-MWF-005, DST-MWF-012, DST-MWF-013, DST-MWF-014 |
| `REQ-DST-075` | DST-MWF-009, DST-MWF-010, DST-MWF-011 |

## Not decided here

- The shell shape that captures status and stderr: a status variable and a
  stderr file, or a wrapper function.
- The digests chosen for the three pins and how the test verifies the tag.
- Whether the header's step list is one sentence or a list.
- Where the inventory test lives and how it discovers environment reads.
- The wording of the amendment record and of the note sentence.

## Compatibility and migration

A consumer whose `.gitignore` block carries HTML markers receives the hash
markers at the next `upgrade --apply`. A consumer who edited inside the block
is blocked as customized, as for any fragment. A consumer's own copy of the
managed workflow is hash-locked and follows the same upgrade.
