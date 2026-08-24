+++
id = "WO-HBI-002"
type = "work_order"
title = "Take every hash mode from the declared class and fix the lock's divergence"
status = "approved"
owners = ["engineering-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "This changes the comparison that authorizes an evaluator upgrade from raw to canonical bytes, and makes every hashing caller read its mode from one declaration. Upgrade, assurance and release decisions rely directly on that comparison being correct, and a wrong mode would either block a legitimate upgrade or accept a lock the authorization never covered, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/hash-bound-integrity/",
  "se_harness/hash_bound.py",
  "se_harness/upgrade_authorization.py",
  "se_harness/mutation_guard.py",
  "se_harness/candidate_acceptance.py",
  "repository_tools/release_bootstrap.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_mutation_guard.py",
  "tests/test_release_bootstrap.py",
  "tests/test_governor_transition.py",
  "tests/fixtures/hash_bound/",
]

[relations]
implements = ["REQ-HBI-002"]
specifications = ["SPEC-HBI-001"]
architecture = ["ARCH-HBI-001", "ADR-HBI-001"]
verification = ["VER-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:43:27Z"
decided_by = "engineering-owner"
reason = "Owner approval recorded 2026-08-24. Authorizes bounded local implementation and local qualification only; implementation start remains a separate explicit decision."
+++

# Work Order: Take every hash mode from the declared class and fix the lock's divergence

## Lifecycle and authorization

Approved on 2026-08-24 by the engineering owner. Approval and start are separate
decisions and only the first has been taken, so implementation is not authorized
yet. The dependency is satisfied: `WO-HBI-001` is implemented and merged, so the
declaration and resolver this work order consumes now exist.

Approval would authorize bounded local implementation and local qualification
only. Commit, branch push, pull request, merge, VREC or RLS preparation or
transition, tag, publication, deployment, credential use, maintenance mutation
and operational governor adoption each remain separately unauthorized.

This is deliberately a second work order rather than added scope on the first.
`WO-HBI-001` adds read-only assessment; this one changes an authorization
comparison. Combined, CI would pass a diff whose riskiest change is reviewed
alongside a benign one, and the reviewer's confirmation would cover both at once.

## Objective

Make every hashing caller for a declared class obtain its mode from that class,
resolve `.engineering-harness.lock`'s two-mode divergence in favour of the
canonical mode, and keep `WO-HUP-002`'s recorded digest readable without
rewriting it.

## In scope

- Add the mode arbiter: one query from repository-relative path to mode,
  delegating to `WO-HBI-001`'s resolver and returning a fail-closed error rather
  than a default.
- Change `se_harness/upgrade_authorization.py` to compare the prior lock digest
  under the mode the `standard-lock` class declares, which is
  `utf8-text-lf-v1`, instead of hashing raw bytes directly.
- Change `se_harness/mutation_guard.py` so the bytes it supplies are hashed under
  the arbitrated mode rather than under an assumption at the call site.
- Make `repository_tools/release_bootstrap.py` obtain the same mode from the
  arbiter instead of canonicalizing locally, so the two callers cannot diverge
  again. Its computed digest and its verdict must not change.
- Recognize digests recorded before their class was declared through
  `se_harness.integrity.matches_legacy_newline_variant`, and report a legacy
  match distinctly from an ordinary match wherever the comparison result is
  reported.
- Give `se_harness/candidate_acceptance.py` an explicit LF newline where it writes
  the lock, and give every other call site that writes a committed hash-bound
  text file the same, so a producer's platform never decides a bound file's bytes.
- Add the tests `VER-HBI-001` requires for `REQ-HBI-002`: mode-divergence
  detection, lock mode convergence across LF and CRLF checkouts, legacy
  recognition against `WO-HUP-002`'s recorded value, the LF, CRLF, CR,
  invalid-UTF-8 and tamper cases per class, and the producer-newline cases on a
  CRLF-default platform.
- Retain work-order-keyed verification evidence under this domain's `evidence/`.
- After separate external-action authority, commit and push the bounded candidate
  and open a pull request declaring `Harness-Work-Order: WO-HBI-002`.

## Out of scope

- The declaration data, the class resolver, the attribute prober and the three
  `doctor` checks. Those are `WO-HBI-001`.
- Changing any class's declared mode, adding a class, or adding a third mode or a
  new canonical form. The two modes are the existing raw bytes and the existing
  `utf8-text-lf-v1` form defined by `REQ-PMI-001`.
- Editing `.gitattributes`, the canonical template fragment, root managed files,
  `.engineering-harness.lock` or `.engineering-harness.toml`.
- Rewriting, correcting or repointing `WO-HUP-002`'s `prior_lock_sha256` or any
  other recorded digest, and any change to a historical `VREC`, `RLS`, `REL`,
  `WO` or evidence fact.
- Changing upgrade classification, customization protection, mutation-guard
  refusal codes, PEP 610 evaluator identity checking, path containment, symlink
  safety or atomic-write behaviour.
- Adding a validator plane rule or adopting a governor.
- Performing an evaluator upgrade, a root adoption, a release preparation, a
  release, a publication, a deployment, or any credential-bearing operation.

## Authorized decision envelope

After approval and explicit start, implementation may choose the arbiter's
function and parameter names, where the legacy-match indication is carried in
existing return shapes, the wording of diagnostics beyond the required class,
path and observed value, and test organization within the scoped paths.

It may not introduce a default mode, keep a locally chosen mode at any caller for
a declared class, change a declared mode, silence a legacy match, change a
mutation-guard refusal code or its meaning, weaken any existing refusal, or
change a file outside the execution scope. If any change would alter
`release_bootstrap`'s computed digest or verdict, stop rather than proceeding.

## Constraints

- Python 3.11+ standard library only.
- Treat lock bytes, artifact metadata, recorded digest fields and environment as
  untrusted input.
- Fail closed where a mode cannot be resolved, and report the exact failed
  predicate.
- No worktree byte of any existing checkout changes as a result of this work; the
  divergence is resolved by mode, not by adding an attribute.
- Preserve every existing refusal, digest and safety check unchanged except the
  single prior-lock comparison this work order names.
- Run the governing evaluator — released `se-harness==0.6.0` installed from the
  wheel whose archive digest matches the lock — from outside the checkout for
  validation and preflight.
- Preserve all unrelated changes and owner content outside managed markers.
- Do not commit, push, open a pull request, merge, verify, release, publish or
  deploy without that separate authority.

## Expected change surface

- The mode arbiter added to the module `WO-HBI-001` introduced.
- The prior-lock comparison in upgrade authorization, and the byte supply path in
  the mutation guard.
- The release bootstrap's local canonicalization replaced by the arbiter, with an
  unchanged result.
- One explicit newline argument at the lock write site, plus any other producing
  call site the audit finds for a declared class.
- Focused tests in the new module and additions to the three existing test
  modules that already cover these callers.
- One retained evidence file.

The execution scope is a maximum allowlist. If the producer audit finds a writing
call site outside these paths, stop and request a bounded scope amendment rather
than editing it.

## Required verification

- Released-evaluator identity proof for exact public `0.6.0`, including the
  installed PEP 610 archive digest matching the lock's `evaluator.archive_sha256`.
- Start preflight after approval and review preflight after implementation.
- Every `REQ-HBI-002` method and case in `VER-HBI-001`.
- Proof that the exact `prior_lock_sha256` recorded by `WO-HUP-002` is still
  recognized after the change, that the recognition is reported as a legacy
  variant, and that the recorded field's bytes on disk are unchanged.
- Proof that upgrade authorization now reaches the same verdict on an LF checkout
  and a CRLF checkout of the same commit, where before it differed.
- Proof that `release_bootstrap`'s computed digest and verdict are byte-identical
  before and after.
- The mode-consistency check from `WO-HBI-001` passing, and a deliberate
  reintroduction of a second mode failing it.
- The full supported test suite, the artifact graph validator, the release
  distribution validator, `python -m se_harness --help`, and `doctor`.
- Windows and Linux lanes without credentials or privileged operations, and no
  actual evaluator upgrade performed.

## Evidence to record

Record in `docs/engineering/hash-bound-integrity/evidence/WO-HBI-002-verification.md`:
the evaluator version and wheel digest; the approved preflight manifests; the
before-and-after digests computed by each caller for `.engineering-harness.lock`
on LF and CRLF checkouts, with the committed blob digest for reference;
`WO-HUP-002`'s recorded value and the exact comparison output showing legacy
recognition; the producer-call-site audit with every writing site found and its
newline handling before and after; the mode-divergence test output in both the
passing and the deliberately failing configuration; `release_bootstrap`'s
unchanged digest and verdict; full test, graph and release-surface results; exact
changed paths; proof that no recorded digest field, root managed file, lock,
worktree byte or Git ref changed; manual owner assessments; and every external
action deliberately not performed, explicitly including that no evaluator upgrade
was executed.

## Stop and escalate conditions

Stop and retain the failing case, rather than working around it, if:
`WO-HBI-001` is not implemented; the packet is not approved; preflight or graph
validation fails; `WO-HUP-002`'s recorded digest cannot be recognized without
rewriting it; legacy recognition would have to be silent to keep an existing
test passing; a caller cannot obtain its mode without a default; the change would
alter `release_bootstrap`'s digest or verdict, a mutation-guard refusal, or an
upgrade classification; a producing call site lies outside the execution scope; a
recorded digest, a root managed file, the lock, a Git ref or external state would
change; or any requested external action lacks separate authority.

## Completion report format

Report the arbiter's single query and every caller now using it; the digests each
caller computes for the lock on LF and CRLF checkouts before and after; the
legacy-recognition output for `WO-HUP-002`; the producer audit result; the
mode-divergence test in both configurations; `release_bootstrap`'s unchanged
result; changed paths; validation and test results; the retained evidence path;
proof that no digest, managed file, lock, worktree byte or ref changed; the final
`WO-HBI-002` lifecycle state; and the one next separately authorized step.
