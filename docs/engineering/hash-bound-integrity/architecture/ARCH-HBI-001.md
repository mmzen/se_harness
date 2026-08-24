+++
id = "ARCH-HBI-001"
type = "architecture"
title = "One declaration boundary for committed hash-bound bytes"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-HBI-001", "REQ-HBI-002"]
conforms_to = ["SPEC-HBI-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["cross-cutting-policy", "security-privacy-or-trust-boundary", "difficult-to-reverse", "material-alternatives"]
rationale = "The architecture decides where the obligation to declare a byte rule lives, which component may answer what governs a file's bytes, and how absence fails. It binds every hashing call site across installer, upgrade authorization, mutation guard, release bootstrap and candidate acceptance, it governs exact-byte trust, its declaration reaches consumer installations through the canonical template and is therefore costly to reverse, and materially different alternatives exist including hand-maintained attributes, a repository-local test, and normalizing all committed text."
assessed_by = "technical-owner"
+++

# Architecture: One declaration boundary for committed hash-bound bytes

## Context and scope

Line-ending correctness for hash-bound text is currently a per-call-site
convention. Three mechanisms coexist: a managed attribute fragment for evidence
JSON, owner-controlled attributes for the migration protocol, and an explicit
`newline="\n"` at the dashboard manifest's write site. Nothing relates them, and
`.engineering-harness.lock` falls between all three while being hashed under two
different rules.

This architecture establishes one semantic boundary so that "what governs this
file's bytes" has exactly one answer, and so that adding a hashing caller cannot
introduce a second answer.

Scope is committed text whose bytes are hash-bound. Managed-file canonical
digests remain owned by `ARCH-PMI-001`; this architecture declares their mode and
changes nothing about how they are computed.

## Components and responsibilities

- **Class declaration:** harness-owned data enumerating hash-bound classes, their
  path patterns, mode, dependent bindings, declaration region and required
  attribute. It contains no executable expression.
- **Class resolver:** maps a repository-relative path to exactly one class by
  most-specific match, or fails closed. Sole authority for that mapping.
- **Mode arbiter:** answers the single question "which mode governs this path"
  for every hashing caller, delegating to the resolver. Returns an error rather
  than a default.
- **Attribute prober:** resolves Git attributes for a working tree as Git would,
  reports the resolved value, and never modifies configuration.
- **Assessment reporter:** renders the three named `doctor` checks with bounded
  details and drives the non-zero exit status.

## Dependency direction

Callers depend on the mode arbiter. The arbiter depends on the resolver; the
resolver depends on the declaration data. The prober depends on Git and on the
declaration, never on a caller. The reporter depends on the resolver and prober.

Nothing in the reverse direction exists: the declaration does not import the
resolver, the resolver does not import callers, and no caller imports the prober.
Integrity primitives in `se_harness/integrity.py` remain a leaf dependency of the
arbiter, not a peer of it.

## Data and control flow

`doctor` invokes the reporter, which enumerates declared classes, asks the
resolver for covered tracked paths, asks the prober for resolved attributes, and
emits three checks. A hashing caller passes a path to the arbiter, receives a
mode, and then calls the existing integrity primitive for that mode. No
component writes.

## Trust boundaries

Repository content and Git attribute output are untrusted input: parsed
defensively, never interpolated into a shell, never executed. Git configuration
is observed as context and is never authority. The declaration is trusted
harness-owned data delivered through the canonical template. Human lifecycle
authority is outside every boundary here; the architecture produces evidence
only.

## Required patterns

- One declaration, one resolver, one arbiter. Exactly one component may answer
  each of "which class", "which mode" and "which attribute resolved".
- Fail closed on every unknown, unreadable or unassessable condition.
- Declaration as data, delivered to consumers through the canonical template for
  `template`-region classes.
- Explicit LF at every producing call site for committed hash-bound text.
- Read-only assessment with bounded, path-level details.

## Prohibited patterns

- Call-site-local newline handling or a locally chosen hash mode.
- A default mode when resolution fails.
- Satisfying an attribute requirement from `.git/info/attributes`, global
  attributes or `core.autocrlf`.
- Recomputing, correcting or repointing any recorded digest.
- Executing repository-provided code or naming an executable in the declaration.
- Relaxing a `raw` class to canonical mode to make an assessment pass.
- A repository-wide line-ending rewrite.

## Quality attributes

Determinism: identical working tree, tracked set and attribute state yield
identical results. Portability: results depend only on versioned content and
resolved attributes, not on operator configuration. Diagnosability: every failure
names class, path, and observed versus required value. Reversibility of
assessment: the checks are read-only, so a wrong declaration is corrected by a
content change and never by repairing damaged state.

## Conformance checks

`VER-HBI-001` executes the contract. Static checks assert the declaration
contains no import, expression or command; that no caller computes a mode
locally; that `template`-region classes are byte-identical between candidate
source and the canonical template fragment; and that the three check names are
present and ordered. Isolated fresh-checkout matrices under LF, CRLF and CR
configurations prove effectiveness per `raw` class.

## Related ADRs

`ADR-HBI-001` records the coherent significant decision this architecture
implements: a declared class registry inside the harness with fail-closed
completeness assessment, in preference to a hand-maintained attribute list, a
repository-local test, or normalizing all committed text before hashing.
