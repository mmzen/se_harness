# Artifact Authoring Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes one managed authoring policy for formal artifacts,
consumed by the existing drafting skill and printed by `create-artifact`, and
the first increment of mechanical requirement-writing rules: the five EARS
statement shapes, singularity and length signals, a closed verification-method
vocabulary, optional priority, source, and measure attributes, approval
predicates against leftover placeholders and open decisions, and a slimmer
requirement template linked to `acceptance/`. It follows the 2026-08-25 review
of `REQUIREMENT.template.md` measured on this repository's 255 requirements.

## Draft definition packet

- `INT-AUT-001`: make artifact quality a policy the tool can check, not advice in a skill.
- `CAP-AUT-001`: author any formal artifact under one managed policy with mechanical checks.
- `REQ-AUT-001`: distribute one managed authoring policy, routed, locked, consumed by the drafting skill and by `create-artifact`.
- `REQ-AUT-002`: five EARS statement shapes; singularity and length signals.
- `REQ-AUT-003`: closed `verification_method` vocabulary with a migration.
- `REQ-AUT-004`: optional `priority`, `source`, and `measure` attributes.
- `REQ-AUT-005`: approval predicates against leftover placeholders and open decisions.
- `REQ-AUT-006`: slimmer requirement template linked to `acceptance/`.
- `REQ-AUT-007`: authoring advisories are reported apart from errors and warnings and raised only on drafts (issue #283; drafted 2026-08-30 with `SPEC-AUT-002`, `VER-AUT-002`, amendment records on `REQ-AUT-002` and `SPEC-AUT-001`, and `WO-AUT-004`).
- `SPEC-AUT-001`: the policy, template, validator, command, and gate contracts.
- `SPEC-AUT-002`: the advisory class of the validator report (`AUT-ADV-001` to `-007`).
- `ARCH-AUT-001` / `ADR-AUT-001`: policy above skills; rules in the validator; the drafting skill unchanged in shape.
- `VER-AUT-001`: independent evidence.
- `VER-AUT-002`: independent evidence for the advisory class.
- `WO-AUT-001`: first increment — policy, template, validator signals, attributes, checklist (REQ-AUT-001, 002, 004, 006).
- `WO-AUT-002`: second increment — vocabulary migration and approval predicates (REQ-AUT-003, 005).
- `WO-AUT-003`: retarget the dry-run pin so requirements drafted in the closed vocabulary do not fail the suite (REQ-AUT-003).
- `WO-AUT-004`: report authoring advisories apart from errors and warnings (REQ-AUT-007), drafted 2026-08-30 from the functional assessment's issue #283.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action.
