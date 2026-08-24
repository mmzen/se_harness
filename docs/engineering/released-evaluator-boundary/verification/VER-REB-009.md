+++
id = "VER-REB-009"
type = "verification"
title = "Independent verification of role-specific release qualification"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-REB-020", "REQ-REB-021", "REQ-REB-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:15:39Z"
decided_by = "quality-owner"
+++

# Verification Contract: Independent verification of role-specific release qualification

## Independence

Verification shall not infer correctness from command names, handler-returned provenance, workflow step prose, or a shared implementation constant. Tests independently construct expected evaluator/target identities from wheels, installed files, Git objects, locks, release records, manifests, and view bytes. They independently snapshot repository/root/external state and parse canonical results with a test-owned strict schema oracle.

Candidate-controlled fixtures may report arbitrary passes, versions, digests, and check lists. The released-verifier and predecessor tests determine whether those claims can affect independent identity or overall results. Workflow conformance tests parse executable command blocks and selected environments rather than trusting labels.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-REB-020` | CLI/parser contract | five-operation positive matrix and all cross-role option combinations | Only the five declared operations and their closed schemas parse |
| `REQ-REB-020` | adversarial runtime/target integration | wrong root lock, candidate-as-verifier, predecessor mismatch, commit/digest substitution, import contamination, wrong target kind | Every mismatch fails before the role's substantive validation and emits no passing result |
| `REQ-REB-020` | process-boundary instrumentation | predecessor and candidate-package subprocess probes | Candidate/successor modules never load in the released verifier or predecessor process |
| `REQ-REB-021` | independent schema oracle | canonical result golden/property corpus | Exact schema, operation, identity, checks, independence, outcome, and no-authority fields agree with independent observations |
| `REQ-REB-021` | replay and fault injection | two identical runs plus interruption/output-collision cases | Decision-bearing bytes replay identically; no interruption or failure leaves a passing/partial replacement |
| `REQ-REB-021` | privacy inspection | hostile paths, environment, credentials, file bodies, subprocess output | Retained JSON contains no absolute workstation paths, secrets, unrelated environment, or untrusted body excerpts |
| `REQ-REB-022` | workflow static contract | candidate, predecessor, release, publication, dashboard, and managed-template workflow corpus | Every qualification claim invokes the required role from the required environment with required provenance; the sole public-0.6.0 bootstrap lane retains only exact legacy acceptance evidence |
| `REQ-REB-022` | workflow mutation tests | replace role commands with raw `doctor`, `validate`, scripts, wrong role, or renamed step | Each mutation is rejected regardless of step prose or raw command exit status |
| `REQ-REB-022` | managed-boundary test | root/template hashes before and after | Candidate template changes as approved; current root managed workflow and lock remain byte-identical |

## Acceptance scenarios

### Released root

1. Exact public 0.6 runtime plus a root lock naming its archive/payload/version passes identity, doctor, complete validation, and no-change checks.
2. Changing any lock identity, running from candidate source, pointing at a candidate archive, enabling user site/`PYTHONPATH`, or contaminating imports fails before doctor/validation.
3. Mutating one managed target byte during validation fails no-change even if validator output is zero.

### Predecessor view

1. The exact historical predecessor and contract-bound 0.5-to-0.6 view pass while retaining separate complete-current and predecessor-view claims.
2. Wrong predecessor version/wheel/payload/entry point, caller-selected omission, view-manifest tamper, source change, rejected-history byte change, post-hash view change, or candidate import fails.
3. A pre-command predecessor can run only through the registered version adapter. An unregistered version or arbitrary script path fails.
4. Repeating construction over one commit/release identity yields identical path manifests and view digests on Windows and POSIX.

### Complete candidate

1. Candidate source and installed candidate package bound to the exact commit pass the complete graph and label all results `candidate-controlled`.
2. Dirty tracked content, wrong commit, source/package version mismatch, incomplete graph, or validator failure fails.
3. A forged candidate result claiming `released-verifier` or `external-predecessor` is rejected by the independent result oracle and workflow contract.

### Candidate package

1. Exact released verifier independently checks a valid candidate wheel in a disposable installation and returns a role-bound pass.
2. Candidate wheel/archive/payload/commit mismatch, unsafe archive member, package metadata mismatch, checkout on verifier `sys.path`, candidate import in the verifier process, or candidate environment escape fails.
3. Mutate candidate `se_harness/cli.py`, validators, result builder, or acceptance output so it claims success. The released verifier's identity, archive checks, isolation checks, and final independently owned decision remain unaffected or fail safely.
4. `accept-candidate` and `qualify candidate-package` produce the same canonical semantics and invoke one handler; a divergence test fails.
5. The initial bootstrap invokes exact public 0.6.0 `accept-candidate` only after archive, payload, entry-point, isolation, candidate commit, candidate wheel, and scenario-contract binding; its result remains `se-harness-functional-acceptance-v1` and cannot be accepted as canonical qualification output.
6. Mutating the bootstrap version, archive or payload digest, entry point, command, schema, scenario contract, or artifact label fails. A fixture representing a released verifier with `qualify candidate-package` makes retention of the bootstrap invocation fail.

### Public install

1. A clean environment installed from an exact released public wheel passes wheel, payload, version, entry point, resource, CLI, release-record, and source-contamination checks without network access.
2. A locally rebuilt same-version wheel, wrong public digest, wrong payload, unreleased record, missing resource, altered entry point, checkout import, or unavailable acquired wheel fails.
3. Public-install success is rejected if reused as a candidate-package, predecessor-view, or released-root result.

## Property and invariant tests

- Operation and independence classification are a fixed one-to-one mapping.
- Every accepted CLI option belongs to exactly one operation or the common rendering/output set.
- Overall `passed` equals the conjunction of all mandatory check outcomes after valid identity; it cannot be set by target-controlled JSON.
- Process exit zero is equivalent to canonical `passed = true`.
- Target and evaluator identity digests change when any decision-bearing input byte changes.
- Nondeterministic platform/run/path/time facts do not change normalized decision-bearing output.
- Evidence output is exclusive and atomic; an existing file, linked parent, repository-internal path, invalid name, write fault, or interruption cannot overwrite or leave a misleading pass.
- Operations leave inspected repository bytes, index, worktree, refs, root lock/configuration, lifecycle state, environments, and external state unchanged.

## Static and architecture checks

- The CLI contains one `qualify` router and five explicit handlers; no general role/script dispatch exists.
- Workflow files use typed operations for release-qualification claims and do not call raw validators for those claims.
- The predecessor handler delegates view construction to the shared service rather than duplicating its omission policy.
- The candidate-package handler delegates to one hardened acceptance implementation; the compatibility alias has no second implementation.
- The immutable public-0.6.0 bootstrap invocation is separately classified as legacy deployment evidence, exact-identity-bound, noncanonical, and removal-triggered; tests do not compare its immutable implementation structure with the new alias.
- Low-level diagnostic APIs do not import workflow YAML.
- Candidate/sdist/wheel help and package resources expose the same command contract.
- Root managed paths are absent from the changed-path set.
- The architecture dependency and prohibited-pattern checks in `ARCH-REB-009` pass.

## Security and privacy checks

Exercise traversal, symlink/junction/hardlink, case collision, duplicate archive member/key, malformed JSON/TOML/front matter, noncanonical UTF-8/LF, oversized file/output, subprocess timeout, invalid digest/commit, executable substitution, environment injection, shell metacharacters, user-site/PYTHONPATH contamination, Git alternate state, and credential-bearing environments.

Instrument imports and child processes to prove candidate/successor code does not execute in released-verifier or predecessor interpreters. Prove secrets and hostile file contents do not enter canonical results or bounded errors.

## Performance and resilience checks

- Verify mandatory hashing and substantive validators run at most once per operation.
- Verify bounded subprocess output, timeout, cleanup, and deterministic failure under a killed child or write fault.
- Run focused role tests and the full supported suite on Windows and Linux.
- Reconcile normalized canonical results for the same immutable fixture across both platforms while retaining platform-specific factual identities separately.

## Manual assessments

Quality, security, and release owners shall review:

- the exact command/role/independence table;
- the legacy predecessor adapter and its removal boundary;
- workflow before/after command maps;
- candidate mutation evidence demonstrating independent decision ownership;
- root/template distinction and the list of operations not authorized;
- human/JSON examples for each role and representative failures.

## Evidence retention

Retain the approved preflight, exact candidate commit when separately authorized, changed-path manifest, command/help snapshots, parser matrix, evaluator/target identity matrix, hostile-case corpus, workflow before/after map, root/template hashes, source/wheel/sdist parity, focused/full/platform outputs, normalized replay hashes, import/process traces, no-change snapshots, and actions-not-performed statement under the work-order evidence path.

A later VREC must bind the exact implementation commit, this verification contract, `WO-REB-020`, and the keyed evidence path. Passing tests or this contract alone do not transition the work order or grant assurance.

## Residual uncertainty

The first implementation will preserve bounded adapters for the exact predecessor view and exact public 0.6.0 candidate acceptance where immutable released tools do not expose typed qualification. Their correctness is covered by identity and isolation tests. The public-0.6.0 candidate adapter has an objective removal trigger: availability of a released verifier exposing `qualify candidate-package`. Removing the predecessor-view adapter depends on future supported-predecessor policy. Hosted package indexes and GitHub services remain outside the command boundary; workflows bind acquisition facts separately.
