+++
id = "WO-ECP-007"
type = "work_order"
title = "Evict the bootstrap bridge and this repository's identifiers from the product"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work deletes shipped modules, hash-bound classes, CI workflows, and the constant that exempts this repository's own release records. Consumer installs, this repository's validator, and every later release decision rely on exact candidate behaviour, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/hash_bound_classes.json",
  "se_harness/hash_bound.py",
  "templates/repository/standard/gitattributes.fragment",
  "se_harness/governance_migration.py",
  "se_harness/governance_migration_contract.py",
  "se_harness/governance_migration_contract.json",
  "se_harness/recovery_rehearsal.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/release_qualification.py",
  "se_harness/legacy_release_evidence.py",
  "se_harness/integrity.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  "repository_tools/",
  "scripts/validate_governor_transition.py",
  "scripts/prepare_predecessor_release.py",
  "scripts/assess_predecessor_evaluator.py",
  "scripts/bind_release_bootstrap.py",
  "scripts/validate_predecessor_publication_view.py",
  "scripts/check_portable_release_surface.py",
  ".github/workflows/",
  ".gitattributes",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "docs/engineering/released-evaluator-boundary/",
  "docs/engineering/legacy-release-evidence/",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-012", "REQ-ECP-013"]
specifications = ["SPEC-ECP-007"]
verification = ["VER-ECP-007"]
+++

# Work Order: Evict the bootstrap bridge and this repository's identifiers from the product

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-012`,
`REQ-ECP-013`, `SPEC-ECP-007`, and `VER-ECP-007` are separate acts by their
owners and precede approval of this work order. This work order is
independent of the others in the packet. The supersession it records is a
separate act by the technical owner or requirements steward who owns the
superseded artifact.

## Objective

Ship only what a consumer repository needs. Today `init`, a commit, then
`doctor` exits 1 in every fresh repository because
`se_harness/hash_bound_classes.json:19-32` declares the
`governance-migration-protocol` class and
`templates/repository/standard/gitattributes.fragment:4-6` pins files that
exist only here (complexity audit P0-1,
`docs/notes/complexity-audit-2026-08.md:97-124`); `qualify
predecessor-view` in the wheel imports the unpackaged `repository_tools`;
six `RLS-SEH-*` identifiers are hard-coded in
`se_harness/legacy_release_evidence.py:30-36`, the template validator, and
`.github/scripts/publish_dashboard.py:76` (audit P1-2; the 2026-08 agentic
execution review, section 5, weakness 5).

## In scope

- Removal of the `governance-migration-protocol` hash-bound class and the
  three fragment lines; `hash_bound.py` treating a pattern that matches no
  tracked path as a warning or as `repository`-region only, per
  `ECP-PRD-*`; this repository's own LF pins moved into its `.gitattributes`
  outside the managed block.
- Removal of the migration stage machine, its contract and JSON, the
  recovery rehearsal, `validate_governor_transition.py`, the predecessor
  scripts, the `accept-candidate` alias, and lock schema-1 write paths;
  `qualify` reduced to the consumer-usable operations with the two
  self-checks moved under `repository_tools/`; `.github/workflows/` and
  `scripts/check_portable_release_surface.py` updated for the removed
  lanes.
- The six-identifier constant deleted from `legacy_release_evidence.py`,
  `installer.py`, `cli.py`, and the template validator; the exemption
  declared through data in this repository per `SPEC-LRE-001`'s own rule 5
  mechanism.
- Amendment records, each a trailing `## Amendment record` section with no
  front-matter change, in the form of
  `docs/engineering/release-orchestration/architecture/ARCH-RLO-004.md:118-128`:
  - `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-009.md`:
    the five-operation `qualify` namespace is superseded by `ADR-ECP-005`;
    the retained operations are named.
  - `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-002.md`,
    rule 14 ("Disposable rehearsal", line 70): satisfied by a real installer
    test rather than `recovery_rehearsal.py`, as `ADR-ECP-005` records.
  - `docs/engineering/legacy-release-evidence/specifications/SPEC-LRE-001.md`,
    rule 11 ("Self-hosting compatibility set", line 138): the six identifiers
    are declared through repository data, not product code, as
    `ADR-ECP-005` records.
- Formal supersession of `ADR-REB-009`, by its owner through
  `harnessctl transition ADR-REB-009=superseded` under the released
  evaluator once `ADR-ECP-005` is active, `--reason` naming the successor.
  `SPEC-REB-002` and `SPEC-LRE-001` have no superseding ECP artifact and
  receive the amendment record only.
- Tests, including the fresh-consumer demonstration on both platforms;
  work-order-keyed evidence.

## Out of scope

- The shipped skills and the manifest (`WO-ECP-008`); the root managed
  `scripts/validate_engineering_artifacts.py` and the lock (the template
  copy is edited); rewriting any historical release, verification, or
  evidence record; approving any ECP artifact; editing front matter of an
  amended artifact; any change to lifecycle states, gate predicates, or
  decision rights.

## Authorized decision envelope

The implementation agent may decide which `qualify` operations survive as
consumer-usable within the two named by the audit, the data form of the
exemption under `SPEC-LRE-001` rule 5, the amendment prose, and test names.
It may not keep an `RLS-SEH-` literal in shipped code, keep a hash-bound
class that fails on absence, apply the supersession itself, or write
outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, preflight, and the
  supersession transition; the released evaluator still carries the
  constant, so this repository's validation under it is unchanged by this
  work.
- Root managed copies are not edited.
- LF line endings; assert bytes against blobs; the moved LF pins are
  measured against the `-text` evidence tree.
- Stage every deletion before any preflight or check run;
  `hash_bound.assess` reads index-tracked paths.

## Expected change surface

Two hash-bound declarations and one fragment, eleven product modules
(several deleted), `repository_tools/`, six root scripts, the CI workflow
directory, `.gitattributes`, the template validator, three amended
artifacts across two domains, tests, evidence.

## Required verification

Execute `VER-ECP-007` completely for `REQ-ECP-012` and `REQ-ECP-013`
(Scenarios 1 to 4 and the corresponding property, static, and security
checks) plus the repository-required checks; run the complete suite on
Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-007/`:
the fresh-consumer transcript per platform, `doctor` output, identifier
grep inventories before and after, the wheel `RECORD`, the supersession
transition result, the amendment diffs, per-platform test figures, and the
complete changed-path set.

## Stop and escalate conditions

Stop if the six historical records cannot stay exempt through data under
the released evaluator, if a removed lane is still referenced by a release
record's recipe, if the released evaluator refuses the supersession, if an
amended artifact's front matter would have to change, or if any path
outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-007 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
