+++
id = "REQ-WAC-005"
type = "requirement"
title = "Distribute assurance classification consistently"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN SE Harness is installed or safely upgraded, the managed work-order template, policy, validation, preflight, inspection, documentation, and package SHALL expose consistent assurance-classification behavior without overwriting repository-specific decisions."
verification_method = "managed parity, package, fresh-install, upgrade, CLI, documentation, and full regression tests"

[relations]
derives_from = ["CAP-WAC-001"]
+++

# Requirement: Distribute assurance classification consistently

## Rationale

A repository-local source change is ineffective if consumers receive a stale template, validator, inspection implementation, or policy explanation. Safe upgrades must preserve repository-owned artifacts and decisions.

## Required response

- Update canonical distribution sources before active managed copies.
- Synchronize managed integrity through the supported mechanism.
- Include the declaration in newly installed work-order templates.
- Keep repository-owned existing work orders untouched during install or upgrade.
- Keep source, package, and released-governor test boundaries explicit.

## Failure and boundary behavior

Doctor reports managed drift. Upgrade stops on customized or ambiguous managed content. No installer or reconciler bulk-edits existing formal work orders.

## Constraints

Preserve one standard distribution, current self-hosting separation, safe upgrade behavior, and the authority boundary of every command.

## Acceptance examples

A fresh installation exposes the new template and commands consistently. An upgrade changes managed controls but leaves repository-owned work-order declarations unchanged.

## Open decisions

None.
