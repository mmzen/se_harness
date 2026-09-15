+++
id = "REQ-PLG-038"
type = "requirement"
title = "Install Verity Plane through standard plugin marketplaces"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-15"
updated = "2026-09-15"
statement = "Users can install the complete Verity Plane plugin through the standard Codex and Claude Code marketplace commands, with public availability stated only for the distribution and catalog routes actually established."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner request to package both plugins for standard marketplace installation, prepare official catalog submissions, and continue plugin publication on 2026-09-15."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T13:40:15Z"
decided_by = "requirements-steward"
reason = "The owner reviewed the four marketplace drafts and replied \"OK i approve the artifacts you can start\" on 2026-09-15. Record approval of this exact reviewed artifact in the named accountable role. This authorizes WO-PLG-023 execution under DR-015, not verification of a future candidate or a provider submission."
+++

# Install Verity Plane through standard plugin marketplaces

## Need

Users currently need a locally assembled package. A complete Git-hosted
marketplace lets each host install the plugin using its normal commands.
Provider catalog review needs the same tested contents and accurate listing
materials. Acceptance into a provider catalog remains that provider's decision.

## Acceptance

- A fresh Codex profile and a fresh Claude Code profile can add the assembled
  marketplace and install verity-plane. Each installation contains the five
  intended skills, setup helper, host manifest, license and selected released wheel.
- Published Git instructions identify the repository and ref containing those
  complete packages. A successful local test alone establishes no public listing.
- The maintainer can prepare provider submission materials from the same
  identified package, with missing publisher information shown explicitly.
- A missing plugin directory, changed package or invalid catalog prevents a
  claim of accepted publication contents and produces an actionable failure.

REQ-PLG-001 and REQ-PLG-002 retain the wheel and shared-source obligations.
REQ-PLG-027 retains truthful installation guidance. This requirement adds the
marketplace delivery route without changing setup or repository governance.
