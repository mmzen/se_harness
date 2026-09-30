+++
id = "SPEC-IAR-016"
type = "specification"
title = "External harness resources and minimal installation"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
contract = "The selected released package supplies harness resources outside the repository; plugins deliver them, while installation and migration preserve portable selection, owner content and lifecycle authority."

[relations]
specifies = ["REQ-IAR-029", "REQ-IAR-030", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 deb4e81838ec4d2fe9ae06c43f00b532490477d413f15547034a228cb8cd1f3e."
+++

# External harness resources and minimal installation

## Contract boundary

This is a proposed future released layout. The repository stays governed by
its installed 0.20.0 evaluator until a separately authorized release and adoption.
The package does not rewrite SPEC-IAR-014 or declare accepted definitions amended.
The applicability decision prepared with this package must be resolved before
implementation approval. Lifecycle meanings, human rights and required gates stay fixed.

## Rules

**IAR-EXT-001.** Resource ownership. Use the exact released evaluator package as
the single source of standard entry text, procedures, authoring guidance, artifact
templates and machine policy. Keep source assets in this product repository for
building distributions; stop copying them into consuming repositories. Reuse
existing wheel payload integrity rather than introduce a second package registry,
independent policy archive, plugin-specific policy edition, or new dependency.

**IAR-EXT-002.** Selection. Keep .engineering-harness.toml and
.engineering-harness.lock as portable repository records. Bind the released
evaluator and resources to their exact version and existing wheel/payload digests.
Add a declared layout/schema discriminator where needed. Persist no workstation
paths in these repository records. Session-local checkout paths follow
IAR-EXT-012. A plugin update does not change these records. A selected older layout
continues to use its original release and rules.

**IAR-EXT-003.** Resolution. Provide one evaluator-owned resource resolver used
by CLI, authoring, checks and discovery. A small read-only CLI operation exposes
the selected release, resource-relative IDs, byte identities and usable local
paths/headings. Its final name and JSON fields are chosen with the implementation
and documented together; these drafts claim no such command exists in 0.20.0.
Validate the complete selection before returning usable instructions or writing
an artifact. Never search candidate source, a different checkout or the newest
plugin directory as a substitute. Do not add a generic URI framework.

**IAR-EXT-004.** Consumer parity. CLI, CI and plugins resolve the same selected
release. Machine policy remains evaluator input; agents read only selected human
instructions. Update discovery metadata explicitly to distinguish released
resources from repository artifacts. Preserve existing consumers or return an
explicit incompatible-schema result. Preserve all decision, scope, gate, evidence
and lifecycle semantics on equivalent inputs; only declared storage/readiness
rules change. Candidate testing must not turn the candidate into this repository's
governing evaluator. A completed candidate package is tested outside the source checkout.

**IAR-EXT-005.** Plugin delivery. Extend the existing setup and hook adapter.
Store evaluator environments outside repositories, keyed by selected release
identity, so two releases coexist. Setup installs an explicitly selected trusted
wheel using the existing identity checks. Hooks resolve already installed
resources, inject the full compact entry and identify the repository and release.
Do not fetch on startup or compaction. Missing, altered or mismatched input gives
a bounded delivery gap for a selected repository. With no selection, use the
bootstrap in IAR-EXT-011. Installation must not require AGENTS.md or create a
managed AGENTS.md/CLAUDE.md gate.

**IAR-EXT-006.** Reading and authoring. Preserve the compact entry's invariant
meanings and the current task/step reading split. Render project name and release
in delivered context without persisting a rendered root copy. Resolve relative
instruction links against the released resource location; repository artifact
links resolve against the selected checkout. Artifact templates and standard
checklists are read directly from the package. No bulk instruction injection.

**IAR-EXT-007.** Fresh installation. With no repository integration requested,
write only the configuration and lock. Optional CI, PR-template or sample-content
scaffolding is explicitly selected and previewed; it is not a matrix of harness
profiles. Do not introduce new sample-generation machinery where existing
commands suffice. Keep AGENTS.md, CLAUDE.md and existing project documents untouched.
Artifact creation writes only its requested output and required parent structure.
Before producing hash-bound evidence, establish the applicable Git byte-preservation
rules through a disclosed, supported setup action; absence is a clear readiness
finding, not permission to relax hashing. Cache/output ignore rules are added
only for a selected integration that actually writes those outputs.

**IAR-EXT-008.** Migration. Implement preview/apply through the existing installer
transaction. Verify target package identity and replacement delivery before retiring
the old entry. Classify all leaving files before writes. Remove recognized managed
copies only within the reviewed plan. Require explicit owner selection to retire
unchanged editable seeds, including templates and ARTIFACT_AUTHORING.md. Preserve
customized owner content and report an action-required item; no automatic content
merger or implicit policy overlay is introduced. Owner rules remain in AGENTS.md
or another explicitly referenced owner file; their manual migration and review
must precede removal of a customized instruction source. Reject path escapes,
symlinks, ambiguous identity and unsupported layouts before partial mutation.
Retain rollback/retry guarantees of the existing transaction.

**IAR-EXT-009.** References and compatibility. Update active product guides,
plugin skills, examples, installer reports and CI instructions to the resource
route. Remove assertions that require current repository copies only when the
successor layout replaces them; retain older-release fixtures and refusal tests.
Classify historical references by their recorded release/commit without rewriting
evidence. Record the old-to-new resource map in ordinary migration documentation,
not another runtime registry or repository pointer forest. CLI/CI remains usable
without a host plugin. Cached selected resources work offline; missing resources
require explicit setup, never an automatic fallback.

**IAR-EXT-010.** Release and qualification. Build from one canonical asset tree
and publish through the existing release/marketplace procedures. Qualify the
candidate wheel, both host packages and plugin-free CI with matching resource
identity. Product release, marketplace publication, and adoption into this
repository require their later explicit authority. These work orders do not bump
the selected root version, remove its installed guides, or publish anything.

**IAR-EXT-011.** Bootstrap. Ship one short selection and recovery instruction in
the shared plugin source. At startup and after compaction, a session without a
selected repository receives this instruction as a normal starting state. It
directs the agent to clone when requested, reuse an identified existing checkout,
activate the exact resulting path, and read the returned entry before governed
work. Ask for a target only when it is ambiguous. A checkout without a harness
selection follows the existing setup procedure; never choose a release silently.
The bootstrap contains no lifecycle policy, artifact templates or work-order
authority. The hook performs no clone, installation or repository mutation.

**IAR-EXT-012.** Session activation. Extend the existing setup skill with one
local activation helper; its command and fields are documented with the
implementation. Use the host-supplied session identity, surfaced in hook context
when the helper needs it. A user statement alone is not a persisted selection.
The agent passes the actual checkout path to the helper after cloning or selecting
existing work. Validate the repository selection and released resource identity,
then record the checkout and return its compact entry immediately. Do not wait
for another startup or compaction event. If resources need preparation, follow
setup and rerun activation before governed work.

Store one small record per host and session in private plugin data outside the
checkout and replaceable plugin package. It records the absolute checkout path,
not policy, artifact states, decisions or credentials. A saved explicit selection
is used before discovery from the host working directory. With no saved selection,
retain direct discovery from that directory and its ancestors; never scan child
repositories or reuse a global last-selected repository. Independent sessions
start with independent selection. A fork or new session with a new host identity
must activate its own target; a host resume preserving identity reuses its record.

Revalidate the record and current repository release on every delivery and
activation. Reject malformed, unreadable, linked or conflicting inputs. A failed
activation does not replace a valid record, and the failed requested target stays
blocked. Explicit switching or clearing affects only that session. Never turn an
invalid saved selection into an unselected startup or a fallback to another
checkout. Native host tests must show that the helper and hooks address the same
session record across compaction and resume; missing host identity is a reported
limitation, not grounds to infer a session from the transcript or shared cwd.

**IAR-EXT-013.** Repeated and parallel work. Each activation selects an exact
checkout or worktree, not just a remote URL. Use separate writable checkouts for
parallel agent work. Keep work-order selection and lifecycle state in the formal
records and evaluator results, not in the session record. New or resumed work
uses the selected release's procedures; activation supplies no implementation,
assurance or external-action authority. After work, use the existing delivery
procedure for the exact candidate and destination. No new Git or PR client is
introduced. A later cycle may reuse or explicitly replace the session's checkout.

Evaluator environments are keyed by the complete released identity. Concurrent
setup for one identity must not expose a partial environment or reinstall over
one in use. Preparing another release leaves existing environments unchanged.
Session-record updates are atomic. These guarantees require only bounded local
coordination; no daemon, shared policy service or cross-session scheduler is added.

## Checkable examples

1. Empty repository, default initialization: only two selection files appear.
2. Repository A selects release A; repository B selects release B: each host
   delivers its own entry before and after compaction, including offline.
3. A template exists only in the selected package: create-artifact writes one
   valid draft in the repository and no copied template directory.
4. Customized old authoring guide: preview identifies owner action and apply
   leaves the installation unchanged until the explicit migration is resolved.
5. Start above a checkout that does not exist yet: receive the bootstrap, clone,
   activate the resulting path, then obtain the selected work order's next action.
   Compaction restores that selection while the host cwd stays in the parent.
6. Two sessions share a parent workspace and activate separate checkouts pinned
   to different releases: interleaved work and compaction preserve both identities.
   Setup requests for the same release cannot expose an incomplete evaluator.
7. A selected checkout is removed or its resources fail validation: delivery
   reports that gap, with no instruction fallback. An unrelated new session
   starts unselected and receives bootstrap guidance.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-IAR-029 | IAR-EXT-001, IAR-EXT-002, IAR-EXT-003, IAR-EXT-004, IAR-EXT-006 |
| REQ-IAR-030 | IAR-EXT-002, IAR-EXT-003, IAR-EXT-005, IAR-EXT-006, IAR-EXT-009, IAR-EXT-011, IAR-EXT-012, IAR-EXT-013 |
| REQ-IAR-031 | IAR-EXT-007, IAR-EXT-008, IAR-EXT-009, IAR-EXT-010 |

## Simplicity and exclusions

Reuse the released wheel, identity checks, setup script, hook, installer transaction
and typed discovery. Keep two selection files. No policy service, background
synchronizer, generic override language, new dependency or instruction copies
inside each plugin build. Add only the layout discriminator and lookup needed
to support external resources and the retained legacy route, plus the short
bootstrap and per-session checkout record required when cloning after startup.
Reuse the host cwd route when it already identifies the checkout. The additional
record covers the confirmed parent-directory and parallel-session workflow.
