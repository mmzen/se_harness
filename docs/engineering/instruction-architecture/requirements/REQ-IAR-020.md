+++
id = "REQ-IAR-020"
type = "requirement"
title = "Carry local operational facts in the owner instruction region"
status = "superseded"
owners = ["repository-owner", "requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-25"
statement = "WHEN a coding agent loads the always-available instruction surface of this repository, the se_harness repository SHALL state, in the owner-controlled region of AGENTS.md, the operational entry point for commands, the authoritative managed-path boundary together with its candidate-source counterpart, and the known pull-request and evaluator failure conditions, and SHALL NOT restate an obligation that a governed requirement already owns."
verification_method = "Automated managed-integrity, lock-derived path-set, and content-presence tests plus accountable review of the drift and authority boundary"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Carry local operational facts in the owner instruction region

## Supersession

Superseded on 2026-08-25 by `REQ-ADS-007` under `WO-ADS-002`, authorized by the
requirements steward with the approval of `REQ-ADS-007`. The successor keeps
every obligation of this requirement except the pointer clause of rules 3-4:
the owner region no longer names the retired repository-context document,
which the harness withdrew under `WO-DST-021`, and instead names the
repository-owned note section that carries the release sequences. The
rationale, required response, and boundary behavior below record what the
region carried while this requirement was active and are retained unchanged
as history. They are no longer obligations.

## Lifecycle

Drafted on 2026-08-21 after analysis of the installed `AGENTS.md` identified that the always-loaded instruction surface carries no operational entry point and no managed-path boundary, while restating obligations that governed requirements already own. This draft approves nothing and authorizes no implementation.

## Rationale

`INT-IAR-001` records that harness ownership is difficult to infer, that some files must be safely customized while others remain managed and integrity-protected, and that the result is avoidable reading and ambiguous precedence. `CAP-IAR-001` establishes that installation preserves local agent guidance. Neither obliges this repository to put anything useful in the region it preserves.

The current owner region demonstrates the gap. It carries ten constraints and no commands, so an agent asked to run tests or make a small change has no operational entry point and no pointer to `docs/engineering/REPOSITORY_CONTEXT.md`, which holds them. The managed gate cannot supply that pointer: `REQ-IAR-001` restricts the managed fragment to exactly one harness destination, and `tests/test_instruction_architecture.py` asserts the fragment does not name `REPOSITORY_CONTEXT.md`. The owner region is therefore the only place the bridge can exist.

The same region is silent about the highest-consequence local hazard. Twenty-eight files are hash-locked managed copies, including eight under `scripts/` that also exist as candidate source under `templates/repository/standard/scripts/`. Editing a root copy breaks `doctor` and the required CI check; editing only the template leaves local tooling unchanged. The two trees already differ, so the hazard is active rather than theoretical.

Three product invariants in the region — one standard installation, Python 3.11+ standard-library runtime behavior, and untrusted input handling — already exist as governed requirements. Restating them creates an unversioned copy that no validator checks and no owner owns, so a revised requirement leaves stale de-facto policy behind. That is the coupling the harness exists to prevent.

## Preconditions and trigger

- A coding agent loads `AGENTS.md`, directly or through the `CLAUDE.md` import, before selecting a task; and
- the task may be operational, corrective, or exploratory rather than a full governed lifecycle stage.

The trigger is not limited to work that reaches a lifecycle handoff. An agent that never opens `ENGINEERING_HARNESS.md` still relies on this region.

## Required response

The owner-controlled region must state:

1. the operational entry point, carrying the setup, test, graph-validation, additional-required-verification, lint-or-format, and entry-point facts inline, and naming `docs/engineering/REPOSITORY_CONTEXT.md` as the repository-owned file holding the build, release-binding, and publication sequences it does not duplicate, described by its content rather than by any harness status;
2. the repository test command, and that no formatter or linter gate exists;
3. that product invariants are governed requirements rather than content of this file, with a pointer to the domain index;
4. the managed-path boundary, distinguishing hash-locked managed paths from owner-editable paths in the same directory, and naming `.engineering-harness.lock` as authoritative;
5. the candidate-source location for the managed scripts, and that root copies belong to the released version and intentionally lag;
6. the standalone `Harness-Work-Order` pull-request field and its stored-event-payload timing; and
7. the released-evaluator isolation condition and its observable failure.

Retained agent-facing constraints that no governed requirement expresses as an instruction — deterministic boundary and failure tests, release-build authorization, untrusted input handling, and preservation of unrelated changes and historical records — remain in the region.

## Failure and boundary behavior

- The managed block between `<!-- se-harness:begin -->` and `<!-- se-harness:end -->` is byte-exact under `utf8-text-lf-v1` canonicalization. Reflowing, splitting, or adding whitespace inside it changes the fragment digest and fails `doctor`, preflight `I001`, and the required CI check.
- A managed-path list that omits a managed file, or names an owner-editable file as managed, is a defect. Naming all of `scripts/` as managed is incorrect and would block the documented release-build path.
- The region may add stricter constraints but cannot waive formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions.
- The region records no product intent, approves nothing, and remains non-authoritative relative to `docs/engineering/`.
- Growth is bounded. The region states local facts and pointers; it does not become a second copy of managed policy.
- The region shall not assert a harness property of any file it points to. In particular it shall not state that `docs/engineering/REPOSITORY_CONTEXT.md` is preflight-required or harness-seeded. Both properties hold today and both are withdrawn by `REQ-DST-065`; a content-based pointer is correct under either state, so this obligation is independent of the order in which the two changes land.

## Constraints

- Change only the owner-controlled region of `AGENTS.md`. Do not modify the managed fragment, `CLAUDE.md`, `ENGINEERING_HARNESS.md`, or any managed policy module.
- Preserve the single managed harness destination and the existing router-to-focused-policy split.
- Do not add a formatter or linter gate, a CLI command, or machine-readable output.
- Do not change portable SE Harness behavior or the packaged `AGENTS.md.fragment`; this obligation is repository-local.

## Acceptance examples

### Example: operational task without a lifecycle stage

**Given** an agent has loaded only `CLAUDE.md` and `AGENTS.md`

**When** it is asked to run the repository test suite

**Then** the owner region names the test command and `docs/engineering/REPOSITORY_CONTEXT.md`, and the agent needs no further reading to proceed correctly.

### Example: managed-path hazard

**Given** an agent is asked to change validator behavior

**When** it consults the owner region

**Then** the region identifies `scripts/validate_engineering_artifacts.py` as a hash-locked managed copy and `templates/repository/standard/scripts/` as its candidate source, so the agent edits the template rather than the root.

### Example: failure behavior

**Given** a proposed revision reflows the paragraph inside the managed markers

**When** managed integrity is evaluated

**Then** the fragment digest no longer equals the value recorded in `.engineering-harness.lock`, and the change is rejected before it reaches a candidate commit.

## Open decisions

Two questions remain for accountable resolution before approval. First, whether reusing `INT-IAR-001` and `CAP-IAR-001` correctly covers a repository-local instruction obligation, or whether a distinct intent and capability are required. Second, whether the managed block should be relocated above the owner sections; relocation is preserved across upgrades because the installer replaces the block in place, but it is not required by this requirement.
