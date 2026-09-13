+++
id = "REQ-PLG-037"
type = "requirement"
title = "Keep development assembly and acceptance small"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "WHEN a developer builds a local plugin, THE BUILD COMMAND SHALL produce a reusable development package without requiring publication provenance."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner acceptance on 2026-09-13 of the plugin simplification proposal; retained under WO-PLG-021 governance evidence."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "requirements-steward"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the requirements-steward approval of REQ-PLG-037 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# Requirement: Keep development assembly and acceptance small

## In plain words

A local plugin build copies the files and creates an archive. Its tests check useful behavior without repeating the same proof.

## Why

Local iteration is frequent. Publication evidence belongs to publication, while historical probes describe what was observed at the time.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A developer builds again in the command-owned output folder. | Replace the build output and identify it as a development package. | Refuse replacement of an unrelated folder and report invalid package inputs. |

## Examples

### Normal

**Given** the command already created its output folder. **When** the developer rebuilds. **Then** the output is refreshed.

### Failure

**Given** the output path belongs to another project. **When** a rebuild is requested. **Then** the command leaves that project alone.
