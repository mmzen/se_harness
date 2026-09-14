+++
id = "REQ-PLG-027"
type = "requirement"
title = "Provide usable installation instructions with honest support claims"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "THE PLUGIN SHALL document the shortest supported installation and project-use route, with claims limited to the release and host behavior actually checked."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner-directed KISS amendment, 2026-09-14; existing PR #416 identifier"

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:16:55Z"
decided_by = "requirements-steward"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."
+++

# Provide usable installation instructions with honest support claims

## In plain words

A user should be able to install the plugin, prepare its checker and use it in a
project by following one short guide. The guide must say what is available now.

## Acceptance

Cover prerequisites, installation, setup, connection, first explicit check and
repair, linking the common setup instructions rather than copying them. Identify
the release and host versions actually exercised. Clearly distinguish a local
development package from a public release. An untested platform is unclaimed,
not a reason to block a working documented route. Missing Python, unsupported
installation and an incompatible checker produce an actionable next step.
