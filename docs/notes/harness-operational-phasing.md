# SE Harness operational phasing

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This note explains timing. It does not replace `docs/engineering/WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, or `TRACEABILITY.md`.

## Lifecycle at a glance

```mermaid
flowchart LR
    P1["1. Frame purpose"] --> H1{"Human product approval"}
    H1 --> P2["2. Define behavior, architecture applicability, and verification"]
    P2 --> H2{"Technical and assurance approval"}
    H2 --> P3["3. Approve bounded work order"]
    P3 --> P4["4. Preflight, implement, check, retain evidence, review"]
    P4 --> C["5. Clean candidate commit C"]
    C --> P6["6. Prepare ready VREC in later governance commit"]
    P6 --> H3{"Human assurance decision"}
    H3 --> P7["7. Prepare ready RLS in later governance commit"]
    P7 --> H4{"Human release decision"}
    H4 --> P8["8. Authorized tag or publication at C; operating assurance"]
```

Automation assists between decision points. Blueprints, test results, a clean Git state, validation, and CI are evidence or controls; none substitutes for the human diamonds.

## Phase-by-phase guide

| Phase | What exists or happens | Typical authority boundary |
| --- | --- | --- |
| 1. Purpose | Draft intent, capability, and observable requirements explain why the change exists. | Product or domain owners approve purpose and obligations. |
| 2. Engineering definition | Specifications define behavior. Architecture addresses only significant requirement drivers and conforms to specifications. Its decision assessment either requires deciding ADRs or records why no significant decision exists. Verification contracts define checks. | Technical owners approve specification and architecture decisions; assurance owners approve verification contracts. |
| 3. Work authorization | A work order selects requirements, specifications, applicable architecture/ADRs, and verification contracts; it defines scope, exclusions, delegated decisions, and stop conditions. | An engineering owner approves the bounded work. Approval is permission to start, not proof of completion. |
| 4. Execution and review | The coding agent runs start preflight, reads its manifest, sets the work order `in_progress`, implements within scope, runs repository checks, retains evidence, validates the graph, generates Explorer, and performs review preflight. | The agent may act only inside approved scope. Reviewers judge semantic fit and evidence quality. |
| 5. Candidate | One clean candidate commit **C** contains implementation, retained evidence, and the honest `implemented` work-order state. | C is the revision later assurance and release records must name. |
| 6. Verification | From clean C, automation may prepare a `ready` VREC. It is retained in a later governance commit. An assurance owner reviews its evidence and may transition it to `verified` in another governance commit. | `ready` is a proposal; `verified` is a human assurance decision about C. |
| 7. Release decision | After eligible verification and release-contract checks, automation may prepare a `ready` RLS, again in a later governance commit. The release owner may transition it to `released`. | The RLS and all included VRECs bind the same C. `released` records authorization; it does not prove that an external action succeeded. |
| 8. Promotion and operation | Authorized automation or humans may tag C, create a GitHub Release, publish the already verified distribution, or deploy it. Operational evidence is evaluated against operating contracts. | Tags, publication, deployment, hosting controls, and service operation are external actions governed by repository policy and accountable owners. |

## Why the records come later

A Git commit cannot contain its own hash. Therefore the record that names candidate C cannot be part of C:

```text
C    implementation + evidence + implemented work-order state
G1   ready VREC -------------------------------> C
G2   VREC transitioned to verified -----------> C
G3   ready RLS --------------------------------> C
G4   RLS transitioned to released ------------> C
T    authorized immutable tag ----------------> C
```

G1 through G4 are governance history. They do not become a new release candidate merely because they occur later. If implementation or evidence changes after C, select a new candidate C2 and capture replacement provenance rather than editing the old claim to point somewhere convenient.

## Commands by phase

The coding agent normally operates these commands; the accountable human makes the adjacent decision.

| When | Agent-operated command | What it does not do |
| --- | --- | --- |
| Before editing | `harnessctl doctor .` and `harnessctl preflight . --work-order WO-EX-001 --phase start` | Does not authorize the work order or prove comprehension. |
| During and before review | repository-specific checks, `harnessctl validate .`, `harnessctl dashboard .`, and `harnessctl preflight . --work-order WO-EX-001 --phase review` | Does not judge semantic correctness or approve the pull request. |
| At clean candidate C | `harnessctl capture-verification ...` | Prepares only a `ready` VREC; does not verify, commit, or push. |
| After human verification and release authorization | `harnessctl prepare-release ...` | Prepares only a `ready` RLS; does not release, tag, publish, or deploy. |

## Formal gates versus Explorer readiness

The authoritative gates in `docs/engineering/QUALITY_GATES.md` are G0 Intent, G1 Definition, G2 Architecture, G3 Work authorization, G4 Verification, and G5 Release and operation.

In version 0.2.2, Harness Explorer reuses G0-G5 labels for a differently grouped, derived per-work-order readiness view. Use Explorer to navigate traceability and anomalies, but use the managed policy for gate meaning. This documentation reports the mismatch; correcting the generator requires separate authorized behavior work.

For one possible mapping onto Git branches and pull requests, continue to the [illustrative branching model](harness-branching-model.md).
