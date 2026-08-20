+++
id = "VER-WEX-001"
type = "verification"
title = "Verify deterministic scoped workflow execution"
status = "approved"
owners = ["quality-owner", "assurance-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
verifies = ["REQ-WEX-001", "REQ-WEX-002", "REQ-WEX-003", "REQ-WEX-004", "REQ-WEX-005"]
+++

# Verification Contract: Verify deterministic scoped workflow execution

## Independence

Primary acceptance tests invoke the public candidate CLI in disposable repositories and compare observed files, exit status, human output, and JSON against fixtures derived from `REQ-WEX-001` through `REQ-WEX-005` and `SPEC-WEX-001`. They do not import the implementation's scope classifier, transition table, next-step registry, renderers, or mutation planner as their oracle.

Expected scope membership, state edges, metadata, immutable fields, and handoff values are declared in verifier-owned scenario data. Candidate-source unit and failure-injection tests add repository-owned evidence but do not substitute for black-box acceptance. Where the self-hosting boundary applies, the standard released evaluator runs outside the checkout and records candidate-package evidence separately from candidate-source checks.

Verification can establish deterministic CLI behavior and adapter conformance. It cannot prove that every language model will always invoke the tool correctly, that a claimed actor truly holds an accountable role, or that a human decision is substantively sound. Those remain explicit manual and authority boundaries.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-WEX-001` bounded scope | black-box `focus` fixtures for WO, VREC, and RLS plus unrelated findings | isolated and mixed-domain repositories; duplicate-ID and damaged-integrity cases | governing and dependency sets exactly match the fixture; selected, repository, and background classes are stable; unrelated findings never become selected-scope actions |
| `REQ-WEX-002` atomic preconditions | plan/apply boundary tests and filesystem failure injection | legal packet, incomplete packet, wrong source state, stale plan, replace failure at every write index | all preconditions are checked before mutation; failures retain pre-operation digests for every path; legal apply writes exactly the plan |
| `REQ-WEX-003` independent lifecycle planes | exact before/after repository comparisons | VREC verify/reject/supersede, RLS release/reject, separate provenance-backed WO transition | selected transition changes only explicitly selected artifacts; assurance and release projections derive from relations without implicit status synchronization |
| `REQ-WEX-004` honest decision metadata | schema, transition, and legacy-compatibility cases | ready preparation, later decision, rejection, unchanged legacy record, transitioned legacy record | ready records contain preparation but no later decision facts; transitions add actor/time/event consistently; immutable provenance remains unchanged |
| `REQ-WEX-005` canonical handoff | human/JSON semantic comparison, golden JSON, and supported-agent adapter corpus | success, plan, failure, stop, missing authority, and legal-alternative states | schema and ordering are stable; human fields equal JSON semantics; exactly one primary next step and correct authority/action are present; adapters preserve the canonical result |

## Acceptance scenarios

1. Focusing an implemented WO returns its intent, capability, requirements, specifications, applicable architecture/ADRs, verification contracts, and direct VREC/RLS coverage in stable order.
2. Focusing a VREC returns its WOs, verification contracts, each WO governing chain, and directly including RLS records without unrelated domain work.
3. Focusing an RLS returns its release contract, included VRECs, released WOs, and the governing chains required to assess release eligibility.
4. Unrelated maintenance warnings are summarized as background and never appear in the primary recommendation; `--include-background` expands them without changing classification.
5. Managed-integrity damage, duplicate formal identity, or an unreadable selected artifact blocks the operation as a repository or selected-scope blocker according to the fixed registry.
6. An absent, malformed, duplicated, or type-incompatible selected ID fails without choosing a nearby filename or relation target.
7. Repeated focus against identical bytes produces byte-identical JSON and semantically identical human handoffs.
8. Planning approval of a complete INT/CAP/REQ/SPEC/VER packet succeeds without writing; omitting required specification or verification coverage fails with no write.
9. Applying that same complete packet after the explicit decisions changes every selected status in one transaction and produces a graph-valid candidate without an intermediate invalid state.
10. Changing any planned input between plan and apply is detected as stale state and leaves the changed repository otherwise untouched.
11. Injected failure before the first replacement, at each replacement boundary, and after the last temporary render either performs the complete transaction or restores every pre-operation byte.
12. Capturing a VREC for a `draft`, `approved`, or `in_progress` WO fails and identifies `implemented` as the required state.
13. Capturing a VREC for an implemented WO with exact VER and evidence coverage creates only a ready VREC containing `prepared_at` and `prepared_by`, with no `verified_at` or `verified_by`.
14. Preparing an RLS from a ready, rejected, or superseded VREC fails; preparing from exact verified coverage creates only a ready RLS with preparation provenance and no `released_at` or `authorized_by`.
15. Verifying a ready VREC adds the verified state, lifecycle event, `verified_at`, and `verified_by` to that VREC only; every related WO and RLS digest is unchanged.
16. Releasing a ready RLS adds the released state, lifecycle event, `released_at`, and `authorized_by` to that RLS only; every included VREC and WO digest is unchanged.
17. Rejecting a ready VREC or RLS adds the rejection event, actor, time, and non-empty reason only to the selected record.
18. Superseding a ready VREC preserves every captured field and relation except the allowed supersession metadata and successor relation.
19. A failed operation's handoff reports no completed mutation, the unchanged formal state, the exact blocker, and one remediation or escalation action.
20. A successful applied transition reports the selected final state and recommends the next legal stage without performing it.
21. A state with multiple legal paths retains one primary recommendation and labels the other paths as bounded alternatives with their separate authorities.
22. An unchanged legacy record without preparation or lifecycle-event metadata remains compatible; a new governed transition adds only the required new event and target-state fields.
23. ChatGPT-, Claude-, and Codex-facing adapters given the same fixture state and explicit decision invoke the provider-neutral contract and expose the same selection, mutation plan, validation outcome, primary next step, and authority fields; prose outside canonical fields may differ.

## Property and invariant tests

- Permuting filesystem enumeration, relation declaration order where order is semantically irrelevant, hash-map insertion, locale, and supported path separators does not change canonical scope, findings, mutation, or JSON ordering.
- Every selected ID appears once in selection, before state, after state, decision mapping, and mutation plan as applicable.
- Scope closure contains only objects admitted by the declared WO, VREC, and RLS traversal rules; arbitrary graph reachability cannot enlarge it.
- Every permitted transition is present in verifier-owned transition cases, and every other source/target pair for that artifact family is rejected.
- A plan's writes equal the applied file changes exactly; no unplanned path or field changes.
- Failure at any validation or write boundary leaves the multiset of repository-relative file digests equal to the pre-operation set.
- VREC and RLS operations preserve related-record digests unless those records are separate explicit `--set` selections.
- Preparation fields precede decision fields temporally; a ready record cannot satisfy a verified or released metadata invariant.
- Each lifecycle event agrees with its artifact's before/after state and type-specific actor/time fields.
- Immutable candidate commit, object format, worktree state, snapshot hash, evidence, work coverage, verification contracts, release contract, version, and supersession facts remain protected according to record type and phase.
- Human and JSON renderings map to one `WorkflowResult`; parsing either canonical form yields the same lifecycle state, blocker set, recommendation, authority, command/response, and alternatives.
- Exactly one primary next action exists for every recognized final state or failure class; unknown states escalate rather than guess.

## Static and architecture checks

- Confirm each public parser shape, JSON field, status edge, scope rule, and metadata field matches `SPEC-WEX-001` and is documented once in the authoritative interface contract.
- Confirm transition, preparation, and focus share one provider-neutral domain implementation while human and JSON rendering consume the same result object.
- Confirm `inspect` retains its repository-wide schema and non-executable suggestion catalog; only `focus` owns selected-scope output.
- Confirm managed root files and `templates/repository/standard/` stay consistent where the work changes the standard installation, without advancing the root released installation improperly.
- Confirm Python 3.11+ standard-library-only runtime and one standard installation remain intact.
- Confirm package data, public documentation, help output, lock data, and fresh-install artifacts include every applicable interface and schema change.
- Confirm technical review records architecture decision applicability for the public CLI, state machine, lifecycle metadata, canonical output schema, and atomic multi-file writer before architecture approval.
- If the assessment is `adr_required`, confirm selected architecture has an active deciding ADR and every later WO selects the complete architecture/ADR chain.

## Security and privacy checks

- Exercise traversal, absolute paths, alternate separators, Windows reserved names, symlink/junction escape, case collision, duplicate ID, and repository-root alias inputs for target, artifact, evidence, and temporary paths.
- Exercise shell metacharacters, control characters, invalid Unicode, TOML delimiters, JSON fragments, format placeholders, and multiline content in actor, reason, and artifact metadata fields.
- Confirm no repository text is evaluated, interpolated into a shell command, imported as code, or emitted as an executable recommendation.
- Confirm recommended commands contain only validated static command grammar and known encoded arguments; human decision text remains a suggested response.
- Confirm normal output does not reveal evidence bodies, credentials, environment secrets, private URLs, or unrelated artifact prose.
- Confirm an actor assertion is retained as data but never treated as proof of role ownership or decision quality.

## Performance and resilience checks

- Measure snapshot validation, focus, and transition planning on deterministic repositories near 100, 500, and 1,000 formal artifacts; investigate superlinear growth not explained by declared graph traversal.
- Repeat each operation under randomized enumeration order and on supported Python 3.11+ runtimes.
- Exercise read-only filesystem, full disk, denied replacement, locked file, interrupted temporary write, concurrent edit, and rollback failure simulations.
- Confirm no failed path leaves temporary files inside formal artifact discovery locations or alters unrelated owner content.
- Confirm repeated plan and validation do not modify timestamps, files, Git index, branch, commits, tags, remotes, or external systems.
- Run the full repository test suite and standard fresh-install, upgrade, managed-integrity, preflight, candidate-acceptance, and distribution-parity checks applicable to the eventual work order.

## Manual assessments

- Product and requirements owners confirm the scope boundary and transition outcomes match the approved intent rather than merely making the current implementation easier to test.
- Technical owners confirm the command and metadata contracts are coherent, evolvable, and accompanied by the required architecture decision assessment.
- Assurance owners inspect representative before/after records and confirm preparation facts cannot be mistaken for verification or release decisions.
- Repository owners confirm stricter capture and release preparation failures are acceptable compatibility changes and are clearly documented.
- Reviewers run the supported-agent conformance corpus and confirm canonical fields make the same next action immediately visible even when surrounding prose differs.
- Reviewers confirm no Skill, agent prompt, branch convention, commit message, or command success is represented as formal authority.

## Evidence retention

Retain the following under the eventual WEX work-order evidence path:

- exact focused and full test commands, runtimes, test counts, duration, and exit status;
- verifier-owned scenario manifest and canonical JSON digests;
- before/after/failed-operation repository digest manifests;
- transition-table and scope-classification coverage reports;
- human/JSON semantic comparison and supported-agent adapter conformance results;
- security, path-boundary, concurrency, interruption, and rollback-failure results;
- candidate-source, candidate-package, and released-evaluator identities kept as separately labeled evidence;
- fresh-install, upgrade, managed-lock, distribution-parity, validation, inspection, preflight, and full-suite outputs;
- changed paths, diff hygiene, deviations, manual assessments, and residual risks.

## Residual uncertainty

Black-box automation cannot establish that an actor has the authority they assert, that a product or release judgment is correct, or that all future agent hosts will reliably invoke a discoverable tool. Filesystem atomicity across every exotic network or virtual filesystem may exceed supported guarantees and must be bounded by documented platform support. Canonical output greatly reduces model-dependent interpretation but does not make free-form prose byte-identical or eliminate malicious prompt behavior outside the harness boundary.

These limits require accountable review and explicit supported-platform and supported-agent declarations; they do not justify implicit transitions, authority inference, partial writes, or provider-specific lifecycle rules.
