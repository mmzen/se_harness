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

Setup uses existing Python outside the project.

## Scope

Plugin readiness; SPEC-PLG-001 supplies the verified wheel.

## Terms

- **Private environment.** Installation in persistent plugin data.
- **Expected identity.** Version, payload digest and archive digest derived from the independently verified bundled wheel, never the unchecked installation.

## Rules

**PLG-ENV-001.** Setup MUST establish Python 3.11+, usable `venv`, and usable `ensurepip` before creation.

**PLG-ENV-002.** Missing prerequisites MUST produce guidance without downloading or installing Python or changing the repository.

**PLG-ENV-003.** Authorized setup MUST create its private environment outside the checkout in selected persistent plugin data.

**PLG-ENV-004.** Installation MUST recheck the bundled wheel against its trusted digest and install offline without indexes, dependencies or source builds.

**PLG-ENV-005.** Readiness MUST verify expected identity through existing checks and require observed `evaluator_archive_sha256` present and equal; supplied `evaluator_wheel_sha256` alone proves no observation.

**PLG-ENV-006.** Governed use MUST invoke verified absolute environment Python with `-I -m se_harness`, matching the repository lock.

**PLG-ENV-007.** Setup MUST reuse matching verified environments and refuse incomplete, mismatched or ambiguous installations.

**PLG-ENV-008.** Repository upgrades MUST follow the separately authorized target-evaluator procedure; plugin updates cannot change the lock silently.

**PLG-ENV-009.** Setup MUST discover explicit Python using host or shell facilities before Python-dependent components.

**PLG-ENV-010.** Evaluator subprocesses MUST clear `PYTHONPATH` and put the verified environment's `bin` or `Scripts` first in controlled `PATH`.

**PLG-ENV-011.** Identity commands MUST supply `--expected-version`, `--evaluator-payload-sha256`, `--evaluator-wheel-sha256`, `--expected-root ENV_DIR`, and `--entry-point` identifying the environment's installed entry point.

**PLG-ENV-012.** Setup MUST require neither manual activation nor system `PATH` changes.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing Python support | Stop before creation | Prerequisite and remedy |
| Interrupted install | Remain unavailable | Incomplete setup |
| Identity or archive observation fails | Refuse readiness | Existing diagnostic or missing/mismatched archive |

## Examples

**Given** absent archive metadata, **when** readiness runs, **then** PLG-ENV-005 refuses plugin readiness.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-003` | PLG-ENV-001, PLG-ENV-002, PLG-ENV-009 |
| `REQ-PLG-004` | PLG-ENV-003, PLG-ENV-004, PLG-ENV-007, PLG-ENV-012 |
| `REQ-PLG-005` | PLG-ENV-005, PLG-ENV-006, PLG-ENV-007, PLG-ENV-008, PLG-ENV-010, PLG-ENV-011 |

## Not decided here

- Directory names, repository initialization and host activation.
- Core identity semantics remain SPEC-REB-001/011/015 and REQ-REB-028; the archive observation requirement applies only to plugin-managed readiness.
