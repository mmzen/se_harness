+++
id = "SPEC-AUT-002"
type = "specification"
title = "The advisory class of the validator report"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-AUT-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T08:59:22Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-30 with the words 'Approve and start WO-AUT-004': AUT-ADV-001 to AUT-ADV-007; the W-AUT family becomes the advisory class, computed only on drafts, listed on request, complete in the JSON; the consumers change only through the report; amendment records restate AUT-STM-002 and AUT-VOC-002."
+++

# Specification: The advisory class of the validator report

## Scope

Adds a third diagnostic class, *advisory*, to the validator report and to
the commands that render it. Moves the `W-AUT-*` family into it. Changes
no error code, no plane and no gate.

## Terms

- **Advisory:** a diagnostic that helps the author of a draft and needs no
  action once the artifact is approved.
- **Report:** the `ValidationReport` the validator script builds and every
  `harnessctl` command reads.

## Behavioral rules

**AUT-ADV-001:** The report carries `advisories`, a sorted, de-duplicated
list of `Diagnostic` values, beside `errors` and `warnings`. A diagnostic
whose code starts with `W-AUT-` is an advisory and appears in no other
list.

**AUT-ADV-002:** `W-AUT-001` to `W-AUT-004` are raised only for an artifact
whose `status` is `draft`. For any other status the checks are not run.

**AUT-ADV-003:** The human summary line is `Artifacts: N | Errors: N |
Warnings: N | Advisories: N`. The `Planes:` line counts errors and
warnings only. The `Advisories:` section, in the same line format as
`Warnings:`, is printed only when the script receives `--advisories`.

**AUT-ADV-004:** The JSON report always carries `advisories` (the list, in
the same shape as `warnings`) and `advisory_count`; `warning_count` and
`plane_counts` exclude advisories.

**AUT-ADV-005:** `harnessctl validate` accepts `--advisories` and passes it
to the script; with `--json` the flag has no effect because the JSON is
complete.

**AUT-ADV-006:** `inspect`, `check`, `preflight` and `doctor` read the
report's `errors` and `warnings` as before; because advisories are no
longer in `warnings`, their counts and finding lists exclude them without
further change. `doctor`'s `W013` pass-through is unchanged.

**AUT-ADV-007:** `docs/notes/harnessctl-reference.md` documents the fourth
number and the flag under `validate`; `docs/notes/harnessctl-check.md`
says in one sentence that advisories are not findings.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-AUT-007 | AUT-ADV-001 to AUT-ADV-007 |

## Failure behaviour

Nothing new fails. A consumer that reads `warnings` from the JSON sees
fewer entries; one that needs the advisories reads `advisories`.

## Compatibility and migration

`AUT-STM-002` and `AUT-VOC-002` of `SPEC-AUT-001` name the four codes as
warnings on plane `maintenance`; an amendment record on that specification
and on `REQ-AUT-002` restates them as advisories on the same plane. The
root copy of the validator is the released 0.11.0 one and keeps reporting
warnings until the next root adoption; the template copy carries the
change.
