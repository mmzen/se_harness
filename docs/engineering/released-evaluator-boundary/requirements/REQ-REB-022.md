+++
id = "REQ-REB-022"
type = "requirement"
title = "Use role-specific qualification in release workflows"
status = "approved"
owners = ["requirements-steward", "repository-owner", "quality-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN repository-owned candidate, release, or publication automation claims release qualification, THE SYSTEM SHALL invoke the matching role-specific operation and test that the workflow cannot substitute a raw validator or incompatible evaluator-target combination."
verification_method = "automated-workflow-contract-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "requirements-steward"
+++

# Requirement: Use role-specific qualification in release workflows

## Rationale

Adding safe commands is insufficient if workflows continue to assemble release evidence from raw `doctor`, `validate`, validator-script, or executable-path calls. The automation must name the intended role and preserve its trust boundary.

## Required response

- Candidate-source automation shall use `complete-candidate` for the full candidate graph and shall label that result candidate-controlled.
- Candidate-package automation shall use `candidate-package` from the exact released verifier and shall not import the candidate package into that verifier process. During the initial bootstrap only, exact public `se-harness==0.6.0`, which predates the `qualify` namespace, may instead execute its existing `accept-candidate` contract after its archive, payload, entry point, and process isolation are verified against the governed 0.6.0 identity.
- Predecessor transition and publication preparation shall use `predecessor-view` with the predecessor identity and deterministic view contract derived from governed release inputs.
- Publication automation shall use `public-install` after installing the exact publicly acquired artifact and shall bind the result to the previously released distribution digests.
- A released-root health workflow shall use `released-root` only when the running evaluator is the one locked to the target repository root.
- Workflow tests shall fail if a release-qualification step is replaced by a raw validator call, calls the wrong role, omits required provenance, or runs from the wrong environment.
- Workflow step names and retained artifact names shall identify the qualification role.

## Compatibility and adoption boundary

The candidate managed-workflow template shall adopt the typed operations so a future repository upgrade installs the corrected workflow. The currently installed root managed workflow is immutable under this packet and remains owned by released `se-harness==0.6.0`; changing its bytes requires a separate governed adoption transaction.

Repository-owned release, candidate, predecessor-assessment, and publication workflows may migrate within the approved execution scope. Historical workflow runs and retained evidence remain unchanged. In newly built versions, the existing `accept-candidate` entry point may remain for one compatibility cycle only as a documented alias that delegates to the typed `candidate-package` operation without changing its security boundary.

The immutable public 0.6.0 distribution is the sole bootstrap exception: its pre-namespace `accept-candidate` result remains explicitly `se-harness-functional-acceptance-v1` legacy evidence and shall not be relabeled as `se-harness-release-qualification-v1`. The workflow shall reject any other version, archive or payload digest, entry point, scenario contract, or executable selection. Once a released verifier exposes `qualify candidate-package`, repository-owned automation shall use that typed operation and the 0.6.0 bootstrap exception shall be removed through a later governed change.

## Failure and boundary behavior

- A workflow cannot turn candidate-controlled output into independent evidence by renaming a step or artifact.
- Failure to establish the expected evaluator, target, digest, commit, or view identity stops the workflow before the role's substantive checks.
- A compatibility alias in a newly built version must emit the same schema and result as its canonical operation and shall not maintain an independent implementation. The immutable 0.6.0 bootstrap command is retained as legacy evidence under the exact exception above, not described as an alias or canonical role result.
- No workflow migration in this requirement authorizes a root evaluator upgrade, release, publication, deployment, tag, credential use, or external-policy change.

## Acceptance examples

### Example: correct candidate lanes

**Given** a candidate branch run

**When** source and package qualification execute

**Then** the source lane retains a candidate-controlled `complete-candidate` result and the package lane retains either an independently produced `candidate-package` result from a released verifier that supports the typed operation or, during the sole initial bootstrap, the exact public 0.6.0 legacy acceptance result with its distinct schema and provenance.

### Example: raw validator regression

**Given** a workflow change replaces `qualify predecessor-view` with direct execution of a repository validator script

**When** workflow conformance tests run

**Then** they fail even if the direct validator command would return zero.
