+++
id = "REQ-HAG-014"
type = "requirement"
title = "Reduce the work needed to author a hosted draft"
status = "approved"
owners = ["mmzen"]
created = "2026-10-08"
updated = "2026-10-08"
statement = "An agent can author a private hosted draft through the installed client using applicable instructions, ordinary document files and concise results, without manually constructing transport encodings or loading unrelated instructions."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "mmzen's 2026-10-08 request to reduce instruction length, duplication, calls and duration; Opus10 evidence under WO-HAG-009"
measure = "Report wall-clock seconds, native tool calls and peak input-context tokens for the same one-intent task; goals are defined in the linked specification."

[relations]
derives_from = ["CAP-HAG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-08T16:03:26Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed REQ-HAG-014, SPEC-HAG-008, VER-HAG-008 and WO-HAG-011 package on 2026-10-08. Approves the bounded client and instruction implementation with required commit-bound verification. Includes ordinary review pushes and updates to draft PR #543 in mmzen/se_harness, source codex/hosted-agent-qualification, target main, its ready verification record and the later separately supplied verification-decision commit. Keep the PR draft while WO-HAG-009/010 qualification remains incomplete. Git remains authoritative. No human verification acceptance, merge, force-push, release, adoption, host-plugin update, permission bypass or changed qualification criterion is granted."
+++

# Reduce the work needed to author a hosted draft

## In plain words

The agent reads what applies, writes the artifact once and submits the file.
The client handles transport formatting and evidence capture. The agent still
chooses the content and each intended operation.

## Why

Opus10 took 673.18 seconds and 56 calls, reaching 112,326 input-context tokens
for a 1,283-byte intent. It also omitted four failed/denied results and did not
complete a sound content review. More instructions alone did not solve this.
These are one run's observations, not a general host benchmark.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Agent selects a hosted drafting task | Deliver the selected route, relevant source pointers and complete applicable instruction sections; leave unrelated routes unloaded | Name the missing or conflicting input; do not guess a path or policy |
| Agent submits a completed document | Preserve its exact bytes; derive transport encoding and mechanical identity fields in the client | Refuse invalid inputs before sending; preserve unknown outcomes after sending |
| Operation returns | Show outcome, identity/version, actionable findings and evidence locations; retain the complete result | Preserve refusals, conflicts and uncertainty; do not report a compact view as a new verdict |
| A comparison run finishes | Retain elapsed time, context, calls, failures and independent content review | An incomplete, assisted or incorrect run is not an efficiency success |

## Acceptance

- Ordinary drafting needs no agent-written base64, copied wheel digest or
  full input inventory. A typed client input is checked against the existing
  wire request it produces.
- Applicable rules and findings remain available, with their selected release
  and source references. Small required content can be returned together;
  a list of pointers alone does not establish that content was read.
- Unknown outcomes, stale versions, changed requests under an existing key,
  imported history, path containment and decision rights keep their current
  behavior. Git remains authoritative.
- Report correctness and the three efficiency goals separately. Preserve
  all missed goals and observed failures. No new KIS score, gate or approval
  process is introduced.

## Examples

### Normal

Given a selected test project and an intent draft file, the agent supplies the
intended operation and version inputs. The client sends the corresponding
existing request and returns its exact saved revision, validation findings and
evidence path. The final document matches the submitted bytes.

### Failure

Given a stale expected version, submission remains a conflict. The client does
not refresh that version and retry a write on its own. The retained failure is
included in the agent's report even if a later explicit correction succeeds.
