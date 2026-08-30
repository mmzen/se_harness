# Glossary

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

## Summary

This page defines the project-specific terms used across the README, the managed instructions, and these notes. Each entry is one or two sentences. Start here when a term is unfamiliar; the [getting started](getting-started.md) page shows the terms in use.

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
