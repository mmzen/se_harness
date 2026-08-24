+++
id = "VER-RLO-005"
type = "verification"
title = "Verify the cross-platform publication rehearsal and its divergence seam"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-RLO-015", "REQ-RLO-016"]
+++

# Verification Contract: Verify the cross-platform publication rehearsal and its divergence seam

## Independence

Expected mechanic sets, platform layouts, path forms, and divergence verdicts are derived from controlled fixtures and from independently parsed workflow text, not by calling the rehearsal's own declaration or classifier to produce the expectation it is then compared against. The orchestrator is compared byte for byte against the content this branch inherited from `main` rather than being re-derived; that reference content moved once, when `main` was merged in, and the comparison then means unchanged *by this packet* rather than unchanged in the repository. No production tag, ref, release, index object, deployment, environment approval, or artifact lifecycle state is mutated as implementation evidence.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-015 | real-platform execution, injected platform state, fixture matrix, boundary inspection | POSIX and Windows layout resolution; alias root canonicalization; temporary-identity assertion and its mismatch; double export; pinned build tools; qualification; unit suite; CLI smoke; deterministic build agreement and injected disagreement; sdist normalization; cross-set manifest and bundle verification and their failures; link-safe teardown, its post-audit of the root's own removal, residue refusal, and link-escape refusal; excluded-mechanic reporting; a predecessor-view subject no committed record can host; an inherited dirty worktree and an inherited line-ending conversion | every mechanic reports `executed` on both platforms in a passing run, or `excluded` with a reason naming the measured identities that make it unexercisable; each injected fault reports `failed` with the platform, mechanic, and observed divergence; no mechanic is silently skipped; teardown's post-audit accepts the rehearsal root's own removal and refuses any other path outside the root; no credential, ref, tag, release, index, deployment, or lifecycle state is created |
| REQ-RLO-016 | strict workflow parsing, classification fixtures, declaration property test | credential-free and credential-bearing job classification; transitively excluded job; absent permission block; unclassifiable job; uncovered mechanic; stale mechanic; name-similarity near miss; undeclared step; changed step digest; stale declared step; unclassified action; unpinned action; undeclared realization surface; bounded-reader and second-parser agreement, disagreement, and absence; data-only declaration; executable declaration; platform-claim check with a missing platform; matrix combination enumeration from `include` and from crossed axes, and its refusal of both together, of `exclude`, and of an empty matrix; an unmodelled `runs-on` expression; a step gated to one matrix mode, an ungated step in a matrix job, a step gated out of every combination, and a gate outside the comparison grammar; a step platform claim that no longer matches its gate; a mechanic platform claim that no longer matches the union over its realizing steps; a declaration whose step omits a platform claim, names an unknown platform family, or realizes no mechanic; a mechanic realized by no declared step of its own job | classification follows declared attributes and propagates through `needs`, with every exclusion reported; both divergence directions fail closed and name the mechanic and direction; a near-miss name does not count as covered; a step whose digest changed fails although every command it invokes is declared; an undeclared or unpinned action fails; a surface outside the vocabulary is refused before comparison; a requested cross-check with no second parser fails rather than falling back; an executable declaration fails; a matrix job's platforms are the union over its resolved combinations and an unmodelled runner expression or matrix shape is refused rather than guessed; a step's platforms follow its own gate rather than its job, a stale step or mechanic platform claim fails closed in the `stale` direction, and a step the orchestrator can no longer reach on any platform fails; a declaration missing a step platform claim or a mechanic's realizing step is refused before any comparison |

## Acceptance scenarios

Executable scenarios are retained in `acceptance/publication-rehearsal.feature` and mapped to automated tests in retained evidence.

## Property and invariant tests

- The interpreter and console-script paths always resolve from the running platform, and no `bin/` or `Scripts/` literal path is constructed unconditionally.
- The rehearsal root is always canonicalized before any environment creation or export.
- A child process always reports the temporary root the parent set.
- Every derived path lies under the rehearsal root.
- Teardown never unlinks a path outside the rehearsal root, and always leaves the repository worktree clean. Its post-audit accepts exactly one path whose parent is outside the root — the root itself — and audits every other removal by its parent.
- The predecessor-view qualification is exercised only against a subject whose committed contract names the evaluator the run resolved; otherwise it is excluded with both identities and never reported as failed.
- The recipe-bound build replay's exclusion reason is measured in a fixed precedence — absent eligible released schema-2 subject, then platform or container runtime, then the boundary naming the dedicated replay lane — so the reported reason is the first one that actually holds.
- Bundle verification in `candidate` mode always compares one distribution set against a manifest derived from the other.
- The result always states its mode, and only `release-record` mode claims comparison against an authorized release identity.
- Mechanic matching is always by exact identity.
- Every credential-free orchestrator step is either declared with a matching normalized-run digest or reported as a divergence; a declared digest is never trusted without recomputation.
- Every declared mechanic names a realization surface drawn from the declared vocabulary.
- A job's platforms are always the union over its enumerated matrix combinations, and a runner label or matrix shape the resolver does not model is always refused rather than defaulted.
- A step's platforms are always its job's combinations minus those its own gate excludes; a gate that reads a run-time context or status function is always treated as able to hold; a gate outside the comparison grammar is always refused.
- Every declared mechanic's platform claim always equals the union over the declared steps of its own job that realize it, so the step-to-mechanic link can never be decorative.
- The recipe-bound build replay is always reported `excluded` with a measured reason, in both modes, and never `executed` and never omitted.
- An orchestrator mechanic is either covered, declared rehearsal-only, or reported as an exclusion with its causing attribute; there is no fourth outcome.
- A job is treated as rehearsable only when it is credential-free itself and depends on no excluded job.
- The rehearsal never constructs a credential, token, environment reference, or write permission.

## Static and architecture checks

- Strict parsing confirms the rehearsal lane declares both the Linux and the Windows runner type and `contents: read` only, with no environment, secret, token, or external-state-mutating action. The bounded reader's structure is confirmed against an independent parser on both workflow files and on every fixture, so strictness is measured rather than assumed.
- `.github/workflows/publish-pypi.yml` is byte-identical to the content this branch inherited from `main`, proven by a pinned digest over the file normalized to LF so a converting checkout compares equal to the stored blob. The pinned digest is re-derived only when a merge brings a change from `main`, and the re-derivation is disclosed with the incoming commit that caused it.
- The mechanic declaration is data only.
- No POSIX-only utility invocation, and no `cygpath` invocation, appears in the rehearsal program or its lane.
- Changed-path, built-wheel, and standard-template inspection confirm no `se_harness/`, `templates/repository/standard/`, managed validator, managed workflow, lock, or consumer change.
- The domain model validates with no new structural, governance, or policy errors.

## Security and privacy checks

Treat orchestrator YAML, declaration data, downloaded evaluator bytes, subprocess output, filesystem state, and link targets as untrusted. Verify the evaluator digest is proven before installation, that no credential or environment value is printed, that the lane holds no write permission, that candidate code runs with no credential, and that a link planted inside a derived tree cannot cause deletion outside the rehearsal root.

## Performance and resilience checks

Confirm the mechanic sequence is fixed and bounded with no retry or polling loop, that the rehearsal builds the candidate exactly twice per platform, and that a failure in one mechanic still yields a complete per-mechanic result rather than an unlabeled abort. Confirm a failed rehearsal leaves no residue.

## Manual assessments

- The release owner confirms that a rehearsal result is understood as derived operational evidence and does not substitute for the qualification inside an authorized release.
- The quality owner confirms the accepted weakness in `ARCH-RLO-005` — that equivalence is checked rather than structural, so a difference in the sequence or surrounding environment of a mechanic both lanes declare is outside the checker's model — is an acceptable residual risk with the recorded revisiting condition.
- The security owner confirms that no credential, token, environment, or write permission is introduced, that `pages_build` is correctly classified as excluded, and that `observe` is correctly excluded through its dependency although it holds no credential of its own.
- The technical owner confirms the portable boundary from `ADR-RLO-002` is unchanged.

## Evidence retention

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-005-implementation.md` with the candidate under measurement, changed surfaces, the complete mechanic table with per-platform outcomes, the full negative-case matrix with exact diagnostic text, the divergence verdicts in both directions, the byte-unchanged orchestrator proof, local execution transcripts on the platform available to the implementer, test commands and counts against a measured baseline, formal graph validation and preflight results, boundary inspection, warnings, residual risks, and every production and external action not performed.

## Residual uncertainty

Local execution and fixtures cannot prove hosted runner-image behavior, and the implementer can execute only one of the two platforms directly; the other platform's real behavior is first proven by the hosted lane. The checked equivalence seam cannot detect a divergence in the sequence of mechanics or in the state surrounding a mechanic that both lanes declare, because its unit of comparison is a step's script rather than the pipeline that reaches it. A local rehearsal additionally inherits its checkout, so a mechanic requiring a clean worktree cannot be proven from a dirty one, and a checkout that converts line endings changes the outcome of byte-exact assertions in the candidate suite; the result reports both conditions rather than concealing them. One mechanic, the predecessor-view qualification, has no valid subject in `candidate` mode on post-release integration and is reported excluded there, so its real behavior is exercised only by a `release-record` rehearsal of a record under preparation or by the release itself. A second mechanic, the recipe-bound build replay, is outside this control's reach in both modes: it needs a released distribution-schema-2 record with a bound recipe, which the repository does not yet have, and an immutable `linux/amd64` container producer, which the Windows runner type cannot run at all. It is declared and reported excluded with its measured reason, and the repository's dedicated credential-free replay lane, not this rehearsal, is what exercises it. That lane is not the declared orchestrator, so this packet's divergence check does not read it; a change to it is therefore invisible here. The first separately authorized production release after merge remains the operational confirmation of publication itself, which this work does not modify.

## Approval

Approved as an independent evidence contract by the accountable repository owner on 2026-08-24 through the statement `OK go for #111`. This does not verify an implementation candidate.

## Amendments during implementation

Accepted by the accountable repository owner on 2026-08-24 through the statement `Accept all seven`, which covers the seven amendments recorded across `SPEC-RLO-005`, `REQ-RLO-015`, and this contract. Every amendment adds a required case or narrows a claim; none removes a case or relaxes a pass condition, and the acceptance verifies no implementation candidate.

- The `REQ-RLO-016` evidence row gains the cases the amended requirement creates: transitive exclusion, an absent permission block, undeclared and changed and stale steps, unclassified and unpinned actions, an undeclared realization surface, and the second parser's agreement, disagreement, and absence.
- Three property tests are added: a recomputed step digest, a closed realization-surface vocabulary, and rehearsability as credential-freedom plus dependency-freedom.
- "Strict YAML parsing" becomes "strict parsing", with the bounded reader's agreement against an independent parser as the measurement of strictness, because the check must run with no repository dependency.
- The quality owner's assessment and the residual uncertainty restate the accepted weakness. Step digests closed the argument-level and within-step ordering cases, so asking the owner to accept them as residual risk would have misstated the risk; the sequence-and-environment case is named in their place.
- The residual uncertainty records that a local rehearsal inherits its checkout. Two shakedown runs measured this on the predecessor-view mechanic — first its refusal of an uncommitted worktree, then, after the packet was committed, `PV001` for a different reason entirely — and a third measurement on the unit suite, whose byte-exact assertions follow the inherited `core.autocrlf` into the candidate checkout.
- The `REQ-RLO-015` pass condition admits an `excluded` outcome with a reason naming the measured identities, alongside `executed`. It already had to: teardown reports `excluded` under `--keep-root`, and `SPEC-RLO-005` amendment A7 adds a mechanic that has no valid subject in `candidate` mode by construction. Requiring `executed` for every mechanic would have made the contract unsatisfiable rather than strict. The owner ruled on 2026-08-24 that `excluded` is the correct report for that mechanic, so a future candidate that reports it `executed` in `candidate` mode against a mismatched subject, or that omits it from the result, fails this contract.
- The `REQ-RLO-016` row, the property tests, and the static orchestrator check gain the matrix-aware layers that `SPEC-RLO-005` amendments `A8` and `A9` add: matrix combination enumeration and its refusals, per-step gate resolution, step and mechanic platform claims in the `stale` direction, the declaration's schema-`v2` refusals, and the twenty-second mechanic's always-excluded outcome. The orchestrator's byte-unchanged check now names the content inherited from `main` rather than the merge base, because `main` changed the file while this branch was open and the claim this packet can honestly make is that it contributes no byte. These two amendments are **not** covered by the `Accept all seven` acceptance above and await the accountable owner's decision.
- The teardown row and property gain the root's own removal. The post-audit was measured refusing the removal it had just performed correctly, which no earlier fixture caught because none put the root in the audited list.
