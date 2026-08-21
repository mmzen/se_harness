+++
id = "REQ-DST-065"
type = "requirement"
title = "Confine harness scaffolding and readiness to governed material"
status = "implemented"
owners = ["product-owner", "requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN the standard harness is installed, upgraded, or evaluated for implementation readiness, THE SYSTEM SHALL scaffold and require only material the harness itself governs, SHALL NOT create or require a repository-local operational context document, and SHALL leave any existing owner-authored context file untouched while omitting the retired path from the regenerated lock."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Confine harness scaffolding and readiness to governed material

## Lifecycle

Drafted on 2026-08-21 following the repository owner's boundary assessment of `docs/engineering/REPOSITORY_CONTEXT.md`, and approved by the repository owner the same day together with `SPEC-DST-021`, `VER-DST-021`, `REQ-IAR-021`, `SPEC-IAR-013`, `VER-IAR-013`, and `WO-DST-021`. The three open decisions were resolved at approval and are recorded below.

Approval makes this requirement active. It does not authorize implementation, which `WO-DST-021` governs, and it does not transition `REQ-DST-008`; that supersession is implementation work under the same work order.

## Rationale

`INT-DST-001` makes the engineering harness repeatably available. `CAP-DST-001` installs and operates a standard repository harness. Neither obliges the harness to author, own, or gate on facts that belong to the consuming repository.

`REQ-DST-008` currently obliges the installer to seed a repository-context scaffold, and `REQ-IAR-005` obliges preflight to require its curation. The result is that a consumer must author fifteen owner-confirmed fields before the first start preflight can pass. Measurement of the released 0.5.0 installer shows the scaffold ships fifteen `TODO[...]` placeholders across four sections, and `se_harness.preflight` rejects every unresolved one with `C004`.

Ten of those fifteen fields are never consumed. Each has exactly one reference in the product: the `CONTEXT_FIELDS` tuple that requires it. Only the five `COMMAND_KEYS` reach a consumer, and they reach it as text: `repository_commands` is assembled in `run_preflight` and used in exactly two places, the rendered report and the serialized JSON. No harness code path executes a repository command. Every executable step across the seventeen procedures in the active workflow contract invokes `harnessctl` itself, and the only argv placeholders are `{artifact_id}` and `{related_id}`.

The scaffold therefore does not supply the harness with anything the harness needs. It relays repository-local facts that the repository already states elsewhere, and `AGENTS.md` is already loaded on every agent turn while the context file is a second document to open. The obligation buys adoption cost and no assurance.

The gate is also weaker than it appears. `UNRESOLVED_CONTEXT` matches only a value that is exactly `TODO` or `TODO[slug]`, so a field reading `TODO[test-command] - ask the owner` satisfies `C004`. A conscientious owner pays the full authoring cost; a hurried one defeats all fifteen checks with trivial edits. Requiring fields that nothing reads and that a placeholder can satisfy produces delay, not confidence.

The product already contemplates the file's absence. `integrity.py` accepts a seed `state` of `present` or `removed`, and `SPEC-DST-002` states that the lock records seed presence or removal without a content hash "so later upgrades preserve repository edits and intentional deletion". The lock format, the integrity model, and an implemented specification all admit deliberate deletion. Only `preflight.REQUIRED_PATHS` forbids it. The product simultaneously permits and requires the same file.

Retirement is mechanically simple for the same reason. The installer discovers seeds by the `.seed` suffix while enumerating the template tree, and it rebuilds the lock `files` map exclusively from the current template item set. Deleting the seed template therefore stops the scaffolding and drops the lock entry without a code change. The `removed` state exists to remember that an owner deleted a seed the harness still ships, so that later upgrades do not recreate it; that purpose ends when the seed stops shipping, and retaining a tombstone would require new code with no consumer.

A second asymmetry confirms which side is wrong. `AGENTS.md` appears in `REQUIRED_PATHS` but not in `POLICY_PATHS`, so the reading manifest treats the owner's own instruction file as outside harness policy scope while pulling the repository-local context file inside it. That inversion is the defect.

## Preconditions and trigger

- A repository is initialized, adopted, or upgraded by the standard installation; or
- implementation or review readiness is evaluated for a work order in that repository.

The trigger does not depend on whether the repository has ever had a context file. Both the never-installed and the previously-seeded cases are in scope.

## Required response

1. Installation and upgrade SHALL NOT create `docs/engineering/REPOSITORY_CONTEXT.md` or any successor scaffold for repository-local operational facts.
2. Readiness evaluation SHALL NOT require the presence of such a file, SHALL NOT parse it, and SHALL NOT emit a diagnostic about its fields.
3. Where a prior installation recorded the seed, upgrade SHALL omit the retired path from the regenerated lock and SHALL leave any existing file on disk untouched as owner content.
4. Upgrade SHALL NOT delete, move, rewrite, or truncate an owner-authored context file under any circumstance, and SHALL NOT report the retired path as drift, as a missing managed file, or as an integrity failure.
5. The readiness reading manifest SHALL list only harness-governed policy material.
6. Installation guidance SHALL direct the repository owner to state build, test, verification, ownership, and boundary facts in the owner-controlled region of `AGENTS.md`, and SHALL NOT direct the owner to curate a harness-scaffolded document.
7. An executable workflow step SHALL NOT resolve through content the harness does not govern. The repository-context action-identifier reference form is withdrawn.
8. The change SHALL be released as a minor version with an explicit migration note, because a repository whose preflight currently passes must not start failing and a repository that removes the file must not start failing either.

## Failure and boundary behavior

- A repository that keeps its context file continues to pass. The file becomes ordinary owner content with no harness meaning; presence is neither required nor forbidden.
- A repository that deletes its context file passes. This is the state the current product rejects and the new obligation permits.
- Upgrade encountering an existing file and a `present` seed entry omits the path from the regenerated lock and does not touch the file. Encountering an absent file and a `present` entry does the same. Both cases converge on the same lock, so repeated upgrades are idempotent.
- A lock that cannot be rewritten transactionally aborts the upgrade without partial writes, per the existing managed-integrity obligation.
- A downgrade to a version that still ships the seed re-creates the file, because no tombstone is retained. That is accepted: downgrade is not a supported operation and the re-created file is owner-editable.
- A workflow procedure that still declares a repository-context action identifier invalidates the workflow contract rather than resolving against ungoverned content.
- Withdrawing the fifteen-field gate removes the structured `repository_commands` object from the preflight payload. Two mechanisms keyed off the retired file and only one was live, so the loss is narrower than the field set suggests. The live half is the label-based parse in `_parse_context`, which selects the five `COMMAND_KEYS` and emits them as JSON on every run; the harness never executes or validates those values, and internally they reach only the rendered report and one test assertion. The dead half is the `CTX-ACT-*` marker form, which is unreachable because no caller supplies `repository_context`. The accepted loss is therefore that an external tool can no longer read a command string from the payload; it reads owner prose instead. The loss is accepted deliberately: the check was placeholder-satisfiable, the value was never validated as a command, and the facts are now stated in the surface an agent already loads.

## Constraints

- Preserve every repository-owned surface. No owner content is deleted, relocated, or rewritten by this change.
- Do not add a replacement scaffold under another name or path. Renaming the obligation does not satisfy it.
- Do not weaken managed-file integrity, the released-evaluator boundary, or the transactional upgrade guarantee.
- Do not change which artifacts the harness governs. This requirement narrows what the harness scaffolds and requires; it does not narrow artifact authority.
- Historical evidence, verification records, and release records that describe the retired obligation remain unchanged. They record what was true when written.

## Acceptance examples

### Example: fresh installation

**Given** an empty repository and the standard installation

**When** the harness is installed and start preflight runs for an approved work order

**Then** no repository-context document is created, no context diagnostic is emitted, and preflight readiness depends only on harness-governed material.

### Example: upgrade preserving owner content

**Given** a repository installed under an earlier version whose `docs/engineering/REPOSITORY_CONTEXT.md` contains owner-authored facts and whose lock records the seed as `present`

**When** the repository is upgraded

**Then** the file is byte-identical afterwards, the regenerated lock contains no entry for the path, `doctor` reports no drift, and preflight neither requires nor parses the file.

### Example: failure behavior

**Given** a candidate workflow contract whose procedure step declares a repository-context action identifier

**When** workflow-contract conformance is checked

**Then** the contract is rejected, because an executable step must not resolve through content outside harness governance.

## Resolved decisions

The repository owner resolved all three on 2026-08-21 at approval.

First, the report schema advances to `se-harness-preflight-v2` rather than being revised in place. Removing `repository_commands` from a versioned public payload is a breaking interface change, and a consumer keying on the field must fail loudly on an unrecognized schema rather than read a silent default from a `v1` payload that no longer carries it. `SPEC-DST-021` rule 10 governs.

Second, withdrawing the command declaration requires no compensating check. The decision was taken on the corrected measurement above, which separates the live JSON payload from the unreachable `CTX-ACT-*` execution form. The owner accepted the loss of the payload object rather than retaining a narrowed five-field scaffold or relocating a typed declaration into governed material; both alternatives were put and both were declined. `SPEC-DST-021` rule 2 therefore stands: no replacement scaffold under any name.

Third, `ARCH-DST-002`, `ARCH-DST-007`, and `ARCH-IAR-001` do not require revision and no deciding ADR is required. The accountable no-ADR rationale is that the change withdraws a scaffolded component and an unreachable extension point without altering any selected architectural boundary, dependency direction, trust boundary, runtime dependency, or deployment architecture. All three artifacts describe the retired document only through the deprecated `constrains` relation and none declares that it addresses this requirement. Their descriptive text is revised under `WO-DST-021` without reopening the accepted decisions.
