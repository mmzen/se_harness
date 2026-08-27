+++
id = "ARCH-CIP-001"
type = "architecture"
title = "One execution per check, one definition per lane, one commit per release unit"
status = "approved"
owners = ["technical-owner", "release-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[decision_assessment]
outcome = "adr_required"
triggers = ["cross-cutting-policy", "material-alternatives"]
rationale = "The proposal replaces the rehearsal's digest-alignment mechanism with invocation of a shared definition, and changes what a release contract freezes. Both are policy choices with material alternatives; two ADRs are required before this architecture can be approved."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-CIP-001", "REQ-CIP-002", "REQ-CIP-003", "REQ-CIP-004", "REQ-CIP-005", "REQ-CIP-006"]
conforms_to = ["SPEC-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "technical-owner"
+++

# Architecture: One execution per check, one definition per lane, one commit per release unit

## Context and scope

The pipeline's checks are sound; their arrangement multiplies them. The
architecture arranges them as a single producer of candidate bytes with
consumers, a single qualification definition with two callers, and a
release unit anchored to a commit.

## Components and responsibilities

### Candidate producer
`candidate-source`: the only job that builds from source. Emits the wheel,
its digest, the qualification result.

### Consumers
`candidate-package` (acceptance by the public predecessor),
`governance-migration` (N-1 to N scenario per platform),
`integration-package` (build, install-test, retain). Each verifies the
digest and never rebuilds.

### Qualification definition
`release-qualification.yml` (`workflow_call`): the release leg. Called by
the rehearsal in both modes and by the release in record mode.

### Pages definition
`pages-publication.yml` (`workflow_call`): build and deploy; two callers.

### Release-unit derivation
`harnessctl release-unit`: measures the census from trailers; the
contract's `gates` is its output. The candidate validator checks the two
agree at approval.

### Predecessor derivation
One step that turns the declared governor and lock into job outputs.

### Notes
`ci-pipeline.md` (baseline, figures per increment),
`developing-se-harness.md` (procedures), `harnessctl-reference.md`.

## Dependency direction

Workflows depend on scripts; scripts depend on `se_harness` and
`repository_tools`; nothing in the package depends on `.github/`. The
rehearsal depends on the qualification definition, never on a copy of it.
The release contract depends on a commit; work orders do not depend on the
contract.

## Trust and failure boundaries

The reusable workflows carry `contents: read` and receive no secrets; the
`pypi` and `github-pages` environments and OIDC stay in `publish-pypi.yml`.
The wheel artifact is inert evidence; the promotable build is still the
recipe replay under a released record. Derivations fail closed: a missing
scenario, a trailer-less commit, or a census mismatch stops the run.

## Quality attributes

Per push, one run per workflow and one wheel build per workflow. Scripts:
at least 2,500 lines fewer, each helper defined once. Release: one contract
per version in the ordinary case.
