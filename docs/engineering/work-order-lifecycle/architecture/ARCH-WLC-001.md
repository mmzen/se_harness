+++
id = "ARCH-WLC-001"
type = "architecture"
title = "Policy-aware lifecycle validation architecture"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
conforms_to = ["SPEC-WLC-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "ADR-WLC-001 chose implemented as the completed state for governance work no record covers, over a new completed value, per-work-order records and a derived warning only. It makes blocking policy of what every repository's lifecycle reading assumes."
assessed_by = "technical-owner"
+++

# Architecture: Policy-aware lifecycle validation architecture

## Components

- `scripts/validate_engineering_artifacts.py` owns policy parsing and authoritative current-state consistency validation.
- `scripts/generate_harness_dashboard.py` consumes validator output and retains only genuinely derived findings.
- `templates/repository/standard/` is the canonical installation boundary.
- Root managed files are the self-installed operational copy protected by `.engineering-harness.lock`.
- Formal work-order files retain explicit lifecycle corrections; VREC and RLS files remain immutable.

## Data flow

The validator loads artifacts and repository configuration, derives verified work coverage from eligible VRECs, and adds an `E010` diagnostic for configured violations. Explorer uses that report and the same policy parser, projects readiness and provenance, and does not recreate the invariant as a warning.

## Constraints

Use Python 3.11+ standard library only. Treat repository configuration and artifacts as untrusted input. Keep configuration-disabled compatibility. Preserve canonical/root parity and the existing no-automatic-authority boundary.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-WLC-001`).** The six
requirements of the legacy relation become `addresses`; `conforms_to` names
`SPEC-WLC-001`, the active specification that specifies them. The assessment
reads the rationale and four rejected alternatives of `ADR-WLC-001`, the one
active ADR that decides this architecture. Title, status, statement and ADR
relations are unchanged.
