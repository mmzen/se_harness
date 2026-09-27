# Versioned rule reference mapping

The following IDs are references to numbered rules in the prior 0.18.0 human
guides. This table shows their location or explicit disposition in the
versioned instruction set. It does not make the old guides additional current policy.

An old reference retains the meaning of the version that issued it. For
example, prior `HRN-003` means bounded scope; consolidated `HRN-003` means
lifecycle authority. Do not reinterpret retained evidence using the new
numbering. The release migration must update active references or identify
their source version. It must preserve historical records.

The existing nine consolidated HRN IDs remain in their agreed order. Named
machine gate, predicate, procedure, and decision-right IDs remain unchanged.
Use the machine IDs returned by the evaluator and the procedure index in [CONTINUE.md](../CONTINUE.md#continue-selected-work).

| Prior rule | Consolidated location | Disposition |
| --- | --- | --- |
| `HRN-001` | [HRN-001 — Formal authority](../../../../ENGINEERING_HARNESS.md#hrn-001--formal-authority) | Retained |
| `HRN-002` | [HRN-007 — Repository ownership](../../../../ENGINEERING_HARNESS.md#hrn-007--repository-ownership) | Strengthened: owner-only AGENTS |
| `HRN-003` | [HRN-004 — Bounded scope](../../../../ENGINEERING_HARNESS.md#hrn-004--bounded-scope) | Retained; renumbered |
| `HRN-004` | [HRN-003 — Lifecycle authority](../../../../ENGINEERING_HARNESS.md#hrn-003--lifecycle-authority) | MAY strengthened to MUST; renumbered |
| `HRN-005` | [HRN-005 — Explicit decisions](../../../../ENGINEERING_HARNESS.md#hrn-005--explicit-decisions) | Retained and expanded |
| `HRN-006` | [HRN-006 — Targeted transitions](../../../../ENGINEERING_HARNESS.md#hrn-006--targeted-transitions) | Retained |
| `HRN-007` | [HRN-008 — Rule precedence](../../../../ENGINEERING_HARNESS.md#hrn-008--rule-precedence) | Retained; renumbered |
| `HRN-008` | [HRN-009 — Required checks](../../../../ENGINEERING_HARNESS.md#hrn-009--required-checks) | Retained; renumbered |
| `DR-001` | [HRN-005 — Explicit decisions](../../../../ENGINEERING_HARNESS.md#hrn-005--explicit-decisions) | Retained |
| `DR-002` | [HRN-006 — Targeted transitions](../../../../ENGINEERING_HARNESS.md#hrn-006--targeted-transitions) | Retained |
| `DR-003` | [Authority from work approval](../AUTHORITY.md#authority-from-work-approval) | Retained |
| `DR-004` | [Decision rights](../AUTHORITY.md#decision-rights) | Retained |
| `DR-005` | [Decision rights](../AUTHORITY.md#decision-rights) | Human decision and agent application clarified |
| `DR-006` | [Decision rights](../AUTHORITY.md#decision-rights) | Rejection reason and successor retained |
| `DR-007` | [Delegation and separation](../AUTHORITY.md#delegation-and-separation) | Human decision delegation; agent application distinguished |
| `DR-008` | [Delegation and separation](../AUTHORITY.md#delegation-and-separation) | Retained |
| `DR-009` | [Delegation and separation](../AUTHORITY.md#delegation-and-separation) | Retained under two profiles |
| `DR-010` | [Delegation and separation](../AUTHORITY.md#delegation-and-separation) | Retained under two profiles |
| `DR-011` | [Delegation and separation](../AUTHORITY.md#delegation-and-separation) | Retained under two profiles |
| `DR-012` | [Verify the outcome](../VERIFY_OUTCOME.md#4-verify-the-outcome) and [Deliver the result](../DELIVER_RESULT.md#5-deliver-the-result) | Preparation identity retained in the record-preparation procedures |
| `DR-013` | [HRN-006 — Targeted transitions](../../../../ENGINEERING_HARNESS.md#hrn-006--targeted-transitions) | Retained |
| `DR-014` | [HRN-006 — Targeted transitions](../../../../ENGINEERING_HARNESS.md#hrn-006--targeted-transitions) | Retained |
| `DR-015` | [Authority from work approval](../AUTHORITY.md#authority-from-work-approval) | Execution grant and historical boundary retained |
| `QG-001` | [Authorize the work](../AUTHORIZE_WORK.md#2-authorize-the-work) and [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Passing-check requirement retained in the procedures |
| `QG-002` | [Authorize the work](../AUTHORIZE_WORK.md#2-authorize-the-work) and [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Agent handling of not_assessable retained; result computation belongs to the evaluator specification |
| `QG-003` | [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Agent stop and reporting instructions retained; evaluator mutation guarantees belong to its specification |
| `QG-004` | [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Use reported severity and blocking effect; evaluator exit behavior omitted from agent instructions |
| `QG-005` | [Authorize the work](../AUTHORIZE_WORK.md#2-authorize-the-work) and [HRN-009 — Required checks](../../../../ENGINEERING_HARNESS.md#hrn-009--required-checks) | Required-check results govern progression; health-score implementation wording omitted |
| `QG-006` | [HRN-008 — Rule precedence](../../../../ENGINEERING_HARNESS.md#hrn-008--rule-precedence) and [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Required checks cannot be waived |
| `QG-007` | [Authorize the work — Resolve approval blockers](../AUTHORIZE_WORK.md#2-authorize-the-work) | Deviation documentation retained in the procedure |
| `QG-008` | [Authorize the work](../AUTHORIZE_WORK.md#2-authorize-the-work) and [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Report the returned identifier and reason; evaluator output requirements omitted |
| `QG-009` | — | Aggregation and predicate-evaluation rules omitted from agent instructions; evaluator specification responsibility |
| `QG-010` | [Execute the work](../EXECUTE_WORK.md#3-execute-the-work) and the transition procedures | Commands and handoff requirement retained; shared-evaluator implementation requirement omitted |
| `QG-011` | [Execute the work](../EXECUTE_WORK.md#3-execute-the-work) | Scope and handoff instructions retained; predicate checkpoint inheritance omitted |
| `TRC-001` | [Declared links](../DEFINITION_LINKS.md#declared-links) | Retained |
| `TRC-002` | [Declared links](../DEFINITION_LINKS.md#declared-links) | Retained |
| `TRC-003` | [Complete work scope](../WORK_AND_EVIDENCE.md#complete-work-scope) | Retained |
| `TRC-004` | [Architecture applicability](../DEFINITION_LINKS.md#architecture-applicability) | Retained |
| `TRC-005` | [Artifact data model](../ARTIFACTS.md#artifact-data-model) | Retained |
| `TRC-006` | [Architecture applicability](../DEFINITION_LINKS.md#architecture-applicability) | Retained |
| `TRC-007` | [Architecture decisions](../DEFINITION_LINKS.md#architecture-decisions) | Retained |
| `TRC-008` | [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Historical-link exposition omitted by agreement; record preservation retained |
| `TRC-009` | [Verification coverage](../WORK_AND_EVIDENCE.md#verification-coverage) | Retained |
| `TRC-010` | [Release coverage](../WORK_AND_EVIDENCE.md#release-coverage) | Retained; pinned preparation constraint explained |
| `TRC-011` | [Release coverage](../WORK_AND_EVIDENCE.md#release-coverage) | Retained |
| `TRC-012` | [Assurance classification](../WORK_AND_EVIDENCE.md#assurance-classification) | Retained |
| `TRC-013` | [Successor coverage](../WORK_AND_EVIDENCE.md#successor-coverage) | Retained |
| `TRC-014` | [Operational coverage](../WORK_AND_EVIDENCE.md#operational-coverage) | Retained |
| `TRC-015` | [Blocking decisions](../RISKS_AND_DECISIONS.md#blocking-decisions) | Retained |
| `TRC-016` | [Raised risks](../RISKS_AND_DECISIONS.md#raised-risks) | Corrected to optional pairing, matching the released evaluator |
| `WFL-001` | [Decision rights](../AUTHORITY.md#decision-rights) | Retained with the Decision rights table |
| `WFL-002` | [HRN-006 — Targeted transitions](../../../../ENGINEERING_HARNESS.md#hrn-006--targeted-transitions) | Retained |
| `WFL-003` | [Continue selected work](../CONTINUE.md#continue-selected-work) | Retained |
| `WFL-004` | [HRN-005 — Explicit decisions](../../../../ENGINEERING_HARNESS.md#hrn-005--explicit-decisions) | Retained |
| `WFL-005` | [If a procedure is blocked](../RESULTS.md#if-a-procedure-is-blocked) | Retained with terminal-state rules |

The old files' unnumbered obligations are covered by Shared policy, the
decision-right rules, the five main processes, and Supporting procedures.
Repository-specific facts and build/test commands remain owner content in
AGENTS. The exception capability has its explicit ownership and implementation
boundary in [EXCEPTIONS.md](../EXCEPTIONS.md#availability).
