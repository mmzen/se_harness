+++
id = "WO-ECP-010"
type = "work_order"
title = "Replace the governance-migration rehearsal with a real upgrade rehearsal"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The work deletes the migration stage machine and its self-hashing contract, replaces the release-qualification lane that every candidate runs on both platforms, and retires three approved definitions by dated amendment. A wrong change either leaves the candidate lanes red or removes the only rehearsal of a root-evaluator handover; both are trusted engineering state that later release decisions depend on, so verification must bind the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/governance_migration.py",
  "se_harness/governance_migration_contract.py",
  "se_harness/governance_migration_contract.json",
  "se_harness/interpreter_safety.py",
  "se_harness/interpreter_safety.json",
  "se_harness/cli.py",
  "pyproject.toml",
  "repository_tools/",
  "scripts/check_portable_release_surface.py",
  ".github/workflows/candidate-evidence.yml",
  ".gitattributes",
  "tests/",
  "docs/notes/",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-016.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-017.md",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-029.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-008.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-013.md",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-007.md",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-012"]
specifications = ["SPEC-ECP-007"]
architecture = ["ARCH-ECP-001", "ADR-ECP-005"]
verification = ["VER-ECP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T13:28:15Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve WO-ECP-010, go', for repository issue #210. Authorizes only the listed execution scope: the repository-owned upgrade rehearsal and its CI lane, the evaluator_facts rename without the scenario coupling, deletion of the governance-migration stage machine, its contract, tests, fixtures, the rehearse-migration subcommand, the MIG family and the package interpreter-safety module, the .gitattributes owner lines, the dated amendments to REQ-REB-016, REQ-REB-017, SPEC-REB-008, REQ-REB-029 and SPEC-REB-013, the narrowing of WO-ECP-007, the notes, tests and evidence. Start, completion, commit-bound verification and release are separate decisions."
+++

# Work Order: Replace the governance-migration rehearsal with a real upgrade rehearsal

## Lifecycle

Draft. Approval authorizes only the scope below. Start, completion,
commit-bound verification, the assurance-owner decision, integration, and
release are separate decisions by the roles that own them. `REQ-ECP-012`,
`SPEC-ECP-007`, `ARCH-ECP-001`, `ADR-ECP-005`, and `VER-ECP-007` are
approved; this work order carries the part of `ECP-PRD-008` that concerns the
migration rehearsal, split out of `WO-ECP-007` on 2026-08-28 for repository
issue #210 so that it is not held by the other evictions that work order
bundles. It depends on nothing; `WO-HBI-005` (merged) already stopped
shipping the `governance_migration*` byte rules this work order deletes the
files for.

## What was found, and by what

Repository issue #210, from finding P0-4 of the 2026-08 complexity audit at
`f0ecd9b`. `harnessctl rehearse-migration` probes two interpreters, then runs
nine stages against a JSON toy graph in a temporary directory; its validation
asserts `schema == 3` and `evaluator_evidence is True`; the predecessor
interpreter does nothing beyond printing its identity. The contract JSON
embeds the module's own `implementation_sha256` six times, the only JSON under
`se_harness/` that embeds a digest of a Python module, so every edit is a
two-file change. `repository_tools/predecessor_facts.derive` fails `PRE009`
unless a hand-authored scenario for the exact predecessor-to-candidate pair
exists under `tests/fixtures/governance_migration/`, so every version bump is
a scenario-authoring ritual (`MIG211`, `WO-REB-023`). The rehearsal's
`semantic_sha256` moves with the commit, so "two replays agree" is only ever
an intra-run check. The guarantee the ritual documents, that the released
predecessor governs until a separately authorized adoption, is enforced by
`mutation_guard` and the lock, not by the toy graph.

## Objective

Make the migration lane rehearse the real handover: the successor's own
`harnessctl upgrade --apply` against a throwaway copy of this repository
holding the released predecessor's lock, judged by both evaluators' `doctor`
and by the resulting lock, on Linux and Windows, with no per-release scenario
and no self-hashing contract.

## In scope

- `repository_tools/upgrade_rehearsal.py`, a repository-owned rehearsal of
  about one hundred lines, with a `python -m repository_tools.upgrade_rehearsal`
  entry point taking `--repository`, `--predecessor-python`,
  `--successor-python`, `--output`. It exports the tracked tree of the
  repository to a throwaway directory (never the operational checkout), runs
  the predecessor evaluator's `doctor` there and requires it to pass, runs the
  successor's `upgrade` plan and then `upgrade --apply --evidence-output`,
  runs the successor's `doctor` and `validate` and requires zero failures and
  zero errors, runs the predecessor's `doctor` again and requires it to fail
  (the released predecessor no longer owns the root), and asserts that the
  resulting `.engineering-harness.lock` is schema 3 naming the successor's
  version and installed-payload digest. It writes one result JSON whose
  `semantic_sha256` is the canonical `utf8-text-lf-v1` digest of the
  resulting lock, the value the two platforms must agree on, and exposes no
  network, credential, or checkout mutation.
- `.github/workflows/candidate-evidence.yml`: the `governance-migration` job
  keeps both platforms, the exact predecessor and successor wheels, the two
  runs, and the cross-platform digest comparison, and invokes the new
  rehearsal instead of `rehearse-migration`; the scenario inputs and the
  `MIGRATION_SCENARIO*` outputs are removed.
- `repository_tools/predecessor_facts.py` renamed `evaluator_facts.py`, its
  scenario coupling (`PRE009` to `PRE012`, `write-scenario`, `load_scenario`,
  `_retarget`) removed, `derive` and `released_evaluator_archive` kept, and
  the `candidate-source` job updated to the new module name.
- Deletion of `se_harness/governance_migration.py`,
  `se_harness/governance_migration_contract.py`,
  `se_harness/governance_migration_contract.json`,
  `tests/test_governance_migration.py`, `tests/fixtures/governance_migration/`,
  the `rehearse-migration` subcommand and its `MIG*` diagnostic family, and
  `se_harness/interpreter_safety.py` with `se_harness/interpreter_safety.json`
  and their `pyproject.toml` package-data entry, whose only product caller was
  the deleted module (`repository_tools/interpreter_safety.py` is issue #220
  and is not touched). `scripts/check_portable_release_surface.py` and the
  tests that name the deleted surface are retargeted; the retired
  `rehearse-migration` name and the `MIG` family are reserved, never reused.
- The three `se_harness/governance_migration*` and
  `tests/fixtures/governance_migration/*` rules removed from the owner region
  of `.gitattributes`.
- Dated retirement amendments, in the form `WO-REB-028` used, to
  `REQ-REB-016`, `REQ-REB-017`, and `SPEC-REB-008`; dated amendments to
  `REQ-REB-029` and `SPEC-REB-013` naming the upgrade rehearsal as the one
  predecessor-to-successor mechanism; the domain index line.
- `WO-ECP-007` narrowed: the migration stage machine, its contract and JSON
  leave its scope; the domain index and ordering updated.
- Notes: `docs/notes/evaluator-migration-rehearsal.md` rewritten for the
  upgrade rehearsal; `developing-se-harness.md`, `ci-pipeline.md`,
  `harnessctl-reference.md`, `release-qualification-roles.md`,
  `harness-dashboard-publication.md`, `harness-installation-and-upgrades.md`
  corrected where they name the retired command.
- Tests: the rehearsal against a fixture repository whose lock names an
  older evaluator, on an LF and a `core.autocrlf=true` checkout; the negative
  cases (predecessor `doctor` failing before, successor `doctor` or `validate`
  failing after, the lock not naming the successor); the absence of the
  deleted surface and of any module digest in a `se_harness/` JSON file; the
  CI workflow shape. Work-order-keyed evidence.

## Out of scope

- `recovery_rehearsal.py`, the `accept-candidate` alias, lock schema-1 write
  paths, `validate_governor_transition.py`, `qualify`, and the six release
  identifiers (`WO-ECP-007`); `repository_tools/interpreter_safety.py` (#220);
  any root managed file; any historical release, verification, or evidence
  record; `SPEC-REB-002` rule 14; any lifecycle transition of any artifact;
  any change to `mutation_guard`, the installer, or the lock format.

## Authorized decision envelope

The implementation agent may decide the rehearsal's result-file fields
beyond `semantic_sha256`, how the tracked tree is exported (a `git archive`
or an index-driven copy, never the operational checkout), the reserved-name
test's form, and the wording of the retirement amendments. It may not weaken
any assertion listed under In scope, keep any part of the stage machine or
its contract, add a network or credential dependency to the rehearsal, or
write outside the listed paths.

## Constraints

- Python 3.11+ standard library only; the rehearsal runs both evaluators
  with `-I` from their own environments and inherits no `PYTHONPATH`.
- The rehearsal never writes to the operational checkout; the CI job keeps
  its "no checkout change" proof.
- Use the exact released evaluator, installed outside the checkout, for
  identity, integrity, graph, focus, preflight, and the handoff check; the
  candidate rehearsal is exercised only against throwaway copies.
- Root managed copies are not edited; LF line endings.
- Stage every change before any preflight or check run.

## Expected change surface

One new repository-owned module and its tests; one renamed module; one
workflow job; the CLI parser; three package files and two JSON contracts
deleted with their tests and fixtures; `.gitattributes` owner lines; five
REB artifacts by dated amendment; one draft work order narrowed; seven
notes; evidence.

## Required verification

Execute the `VER-ECP-007` rows that name `REQ-ECP-012` and `ECP-PRD-008`
plus the repository-required checks; the candidate lanes green on Linux and
Windows with the new rehearsal, its two runs agreeing on `semantic_sha256`
per platform and across platforms; run the complete suite on both platforms
with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-010/`: the
rehearsal's result JSON from each platform and both runs, the deleted-surface
inventory, the negative-case transcripts, the retirement amendments' list,
per-platform test figures, and the complete changed-path set.

## Stop and escalate conditions

Stop if the successor's `upgrade --apply` cannot run against the exported
copy without a change to `mutation_guard` or the installer, if the
cross-platform lock digests disagree for a reason other than a rehearsal
defect, if a consumer of `rehearse-migration` or of the migration contract
is found outside this repository's tests and notes, or if any path outside
scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-010 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
