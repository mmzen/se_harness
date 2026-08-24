+++
id = "VER-REB-010"
type = "verification"
title = "Independent verification of environment entry-point safety"
status = "approved"
owners = ["quality-owner", "security-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-REB-023", "REQ-REB-024", "REQ-REB-025", "REQ-REB-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "quality-owner"
+++

# Verification Contract: Independent verification of environment entry-point safety

## Independence

Verification shall not infer correctness from the declaration's own text, from a loader's return value, from a shared constant, or from a docstring claiming a property. Tests construct real filesystem objects — ordinary directories, symbolic links, Windows junctions, dangling links, short-name aliases, case variants, and files inside and outside a checkout — and assert the outcome each boundary produces for each of them.

The corpus is owned by the tests as data and is compared against the declaration in both directions, so neither the declaration nor an implementation can define its own passing condition. Digests of the resolved interpreter are recomputed by the tests from the bytes they wrote, not read back from the observation under test.

Every claim of non-change is measured against an independently captured baseline at the base commit rather than inferred from an unchanged total or from a passing suite.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-REB-023` | Linux integration | a real `python -m venv` environment holding the exact released distribution, driven through every boundary that takes an external interpreter | The lexical `bin/python` is accepted, the environment root is the venv, and identity verification proceeds |
| `REQ-REB-023` | Windows integration | an ordinary `Scripts/python.exe` environment through the same boundaries | Accepted under the same rule with no platform branch in policy |
| `REQ-REB-023` | end-to-end bootstrap | release bootstrap binding against a POSIX venv evaluator | The binding completes; the derived evaluator root is the venv, not the system prefix |
| `REQ-REB-024` | adversarial corpus | symbolic-link parent, junction parent, terminal junction, dangling link, non-file target, chained target, lexical path in checkout, resolved target in checkout, short-name alias, case-variant alias, redirected temporary directory, relative and parent components, rootless path | Each returns its declared case identifier, before any interpreter is spawned and before any target validation |
| `REQ-REB-024` | junction predicate test | `mklink /J` parent with `is_symlink()` false and an independently observed mount-point reparse tag; a stubbed runtime without `pathlib.Path.is_junction`; and a stubbed runtime without either route | Both available routes refuse the junction parent; a runtime with neither route refuses rather than passes |
| `REQ-REB-024` | refusal-preservation test | every refusal each boundary produces at the base commit | No base-commit refusal is lost by the terminal-link relaxation |
| `REQ-REB-025` | identity fact test | POSIX venv, Windows ordinary file, and an environment-internal resolved target | `python_executable`, `python_entry_is_link`, `python_binary_position`, and `python_binary_sha256` all match independently computed values |
| `REQ-REB-025` | tamper test | interpreter link repointed, and binary bytes altered, between the boundary's observation and the identity observation | The boundary's own comparison fails and no passing proof is retained |
| `REQ-REB-025` | frozen-document test | every existing `docs/engineering/**/evidence/*-evaluator.json` and its recorded digest | Canonical bytes and recorded digests are byte-identical to the base commit |
| `REQ-REB-025` | additive-compatibility test | every consumer that validates a required identity field subset, plus the installed root validator and the dashboard publisher | The enlarged observation is accepted; the schema identifier is still `se-harness-runtime-identity-v3` |
| `REQ-REB-025` | privacy inspection | retained identity output for a resolved target outside every declared root | No absolute workstation path for the resolved target, no unrelated environment content, no credential material |
| `REQ-REB-026` | boundary registry check | every interpreter validation found in both runtimes | The registry matches exactly; an unregistered validation fails |
| `REQ-REB-026` | cross-runtime corpus | the declared corpus through both loaders on Windows and Linux | Identical outcomes; a divergence names the case and both outcomes |
| `REQ-REB-026` | bidirectional declaration check | a case added with no implementation; an implementation outcome absent from the declaration | Both fail |
| `REQ-REB-026` | import barrier check | the `repository_tools` import graph | Standard library and `repository_tools` only; no boundary imports another boundary's private link helper |

## Acceptance scenarios

### POSIX acceptance

1. A `python -m venv` environment outside the checkout, holding the exact released `se-harness`, passes the released-evaluator identity command, release bootstrap binding, predecessor preparation, predecessor assessment, predecessor publication, external-evaluator location in release qualification, and the governance-migration runtime probe.
2. The derived evaluator root equals the virtual environment in every one of those boundaries. No boundary reports the system prefix.
3. The retained interpreter origin normalizes against the environment root and preserves the `bin/python` remainder.
4. Repeating the run over the same immutable environment yields identical decision-bearing facts.

### Refusals

1. Each adversarial form in the matrix produces its declared case identifier from every boundary that receives an interpreter path.
2. Instrumentation proves no interpreter subprocess was spawned and no target validation ran for any refused form.
3. A junction parent is refused on Windows. The test asserts independently that `is_symlink()` is false for that parent and that its `lstat` result carries the reparse-point attribute with the mount-point reparse tag, so the case cannot pass through symbolic-link detection alone. Where the running Python also exposes `pathlib.Path.is_junction`, the test asserts it is true for the same parent and that both routes agree.
4. A runtime exposing neither `pathlib.Path.is_junction` nor the reparse-point `stat` constants refuses with the unavailable-predicate case rather than skipping the check. A runtime exposing only one of the two routes does not refuse for that reason; the test asserts each route in isolation reaches the same junction refusal.
5. A resolved target inside the candidate checkout is refused even when the lexical path is outside it.
6. No refusal is downgraded to a warning, an allowlisted diagnostic, or a maintenance-plane observation.

### Recorded facts

1. For a POSIX venv the observation reports a true terminal-link property, the outside-declared-roots position class, and a digest equal to the SHA-256 the test computes from the system interpreter's bytes.
2. For a Windows ordinary interpreter it reports a false terminal-link property, the within-expected-root position class, and a matching digest.
3. A boundary that expects a specific environment rejects a mismatched terminal-link property, position class, or digest before substantive validation.
4. An unreadable resolved target is refused rather than recorded with a null digest.
5. The `within-checkout-root` position class is unreachable through the rule; a test asserts the constant exists and that no accepted path produces it.

### Declaration and boundaries

1. The declaration parses under its schema identifier, rejects duplicate keys, rejects an unknown case identifier, and rejects a malformed corpus entry.
2. The declaration contains no executable code, no per-boundary waiver, and no allowlist; the test asserts the absence structurally rather than by inspecting prose.
3. Adding an unregistered interpreter validation to either runtime fails the registry check.
4. Changing one loader's outcome for one case fails the cross-runtime check with that case named.

### Preserved behavior

1. `repository_tools/predecessor_preparation.py` and `repository_tools/predecessor_assessment.py` produce the same accept/refuse outcome and the same normalized origin for every case they handled at the base commit.
2. `RID004`, `RID006`, and `MIG205` keep their identifiers, subjects, and triggering conditions.
3. The governance-migration contract document and every digest bound to it are unchanged, or the move is measured and recorded rather than assumed.
4. Root managed files, the installed root lock and configuration, released bytes, history, refs, tags, and public distributions are unchanged.

## Property and invariant tests

- Rule evaluation is a pure function of the supplied paths and observed filesystem state; it mutates nothing and opens no socket.
- First-refusal-wins holds: a path form yields the same case identifier regardless of which boundary evaluates it.
- Acceptance is monotone with respect to the base commit: every path accepted at the base commit is still accepted.
- Refusal is monotone in the other direction: every path refused at the base commit by a given boundary is still refused by that boundary.
- The environment root is a lexical function of the supplied path alone and never depends on the resolved target.
- Interpreter-path equality is decided lexically on both sides at every boundary.
- Recorded facts are deterministic for an immutable environment across runs, working directories, and platforms, apart from the platform-specific facts recorded separately.
- The digest read is bounded and occurs at most once per observation.
- Normalized retained origins match the declared origin pattern and contain no drive letter, backslash, or user directory name.

## Static and architecture checks

- Every registered boundary calls its runtime's loader; no boundary restates a declared refusal inline.
- No call site derives an environment root from a resolved interpreter target.
- No interpreter comparison resolves both sides.
- `repository_tools` imports only the standard library and its own package; `se_harness` does not import `repository_tools`.
- No module reaches into another module's private link helper as the definition of link safety.
- The declaration ships as package data and appears in the portable-release-surface list.
- The evaluator-evidence `origins` and `environment` field sets are unchanged, and the runtime-identity schema identifier is unchanged.
- Every prohibited pattern in `ARCH-REB-010` has a corresponding failing-case test.

## Security and privacy checks

Exercise symbolic links, Windows junctions, hardlinks, dangling links, link cycles, deep parent chains, short-name aliases, case-colliding paths, Unicode-confusable path components, oversized paths, redirected `TEMP` and `TMP`, a checkout mounted through a link, a resolved target inside the checkout, a non-file interpreter, an unreadable interpreter, and a malformed declaration.

Instrument subprocess creation to prove no interpreter runs before the rule accepts. Instrument imports to prove candidate modules do not load into a released-evaluator or predecessor process. Prove no refusal message, no retained identity output, and no bounded diagnostic contains file contents, credentials, package-index configuration, or unrelated environment values.

## Performance and resilience checks

- The ancestor walk, the single resolution, and the single bounded digest read are each performed at most once per observation; a counter test enforces it.
- A deep parent chain terminates at the filesystem root without unbounded recursion.
- A link cycle is refused rather than looping.
- Run focused tests plus the complete supported suite on Windows and Linux. Compare failure names against an independently captured baseline in a clean worktree at the base commit; the delta shall be exactly the tests added by this work order.
- Platform-unconstructable corpus forms are skipped explicitly with a recorded reason, never silently.

## Manual assessments

Quality, security, and repository owners shall review:

- the declared case list against `REQ-REB-023` and `REQ-REB-024`, item by item;
- the boundary registry against an independently produced inventory of interpreter validations in both runtimes;
- the before-and-after outcome table for all six boundaries, including the two whose behavior must not change;
- evidence that the declaration carries no waiver, exception, or allowlist;
- the recorded-facts privacy review for a POSIX resolved target;
- the frozen-document and bound-digest non-change evidence;
- the list of actions not performed.

## Evidence retention

Retain, under the work-order evidence path: the approved packet and preflight; the base commit and the independently captured base-commit test baseline with failure names; the changed-path manifest; the declared case list and its bidirectional comparison with the test-owned corpus; the boundary registry and the independent inventory it was checked against; the per-boundary before-and-after outcome table; the adversarial corpus results per platform with explicit skip reasons; subprocess and import instrumentation traces; the recorded-facts matrix with independently computed digests; the evaluator-evidence sidecar bytes and digests before and after; the bound-digest re-measurement for the governance-migration class and package data; the root managed, lock, history, ref, tag, and distribution non-change proofs; focused and full suite output for Windows and Linux; and the complete actions-not-performed statement.

A later VREC must bind the exact implementation commit, this verification contract, `WO-REB-021`, and the keyed evidence path. Passing tests, this contract, or a green check alone do not transition the work order and grant no assurance.

## Residual uncertainty

Windows cannot create symbolic links without privilege in the local development environment, so the symbolic-link half of the corpus is provable only where that privilege exists or on Linux; the junction half is provable only on Windows. Neither platform alone verifies `REQ-REB-024`, and the contract therefore requires both lanes rather than accepting a single-platform pass.

Short-name alias and case-variant behavior depends on filesystem configuration that the tests can observe but not guarantee on every host; those cases record the observed filesystem property alongside the outcome.

The declaration's own schema will need a governed change if a future case cannot be expressed as data. Whether the enlarged runtime-identity observation should eventually carry a distinct schema identifier is deferred, because the installed root validator accepts only v2 and v3; that deferral is recorded rather than resolved here.

## Amendment record

**Junction-predicate restatements, amended 2026-08-24 by the quality owner during
the implementation of `WO-REB-021`, in the same act that amended `SPEC-REB-011`
rule 4.** This contract restated the approved rule's `is_junction`-only predicate
in three places: the `REQ-REB-024` junction-predicate method row, refusal
scenario 3, and refusal scenario 4. Because `pathlib.Path.is_junction` exists
only from Python 3.12 while every supported lane pins Python 3.11, those three
statements were unsatisfiable as written — scenario 3 asserted a `Path` method
that does not exist on the running interpreter, and scenario 4 required a refusal
that the amended rule does not produce.

The three statements now describe the amended rule: the reparse-point `stat`
route is the predicate where `is_junction` is absent, `EPS011` is required only
where neither route exists, and where both routes are available the contract
requires them to be proven in agreement. This strengthens the verification
obligation rather than relaxing it — it adds the two-route agreement check and
the single-route isolation checks — and it changes no requirement, no pass
condition for any other row, and no evidence obligation.
