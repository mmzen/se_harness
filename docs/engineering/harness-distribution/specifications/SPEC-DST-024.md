+++
id = "SPEC-DST-024"
type = "specification"
title = "Verity Plane public README presentation contract"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
specifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T20:43:53Z"
decided_by = "technical-owner"
reason = "Record the owner-selected wording, layout, images, and preserved operational boundaries in the approved README."
+++

# Specification: Verity Plane public README presentation contract

## Scope and relationship to earlier contracts

This owner-selected revision is the current presentation contract for README.md.
For that file only, it replaces earlier requirements for exact headings, an
expertise label, a candidate-version install pin, an exhaustive command tour,
a worked scenario, a Mermaid diagram, three dashboard images, a responsibility
table, skill inventories, and a standalone limitations section in the earlier
public-onboarding and progressive-documentation packets, including SPEC-DST-003,
SPEC-DST-004, SPEC-DST-006, SPEC-DST-007, and SPEC-DST-009. Those packets and their
evidence retain their historical meaning. Their detailed-note, CLI, provenance,
authority, upgrade, and runtime obligations continue unchanged.

The root still links to the notes index, overview, complete example, command
reference, installation/upgrade procedure, and contributor guide. This changes
public presentation inside the existing layered documentation architecture.
The integration-package guide remains reachable through that notes index; its
name need not also appear in the root README. Its detailed safety guidance and
regression assertions continue unchanged.

## Inputs and outputs

Inputs are the owner-reviewed Markdown proposal and supplied Virtual Twin image.
Outputs are README.md, the repository-owned image, aligned documentation checks,
and retained evidence. No runtime, managed policy, package version, release,
workflow, or installed file changes are required.

## Rules

- **PUB-BUDGET-001:** The root has at most 650 whitespace-separated source words,
  200 physical lines, and seven level-two headings including the product title.
- **PUB-VALUE-001:** The opening identifies an open source harness for AI coding
  agents and connects delegation to bounded authority, independent verification,
  human decisions, and inspectable evidence.
- **PUB-WORK-001:** The current workflow explains approved scope, agent execution,
  evidence tied to the exact candidate commit, and separate assurance/release owners.
- **PUB-VISION-001:** The Virtual Twin is described as the authoritative model of
  intended software in a vision being built, with code conformity supported by
  independent verification rather than an already-delivered universal guarantee.
- **PUB-START-001:** New users receive Python 3.11+, an external virtual environment,
  released PyPI installation, working init/doctor examples, and an adopt alternative.
- **PUB-UPGRADE-001:** Existing users are directed to the repository's pinned version
  and a separate upgrade procedure; updating the package leaves managed files unchanged.
- **PUB-ROUTES-001:** Local documentation/image links resolve, public project routes
  remain available, and the detailed command guide remains linked.
- **PUB-IMAGES-001:** The root shows repository-owned Lineage and Virtual Twin PNGs
  with descriptive alternative text; the latter uses the owner's supplied image.
- **PUB-RENDER-001:** The product title is a left-aligned level-two heading and the
  tagline is a centered, italic level-four heading using GitHub-compatible HTML.
- **PUB-CHECKS-001:** Checks reject broken links, unreadable images, unsafe inline
  scripts/styles, malformed fences, agent-only quick-start commands, and unsupported
  current-capability claims without restoring the retired presentation inventory.

## Failure behavior

A broken local route, unusable command, unsupported claim, or changed managed path
blocks completion. Detailed notes remain the owner of advanced operational guidance.
Tests compare command syntax with the parser and images with actual files.

## Open decisions

None.
