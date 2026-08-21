# Quality Gates

## Normative language

Uppercase **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** have the meanings defined by BCP 14 (RFC 2119 and RFC 8174). Lowercase forms have their ordinary meaning.

## Purpose

A quality gate is a named predicate. A gate reports `pass`, `fail`, or `not_assessable`. It does not approve an artifact or exercise a decision right.

**QG-001:** A workflow action that references a gate MUST proceed only when that gate reports `pass`.

**QG-002:** Missing, unreadable, or externally held required evidence MUST produce `not_assessable`; it MUST NOT be treated as `pass`.

**QG-003:** A failed or non-assessable required gate MUST leave lifecycle state unchanged.

## Gate catalog

| ID | Evaluated when | Pass predicate | Required evidence | Failure result |
| --- | --- | --- | --- | --- |
| `QG-G0-INTENT` | Definition work is proposed | An approved INT defines the problem, outcome, scope boundary, and accountable product owner; approved CAP and REQ artifacts derive from it | INT, CAP, REQ metadata and bodies | Definition packet is not eligible for approval |
| `QG-G1-DEFINITION` | A definition packet or WO is reviewed | Every selected active REQ has selected active SPEC and VER coverage | Formal graph and selected packet | Packet or WO is not eligible |
| `QG-G2-ARCHITECTURE` | Architecture is applicable | Every selected ARCH identifies its architecturally significant requirement drivers and conforming specifications; its decision assessment is valid; each `adr_required` architecture has active deciding ADR coverage | ARCH, SPEC, REQ, ADR metadata and decision assessment | Architecture or WO is not eligible |
| `QG-G3-WORK-AUTHORIZATION` | Implementation start is requested | One approved WO selects the complete applicable chain, declares assurance applicability, passes start preflight, and has no scoped or repository blocker | WO, reading manifest, start-preflight result | Implementation MUST NOT start |
| `QG-G4-IMPLEMENTATION-EVIDENCE` | WO completion is requested | Approved scope is implemented; required checks pass; retained evidence identifies the WO; review preflight passes; no scoped or repository blocker remains | Diff review, commands and results, evidence path, review-preflight result | WO MUST remain `in_progress` or be explicitly rejected |
| `QG-G4-CANDIDATE-READY` | VREC preparation is requested | Selected WO set is `implemented`; declared VER coverage and retained evidence are exact; candidate commit is clean and immutable for the record | Commit identity, worktree state, WO set, VER set, evidence paths, snapshot | No VREC is written |
| `QG-G4-ASSURANCE-DECISION` | A ready VREC is reviewed | Candidate identity, selected work, verification contracts, retained evidence, required tests, and unresolved findings have been assessed against the VER pass criteria | Ready VREC and retained evidence | Assurance owner MUST reject, request remediation, or leave the VREC ready |
| `QG-G4-VERIFIED-COVERAGE` | Delivery is considered | At least one eligible verified or released VREC covers the exact intended work and candidate | VREC relations and commit identity | Integration or release preparation MUST NOT claim verified coverage |
| `QG-G5-RELEASE-PREPARATION` | RLS preparation is requested | All included VRECs are eligible and verified; released-work equality, release-contract coverage, and commit identity equality pass | REL, VRECs, WOs, version and commit inputs | No RLS is written |
| `QG-G5-RELEASE-DECISION` | A ready RLS is reviewed | Release scope, verified coverage, version, rollback conditions, and release evidence satisfy the REL contract | Ready RLS, REL and retained release evidence | Release owner MUST reject, request remediation, or leave the RLS ready |
| `QG-G5-EXTERNAL-ACTION` | A tag, merge, publication, deployment, or operation is proposed | The exact action, target, accountable owner, prerequisites, and recovery conditions are explicit | Action-specific request and evidence | The external action MUST NOT occur |

The G0-G5 labels group related gates for reporting. They MUST NOT replace the exact gate IDs above.

## Validation assessment planes

| Plane | Meaning | Blocking rule |
| --- | --- | --- |
| `structure` | Formal syntax, identity, type, and graph shape | Error severity blocks; warning severity does not |
| `governance` | Non-waivable lifecycle, assurance, and provenance invariants | Error severity blocks |
| `policy` | A rule activated by explicit repository configuration | Configured error severity blocks |
| `maintenance` | Compatibility or placement advice | Non-blocking unless another exact rule raises an error |

**QG-004:** A diagnostic plane MUST NOT change error-versus-warning severity, lifecycle authority, or process exit behavior.

**QG-005:** Gates MUST NOT be replaced by an aggregate health score.

## Exceptions

**QG-006:** A `MUST` gate has no implicit exception.

**QG-007:** A documented `SHOULD` deviation MUST state the rule ID, reason, impact, accountable owner, and compensating evidence.

**QG-008:** A tool MUST report the exact failed predicate. It MUST NOT report only a generic message such as "quality is insufficient."

Workflow actions reference these gate IDs from [WORKFLOW.json](WORKFLOW.json). Decision ownership is defined by [DECISION_RIGHTS.md](DECISION_RIGHTS.md).
