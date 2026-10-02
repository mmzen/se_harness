+++
id = "DEC-RLS-003"
type = "decision"
title = "Accept missing Claude public-route native tests for plugin 0.2.4"
status = "decided"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
kind = "deviation"
question = "May WO-RLS-033 continue with missing Claude public-route native session tests explicitly unverified and their residual risk accepted for plugin 0.2.4 only?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-RLO-006#RLO-DLV-003"
observed = "VER-RLS-032 requires native public-route startup, activation, compaction and resume observations. Public Claude fresh/update package installation, exact files, offline setup and init-only bootstrap pass; authenticated native session coverage is missing. The human accepts this lack of tests."

[[options]]
id = "accept"
label = "Accept the missing Claude native tests for WO-RLS-033 only, retaining unverified results and residual risk."

[[options]]
id = "stop"
label = "Keep the affected work pending until the Claude native tests pass or another formal resolution is made."

[relations]
concerns = ["RISK-RLS-003", "WO-RLS-033", "SPEC-RLO-006", "VER-RLS-032", "REL-SEH-033"]
blocks = ["WO-RLS-033"]

[disposition]
option = "accept"
label = "Accept the missing Claude native tests for WO-RLS-033 only, retaining unverified results and residual risk."
decided_by = "mmzen"
decided_at = "2026-10-02T07:08:23Z"
reason = "Human mmzen: Continue, mark claude lack of tests as accepted. Accepts only the disclosed missing Claude native public-route tests and residual risk for WO-RLS-033, plugin 0.2.4 at 7e366438165a40a14783bac650a2887e7ec8bc75. Keep results unverified; Codex obligations and other decisions remain separate."
revisit = "Before the next plugin release, before claiming this Claude route is verified, or before adoption that depends on verified Claude delivery, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-02T07:08:23Z"
decided_by = "mmzen"
reason = "Human mmzen: Continue, mark claude lack of tests as accepted. Accepts only the disclosed missing Claude native public-route tests and residual risk for WO-RLS-033, plugin 0.2.4 at 7e366438165a40a14783bac650a2887e7ec8bc75. Keep results unverified; Codex obligations and other decisions remain separate."
+++

# Accept missing Claude public-route native tests for plugin 0.2.4

## Human instruction

Human mmzen stated: "Continue, mark claude lack of tests as accepted".
This record implements that decision for the missing Claude tests disclosed
in WO-RLS-033. The evaluator writes its disposition separately.

## Exact boundary

The decision applies only to public plugin 0.2.4 at
`7e366438165a40a14783bac650a2887e7ec8bc75`, with the evaluator 0.21.0 wheel
bound by RLS-SEH-031, and to WO-RLS-033's Claude native session coverage.
It permits this bounded evidence omission against RLO-DLV-003 as specified
by VER-RLS-032. It accepts possible undetected Claude-specific startup,
activation, compaction or resume defects. Missing tests remain unverified.

Public fresh installation and update from 0.2.3 pass all 29 installed-file
comparisons. Offline setup, isolated evaluator identity, initialization,
resource lookup and reuse pass. Native init-only bootstrap callbacks pass.
These compensating observations do not prove authenticated native sessions.
See `../evidence/WO-RLS-033/routes.json`, `setup.json` and `native.json`.

## Limits and follow-up

Only the Claude omission is accepted. Codex CLI tests, hook trust and Codex
Windows desktop evidence keep their existing obligations. Earlier decisions
retain their original scope. No verification acceptance, push, PR, release-marker
change, adoption or complete-delivery claim follows from this decision.

mmzen owns the residual risk and follow-up. Revisit before the next plugin
release, before claiming this Claude route is verified, or before adoption
that depends on verified Claude delivery, whichever occurs first. Restore
Claude authentication and run the native matrix when access permits.

The `accept` option records the supplied human decision. The `stop` option
would keep the affected step pending. Neither option changes recorded test
outcomes or excuses any observed failing check.
