+++
id = "WO-LRE-001"
type = "work_order"
title = "Implement declared legacy release-evidence exemptions and the pre-apply upgrade refusal"
status = "in_progress"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The change decides when a governance error on an immutable released record may be relaxed, and it adds surface to the [evaluator_upgrade] authorization packet that every consumer repository writes by hand. Both become trusted engineering state that later upgrade, assurance and release decisions read, and once released the semantics can never be narrowed. A wrong implementation would either keep repositories frozen or silently accept unbound releases, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/legacy-release-evidence/",
  "docs/engineering/README.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "se_harness/legacy_release_evidence.py",
  "se_harness/upgrade_authorization.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  ".github/scripts/publish_dashboard.py",
  "tests/test_legacy_release_evidence.py",
  "tests/test_release_bootstrap.py",
  "tests/fixtures/legacy_release_evidence/",
]

[relations]
implements = ["REQ-LRE-001", "REQ-LRE-002"]
specifications = ["SPEC-LRE-001"]
architecture = ["ARCH-LRE-001", "ADR-LRE-001"]
verification = ["VER-LRE-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T10:45:00Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement declared legacy release-evidence exemptions and the pre-apply upgrade refusal

## Lifecycle and authorization

Authority for this work order is the accountable instruction recorded verbatim in
this domain's README, given on 2026-08-24 after the owner was shown the measured
freeze in a consumer repository and the three candidate resolutions. That
instruction is the sole basis for the `draft` to `approved` events of every
artifact in this domain and for this work order's own transition to
`in_progress`.

It authorizes exactly the implementation described below, within the declared
execution scope. It does not authorize a release, a version bump, a tag, a build,
a publication, a push, a pull request, a governor adoption, a deployment, a
consumer upgrade, or any edit to an artifact of another domain.

## Objective

Give a repository holding pre-enforcement released records a governed way to
declare them, so it can adopt schema-3 evaluator-evidence enforcement without
rewriting an immutable record and without freezing its own work, and make the
frozen state recorded in issue #126 unreachable by refusing the upgrade that
would cause it.

## In scope

- Add the optional key `legacy_releases_without_evaluator_evidence` to the
  `[evaluator_upgrade]` packet contract in `se_harness/upgrade_authorization.py`,
  validate its shape, and carry it on the loaded authorization.
- Add `se_harness/legacy_release_evidence.py` as the package-side resolver: a
  pure function from a repository root to the accepted mapping of exempt release
  record to declarer, plus the defect list, implementing `SPEC-LRE-001` rules 1
  through 11.
- Refuse in `se_harness/installer.py`, before the first write of an authorized
  evaluator identity transition, when an undeclared unbound `released` record
  remains, naming every such identifier and the authorizing work order.
- Report the same finding as a notice on the planning path in
  `se_harness/cli.py`, without refusing and without changing the exit status.
- Record the declared identifiers in the retained transition evidence when the
  declaration is non-empty, leaving the evidence shape unchanged when it is empty.
- Implement resolution and diagnostics in
  `templates/repository/standard/scripts/validate_engineering_artifacts.py`: the
  exemption at the release-record binding decision, `E012` on a declaring work
  order for every unresolved declaration, and one `W024` maintenance warning per
  accepted exemption including those granted by the compatibility set.
- Re-scope the six-identifier compatibility set in the candidate validator and in
  `.github/scripts/publish_dashboard.py` as an explicitly frozen self-hosting set,
  closed to additions, and apply the same `W024` to it.
- Add `tests/test_legacy_release_evidence.py` and the shared canonical vector
  fixture under `tests/fixtures/legacy_release_evidence/`, covering every case in
  `VER-LRE-001`'s matrix.
- Update the assertion in `tests/test_release_bootstrap.py` that depends on the
  shape of the compatibility-set constant.
- Document the declaration, the `W024` code and the refusal in
  `docs/notes/harness-installation-and-upgrades.md`, and register the domain in
  `docs/engineering/README.md`.

## Out of scope

- Editing `scripts/validate_engineering_artifacts.py` or any other managed root
  copy. Those belong to the exact released version recorded in
  `.engineering-harness.toml` and are hash-locked. The change lands only in the
  candidate template.
- Editing any artifact of another domain, including `WO-HUP-002`, `SPEC-REB-001`,
  `REQ-REB-008` and `SPEC-REB-003`. No amendment to those is required: declaring
  that a record predates a rule is not rewriting the record, and a per-record,
  owner-declared, date-guarded set is not the generic fallback `REQ-REB-008`
  excludes.
- Retiring the six-identifier compatibility set, or migrating this repository's
  own history onto the declaration.
- Any change to evaluator-evidence capture, canonical form or hashing, to the
  `ready` record binding written by `prepare-release`, or to the
  predecessor-bootstrap contract.
- Any change to the `prior_lock_sha256` line-ending sensitivity reported alongside
  issue #126. That is a separate defect with its own chain.
- Building, binding, publishing or promoting a distribution, and bumping the
  package version.
- Committing a verification record or a release record. A record cannot contain the
  hash of its own commit.

## Authorized decision envelope

The implementer may choose the internal structure of the resolver, the wording of
diagnostics, the layout of the vector fixture, and the placement of the refusal
within the pre-write region of `apply_changes`, provided the observable behaviour
matches `SPEC-LRE-001`.

The implementer may not choose a different declaration location, a different set
of acceptance conditions, a different bound on declaration size, or a warning code
other than `W024`. The implementer may not add an override, a flag, an environment
variable or a configuration key to any part of this behaviour.

Where the specification and this work order disagree, the specification governs and
the disagreement is a stop condition.

## Constraints

- Treat every declaration member, artifact path, front-matter value and lock value
  as untrusted input. No declaration content reaches a filesystem call, a
  subprocess, an import or an evaluated expression.
- The validator script imports nothing from `se_harness` and remains runnable as a
  standalone file inside a consumer repository.
- The resolver depends only on front-matter parsing and the standard library, and
  never on the lock, the installed evaluator identity or any run-time state.
- Authority-granting work-order statuses are derived from the managed workflow
  lifecycle registry, never written as a literal list.
- Existing behaviour is preserved exactly: no existing digest, comparison,
  authorization check, mutation-guard code, replay postcondition or evaluator
  binding check changes.
- The two implementations must agree on every shared canonical vector, asserted by
  test rather than by inspection.
- No file is written by a refused upgrade.
- Line endings of committed files follow the repository's declared byte rules; new
  test fixtures are written with explicit newlines rather than platform defaults.
- Do not push, open a pull request, tag, publish, or run any command that contacts
  an external service.

## Expected change surface

One new package module and one new test module. Additive changes to the packet
contract, the installer's pre-write region, the upgrade CLI's planning output, the
candidate validator's constants and release-record path, and the dashboard
publisher's legacy check. One assertion updated in an existing test module. Two
documentation files and the domain index. The complete governing packet for this
domain.

No managed root file, no released record, no verification record, no other
domain's artifact, and no packaging metadata is expected to change. If the change
requires touching a path outside the declared execution scope, that is a stop
condition.

## Required verification

- Full suite: `python -m unittest discover -s tests -p "test_*.py"`, with the
  count, skips, platform and Python version recorded, and no new failure against
  the recorded baseline.
- Graph: `python scripts/validate_engineering_artifacts.py --root .` passes, with
  before-and-after error and warning counts recorded.
- Candidate graph: the patched candidate validator run over this repository, with
  its error and warning counts recorded and the six compatibility-set `W024`
  entries identified.
- `python scripts/validate_release_distributions.py --root .`,
  `python -m se_harness --help`, and `python -m se_harness doctor .`.
- Phase-appropriate `python -m se_harness preflight . --work-order WO-LRE-001`.
- Every negative case in `VER-LRE-001`'s matrix, with its exact diagnostic text.
- The refused-upgrade case, with a tree digest before and after proving byte
  identity, and the planning case showing a notice and exit status zero.
- The cross-implementation equivalence result over the committed vector fixture.
- The end-to-end reproduction against the consumer repository from issue #126 at a
  recorded commit: upgrade applied, patched candidate validator passing with
  exactly one `W024`, and `RLS-MOK-001` front matter shown byte-identical.

## Evidence to record

Retain under `docs/engineering/legacy-release-evidence/evidence/` everything
`VER-LRE-001` requires, and in particular: the baseline and post-change counts for
tests and for both validators; the complete diagnostic text of every negative
case; the vector fixture and both implementations' results over it; the
refused-upgrade transcript with before-and-after tree digests; the end-to-end
reproduction with the consumer repository's commit, its upgrade transcript, its
passing validation output and its unchanged record front matter; and an explicit
list of actions not performed, naming at least the absence of any push, pull
request, tag, build, release, publication and consumer upgrade.

## Stop and escalate conditions

Stop and escalate to the accountable owner when: the change would require editing
a managed root file, a released or verified record, or another domain's artifact;
the specification and an existing approved artifact in the
`released-evaluator-boundary` domain turn out to conflict in substance rather than
in appearance; a path outside the declared execution scope must change; the
existing test baseline cannot be held; the two implementations cannot be made to
agree without changing the specification; the end-to-end reproduction does not
resolve to a pass with exactly one `W024`; or a release, publication or external
action appears necessary to complete the work.

## Completion report format

Report: the exact commit implemented; each file changed with the reason; the
observable behaviour added, stated as the specification rules it satisfies; the
full verification results with counts, platform and Python version; every negative
case with its diagnostic; the end-to-end reproduction result; anything in scope
that was not done and why; and the explicit list of actions not performed.
