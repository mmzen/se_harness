+++
id = "ARCH-LRE-001"
type = "architecture"
title = "One declaration semantics shared by validation and the upgrade transaction"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-LRE-001", "REQ-LRE-002"]
conforms_to = ["SPEC-LRE-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "security-privacy-or-trust-boundary", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The architecture adds an optional key to the [evaluator_upgrade] authorization packet, which is a published contract every consumer repository writes by hand and which the upgrade path treats as an exact field set. It decides what may relax a governance error on an immutable record, which is a trust-boundary question. It binds validation, dashboard publication and the upgrade transaction to one shared semantics that necessarily exists in two implementations because the validator script must stay self-contained. Once released it can never be narrowed without breaking repositories that relied on it, and materially different alternatives exist including a repository-local configuration key, a bootstrap-contract extension, and per-record artifact fields."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "technical-owner"
+++

# Architecture: One declaration semantics shared by validation and the upgrade transaction

## Context and scope

Three components must agree about which released records are legitimately
unbound: the validator script, which decides whether the repository passes; the
upgrade transaction, which must not create a repository that cannot pass; and
dashboard publication, whose release view is read by humans. Today all three
share a hard-coded six-identifier set, which is why they agree.

Replacing that set with a declaration means the agreement has to be constructed
rather than inherited. The complicating constraint is that the validator script
ships into consumer repositories and runs there as a standalone file: it may not
import the harness package. The upgrade transaction, by contrast, lives inside the
package and never runs as a standalone script.

The architecture therefore accepts two implementations of one semantics and makes
their equivalence a tested property. It does not attempt to unify them by making
the validator importable, which would change the self-hosting boundary, nor by
making the installer shell out to the script, which would make an authorization
decision depend on a subprocess.

## Components and responsibilities

- **The declaration** is data in a work order's `[evaluator_upgrade]` table. It
  owns nothing; it is read.
- **`se_harness/upgrade_authorization.py`** owns the shape of the packet. It
  admits the optional key, validates it, and carries it on the loaded
  authorization. It does not resolve exemptions, because at load time it holds one
  work order and resolution needs the whole graph.
- **`se_harness/legacy_release_evidence.py`** owns resolution for the package
  side: given a repository root, it enumerates release records and
  authority-granting declaring work orders and returns the accepted mapping. It
  makes no decision about what to do with it.
- **`se_harness/installer.py`** owns the refusal. It asks the resolver, subtracts,
  and refuses or notices. It decides nothing about what a valid declaration is.
- **The validator script** owns resolution and diagnostics for the consumer side.
  It resolves from artifacts already loaded in memory and emits `E012` and `W024`.
- **`.github/scripts/publish_dashboard.py`** consumes the same rule for its
  release view and owns no rule of its own.

## Dependency direction

Dependencies point from deciders to the resolver, and from the resolver to
artifact data. `installer.py` depends on `legacy_release_evidence.py`;
`legacy_release_evidence.py` depends only on front-matter parsing and the standard
library. Nothing depends on `installer.py`. The validator script depends on
nothing outside itself.

The resolver must not depend on `installer.py`, on the lock, on the installed
evaluator identity, or on any run-time state, because its answer must be a
property of the repository's governed content alone.

## Data and control flow

At validation: artifacts are loaded once; resolution runs once over them; the
resulting mapping is consulted where the release-record binding is currently
decided, and again to emit one `W024` per accepted record. No second pass over the
filesystem occurs.

At upgrade: the authorization is loaded and matched as it is today; the resolver
walks the artifact tree; the remainder is computed; refusal happens before the
plan is executed and therefore before the first write. On the planning path the
same computation produces a notice and control continues.

At dashboard publication: the same rule is applied to the same artifact data
already loaded for the release view.

## Trust boundaries

The declaration crosses from repository content into a decision that relaxes a
governance error, so it is the trust boundary of this design. It is constrained
by three independent facts that run-time input cannot supply: the declarer's
status must grant authority under managed lifecycle policy, the record must
already be `released` with both binding fields absent, and the record's
`released_at` must precede the declarer's approval instant.

Everything else stays outside the boundary. Operator environment values,
command-line flags and local configuration are not inputs. The declaration is
never used as a path, an import, a command or an expression. The refusal is a
governance observation and grants no authority.

## Required patterns

- Resolution is a pure function of loaded artifact data, deterministic and
  side-effect free.
- Authority-granting statuses come from the managed work-order lifecycle registry,
  never from a literal list in either implementation.
- Timestamps are compared in the single canonical form the rest of the harness
  already validates.
- A declaration that does not resolve produces a diagnostic on the declarer.
- The two implementations are asserted equivalent against a shared committed
  vector fixture.
- The refusal path is checked before any write and leaves the tree untouched.

## Prohibited patterns

- Importing `se_harness` from the validator script.
- Invoking the validator script to make an authorization decision.
- Consulting an environment variable, flag or local configuration value in
  resolution or refusal.
- Adding an identifier to the frozen self-hosting compatibility set.
- Editing, recomputing or repointing any record field to make a check pass.
- Treating a malformed declaration as an empty one.
- Accepting a declaration from a work order whose status does not grant authority.

## Quality attributes

Correctness is prioritized over convenience: the design would rather refuse an
upgrade than complete one that freezes a repository. Auditability is served by
placing the declaration in the artifact whose approval is the accountable act.
Reversibility is deliberately asymmetric: the exemption is easy to grant in a
reviewed diff and impossible to grant at run time. Determinism is required because
the same content must produce the same diagnostics on every platform and in CI.

## Conformance checks

- A test asserts the two implementations agree on every shared canonical vector.
- A test asserts an authority-granting declaration exempts, and that the same
  declaration in a `draft` work order does not.
- A test asserts a later packet declaring nothing does not revoke an earlier
  declaration.
- A test asserts each fail-closed case produces `E012` on the declaring work order.
- A test asserts one `W024` per accepted record, including for the compatibility
  set.
- A test asserts a refused upgrade leaves the repository byte-identical, and that
  the planning path notices without refusing.
- A test asserts `[evaluator_upgrade]` still rejects any key other than the nine
  required fields and the one optional key.

## Related ADRs

`ADR-LRE-001` records where the declaration lives and why, and why the two
implementations are accepted rather than unified. `ADR-REB-003` is unchanged and
this architecture depends on it for the canonical form of evidence bytes.
