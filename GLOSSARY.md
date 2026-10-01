# Glossary

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

## Summary

This page defines the project terms of the se_harness repository: the words
used across the README, the formal artifacts and these notes whose meaning
belongs to this repository. Each entry is one or two sentences and, where
one artifact fixes the meaning, names it. Start here when a term is
unfamiliar; the [getting started](docs/notes/getting-started.md) page shows the
terms in use.

Two vocabularies meet in a requirement. Harness terms, such as work order,
verification record, decision right and checkpoint, are the same in every
repository that uses the harness and are defined in the managed
instructions; a few are repeated here because this repository's readers
meet them first. Project terms, such as candidate, digest and evaluator, are
this repository's own. This page is repository content at the repository root.
Repository-copy releases seed an empty `GLOSSARY.md`; the external-resource
candidate creates no glossary by default. The harness never rewrites it, and no
entry here ships to another repository. `harnessctl inspect` names the frequent
project terms that lack an entry and the entries whose term has left the
artifacts.

## Terms

**Work order (WO).** A file that authorizes one bounded change and lists the paths it may touch. Nothing is implemented without one.

**Verification record (VREC).** A file that binds evidence and one or more work orders to one exact commit. A human decides whether to accept it as `verified`; later permitted lifecycle transitions preserve its candidate and evidence history (see [verification decisions](docs/engineering/harness/VERIFY_OUTCOME.md#record-the-verification-decision)).

**Release record (RLS).** A file that binds a release contract, eligible verification records and one exact candidate commit. Preparation creates a `ready` record; an authorized human makes the separate release decision (see [release decisions](docs/engineering/harness/RELEASE.md#obtain-the-release-decision-when-required)).

**Definition.** The collective name for the artifacts that describe a plan before work starts: intent, capability, requirement, specification, architecture, ADR, verification contract, release contract, and operating contract.

**Decision right.** The rule that identifies who may authorize a specific action. The evaluator reports the required right and checks the action; a command may apply an authorized decision, but running it does not supply that decision (see [decision rights](docs/engineering/harness/AUTHORITY.md#decision-rights)).

**Evaluator.** The installed copy of SE Harness that judges a repository. It runs at a pinned released version, from a virtual environment outside the checkout.

**External resources.** The successor layout keeps standard instructions, policy
and templates in the exact selected evaluator wheel. The repository holds its
portable selection, owner content and formal artifacts. The plugin delivers
selected instructions; it does not supply a separately versioned policy copy.

**Session activation.** Selection of an exact checkout for one native host session.
The plugin validates the release, saves a private local locator and returns the
entry immediately. The locator grants no authority and is not a repository file.

**Plugin.** A package loaded by a coding application to add instructions, event handlers, and other supported components.

**Coding host.** The application running the coding agent, such as Codex or Claude Code. Each host controls how plugins and tools are loaded.

**Skill.** Instructions an agent follows for a named task. A skill may direct tool use but does not grant decision authority.

**Hook.** A host event registration that invokes code, for example when a session starts or before a supported tool action.

**Private environment.** An isolated Python environment created for the plugin outside the target repository. It uses provided Python and contains the selected released evaluator.

**Wheel.** An installable Python package archive. It contains package files and metadata; it does not supply the Python interpreter.

**Root evaluator versus candidate.** The root evaluator is the released version the repository pins in `.engineering-harness.toml`. The candidate is the source code being developed in the checkout: it is judged, and it never judges.

**Managed file.** A file the tool installs and hash-locks. Editing it by hand breaks `doctor` and the required CI check.

**Owner file.** Repository content the owner controls, such as product code and local instructions. The harness may seed some owner files at installation, but later replacement requires explicit owner authority; owner content is not hash-locked as managed policy (see [upgrades](docs/engineering/harness/UPGRADE.md#upgrade-the-installed-harness)).

**Lock.** The file `.engineering-harness.lock`, which records the selected evaluator identity and hashes for managed repository files. Schema 5 also selects external resources; its file entries cover only selected repository integrations.

**Gate.** A named group of checks evaluated together. A gate passes only when every one of its checks passes.

**Checkpoint.** The moment in a procedure at which `check` runs a gate: `start`, `pre-action`, `transition`, `handoff`, or `scope`.

**Projection.** A `check` result obtained without a checkpoint. It reports lifecycle context and the next step; it does not evaluate checkpoint gates or authorize work (see [continuation](docs/engineering/harness/CONTINUE.md#continue-selected-work)).

**Restitution.** The operator-facing summary in a workflow result: what completed, what is blocked, the decision due and one next step. Agents report that result without inventing effects or authority (see [reporting results](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result)).

**result_sha256.** The digest that binds the declared machine fields of a workflow result; in the current format, explanatory wording is excluded. A generated `Harness-Restitution` field refers to one work-order result and does not replace checking the current PR body and complete diff (see [result digests](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result) and [PR checks](docs/engineering/harness/PULL_REQUEST.md#check-a-governed-pull-request)).

**Evidence packet.** The retained file recording what was done and checked for one work order. It is bound to the formal snapshot current when it was written, so later artifact edits are detectable.

**Handoff.** The moment an in-progress work order's implementation is offered as complete. The handoff check judges the change set, scope, and evidence, and retains its own result.

**Formal snapshot.** A digest over the canonical bytes of every formal artifact in the repository. Evidence packets bind to it.

**Delegation class.** A historical work-order table that granted specified execution steps under the rules of its release. Current work-order approval grants bounded execution through [authority from work approval](docs/engineering/harness/AUTHORITY.md#authority-from-work-approval); older approvals keep their recorded limits, and human-reserved decisions remain with humans.

**Change set.** The list of paths a change touched, derived from Git or explicitly declared. Scope checks compare it against the paths the work order authorizes.

**Domain.** One directory under `docs/engineering/` that groups related artifacts and their evidence, named by a three-letter code that appears in artifact identifiers.

**Candidate.** The source code of this checkout as it stands on a branch: judged by the root evaluator, never judging. The word takes a qualifier when it matters: a candidate commit is one exact revision; the candidate package is a wheel built from it and never promoted; the candidate templates are the managed files under `templates/repository/standard/` that ship with the next release (`SPEC-DST-014`, `WO-DST-023`).

**Digest.** A SHA-256 value computed from the bytes or canonical fields specified by its contract. Examples include managed-file hashes, formal-snapshot and evaluator-evidence hashes, and the workflow result's `result_sha256`; each uses its own declared input and format (`SPEC-REV-001`, [current result format](docs/engineering/harness/RESULTS.md#report-a-lifecycle-result)).

**Canonical.** The single byte form a file is reduced to before it is hashed or compared: LF line endings for text, sorted keys and fixed separators for JSON. Two files that differ only outside the canonical form have the same digest (`SPEC-DST-014`).

**Deterministic.** Producing identical bytes from identical inputs, on every platform and every run: no timestamps, no environment detail, sorted output. The Explorer build, the diagnostic-code index and the vocabulary report are deterministic (`SPEC-TCM-002`, `SPEC-TCM-003`).

**Schema.** The declared shape of a machine-read document, named by a string such as `se-harness-inspection-v2`. A consumer refuses a document whose schema it does not know; a new field means a new schema name (`SPEC-ECP-006`).

**Accountable role.** A legacy label for a decision responsibility, such as assurance owner or release owner. Current [decision rights](docs/engineering/harness/AUTHORITY.md#decision-rights) distinguish humans and agents and record the actual decision-maker and authority; a profile or role label alone grants no permission.

**Dashboard snapshot.** The generator's canonical projection of every artifact, relation and diagnostic, from which the Explorer bundle and the inspection are built. Not the formal snapshot, which is a digest over artifact bytes (`SPEC-DST-014`).

**Provenance.** The recorded chain from a claim to the exact revision and evidence behind it: the commit a record binds, the worktree state, the evaluator that produced the evidence and its digest (`SPEC-REV-001`).

**Predicate.** One exact condition assessed by a gate, such as `QGP-G4I-PATHS`. At the selected checkpoint, every required predicate assessed there must pass before that gate permits the action (see [gates](docs/engineering/harness/RESULTS.md#gates)).

**Contract (of a specification).** The one sentence in a specification's front matter saying what an implementation must do to conform. The Explorer shows it under the title; the validator budgets it at 30 words on a draft (`SPEC-TCM-006`).

**Rule identifier.** The stable name of one rule in a specification, `<PREFIX>-<AREA>-NNN`, written in bold at the start of the rule. It is how a verification contract, a work order, an evidence packet or a deviation cites the rule; it never moves and is never reused (`SPEC-TCM-006`).

**Coverage table.** The table at the end of a specification mapping each requirement it specifies to the rule identifiers that meet it. The validator reads it on drafts and the Explorer shows it on the specification and, as "Covered by", on each requirement (`SPEC-TCM-006`).

## Upkeep

Follow the repository's selected harness procedure when changing this page,
then use a reviewed pull request. SE Harness 0.20.0 has no owner-configured
documentation exception; [EXCEPTIONS.md](docs/engineering/harness/EXCEPTIONS.md#availability)
therefore directs this work through the normal definition and work-order process.

`harnessctl inspect` reports frequent project terms without an entry and entries
whose term appears in no artifact. Use that report and reviewers' questions to
propose glossary updates; the report grants no change authority.
