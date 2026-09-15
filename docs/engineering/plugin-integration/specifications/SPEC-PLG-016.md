+++
id = "SPEC-PLG-016"
type = "specification"
title = "Write and exercise one practical installation guide"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"
contract = "Provide a short installation guide whose availability and host claims match actual use, with useful prerequisite and repair guidance."

[relations]
specifies = ["REQ-PLG-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:16:55Z"
decided_by = "technical-owner"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."
+++

# Write and exercise one practical installation guide

## Rules

- **PLG-DOC-001:** Write a short guide for the existing Codex and Claude Code plugin
  packages: prerequisites, host installation, setup, project connection, first
  explicit check and the existing repair command. Link shared instructions.
- **PLG-DOC-002:** Check one ordinary end-to-end route in each host for which the
  guide claims support, beginning with the owner's Windows use. Record actual host
  and checker versions. Reuse unchanged discovery/setup evidence and run the missing
  steps. Do not infer a full install from a discovery-only probe. Other platforms
  need evidence only when a claim about them is added.
- **PLG-DOC-003:** Draft and check the development route using an existing local
  package and disposable project. Clearly label unavailable public releases or
  catalog routes. Once an actual release is selected, check its real installation
  before advertising that route. Drafting does not wait on an invented launch gate.
- **PLG-DOC-004:** Check that guidance for missing Python, incompatible wheels and
  repair agrees with existing behavior. Reuse setup/installer tests; add no fresh
  environment switch, hidden download, activation receipt or local enforcement claim.
- **PLG-DOC-005:** If the walkthrough exposes a delay or repeated prompt, record its
  cause and the user's impact. Measure further only to answer an observed problem;
  there is no mandatory percentile, timing threshold, cold/warm benchmark matrix,
  exact host-version allowlist or separate qualification workflow.

## Applicability and simpler choice

This replaces the unmerged SPEC-PLG-016 and absorbs the useful host evidence from
SPEC-PLG-015. REQ-PLG-027 covers truthful availability and observed usability.
Instructions plus an actual walkthrough answer the current need. DEC-PLG-003 and
DEC-PLG-005 remain historical draft proposals, not dependencies to import. Selection
of an actual release/installation action uses the existing owner decision at that time.
