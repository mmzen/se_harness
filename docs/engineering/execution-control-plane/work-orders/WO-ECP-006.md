+++
id = "WO-ECP-006"
type = "work_order"
title = "Reduce Phase 4 to its guarantee and introduce the delegation class"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work deletes an execution model reachable from the CLI, keeps its crash-safe apply for every harness-owned multi-file write, and adds a delegation attribute that lets a non-human actor apply three transitions. Every future delegated transition and every journaled write relies on exact candidate behaviour, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/delegated_workflow.py",
  "se_harness/effect_broker.py",
  "se_harness/delegated_authority.py",
  "se_harness/change_bundle.py",
  "se_harness/repository_state.py",
  "se_harness/runtime_state.py",
  "se_harness/agent_contract.py",
  "se_harness/agent_contract.json",
  "se_harness/effect_contract.json",
  "se_harness/skill_contract.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_contract.json",
  "se_harness/cli.py",
  "se_harness/mutation_guard.py",
  "pyproject.toml",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "docs/engineering/agentic-execution/",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-011", "REQ-ECP-017", "REQ-ECP-018"]
specifications = ["SPEC-ECP-006"]
architecture = ["ARCH-ECP-001", "ADR-ECP-002"]
verification = ["VER-ECP-006"]
+++

# Work Order: Reduce Phase 4 to its guarantee and introduce the delegation class

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-011`,
`REQ-ECP-017`, `REQ-ECP-018`, `SPEC-ECP-006`, `ARCH-ECP-001`, `ADR-ECP-002`,
and `VER-ECP-006` are separate acts by their owners and precede approval of
this work order. This work order follows `WO-ECP-003` (the gate it unlocks
behind) and `WO-ECP-005` (the gate evaluator `transition` uses). The
supersessions it records are separate acts by the requirements steward and
the technical owner.

## Objective

Keep what Phase 4 guarantees and remove what it defends against. Today the
envelope's nonce, five-minute lifetime, revocation store, retry ordinal, and
two-capture stability guard a token that never leaves the process that
minted it (`revoked=` has zero callers, `retry_ordinal` is always 0;
complexity audit P1-3, `docs/notes/complexity-audit-2026-08.md:260`); the
broker accepts caller-asserted gates
(`se_harness/delegated_workflow.py:399`); no formal work order carries
`[agentic_delegation]`, so `resolve_delegation` raises `AEXAUTH003` on
every real one (the 2026-08 agentic execution review, section 3). What is
worth keeping is the journaled apply, rollback, and `human-recovery-stop`
with its fault matrix (`se_harness/effect_broker.py:1029-1160`;
`tests/test_effect_broker.py:308-344`; review section 8).

## In scope

- Removal of the envelope apparatus (nonce ledger, lifetime, revocation,
  retry ordinal, stability guard), the v1 envelope constructors, the
  proposed-workspace broker path, `harnessctl delegated-workflow`,
  `se_harness/skill_contract.py`, `se_harness/agent_contract.json`, and
  `se_harness/effect_contract.json`, with `pyproject.toml` package data and
  `se_harness/mutation_guard.py` references updated, per `ECP-DLG-*`.
- The journaled apply retained as the one write path for every
  harness-owned multi-file write (`transition --apply`, `evidence`
  rebinding), with rollback and `human-recovery-stop`, per `ECP-JNL-*`.
- A `[delegation]` class on the work-order template and in
  `se_harness/workflow_contract.json` and its template renderings, letting
  the delegated actor apply `DR-WO-START`, `DR-WO-COMPLETE`, and
  `DR-VREC-PREPARE` only while the candidate's required check is passing,
  read from the CI provider by commit id.
- Amendment records, each a trailing `## Amendment record` section with no
  front-matter change, in the form of
  `docs/engineering/release-orchestration/architecture/ARCH-RLO-004.md:118-128`:
  - `docs/engineering/agentic-execution/architecture/adr/ADR-AEX-006.md`:
    the evaluator-derived ephemeral envelope is superseded by the
    delegation class of `ADR-ECP-002`; the formal maximum delegation on the
    work order is retained as the class.
  - `docs/engineering/agentic-execution/architecture/adr/ADR-AEX-007.md`:
    the isolated-proposal write boundary is superseded by the Git boundary
    of `ADR-ECP-002`; the transactional bundle apply is retained as the
    journaled apply.
  - `docs/engineering/agentic-execution/architecture/ARCH-AEX-002.md`: the
    single-agent effect broker is withdrawn as an architecture; the
    journaled apply and `human-recovery-stop` conformance checks are
    retained and re-homed under `ARCH-ECP-001`.
  - `docs/engineering/agentic-execution/README.md`: the domain index notes
    the three amendments.
- Formal supersession, by the requirements steward through
  `harnessctl transition ... =superseded` under the released evaluator,
  of each artifact in `docs/engineering/agentic-execution/` for which a
  superseding ECP artifact exists once that artifact is active; `--reason`
  names the successor. Artifacts with no successor receive the amendment
  record only.
- Tests, including the fault matrix on both platforms; work-order-keyed
  evidence.

## Out of scope

- Approving any ECP artifact; the gate itself (`WO-ECP-003`); the gate
  evaluator (`WO-ECP-005`); authenticated records (`WO-ECP-004`); retiring
  the shipped skills (`WO-ECP-008`); root managed copies; editing any
  front matter of an amended artifact; any change to lifecycle states,
  gate predicates, or decision rights beyond the delegation class's use of
  the three named rights.

## Authorized decision envelope

The implementation agent may decide the internal shape of the retained
journal, the CI provider reader's module placement, diagnostic code
numbers, the amendment prose, and test names. It may not keep any
envelope symbol reachable from the public API or CLI, accept a gate state
from a request body, add a fourth right to the class, apply any
supersession itself, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, preflight, and every
  supersession transition.
- Root managed copies are not edited; the template `WORKFLOW.json`,
  `WORKFLOW.md`, and `WORK_ORDER.template.md` are.
- LF line endings; assert bytes against blobs.
- Stage every deletion (the removed modules and JSON mirrors) before any
  preflight or check run; `hash_bound.assess` reads index-tracked paths.
- The Windows fault case (a target held open mid-bundle) is run on
  Windows, not skipped.

## Expected change surface

Nine Phase 4 modules and mirrors (several deleted), the workflow contract
loader and JSON with two template renderings, the work-order template, the
CLI, the mutation guard, `pyproject.toml`, four amended artifacts under
`docs/engineering/agentic-execution/`, tests, evidence.

## Required verification

Execute `VER-ECP-006` completely plus the repository-required checks; run
the complete suite on Linux and Windows with figures labelled per platform.
The Scenario 1 demonstration is run only after a work order carrying the
class has been approved by its owner.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-006/`:
the fault matrix per platform, journal files from stopped retries, the
wheel symbol inventory and `--help` walk, the demonstration pull request
and check-run identifiers, the supersession transition results, the
amendment diffs, per-platform test figures, and the complete changed-path
set.

## Stop and escalate conditions

Stop if the journaled apply cannot be separated from the broker without
losing a fault-matrix case, if the CI provider offers no check-run reading
by commit id, if the released evaluator refuses a supersession transition
or the edited workflow contract, if an amended artifact's front matter
would have to change, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-006 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
