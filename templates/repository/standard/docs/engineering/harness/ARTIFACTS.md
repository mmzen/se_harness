# Artifact data model

A formal artifact is a record with a stable ID, a type, a lifecycle state,
content, and links to other artifacts. These records explain why a change is
needed, what it must do, who may carry it out, and how its result is checked.

Artifacts use TOML metadata between `+++` markers. Links are recorded in the
`[relations]` table using artifact IDs. A filename, a shared directory, or a
mention in prose does not create a formal link.

The tables below describe artifact types and permitted links. They are not a
manually maintained list of the repository's actual artifacts. `harnessctl`
reads those artifacts and checks their links and lifecycle states.

## Artifact types

“Required” means the selected work needs coverage of that type. It does not
mean every change must create a new file. Reuse an existing active artifact
when its accepted meaning and scope still cover the work. Create a conditional
artifact only when its condition applies.

For an existing selected work order (WO), get its current state and next
action with:

```text
harnessctl check REPO --artifact WO-ID --json
```

Before implementation, check whether that work order (WO) and its linked
definitions are eligible to start:

```text
harnessctl preflight REPO --work-order WO-ID --phase start --json
```

The first command reports lifecycle context without evaluating checkpoint
gates. The second evaluates start readiness, including the states and coverage
of the selected definitions. Neither command approves or starts work.
Here, `REPO` is the absolute repository path and `WO-ID` is the actual ID of
the selected work order (WO). Use the repository's selected released evaluator.

| Type                  | ID prefix | Purpose                                                                                                                                                                      | When needed                                                                                                                                              |
|-----------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `intent`              | `INT-`    | States the problem, intended outcome, and limits of responsibility.                                                                                                          | The work needs an accepted purpose. Reuse an intent (INT) when that purpose still applies.                                                               |
| `capability`          | `CAP-`    | Describes an ability that a human or agent should have.                                                                                                                      | Requirements (REQ) need a link to the capability (CAP) they support.                                                                                     |
| `requirement`         | `REQ-`    | States required behavior or a constraint, with a condition for acceptance.                                                                                                   | The change creates or changes an obligation. Reuse a requirement (REQ) only if its meaning stays unchanged.                                              |
| `specification`       | `SPEC-`   | Defines the detailed behavior, interfaces, constraints, and rejection conditions.                                                                                            | Each requirement (REQ) selected for implementation needs specification (SPEC) coverage.                                                                  |
| `architecture`        | `ARCH-`   | Defines system structure and boundaries needed to meet significant requirements (REQ).                                                                                       | An active architecture (ARCH) directly addresses a requirement (REQ) selected by the work order (WO).                                                    |
| `adr`                 | `ADR-`    | Records an architecture decision (ADR), the alternatives, and their consequences.                                                                                            | An applicable architecture (ARCH) declares that a significant decision is required.                                                                      |
| `verification`        | `VER-`    | Defines how requirements (REQ) will be checked and what counts as a pass.                                                                                                    | Each selected requirement (REQ) needs verification coverage. This is the verification contract (VER), not a test result.                                 |
| `work_order`          | `WO-`     | Defines the bounded work to execute and its governing artifacts. Approval grants work authority.                                                                             | Before execution. One work order (WO) may cover several requirements (REQ). Completed scope does not authorize later work.                               |
| `verification_record` | `VREC-`   | Binds work orders (WO), verification contracts (VER), evidence, and one exact candidate commit for assessment.                                                               | When verification tied to a commit is required. One record may cover several work orders (WO) at the same commit.                                        |
| `release_contract`    | `REL-`    | Defines permitted release scope, gates, rollback conditions, and authority limits.                                                                                           | When a release record (RLS) is proposed.                                                                                                                 |
| `release_record`      | `RLS-`    | Records preparation and the later release decision for verified work at one exact commit.                                                                                    | When a formal release is proposed. Preparing the record does not release the work.                                                                       |
| `decision`            | `DEC-`    | Records a question, options, recommendation, decision maker, affected artifacts, and the eventual answer. It can also record a deviation from one specification (SPEC) rule. | A question blocks a transition, affects more than one artifact, or must remain recorded after approval; or work cannot meet a specification (SPEC) rule. |
| `risk`                | `RISK-`   | Records a threat, an owner, and a next action. Scoring and categories are optional.                                                                                          | A concern needs follow-up. A separate decision (DEC) is used when the concern must block work.                                                           |
| `operating_contract`  | `OPS-`    | Defines continuing service, support, monitoring, or operational assurance obligations.                                                                                       | Ongoing operational commitments apply. Omitting the record does not prove those commitments have been met.                                               |

Code, tests, acceptance scenarios, evidence files, commits, dashboards, tickets,
and conversations are not additional formal artifact types. They may support
or be referenced by formal artifacts but do not grant authority by themselves.

## Artifact locations

New formal artifacts use these directories below
`docs/engineering/DOMAIN/`. `DOMAIN` is the selected domain name. These paths
describe storage, not authority; the artifact ID, metadata, and typed links
remain authoritative. Use the supported authoring command to obtain the actual
path. Do not move existing records merely to match this table.

| Artifact | TYPE | Directory |
| --- | --- | --- |
| Intent (INT) | `intent` | `intent/` |
| Capability (CAP) | `capability` | `capabilities/` |
| Requirement (REQ) | `requirement` | `requirements/` |
| Specification (SPEC) | `specification` | `specifications/` |
| Architecture (ARCH) | `architecture` | `architecture/` |
| Architecture decision (ADR) | `adr` | `architecture/adr/` |
| Verification contract (VER) | `verification` | `verification/` |
| Work order (WO) | `work_order` | `work-orders/` |
| Verification record (VREC) | `verification_record` | `verification-records/` |
| Release contract (REL) | `release_contract` | `release/` |
| Release record (RLS) | `release_record` | `releases/` |
| Operating contract (OPS) | `operating_contract` | `operations/` |
| Decision (DEC) | `decision` | `decisions/` |
| Risk (RISK) | `risk` | `risks/` |

The same domain has `evidence/` for retained work-order evidence and
`acceptance/` for acceptance scenarios. These are supporting files, not new
formal artifact types. Legacy flat artifact locations remain readable and
MUST NOT be moved by an upgrade without separate authority.

Templates under `docs/engineering/templates/` are authoring assets. They are
excluded from active-artifact validation and grant no authority. Use
`capture-verification` and `prepare-release` for commit-bound VREC and RLS
instances; an edited template is not a substitute for their derived evidence.
