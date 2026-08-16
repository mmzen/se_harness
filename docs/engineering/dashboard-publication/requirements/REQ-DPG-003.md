+++
id = "REQ-DPG-003"
type = "requirement"
title = "Operate a controlled replayable Pages deployment"
status = "implemented"
owners = ["service-owner", "repository-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN the release dashboard workflow uploads or deploys a Pages artifact, THE SYSTEM SHALL use least privilege, serialize deployments, retain observable provenance, and support an idempotent authorized replay without committing generated output."
verification_method = "automated-workflow-policy-test-and-deployment-review"

[relations]
derives_from = ["CAP-DPG-001"]
+++

# Requirement: Operate a controlled replayable Pages deployment

## Rationale

Pages deployment changes public external state. A promotional site does not justify broad repository permissions, generated-output branches, silent overlapping deploys, or untraceable manual repair.

## Preconditions and trigger

Repository Pages settings select GitHub Actions as the source. The workflow runs in this repository under the protected `github-pages` environment.

## Required response

- Grant read-only repository access during resolution and generation, and grant Pages deployment permissions only to the deployment job.
- Use official Pages actions pinned to immutable commit SHAs and record their corresponding reviewed release versions.
- Upload one bounded Pages artifact and deploy it through the `github-pages` environment.
- Serialize deployments with a dedicated concurrency group and avoid cancelling an active deployment midway.
- Record the GitHub Release tag, release record, candidate commit, governance commit, snapshot SHA-256, generated dashboard SHA-256, workflow run, and resulting Pages URL.
- Provide an authorized manual replay using explicit release and governance inputs, subject to the same checks as automatic publication.
- Never commit generated dashboard output to `main`, `gh-pages`, a release branch, or a work branch.

## Failure and boundary behavior

Insufficient permissions, unavailable dependencies, provenance mismatch, upload failure, environment rejection, or deploy failure must produce a failed workflow with diagnostics. Automation may report and retry; it may not change formal lifecycle state, tags, releases, or repository settings.

## Constraints

The live site represents the most recently successful selected deployment, not an append-only archive of all releases. Historical formal records and Git history remain the durable source.

## Acceptance examples

### Example: authorized replay

**Given** a prior deployment failed after release provenance was validated

**When** a maintainer replays the same release record and full governance commit

**Then** the same snapshot is generated and a successful deployment reports the same provenance hashes.

### Example: overlapping run

**Given** a Pages deployment is active

**When** another publication is requested

**Then** the requests are serialized and the active deployment is not cancelled midway.

## Open decisions

None.
