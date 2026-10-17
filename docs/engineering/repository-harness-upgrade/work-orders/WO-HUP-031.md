+++
id = "WO-HUP-031"
type = "work_order"
title = "Adopt released evaluator 0.23.0"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-17"
updated = "2026-10-17"

[execution_scope]
paths = [
  ".engineering-harness.toml",
  ".engineering-harness.lock",
  ".github/workflows/engineering-harness.yml",
  "pyproject.toml",
  "se_harness/__init__.py",
  "README.md",
  "docs/engineering/README.md",
  "docs/engineering/self-hosting-boundary/SELF_HOSTING.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/release-0-23-0/README.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/harnessctl-reference.md",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-031.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-026.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-031/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-031-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-029.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-029-evaluator.json"
]

[assurance]
commit_bound_verification = "required"
rationale = "The repository evaluator selection, CI pin, source version boundary and current instructions change trusted state used by later decisions."
decided_by = "mmzen"

[relations]
implements = ["REQ-REB-027", "REQ-IAR-031"]
specifications = ["SPEC-REB-012", "SPEC-IAR-016"]
architecture = ["ARCH-REB-011", "ADR-REB-011", "ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-17T09:49:41Z"
decided_by = "mmzen"
reason = "mmzen approved implementation and review publication for repository/CI adoption of public 0.23.0, development source 0.23.1, the named documentation/test changes, required commit-bound verification, review pushes/draft PR codex/adopt-0-23-0 to mmzen/se_harness:main and the later verification-decision push. Human verification, merge and host-plugin updates remain separate."
scope_paths = [".engineering-harness.toml", ".engineering-harness.lock", ".github/workflows/engineering-harness.yml", "pyproject.toml", "se_harness/__init__.py", "README.md", "docs/engineering/README.md", "docs/engineering/self-hosting-boundary/SELF_HOSTING.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/release-0-23-0/README.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/release-delivery-completion.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/harnessctl-reference.md", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-031.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-026.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-031/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-031-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-029.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-029-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-17T09:52:31Z"
decided_by = "codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved adoption under mmzen authority."
+++

# Adopt released evaluator 0.23.0

## Objective

Use public evaluator 0.23.0 for this repository, its instructions and CI.
Preserve owner files and historical artifacts. Advance development source to
unpublished 0.23.1 so candidate CI can distinguish it from the released evaluator.
Human mmzen requested "Go repository adoption" after the verified release
closeout merged. This draft makes the exact changes and assurance request reviewable.

## Exact inputs

- Base: `ed29d435f37b5c2c8b81b1e1375d504edc98787a`, merged PR #548.
- Current selection: 0.22.1, schema 5, `released-resources-v1`.
- Release: RLS-SEH-034, candidate `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15`.
- Wheel: `se_harness-0.23.0-py3-none-any.whl`.
- Wheel SHA-256: `ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c`.
- Payload SHA-256: `8b5671743d56fceb81bf6117fca97c807f407bafaf9137d629ac60b91ffa14b6`.
- Independent public-delivery assurance: verified VREC-RLS-005, merged in PR #548.

## In scope

1. Reuse the separately installed, digest-checked public 0.23.0 environment.
   Keep released 0.22.1 as the governor until the authorized upgrade applies.
2. Recheck and apply the two-file installer plan. Retain its canonical transaction.
3. Change the owner CI pin to 0.23.0. Preserve its checked-wheel installation
   and provider controls. Change both development version declarations to 0.23.1.
4. Correct current release/adoption statements in the named guides and indexes.
   Link public delivery and verification. Preserve historical observations and
   immutable published README snapshots. Describe the observed Codex update recovery
   without claiming that its timed-out normal update attempts passed.
5. Update the existing refresh-guidance test to the 0.23.0 / 0.2.7 public receipts.
   Keep independently specified expected identities and negative cases for wrong
   versions, missing or contradictory observations, false claims and broken links.
   Adjust cases that currently assume candidate and public versions always differ.
6. Run VER-HUP-026, activate the adopted checkout for this session, retain checks,
   record completion and prepare commit-bound verification for human review.

## Expected change surface

| Files | Purpose and limit |
| --- | --- |
| `.engineering-harness.toml`, `.engineering-harness.lock` | Installer-owned selection changes; no manual lock edit. |
| `.github/workflows/engineering-harness.yml` | Only the evaluator version pin. |
| `pyproject.toml`, `se_harness/__init__.py` | Matching unpublished 0.23.1 source versions; no runtime behavior change. |
| `README.md`, `docs/engineering/README.md`, `docs/engineering/self-hosting-boundary/SELF_HOSTING.md` | Current public release, selected evaluator and development boundary. |
| `docs/engineering/repository-harness-upgrade/README.md`, `docs/engineering/release-0-23-0/README.md` | Adoption and completed delivery links; preserve prior decisions. |
| `docs/notes/developing-se-harness.md`, `docs/notes/harness-installation-and-upgrades.md`, `docs/notes/harnessctl-reference.md` | Current version, released command availability and adoption guidance. Preserve the separate service pin. |
| `docs/notes/release-delivery-completion.md`, `docs/notes/plugin-installation-guide.md`, `docs/notes/plugin-marketplace-publication.md` | Actual public delivery status and supported installation/update guidance, with existing limitations. |
| `tests/plugin_integration/package_assembly/test_refresh_guidance.py` | Current public identities and evidence; preserve meaningful negative assertions. |
| WO-HUP-031, VER-HUP-026 and `evidence/WO-HUP-031/` | This proposal, actual checks, preparation review, handoff and completion evidence. |
| `evidence/WO-HUP-031-evaluator-upgrade.json` | Fixed installer transaction destination required by predecessor CI. |
| `verification-records/VREC-HUP-029.md`, `evidence/VREC-HUP-029-evaluator.json` | Proposed fixed capture outputs, relative to this domain. |

The installer preview preserves `.gitattributes`, `.gitignore`, the PR template
and CI. The CI pin is a separately declared owner edit. The proposed VREC ID is
unused across fetched local Git refs. Recheck before capture; resolve any collision
before writing. No unnamed generated destination is assumed to be covered.

## Constraints and exclusions

Use the normal upgrade transaction and existing definitions. Add no new mechanism
or copied instructions. Preserve pre-existing formal artifacts and evidence bytes,
except the explicitly named current documentation. Do not amend HAG definitions:
the private service remains pinned to 0.22.1, and Git remains authoritative.

Host-plugin installation, live Claude/Codex sessions, desktop qualification,
performance work, publication, tags, deployment and provider settings are excluded.
Keep R23-NATIVE-010/011 open under DEC-RLS-010 / RISK-RLS-008 and desktop unverified
under DEC-RLS-011 / RISK-RLS-009. Adoption supplies no new test pass or risk waiver.

## Required verification and evidence

VER-HUP-026 defines the checks. Required commit-bound verification is proposed
because later decisions rely on the evaluator selection, CI and current instructions.
The human must confirm this classification with approval; no `assurance.decided_by`
is invented during drafting. Retain commands, working directories, identities,
exits, skipped checks, failures and recovery under `evidence/WO-HUP-031/`.
Preparation rehearsals do not replace checks on the actual adoption candidate.

## Authorized decision envelope

Proposed approval covers this work order, VER-HUP-026, required commit-bound
verification, local execution and checks, completion, session activation and
verification preparation. Codex may choose disposable paths and internal helpers.
The target must be the independently released wheel named above.

The proposal includes ordinary review pushes and a draft PR from
`codex/adopt-0-23-0` to `mmzen/se_harness:main`, covering these artifacts, the
implementation, evidence and ready VREC. It includes the later decision-only push
and marking the PR ready after the human verification is recorded remotely.
Human verification acceptance and merge remain separate. This draft is not approval.

## Stop conditions and completion

Stop for a changed public identity, unexpected installer write, owner conflict,
failed required check, uncovered path or generated-output collision. Preserve
failures and inspect uncertain effects before retries. New product corrections
need their own bounded review; do not weaken checks or change comparison bases.

Report the selected release, actual changed files, source/CI versions, preservation
results, candidate, checks, limitations and evaluator-selected next decision.
One work order and one verification contract reuse the existing upgrade rules.
