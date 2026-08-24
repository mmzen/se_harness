+++
id = "REQ-REB-023"
type = "requirement"
title = "Accept a real POSIX virtual environment as an evaluator entry point"
status = "draft"
owners = ["requirements-steward", "repository-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an evaluator-identity boundary receives the interpreter path of an ordinary virtual environment whose final path component is a terminal interpreter link, THE SYSTEM SHALL treat that lexical path as the environment entry point, derive the environment root from it without dereferencing, and continue identity verification."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Accept a real POSIX virtual environment as an evaluator entry point

## Rationale

On POSIX, `python -m venv` normally creates `<env>/bin/python` as a symbolic link to the system interpreter. The virtual environment is the execution boundary that supplies the installed distribution, its templates, and its entry points; the link target is a shared system binary that belongs to no environment.

Identity code that resolves the interpreter before deriving the environment root therefore computes the wrong root, and code that forbids any link on the interpreter path refuses the only interpreter such an environment has. Release 0.6.0 recorded both failures: a valid isolated released evaluator was rejected and its root was reported as the system prefix. The documented bootstrap sequence in `docs/engineering/REPOSITORY_CONTEXT.md` and `AGENTS.md` instructs operators to build exactly that environment, so the defect makes the governing path unusable on POSIX rather than merely inconvenient.

## Preconditions and trigger

The trigger is any evaluator-identity boundary that receives an external interpreter path and must establish an environment root, an entry point, and an installed distribution before trusting the runtime. This includes the released-evaluator identity command, released-root and predecessor qualification, release bootstrap binding, predecessor preparation, predecessor assessment, predecessor publication, and governance-migration runtime probes.

## Required response

- The environment root shall be derived from the lexical interpreter path with the user prefix expanded and the path made absolute, and with no symbolic-link or junction resolution applied to any component.
- A final path component that is a symbolic link shall be accepted when every enclosing directory is an ordinary directory and the resolved target is an ordinary existing file.
- Identity comparison of an interpreter path against an expected interpreter path shall compare the two lexical paths, not their resolved targets.
- Normalizing an accepted interpreter for retained evidence shall preserve its position inside the declared environment root and shall not substitute the resolved target.
- A binary interpreter that is an ordinary file with no link on its path — the normal Windows case — shall remain accepted under the same rule with no separate code path.
- Acceptance shall not depend on the platform name, on an environment variable, on a directory name such as `bin` or `Scripts`, or on the interpreter file name.

## Failure and boundary behavior

- The rule accepts a link only as the final component. Every unsafe path form remains a refusal under `REQ-REB-024`; this requirement widens nothing beyond the terminal interpreter link.
- An interpreter path with fewer than two parent components has no derivable environment root and is refused rather than defaulted to the filesystem root.
- Accepting the entry point establishes no other identity fact. Version, distribution origin, template origin, entry point, payload digest, isolation, and checkout separation continue to be verified independently, and any of them may still fail.
- No acceptance under this requirement authorizes a lifecycle change, a mutation of an installed root, a release, a publication, or a governor adoption.

## Constraints

- The accepted entry point is a path fact only. It never becomes a capability token and never substitutes for an approved decision.
- Retained evidence shall not contain a personal or workstation-specific absolute path.

## Acceptance examples

### Example: normal behavior

**Given** a POSIX virtual environment at `<env>` created by `python -m venv`, in which `<env>/bin/python` is a symbolic link to a system interpreter outside `<env>`, holding the exact released `se-harness` distribution

**When** an evaluator-identity boundary is given `<env>/bin/python`

**Then** the environment root is `<env>`, the entry point is `<env>/bin/harnessctl`, the interpreter identity is recorded as `<env>/bin/python`, and identity verification proceeds to its remaining checks.

### Example: failure behavior

**Given** the same request where `<env>/bin/python` names a path that does not exist

**When** the boundary validates the interpreter

**Then** it refuses with a stable diagnostic identifying the missing interpreter and performs no substantive validation of any target.
