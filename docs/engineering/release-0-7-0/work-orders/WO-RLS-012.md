+++
id = "WO-RLS-012"
type = "work_order"
title = "Qualify and build the final se-harness 0.7.0 candidate from main"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package installation, managed-policy upgrade, recipe-bound build replay, credential-free publication and future evaluator decisions rely on the exact candidate, its retained evidence and its reproducible distributions."
decided_by = "repository-owner"

[execution_scope]
paths = ["docs/notes/developing-se-harness.md", "docs/engineering/README.md", "docs/engineering/release-0-7-0/"]

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T20:59:09Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-26 with the words 'I approve WO-RLS-012', as a decision distinct from the approval of REL-SEH-017. Approval authorizes start preflight and then only the declared qualification, recipe-bound reproducible-build, index-maintenance and retained-evidence work inside the three declared execution-scope paths. Re-measured immediately before this transition over branch state f310024 carrying unmoved main be2f0cf: ninety-seven implemented unreleased work orders, fifty-two of them members of REL-SEH-017's gates and forty-five excluded by name-class; no ready record beyond the two canonical templates; validate PASS at 952 artifacts, 0 errors, 50 pre-existing maintenance warnings; doctor 0 FAIL. Approval authorizes no contract approval, no candidate commit, no VREC-SEH-014 or RLS-SEH-014 work, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator upgrade. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T20:59:40Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-26, 'you can then start WO-RLS-012'. Start preflight PASS at phase start over branch state 6d5aeab carrying unmoved main be2f0cf, run with the governing exact public 0.6.0 evaluator outside the checkout. REL-SEH-017 is approved, so its fifty-three-work-order gates array is fixed authority and this work order's deferred census resolves to it. Bounded to the three declared execution-scope paths. This start authorizes no candidate commit, no promotable build beyond the declared recipe-bound reproducibility work, no VREC-SEH-014 or RLS-SEH-014 preparation or transition, no tag, no publication, no deployment, no maintenance-line mutation, no credential use and no root-evaluator change."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T21:20:24Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-26 under DR-WO-COMPLETE, 'mark WO-RLS-012 implemented', on the handoff gate reading Completed over candidate commit 24cf7c767583e83b9056d03d7dd5de6622fef91c, tree 05b0e6dd2b39da89180e4712a5a2fdc6d2f861f4, formal snapshot 685a2400d0e04bdc4f6dbf6ce2d2c677352691e48b570bbda565f673f8d8b08b, change set asserted complete over the one changed path, the keyed evidence. Exact-candidate readings, governing exact public 0.6.0 evaluator outside the checkout in isolated mode: validate PASS at 952 artifacts, 0 errors, 50 pre-existing maintenance warnings, every plane E0; doctor 87 PASS 0 FAIL; review preflight PASS; upgrade plan 36 unchanged; release-distribution validation PASS; portable surface PASS; governor succession plan passed with transition required false; recovery rehearsal PASS; governance migration rehearsal 0.6.0 to 0.7.0 pass and compatible; Explorer deterministic. Build of record through the pinned linux/amd64 producer on this workstation via Docker Desktop: state exact, two byte-identical builds, wheel 4d0589fded5c3da4f247c3f54e4204334ad283ea6b90f6dcc67c559726f557ca, sdist d05541fd94a3d444da20bb539eb6ca211ae10e1ccb0ff04a0f1628ec7e111f6c. Released 0.6.0 verifier black-box acceptance ten of ten on that wheel. Suites: Windows CPython 3.14.6 and 3.11.9 both 995 tests OK with 24 platform-guard skips at full scale; hosted Linux 995 tests OK with 4 skips. All four pull-request lanes success on head 24cf7c7. Census re-derived from REL-SEH-017 at the candidate: 53 members, 24 verification contracts, 65 requirements, 58 keyed evidence paths. Three deviations accepted by the owner and recorded in the evidence; VREC-IPK-001's merge-preview bound commit carried as residual risk. This authorizes no further act."
+++

# Work Order: Qualify and build the final se-harness 0.7.0 candidate from main

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp and
reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It is the successor to `WO-RLS-011` for the
remaining release work and is governed by `REL-SEH-017`, which names it in
`gates`.

On 2026-08-26 the repository owner instructed that 0.7.0 must contain
everything currently on `main` and follow the complete release process, and
that the previous attempt on pull request #169 is closed unmerged. Put three
measured options, the owner chose the payload-bearing verified unit,
the allow-list contract form, and succession of `WO-RLS-011` by this work
order. The owner also chose to reject `WO-RLS-011`; the governing workflow
contract admits only `verified` or `released` from `implemented` (`WEX201`),
so `WO-RLS-011` stays `implemented`, remains a member of the unit, and is
covered by the aggregate record. This work order does not repeat its work.

What `WO-RLS-011` already did, and this work order inherits from `main`: the
0.7.0 identity in `pyproject.toml`, `se_harness/__init__.py` and `README.md`;
the retargeted fixture in `tests/test_release_qualification.py`; the
`release-0-7-0/` entry in the engineering domain index; the current-candidate
statements in `docs/notes/developing-se-harness.md`; and the two-stage
qualification evidence in
`docs/engineering/release-0-7-0/evidence/WO-RLS-011-verification.md`. `main`
has since gained the migration scenario for 0.7.0 (`WO-REB-023`) and sixteen
further members; none of `WO-RLS-011`'s files needs to move again unless
re-measurement at the candidate says otherwise.

Approval authorizes start preflight followed by only the declared
qualification, recipe-bound reproducible-build, index-maintenance, and
retained-evidence work within the three declared execution-scope paths.
Approval explicitly does not authorize `REL-SEH-017`'s approval, the candidate
commit, `VREC-SEH-014` or `RLS-SEH-014` preparation or transition, branch push,
tag creation or movement, GitHub or PyPI publication, Pages deployment,
maintenance-line mutation, credential use, external policy change, or
root-evaluator upgrade.

Commit-bound verification is classified `required` because the release owner,
the assurance owner, consumers, publication automation, the recipe interpreter,
and future repository upgrades will rely on the exact integrated package,
standard template, evaluator boundary, provenance, and distribution bytes.

## Objective

Produce one clean, fully qualified 0.7.0 candidate cut from `main` containing
exactly the fifty-three work orders `REL-SEH-017` names in `gates`, with
consistent version identity, one standard installation, independently proven
evaluator, candidate-source and candidate-package roles, recipe-bound
reproducible distributions built twice byte-identically, a release bundle
manifest, complete retained evidence, and exact aggregate verification inputs.
Stop after an implemented candidate and retained evidence unless later
authority permits the candidate commit and `VREC-SEH-014` preparation.

## Aggregate scope

The release unit is exactly what `REL-SEH-017` names in `gates` at its
approval. Every derived aggregate is re-measured against the candidate and
recorded as a measured figure. Dated observation at drafting, over `main` at
`be2f0cfec18b86d273400466cdf1c8c691d92f75`: fifty-three work orders,
twenty-four verification contracts, a sixty-five-requirement union, fifty-eight
keyed evidence paths (fifty-seven existing plus the one this work order
retains). These are observations, not scope.

Fixed regardless of the census:

- New evidence:
  `docs/engineering/release-0-7-0/evidence/WO-RLS-012-verification.md`, one
  file, two stages (working tree, then exact candidate), as `WO-RLS-011`'s
  evidence is structured and for the same reason: the file is committed inside
  the candidate it describes and cannot name that commit.
- Planned aggregate record after an authorized clean candidate commit:
  `docs/engineering/release-0-7-0/verification-records/VREC-SEH-014.md`.
- Planned release record after verified aggregate assurance and separate
  release-preparation authority:
  `docs/engineering/release-0-7-0/releases/RLS-SEH-014.md`.
- Public version and immutable tag: `0.7.0` and `v0.7.0`.

## In scope

After separate approval of this work order:

- Re-derive the release unit from `REL-SEH-017`'s `gates` at the candidate and
  prove the two agree exactly: every member reads `implemented` with verified
  coverage (`WO-RLS-011` excepted, covered by the aggregate record), every
  member's bound verification commit is reachable from the candidate, and no
  work order whose bytes are in the packaged surface is unnamed. Retain
  `harnessctl release-unit . --from v0.6.0 --to <candidate> --json` output as
  the reported census.
- Confirm at the candidate that the packaged surface (an explicitly
  non-promotable ephemeral sdist built outside the checkout is acceptable for
  the measurement) carries no bytes authorized by any of the forty-five
  excluded work orders.
- Carry forward, without softening, the disclosed limitations `REL-SEH-017`
  lists, and record which of the ADS pull-request-lane gaps the candidate's own
  dual-platform run resolves.
- Confirm the version inventory: candidate-bearing surfaces equal 0.7.0, the
  migration scenario declares 0.7.0 as its successor, and historical and
  root-evaluator identities remain truthful. Move nothing that already agrees.
- Preserve the root `.engineering-harness.toml`, `.engineering-harness.lock`,
  `ENGINEERING_HARNESS.md`, and the managed CI workflow as the exact released
  0.6.0 installation.
- Run formal graph, release-distribution, managed-integrity, identity,
  byte-rule inventory, workflow, CLI, package-surface, archive-safety,
  reproducibility, Explorer, recovery, portable-surface, and full
  supported-runtime verification, the suite through
  `python scripts/run_tests.py --scale full` and the canonical serial command
  where a contract requires it.
- Exercise the `qualify` operations applicable to a candidate root and record
  the boundary refusals of the others.
- Under the build authority this approval grants, replay the recipe-bound build
  twice from the exact candidate through `python -m repository_tools.release_build
  replay --repository . --commit <candidate> --version 0.7.0 --output-directory
  <bundle-dir> --result <replay.json>` and prove byte identity, safe archives,
  and reconstruction equivalence; produce the bundle manifest with
  `scripts/create_release_bundle_manifest.py` bound to the candidate's own
  `release/build-recipe.json`; record the manifest identities the schema-2
  binding will consume. The build runs on this workstation through Docker
  Desktop (`linux/amd64`, the digest-pinned producer image); the hand-back step
  is POSIX-only and its absence on Windows is recorded, not worked around.
- Install the exact candidate wheel in fresh isolated environments and run
  verifier-owned black-box acceptance without checkout import fallback.
- Retain exact commands, outcomes, identities, hashes, manifests, changed-path
  ledger, warnings, deviations, residual risks, and unperformed actions in the
  keyed evidence.
- Update the release-0-7-0 domain index for this packet, and the developer
  note only if a version or sequence statement it carries is measured stale.
- Transition only this work order through its authorized lifecycle.

## Out of scope

- Approving `REL-SEH-017`; the candidate commit; preparing or transitioning
  `VREC-SEH-014` or `RLS-SEH-014`; binding the distribution table; the tag;
  publication; deployment; the maintenance line; credential use; root-evaluator
  change. Each is a separate later decision.
- Adding product behavior, or admitting a work order into the unit by any route
  other than rejecting and re-issuing the contract.
- Re-litigating any member's verified coverage or its disclosed limitations.
- Answering issue #142 or changing `unbound_digest_fields`.
- Editing `tests/`, `.github/`, `se_harness/`, `templates/`, `pyproject.toml`,
  or `README.md`: every version-bearing surface already reads 0.7.0 on `main`.
  A measured need to touch one is a stop condition and a scope amendment
  decision, not an edit.
- Rewriting historical VREC, RLS, evidence, release, tag, incident, publication,
  or evaluator facts, or the rejected history of the contracts this packet
  supersedes, or anything on the closed pull request #169.
- Using candidate source or an editable or contaminated install as the root
  evaluator or independent verifier.

## Authorized decision envelope

The implementation agent may choose deterministic temporary directories outside
the checkout, the candidate epoch, the evidence-table layout, and the build host
between this workstation's Docker Desktop and the hosted `candidate`-mode
rehearsal of the candidate's pull request when the workstation replay cannot
complete; the choice and its reason are recorded. It may not reinterpret the
allow-list, change accepted behavior, widen changed paths, alter the root
evaluator identity or lock, decide historical VREC disposition, make accountable
transitions, or perform external release actions. Uncertainty escalates.

## Constraints

- Python 3.11+ standard-library runtime behavior; no runtime dependencies.
- Use the exact independently installed released 0.6.0 evaluator, outside the
  checkout and in isolated mode, for root doctor, preflight, validation, and any
  authorized root lifecycle mutation.
- Keep candidate-source and candidate-package evidence separately identified.
- Label every platform-dependent figure with its platform.
- Write evidence JSON with LF endings as the managed `.gitattributes` rule
  requires.
- Do not write the literal token of the repository-context path `WO-ADS-002`
  retired into any file in this packet; describe the retirement in prose.
- Derive the work-order, requirement, and verification-contract unions from the
  contract's `gates` at the candidate; carry no figure forward.
- Make no candidate mutation after exact-commit replay or aggregate capture.
- Stop if the reviewed packet or candidate changes underneath execution.

## Expected change surface

- `docs/engineering/release-0-7-0/`: this work order, the contract, the domain
  index, the retained evidence, and later separately prepared records.
- `docs/engineering/README.md` only if the domain index is measured stale.
- `docs/notes/developing-se-harness.md` only if a version or sequence
  statement is measured stale.
- Derived build, test, acceptance, replay, and dashboard output only in bounded
  disposable locations outside formal artifact discovery.

## Required verification

- Released-0.6.0 start and review preflight, doctor, formal graph validation,
  inspection, and Explorer observations from outside the checkout in isolated
  mode; no structure, governance, or policy errors; maintenance warnings
  counted and dispositioned.
- Complete supported-runtime suites with exact counts and only explained
  conditional skips; Windows platform-guard skips expected; the hosted Linux
  lane runs the same suite without them at full scale (`WO-TST-003`).
- Candidate-source, candidate-package, and released-evaluator identities and
  isolation.
- Exact version inventory, package and template parity, payload manifest,
  wheel archive identity, mutation-guard coverage, hash-bound class
  completeness, byte-rule inventory coverage, workflow and gate contract
  parity, operating-card bound.
- Governor-succession assessment proving the released 0.6.0 evaluator governs
  the 0.7.0 candidate root without a version-specific exception.
- Credential-free publication rehearsal on both runner platforms.
- Two recipe-bound replays byte-identical at one epoch; safe, equivalent
  archives; the reconstructed wheel equal to the direct wheels and passing
  fresh Python 3.11 operation.
- Bundle manifest, checksums, source manifest, candidate commit, tree and
  epoch, Git ancestry including every member's bound verification commit,
  changed-path ledger, secret and private-path scan, and `git diff --check`.
- Aggregate VREC inputs: exactly the work-order set `REL-SEH-017` names, its
  derived verification contracts, its keyed evidence paths, one clean candidate
  commit, one artifact snapshot, matching evaluator evidence — all three counts
  measured at the candidate.

## Evidence to record

`docs/engineering/release-0-7-0/evidence/WO-RLS-012-verification.md`: the
baseline and candidate commit, tree and epoch; the allow-list and exclusions as
the contract names them at approval; every work order that landed after this
packet was written and its disposition; the reported commit census; the version
inventory; evaluator, source and package origins; commands and exit results;
test counts per platform; graph planes; managed-root integrity; recipe identity
and both replay hash sets; reproducibility; the acceptance manifest; the bundle
manifest identities; hosted run, job and artifact identities; warnings;
deviations; residual risks; and every unperformed transition or external action.

## Stop and escalate conditions

Stop on packet or scope change, a work order whose bytes are in the packaged
surface and which the contract does not name or which holds no verified
coverage at aggregate capture, an approved contract whose `gates` no longer
describes the unit, a member whose bound verification commit is unreachable
from the candidate, missing keyed evidence, an unresolved historical `ready`
record, an invalid graph, failed preflight, version drift, root evaluator or
lock change, candidate contamination, unsafe path or archive, a failed required
check, an unexplained warning, nondeterminism between the two replays, package
or template divergence, candidate mutation after exact evidence, a hosted lane
that does not run on the expected event, or a need for authority beyond the
approved stage.

## Completion report format

The `harnessctl check . --artifact WO-RLS-012 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set and its `result_sha256`,
followed by: the work-order scope and exclusions as measured from `gates` at
the candidate; every work order that landed during execution and its
disposition; the disclosed limitations and their disposition; the baseline and
candidate identity; the version inventory; evaluator, source and package
origins; root integrity; exact commands and test results with their platforms;
build host, hashes and manifests; the evidence path; the planned aggregate VREC
inputs; deviations and residual risks; and every unperformed commit, push,
verification transition, release preparation and transition, merge, tag,
publication, deployment, maintenance-line, credential, and root-upgrade action.
