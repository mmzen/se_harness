+++
id = "REQ-PLG-027"
type = "requirement"
title = "Provide usable installation instructions with honest support claims"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "THE PLUGIN SHALL document the shortest supported installation and project-use route, with claims limited to the release and host behavior actually checked."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner-directed KISS amendment, 2026-09-14; existing PR #416 identifier"

[relations]
derives_from = ["CAP-DST-001"]
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
