+++
id = "SPEC-PLG-002"
type = "specification"
title = "Provided Python and private evaluator setup"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Setup uses available Python to prepare an isolated evaluator from the supplied wheel, without network access or changes to the target repository."

[relations]
specifies = ["REQ-PLG-003", "REQ-PLG-004", "REQ-PLG-005"]
+++

# Specification: Provided Python and private evaluator setup

## In plain words

Setup prepares the checking tool using existing Python. Its files stay outside the project.

## Scope

This governs setup commands. SPEC-PLG-001 supplies the wheel; repository initialization and host activation remain separate.

## Terms

- **Private environment.** The isolated installation in persistent plugin data.

## Rules

**PLG-ENV-001.** Setup MUST establish Python 3.11 or newer, usable `venv`, and usable `ensurepip` before environment creation.

**PLG-ENV-002.** Missing prerequisites MUST produce installation guidance without downloading Python, installing Python, or changing the target repository.

**PLG-ENV-003.** Authorized setup MUST create its private environment outside the target checkout, beneath the host's selected persistent plugin-data directory.

**PLG-ENV-004.** Installation MUST use the supplied wheel offline, without indexes, dependency downloads, or source builds.

**PLG-ENV-005.** Setup MUST verify the installed release and payload through existing evaluator identity checks before making the environment available.

**PLG-ENV-006.** Governed use MUST invoke the verified absolute environment interpreter with `-I -m se_harness`, matching the repository lock.

**PLG-ENV-007.** Setup MUST reuse a matching verified environment and refuse incomplete, mismatched, or ambiguous installations.

**PLG-ENV-008.** Repository upgrades MUST follow the existing separately authorized target-evaluator procedure; a plugin update cannot silently change the repository lock.

**PLG-ENV-009.** Setup MUST discover an explicit Python path using host or shell facilities before invoking any Python-dependent plugin component.

**PLG-ENV-010.** Evaluator subprocesses MUST clear inherited `PYTHONPATH` and use controlled `PATH` with the verified environment's `bin` or `Scripts` directory first.

**PLG-ENV-011.** Identity commands MUST name `--expected-root ENV_DIR` and `--entry-point` pointing to that environment's pip-installed entry point.

**PLG-ENV-012.** Setup MUST require neither manual shell activation nor a system `PATH` change.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Python support missing | Stop before creation | Missing prerequisite and remedy |
| Installation interrupted | Keep the environment unavailable | Incomplete setup |
| Identity fails | Stop governed use | Existing identity diagnostics |

## Examples

**Given** supported Python, **when** setup completes, **then** PLG-ENV-005 establishes identity.

**Given** an incomplete environment, **when** readiness runs, **then** PLG-ENV-007 refuses it.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-003` | PLG-ENV-001, PLG-ENV-002, PLG-ENV-009 |
| `REQ-PLG-004` | PLG-ENV-003, PLG-ENV-004, PLG-ENV-007, PLG-ENV-012 |
| `REQ-PLG-005` | PLG-ENV-005, PLG-ENV-006, PLG-ENV-007, PLG-ENV-008, PLG-ENV-010, PLG-ENV-011 |

## Not decided here

- Internal directory names.
- New helpers or Python installation.
- Identity semantics: reuse SPEC-REB-001, SPEC-REB-011 rules 1–11, and SPEC-REB-015.
