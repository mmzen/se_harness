+++
id = "REQ-ECP-033"
type = "requirement"
title = "The shipped surface carries no dead code, dormant command or unreachable contract entry"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "THE SYSTEM SHALL ship no unreferenced code, no command never used operationally, no unreachable contract entry, no orphan fixture and no unconsumed workflow output."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #376 (code health assessment 2026-09-07, wave 1, docs/notes/code-health-assessment-2026-09-07.md sections 1, 4 and 5) and the owner decisions of 2026-09-07 recorded on issue #381: retire journaled_apply.py, remove renumber-artifacts and rehearse-recovery; REQ-ECP-030, whose one-release rule the adopt alias now meets"
measure = "vulture at confidence 60 and pyflakes report nothing on se_harness, scripts and repository_tools; harnessctl --help lists no adopt, renumber-artifacts or rehearse-recovery; the wheel carries no journaled_apply.py; quality_gates_contract.json has no QG-G0-INTENT and workflow_contract.json no PROC-CANDIDATE-COMMIT; the eight orphan fixtures and the nine unconsumed workflow outputs are gone; the suite is at its baseline"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:27:10Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #385 and its summary were presented: the shipped surface carries no dead code, dormant command or unreachable contract entry (issue #376, wave 1 of the code health assessment of 2026-09-07, with the owner decisions of issue #381). Approval of a definition authorizes no work."
+++

# Requirement: The shipped surface carries no dead code, dormant command or unreachable contract entry

## In plain words

Code, commands, contract entries and fixtures that nothing uses still ship
today. This requirement removes them.

## Why

The code health assessment of 2026-09-07 counted about three hundred lines
of unreferenced core code and two commands never used operationally. It
also found a module nothing imports, two unreachable contract entries and
eight fixtures no test reads. Each is a place the next change must read, test and
keep hash-bound for no return. The owner decided the three open cases on
2026-09-07.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a symbol has no caller in product code or tests | it is removed with its tests | the dead-code scan names it |
| a command has no operational use and no caller | its module, parser entry, tests and reference rows go, with amendment records | the parser-shape test names it |
| a contract entry is reachable from no rule, step or binding | it leaves the package and template contracts and their documentation | the documentation-contract test names it |
| a fixture, manifest line, config key or workflow output has no consumer | it is deleted | inspection |

## Examples

### Normal

**Given** the candidate after this change,

**When** the dead-code scan runs over the package,

**Then** it reports nothing, and the parser lists neither retired command.

### Failure

**Given** a retired command name typed at the shell,

**When** the parser reads it,

**Then** argparse refuses it as any unknown command, exit 2.
