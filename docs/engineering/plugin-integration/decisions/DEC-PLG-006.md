+++
id = "DEC-PLG-006"
type = "decision"
title = "Accepted local hook-loss limitation on the tested host profiles"
status = "decided"
owners = ["technical-owner"]
created = "2026-09-12"
updated = "2026-09-12"
kind = "deviation"
question = "How is the operator's accepted local hook-loss limitation recorded for the two tested adapter profiles?"
raised_by = "implementation-agent"
recommendation = "accept"
against = "SPEC-PLG-008#PLG-HOOK-002"
observed = "On the tested Windows profiles, hook timeout, missing or invalid output, and loss of an active binding allowed local edits without the required refusal. Claude also demonstrated launch failure; literal Codex OS shell-start failure remains unobserved."

[[options]]
id = "accept"
label = "Retain the documented local hook-loss limitation and its revisit trigger without claiming enforcement or deciding adapter qualification."

[[options]]
id = "stop"
label = "Stop acceptance of the affected adapter use until the local hook-loss limitation is remediated."

[relations]
concerns = ["WO-PLG-005", "WO-PLG-006", "WO-PLG-019", "SPEC-PLG-005", "SPEC-PLG-006", "SPEC-PLG-008", "VER-PLG-005", "VER-PLG-006", "VER-PLG-008", "VER-PLG-019"]
blocks = ["WO-PLG-005", "WO-PLG-006"]

[disposition]
option = "accept"
label = "Retain the documented local hook-loss limitation and its revisit trigger without claiming enforcement or deciding adapter qualification."
decided_by = "technical-owner"
decided_at = "2026-09-12T07:27:41Z"
reason = "I accept the hook failure as a documented local limitation"
revisit = "Before the first public plugin release, any supported host-profile expansion, or introduction of remote acceptance controls."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-12T07:27:41Z"
decided_by = "technical-owner"
reason = "I accept the hook failure as a documented local limitation"
+++

# Decision: Accepted local hook-loss limitation on the tested host profiles

## Question

The operator already accepted the local limitation in both adapter tasks. This record retains that acceptance; it does not reopen the choice.
The immutable acceptance records and failed C10/C11 observations are identified in WO-PLG-019's sources.json.

The accepted profiles are Codex CLI 0.153.4 and Claude Code 2.1.266 on Windows, using Python 3.14.6 and released evaluator 0.16.0.
An unavailable guard or usable response can leave an edit to ordinary permissions. Accepting this fact does not authorize out-of-scope work.
Healthy supported checks and timely denial by a running handler remain required; asynchronous or inadequate-timeout bindings remain rejected.
The local limitation covers no remote action, credential, protected-branch update, merge, release or deployment authority.

## Options

**accept.** Retain the operator's exact acceptance, the affected profiles, failed enforcement and unavailable observations, with a review trigger.
Separate specification and assurance decisions define whether an adapter can qualify for use with this limitation.

**stop.** Keep the affected use stopped pending remediation. This required alternative does not erase the already retained operator acceptance.

## Recommendation

Record accept, preserving the already supplied reason: "I accept the hook failure as a documented local limitation".
The proposed revisit trigger is: "Before the first public plugin release, any supported host-profile expansion, or introduction of remote acceptance controls."
This trigger is an owner review obligation, not an implemented automatic expiry or remote gate.

## Disposition

Only the released evaluator may write the disposition and lifecycle event after the recording scope and exact revisit input are authorized.
No disposition has been applied by preparing this file. DEC-PLG-001 and DEC-PLG-002 remain terminal and unchanged.
Future verification and release records must retain this standing deviation when they cover the concerned work.
