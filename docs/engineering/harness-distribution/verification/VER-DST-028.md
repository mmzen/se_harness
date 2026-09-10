+++
id = "VER-DST-028"
type = "verification"
title = "Evidence for the issue #433 managed-template leftovers"
status = "draft"
owners = ["quality-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[relations]
verifies = ["REQ-DST-076", "REQ-DST-077"]
+++

# Verification Contract: Evidence for the issue #433 managed-template leftovers

## Independence

Cases are written from the rule identifiers of `SPEC-DST-028` and from issue
#433's acceptance, not from the diff. The template texts are read as a
consumer's installer would ship them, from `templates/repository/standard/`.
The parity case runs against this repository's released 0.17.0 root, which
the work may not touch. The candidate suite runs on the hosted Linux lane;
the local Windows suite is a control, not the record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-076` | test | the template's `TRC-008` (DST-TPL-001, DST-TPL-002) | the rule names `constrains` retired, says a validator refuses it with `E016` whatever the status, names `addresses` and `conforms_to` as the only form; `compatibility-only` and `MAY classify` are absent |
| `REQ-DST-076` | test | the rest of the template (DST-TPL-003) | the last sentence of the rule is unchanged; every other line equals the released root's |
| `REQ-DST-076` | inspection | issue #433 acceptance 1 | `grep -rn constrains` over the template names the relation retired and refused |
| `REQ-DST-076` | test | `docs/notes/harness-uml-model.md` (DST-TPL-005) | the note says the relation is retired and refused; "may still carry" is absent |
| `REQ-DST-077` | test | the template's completion report heading (DST-TPL-004) | the guidance under it names the engineering owner and the `delegated-executor` under `[delegation] class = "execution"` |
| `REQ-DST-077` | inspection | issue #433 acceptance 3 | a work order drafted from the candidate template carries no sentence giving completion to the engineering owner |
| both | test | the parity test (DST-TPL-006) | under the 0.17.0 root it strips exactly the two declared changes and finds equality; the equality branch is reached once a root carries them |
| both | inspection | this repository's root (DST-TPL-008) | the work order's diff touches no root managed file, not the lock, and no existing work order |
| both | regression | the full suite, `validate`, `doctor`, the hosted lanes | suite at its baseline; graph 0 errors under the released 0.17.0 evaluator; every lane green at the head |
| both | the work order's own lifecycle events | the start, implemented and record-preparation events name `delegated-executor` with the class, the check-run id and the head sha; the approval and verification events name humans |

DST-TPL-009 binds the later root-adoption work order and is verified by its
contract, not this one.

## Acceptance scenarios

Scenario A, the shipped rule: read `TRC-008` from the candidate template as
text; expected: retired, refused, `E016`, the typed pair, the unchanged last
sentence, no stale phrase.

Scenario B, the drafted work order: create a work order from the candidate
template into a scratch domain and read its completion section; expected:
the guidance names both deciders and no sentence gives the decision to the
engineering owner alone.

Scenario C, parity under the released root: run the parity test on this
checkout under the 0.17.0 root; expected: pass by the declared-exception
branch, with the two exceptions and nothing else stripped.

## Evidence retention

`docs/engineering/harness-distribution/evidence/WO-DST-027-verification.md`
with the rule before and after, the template guidance, the note sentence
before and after, the parity test's branch taken, the three scenario
outputs, the hosted lane's test report and the local control reading
labelled as such; the handoff packet under `evidence/WO-DST-027/`.

## Pass criteria

Every row passes on the hosted Linux lane and on the Windows workstation;
the released 0.17.0 evaluator's `validate` reports 0 errors; the pull
request's lanes are green through completion and the record head; no root
managed byte changes.

## Residual uncertainty

The end of the copying is observed on the next work order drafted after the
carrying release is adopted, not here. This repository's own root is not
exercised; the root-adoption work order verifies it.
