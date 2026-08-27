+++
id = "WO-RLO-007"
type = "work_order"
title = "Tear down the producer workspace on a hosted runner after a recipe replay"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The recipe replay is the build the 0.7.0 release and every later release depend on, and it has never completed on a hosted runner. The change touches the replay's workspace lifecycle in repository_tools.release_build; assurance must bind the exact commit whose hosted rehearsal run completes."
decided_by = "engineering-owner"
[relations]
implements = ["REQ-RLO-013", "REQ-RLO-014"]
specifications = ["SPEC-RLO-004"]
architecture = ["ARCH-RLO-004", "ADR-RLO-004"]
verification = ["VER-RLO-004"]
[execution_scope]
paths = [
  "repository_tools/release_build.py",
  "tests/test_release_build.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/release-orchestration/README.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-007.md",
  "docs/engineering/release-orchestration/evidence/",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T17:21:50Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: i approve WO-RLO-007 and start it. Approval ratifies commit_bound_verification required: the recipe replay is the build every release depends on and has never completed on a hosted runner."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T17:21:53Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: start WO-RLO-007."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T17:56:42Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: completion follows the hosted reading; run 32995876112 completed the first hosted recipe replay (state exact) after two recorded failed attempts; five deviations accepted interactively."
+++

# Work Order: Tear down the producer workspace on a hosted runner after a recipe replay

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

Make `repository_tools.release_build.replay_build` complete on a GitHub-hosted
Linux runner. Today every hosted recipe replay in this repository's history
fails after the two producer builds with
`[Errno 1] Operation not permitted: <work root>/b/source/build`: the
producer container writes its trees as root inside the bind-mounted
workspace, and the `tempfile.TemporaryDirectory` teardown, running as the
runner user, cannot remove them. Observed on the four
`release-candidate-replay.yml` runs to date (three on 2026-08-22, one on
2026-08-26 on the 0.7.0 contract branch) and on the first hosted execution
of the reusable qualification definition (pull request #173,
`WO-CIP-002`). `publish-pypi.yml`'s schema-2 leg has never run and would
fail the same way, so the 0.7.0 release path is blocked by this defect.

## In scope

- In `replay_build`, after the producer observations are collected and
  before the workspace is released — and on every exit path — hand the
  workspace back to the calling user: one further run of the same pinned
  producer image (`docker run --rm --mount type=bind,source=<work root>,target=/workspace <image> chown -R <uid>:<gid> /workspace`)
  on POSIX hosts, with the image digest already resolved by
  `_docker_image_identity`. No new dependency, no change to the recipe, the
  lock, the producer arguments, or the compared outputs.
- Teardown failures are reported as their own error after the build result
  is known, never masking a build comparison result.
- Tests in `tests/test_release_build.py`: the hand-back command is issued
  with the resolved uid/gid on POSIX and skipped on Windows; it is issued on
  the failure path too; a hand-back failure after a successful comparison
  surfaces as a distinct error; the existing determinism and hash tests are
  unchanged.
- `docs/notes/developing-se-harness.md`, "Building and releasing": one
  sentence on the hand-back step. `README.md` row. Evidence under
  `evidence/WO-RLO-007/`, including the hosted reading.

## Out of scope

The recipe, the lock, the producer image, the bound hashes of any record,
`scripts/replay_release_build.py`, the workflows, and any lifecycle
transition of a release record or contract. Running the producer as a
non-root user is out of scope: it would change the producer's runtime
identity and therefore the recipe.

## Authorized decision envelope

The engineering owner may implement the hand-back as a `docker run` with
`--user` on a minimal command inside the pinned image, or as a
`chown` inside that image, whichever the image supports; the evidence
records which and why.

## Constraints

No byte in the distributed surface changes (`repository_tools` is not
packaged). The change is measured on a hosted runner before completion: the
pull request's rehearsal (`candidate` mode of the reusable definition) is the
reading, and `release-candidate-replay.yml` on a ready record when one
exists.

## Expected change surface

One function in `repository_tools/release_build.py`, tests, one note
sentence, the README row, evidence.

## Required verification

`VER-RLO-004`'s hosted replay row; repository-required checks; full suite on
both platforms; the pull request's rehearsal job green; handoff check with
the complete changed-path set.

## Evidence to record

Under `docs/engineering/release-orchestration/evidence/WO-RLO-007/`: the
failing hosted run before the change and the passing one after, with the
run identifiers; the hand-back mechanism chosen.

## Stop and escalate conditions

Stop if the pinned image cannot execute a hand-back command, if the fix
would require changing the recipe or the lock, or if the hosted rehearsal
still fails after the change.

## Completion report format

The `harnessctl check . --artifact WO-RLO-007 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
