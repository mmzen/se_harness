# WO-SHB-002 Implementation Evidence

Date: 2026-08-15
Lifecycle: provisional implementation evidence; not a VREC, release decision, publication, or governor promotion

## Scope and authority

The repository owner approved `WO-SHB-002` and explicitly instructed implementation. This record covers the resulting source, package, migration, workflow, upgrade-protection, and local acceptance evidence. It does not authorize a commit, verification transition, release, publication, root reconciliation, or governor promotion.

The selected current governor remains release 0.2.1, wheel SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`, as declared by `.self-hosting/governor.toml`. Development started from commit `5d154448295e6a46cb75993d52bf5fd601dec817` on `work/WO-SHB-002`; that commit does **not** contain this implementation and is recorded only as the baseline. The enclosing candidate commit cannot contain its own Git object ID; its exact identity must be recorded by the subsequent commit-bound acceptance manifest and VREC preparation.

## Implemented boundary

- Added a shared fail-closed `consumer`, `self-hosting`, or `ambiguous` classifier and the exact protected set `.engineering-harness.toml` plus `.github/workflows/engineering-harness.yml`.
- Changed normal self-hosting upgrade planning to report lock-matching controls as `protected`; a missing or mismatched protected control blocks every write. Ordinary consumer planning and application remain unchanged.
- Added plan-first `harnessctl reconcile-governor`. It runs only for the exact implementation repository under the currently selected external governor, requires an authorized work order, inspects an exact target wheel as ZIP data without importing target modules, and accepts an immutable full commit, release record, version, and wheel digest.
- Added a versioned data-only migration manifest with release-managed, repository-identity, and repository-policy ownership. Safe defaults are typed; decision-required values must be supplied explicitly; extension namespaces are preserved only when declared.
- Added release-owned self-hosting workflow material. Reconciliation selects the self-hosting role, rejects generic YAML merge and unrecognized local deltas, and limits its transaction to the descriptor, configuration, self-hosting workflow, lock, and bounded recovery metadata.
- Added rollback and recovery behavior for interrupted replacement boundaries and checks current bytes immediately before apply to prevent stale-plan application.
- Added `harnessctl accept-candidate`, which installs an exact wheel into a fresh environment, invokes installed behavior outside the checkout, runs the ordered black-box scenario contract, detects checkout mutation, and emits canonical JSON only after every scenario passes.
- Kept `templates/repository/standard` as the sole consumer installation profile. The three self-hosting release assets are package data under `share/se-harness/self-hosting`, not a second public repository template.
- Updated the self-hosting operations guide, repository context, command reference, development note, domain index, feature contract, and focused tests.

## Protected-control evidence

Before the correction, diagnosis of the root plan classified both repository-specific controls as consumer-template `update` actions. No apply was performed. With the corrected implementation, the same read-only command reports:

```text
protected  .engineering-harness.toml
protected  .github/workflows/engineering-harness.yml
summary: 33 files, 31 unchanged
```

`harnessctl doctor .` passes and explicitly reports both files as `repository-specific self-hosting control` while retaining their managed-integrity checks. Start preflight for `WO-SHB-002` passes in `in_progress` state.

Current protected and governor-control hashes are:

| Path | SHA-256 |
|---|---|
| `.engineering-harness.toml` | `0ed769cd5cfad1047ec5bca805b6ad3f69af946dadf1ba5920182b13cee4e6af` |
| `.github/workflows/engineering-harness.yml` | `d2001d3b6569cf3c0605aac4170edef04bb9a8596d7532ddf5ebb7d9f7ccead8` |
| `.engineering-harness.lock` | `1c5015d33474513fbc6e6b1452af1effa97cce208ec9e719a3a93438706576bb` |
| `.self-hosting/governor.toml` | `00e34f52be9bb4e3b9032e69a294afe62077c253235bff1bc4d574b736d86130` |

Normal upgrade did not write or refresh any of these files. Actual root reconciliation remains out of scope.

## Migration and workflow evidence

The non-executable target contract and role-specific workflow hashes are:

| Material | SHA-256 |
|---|---|
| `self_hosting/governor-migration.toml` | `1186e4dfb844993ae9270999983dcfb996c211fb5118d97c8570e4f1508bffe8` |
| `self_hosting/engineering-harness.yml.tpl` | `1798781352f33260d7b9930c3c346db5b7bcc9fffaab97794c94ac1243a11a09` |
| `self_hosting/self-hosting-governor.yml` | `4207c62360f6a3709beba0de3456f7ddeb27851cd1f6889611d08c4d6cf93080` |
| `.github/workflows/self-hosting-governor.yml` | `4207c62360f6a3709beba0de3456f7ddeb27851cd1f6889611d08c4d6cf93080` |

Focused tests cover exact target resolution, target-code non-execution, field ownership, policy preservation, safe defaults, explicit decisions, extension namespaces, self-hosting workflow selection, local-delta conflicts, bounded destinations, pre-apply byte revalidation, and interruption rollback. The first publication of this material remains candidate evidence; it cannot reconcile or independently govern its own creation release.

## Source and package qualification

Complete source suites passed from the checkout:

- Python 3.14.6: 159 tests in 50.453 seconds; three conditional skips; zero failures.
- Python 3.11.9: 159 tests in 51.853 seconds; three conditional skips; zero failures.

Formal artifact validation passed with 294 artifacts, zero errors, and 38 pre-existing legacy/location warnings. `git diff --check` passed; its only output was the repository's Windows LF-to-CRLF conversion warnings.

The wheel build also emitted the pre-existing setuptools deprecation warning for the TOML-table form of `project.license`, whose announced support deadline is 2027-02-18. It did not affect this build and is unrelated to the authorized self-hosting change, but should be handled under a separate bounded maintenance work order.

An explicitly non-promotable wheel was built from the uncommitted working tree for package inspection only:

- wheel: `se_harness-0.2.2-py3-none-any.whl`;
- SHA-256: `cd05e2df989ff4750cef7e17da2a4ffb4e6f384a24f47676dc07cf9da42855e2`;
- packaged modules include `self_hosting_policy.py`, `governor_reconciliation.py`, and `candidate_acceptance.py`;
- packaged self-hosting data contains exactly the migration manifest, workflow locator template, and role-specific reusable workflow;
- no `templates/repository/self-hosting` profile exists.

The wheel was installed without dependencies into fresh Python 3.14 and Python 3.11 virtual environments outside the checkout. In both environments the installed `harnessctl` exposed `reconcile-governor` and `accept-candidate`; fresh consumer `init` and `doctor` passed. The Python 3.11 environment resolved Python 3.11.9 and `se-harness` 0.2.2. The acceptance interface requires the caller-selected candidate SHA-256, reads and checks the candidate bytes once, and installs a private snapshot of those bytes; target reconciliation likewise inspects its checked in-memory target bytes rather than reopening a mutable path. These are candidate-package observations only.

## Adversarial and recovery coverage

Automated tests reject or recover from:

- partial, malformed, or spoofed self-hosting identity;
- missing or modified protected controls and mixed protected/ordinary updates;
- malicious target modules, corrupt wheels, unsupported protocols, invalid hashes, and mutable or incomplete target identities;
- duplicate, unknown, mistyped, lossy, ambiguous, or decision-required policy fields;
- consumer-workflow substitution, generic YAML merge, missing required roles, and undocumented local workflow deltas;
- destinations outside the four declared controls plus bounded transaction metadata;
- target changes between planning and apply;
- simulated interruption at replacement boundaries, restoring a complete prior state;
- candidate checkout ownership of the independent runner, candidate import leakage, missing scenarios, nonzero required commands, checkout mutation, and non-canonical temporary paths.
- wrong candidate-wheel digests, oversized wheel or checkout inputs, and checkout symlinks that could escape or destabilize the bounded snapshot.

## Pending commit-bound and external gates

The canonical `accept-candidate` manifest is intentionally not generated inside this evidence-bearing candidate. A commit cannot contain an acceptance manifest that truthfully names its own not-yet-created object ID. After this candidate commit exists, the exact wheel must be rebuilt or deterministically associated with that commit, exercised by the released verifier contract, and recorded with its real full commit and wheel digest in later governance evidence.

The following remain pending before a VREC can be prepared or independently transitioned:

- exact candidate-commit source and package identities;
- commit-bound canonical replay manifest and repeatability comparison;
- review preflight over the final committed candidate/evidence boundary;
- hosted GitHub `governor`, `candidate-source`, and `candidate-package` results;
- accountable manual review of authority wording, role separation, policy ownership, workflow permissions, and retained replay sufficiency.

No root reconciliation, push, pull request, VREC capture or transition, release record, tag, GitHub Release, PyPI publication, deployment, or governor promotion is authorized or claimed by this evidence. The enclosing candidate commit records implementation only.

## Residual risks

- Local tests cannot prove GitHub runner permissions, reusable-workflow resolution, or all platform-specific process and filesystem behavior.
- The first released reconciler and acceptance runner remain candidate-owned evidence until immutable publication and a separate promotion work order select them as governor.
- Future schema jumps that the selected governor cannot parse require a compatible bridge release; the implementation fails closed rather than executing target code.
- The recovery transaction is tested with injected Python-level failures; operating-system termination at every filesystem durability boundary remains platform-dependent and must be challenged in hosted qualification.
