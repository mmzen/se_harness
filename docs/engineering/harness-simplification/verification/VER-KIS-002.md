+++
id = "VER-KIS-002"
type = "verification"
title = "Check the simplicity policy and its actual authoring routes"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
verifies = ["REQ-KIS-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "assurance-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record assurance-owner approval of VER-KIS-002 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."
+++

# Check the simplicity policy and its actual authoring routes

## Independence

Expected outcomes come from the accepted owner proposal and SPEC-KIS-002. Tests observe
installed files, CLI output and manifests. Human inspection judges the content; neither
string counts nor a complexity score establish a good design.

## Requirement-to-evidence matrix

| Requirement | Evidence | Pass condition |
| --- | --- | --- |
| REQ-KIS-008 | A: policy/route review; B: installed CLI and manifest tests | Accepted wording is generic, every requested route reaches it and no additional machinery is required. |

## Checks

**A — Review:** Inspect the sole shared policy, relevant template links, router and common
skills. Confirm necessity is reviewed before specification approval and at implementation
review; quality constraints remain binding and justification is proportionate. Confirm
unused verification sections are optional and adoption instructions respect editable files.
Check the CSV examples against the rule. Explain any material remaining limitation.

**B — Integration:** Install candidate templates in a disposable target. Create artifacts
and observe the applicable checklist from the installed policy; editing that seed changes
subsequent output. Both start and review list it in the reading manifest. Reuse existing
missing-required-policy, quiet-output and validation coverage rather than inventing a
failure matrix. Run focused authoring/instruction tests and repository-required checks.

Use Windows locally and the existing hosted source/package checks on supported platforms.
The isolated released 0.17.0 evaluator governs the real work order; candidate source and
non-promotable test wheels assess product behavior only. Preserve failed attempts and
report unavailable evidence honestly. Concise tracked evidence links raw test/CI results;
do not copy source trees or repeat the same review for evidence preparation.
