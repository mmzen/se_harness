+++
id = "REQ-ECP-035"
type = "requirement"
title = "One engine, imported once and run once per command"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE SYSTEM SHALL load its evaluator engine by import, validate the repository once per governance command, keep every output byte-identical, and hold no function above cyclomatic complexity 60."
verification_method = ["test", "inspection"]
priority = "should"
measure = "the engine imported by every caller and loaded by path nowhere; one validate_repository call per command under a counting patch; formal snapshot digests, the dashboard manifest and result_sha256 equal to main's; radon cc reports no function above 60; no underscore-private import across package modules; the suite at its baseline"
source = "issue #378 (code health assessment 2026-09-07, sections 2.1, 2.2, 3.6 and the wave 3 plan) and the revisit triggers of DEC-ECP-001 and DEC-ECP-002, which name wave 3 as the decision on the engine's import surface"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:13:26Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #404, #405 and #406 and their summary were presented: wave 3 of the code health assessment of 2026-09-07 (issue #378) and the revisit triggers of DEC-ECP-001 and DEC-ECP-002, the engine as an import surface, one validation per governance command, the three largest modules split along their seams, every recorded output byte-identical. Approval of a definition authorizes no work."
+++

# Requirement: One engine, imported once and run once per command

## In plain words

The evaluator's own scripts are loaded two contradictory ways, copy tables
the package owns, and run two or three times per command. This requirement
makes them one importable engine, run once.

## Why

The engine declares itself not an import surface. One module imports it by
path and five run it as a subprocess. It duplicates five definitions the
package owns, and three duplicate blocks wave 2 could not remove sit on its
side. Every governance command validates the repository two or three times,
and eleven functions exceed complexity 60. Each copy and each re-run is a
place the next fix can miss.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a caller needs an engine module | it imports it | the loader test names the path load |
| a governance command runs | it validates the repository once and passes the report on | the call-count test names the command |
| an output is compared with the previous head | it is byte-identical | the comparison names the output |
| a function is measured | its complexity is at most 60 | the complexity test names the function |

## Examples

### Normal

**Given** the candidate after this change,

**When** the start checkpoint check runs under a patch that counts
validations,

**Then** the count is one and the result digest is unchanged.

### Failure

**Given** a module that still loads the validator by path,

**When** the loader test runs,

**Then** it names the module and fails.

## Open decisions

None.
