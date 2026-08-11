# SE Harness

SE Harness turns a repository into a governed software-engineering workspace for humans and coding agents. It installs one complete, repository-native system for intent, requirements, architecture, authorized work, verification evidence, commit provenance, release decisions, validation, and visualization.

The objective is practical: make every material change explainable from intent to evidence and an exact Git commit, while keeping approval and release authority with accountable humans.

SE Harness is specification-driven, uses Python 3.11 or later, and gives each installed repository local validation and dashboard scripts that do not require an external service.

## What it provides

Every installation receives the same standard harness:

- formal Markdown artifacts for intent, capabilities, requirements, specifications, architecture, decisions, verification, work orders, releases, and operations;
- one shared repository-local agent contract, loaded by Codex through `AGENTS.md` and by Claude Code through a thin `CLAUDE.md` import;
- a repository-owned context file for confirmed purpose, commands, architecture, and constraints;
- a deterministic validator for artifact structure, coverage, relations, evidence paths, and commit provenance;
- Harness Explorer, a self-contained dashboard for traceability, readiness, findings, and anomalies;
- commit-bound verification and release records;
- retained evidence conventions and reusable artifact templates;
- safe adoption and hash-based upgrades that preserve repository customizations;
- a GitHub Actions workflow using the same repository-local checks.

There is exactly one standard installation. Minimal, offline, and selectable installation profiles are deliberately unsupported.

## Install the CLI

From a checkout of this repository:

```powershell
cd C:\path\to\se_harness
python -m pip install .
harnessctl --version
```

For editable local development:

```powershell
python -m pip install -e .
```

Commands can also be invoked as `python -m se_harness` while this source tree is importable.

## Initialize or adopt a repository

Initialize an absent or empty target:

```powershell
harnessctl init C:\path\to\new-repository --project-name my-project
```

Adopt an existing repository without replacing its ordinary files:

```powershell
harnessctl adopt C:\path\to\existing-repository --project-name my-project
```

Adoption writes `docs/engineering/ADOPTION_REPORT.md`. The report contains bounded observations about the repository, not approved intent, requirements, architecture, or release authority. Accountable humans must author and approve the first formal engineering chain.

After either command, curate `docs/engineering/REPOSITORY_CONTEXT.md`. The installer seeds its structure but never infers commands, architectural claims, or product authority from observed repository content.

## Agent instructions and repository context

`AGENTS.md` is the canonical shared operating contract. The harness owns only its bounded `se-harness` block; repositories own all content outside that block and may add nested `AGENTS.md` or `AGENTS.override.md` files for component-specific rules.

`CLAUDE.md` is a thin compatibility adapter containing `@AGENTS.md` inside the same kind of bounded block. Repository-specific Claude Code instructions may be kept outside the block. This avoids maintaining a second copy of shared rules.

`docs/engineering/REPOSITORY_CONTEXT.md` is seeded once and immediately becomes repository-owned. Confirm the exact setup, build, test, lint, entry points, generated paths, sensitive paths, and specialized review constraints there. It informs execution but cannot replace approved intent, requirements, architecture decisions, or a work order.

During upgrade, shared managed fragments are hash-checked; customized content is preserved. Repository context is neither content-hashed nor overwritten. If its accounted seed is intentionally removed, upgrade does not silently recreate it, while `doctor` reports the missing required context for explicit resolution.

## Five-minute operating workflow

1. Run `init` for a new repository or `adopt` for an existing one.
2. Author the intent, capability, requirements, specifications, architecture, decisions, verification contract, and work order in `docs/engineering/`.
3. Obtain explicit human approval for the governing artifacts and work order.
4. Validate the graph and open Harness Explorer.
5. Implement only the approved work order and retain evidence keyed to its ID.
6. Run the required tests and checks, then commit the clean candidate source and evidence.
7. Prepare a commit-bound verification record, obtain human assurance review, and retain the record in a later governance commit.
8. If release is separately authorized, prepare a release record for the same candidate commit. Tagging, release transition, pushing, and publication remain separate human-controlled actions.

Typical operating commands:

```powershell
harnessctl doctor C:\path\to\repository
harnessctl validate C:\path\to\repository
harnessctl dashboard C:\path\to\repository
```

Harness Explorer is generated at:

```text
target/harness-dashboard/index.html
```

## Engineering artifact model

The formal graph separates reusable engineering policy from individual verification and release decisions:

```text
INT -> CAP -> REQ
               |-> SPEC
               |-> ARCH <- ADR
               |-> VER
               `-> WO

WO + VER + evidence + candidate commit C -> VREC
REL gates WO
RLS includes VREC and releases WO at the same commit C
OPS assures REL
```

| Artifact | ID prefix | Purpose |
| --- | --- | --- |
| Intent | `INT-` | Defines the approved outcome and problem. |
| Capability | `CAP-` | Describes what stakeholders must be able to do. |
| Requirement | `REQ-` | States verifiable system obligations. |
| Specification | `SPEC-` | Defines behavior and implementation contracts. |
| Architecture | `ARCH-` | Constrains structure and technical boundaries. |
| Architecture decision | `ADR-` | Records an accountable architectural decision. |
| Verification contract | `VER-` | Defines how requirements must be verified. |
| Work order | `WO-` | Authorizes a bounded implementation. |
| Verification record | `VREC-` | Binds work, evidence, and verification policy to an exact clean commit. |
| Release contract | `REL-` | Defines reusable release conditions. |
| Release record | `RLS-` | Records one release decision for the verified candidate commit. |
| Operating contract | `OPS-` | Defines operational assurance expectations. |

Source files and tests are not automatically formal artifact nodes. A work order authorizes their change, retained evidence demonstrates the checks performed, and a verification record binds that evidence to the exact candidate commit.

## What Harness Explorer answers

Harness Explorer is a derived, read-only view. It never approves work or releases. It is designed to answer five practical questions:

1. **Why does this work exist?** Trace a work order or requirement back through capability to approved intent.
2. **Is the engineering chain complete?** Identify active requirements without specification or verification coverage and relations with missing or incorrect targets.
3. **Where are the inconsistencies or anomalies?** Surface validation errors, missing work-order evidence, lifecycle inconsistencies, unsafe evidence paths, duplicate release versions, commit mismatches, and unavailable commits.
4. **What exact revision was verified or released?** Show declared candidate commits, related evidence and work orders, local commit availability, and comparison with the observed checkout.
5. **How ready is the work?** Show gates G0 through G5 as `satisfied`, `unsatisfied`, or `not_assessable` from intent readiness through operational acceptance.

The readiness gates are:

- G0: Intent ready
- G1: Requirement ready
- G2: Engineering ready
- G3: Implementation complete
- G4: Release ready
- G5: Operationally accepted

Missing human judgment or external evidence remains `not_assessable`; it is never silently converted into success.

## Commit-bound verification and release lineage

The authoritative lineage is:

```text
Intent -> Capability -> Requirement -> Work order(s)
       -> Aggregate verification record at final candidate commit C
       -> Aggregate release record for the same candidate commit C
       -> Operating assurance
```

First commit the completed candidate source and retained evidence. The worktree must be clean. Then prepare a verification record:

```powershell
harnessctl capture-verification C:\path\to\repository `
  --id VREC-001 `
  --work-order WO-001 `
  --verification VER-001 `
  --evidence docs/engineering/DOMAIN/evidence/WO-001-verification.md
```

The command derives the full SHA-1 or SHA-256 `HEAD`, checks the graph and evidence path, captures the dashboard snapshot hash, and writes only a `ready` `VREC-*`. It does not approve, commit, tag, release, push, or publish.

For a final candidate containing multiple release-bearing work orders, repeat the scope options. The selected verification contracts must equal the union declared by the work orders, and evidence must be retained for each work order:

```powershell
harnessctl capture-verification C:\path\to\repository `
  --id VREC-SEH-001 `
  --work-order WO-DST-001 `
  --work-order WO-REV-001 `
  --verification VER-DST-001 `
  --verification VER-REV-001 `
  --evidence docs/engineering/distribution/evidence/WO-DST-001-verification.md `
  --evidence docs/engineering/provenance/evidence/WO-REV-001-verification.md
```

An accountable human reviews the evidence and decides whether to transition the record to `verified`. The record is retained in a later governance commit because a file cannot contain the hash of the commit that contains itself.

After verification and separate release authorization, prepare a release record:

```powershell
harnessctl prepare-release C:\path\to\repository `
  --id RLS-001 `
  --release-contract REL-001 `
  --verification-record VREC-001 `
  --work-order WO-001 `
  --version 1.0.0 `
  --authorized-by release-owner
```

The resulting `ready` `RLS-*` copies candidate commit C from the verification record. It does not point to the later governance commit and does not create or verify a Git tag.

An aggregate release repeats `--work-order` and, when needed, `--verification-record`. Its released-work set must exactly equal the union covered by the included verification records, every work order must be gated by the release contract, and all included records must name the same candidate commit:

```powershell
harnessctl prepare-release C:\path\to\repository `
  --id RLS-SEH-001 `
  --release-contract REL-SEH-001 `
  --verification-record VREC-SEH-001 `
  --work-order WO-DST-001 `
  --work-order WO-REV-001 `
  --version 1.0.0 `
  --authorized-by release-owner `
  --tag v1.0.0
```

Only release-bearing implementation work belongs in `releases_work`. Publication, approval, verification-transition, and other governance-only work orders remain auditable on the governing branch but are not automatically shipped in the wheel.

Explorer compares each declared candidate commit with the observed checkout:

- `exact`: the checkout is the declared candidate;
- `different`: the checkout has moved, commonly because a later governance commit retains the record;
- `not_assessable`: the checkout or declared revision cannot be evaluated locally.

A `different` state is review information, not automatic proof of failure. Commit consistency between verified and released records remains a blocking invariant.

## Command reference

| Command | Behavior |
| --- | --- |
| `init` | Installs the standard harness into an absent or empty repository. |
| `adopt` | Installs into an existing repository and generates a non-authoritative adoption report. |
| `validate` | Validates the formal artifact graph and preserves the validator exit status. |
| `dashboard` | Generates the deterministic Harness Explorer and preserves generator status. |
| `doctor` | Checks runtime compatibility, configuration, lock integrity, required files, and managed-file drift. |
| `upgrade` | Plans a managed-file upgrade without writing by default. |
| `upgrade --apply` | Applies only additions, integrations, and updates to unmodified managed content. |
| `capture-verification` | Prepares a `ready` single or aggregate verification record at one final candidate commit. |
| `prepare-release` | Prepares a `ready` single or aggregate release record using that same candidate commit. |

Use `harnessctl <command> --help` for all arguments.

## Safety and authority boundaries

- Installation resolves and plans every destination before writing.
- Ordinary destination conflicts stop initialization or adoption without known partial writes.
- Existing `AGENTS.md`, `CLAUDE.md`, and `.gitignore` receive bounded managed blocks rather than wholesale replacement.
- Repository context is seeded only when absent and then remains repository-owned.
- `.engineering-harness.lock` records explicit schema-2 canonical UTF-8 text hashes and management modes for tool-owned content.
- Upgrade changes only missing or unmodified managed content; customized files remain untouched for manual reconciliation.
- Symlink traversal, repository escape, unsafe evidence paths, absent Git `HEAD`, dirty verification state, duplicate output, and inconsistent provenance fail closed.
- Adoption inventories observable repository signals but never manufactures approved product authority.
- Automation may prepare `ready` records but never grants verification or release authority.
- The harness does not create commits, tags, pushes, releases, deployments, or publications.
- The harness structures engineering evidence but does not itself declare regulatory compliance.

## Installed repository layout

```text
.engineering-harness.toml            harness configuration and schema
.engineering-harness.lock            managed-content hashes and modes
AGENTS.md                             bounded agent operating contract
CLAUDE.md                             thin import of the shared AGENTS contract
ENGINEERING_HARNESS.md                repository engineering entry point
.github/workflows/
  engineering-harness.yml            CI validation
docs/engineering/
  REPOSITORY_CONTEXT.md               repository-owned commands and constraints
  DECISION_RIGHTS.md                  human and automation authority
  QUALITY_GATES.md                    G0-G5 gate definitions
  TRACEABILITY.md                     relation and evidence model
  WORKFLOW.md                         operating sequence
  templates/                          formal artifact templates
scripts/
  validate_engineering_artifacts.py   deterministic validator
  generate_harness_dashboard.py      deterministic Explorer generator
  harness_explorer/                   self-contained Explorer view
target/harness-dashboard/             generated read-only dashboard
```

Target repositories own their product artifacts and customizations after installation. The distribution repository supplies versioned managed content; it does not become authoritative for target product intent.

## Safe upgrades

Inspect an upgrade plan:

```powershell
harnessctl upgrade C:\path\to\repository
```

Apply safe managed changes:

```powershell
harnessctl upgrade C:\path\to\repository --apply
```

Schema-2 locks use SHA-256 over `utf8-text-lf-v1`, so LF, CRLF, and CR checkout representations compare equally while every other content distinction remains significant. Schema-1 raw-byte locks remain readable and migrate only when an exact legacy match or canonical equality to the rendered desired template proves the operation safe. Customized or ambiguous managed files are reported for human reconciliation and are not overwritten.

## Distribution repository

```text
se_harness/                              CLI and safe installation control plane
templates/repository/standard/           canonical standard installation
scripts/                                 self-validation and Explorer generation
tests/                                   deterministic installer and provenance tests
docs/engineering/harness-distribution/   distribution governance and evidence
docs/engineering/revision-provenance/    commit-lineage governance and evidence
```

Run the development checks from this repository:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python -m unittest discover -s tests -p "test_*.py"
python -m se_harness --help
```

The validator, Explorer generator, and view at the repository root are byte-identical to their canonical managed-template copies. This allows the distribution repository to validate and visualize itself using the same machinery installed elsewhere.
