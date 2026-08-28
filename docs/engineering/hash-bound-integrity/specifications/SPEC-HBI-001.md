+++
id = "SPEC-HBI-001"
type = "specification"
title = "Declared hash-bound text classes and fail-closed completeness assessment"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-28"

[relations]
specifies = ["REQ-HBI-001", "REQ-HBI-002", "REQ-HBI-003", "REQ-HBI-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "technical-owner"
+++

# Specification: Declared hash-bound text classes and fail-closed completeness assessment

## First amendment, 2026-08-28 — proposed

Proposed under `WO-HBI-005` for repository issue #207. Not yet accepted; the
rules below read as approved until the accountable technical owner accepts
this section, and `WO-HBI-005` must not be approved before that acceptance.

Rule 2 declared `governance-migration-protocol`, a `repository`-region class
whose three patterns name paths that exist only in this repository, and the
canonical fragment carried the same three rules into every consumer's managed
region. Rule 9 made "untracked declared path" fail closed for every class,
including `evaluator-evidence`, which a repository cannot satisfy before its
first verification record. Together they make `doctor` fail in every fresh
consumer repository after its first commit, contradicting `VER-HBI-001`
acceptance scenario 7.

The amendment changes three rules and adds none:

- **Rule 2** declares exactly two classes: `evaluator-evidence` and
  `standard-lock`, as before. `governance-migration-protocol` is withdrawn from
  the shipped table. The `implementation_sha256` binding it carried moves to
  `unbound_digest_fields` with the reason that it is bound in harness data and
  pinned by this repository's owner-controlled `.gitattributes` content, so an
  unclaimed digest field is still refused. No recorded digest changes.
- **Rule 9** keeps every listed fail-closed condition, and qualifies one:
  "untracked declared path" fails closed for a `repository`-region class, whose
  owner declared it for paths known to exist. A `template`-region class whose
  patterns cover no tracked path is *vacuously declared*:
  `hash-bound-class-declared` passes for it with a detail naming the class and
  `0 tracked paths`.
  Nothing becomes advisory; the condition an owner can break — the rule's
  absence from the managed region — still fails `hash-bound-attribute-effective`
  under rule 10, which is assessed independently of coverage.
- **Rule 10** adds one sentence: the canonical template fragment carries only
  `template`-region classes. A `repository`-region pattern present in the
  fragment is a declaration defect, detectable by static test, because it would
  install into every consumer a rule the shipped table says belongs to owner
  content.

The amendment is backward-compatible for every existing passing repository:
a class that covered paths before still covers them, every attribute and mode
obligation is unchanged, and this repository's own migration-protocol byte pin
survives in its owner region. The only observable change is that a fresh
consumer repository passes.

## Scope

Define one declaration of committed hash-bound text classes, one resolution rule
from path to class, one mode determination shared by every hashing caller, and
three named read-only `doctor` checks that fail closed.

Out of scope: uncommitted release-bundle text, generated content under
`target/`, binary archives, the computation of the `utf8-text-lf-v1` canonical
form itself, and any validator plane rule.

## Actors and external systems

- `doctor` consumes the declaration and reports named checks.
- The installer, upgrade authorization, mutation guard, release bootstrap and
  candidate acceptance consume mode determination before hashing.
- Git resolves attributes for a working tree; the specification observes that
  resolution and never changes Git configuration.
- Assurance and release owners consume diagnostics and retain lifecycle
  authority.

No network service participates.

## Inputs

- The declared class table, shipped as harness data.
- The repository's tracked file set.
- Resolved Git attributes for candidate paths in the working tree under
  assessment.
- Committed file bytes, read read-only.

## Outputs

- Three named `InstallationCheck` results with bounded, path-level details.
- A resolved mode for a given repository-relative path, or a fail-closed error.
- A non-zero `doctor` exit status when any of the three checks fails.

## State model

Assessment is stateless and read-only. It writes nothing, mutates no lock, and
records no digest. For a fixed working tree, tracked file set and attribute
state, results are deterministic.

## Behavioral rules

1. **Declared class table.** Each class declares an ID, an ordered set of
   repository-relative POSIX path patterns, a mode of exactly `raw` or
   `utf8-text-lf-v1`, the bindings that depend on it, the declaration region
   (`template` or `repository`), and, when the mode is `raw`, the exact required
   Git attribute.
2. **Initial classes.** The table declares exactly three classes at
   implementation: `evaluator-evidence` covering
   `docs/engineering/**/evidence/*.json`, mode `raw`, attribute `text eol=lf`,
   region `template`; `governance-migration-protocol` covering
   `se_harness/governance_migration*.py`,
   `se_harness/governance_migration_contract.json` and
   `tests/fixtures/governance_migration/*.json`, mode `raw`, attribute
   `text eol=lf`, region `repository`; and `standard-lock` covering
   `.engineering-harness.lock`, mode `utf8-text-lf-v1`, no required attribute,
   region `template`.
3. **Declarations are data.** No class entry names an import path, expression,
   shell command or repository-provided executable. The table is loaded as data
   and never evaluated.
4. **Resolution.** A path resolves to the class whose most specific matching
   pattern covers it. An exact path is more specific than a component-boundary
   prefix, which is more specific than a wildcard. A path matching patterns in
   two classes at equal specificity is a declaration defect and fails closed.
5. **Single mode per class.** Every caller obtains the mode from the class. A
   caller must not apply a locally chosen mode, and must not fall back to a
   default when resolution fails. Two modes observed for one class is a defect,
   detectable by test.
6. **Attribute effectiveness.** For each `raw` class, resolve the required
   attribute for its patterns as Git would resolve it for the working tree, by
   `git check-attr` or an equivalent resolution. The class is effective only when
   the resolved value equals the declared requirement for every covered tracked
   path. A more specific conflicting attribute makes the class ineffective.
7. **Versioned sources only.** `.git/info/attributes`, global attributes, and
   local `core.autocrlf` or `core.eol` values are diagnostic context only. They
   never satisfy an attribute requirement, and a class is never reported
   effective on their strength.
8. **Named checks.** `doctor` reports `hash-bound-class-declared`,
   `hash-bound-attribute-effective` and `hash-bound-mode-consistent`, in that
   order, each with a bounded detail naming the exact class, path and observed
   value. Names follow the existing `InstallationCheck` convention and no new
   diagnostic code family is introduced.
9. **Fail closed.** An unreadable `.gitattributes`, unavailable attribute
   resolution, unavailable Git, untracked declared path, invalid UTF-8 in a
   text-mode class, or unresolvable mode produces a failing check with the exact
   reason. No such condition is ever reported as a pass, and no condition is
   reported as merely advisory.
10. **Two-region completeness.** Classes declared `template` must be present in
    the canonical standard template fragment and, after installation, in the
    target's managed fragment block. Classes declared `repository` must be
    present in owner-controlled `.gitattributes` content outside the managed
    markers. Completeness is assessed over the union of both regions; a class
    present in the wrong region is ineffective.
11. **No historical rewrite.** No recorded digest is recomputed, corrected or
    repointed. `WO-HUP-002`'s `prior_lock_sha256`, every
    `evaluator_evidence_sha256`, `preparation_view_evidence_sha256` and
    `from_lock_sha256` remain exactly as recorded.
12. **Legacy recognition.** Where a stored digest predates its class
    declaration, comparison may recognize the documented newline variants
    through `se_harness.integrity.matches_legacy_newline_variant`. Such a match
    is reported distinctly from an ordinary match and never silently.
13. **Explicit producer newlines.** Every call site that writes a committed
    hash-bound text file passes an explicit LF newline. A producer's platform
    default never decides a bound file's bytes.
14. **Assessment adds nothing else.** Existing digests, comparisons, upgrade
    classification, customization protection, path containment, symlink safety
    and atomic writes are unchanged. The specification adds assessment and mode
    determination only.

## Error and recovery behavior

Every failure names the class, the path and the observed versus required value.
Recovery is a repository content change: declare the missing class, add or
correct the attribute in the correct region, or correct the offending caller.
Recovery is never a Git configuration change and never a digest rewrite. A
failing assessment blocks nothing by itself; it makes `doctor` exit non-zero and
leaves every lifecycle state unchanged.

## Data and interface contracts

The class table is harness-owned data with a stable shape. Mode determination
exposes one query from repository-relative path to mode, returning a
fail-closed error rather than a default. `doctor` check names are part of the
observable contract and are stable once released.

## Security and privacy properties

Assessment is read-only and reads only tracked repository content and resolved
attributes. It executes no repository-provided code and interpolates no
repository content into a shell. Exact-byte trust is preserved for every `raw`
class; no class is relaxed to canonical mode to make an assessment pass, except
`standard-lock`, whose canonical mode is specified here and justified by
`ADR-HBI-001`.

## Performance and capacity

Assessment is bounded by the tracked file set and the number of declared
classes. Attribute resolution is batched per class rather than per file where the
resolution mechanism supports it. `doctor` remains usable on a repository of
this size without a measurable change in its current runtime.

## Observability

Each named check reports pass or fail with a single-line bounded detail.
Aggregate `doctor` behaviour is unchanged: named lines, then any `W013`
maintenance warning, then a non-zero exit when any check failed. A legacy-variant
match is reported wherever the comparison result is reported.

## Compatibility and migration

The declaration describes existing behaviour for `evaluator-evidence` and
`governance-migration-protocol`; neither changes. `standard-lock` changes
`se_harness/upgrade_authorization.py` from raw to canonical comparison, which is
the only behavioural change to an existing comparison. That change is
backward-compatible through rule 12 and rewrites nothing. Consumer repositories
receive only the `template` classes. The new checks bind this repository's own
required gate only after a separately authorized governor upgrade.

## Examples and counterexamples

- A new committed text file whose digest is recorded in a work order and which
  matches no class: `hash-bound-class-declared` fails naming the path.
- `docs/engineering/**/evidence/*.json` overridden by a more specific
  `docs/engineering/x/evidence/*.json -text`: `hash-bound-attribute-effective`
  fails naming both attributes.
- `.engineering-harness.lock` on a CRLF checkout: all three checks pass, because
  its declared mode normalizes line endings and it requires no attribute.
- Counterexample: a passing assessment obtained by setting
  `core.autocrlf=false` locally. Rule 7 forbids reporting effectiveness on that
  basis.
- Counterexample: making `evaluator-evidence` canonical to avoid needing an
  attribute. Rejected by `ADR-REB-003` and out of scope here.

## Explicitly unspecified decisions

The implementation agent chooses the module name and file layout for the
declaration and resolver, the internal shape of the class table, whether
attribute resolution calls `git check-attr` once per class or once per path set,
the ordering of work within a single check, the wording of bounded details
beyond the required class, path and value, and test file organization.
