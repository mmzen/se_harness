+++
id = "SPEC-REB-011"
type = "specification"
title = "Declared environment entry-point safety rule and interpreter identity facts"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-REB-023", "REQ-REB-024", "REQ-REB-025", "REQ-REB-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "technical-owner"
+++

# Specification: Declared environment entry-point safety rule and interpreter identity facts

## Scope

This specification defines one declared rule for validating an interpreter path as an environment entry point, the two conforming loaders that expose it to the package runtime and the repository-tools runtime, the identity facts recorded about an accepted interpreter, and the per-boundary migration required by issue #106 / RCA `RC-060-06`.

It does not change lifecycle policy, the canonical evaluator-evidence document, the runtime-identity schema identifier, the release-qualification result schema, the compatibility-view contract, product version, root managed bytes, or any public distribution.

## Actors and external systems

- **Package runtime.** `se_harness` modules that observe or verify runtime identity: `runtime_identity`, `release_qualification`, `governance_migration`, `mutation_guard` through `runtime_identity`, and the `identity` CLI command.
- **Repository-tools runtime.** `repository_tools` modules that validate externally supplied interpreters: `release_bootstrap`, `predecessor_preparation`, `predecessor_assessment`, `predecessor_publication`. This runtime imports only the standard library and its own package.
- **Filesystem.** Supplies symbolic links, Windows directory junctions, short-name aliases, and case-insensitive path variants. All path input is untrusted.
- **External interpreters.** Released-evaluator and predecessor environments outside the checkout, spawned as isolated subprocesses.

## Inputs

- A supplied interpreter path, which may be relative, may contain a user prefix, and may traverse links.
- A checkout root, when the boundary has one.
- A declared environment root, when the boundary derives an expected identity from governed inputs such as a lock, a release record, or a bootstrap contract.
- The declared rule document.

## Outputs

- An accepted entry point: one lexical absolute path.
- A derived environment root.
- A resolved interpreter target, used for digest and position facts and then discarded as a path.
- On refusal, one stable case identifier and subject.

## State model

The rule is stateless and performs no mutation. Evaluation is a pure function of the supplied paths and the filesystem state observed during the call. A boundary that must detect change between two observations compares recorded facts under rule 20; the rule itself makes no such claim.

## Behavioral rules

### The declared rule

1. **Normalization.** Expand a leading user prefix, then make the path absolute against the current working directory using lexical normalization only. No component is dereferenced. The result is the *lexical path*.
2. **Environment root.** The *environment root* is the lexical path's second parent. A lexical path with fewer than two parent components has no environment root and is refused with `EPS010`.
3. **Parent link refusal.** Walk every enclosing directory of the lexical path from its immediate parent to the filesystem root. If any of them is a symbolic link, refuse with `EPS001`. If any of them is a Windows directory junction, refuse with `EPS002`.
4. **Junction detection.** Junction detection is a separate predicate from symbolic-link detection. Where the running Python exposes `pathlib.Path.is_junction`, it is used. Where it is absent, the rule refuses with `EPS011` rather than passing the check silently.
5. **Existence and resolution.** Resolve the lexical path strictly. If resolution fails, refuse with `EPS003`. The result is the *resolved target*.
6. **Ordinary-file refusal.** If the lexical path is not a file, or the resolved target is not a file, refuse with `EPS004`.
7. **Final-component refusal.** If the lexical path traverses a link but is not itself a symbolic link, refuse with `EPS005`. This is the position that a junction or another reparse point occupies when it stands as the final component.
8. **Chained-target refusal.** If the resolved target's own path traverses a link, refuse with `EPS006`. A fully resolved target normally traverses none; this refusal is retained so that a partially resolvable path cannot smuggle a second hop.
9. **Checkout refusal.** When a checkout root is supplied, refuse with `EPS007` if the lexical path lies inside it and with `EPS008` if the resolved target lies inside it. Containment is tested on the lexical path lexically and on the resolved target after resolving both sides.
10. **Declared-root refusal.** When a declared environment root is supplied, refuse with `EPS009` unless the lexical path lies lexically inside it with a non-empty relative remainder.
11. **Acceptance.** A path that survives rules 1 through 10 is accepted. Its accepted entry point is the lexical path; a terminal symbolic link in the final position is accepted and is not dereferenced for any purpose other than the facts in rules 14 through 17.

Rules are evaluated in this order and the first refusal wins, so a refusal identifier is stable for a given path form. No rule consults the platform name, the interpreter file name, or a directory name such as `bin` or `Scripts`.

### The declaration

12. The declaration is `se_harness/interpreter_safety.json` with schema identifier `se-harness-interpreter-safety-v1`. It is data only: no code, no platform conditional expressed as code, and no per-boundary waiver.
13. It contains the ordered case list with each case's identifier, subject, and refusal or acceptance outcome; the boundary registry naming every identity boundary in both runtimes; and the conformance corpus of declared path forms with their expected outcome and the platforms on which each form can be constructed. A case present in the declaration with no implementation, and an implementation outcome absent from the declaration, are both conformance failures.

### Recorded identity facts

14. `RuntimeIdentity` retains `python_executable` as the lexical entry point.
15. `RuntimeIdentity` gains `python_entry_is_link`, a boolean that is true when the accepted entry point is a terminal symbolic link.
16. `RuntimeIdentity` gains `python_binary_position`, one of the constants `within-expected-root`, `within-checkout-root`, or `outside-declared-roots`. `within-checkout-root` is unreachable through rule 9 and exists so that an unbounded observation cannot silently omit the case. No absolute path for the resolved target is reported.
17. `RuntimeIdentity` gains `python_binary_sha256`, the lowercase SHA-256 of the resolved target's bytes, read once and bounded. An unreadable target is a refusal, never a null digest.
18. The schema identifier remains `se-harness-runtime-identity-v3`. The three additions are strictly additive; every consumer that validates a required field subset continues to accept the observation.
19. The canonical `se-harness-evaluator-evidence-v1` document is unchanged. Its `origins` and `environment` objects keep their exact five members each, and the added facts do not appear in it.
20. A boundary that supplies an expected environment verifies each added fact against its own observation: the entry path lexically, the terminal-link property against its own filesystem probe, the position class against its own containment test, and the digest against a digest it computes itself. A mismatch stops the boundary before substantive target validation.

### Per-boundary behavior

21. `repository_tools/release_bootstrap.py` validates the released-evaluator interpreter with the declared rule instead of `_ordinary_external_file`, derives the evaluator root from the accepted lexical entry point, and normalizes the interpreter origin lexically. `_ordinary_external_file` remains in use for the entry point and the wheel, which are ordinary files and must keep refusing every link.
22. `repository_tools/predecessor_preparation.py` and `repository_tools/predecessor_assessment.py` delegate their existing interpreter validation and origin normalization to the declared rule. Their current observable behavior is the reference for the rule and shall not change.
23. `repository_tools/predecessor_publication.py` continues to reach the rule through `predecessor_preparation`.
24. `se_harness/runtime_identity.py` applies the declared rule to `sys.executable` for the `released-evaluator` and `candidate-package` roles, keeps the existing lexical checks that produce `RID004` and `RID006`, and adds one diagnostic identifier for a declared-rule refusal.
25. `se_harness/release_qualification.py` external-evaluator location applies the declared rule, which adds the parent-link, junction, final-component, and resolved-target-in-checkout refusals it currently lacks, and keeps its existing entry-point and provenance checks.
26. `se_harness/governance_migration.py` replaces its `is_symlink`-only parent check with the declared rule. Its `MIG205` identifier and message are retained for parent-link and junction refusals so that its bound contract and fixtures keep their meaning, and its existing resolved-byte read becomes the rule's digest.
27. Interpreter-path comparison at every boundary is lexical on both sides. `repository_tools/release_bootstrap.py` stops resolving both sides of its `python_executable` comparison, matching the comparison already used by `repository_tools/predecessor_assessment.py`.

## Error and recovery behavior

Each runtime maps a declared case identifier onto its own existing error vocabulary: a `ReleaseBootstrapError`, `PredecessorPreparationError`, or `PredecessorAssessmentError` message in the repository-tools runtime; an `IdentityDiagnostic`, `HarnessError`, or `GovernanceMigrationError` in the package runtime. The declared case identifier appears in the diagnostic so that a refusal is traceable to the rule, and the existing identifiers that other artifacts and tests bind — `RID004`, `RID006`, `MIG205` — are preserved.

A refusal is terminal for that boundary. There is no retry with a resolved path, a relaxed rule, a different interpreter, a diagnostic allowlist, or a warning. Recovery requires correcting the supplied path or rebuilding the environment.

## Data and interface contracts

The package loader is `se_harness/interpreter_safety.py`, a sibling of its declaration, following the pattern already used by `se_harness/hash_bound.py` and `se_harness/governance_migration_contract.py`. The repository-tools loader is `repository_tools/interpreter_safety.py`, which reads the same declaration from its position relative to the repository root. Neither loader imports the other runtime; both use only the standard library.

Both loaders expose the same two operations: evaluate a supplied path against the rule, returning the accepted entry point, environment root, resolved target, and the recorded facts; and enumerate the declared cases and boundary registry for conformance checking.

The declaration ships in the wheel as package data alongside the existing declarations, and the portable-release-surface check lists it.

## Security and privacy properties

- Every path input is untrusted, including paths that arrive through a lock, a release record, a bootstrap contract, a view manifest, or a command line.
- Link and junction detection happens before the interpreter is spawned, before any target validation, and before any byte of the resolved target is read for a purpose other than the digest.
- No refusal message echoes file contents, credentials, package-index configuration, or unrelated environment values.
- Retained identity output contains no absolute path for the resolved target. The position class and the digest carry the fact without carrying the location.
- The rule opens no network connection and mutates nothing.

## Performance and capacity

Rule evaluation walks the lexical path's ancestors once and stats each, resolves once, and hashes the resolved target once per observation. The digest read is bounded and streamed. A boundary that already read the resolved target's bytes performs no additional read.

## Observability

A refusal names the declared case identifier, the role, and the failing subject. An acceptance is silent; the recorded facts are the observable output. The conformance check reports each diverging case with both observed outcomes rather than a count.

## Compatibility and migration

- The evaluator-evidence document, its closed field sets, and every existing bound sidecar digest are unchanged.
- The runtime-identity schema identifier stays at v3; a distinct identifier for the enlarged observation is deferred to a later governed change that also adopts a matching root evaluator.
- `RID004`, `RID006`, and `MIG205` keep their identifiers and meanings.
- Boundaries that are already correct keep their observable behavior; the change is where the rule lives, not what those boundaries decide.
- The corrected POSIX behavior is a relaxation of exactly one path form. Every environment that is accepted today remains accepted.
- Root managed files and the installed root evaluator are unchanged.

## Examples and counterexamples

| Path form | Outcome |
| --- | --- |
| `<env>/bin/python` as a terminal symbolic link to a system interpreter | accepted; environment root `<env>` |
| `<env>/Scripts/python.exe` as an ordinary file | accepted; environment root `<env>` |
| `<link>/bin/python` where `<link>` is a symbolic link to a real environment | `EPS001` |
| `<link>/Scripts/python.exe` where `<link>` is a `mklink /J` junction | `EPS002` |
| `<env>/bin/python` as a junction in the final position | `EPS005` |
| `<env>/bin/python` as a dangling link | `EPS003` |
| `<env>/bin/python` resolving to a file inside the candidate checkout | `EPS008` |
| `<checkout>/.venv/bin/python` with the checkout as the checkout root | `EPS007` |
| `/python` | `EPS010` |
| `<other>/bin/python` with `<env>` supplied as the declared root | `EPS009` |

## Explicitly unspecified decisions

Implementation may choose the loader module and function names, the internal result type, the exact refusal message wording beyond the required case identifier and subject, the digest streaming block size, the conformance-test module decomposition, and how the corpus expresses platform constructability.

It may not add, remove, renumber, or reorder a declared case; change an acceptance into a refusal or the reverse; add a per-boundary waiver; change a recorded fact's name or value domain; alter the runtime-identity or evaluator-evidence schemas; make `repository_tools` import `se_harness`; or leave a boundary unregistered.
