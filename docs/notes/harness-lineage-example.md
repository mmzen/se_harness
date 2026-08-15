# Practical SE Harness examples

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Every `EX` identifier, title, path, version, and commit in this note is fictional. The examples demonstrate current behavior; they are not repository state and grant no authority.

## Example 1: add per-customer API rate limiting

### The user request

The repository owner asks a coding agent:

> Add per-customer API rate limiting. Preserve existing clients, return `429` with `Retry-After`, and prepare the engineering material for review before implementation.

That request is useful input, but a conversation is not formal authority. The agent drafts a chain under a repository domain such as `docs/engineering/api-governance/`:

```text
intent/INT-EX-001.md
capabilities/CAP-EX-001.md
requirements/REQ-EX-001.md        per-customer limit
requirements/REQ-EX-002.md        429 and Retry-After behavior
specifications/SPEC-EX-001.md      counter key, window, response contract
architecture/ARCH-EX-001.md        rate-limit boundary and data ownership
architecture/adr/ADR-EX-001.md     selected store and failure behavior
verification/VER-EX-001.md         deterministic and concurrency checks
work-orders/WO-EX-001.md           bounded implementation authorization
release/REL-EX-001.md              reusable release conditions
```

The declared relations point in the current metadata direction:

```text
CAP-EX-001.derives_from       -> INT-EX-001
REQ-EX-001..002.derives_from  -> CAP-EX-001
SPEC-EX-001.specifies         -> REQ-EX-001..002
ARCH-EX-001.addresses         -> significant REQ-EX-001..002 drivers
ARCH-EX-001.conforms_to       -> SPEC-EX-001
ADR-EX-001.decides            -> ARCH-EX-001
VER-EX-001.verifies           -> REQ-EX-001..002
WO-EX-001.implements          -> REQ-EX-001..002
WO-EX-001.specifications      -> SPEC-EX-001
WO-EX-001.architecture        -> ARCH-EX-001, ADR-EX-001
WO-EX-001.verification        -> VER-EX-001
REL-EX-001.gates              -> WO-EX-001
```

Architecture exists here because shared counter ownership, trust boundaries, and failure behavior materially shape the system. Its decision assessment is `adr_required`, so the selected work order includes the deciding ADR. A routine wording-only requirement might have no active architecture `addresses` edge; the agent must not invent a ceremonial ADR for it.

### Human approvals before code

The product owner approves the intent, capability, and requirements. Technical and assurance owners approve the specification, architecture assessment and ADR, and verification contract. The engineering owner reviews the work order's scope and exclusions.

Only after the user says, for example, “I approve `WO-EX-001`; implement it,” does the work order become implementation authority. An agent must not interpret its own drafts as approval.

### Agent execution

The coding agent normally runs:

```powershell
harnessctl doctor .
harnessctl preflight . --work-order WO-EX-001 --phase start
```

It reads the returned manifest, transitions the approved work order to `in_progress`, and implements only its scope. It then runs the commands owned by this repository, followed by harness observations:

```powershell
# Repository-specific examples; use the actual commands in REPOSITORY_CONTEXT.md
python -m unittest discover -s tests -p "test_*.py"

harnessctl validate .
harnessctl inspect .
harnessctl dashboard .
harnessctl preflight . --work-order WO-EX-001 --phase review
```

`validate` supplies gate-oriented graph results. `inspect` then groups current lifecycle attention, retained findings, and bounded suggestions for possible accountable next steps; it executes nothing and does not establish eligibility or approval. The dashboard provides the visual view of the same repository evidence.

The agent retains an evidence report at:

```text
docs/engineering/api-governance/evidence/WO-EX-001-verification.md
```

Before selecting a candidate, the same change contains the honest work-order transition to `implemented`. Reviewers confirm semantic scope, tests, evidence, and visible anomalies. The implementation, evidence, and lifecycle state are committed together or integrated into one clean candidate commit **C**.

### Commit-bound verification

With `HEAD` at clean candidate C, the agent prepares a record:

```powershell
harnessctl capture-verification . `
  --id VREC-EX-001 `
  --work-order WO-EX-001 `
  --verification VER-EX-001 `
  --evidence docs/engineering/api-governance/evidence/WO-EX-001-verification.md
```

The command derives the full Git hash, requires a clean worktree, checks selected coverage and evidence, captures the artifact snapshot hash, and writes only a `ready` VREC. The generated metadata contains:

```text
VREC-EX-001.verifies_work_order -> WO-EX-001
VREC-EX-001.conforms_to         -> VER-EX-001
VREC-EX-001.commit              -> C
```

The ready record is committed later because it cannot contain the hash of its own commit. The assurance owner reads `VER-EX-001` and the retained evidence and may transition the VREC to `verified` in another governance commit. The command did not make that decision.

### Separate release decision

After the verified record is retained and the release owner authorizes preparation, the agent runs:

```powershell
harnessctl prepare-release . `
  --id RLS-EX-001 `
  --release-contract REL-EX-001 `
  --verification-record VREC-EX-001 `
  --work-order WO-EX-001 `
  --version 1.4.0 `
  --authorized-by release-owner `
  --tag v1.4.0
```

This prepares only a `ready` RLS whose current relations are:

```text
RLS-EX-001.satisfies             -> REL-EX-001
RLS-EX-001.includes_verification -> VREC-EX-001
RLS-EX-001.releases_work         -> WO-EX-001
RLS-EX-001.commit                -> C
```

The release owner may later transition the record to `released`. If authorized, a human or repository automation creates `v1.4.0` at **C**, not at the later governance commit. GitHub Release creation, package publication, and deployment remain separate external actions; the harness command performs none of them.

### Timeline and authority

```text
approved INT/CAP/REQ/SPEC/ARCH/ADR/VER/WO
              |
              v
C   implementation + evidence + WO implemented
              ^
              | binds exact commit
G1  ready VREC proposal
G2  human assurance: VREC verified
              ^
              | same exact commit
G3  ready RLS proposal
G4  human release decision: RLS released
T   authorized tag v1.4.0 ----------------------> C
```

The value is the complete, inspectable answer: why the change exists, what was in scope, how it was tested, which exact integrated revision was assessed, and which accountable people made the assurance and release decisions.

## Example 2: one release contains multiple work orders

Suppose the final candidate also contains an independently approved documentation work order `WO-EX-002`, with `VER-EX-002` and its own retained evidence. A release is not forced to correspond to one governance topic. One aggregate VREC can cover the complete candidate payload:

```powershell
harnessctl capture-verification . `
  --id VREC-EX-002 `
  --work-order WO-EX-001 `
  --work-order WO-EX-002 `
  --verification VER-EX-001 `
  --verification VER-EX-002 `
  --evidence docs/engineering/api-governance/evidence/WO-EX-001-verification.md `
  --evidence docs/engineering/documentation/evidence/WO-EX-002-verification.md
```

The selected verification contracts must equal the union declared by both work orders, and evidence must exist for each. After human verification, one RLS can include that VREC and repeat both `--work-order` options. Its `releases_work` set must exactly equal the VREC coverage union, and every record still binds the same final candidate C.

A governance-only work order that merely authorizes VREC/RLS transitions is not automatically part of this release payload. It normally stops at `implemented`, preventing an infinite requirement to verify the act of recording verification.

## Common mistakes exposed by the examples

| Mistake | Correct interpretation |
| --- | --- |
| Starting implementation from agent-authored drafts | Accountable humans approve the governing chain and bounded work order first. |
| Creating an ADR for every requirement | Assess architecture triggers; record ADRs only for significant decisions. |
| Capturing before the work order and evidence are in C | Candidate C must already contain implementation, evidence, and honest lifecycle state. |
| Treating green CI or Explorer as verification | These are observations; only the assurance owner decides `verified`. |
| Binding the RLS to a later governance commit | The RLS binds the same C as all included VRECs. |
| Tagging the current branch tip automatically | The authorized immutable tag targets C. |
| Assuming `prepare-release` publishes | It writes a ready record only; publication is separate. |

For entity relationships, see the [simplified UML model](harness-uml-model.md). For lifecycle timing and one optional Git mapping, see [operational phasing](harness-operational-phasing.md) and the [illustrative branching model](harness-branching-model.md).
