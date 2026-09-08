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

196 codes across 30 registered prefixes.

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
| `E-DCM` | installed validator | a decision-artifact rule error. | 5 |
| `E-ECP` | installed validator | a control-plane rule error. | 1 |
| `E-RSK` | installed validator | a risk-artifact rule error. | 5 |
| `W` | installed validator | a warning; validation still passes. | 19 |
| `W-ADS` | installed validator | an agent-directive-surface warning. | 2 |
| `W-AUT` | installed validator | an authoring-style advisory, raised only on drafts. | 23 |
| `W-DCM` | installed validator | a decision-artifact warning. | 2 |
| `W-ECP` | installed validator | a control-plane warning. | 2 |
| `W-REB` | installed validator | a released-evaluator-boundary warning. | 3 |
| `W-REV` | installed validator | a revision-provenance warning. | 3 |
| `W-RSK` | installed validator | a risk-artifact warning. | 1 |
| `W-HEX` | dashboard and inspection scripts | a Harness Explorer publication warning. | 6 |
| `A` | preflight | the artifact graph could not be read or validated. | 1 |
| `I` | preflight | an installation check failed. | 1 |
| `WEX` | workflow execution | a check, transition, or evidence operation is refused. | 16 |
| `WEX-ADS` | workflow execution | a directive-surface workflow refusal. | 2 |
| `WEX-ECP` | workflow execution | a control-plane workflow refusal. | 12 |
| `MG` | mutation guard | an installed-root write is refused before any file changes. | 5 |
| `RID` | runtime identity | the running evaluator's identity could not be proven. | 25 |
| `EPS` | interpreter safety | the environment entry-point safety rule failed. | 11 |
| `PRE` | evaluator-facts derivation | CI could not derive a complete fact set from the declared root. | 10 |
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
| `E-CIP-001` | `CIP-RLU: a release contract that names a candidate commit declares the census the history yields. A contract …`; `E-CIP-001` (+7 more) |

### `E-DCM` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-DCM-001` | `E-DCM-001` |
| `E-DCM-002` | `E-DCM-002` |
| `E-DCM-003` | `E-DCM-003` |
| `E-DCM-004` | `E-DCM-004`; `E-DCM-004: {…} has an open decision written as prose: {…} (the Open decisions section reads exactly None, or …` |
| `E-DCM-005` | `E-DCM-005` |

### `E-ECP` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-ECP-001` | `E-ECP-001` |

### `E-RSK` — installed validator

| Code | Message text in the source |
| --- | --- |
| `E-RSK-001` | `E-RSK-001` |
| `E-RSK-002` | `E-RSK-002` |
| `E-RSK-003` | `E-RSK-003` |
| `E-RSK-004` | `E-RSK-004` |
| `E-RSK-005` | `E-RSK-005` |

### `W` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W001` | `W001`; `W001: invalid work-order ID` |
| `W002` | `W002`; `W002: unknown work-order ID` |
| `W003` | `W003`; `W003: work-order ID is not unique` |
| `W004` | `W004`; `W004: selected artifact is not a work order` |
| `W005` | `W005`; `W005: status {…} is not eligible for {…}; expected one of {…}` |
| `W010` | `W010`; `W010: required relation {…} is empty` |
| `W011` | `W011`; `W011: missing target of {…}` |
| `W012` | `W012`; `W012: {…} targets type {…}` |
| `W013` | `W013`; `W013: governing artifact {…} is not active` |
| `W014` | `W014` |
| `W015` | `W015` |
| `W016` | `W016`; `W016: {…} coverage is missing {…}` |
| `W017` | `W017`; `W017: ADR does not decide a selected architecture` |
| `W018` | `W018`; `W018: adr_required architecture {…} has no selected active deciding ADR` |
| `W019` | `W019`; `W019: legacy architecture {…} has no selected active deciding ADR` |
| `W020` | `W020`; `W020: architecture {…} has no valid decision assessment: {…}` |
| `W021` | `W021`; `W021: selected architecture {…} is unrelated to selected specifications or requirements` |
| `W022` | `W022`; `W022: applicable architecture {…} is not selected by the work order` |
| `W023` | `W023` |

### `W-ADS` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-ADS-001` | `A coded selection refusal (W-ADS-001, WEX-ECP-014): a `SelectionError` that carries its code.`; `Report W-ADS-001 for a pull-request body whose trailer carries a carriage return.` (+4 more) |
| `W-ADS-002` | `W-ADS-002`; `W-ADS-002: ready verification records for the work order whose candidate left HEAD.` (+1 more) |

### `W-AUT` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-AUT-001` | `W-AUT-001` |
| `W-AUT-002` | `W-AUT-002` |
| `W-AUT-003` | `W-AUT-003` |
| `W-AUT-004` | `W-AUT-004` |
| `W-AUT-005` | `W-AUT-005` |
| `W-AUT-006` | `W-AUT-006` |
| `W-AUT-007` | `W-AUT-007` |
| `W-AUT-008` | `W-AUT-008` |
| `W-AUT-009` | `W-AUT-009` |
| `W-AUT-010` | `W-AUT-010` |
| `W-AUT-011` | `W-AUT-011` |
| `W-AUT-012` | `W-AUT-012` |
| `W-AUT-013` | `W-AUT-013` |
| `W-AUT-014` | `W-AUT-014` |
| `W-AUT-015` | `W-AUT-015` |
| `W-AUT-016` | `W-AUT-016` |
| `W-AUT-017` | `W-AUT-017` |
| `W-AUT-018` | `W-AUT-018` |
| `W-AUT-019` | `W-AUT-019` |
| `W-AUT-020` | `W-AUT-020` |
| `W-AUT-021` | `W-AUT-021` |
| `W-AUT-022` | `W-AUT-022` |
| `W-AUT-023` | `W-AUT-023` |

### `W-DCM` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-DCM-001` | `W-DCM-001` |
| `W-DCM-002` | `W-DCM-002` |

### `W-ECP` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-ECP-002` | `W-ECP-002` |
| `W-ECP-005` | `W-ECP-005`; `W-ECP-005: delegation.gate_source is local-file outside a rehearsal; the gate this run reads is not the CI pr…` |

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

### `W-RSK` — installed validator

| Code | Message text in the source |
| --- | --- |
| `W-RSK-001` | `W-RSK-001` |

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
| `A001` | `A001`; `A001: validator unavailable: {…}` |

### `I` — preflight

| Code | Message text in the source |
| --- | --- |
| `I001` | `I001` |

### `WEX` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX001` | `WEX001` |
| `WEX190` | `WEX190` |
| `WEX200` | `WEX200`; `WEX200: --change-manifest is mutually exclusive with --changed-path and --changes-complete` (+23 more) |
| `WEX201` | `Generate the diagnostic-code index note from the candidate source. `WO-TCM-003` (`REQ-TCM-005`, `SPEC-TCM-002…`; `WEX201` (+2 more) |
| `WEX210` | `Generate the diagnostic-code index note from the candidate source. `WO-TCM-003` (`REQ-TCM-005`, `SPEC-TCM-002…`; `WEX210` (+16 more) |
| `WEX220` | `WEX220`; `WEX220: --procedure is required for pre-action` (+3 more) |
| `WEX221` | `WEX221`; `WEX221: optional procedure parameter {…} has an invalid value` (+8 more) |
| `WEX230` | `A schema-2 result or restitution that does not hold (WEX230); a `ValueError` to its callers.`; `WEX230` (+15 more) |
| `WEX301` | `WEX301` |
| `WEX302` | `WEX302` |
| `WEX303` | `WEX303` |
| `WEX304` | `WEX304` |
| `WEX401` | `WEX401` |
| `WEX402` | `WEX402` |
| `WEX403` | `WEX403` |
| `WEX404` | `WEX404` |

### `WEX-ADS` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX-ADS-001` | `WEX-ADS-001`; `WEX-ADS-001: step {…} has no corrective form for {…}` (+9 more) |
| `WEX-ADS-003` | `WEX-ADS-003`; `WEX-ADS-003: operating card is {…} bytes; limit is {…}` |

### `WEX-ECP` — workflow execution

| Code | Message text in the source |
| --- | --- |
| `WEX-ECP-001` | `WEX-ECP-001` |
| `WEX-ECP-002` | `WEX-ECP-002`; `WEX-ECP-002: --from-git is mutually exclusive with --changed-path, --changes-complete and --change-manifest` |
| `WEX-ECP-003` | `Derive the change set from Git (ECP-CHG-002 to -004). The set is the union of `git diff --name-only BASE` aga…`; `WEX-ECP-003` (+4 more) |
| `WEX-ECP-010` | `Split a packet into its machine header and retained body (ECP-EVD-002, -004). Returns `(None, data)` when no …`; `WEX-ECP-010` (+13 more) |
| `WEX-ECP-011` | `WEX-ECP-011`; `WEX-ECP-011: a .gitattributes rule would convert line endings of {…} ({…})` |
| `WEX-ECP-012` | `WEX-ECP-012`; `WEX-ECP-012: the working tree selects {…} (the one in_progress work order), not {…}` |
| `WEX-ECP-013` | `WEX-ECP-013`; `WEX-ECP-013: domain {…} has no artifact to read its identifier token from; pass --id explicitly` (+4 more) |
| `WEX-ECP-014` | `A coded selection refusal (W-ADS-001, WEX-ECP-014): a `SelectionError` that carries its code.`; `WEX-ECP-014` (+5 more) |
| `WEX-ECP-022` | `WEX-ECP-022`; `WEX-ECP-022: {…} carries no [delegation] class at the base {…}; a branch cannot widen its own delegation` (+2 more) |
| `WEX-ECP-030` | `WEX-ECP-030`; `WEX-ECP-030: duplicate transition binding {…}:{…}` (+11 more) |
| `WEX-ECP-031` | `Read and validate `agentic_operations` (ECP-PRM-019, ECP-PRM-023). Every entry carries exactly the seven fiel…`; `WEX-ECP-031` |
| `WEX-ECP-040` | `WEX-ECP-040`; `WEX-ECP-040: check {…} is missing at head {…}` (+13 more) |

### `MG` — mutation guard

| Code | Message text in the source |
| --- | --- |
| `MG001` | `MG001`; `MG001: cannot read the standard config: {…}` (+6 more) |
| `MG003` | `MG003`; `MG003: standard config and lock tool versions differ` |
| `MG004` | `MG004`; `MG004: cannot identify the target evaluator: {…}` (+1 more) |
| `MG005` | `MG005` |
| `MG006` | `MG006`; `MG006: cannot canonicalize evaluator evidence: {…}` |

### `RID` — runtime identity

| Code | Message text in the source |
| --- | --- |
| `RID000` | `RID000` |
| `RID001` | `RID001`; `RID001: unsupported runtime role` |
| `RID002` | `RID002`; `RID002: resolved {…}; expected {…}` |
| `RID003` | `RID003`; `RID003: origin is outside the expected runtime root` |
| `RID004` | `RID004`; `RID004: installed-runtime path is outside its environment` (+2 more) |
| `RID005` | `RID005`; `RID005: checkout boundary is required` |
| `RID006` | `RID006`; `RID006: installed runtime launcher is inside the checkout` (+1 more) |
| `RID007` | `RID007`; `RID007: effective import search contains the checkout` |
| `RID008` | `RID008`; `RID008: runtime inherited PYTHONPATH` |
| `RID009` | `RID009`; `RID009: runtime enables user site-packages` |
| `RID010` | `RID010`; `RID010: harnessctl resolves outside the environment` |
| `RID011` | `RID011`; `RID011: harnessctl entry point is unavailable` |
| `RID012` | `RID012`; `RID012: candidate source root must equal the checkout root` |
| `RID013` | `RID013`; `RID013: the optional digest must be a lowercase SHA-256` |
| `RID014` | `RID014`; `RID014: released evaluator identity cannot claim a candidate commit` |
| `RID015` | `RID015`; `RID015: a full lowercase candidate commit is required` |
| `RID016` | `RID016`; `RID016: candidate identity cannot claim a released evaluator digest` |
| `RID017` | `RID017`; `RID017: Python isolated mode is required` |
| `RID018` | `RID018`; `RID018: source distribution metadata resolves outside the checkout` |
| `RID019` | `RID019`; `RID019: installed payload identity failed: {…}` |
| `RID020` | `RID020`; `RID020: the expected payload digest must be a lowercase SHA-256` |
| `RID021` | `RID021`; `RID021: installed payload digest differs from the expected evaluator payload` |
| `RID022` | `RID022`; `RID022: installed PEP 610 archive digest differs from the expected evaluator wheel` |
| `RID023` | `RID023`; `RID023: candidate identity cannot claim a released evaluator payload` |
| `RID024` | `RID024`; `RID024: launcher refused by interpreter-safety case {…}` |

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

### `RQ` — release qualification

| Code | Message text in the source |
| --- | --- |
| `RQ001` | `RQ001` |
| `RQ002` | `RQ002` |

### `CC` — release qualification

| Code | Message text in the source |
| --- | --- |
| `CC001` | `CC001`; `CC001: candidate-runtime` |
| `CC002` | `CC002`; `CC002: candidate-commit` |
| `CC003` | `CC003`; `CC003: not run after candidate identity failure` |
| `CC004` | `CC004`; `CC004: repository-state` |

### `CP` — release qualification

| Code | Message text in the source |
| --- | --- |
| `CP001` | `CP001`; `CP001: released-verifier` |
| `CP002` | `CP002`; `CP002: candidate-wheel` (+2 more) |

### `RR` — release qualification

| Code | Message text in the source |
| --- | --- |
| `RR001` | `RR001`; `RR001: released-evaluator` (+1 more) |
| `RR002` | `RR002`; `RR002: not run after evaluator identity failure` (+1 more) |
| `RR003` | `RR003`; `RR003: not run after evaluator identity failure` |
| `RR004` | `RR004`; `RR004: repository-state` |

### `PI` — release qualification

| Code | Message text in the source |
| --- | --- |
| `PI001` | `PI001`; `PI001: public-wheel` |
| `PI002` | `PI002`; `PI002: installed-payload` |
| `PI003` | `PI003`; `PI003: installed-runtime` |
| `PI004` | `PI004`; `PI004: public-cli` |
| `PI005` | `PI005`; `PI005: repository-state` |

### `PV` — release qualification

| Code | Message text in the source |
| --- | --- |
| `PV001` | `PV001` |
| `PV002` | `PV002` |
