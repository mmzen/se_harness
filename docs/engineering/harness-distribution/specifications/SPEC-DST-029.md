+++
id = "SPEC-DST-029"
type = "specification"
title = "Plugin-first public onboarding with linked checker guidance"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-09-16"
updated = "2026-09-16"
contract = "The public README provides native plugin installation and explicit setup, with manual checker installation and upgrade details available through direct documentation links."

[relations]
specifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T12:40:39Z"
decided_by = "technical-owner"
reason = "The owner approved the reviewed replacement package with \"i approve\" on 2026-09-16, exercising the named technical-owner decision for SPEC-DST-029. Reviewed SHA-256 838730f9bd4ae442fdb3b7ab0c2be9b3363e78bf86bbc3925d07dba6772d94d0. This records the definition or execution-scope approval; it makes no assurance or external-delivery decision."
+++

# Plugin-first public onboarding with linked checker guidance

## Scope and applicability

For WO-PLG-025 and its resulting README, this addendum replaces the requirement
in SPEC-DST-024 PUB-START-001 and PUB-UPGRADE-001 to put manual checker setup and
upgrade details inline. It also permits native plugin installation commands and
the explicit setup skill under PUB-CHECKS-001. The other SPEC-DST-024 rules,
including size limits, truthful capability claims, human decisions, valid links
and images, remain applicable. The older specification and its history are
preserved. Drafting this addendum does not activate it.

This keeps the owner's current public presentation while preserving a usable
route to detailed checker guidance. It changes presentation and its checks;
it does not change the installer, evaluator, plugin package or release identity.

## Rules

**PUB-ENTRY-001.** The README MUST provide the published native Codex and Claude
Code marketplace installation commands and an explicit setup step identifying
the project and private environment location. It MUST state Python prerequisites
and the published plugin/checker identities accurately. Installing a plugin,
preparing its checker, and initializing or upgrading a project MUST remain
distinct operations.

**PUB-ENTRY-002.** The README MUST explain that the current published plugin's
setup installs its bundled released wheel offline into a private environment.
It MUST NOT claim that native plugin installation alone downloads SE Harness
from PyPI or mutates the target project's managed installation.

**PUB-ENTRY-003.** Direct links to the getting-started and installation/upgrade
guides MUST remain in the README. These linked guides provide manual external-
environment setup, released PyPI installation, init/doctor examples, repository
version selection and the separate upgrade procedure. Those details need not
be duplicated in the README. The root's PyPI project link remains available.

**PUB-ENTRY-004.** Documentation checks MUST exercise the published onboarding
route and resolve the linked manual guidance. They MUST retain meaningful
checks for command arguments, setup prerequisites, release-versus-candidate
identity, project mutation boundaries and local link validity. Tests MUST NOT
require retired inline manual examples or pass vacuously when expected command
examples are absent. Harness examples in the linked installation guide are
checked against the CLI parser; native commands are compared with the retained
published marketplace instructions without installing into user profiles.

## Examples and failure behavior

A README with both native installation routes, explicit setup and the two
direct manual-guide links can pass without inline venv or init/doctor commands.
A missing route, missing linked example, incorrect marketplace ref, or claim
that plugin installation upgrades a project fails the relevant documentation
check. The remedy preserves correct operational guidance rather than deleting
the failing assertion without a replacement acceptance condition.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-DST-069 | PUB-ENTRY-001, PUB-ENTRY-002, PUB-ENTRY-003, PUB-ENTRY-004 |

## Design rationale

Reuse the installed plugin, existing guides and existing documentation tests.
Keeping one detailed manual-installation location reduces duplication; the
README still gives a usable entry point. No new runtime mechanism, helper
framework, architecture or ADR is needed for this presentation change.
