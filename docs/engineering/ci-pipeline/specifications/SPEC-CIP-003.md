+++
id = "SPEC-CIP-003"
type = "specification"
title = "Wave 5 pipeline hygiene: one qualification per pull request, one form for each pin, version and name"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Each pull request qualifies and tests its commit once, every repository-owned workflow states each check, pin, version and name once, and Pages deployments queue behind one group."

[relations]
specifies = ["REQ-CIP-008", "REQ-CIP-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:55:49Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all three (Recommended)', given after the three wave 5 packets for issue #380 (code health assessment 2026-09-07, sections 2.2 and 4 and the wave 5 plan; issue #381 owner decision 3) were presented. Approval of a definition authorizes no work. Rules CIP-ONE-001 to CIP-ONE-017."
+++

# Specification: Wave 5 pipeline hygiene: one qualification per pull request, one form for each pin, version and name

## In plain words

One work order over the repository-owned workflows: the candidate leg stops
repeating the qualification, the re-checks go, and pins, versions and names
take one form. The Pages deployment queues behind one group.

## Scope

The nine workflows under `.github/workflows/` that this repository owns, the
release-bundle manifest script, the CI note and the tests that pin them. The
managed template `engineering-harness.yml` and its hash-locked root copy are
`SPEC-DST-027`'s; the trigger policy and artifact handoff stay under
`SPEC-CIP-001`.

## Terms

- **Candidate leg.** The `rehearse-candidate` job of the publication
  rehearsal, which calls the qualification definition in `candidate` mode.
- **Pin form.** A `uses:` line naming a full commit digest, followed by a
  comment with the exact tag that digest was peeled from.
- **Retired name.** `governor`, `governor-transition` or
  `governance-migration`, names of mechanisms removed under `WO-ECP-010`,
  `WO-ECP-011` and `WO-REB-028`.

## Rules

**CIP-ONE-001.** `release-qualification.yml` MUST run `qualify
complete-candidate`, `unittest discover` and the `--help` smoke only when
`inputs.mode == 'release-record'`; candidate mode MUST replay the recipe only.

**CIP-ONE-002.** On a pull-request event, the `candidate-source` job of
`candidate-evidence.yml` MUST be the only job that runs `qualify
complete-candidate` or the test suite.

**CIP-ONE-003.** The inline forbidden-member assertion that follows
`check_portable_release_surface.py --wheel` in `candidate-package` MUST be
removed; the script's `FORBIDDEN_MEMBERS` is the one definition.

**CIP-ONE-004.** The `--help` grep for `reconcile-governor` in the
disposable-repository step MUST be removed; `check_portable_release_surface.py
--harnessctl` already refuses every `FORBIDDEN_CLI` entry.

**CIP-ONE-005.** Every `python-version` in a repository-owned workflow MUST be
the one string `"3.11"`; `publish-pypi.yml` MAY keep it in its
`PYTHON_VERSION` env.

**CIP-ONE-006.** Every `uses:` of a public action in a repository-owned
workflow MUST take the pin form; no floating tag and no bare-major comment
such as `# v4` MAY remain.

**CIP-ONE-007.** The integration build's `build`, `setuptools` and `wheel`
versions MUST appear once, in a job `env` block read by both the install and
the `--expect-*-version` arguments.

**CIP-ONE-008.** The `deploy` job of `pages-publication.yml` MUST declare
`concurrency` with group `se-harness-pages-deploy` and `cancel-in-progress:
false`, so every Pages deployment queues whichever caller invoked it.

**CIP-ONE-009.** `publish-pypi.yml` MUST pass `--evaluator-payload-sha256`
unconditionally; its `--help` probe is removed because the evaluator it
resolves from `main` postdates the flag.

**CIP-ONE-010.** `pages-publication.yml` MUST keep its probe, with a comment
stating that its evaluator is the released record's own governance root,
which may predate the flag.

**CIP-ONE-011.** `predecessor-evaluator-assessment.yml` MUST name its workflow,
job, concurrency group, artifact and temporary files after the predecessor
evaluator assessment; no retired name MAY remain in it.

**CIP-ONE-012.** The `governance-migration` job of `candidate-evidence.yml`
MUST be renamed `upgrade-rehearsal`, with its artifact name, `needs` entries
and output references; no retired name MAY remain in a workflow.

**CIP-ONE-013.** `scripts/create_release_bundle_manifest.py` MUST require
`--build-recipe`, and `release_distribution.create_manifest` MUST refuse
`build_recipe=None`; reading a schema-1 manifest is unchanged.

**CIP-ONE-014.** `docs/notes/ci-pipeline.md` MUST list all nine workflows,
including `release-qualification.yml` and `pages-publication.yml`, and record
the per-pull-request counts before and after under an "After `WO-CIP-007`"
heading.

**CIP-ONE-015.** `SPEC-CIP-001` MUST be amended by record: CIP-ART 3 and 5 for
the renamed job, CIP-QLF 2 and 3 for the steps that run in release-record
mode only and on one platform.

**CIP-ONE-016.** `tests/test_ci_pipeline.py` MUST pin CIP-ONE-001, -002, -005
to -009, -011 and -012 by parsing the workflow files; every test naming a
retired name MUST name the new one instead.

**CIP-ONE-017.** Every changed workflow's header comment MUST describe the
file after this change, per `SPEC-CIP-001` CIP-DOC 4.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| a second job runs the suite on a pull-request event | the one-run test fails naming the job | test failure |
| a `uses:` line lacks a full digest or an exact tag comment | the pin-form test fails naming file and line | test failure |
| a `python-version` differs from the one string | the version test fails naming file and line | test failure |
| a retired name survives in a workflow | the name test fails naming the file | test failure |
| `create_release_bundle_manifest.py` is called without `--build-recipe` | the parser refuses before any Git call | exit 2, usage |
| `create_manifest(build_recipe=None)` | refused | `ReleaseDistributionError` |
| a renamed job was a required check in the repository ruleset | the pull request shows the old name as expected and missing | owner updates the ruleset |

## Examples

**Given** a pull request at commit C, **when** the rehearsal's candidate leg
runs, **then** its log holds the recipe replay and neither `qualify
complete-candidate` nor a test run (CIP-ONE-001, CIP-ONE-002).

**Given** the release workflow dispatched for a released record, **when** the
Pages job and the standalone dashboard workflow run together, **then** the
second deployment waits for the first (CIP-ONE-008).

**Given** `publish-dashboard-pages.yml` dispatched for a record whose
governance root pins an evaluator without the payload flag, **when** the
identity step runs, **then** the probe omits the flag and the step passes
(CIP-ONE-010).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-CIP-008` | CIP-ONE-001, CIP-ONE-002, CIP-ONE-014, CIP-ONE-015, CIP-ONE-016, CIP-ONE-017 |
| `REQ-CIP-009` | CIP-ONE-003, CIP-ONE-004, CIP-ONE-005, CIP-ONE-006, CIP-ONE-007, CIP-ONE-008, CIP-ONE-009, CIP-ONE-010, CIP-ONE-011, CIP-ONE-012, CIP-ONE-013, CIP-ONE-015, CIP-ONE-016, CIP-ONE-017 |

## Not decided here

- The exact digests chosen for the pin form: the newest release of the major
  each file already uses, verified against the action's tag.
- The names of the renamed temporary files, env variables and step titles.
- Whether the retained artifact of the renamed rehearsal job keeps its
  platform suffix.
- The wording of the amendment record on `SPEC-CIP-001` and of the note's
  "after" figures.
- Whether the owner updates a repository ruleset that named a renamed job; a
  GitHub setting is the owner's.


## Approved supplemental reconciliation — 2026-09-12

The operator approved WO-PLG-020 supplement revision 2 as `technical-owner` at `2026-09-12T14:49:44Z`. The recorded instruction was: "i approve supplement revision 2 to reconcile the CI/CLI contracts and ten required scope additions". The retained proposal and decision receipt are in WO-PLG-020's governance evidence. This records only the selected definition amendment; historical approvals and observations remain unchanged.

### Applicability amendment — WO-PLG-020 ownership acceptance

For the ownership acceptance required by VER-PLG-020, CIP-ONE-005 permits one additional pinned major/minor interpreter selection, `"3.13"`, in the existing `upgrade-rehearsal` job of `.github/workflows/candidate-evidence.yml`. The additional interpreter runs only the complete WO-PLG-020 source and isolated installed-candidate ownership and fault matrix on Ubuntu and Windows. Existing qualification, the canonical complete candidate-source regression, candidate wheel production, integration packaging, and predecessor-to-successor upgrade rehearsals retain Python `"3.11"`; ownership interface and compatibility smoke also runs on `"3.11"`. Every acceptance consumer uses the same verified non-promotable candidate wheel built once by `candidate-source`; this exception authorizes no additional release build, qualification duplicate, new job, publication, or adoption. As a bounded exception to CIP-ONE-002, the same `upgrade-rehearsal` job may run only these WO-PLG-020 ownership acceptance subsets; complete-candidate qualification and the canonical full repository test suite still run once in `candidate-source`. Every other application of CIP-ONE-002 and CIP-ONE-005, and all other SPEC-CIP-003 rules, remain unchanged.
