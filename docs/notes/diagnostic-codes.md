<!-- GENERATED FILE (WO-TCM-003). Do not edit by hand: regenerate with
     python -m repository_tools.diagnostic_code_index --write
     tests/test_diagnostic_code_index.py fails when this page drifts. -->

# Diagnostic code index

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

## Summary

When a harness command refuses, or a validation reports a problem, it
prints a short code such as `MG001`, `WEX210` or `E012` beside its
message. This page lists every diagnostic code the candidate source can
emit, grouped by prefix, with the message text each code appears in. It
is generated from the source by
`repository_tools/diagnostic_code_index.py`, so it cannot drift, and a
test fails the suite when it does. The installed root evaluator is a
released version and may emit a slightly older set until the repository
adopts the next release.

262 codes across 30 registered prefixes.

## How to read a code

The prefix names the component that speaks; the number identifies the
exact rule or failure. Artifact identifiers such as `WO-ECP-010` and
specification rule identifiers such as `ECP-DLG-001` share this shape
but are not diagnostics and are not listed here.

| Prefix | Component | Meaning | Codes |
| --- | --- | --- | ---: |
| `E` | installed validator | an artifact-graph or integrity error; validation fails. | 19 |
| `E-AUT` | installed validator | an authoring-rule error on a formal artifact. | 2 |
| `E-CIP` | installed validator | a CI-pipeline rule error. | 1 |
| `E-DCM` | installed validator | a decision-artifact rule error. | 4 |
| `E-ECP` | installed validator | a control-plane rule error. | 1 |
| `W` | installed validator | a warning; validation still passes. | 19 |
| `W-ADS` | installed validator | an agent-directive-surface warning. | 2 |
| `W-AUT` | installed validator | an authoring-style advisory, raised only on drafts. | 4 |
| `W-DCM` | installed validator | a decision-artifact warning. | 2 |
| `W-ECP` | installed validator | a control-plane warning. | 2 |
| `W-REB` | installed validator | a released-evaluator-boundary warning. | 3 |
| `W-REV` | installed validator | a revision-provenance warning. | 3 |
| `W-HEX` | dashboard and inspection scripts | a Harness Explorer publication warning. | 6 |
| `A` | preflight | the artifact graph could not be read or validated. | 1 |
| `I` | preflight | an installation check failed. | 1 |
| `WEX` | workflow execution | a check, transition, or evidence operation is refused. | 16 |
| `WEX-ADS` | workflow execution | a directive-surface workflow refusal. | 2 |
| `WEX-ECP` | workflow execution | a control-plane workflow refusal. | 13 |
| `MG` | mutation guard | an installed-root write is refused before any file changes. | 5 |
| `RID` | runtime identity | the running evaluator's identity could not be proven. | 25 |
| `EPS` | interpreter safety | the environment entry-point safety rule failed. | 11 |
| `JNL` | journaled apply | the journaled writer refused or could not recover. | 10 |
| `PRE` | evaluator-facts derivation | CI could not derive a complete fact set from the declared root. | 10 |
| `REN` | renumber-artifacts | an identifier-renumbering plan or apply is refused. | 81 |
| `RQ` | release qualification | a qualification result could not be produced or retained. | 2 |
| `CC` | release qualification | a complete-candidate check. | 4 |
| `CP` | release qualification | a candidate-package check. | 2 |
| `RR` | release qualification | a released-root check. | 4 |
| `PI` | release qualification | a public-install check. | 5 |
| `PV` | release qualification | retired predecessor-view codes, reserved and emitted by no path. | 2 |

## Codes

### `E` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E001` | `E001` |
| `E002` | `E002` |
| `E003` | `E003` |
| `E004` | `E004` |
| `E005` | `E005` |
| `E006` | `E006` |
| `E007` | `E007` |
| `E008` | `E008` |
| `E009` | `E009` |
| `E010` | `E010` |
| `E011` | `E011` |
| `E012` | `E012`; `Rehearse the real root-evaluator handover: the successor's `upgrade --apply`. `WO-ECP-010` (`REQ-ECP-012`, `S…` (+3 more) |
| `E014` | `E014` |
| `E015` | `E015` |
| `E016` | `E016` |
| `E017` | `E017` |
| `E018` | `E018` |
| `E019` | `E019` |
| `E020` | `E020` |

### `E-AUT` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-AUT-001` | `E-AUT-001` |
| `E-AUT-002` | `E-AUT-002` |

### `E-CIP` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-CIP-001` | `CIP-RLU: a release contract that names a candidate commit declares the census the history yields. A contract …`; `E-CIP-001:` (+6 more) |

### `E-DCM` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-DCM-001` | `E-DCM-001` |
| `E-DCM-002` | `E-DCM-002` |
| `E-DCM-003` | `E-DCM-003` |
| `E-DCM-004` | `E-DCM-004:` |

### `E-ECP` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-ECP-001` | `E-ECP-001` |

### `W` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W001` | `W001` |
| `W002` | `W002` |
| `W003` | `W003` |
| `W004` | `W004` |
| `W005` | `W005` |
| `W010` | `W010` |
| `W011` | `W011` |
| `W012` | `W012` |
| `W013` | `W013` |
| `W014` | `W014` |
| `W015` | `W015` |
| `W016` | `W016` |
| `W017` | `W017` |
| `W018` | `W018` |
| `W019` | `W019` |
| `W020` | `W020` |
| `W021` | `W021` |
| `W022` | `W022` |
| `W023` | `W023` |

### `W-ADS` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-ADS-001` | `Report W-ADS-001 for a pull-request body whose trailer carries a carriage return.`; `UTF-8 byte offsets of a carriage return that ends a Harness-Work-Order line (W-ADS-001).` (+3 more) |
| `W-ADS-002` | `W-ADS-002`; `W-ADS-002:` (+1 more) |

### `W-AUT` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-AUT-001` | `W-AUT-001` |
| `W-AUT-002` | `W-AUT-002` |
| `W-AUT-003` | `W-AUT-003` |
| `W-AUT-004` | `W-AUT-004` |

### `W-DCM` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-DCM-001` | `W-DCM-001` |
| `W-DCM-002` | `W-DCM-002` |

### `W-ECP` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-ECP-002` | `. W-ECP-002: the packet carries no machine header; migrate it with harnessctl evidence . --artifact` |
| `W-ECP-005` | `W-ECP-005: delegation.gate_source is local-file outside a rehearsal; the gate this run reads is not the CI pr…` |

### `W-REB` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-REB-001` | `W-REB-001` |
| `W-REB-002` | `W-REB-002` |
| `W-REB-003` | `W-REB-003` |

### `W-REV` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-REV-002` | `W-REV-002` |
| `W-REV-003` | `W-REV-003` |
| `W-REV-004` | `W-REV-004` |

### `W-HEX` — dashboard and inspection scripts

| Code | Message text in the source |
| --- | --- |
| `W-HEX-001` | `W-HEX-001` |
| `W-HEX-002` | `W-HEX-002` |
| `W-HEX-003` | `W-HEX-003` |
| `W-HEX-004` | `W-HEX-004` |
| `W-HEX-005` | `W-HEX-005` |
| `W-HEX-006` | `W-HEX-006` |

### `A` — preflight

| Code | Message text in the source |
| --- | --- |
| `A001` | `A001` |

### `I` — preflight

| Code | Message text in the source |
| --- | --- |
| `I001` | `I001` |

### `WEX` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX001` | `WEX001` |
| `WEX190` | `WEX190` |
| `WEX200` | `WEX200`; `WEX200:` (+22 more) |
| `WEX201` | `WEX201`; `WEX201: changed path is outside execution scope:` |
| `WEX210` | `WEX210`; `WEX210:` (+13 more) |
| `WEX220` | `WEX220: --procedure is required for pre-action`; `WEX220: procedure` (+1 more) |
| `WEX221` | `WEX221: optional procedure parameter`; `WEX221: procedure parameter` (+3 more) |
| `WEX230` | `WEX230: blocked restitution requires an exact blocker`; `WEX230: canonical restitution requires schema 2` (+13 more) |
| `WEX301` | `Composed at run time as WEX30 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the state cause.` |
| `WEX302` | `Composed at run time as WEX30 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the provenance cause.` |
| `WEX303` | `Composed at run time as WEX30 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the evidence cause.` |
| `WEX304` | `Composed at run time as WEX30 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the inputs cause.` |
| `WEX401` | `Composed at run time as WEX40 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the state cause.` |
| `WEX402` | `Composed at run time as WEX40 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the provenance cause.` |
| `WEX403` | `Composed at run time as WEX40 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the evidence cause.` |
| `WEX404` | `Composed at run time as WEX40 plus the cause digit (state 1, provenance 2, evidence 3, inputs 4); this one is the inputs cause.` |

### `WEX-ADS` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX-ADS-001` | `WEX-ADS-001:`; `WEX-ADS-001: step` (+1 more) |
| `WEX-ADS-003` | `WEX-ADS-003: operating card is` |

### `WEX-ECP` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX-ECP-001` | `WEX-ECP-001:` |
| `WEX-ECP-002` | `WEX-ECP-002: --from-git is mutually exclusive with --changed-path, --changes-complete and --change-manifest` |
| `WEX-ECP-003` | `Derive the change set from Git (ECP-CHG-002 to -004). The set is the union of `git diff --name-only BASE` aga…`; `WEX-ECP-003:` (+4 more) |
| `WEX-ECP-010` | `Split a packet into its machine header and retained body (ECP-EVD-002, -004). Returns `(None, data)` when no …`; `WEX-ECP-010` (+10 more) |
| `WEX-ECP-011` | `WEX-ECP-011: a .gitattributes rule would convert line endings of` |
| `WEX-ECP-012` | `WEX-ECP-012: the working tree selects` |
| `WEX-ECP-013` | `WEX-ECP-013:`; `WEX-ECP-013: domain` (+4 more) |
| `WEX-ECP-014` | `WEX-ECP-014:`; `WEX-ECP-014: the generated body does not round-trip through the selector` (+1 more) |
| `WEX-ECP-022` | `WEX-ECP-022` |
| `WEX-ECP-030` | `WEX-ECP-030:`; `WEX-ECP-030: duplicate transition binding` (+8 more) |
| `WEX-ECP-040` | `WEX-ECP-040` |
| `WEX-ECP-041` | `WEX-ECP-041` |
| `WEX-ECP-042` | `WEX-ECP-042` |

### `MG` — mutation guard

| Code | Message text in the source |
| --- | --- |
| `MG001` | `MG001`; `prints a short code such as `MG001`, `WEX210` or `E012` beside its` |
| `MG003` | `MG003` |
| `MG004` | `MG004` |
| `MG005` | `MG005` |
| `MG006` | `MG006` |

### `RID` — runtime identity

| Code | Message text in the source |
| --- | --- |
| `RID000` | `RID000` |
| `RID001` | `RID001` |
| `RID002` | `RID002` |
| `RID003` | `RID003` |
| `RID004` | `RID004` |
| `RID005` | `RID005` |
| `RID006` | `RID006` |
| `RID007` | `RID007` |
| `RID008` | `RID008` |
| `RID009` | `RID009` |
| `RID010` | `RID010` |
| `RID011` | `RID011` |
| `RID012` | `RID012` |
| `RID013` | `RID013` |
| `RID014` | `RID014` |
| `RID015` | `RID015` |
| `RID016` | `RID016` |
| `RID017` | `RID017` |
| `RID018` | `RID018` |
| `RID019` | `RID019` |
| `RID020` | `RID020` |
| `RID021` | `RID021` |
| `RID022` | `RID022` |
| `RID023` | `RID023` |
| `RID024` | `RID024` |

### `EPS` — interpreter safety

| Code | Message text in the source |
| --- | --- |
| `EPS001` | `EPS001` |
| `EPS002` | `EPS002` |
| `EPS003` | `EPS003` |
| `EPS004` | `EPS004` |
| `EPS005` | `EPS005` |
| `EPS006` | `EPS006` |
| `EPS007` | `EPS007` |
| `EPS008` | `EPS008` |
| `EPS009` | `EPS009` |
| `EPS010` | `EPS010` |
| `EPS011` | `EPS011`; `Report whether this runtime can classify a path as a symbolic link or junction. Symbolic-link detection is pr…` |

### `JNL` — journaled apply

| Code | Message text in the source |
| --- | --- |
| `JNL001` | `JNL001` |
| `JNL002` | `JNL002` |
| `JNL003` | `JNL003` |
| `JNL004` | `JNL004` |
| `JNL005` | `JNL005` |
| `JNL006` | `JNL006` |
| `JNL007` | `JNL007` |
| `JNL010` | `JNL010` |
| `JNL013` | `JNL013` |
| `JNL014` | `JNL014` |

### `PRE` — evaluator-facts derivation

| Code | Message text in the source |
| --- | --- |
| `PRE001` | `PRE001:` |
| `PRE002` | `PRE002:` |
| `PRE003` | `PRE003: cannot read the candidate version from` |
| `PRE004` | `PRE004: cannot read` |
| `PRE005` | `PRE005: cannot read` |
| `PRE006` | `PRE006:` |
| `PRE007` | `PRE007: declared root versions disagree:` |
| `PRE008` | `PRE008: the candidate version` |
| `PRE014` | `PRE014:` |
| `PRE015` | `PRE015:` |

### `REN` — renumber-artifacts

| Code | Message text in the source |
| --- | --- |
| `REN001` | `REN001` |
| `REN002` | `REN002` |
| `REN003` | `REN003` |
| `REN004` | `REN004` |
| `REN005` | `REN005` |
| `REN006` | `REN006` |
| `REN007` | `REN007` |
| `REN008` | `REN008` |
| `REN009` | `REN009` |
| `REN010` | `REN010` |
| `REN011` | `REN011` |
| `REN012` | `REN012` |
| `REN013` | `REN013` |
| `REN014` | `REN014` |
| `REN015` | `REN015` |
| `REN016` | `REN016` |
| `REN017` | `REN017` |
| `REN018` | `REN018` |
| `REN019` | `REN019` |
| `REN020` | `REN020` |
| `REN021` | `REN021` |
| `REN022` | `REN022` |
| `REN023` | `REN023` |
| `REN024` | `REN024` |
| `REN025` | `REN025` |
| `REN026` | `REN026` |
| `REN027` | `REN027` |
| `REN028` | `REN028` |
| `REN029` | `REN029` |
| `REN030` | `REN030` |
| `REN031` | `REN031` |
| `REN032` | `REN032` |
| `REN033` | `REN033` |
| `REN034` | `REN034` |
| `REN035` | `REN035` |
| `REN036` | `REN036` |
| `REN037` | `REN037` |
| `REN038` | `REN038` |
| `REN039` | `REN039` |
| `REN040` | `REN040` |
| `REN041` | `REN041` |
| `REN042` | `REN042` |
| `REN043` | `REN043` |
| `REN044` | `REN044` |
| `REN045` | `REN045` |
| `REN046` | `REN046` |
| `REN047` | `REN047` |
| `REN048` | `REN048` |
| `REN049` | `REN049` |
| `REN050` | `REN050` |
| `REN051` | `REN051` |
| `REN052` | `REN052` |
| `REN053` | `REN053` |
| `REN054` | `REN054` |
| `REN055` | `REN055` |
| `REN056` | `REN056` |
| `REN057` | `REN057` |
| `REN058` | `REN058` |
| `REN059` | `REN059` |
| `REN060` | `REN060` |
| `REN061` | `REN061` |
| `REN062` | `REN062` |
| `REN063` | `REN063` |
| `REN064` | `REN064` |
| `REN065` | `REN065` |
| `REN066` | `REN066` |
| `REN067` | `REN067` |
| `REN068` | `REN068` |
| `REN069` | `REN069` |
| `REN070` | `REN070` |
| `REN071` | `REN071` |
| `REN072` | `REN072` |
| `REN073` | `REN073` |
| `REN074` | `REN074` |
| `REN075` | `REN075` |
| `REN076` | `REN076` |
| `REN077` | `REN077` |
| `REN078` | `REN078` |
| `REN079` | `REN079` |
| `REN080` | `REN080` |
| `REN081` | `REN081` |

### `RQ` — release qualification

| Code | Message text in the source |
| --- | --- |
| `RQ001` | `RQ001` |
| `RQ002` | `RQ002` |

### `CC` — release qualification

| Code | Message text in the source |
| --- | --- |
| `CC001` | `CC001` |
| `CC002` | `CC002` |
| `CC003` | `CC003` |
| `CC004` | `CC004` |

### `CP` — release qualification

| Code | Message text in the source |
| --- | --- |
| `CP001` | `CP001` |
| `CP002` | `CP002` |

### `RR` — release qualification

| Code | Message text in the source |
| --- | --- |
| `RR001` | `RR001` |
| `RR002` | `RR002` |
| `RR003` | `RR003` |
| `RR004` | `RR004` |

### `PI` — release qualification

| Code | Message text in the source |
| --- | --- |
| `PI001` | `PI001` |
| `PI002` | `PI002` |
| `PI003` | `PI003` |
| `PI004` | `PI004` |
| `PI005` | `PI005` |

### `PV` — release qualification

| Code | Message text in the source |
| --- | --- |
| `PV001` | `PV001` |
| `PV002` | `PV002` |
