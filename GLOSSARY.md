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
this repository's own. This page is repository content at the repository root: the harness seeds
an empty `GLOSSARY.md` there at installation and never rewrites it, and no
entry here ships to another repository. `harnessctl inspect` names the frequent
project terms that lack an entry and the entries whose term has left the
artifacts.

## Terms

**Work order (WO).** A file that authorizes one bounded change and lists the paths it may touch. Nothing is implemented without one.

**Verification record (VREC).** A file that binds a work order's evidence to one exact commit. A human decides whether it becomes `verified`; after that it can never be edited.

**Release record (RLS).** A file recording the separate release decision, tied to the same exact commit that verification assessed.

**Definition.** The collective name for the artifacts that describe a plan before work starts: intent, capability, requirement, specification, architecture, ADR, verification contract, release contract, and operating contract.

**Decision right.** The rule that says who may take a given decision. Commands report which decision is due and which right owns it; they never take it.

**Evaluator.** The installed copy of SE Harness that judges a repository. It runs at a pinned released version, from a virtual environment outside the checkout.

**Root evaluator versus candidate.** The root evaluator is the released version the repository pins in `.engineering-harness.toml`. The candidate is the source code being developed in the checkout: it is judged, and it never judges.

**Managed file.** A file the tool installs and hash-locks. Editing it by hand breaks `doctor` and the required CI check.

**Owner file.** Repository content the owner controls, such as product code and local instructions. The harness does not write or lock it.

**Lock.** The file `.engineering-harness.lock`, which records the digest of every managed file and the identity of the evaluator release that installed them.

**Gate.** A named group of checks evaluated together. A gate passes only when every one of its checks passes.

**Checkpoint.** The moment in a procedure at which `check` runs a gate: `start`, `pre-action`, `transition`, `handoff`, or `scope`.

**Projection.** `check` without a checkpoint. It reads the state and names the next step; it judges nothing and writes nothing.

**Restitution.** The fixed-format result block every workflow command prints: what completed, what is blocked, the decision due, and one next step, with a digest of its own content.

**result_sha256.** The digest inside a restitution. For a completed handoff it covers the change set and every check's status, and the pull-request body declares it, so the reviewed result and the reviewed tree cannot drift apart.

**Evidence packet.** The retained file recording what was done and checked for one work order. It is bound to the formal snapshot current when it was written, so later artifact edits are detectable.

**Handoff.** The moment an in-progress work order's implementation is offered as complete. The handoff check judges the change set, scope, and evidence, and retains its own result.

**Formal snapshot.** A digest over the canonical bytes of every formal artifact in the repository. Evidence packets bind to it.

**Delegation class.** One table on a work order that lets an automated actor take three named lifecycle steps while the required pull-request check is green. Every other decision stays human.

**Change set.** The list of paths a change touched, derived from Git or explicitly declared. Scope checks compare it against the paths the work order authorizes.

**Domain.** One directory under `docs/engineering/` that groups related artifacts and their evidence, named by a three-letter code that appears in artifact identifiers.

**Candidate.** The source code of this checkout as it stands on a branch: judged by the root evaluator, never judging. The word takes a qualifier when it matters: a candidate commit is one exact revision; the candidate package is a wheel built from it and never promoted; the candidate templates are the managed files under `templates/repository/standard/` that ship with the next release (`SPEC-DST-014`, `WO-DST-023`).

**Digest.** A SHA-256 over exact bytes. The lock holds one per managed file, a verification record holds one over the formal snapshot and one over its evaluator evidence, and a restitution holds one over its own content as `result_sha256` (`SPEC-REV-001`).

**Canonical.** The single byte form a file is reduced to before it is hashed or compared: LF line endings for text, sorted keys and fixed separators for JSON. Two files that differ only outside the canonical form have the same digest (`SPEC-DST-014`).

**Deterministic.** Producing identical bytes from identical inputs, on every platform and every run: no timestamps, no environment detail, sorted output. The Explorer build, the diagnostic-code index and the vocabulary report are deterministic (`SPEC-TCM-002`, `SPEC-TCM-003`).

**Schema.** The declared shape of a machine-read document, named by a string such as `se-harness-inspection-v2`. A consumer refuses a document whose schema it does not know; a new field means a new schema name (`SPEC-ECP-006`).

**Accountable role.** The named role that holds a decision right and answers for the decision: product owner, technical owner, assurance owner, release owner, engineering owner. In this repository one person holds every role; the record still names the role, not the person (`DECISION_RIGHTS.md`).

**Dashboard snapshot.** The generator's canonical projection of every artifact, relation and diagnostic, from which the Explorer bundle and the inspection are built. Not the formal snapshot, which is a digest over artifact bytes (`SPEC-DST-014`).

**Provenance.** The recorded chain from a claim to the exact revision and evidence behind it: the commit a record binds, the worktree state, the evaluator that produced the evidence and its digest (`SPEC-REV-001`).

**Predicate.** One named check inside a gate, such as `QGP-G4I-PATHS`, with a fixed evaluator and the evidence it needs. A gate passes when every predicate it binds to the checkpoint passes (`QUALITY_GATES.md`).

## Upkeep

This page is a note: change it by pull request and review, never by a work
order. `harnessctl inspect` reports the frequent project terms without an
entry and the entries whose term appears in no artifact; add or retire
entries from that report and from reviewers' questions.
