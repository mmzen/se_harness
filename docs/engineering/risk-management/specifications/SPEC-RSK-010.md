+++
id = "SPEC-RSK-010"
type = "specification"
title = "The risk artifact: measurement, the decision that stops the stage, and closure under verified coverage"
status = "draft"
owners = ["technical-owner", "assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"
contract = "A risk records one measured threat, is raised for an answer, is answered by disposing the decision that blocks the threatened work, and closes only under verified coverage."

[relations]
specifies = ["REQ-RSK-010", "REQ-RSK-011", "REQ-RSK-012", "REQ-RSK-013", "REQ-RSK-014", "REQ-RSK-015", "REQ-RSK-016"]
+++

# Specification: The risk artifact: measurement, the decision that stops the stage, and closure under verified coverage

## In plain words

A risk file holds the measurement of one threat and nothing that decides
anything. The decision artifact holds the answer, and the harness copies that
answer back onto the risk.

## Scope

One new artifact type, the risk (`RISK-`), with its lifecycle, its two commands,
its diagnostics and the release register. It also adds the scope admission that
lets anyone record a threat mid-execution. It adds no gate predicate: the stop on a
threatened artifact is `QGP-DECISION-OPEN` of `SPEC-DCM-001`. It changes no
decision, and it adds one decision right, for closure only.

## Terms

- **Threat.** A future event that would damage governed work if it happened.
- **Score.** The product of `likelihood` and `impact`, each an integer from 1 to
  5, so a value from 1 to 25.
- **Residual.** What remains of the threat after the answer, in one sentence.
- **Closure.** The move to `mitigated`, the only risk state that asserts the
  threat was reduced by checked work.

## State model

```text
identified -> raised                        identified -> withdrawn
raised -> accepted | avoided | mitigating   raised -> withdrawn
mitigating -> mitigated                     mitigating -> withdrawn
```

`accepted`, `avoided`, `mitigated` and `withdrawn` are terminal and retained. No
risk state grants authority.

## Rules

**RSK-MGT-001.** `type = "risk"`, prefix `RISK-`, canonical directory `risks/`
in the domain; the layout registry, the templates index and
`ARTIFACT_AUTHORING.md` MUST name it.

**RSK-MGT-002.** A risk MUST declare `cause`, `effect`, `stage`, `category`,
`likelihood`, `impact`, `score` and `raised_by`; a missing field is `E-RSK-001`.

**RSK-MGT-003.** `likelihood` and `impact` MUST be integers from 1 to 5 and
`score` MUST equal their product; otherwise `E-RSK-002`.

**RSK-MGT-004.** `stage` MUST name exactly one of `definition`,
`architecture`, `implementation`, `verification`, `release` and `operation`.

**RSK-MGT-005.** `category` MUST name exactly one of `safety`, `security`,
`compliance`, `process`, `schedule` and `quality`.

**RSK-MGT-006.** `cause` and `effect` MUST each be one sentence naming one
cause and one consequence.

**RSK-MGT-007.** The workflow contract MUST declare the lifecycle family
`risk` with exactly the edges of this specification's state model.

**RSK-MGT-008.** No risk lifecycle state MUST grant authority, and
`accepted`, `avoided`, `mitigated` and `withdrawn` MUST be terminal.

**RSK-MGT-009.** `harnessctl raise-risk` MUST compute `score`, write the file
and apply `identified -> raised` in one act.

**RSK-MGT-010.** `raise-risk` MUST refuse and write nothing when a measurement
is out of range or the identifier is already declared anywhere.

**RSK-MGT-011.** No configuration key MUST govern the raise; every recorded
risk is raised, and no acceptance level is read from anywhere.

**RSK-MGT-012.** A risk in `raised` MUST be named in `concerns` by exactly one
decision in `open` or `deferred`; otherwise `E-RSK-003`.

**RSK-MGT-013.** That decision's `blocks` set MUST equal the risk's `threatens`
set; otherwise `E-RSK-004`.

**RSK-MGT-014.** This specification MUST NOT add a gate predicate or gate
group; the stop on a threatened artifact is `QGP-DECISION-OPEN`.

**RSK-MGT-015.** `raise-risk --with-decision` MUST write the decision beside
the risk with options `accept`, `avoid` and `mitigate`, and `blocks` equal to
`--threatens`.

**RSK-MGT-016.** `harnessctl decide --apply` on a decision concerning a raised
risk MUST also apply the risk transition its chosen option names.

**RSK-MGT-017.** A hold MUST use the decision's deferral, with scope and
revisit trigger, and MUST leave the risk in `raised`.

**RSK-MGT-018.** The risk's `[disposition]` table MUST be written only by that
act, carrying option, role, UTC time and verbatim reason; a hand-written table
is `E-RSK-005`.

**RSK-MGT-019.** Accepting MUST copy the decision's revisit trigger onto the
risk; `W-RSK-001` when that trigger has passed and no later decision concerns
the risk.

**RSK-MGT-020.** `mitigate` MUST record `mitigated_by`, naming one or more work
orders; `avoid` MUST record `avoided_by`, naming one ADR or one decision.

**RSK-MGT-021.** A risk's `status` MUST be written only by `raise-risk`,
`decide` or `transition`; no other command writes it.

**RSK-MGT-022.** `mitigating -> mitigated` MUST be applied by `harnessctl
transition` under `DR-RISK-CLOSE`, held by the assurance owner.

**RSK-MGT-023.** That transition MUST refuse unless every work order in
`mitigated_by` is covered by a `verified` or `released` record.

**RSK-MGT-024.** The validator MUST reject a risk in `mitigated` whose
`mitigated_by` work orders are not all so covered, as `E-RSK-006`.

**RSK-MGT-025.** `residual` MUST be present and non-empty on a risk in
`accepted` or `mitigated`; otherwise `E-RSK-007`.

**RSK-MGT-026.** `QGP-G4I-PATHS` MUST admit one added path
`docs/engineering/<domain>/risks/RISK-<DOMAIN>-NNN.md` for an in-progress work
order of that domain.

**RSK-MGT-027.** That admission MUST cover added files only; a modified or
deleted risk file still requires a declared path.

**RSK-MGT-028.** `prepare-release` MUST derive `[[risks]]` rows for every risk
in `raised`, `mitigating` or `accepted` that threatens an artifact of the
released-work closure.

**RSK-MGT-029.** Each row MUST carry the identifier, `score`, `status`, the
revisit trigger when present and `residual` when present.

**RSK-MGT-030.** The validator MUST reject a release record whose `[[risks]]`
rows differ from the derived set; the rows MUST NOT be hand-written.

**RSK-MGT-031.** `TRACEABILITY.md` MUST declare `threatens` as `RISK -> any`,
`mitigated_by` as `RISK -> WO` and `avoided_by` as `RISK -> ADR or DEC`, with
the catalog row for `risk`.

**RSK-MGT-032.** `DECISION_RIGHTS.md` MUST declare `DR-RISK-CLOSE` and MUST NOT
declare any right to dispose a risk; disposal stays `DR-DECISION-DISPOSE`.

**RSK-MGT-033.** `harnessctl risks --artifact ID` MUST list the risks
threatening that artifact and its governing chain, and MUST write nothing.

**RSK-MGT-034.** `renumber-artifacts` MUST treat `RISK-` like every other
prefix, and a terminal risk MUST NOT be deleted or rewritten.

**RSK-MGT-035.** The Explorer's in-flight tile MUST list every risk in `raised`
or `mitigating` with its score and the artifacts it threatens.

**RSK-MGT-036.** Each rule from RSK-MGT-001 to RSK-MGT-035 MUST have a test
that fails on the code before its change and passes after it.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| a required field is missing | the risk is rejected, naming the field | `E-RSK-001` |
| likelihood, impact or score is wrong | the risk is rejected, naming the value | `E-RSK-002` |
| a raised risk names no pending decision | the risk is rejected, naming the corrective command | `E-RSK-003` |
| the decision blocks a different set | the risk is rejected, naming both sets | `E-RSK-004` |
| a disposition was typed by hand | the risk is rejected | `E-RSK-005` |
| `mitigated` without verified coverage | the risk is rejected, naming the uncovered work order | `E-RSK-006` |
| `accepted` or `mitigated` without a residual | the risk is rejected | `E-RSK-007` |
| an accepted risk's revisit trigger has passed | a warning on the risk | `W-RSK-001` |
| a release record's rows differ from the derived set | the record is rejected | `E-RSK-008` |
| `raise-risk` receives an out-of-range measurement | refusal on standard error, nothing written | none |

## Examples

**Given** a work order in progress, **when** `raise-risk --domain DST
--likelihood 3 --impact 4 --threatens WO-DST-030 --with-decision` runs, **then**
a risk of score twelve is `raised` and a decision blocks `WO-DST-030`
(RSK-MGT-009, RSK-MGT-015).

**Given** that risk, **when** `WO-DST-030` asks to become `implemented`,
**then** the refusal names the decision and its three options, not the risk
(RSK-MGT-014).

**Given** that decision, **when** the owner disposes it with `mitigate`,
**then** the risk becomes `mitigating` and names the mitigating work order
(RSK-MGT-016, RSK-MGT-020).

**Given** a `mitigating` risk whose work order only reached `implemented`,
**when** closure is applied, **then** the transition refuses and the risk stays
`mitigating` (RSK-MGT-023).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-RSK-010` | RSK-MGT-001, RSK-MGT-002, RSK-MGT-003, RSK-MGT-004, RSK-MGT-005, RSK-MGT-006, RSK-MGT-036 |
| `REQ-RSK-011` | RSK-MGT-009, RSK-MGT-010, RSK-MGT-011 |
| `REQ-RSK-012` | RSK-MGT-007, RSK-MGT-008, RSK-MGT-012, RSK-MGT-013, RSK-MGT-014, RSK-MGT-015, RSK-MGT-033, RSK-MGT-035 |
| `REQ-RSK-013` | RSK-MGT-016, RSK-MGT-017, RSK-MGT-018, RSK-MGT-019, RSK-MGT-020, RSK-MGT-021, RSK-MGT-031, RSK-MGT-034 |
| `REQ-RSK-014` | RSK-MGT-022, RSK-MGT-023, RSK-MGT-024, RSK-MGT-025, RSK-MGT-032 |
| `REQ-RSK-015` | RSK-MGT-026, RSK-MGT-027 |
| `REQ-RSK-016` | RSK-MGT-028, RSK-MGT-029, RSK-MGT-030 |

## Data and interface contracts

```toml
id = "RISK-DST-001"
type = "risk"
status = "raised"
title = "The reduced configuration lands in a consumer that never upgrades"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
stage = "release"
category = "process"
cause = "A consumer pins the harness and never runs the upgrade."
effect = "The consumer keeps writing keys the evaluator no longer reads."
likelihood = 3
impact = 2
score = 6
raised_by = "implementation-agent"
residual = ""

[relations]
threatens = ["WO-DST-030"]
```

The `[disposition]` table and the `mitigated_by` and `avoided_by` relations are
written by the tool, never by hand.

## Not decided here

- Test names and placement.
- Whether the two commands share one module with the decision code.
- The Explorer's wording and the ordering of the in-flight rows.
- Whether a later amendment introduces a raise threshold, and on what evidence.
- The row order of the release register.
