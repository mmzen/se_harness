+++
id = "WO-IAR-027"
type = "work_order"
title = "Align owner glossary with the adopted instruction policy"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification when approving WO-IAR-027 and VER-IAR-019. Later decisions rely on the corrected explanations of authority, lifecycle, exceptions and evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  "GLOSSARY.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-027.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-019.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-017.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-017-evaluator.json",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-027/"
]

[relations]
implements = ["REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T07:14:21Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve both. Confirmed eleven glossary entries and Upkeep, required commit-bound verification, and VER-IAR-019. Reviewed WO SHA-256 bea21c2aedc2fa5e937920db27f6a5356de65ddf63f994e267a25a56413473eb. Only the confirmed assurance fields were added before preview. Scope clarification: Correct all identified stale glossary entries."
scope_paths = ["GLOSSARY.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-027.md", "docs/engineering/instruction-architecture/verification/VER-IAR-019.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-017.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-017-evaluator.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-027/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T07:15:06Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the exact approved glossary replacements under mmzen approval; required commit-bound verification remains mandatory."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-30T07:18:07Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the exact approved eleven glossary entries and Upkeep under mmzen approval. Seventeen focused tests and fourteen links pass; unselected glossary bytes and all term names preserved. Released doctor, validation, review preflight and complete Git-derived handoff pass. Required commit-bound verification and separate human acceptance remain pending."
+++

# Align owner glossary with the adopted instruction policy

## Objective

Readers of this repository's glossary get the adopted Human/Agent authority
model, correct result and lifecycle meanings, and working current guide links.
This is explanatory owner-prose maintenance under the unchanged meanings of
REQ-IAR-027 and SPEC-IAR-014, not a new harness rule.

## Confirmed scope

The user approved the glossary follow-up after PR #504 and then selected
"Correct all identified stale glossary entries". This confirms the proposed
scope below; formal work approval and assurance classification remain pending.

Update only the eleven entries and Upkeep paragraph listed below. Keep their
term names, all other paragraphs, and the project-only glossary ownership.
The selected release has no configurable documentation exception; the existing
claim to change the glossary "never by a work order" is not applicable authority.

## Reviewed inputs

Base: 7bf6850bca0526791756cf9dbfb07b201b87aeda (merged PR #504).
Selected evaluator: released 0.20.0, wheel SHA-256
7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0.
The current glossary raw-byte SHA-256 is 25b711d3f7cd64aab058727595f62217e177d009f17a371dd03b007bcda50c8b.
The proposed full glossary, normalized to LF for review, has SHA-256
4eb639dffb6308db4633c9f5046194041d27aca7e9ada7d49f4bd340c9c6f410. Apply the exact reviewed replacements while preserving the
remaining file bytes; do not normalize unrelated content or edit other entries.

## Selected replacement wording

### Verification record (VREC)

**Verification record (VREC).** A file that binds evidence and one or more work orders to one exact commit. A human decides whether to accept it as `verified`; later permitted lifecycle transitions preserve its candidate and evidence history (see [verification decisions](docs/engineering/harness/VERIFY_OUTCOME.md#record-the-verification-decision)).

### Release record (RLS)

**Release record (RLS).** A file that binds a release contract, eligible verification records and one exact candidate commit. Preparation creates a `ready` record; an authorized human makes the separate release decision (see [release decisions](docs/engineering/harness/RELEASE.md#obtain-the-release-decision-when-required)).

### Decision right

**Decision right.** The rule that identifies who may authorize a specific action. The evaluator reports the required right and checks the action; a command may apply an authorized decision, but running it does not supply that decision (see [decision rights](docs/engineering/harness/AUTHORITY.md#decision-rights)).

### Owner file

**Owner file.** Repository content the owner controls, such as product code and local instructions. The harness may seed some owner files at installation, but later replacement requires explicit owner authority; owner content is not hash-locked as managed policy (see [upgrades](docs/engineering/harness/UPGRADE.md#upgrade-the-installed-harness)).

### Projection

**Projection.** A `check` result obtained without a checkpoint. It reports lifecycle context and the next step; it does not evaluate checkpoint gates or authorize work (see [continuation](docs/engineering/harness/CONTINUE.md#continue-selected-work)).

### Restitution

**Restitution.** The operator-facing summary in a workflow result: what completed, what is blocked, the decision due and one next step. Agents report that result without inventing effects or authority (see [reporting results](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result)).

### result_sha256

**result_sha256.** The digest that binds the declared machine fields of a workflow result; in the current format, explanatory wording is excluded. A generated `Harness-Restitution` field refers to one work-order result and does not replace checking the current PR body and complete diff (see [result digests](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result) and [PR checks](docs/engineering/harness/PULL_REQUEST.md#check-a-governed-pull-request)).

### Delegation class

**Delegation class.** A historical work-order table that granted specified execution steps under the rules of its release. Current work-order approval grants bounded execution through [authority from work approval](docs/engineering/harness/AUTHORITY.md#authority-from-work-approval); older approvals keep their recorded limits, and human-reserved decisions remain with humans.

### Digest

**Digest.** A SHA-256 value computed from the bytes or canonical fields specified by its contract. Examples include managed-file hashes, formal-snapshot and evaluator-evidence hashes, and the workflow result's `result_sha256`; each uses its own declared input and format (`SPEC-REV-001`, [current result format](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result)).

### Accountable role

**Accountable role.** A legacy label for a decision responsibility, such as assurance owner or release owner. Current [decision rights](docs/engineering/harness/AUTHORITY.md#decision-rights) distinguish humans and agents and record the actual decision-maker and authority; a profile or role label alone grants no permission.

### Predicate

**Predicate.** One exact condition assessed by a gate, such as `QGP-G4I-PATHS`. At the selected checkpoint, every required predicate assessed there must pass before that gate permits the action (see [gates](docs/engineering/harness/RESULTS.md#gates)).

### Upkeep

Follow the repository's selected harness procedure when changing this page,
then use a reviewed pull request. SE Harness 0.20.0 has no owner-configured
documentation exception; [EXCEPTIONS.md](docs/engineering/harness/EXCEPTIONS.md#availability)
therefore directs this work through the normal definition and work-order process.

`harnessctl inspect` reports frequent project terms without an entry and entries
whose term appears in no artifact. Use that report and reviewers' questions to
propose glossary updates; the report grants no change authority.


## Out of scope

No managed instruction, machine contract, accepted definition, template, source
code, test module, plugin, host setting, credential, version or historical record
changes. No new exception or delegation capability. No removal or recreation of
the retired pointers. No push, PR, merge, release or publication authority.

## Authorized decision envelope

After approval, Codex may start this work, apply the reviewed owner-prose changes,
run required checks, retain evidence, create local commits, record completion
and prepare VREC-IAR-017 through the released evaluator. Human verification
acceptance and external delivery remain separate. This draft grants none of
those rights before approval.

## Proposed assurance classification

Propose `required`: readers may rely on this explanation of authority, lifecycle,
exceptions and evidence when taking later actions. This is not solely recording
or transporting an already made decision. The human must confirm this with work
approval; only then record the classification and actual decision-maker under
`[assurance]`. No actor identity is invented to satisfy an approval gate.

## Required verification and evidence

Execute VER-IAR-019: source-to-wording review, new link/anchor checks, preservation
of unrelated paragraphs and term names, existing focused glossary/documentation
tests, released identity/doctor/validation, and complete scope/handoff checks.
Retain actual outputs and review under evidence/WO-IAR-027/. Use one clean
committed candidate for VREC-IAR-017 and its generated evaluator companion.
Before capture, confirm the proposed record ID is still unused across local refs.

The one-file prose correction needs no new architecture: no active architecture
directly addresses REQ-IAR-027. Existing INT-IAR-001, CAP-IAR-002, REQ-IAR-027 and
SPEC-IAR-014 are reused unchanged. A new focused verification contract avoids
repeating the original full instruction-delivery migration qualification.

## Stop conditions

Stop for changed reviewed input bytes, an unresolved source contradiction,
missing authority, failed checks or writes beyond the selected scope. Retain
the failure and request a bounded correction if needed. Do not rewrite accepted
policy or invent another exception to make the prose or a check pass.

## Completion report

Report the selected paragraphs changed, preserved content, actual checks,
candidate and evidence paths, any unresolved findings, and the evaluator's next
step. Preparing a verification record does not accept it or deliver the branch.
