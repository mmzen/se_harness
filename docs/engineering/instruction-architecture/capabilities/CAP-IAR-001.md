+++
id = "CAP-IAR-001"
type = "capability"
title = "Route and enforce repository-aware engineering instructions"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-IAR-001"]
+++

# Capability: Route and enforce repository-aware engineering instructions

## Capability statement

Repository owners can install or adopt one standard harness that preserves local agent guidance, presents every supported engineering agent with the same authoritative route, and supplies executable readiness and CI checks without converting repository context or automation into product authority.

## Observable outcomes

- An agent reaches the managed contract through `AGENTS.md`; Claude reaches the same entry by importing `AGENTS.md`.
- The managed contract distinguishes owner facts, formal authority, policy modules, executable evidence, and human decisions.
- Preflight rejects incomplete context, damaged managed content, an invalid graph, an ineligible work order, or an incomplete governing chain.
- New installation, existing-repository adoption, and upgrade preserve owner-controlled content and produce deterministic conflict reports.
- Required pull-request CI uses an explicit work-order selection and a separately pinned harness executable.

## Exclusions

The capability does not prove that a human or agent read a file, interpret arbitrary natural-language conflicts, infer product intent from a repository, modify host branch-protection settings, approve work, transition governance records, or publish software.
