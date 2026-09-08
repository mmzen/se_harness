+++
id = "ARCH-PLG-001"
type = "architecture"
title = "Provided Python and one released evaluator"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[decision_assessment]
outcome = "adr_required"
triggers = ["deployment-or-operating-model", "security-privacy-or-trust-boundary", "material-alternatives"]
rationale = "The plugin supplies code while the operator supplies Python; a separate environment preserves the released evaluator boundary."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-PLG-001", "REQ-PLG-002", "REQ-PLG-004", "REQ-PLG-005"]
conforms_to = ["SPEC-PLG-001", "SPEC-PLG-002"]
+++

# Architecture: Provided Python and one released evaluator

## Context and scope

The package contains a published wheel and host resources. The operator supplies Python.
This proposed boundary extends distribution without creating another evaluator or installation profile.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Package assembly | Combine common resources with one host manifest and the exact released wheel. |
| Setup skill | Check provided Python and prepare a private environment outside the target repository. |
| Installed evaluator | Own installation checks, lifecycle rules, and structured results. |
| Host adapter | Invoke that environment through supported host events and tools. |

## Dependency direction

Host tools and adapters call the installed evaluator. The evaluator does not depend on the plugin.
Assembly reads release files; it does not import candidate evaluator code.

## Data and control flow

Provided Python creates the environment. Offline wheel installation precedes identity checks.
Ordinary commands use the verified absolute interpreter with isolated imports.
The repository lock chooses the governing evaluator version; updating plugin files changes no lock.

## Trust boundaries

The supplied Python installation is a trusted prerequisite. Trusted release metadata identifies the wheel.
Existing evaluator checks establish installed identity, import isolation, and interpreter-path boundaries; they do not prove the interpreter itself trustworthy.
Repository content cannot select executable commands or replace expected identities.
Persistent plugin data is local storage, not authenticated human authority.

## Required patterns

Keep package metadata and templates intact. Use the process environment defined by SPEC-PLG-002.
Retain repository evidence outside plugin caches.

## Prohibited patterns

No distributed Python binary, custom runtime wrapper, editable checkout import, automatic Python installer, or separate policy engine.

## Quality attributes

One pure-Python wheel avoids interpreter distribution per operating system.
Python availability remains an explicit prerequisite.

## Conformance checks

VER-PLG-001 and VER-PLG-002 check package contents, isolation, wrong identities, and missing Python.

## Related ADRs

ADR-PLG-001 records this proposed deployment choice. Technical approval remains pending.
