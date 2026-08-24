+++
id = "ADR-HBI-001"
type = "adr"
title = "Declared hash-bound class registry with fail-closed completeness assessment"
status = "draft"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-HBI-001"]
+++

# ADR: Declared hash-bound class registry with fail-closed completeness assessment

## Status

Proposed. Nothing in this record authorizes implementation, a lifecycle
transition, a commit, a push, a pull request, a governor adoption, a
publication, a deployment or any external action.

## Context

`ADR-REB-003` already decided *how* to preserve hash-bound bytes: a narrow
versioned `text eol=lf` attribute, with validator hashing left strict. It
explicitly rejected normalizing evidence before hashing, because that would
weaken the exact-byte trust contract and would accept noncanonical worktree
bytes. That decision stands and this record does not reopen it.

What no record decides is *completeness*: which files carry the obligation, where
that answer lives, and what happens when it is missing. Today the answer is
distributed across a managed attribute fragment, an owner-controlled attribute
block, and an explicit newline argument at one write site, with nothing relating
them. `.engineering-harness.lock` is hash-bound, declared nowhere, and hashed
under two different rules by two callers.

So the decision here is narrower than `ADR-REB-003` and orthogonal to it: where
the declaration lives, and how its absence fails.

## Decision drivers

- Make "what governs this file's bytes" answerable from versioned content alone.
- Detect an undeclared hash-bound file when it is added, not at the release that
  depends on it.
- Preserve exact-byte trust for classes that have it, and preserve every recorded
  historical digest unrewritten.
- Deliver rules that consumer repositories need through the canonical template,
  without imposing repository-specific rules on them.
- Fail closed, so an unassessable condition can never read as a pass.
- Avoid a repository-wide line-ending rewrite.

## Considered options

1. **Keep hand-maintained attributes and rely on review.** Rejected. This is the
   status quo, and it already failed: the lock has been hash-bound and
   undeclared through multiple reviews, a release incident and a governor
   upgrade. Review discipline is not a mechanism.
2. **Add a repository-local test only, with no declaration in the harness.**
   Rejected. It would protect this repository and no consumer installation, the
   assertions would restate path lists a test cannot deliver to a target, and
   `doctor` would still report a healthy installation whose bound bytes are
   unprotected.
3. **Declared class registry inside the harness with fail-closed completeness
   assessment.** Selected. One data declaration answers class, mode and required
   attribute; one resolver and one mode arbiter serve every caller; three named
   `doctor` checks fail closed on absence, ineffectiveness or mode divergence.
   `template`-region classes reach consumer installations through the canonical
   template.
4. **Normalize all committed text before hashing, removing the need for
   attributes.** Rejected, and not ours to reject afresh: `ADR-REB-003` already
   decided this for evaluator evidence. Applying it universally would relax
   exact-byte trust precisely where the release chain depends on it.
5. **Mark hash-bound text as binary.** Rejected for the reason
   `ADR-REB-003` gave: this content is governed text, and binary treatment
   obscures the intended canonical LF semantics while breaking diffs and review.

## Decision

Declare committed hash-bound text classes as harness-owned data. Each class
declares its path patterns, its mode of exactly `raw` or `utf8-text-lf-v1`, the
bindings depending on it, its declaration region, and the required Git attribute
when the mode is `raw`. Resolve a path to exactly one class by most-specific
match, and fail closed rather than defaulting.

Assess completeness through three named read-only `doctor` checks —
`hash-bound-class-declared`, `hash-bound-attribute-effective` and
`hash-bound-mode-consistent` — using the existing `InstallationCheck`
convention rather than a new diagnostic code family. Resolve attributes as Git
would; never accept `.git/info/attributes`, global attributes or `core.autocrlf`
as satisfying a requirement.

Assign the three existing classes explicitly. `evaluator-evidence` and
`governance-migration-protocol` remain `raw` with `text eol=lf`, unchanged.
`.engineering-harness.lock` becomes `utf8-text-lf-v1`, because its content is
governed JSON whose own managed-file digests are already canonical, because one
of its two existing callers already canonicalizes it, and because canonical mode
removes the need for an attribute rather than adding one that would change
worktree bytes on every existing Windows checkout.

Place the completeness assessment in `doctor` and not in the validator. Checkout-
byte effectiveness is a property of an installed working tree, not of the
artifact graph; and a validator rule would not bind this repository's own
required gate until a separately authorized governor upgrade, which would leave
the defect live for exactly as long.

## Consequences

### Positive

- One reviewable declaration replaces three unrelated mechanisms.
- An undeclared hash-bound file, an overridden attribute and a two-mode class
  each become a named failing check.
- The two existing `raw` classes keep their exact-byte contract untouched.
- Consumer installations inherit the byte rules they need and none of this
  repository's specifics.
- The lock's two-mode divergence resolves without adding an attribute, so no
  existing checkout's worktree bytes change.

### Negative and migration cost

- `se_harness/upgrade_authorization.py` changes from raw to canonical comparison.
  That is the only behavioural change to an existing comparison, and it means
  `WO-HUP-002`'s recorded `prior_lock_sha256` is recognized through documented
  legacy newline-variant comparison rather than by direct equality.
- The declaration is delivered through the canonical template, so changing a
  `template`-region class later is a template change with the usual candidate,
  parity and installation-lock consequences. This is deliberately difficult to
  reverse.
- Adding a genuinely new hash-bound file now costs a declaration edit. That cost
  is the point.
- The three checks do not bind this repository's required CI gate until a
  separately authorized governor upgrade. Until then they protect through
  `doctor`, candidate CI and the test suite only, and that limit must be stated
  wherever the work is reported.

### Operational and security consequences

- A conflicting more-specific attribute makes a class ineffective and fails.
- Unreadable attributes, unavailable Git, untracked declared paths and invalid
  UTF-8 all fail closed; none is advisory.
- No historical digest is recomputed, corrected or repointed, and a legacy-variant
  match is always reported distinctly rather than silently.
- Assessment executes no repository-provided code and interpolates no repository
  content into a shell.
- Every lifecycle transition, commit, branch, credential and external action
  remains separately authorized.

## Validation

Execute `VER-HBI-001`. Require isolated fresh-checkout matrices under
`core.autocrlf` values `true`, `input` and `false` for each `raw` class; LF, CRLF,
CR, invalid-encoding and tamper cases per class; a static check that the
declaration contains no import, expression or command; byte-identical parity
between candidate source and the canonical template fragment for
`template`-region classes; a mode-divergence test that fails when one class is
hashed two ways; and proof that `WO-HUP-002`'s recorded digest is still
recognized without being rewritten.
