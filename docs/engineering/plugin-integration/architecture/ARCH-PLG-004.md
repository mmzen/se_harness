+++
id = "ARCH-PLG-004"
type = "architecture"
title = "Thin plugin with ordinary file replacement"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "public-interface-or-protocol"]
rationale = "The change removes automatic interception and transaction machinery, and simplifies the provider protocol."
assessed_by = "implementation-planner"

[relations]
addresses = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-PLG-035", "REQ-PLG-036", "REQ-PLG-037"]
conforms_to = ["SPEC-PLG-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "technical-owner"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the technical-owner approval of ARCH-PLG-004 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Architecture: Thin plugin with ordinary file replacement

## Context and scope

The plugin helps one owner use the existing evaluator. It does not enforce an extra policy around every edit.
SPEC-PLG-021 supplies the replacement behavior and prior-contract applicability.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Migration command | Check the selected replacement and four destination paths, replace disposable copies, save the provider last. |
| Installer and doctor | Use one provider choice to select the repository inventory. |
| Setup instructions or small helper | Create or repair the private environment and run the selected checker. |
| Native manifests and shared skills | Expose the skills and direct ordinary instruction reading and explicit checks. |
| Local build command | Copy shared sources, validate required contents once, and create a development archive. |
| Existing released evaluator | Own lifecycle decisions, managed integrity, assurance and release rules. |

## Dependency direction

Native skill instructions call the installed evaluator through its CLI.
The migration command reads plugin data; it never imports plugin code.
Installer and doctor share the provider inventory. Plugin packages do not embed a second evaluator policy.
Publication uses the existing release path; local assembly needs no release record.

## Trust boundaries

Deletion is confined to four selected directories inside the target repository.
Plugin manifests and required files establish the replacement's presence, not authenticity or host activation.
The existing released evaluator retains authority for governed work.
No mutex, journal, process-tree supervisor or per-edit hook sits between the user and ordinary editing.

## Recovery and compatibility

Save the lock atomically after file replacement. An ordinary error identifies the failed operation and allows a rerun.
Read previous schema-4 records and normalize them when migration is requested again.
Keep the schema-3 repository mode, portable clone checks and unrelated owner content.
ADR-PLG-004 records why this smaller design is appropriate now.
