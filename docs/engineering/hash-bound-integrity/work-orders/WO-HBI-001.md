+++
id = "WO-HBI-001"
type = "work_order"
title = "Declare hash-bound text classes and assess their completeness in doctor"
status = "draft"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The declaration becomes the single answer to what governs a committed file's bytes, and its three checks become trusted engineering state that later assurance, upgrade and release decisions read. A wrong or incomplete declaration would report a healthy installation whose bound bytes are unprotected, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/hash-bound-integrity/",
  "docs/engineering/README.md",
  "se_harness/hash_bound.py",
  "se_harness/hash_bound_classes.json",
  "se_harness/preflight.py",
  "se_harness/cli.py",
  "pyproject.toml",
  "MANIFEST.in",
  "tests/test_hash_bound_integrity.py",
  "tests/fixtures/hash_bound/",
]

[relations]
implements = ["REQ-HBI-001"]
specifications = ["SPEC-HBI-001"]
architecture = ["ARCH-HBI-001", "ADR-HBI-001"]
verification = ["VER-HBI-001"]
+++

# Work Order: Declare hash-bound text classes and assess their completeness in doctor

## Lifecycle and authorization

Not authorized. This work order is `draft` and no owner decision exists yet. It
requires approval of `INT-HBI-001`, `CAP-HBI-001`, `REQ-HBI-001`, `REQ-HBI-002`,
`SPEC-HBI-001`, `ARCH-HBI-001` including its `adr_required` decision assessment,
`ADR-HBI-001`, `VER-HBI-001` and this work order, plus a separate explicit start
before any implementation surface changes.

Approval would authorize bounded local implementation and local qualification
only. Commit, branch push, pull request, merge, VREC or RLS preparation or
transition, tag, publication, deployment, credential use, maintenance mutation
and operational governor adoption each remain separately unauthorized.

`INT-HBI-001` carries one open decision — whether the same completeness
assessment additionally becomes a validator plane rule. This work order
implements the `doctor` plane only and is satisfiable regardless of how that
decision resolves. It must not be approved as an implicit answer to it.

## Objective

Make "what governs this file's bytes" answerable from one declaration, and make
its absence, ineffectiveness or override a named failing `doctor` check, without
changing any existing digest, any managed root file, or any checkout's worktree
bytes.

## In scope

- Add the declared hash-bound class table as harness-owned data with the three
  classes fixed by `SPEC-HBI-001` rule 2, and a loader that reads it as data.
- Add the class resolver: repository-relative POSIX path to exactly one class by
  most-specific match, failing closed on no match and on equal-specificity
  overlap.
- Add the attribute prober: resolve the required attribute for a working tree as
  Git would, reporting the resolved value and modifying no configuration.
- Add `hash-bound-class-declared`, `hash-bound-attribute-effective` and
  `hash-bound-mode-consistent` to `inspect_installation`, emitted in that order
  through the existing `InstallationCheck` convention, driving the existing
  non-zero `doctor` exit status. Introduce no new diagnostic code family.
- Derive the assessed hash-bound inventory from recorded digest fields in
  governed artifacts, so an undeclared hash-bound path is detectable.
- Declare the new data file in package data and the source manifest so an
  installed distribution carries it.
- Add the tests, fixtures and fresh-checkout matrices `VER-HBI-001` requires for
  `REQ-HBI-001`, including the attribute-absent, attribute-override,
  unversioned-source, region-placement, template-parity and fail-closed cases.
- Add `hash-bound-integrity` to `docs/engineering/README.md`.
- Retain this complete hash-bound-integrity governing packet.
- Retain work-order-keyed verification evidence under this domain's `evidence/`.
- After separate external-action authority, commit and push the bounded
  candidate and open a pull request declaring `Harness-Work-Order: WO-HBI-001`.

## Out of scope

- Editing `.gitattributes` or `templates/repository/standard/gitattributes.fragment`.
  Both existing `raw` classes already have their attribute in the correct region
  and `standard-lock` requires none, so no attribute content changes. If
  implementation concludes an attribute must change, stop and request a bounded
  amendment rather than editing a managed fragment.
- Every mode-determination and caller change, including
  `se_harness/upgrade_authorization.py`, `se_harness/mutation_guard.py`,
  `se_harness/candidate_acceptance.py` and
  `repository_tools/release_bootstrap.py`. Those belong to `WO-HBI-002`.
- Adding a validator plane rule, changing the managed validator script, changing
  any managed policy document, or adopting a governor.
- Editing root managed files, `.engineering-harness.lock` or
  `.engineering-harness.toml`.
- Recomputing, correcting, repointing or rewriting any recorded digest, and any
  change to a historical `VREC`, `RLS`, `REL`, `WO` or evidence fact.
- Uncommitted release-bundle text, generated content, binary archives, and any
  repository-wide line-ending change or re-normalization.
- Reopening `ADR-REB-003`'s selected mechanism or its rejected options.
- Missing or incorrect entries in `docs/engineering/README.md` other than
  `hash-bound-integrity`; the absent `release-0-6-0` entry belongs to its own
  work order.
- Building promotable distributions, releasing, publishing, deploying, or any
  credential-bearing operation.

## Authorized decision envelope

After approval and explicit start, implementation may choose the internal shape
of the class table, function and helper names, whether attribute resolution runs
once per class or once per path set, the ordering of work inside a single check,
the wording of bounded details beyond the required class, path and value, and
test and fixture organization within the scoped paths.

It may not add, remove or rename a class, change a class's mode or required
attribute, add a fourth check or a new diagnostic code family, introduce a
default mode, accept Git configuration as satisfying an attribute requirement,
relax a `raw` class, change a file outside the execution scope, or answer
`INT-HBI-001`'s open decision. A different module or data file name than the two
declared paths requires a bounded scope amendment.

## Constraints

- Python 3.11+ standard library only.
- Assessment is read-only: no file, lock, index or Git configuration write. Prove
  it by a before-and-after comparison of the working tree.
- Treat repository content, tracked paths, `.gitattributes` bytes and attribute
  resolution output as untrusted input. Never interpolate them into a shell and
  never execute repository-provided code.
- Fail closed on every unknown, unreadable or unassessable condition, with the
  exact failed predicate in the detail. Never report such a condition as a pass
  and never as advisory.
- Preserve every existing digest, comparison, upgrade classification,
  customization protection, path containment, symlink safety and atomic write
  unchanged.
- Run the governing evaluator — released `se-harness==0.6.0` installed from the
  wheel whose archive digest matches the lock — from outside the checkout for
  validation and preflight. An in-tree `doctor` skew report is boundary evidence,
  not authorization to overwrite a root managed file.
- Preserve all unrelated changes and owner content outside managed markers.
- Do not commit, push, open a pull request, merge, verify, release, publish or
  deploy without that separate authority.

## Expected change surface

- One new declaration data file and one new module holding the loader, resolver
  and attribute prober.
- The three named checks added to installation inspection, surfaced by the
  existing `doctor` command path.
- Package data and source manifest entries for the new data file.
- One new focused test module plus fixtures for the checkout and attribute
  matrices.
- The engineering domain index entry, this governing packet, and one retained
  evidence file.

The execution scope is a maximum allowlist, not an obligation to change every
listed file. `se_harness/cli.py` is listed only in case check surfacing requires
it; leaving it unchanged is the expected outcome.

## Required verification

- Released-evaluator identity proof for exact public `0.6.0`, including the
  installed PEP 610 archive digest matching the lock's `evaluator.archive_sha256`.
- Start preflight after approval and review preflight after implementation.
- Every `REQ-HBI-001` method and case in `VER-HBI-001`, including isolated
  fresh-checkout matrices per `raw` class under `core.autocrlf` values `true`,
  `input` and `false`, with digests computed independently of any value the
  implementation reports.
- The static checks in `VER-HBI-001`: declaration contains no import, expression
  or command; the three check names are exact and ordered; `template`-region
  classes are byte-identical to the canonical template fragment.
- The full supported test suite, the artifact graph validator, the release
  distribution validator, `python -m se_harness --help`, and `doctor` before and
  after.
- Proof that no recorded digest field changed and that the managed
  `.gitattributes` block still matches its recorded lock digest.
- Windows and Linux lanes without credentials or privileged operations.
- Hosted Engineering Harness and Candidate Evidence checks only after separately
  authorized pull-request creation.

## Evidence to record

Record in `docs/engineering/hash-bound-integrity/evidence/WO-HBI-001-verification.md`:
the evaluator version and wheel digest; the approved preflight manifests; the
`RC-060-02` reproduction including the committed blob digest and the CRLF
worktree digest of `.engineering-harness.lock`; the derived hash-bound inventory
with the source artifact field for each entry; per-class fresh-checkout results
for all three `core.autocrlf` values; `git check-attr` output for every declared
pattern; every negative case with its exact failing check line; `doctor` output
before and after; full test, graph and release-surface results; exact changed
paths; the unchanged state of every recorded digest field and of the managed
`.gitattributes` digest; manual owner assessments; diff hygiene; the explicit
statement that these checks do not bind this repository's required CI gate until
a separately authorized governor upgrade; and every external action deliberately
not performed.

## Stop and escalate conditions

Stop and retain the failing case, rather than working around it, if: the packet
is not approved or the technical owner rejects the decision assessment; preflight
or graph validation fails; an attribute or a managed fragment would have to
change; a fourth class or a fourth check appears necessary; the inventory
derivation finds a hash-bound path that no proposed class can cover without
broadening a pattern beyond its bindings; attribute effectiveness cannot be
resolved on a supported platform; a check can pass only by accepting Git
configuration, adding an allowlist, or relaxing a `raw` class; a recorded digest,
a root managed file, the lock, a Git ref or external state would change; the work
requires `WO-HBI-002`'s surface; or any requested external action lacks separate
authority.

## Completion report format

Report the declared classes with mode, region and required attribute; the three
check names and their observed output; the derived inventory and any path it left
unmatched; fresh-checkout matrix results per class and configuration; the
negative cases and their exact failing lines; changed paths; validation and test
results; the retained evidence path; proof that no digest, managed file, lock or
worktree byte changed; the stated CI-binding limit; the final `WO-HBI-001`
lifecycle state; and the one next separately authorized step.
