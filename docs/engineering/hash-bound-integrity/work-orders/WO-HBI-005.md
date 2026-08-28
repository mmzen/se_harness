+++
id = "WO-HBI-005"
type = "work_order"
title = "Make doctor pass in a fresh consumer repository: drop the self-hosting class from the shipped surface and assess empty template classes vacuously"
status = "in_progress"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "This changes the shipped hash-bound declaration, the canonical template fragment every consumer installs, and the fail-closed rule of a doctor check that the required CI gate and every consumer's installation assessment rely on. A wrong change here either leaves every fresh installation red, as today, or silently stops reporting a missing byte rule; both are trusted engineering state that later assurance, upgrade and release decisions depend on, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/hash_bound.py",
  "se_harness/hash_bound_classes.json",
  "templates/repository/standard/gitattributes.fragment",
  "tests/test_hash_bound_integrity.py",
  "tests/test_public_onboarding.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/engineering/hash-bound-integrity/",
  "docs/notes/harness-installation-and-upgrades.md",
]

[relations]
implements = ["REQ-HBI-001", "REQ-HBI-003", "REQ-HBI-004"]
specifications = ["SPEC-HBI-001"]
architecture = ["ARCH-HBI-001", "ADR-HBI-001"]
verification = ["VER-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T10:18:43Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I accept SPEC-HBI-001/VER-HBI-001 and I approve WO-HBI-005', after acceptance of the first amendment to SPEC-HBI-001 and the third amendment to VER-HBI-001. Authorizes only the stated scope: remove governance-migration-protocol from se_harness/hash_bound_classes.json and its four lines from templates/repository/standard/gitattributes.fragment, gate the untracked-pattern failure in _class_declared on repository-region classes, add the fresh-consumer onboarding test on LF and core.autocrlf=true checkouts, retarget the hash-bound tests, apply the accepted amendments, note the fragment update in the installation guide, and retain evidence. No root managed file, no governance_migration source or fixture, no recorded digest. Start, completion, commit-bound verification, release and publication are separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T10:18:46Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-28 by the accountable owner immediately after approval, on the standing instruction to implement the work order the moment it is approved. Execution is confined to the approved scope and the execution_scope paths; completion, commit-bound verification and release remain separate decisions."
+++

# Work Order: Make doctor pass in a fresh consumer repository

## Lifecycle and authorization

Draft. Nothing in this record authorizes implementation, a lifecycle
transition, a commit, a push, a pull request, a governor adoption, a release, a
publication or any external action. Approval by the engineering owner
authorizes bounded local implementation, local qualification, one
implementation branch and one pull request declaring
`Harness-Work-Order: WO-HBI-005`. Merge, `VREC` preparation or transition, tag,
release, publication, deployment, credential use, maintenance mutation and
governor adoption each remain separately unauthorized.

This work order depends on accountable acceptance of the proposed third
amendment to `VER-HBI-001` and the proposed first amendment to `SPEC-HBI-001`,
both drafted in the same packet. Approving the work order without accepting the
amendments would authorize implementation against a specification that still
declares the class being removed and still fails the case being made vacuous.

## What was found, and by what

Repository issue #207, raised from finding P0-1 of the 2026-08 complexity audit
at `f0ecd9b`, reports that `harnessctl doctor` exits 1 in every consumer
repository after its first commit. Reproduced on 2026-08-28 from candidate
source on Linux:

```text
harnessctl init consumer --project-name demo
cd consumer && git init && git add -A && git commit -m init
harnessctl doctor consumer
FAIL hash-bound-class-declared: evaluator-evidence: pattern
     docs/engineering/**/evidence/*.json matches no tracked path;
     governance-migration-protocol: pattern se_harness/governance_migration*.py
     matches no tracked path; ... (+1 more)
FAIL hash-bound-attribute-effective: governance-migration-protocol: pattern
     se_harness/governance_migration*.py is declared in template; requires the
     repository region; ... (x3)
```

`se_harness/hash_bound.py` and `se_harness/hash_bound_classes.json` are
byte-identical between `v0.7.1` and `main`, so the published evaluator behaves
the same way.

Two independent defects produce those two lines, and a consumer needs both
fixed to reach exit 0:

1. **A self-hosting class in the shipped surface.** `hash_bound_classes.json`
   declares `governance-migration-protocol` over `se_harness/governance_migration*.py`,
   `se_harness/governance_migration_contract.json` and
   `tests/fixtures/governance_migration/*.json`, which exist only in this
   repository. `templates/repository/standard/gitattributes.fragment` lines 3–6
   install the same three rules into every consumer's managed region, while the
   class is declared `repository`-region. The class therefore fails both checks
   in any repository but this one. `VER-HBI-001` acceptance scenario 7 already
   promises the opposite; the divergence was pinned by
   `test_candidate_fragment_promotion_of_repository_patterns_is_pinned` rather
   than refused.
2. **"Matches no tracked path" is unconditionally fatal.** `_class_declared`
   (`hash_bound.py:454-457`) fails any pattern that covers no tracked path.
   `evaluator-evidence` legitimately covers nothing until the first `VREC` is
   captured, so a fresh repository fails even after defect 1 is removed.

The acceptance lane never observed this because `candidate_acceptance.py`
initializes its target without `git init`, and `preflight.py:131-132` emits no
hash-bound check outside a Git working tree. The defect lives in the gap between
"installed" and "first commit", which no existing scenario exercises.

## Objective

Make `harnessctl init` followed by a first commit and `harnessctl doctor` exit 0
on Linux and Windows, by removing the repository-only class from the shipped
declaration and fragment and by assessing an empty `template`-region class as
vacuously declared, without weakening any fail-closed condition that an owner
can actually break.

## In scope

- Remove the `governance-migration-protocol` class from
  `se_harness/hash_bound_classes.json`. Add `implementation_sha256` to
  `unbound_digest_fields` with the reason that it is bound in harness data and
  pinned by owner-controlled `.gitattributes` content. The reason text must
  match `_REASON` in `se_harness/hash_bound.py` (`^[A-Za-z0-9 ;,.()_-]+$`): an
  apostrophe or any other character outside that class makes
  `load_declaration` raise and every hash-bound check fail, in this repository
  and in every consumer.
- Remove the comment line and the three `governance_migration` rules from
  `templates/repository/standard/gitattributes.fragment`, leaving the
  `evaluator-evidence` rule and its comment.
- In `se_harness/hash_bound.py`, restrict the "pattern matches no tracked path"
  failure in `_class_declared` to `repository`-region classes. A
  `template`-region class with no covered path passes with a detail that names
  the class and `0 tracked paths`. `_attribute_effective`, `_mode_consistent`,
  resolution, mode determination and every digest comparison are unchanged.
- In `tests/test_public_onboarding.py`, add the fresh-consumer scenario:
  `init` into a temporary directory, `git init`, `add -A`, `commit`, then
  `doctor` asserting exit 0 and that all three `hash-bound-*` checks are
  present and passing; run once with `core.autocrlf=true` to mirror a Windows
  checkout. Skip only when Git is unavailable, as the hash-bound tests already
  do.
- In `tests/test_hash_bound_integrity.py`: retarget
  `test_untracked_declared_path_fails_closed` at a synthetic `repository`-region
  class; add a case that a `template`-region class covering nothing passes
  `hash-bound-class-declared` and fails `hash-bound-attribute-effective` when
  its rule is absent; add a case that a `repository`-region class declared only
  in the template region still fails when its pattern does match tracked paths;
  add a static portability test that no pattern in the shipped declaration or
  rule in the canonical fragment begins with `se_harness/`, `tests/` or
  `repository_tools/`; delete
  `test_candidate_fragment_promotion_of_repository_patterns_is_pinned` and
  update `test_declares_exactly_the_specified_classes`,
  `test_known_paths_resolve_to_exactly_one_class`,
  `test_declared_bindings_are_actually_recorded_somewhere` and the synthetic
  fixture set for the two-class declaration.
- Apply the accepted amendments to `SPEC-HBI-001` (rules 2, 9 and 10) and
  `VER-HBI-001` (matrix rows, scenarios) as drafted in this packet.
- Note in `docs/notes/harness-installation-and-upgrades.md` that the next
  release's `upgrade` plan classifies the managed `.gitattributes` block as
  `update` and that owner content outside the markers is preserved.
- Retain work-order-keyed implementation and verification evidence under this
  domain's `evidence/`, including the before-and-after `doctor` transcript from
  a fresh consumer on Linux and on Windows CI.
- Commit on one branch and open one pull request declaring
  `Harness-Work-Order: WO-HBI-005`.

Amended on 2026-08-28 by the accountable owner during execution, on the
implementer's escalation: `tests/test_standard_repository_lifecycle.py` is
added to the execution scope. Its
`test_evaluator_evidence_bytes_are_portable_across_git_checkouts` hard-codes the
six-line fragment and asserts it equal to both the shipped fragment and the
root managed block, so it fails on the two-line fragment; it is retargeted to
assert the shipped and freshly installed fragment are the two-line form while
the root managed block keeps the released 0.7.1 six-line block and the owner
region keeps its three rules. No other scope change.

## Out of scope

- Deleting, moving or changing `se_harness/governance_migration.py`,
  `governance_migration_contract.py`, their JSON contract, their fixtures, the
  `rehearse-migration` command or its CI lanes. That is audit finding P0-4 and
  needs its own packet; this work order neither depends on it nor prejudges it.
- The owner-controlled region of the root `.gitattributes`. The three
  `governance_migration` rules stay there; they are what keeps this repository's
  `implementation_sha256` bytes stable once the shipped class is gone.
- The managed region of the root `.gitattributes`, `.engineering-harness.lock`,
  `.engineering-harness.toml` and every other root managed file. The root block
  belongs to released 0.7.1 and is rewritten only by a separately authorized
  governor upgrade.
- Making any empty-pattern condition advisory. `SPEC-HBI-001` rule 9 and
  `HRN-008` forbid reporting a completeness condition as a warning; the change
  is a region-scoped pass, not a downgrade.
- A second, repository-owned declaration file for classes. It would contradict
  `SPEC-HBI-001` rule 3 and add surface for a class the audit wants removed.
- `candidate_acceptance.py` and the acceptance lane's lack of `git init`. The
  new onboarding test covers the scenario; changing the lane is separate work.
- Rewriting or repointing any recorded digest, `VREC`, `RLS` or evidence fact,
  and converting any committed file's bytes.
- Preparing a `VREC`, merging, tagging, releasing, publishing, deploying, or
  any credential-bearing operation.

## Authorized decision envelope

Implementation may choose the exact wording of check details, test and fixture
names, how the synthetic two-class declaration is expressed, where in
`test_public_onboarding.py` the consumer scenario lives, and the placement of
the note in the installation guide.

It may not add or rename a class, change a class's mode or region, change
`_attribute_effective` or `_mode_consistent`, relax the failure for a
`repository`-region class, touch any root managed file, delete or edit any
`governance_migration` source or fixture, or edit a file outside the execution
scope. If removing the class turns out to change any digest comparison a
product code path performs, stop rather than proceeding; the packet's premise is
that none does.

## Constraints

- Python 3.11+ standard library only.
- `hash-bound-class-declared`, `hash-bound-attribute-effective` and
  `hash-bound-mode-consistent` keep their names, order and
  `InstallationCheck` convention; no new diagnostic code family.
- The rule must remain effective from versioned repository content. A local
  `core.autocrlf`, a global attributes file or `.git/info/attributes` still
  satisfies nothing.
- This repository's own `doctor` must keep passing throughout, including
  `managed:.gitattributes: unchanged`; `test_this_repository_passes_every_check`
  is unchanged.
- Qualify the consumer scenario in a checkout with `core.autocrlf=true` as well
  as an LF checkout. A green result on LF alone proves nothing for the Windows
  criterion.
- Candidate `doctor` on this repository, run from the checkout, must also keep
  every hash-bound check passing: `test_this_repository_passes_every_check`
  exercises the candidate code, not the released evaluator, and the removed
  class's paths are still tracked here.
- `WO-REB-029`'s approval envelope named "no byte of
  `se_harness/hash_bound_classes.json`"; that envelope closed with that work
  order and binds nothing here. This work order is the first to change the file
  since `WO-HBI-001`, and no test pins its digest.
- Run the governing evaluator — released `se-harness==0.7.1` — from outside the
  checkout for validation and preflight. Its own `doctor` on this repository is
  unaffected: the root managed block and the owner rules are untouched.
- Preserve all unrelated changes and owner content outside managed markers.

## Expected change surface

`se_harness/hash_bound.py` (about eight lines in `_class_declared`);
`se_harness/hash_bound_classes.json` (one class removed, one unbound field
added); `templates/repository/standard/gitattributes.fragment` (four lines
removed); `tests/test_hash_bound_integrity.py` and
`tests/test_public_onboarding.py` (about 120 lines net); the amended
`SPEC-HBI-001` and `VER-HBI-001`; one note; one evidence file.

## Required verification

Perform every `VER-HBI-001` case that names `REQ-HBI-001`, `REQ-HBI-003` or
`REQ-HBI-004`, including the new fresh-consumer, vacuous-class, misplaced-class
and portability rows; run the full suite on Python 3.11 and the local runtime
on an LF checkout and a `core.autocrlf=true` checkout; validate the graph before
and after; run `doctor` on this repository and on a fresh consumer; and review
the final diff against the execution scope.

## Evidence to record

Commands and results for every required check; the fresh-consumer `doctor`
transcript before and after, on Linux and on Windows CI; the list of tests
added, retargeted and deleted with the reason for each; confirmation that no
product code path resolves `governance-migration-protocol`; deviations from
this order; and the authority boundaries observed.

## Stop and escalate conditions

Stop if removing the class changes any digest comparison outcome in the suite;
if this repository's own `doctor` or the released 0.7.1 evaluator's `doctor`
stops passing; if making the empty `template` case vacuous would also pass a
case where the required attribute rule is absent; if a required test fails on
either checkout; if the change would require editing a root managed file; or if
completion would require commit, remote, release or publication authority
beyond the single branch and pull request authorized here.

## Completion report format

Report the artifact IDs touched, the observed effects and material non-effects
(in particular that no root managed file, no `governance_migration` source and
no recorded digest changed), blockers, the final lifecycle state, the
accountable decision required next, and exactly one typed next step, taken from
the `harnessctl check` schema-2 result.
