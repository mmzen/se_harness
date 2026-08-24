+++
id = "REQ-HBI-001"
type = "requirement"
title = "Declare and enforce a byte rule for every committed hash-bound text file"
status = "approved"
owners = ["repository-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a committed text file's bytes are bound by a recorded SHA-256, THE SYSTEM SHALL resolve that file to a declared hash-bound class carrying an explicit byte rule, and SHALL fail closed when a raw-mode class has no effective versioned Git attribute preserving those bytes."
verification_method = "automated-cross-platform-checkout-test"

[relations]
derives_from = ["CAP-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "repository-owner"
+++

# Requirement: Declare and enforce a byte rule for every committed hash-bound text file

## Rationale

`ADR-REB-003` chose the right mechanism and applied it to one path class. The
mechanism does not generalize by itself, and nothing detects its absence
elsewhere. `.engineering-harness.lock` demonstrates the consequence: it is
hash-bound, it has no attribute, and every existing check passes.

A declaration without enforcement is a comment. Enforcement without a
declaration cannot say what it is enforcing. This requirement therefore obliges
both, and obliges them to agree.

## Preconditions and trigger

- A file is tracked in Git and its bytes are bound by a SHA-256 recorded in a
  governed artifact field or supplied as an authorization input.
- `doctor` evaluates an installed repository, or a test evaluates candidate
  source.
- Git attributes are resolved from versioned repository content in effect for
  that working tree.

## Required response

- Resolve the file to exactly one declared hash-bound class. Each class declares
  its path patterns, its hash mode, the bindings that depend on it, and, when the
  mode is raw, the Git attribute required to preserve its bytes.
- Report a named failing check when a hash-bound file resolves to no declared
  class.
- Report a named failing check when a raw-mode class's required attribute does
  not resolve effectively for its paths, including when a more specific
  conflicting attribute overrides it.
- Span both `.gitattributes` regions. Classes that must reach consumer
  installations are declared in the canonical template fragment; repository-
  specific classes are declared in owner-controlled content. Completeness is
  assessed over the union.
- Preserve every existing digest, comparison and safety check unchanged. The
  obligation adds assessment; it removes none.

## Failure and boundary behavior

A missing, broadened, overridden or ineffective attribute fails. An undeclared
hash-bound file fails. A declaration naming a path that is not tracked fails. An
unreadable `.gitattributes`, an unavailable Git attribute resolution, or invalid
UTF-8 in a text-mode class fails closed with a bounded path-level detail; none of
these is ever reported as a pass.

Canonical-mode classes require no attribute and their absence is not a failure,
because `utf8-text-lf-v1` normalizes line endings before hashing.

Local or global Git configuration is never formal authority. No recorded digest
is recomputed, rewritten or repointed. No lifecycle transition, credential use,
publication, deployment or governor adoption follows from this requirement.

## Constraints

Declarations are data: no import path, expression, shell command or repository-
provided executable appears in a class declaration. Path patterns use
repository-relative POSIX form. Assessment is read-only and deterministic for a
given working tree and attribute state.

## Acceptance examples

### Example: normal behavior

**Given** a repository whose declared classes cover `docs/engineering/**/evidence/*.json`
as raw mode requiring `text eol=lf`,

**When** `doctor` runs on a checkout where that attribute resolves effectively,

**Then** the class-declared and attribute-effective checks pass and the evidence
digests match their bound values under LF, CRLF and CR checkout configurations.

### Example: failure behavior

**Given** a new committed text file whose SHA-256 is recorded in a work order and
which matches no declared class,

**When** `doctor` runs,

**Then** the class-declared check fails naming that exact path, and the process
exit status is non-zero.

**Given** a raw-mode class whose required `text eol=lf` is overridden by a more
specific conflicting attribute,

**When** `doctor` runs,

**Then** the attribute-effective check fails naming the class, the resolved
attribute and the conflict.

## Open decisions

None. `INT-HBI-001`'s open decision was answered on 2026-08-24 with `doctor
alone`, so this requirement is satisfied by a `doctor` assessment and a validator
plane rule is outside the packet.
