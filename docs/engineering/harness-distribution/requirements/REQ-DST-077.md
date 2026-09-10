+++
id = "REQ-DST-077"
type = "requirement"
title = "Name who decides completion in the work-order template"
status = "draft"
owners = ["product-owner", "technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
statement = "THE WORK-ORDER TEMPLATE SHALL state under its completion report heading who decides completion: the engineering owner, or the delegated executor under the execution delegation class."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #433 finding 3; measured on main at f0a3a223: 79 work orders end their Completion report format section with 'the completion decision is the engineering owner's', 14 of them carrying [delegation] class = 'execution' (WO-CIP-006, WO-CIP-007, WO-ECP-018, WO-ECP-025 to WO-ECP-028, WO-TCM-004 to WO-TCM-009, WO-TCM-011), under which SPEC-ECP-006 ECP-DLG-002 gives DR-WO-COMPLETE to the delegated executor; the template heading at templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md line 80 carries no guidance"
measure = "the template heading carries one guidance sentence naming both deciders; the next delegated work order drafted from it carries no sentence giving completion to the engineering owner"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Name who decides completion in the work-order template

## In plain words

Work orders copy a closing sentence from one another that names the wrong
decider when the work is delegated. The template should say who decides,
so the copying stops.

## Why

The template's last heading is empty, so drafters filled it from the previous
work order. The copied sentence gives the completion decision to the
engineering owner. Under the execution delegation class that decision is the
delegated executor's while the required check is green. So 14 delegated work
orders contradict their own front matter, and three disclosed it on the
delegated route. One sentence in the template names both deciders and ends
the copying.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a drafter reaches the completion report heading of the template | guidance names the engineering owner by default and the delegated executor under the execution class | a test names the missing guidance |
| a delegated work order is drafted from the template | its completion section carries no sentence giving the decision to the engineering owner | the handoff discloses the contradiction, as before |

## Examples

### Normal

**Given** the candidate template,

**When** the section under its completion report heading is read,

**Then** it names the engineering owner as the default decider and the
`delegated-executor` under `[delegation] class = "execution"`.

### Failure

**Given** a template whose completion report heading has nothing under it,

**When** the suite runs,

**Then** the template test fails naming the heading.
