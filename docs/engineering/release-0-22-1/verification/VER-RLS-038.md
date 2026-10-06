+++
id = "VER-RLS-038"
type = "verification"
title = "Confirm complete public 0.22.1 delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020", "REQ-RLO-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 de767def9c1bb5ce0fd56df405316ca7bd10c12fbd2507dcb8b69455858eda4c."
+++

# Confirm complete public 0.22.1 delivery

## Independence

Use the frozen reviewed plan and approved RLS/package identities as expected
values. Independently read public endpoints after authorized publication. A
successful publication command alone is not confirmation of its effects.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-RLO-019 | Public GitHub/PyPI archives; marketplace fresh/update on both claimed hosts; documentation and Pages readback | All observed versions, archive/package identities and documented routes match the approved plan; missing tests stay missing. |
| REQ-RLO-020 | Five-surface report and retained retry/failure observations | Delivery is complete only when every required surface observation passes. Unknown, failed, deferred or pending evidence is explicit. |
| REQ-RLO-022 | Publisher/resolver output, maintenance/marker readback and existing recovery rehearsal | Authorized immutable payloads are reused; marketplace is an ordinary descendant; maintenance line and latest/last match the RLS candidate; unexpected changes stop. |

## Procedure and retention

After the exact complete-release grant, run the trusted-main publisher and its
existing resolver, qualification and complete-delivery path. Inspect uncertain
remote state before retry. Obtain public archives independently and compare
hashes. Test fresh install and update from plugin 0.2.5, without normal-profile
changes. Read back release/0.22, v0.22.1, latest, last, both marketplace packages,
current instructions and https://mmzen.github.io/se_harness/ provenance.

Retain actual commands, public identities, failures and closeout under
evidence/WO-RLS-042/. Evidence receipts must use the reviewed plan's permitted
paths and shape. Do not overwrite frozen plans or historical receipts.
Capture required commit-bound verification of this observation/documentation
work. This post-publication record is not a prerequisite of the already
qualified release candidate; it cannot retroactively change its assurance.
