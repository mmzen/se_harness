# Clarify the existing public query syntax

Claude's fresh report32 diagnostic read the required guides and exercised all
seven read tools. It still incorrectly described Cypher as single-node-only after
an anonymous relationship pattern was refused. The public query guide did not
state that relationships need variable names. The parser and an earlier actual
native read establish that named relationships are supported.

Clarify the existing public form in server/contracts/lifecycle-v2.md: named,
typed relationships, required variables and optional return aliases. Keep the
existing read limits and admission boundary. No fixture answer, selected artifact
ID or completed request is added. The evidence guide also distinguishes the
captured tool-error count from service refusals inside ordinary tool responses.

This is existing behavior explained at its two owning documents. It adds no
parser rule, permission, endpoint, reporting framework or acceptance criterion.
The installed parser observation accepts named relationships and absent aliases,
and refuses anonymous relationship syntax. That check is not a live graph read.

Focused tests, the source suite, distribution/CLI checks, released validation,
scope checks and review preflights pass. Exact results are in checks.zip. Native
qualification remains separate. Rerun the unchanged focused diagnostic on the
exact package before the affected full lifecycle case. Preserve all earlier
observations and failed report claims.
