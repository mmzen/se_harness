+++
id = "VER-CIP-003"
type = "verification"
title = "Independent evidence for the wave 5 pipeline hygiene"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-CIP-008", "REQ-CIP-009"]
+++

# Verification Contract: Independent evidence for the wave 5 pipeline hygiene

## Independence

Expected values come from `REQ-CIP-008`, `REQ-CIP-009` and the rules of
`SPEC-CIP-003`, never from the changed files. The workflow tests parse the
YAML as text and as a job graph. The run observations are GitHub's own run
list and step logs for the pull request that carries the change, read at its
head. The count of qualifications and suite runs per pull request is read
from the run list before (`main` at `a68caf70`) and after.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-CIP-008` one run | test: parse `release-qualification.yml` and every workflow triggered by `pull_request` | the qualification, suite and smoke step carries `if: inputs.mode == 'release-record'`; `candidate-source` is the only job running `qualify complete-candidate` or the suite on a pull-request event (CIP-ONE-001, CIP-ONE-002) |
| `REQ-CIP-008` run observation | the pull request that carries this change | its run list shows one `qualify complete-candidate` and one suite run for the head commit; the candidate leg's log shows the recipe replay and no test run; every lane green |
| `REQ-CIP-009` duplicate checks | test: text of `candidate-evidence.yml` | no `zipfile` assertion follows the `--wheel` call; no `--help` grep for `reconcile-governor`; the surface script's `FORBIDDEN_MEMBERS` and `FORBIDDEN_CLI` still hold the names (CIP-ONE-003, CIP-ONE-004) |
| `REQ-CIP-009` versions and pins | test over all repository-owned workflows | every `python-version` is `"3.11"`; every public `uses:` matches `@[0-9a-f]{40} # v\d+\.\d+\.\d+`; the integration tool versions appear once in an `env` block (CIP-ONE-005 to CIP-ONE-007) |
| `REQ-CIP-009` Pages queue | test and inspection of `pages-publication.yml` | the `deploy` job declares the `se-harness-pages-deploy` group with `cancel-in-progress: false` (CIP-ONE-008) |
| `REQ-CIP-009` probes | test on both files | `publish-pypi.yml` passes the payload flag without a probe; `pages-publication.yml` keeps the probe and the comment (CIP-ONE-009, CIP-ONE-010) |
| `REQ-CIP-009` retired names | test: grep over `.github/workflows/` | no `governor`, `governor-transition` or `governance-migration`; the rehearsal job is `upgrade-rehearsal` and every `needs` and output reference follows (CIP-ONE-011, CIP-ONE-012) |
| `REQ-CIP-009` manifest schema | test | the script without `--build-recipe` exits 2 with usage; `create_manifest(build_recipe=None)` raises; a schema-1 manifest still reads (CIP-ONE-013) |
| `REQ-CIP-008`, `REQ-CIP-009` documentation | inspection | the note's table lists nine workflows and the "after" section carries the before-and-after counts; `SPEC-CIP-001` carries the amendment record; every changed header describes the file (CIP-ONE-014, CIP-ONE-015, CIP-ONE-017) |
| both | regression: the full suite, `validate`, `doctor`, the hosted lanes | suite at its baseline; graph 0 errors under the released 0.16.0 evaluator; no managed path changed; every lane green at the head |
| both | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

## Acceptance scenarios

- Read the run list of the base commit's last pull request and of this
  pull request's head; record both counts of qualifications and suite runs
  in the evidence packet.
- Remove the release-record condition in a scratch copy: the one-run test
  fails and names `release-qualification.yml`.
- Change one pin to a floating tag in a scratch copy: the pin-form test
  names the file and line.
- Call the manifest script without `--build-recipe`: exit 2, no Git call.
- Dispatch nothing: the Pages group is verified by test and inspection; its
  first live observation is the next release, recorded there.

## Evidence retention

One evidence packet under `docs/engineering/ci-pipeline/evidence/WO-CIP-007/`
holding the run-list readings before and after with their run ids, the pin
and version inventory before and after, the retired-name grep before and
after, the manifest-script refusal, the `validate` and `doctor` readings,
and the lane results at the head.

## Pass criteria

Every row of the matrix passes on the hosted Linux lane and on the Windows
workstation; the released 0.16.0 evaluator's `validate` reports 0 errors;
the pull request's lanes are green through completion and the record head;
no managed path changes.

## Residual uncertainty

The Pages concurrency group is exercised only when a release or a dashboard
publication runs; until then it is verified by test and inspection. A
repository ruleset that named a renamed job is the owner's setting and is
not read by the suite. The Windows baseline carries the two known failures
recorded under `WO-TST-004`.
