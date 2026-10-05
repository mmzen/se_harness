# Corrected evaluator 0.22.1 and plugin 0.2.6 qualification

The approved transition correction passes source, installed-package and native
CLI checks. Release preparation remains incomplete. WO-RLS-040, WO-RLS-041 and
WO-RLS-043 remain in progress. No final aggregate VREC or RLS is ready, and this
review does not request verification or merge.

## What changed

An unrelated draft may name evidence that does not exist yet. The transition
planner now retains that absence and rechecks it before apply. Required evidence
still has to pass the selected action's gates. Unreadable files, directories and
unsafe links remain errors. Appearance, disappearance or changed bytes invalidate
the plan before writes. Selected writes and rollback behavior are unchanged.

The implementation adds one small read helper and reuses the existing snapshot,
plan and apply boundaries. Review found no new policy engine, lifecycle edge,
CLI option, schema, dependency or generalized framework. The six new tests cover
the observed defect and distinct safety boundaries. Existing stale-input and
rollback tests remain active.

mmzen's correction approval and exact manual linked REL-SEH-035 amendment were
applied. [The amendment record](amendment.json) preserves the actual response and
reviewed hashes. [The previous accepted contract](REL-SEH-035-accepted-before.txt)
and its lifecycle history remain intact. The release now includes WO-RLS-043 and
VER-RLS-004 in addition to its previous approved membership.

## Exact qualification inputs

- Tested source: `061307929c94314ccd2beb4a53f174e536fceba8`.
- Later CI review head: `82c8c5a78a5b44cfbafb4b96514ea4be83905e7f`.
  Its only intervening change refreshes the required pre-action evidence header.
- Released governor: 0.22.0 in its separate environment; candidate 0.22.1 runs
  only as the system under test.
- Wheel SHA-256: `41aa3f93f126c1f7cbb9efb6b31d5bb3ad755358e37069699d21bfee9be39475`.
- Sdist SHA-256: `62dc183f62eb75d5c76ba08e4a4d93b54af601bbb461f6b50105c9c60ff097d9`.
- Payload SHA-256: `0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff`.

[The corrected bundle](corrected-bundle.json) and
[package identity](corrected-package-identity.json) bind the complete inputs.
These are preparation qualification identities, not a final release binding.
Final capture must use a clean, eligible candidate and matching qualification.
The earlier failed wheel and its observations remain historical evidence.

## Observed checks

| Check | Result |
| --- | --- |
| Windows full-scale source suite, Python 3.14.6 | Exit 0; 1,293 tests, 23 reported skips. |
| Ubuntu full-scale source suite, Python 3.12.3 | Exit 0; 1,293 tests, 2 reported skips. Linux executes the new unsafe-link case skipped on Windows. |
| Distribution and CLI smoke | Passed; 22 distribution records. |
| Pinned recipe replay, CPython 3.11.9 | Two independent producers produced byte-identical wheel and sdist archives. |
| Windows/Linux installed wheel and sdist | Identity, initialization, doctor and validation passed. |
| Installed HAG corrections | Actual-identity decision probe and standalone draft-admission normal/refusal cases passed on both platforms. |
| Exact original transition defect | Corrected Windows/Linux CLI probes pass without creating the absent draft evidence or changing the unrelated draft. |
| Upgrade from 0.22.0 | Two real runs per platform passed with the same semantic digest. |
| Dashboard | 4 MiB boundary tests pass; actual topology is 2,172,957 bytes with 2,021,347 bytes of headroom. Repeated bundles match. Eleven preserved predecessor revisions match their recorded hashes. |
| Plugin assembly | Windows/Linux staging and check-stage pass. Expanded files, metadata and inventories match. Compressed ZIP bytes differ across runtimes; the exact Windows staged bytes are identified. |
| Codex CLI 0.159.2 | Native startup above a clone, activation, manual/automatic compaction, resume, parallel selection, switch/clear and explicit missing-checkout gap pass. |
| Claude Code 2.1.273 | The corresponding native events and selection boundaries pass with the corrected package. |
| Claude context bound | Adapter replay delivers complete instructions at 9,989 and 10,000 units and an explicit gap at 10,001. This is not a native desktop or arbitrary-filesystem-path claim. |
| PR checks attached to 82c8c5a | Required validate, source/package, upgrade, integration-package, predecessor and CodeQL jobs pass. PR merge-checkout evidence is distinct from the C3 source tests above. |
| Manual publication rehearsal 37252846313 | Candidate replay, historical release-record replay and complete-delivery/recovery jobs pass. The historical record leg is RLS-SEH-032, not a new 0.22.1 record. |

The manual candidate replay selects review head 82c8c5a. Neither its build nor
PR merge-checkout results are relabelled as a build or test of 0613079. The
retained local pinned replay qualifies 0613079 separately.

## Native workflow results

Each fixture retains a new unapproved proposal, then executes its separate
synthetically approved work order. Independent byte and Git comparisons confirm
exact note content, one start and completion, preserved accepted definitions,
bounded changes, a clean local commit, and an empty local remote. Neither test
host creates a real PR or supplies a human verification decision.

| Host and fixture | Independent assessment | Local synthetic candidate |
| --- | --- | --- |
| codex, successor | Passed | `56db17fc2f74bf2c8489371f152034c027dee262` |
| codex, legacy | Passed | `719bd83cbc73e36101ba44194bce09780c41a84e` |
| claude, one | Passed | `180a33237b72412cc3964bf1356e9f978c16406e` |
| claude, two | Passed | `eb0ff43ba30e3a6b5c7f1975f902cdb5da6279fc` |

The original Claude draft remains byte-identical (SHA-256
`63e9d2834d5638016bcc97702b3e9828c0a2334380cee02fa12d0a5a78bd5a30`).
Its absent evidence declaration was preserved. The only test-setup change before
continuation was a supported upgrade of the fixture lock to the corrected wheel;
the original and updated baselines and exact changed paths are retained. The
second-checkout cycle separately confirms continued selection and handoff.

These are real CLI runs with individually reviewed tool requests. No saved host
permissions, real credentials or normal workstation profiles were changed.
The disposable Codex profile is restored after qualification.
The Codex fixture label `legacy` is a historical helper name; both workflow
fixtures use 0.22.1. Distinct 0.20.0 selection is covered by the boundary traces.

## Failures and limitations

Original failures remain in their existing evidence. This includes the initial
native transition crash, Windows/Linux reproductions, test-fixture corrections,
stale evidence-binding refusal, and prior environment/command failures. Native
read/command recoveries are retained with their successful results. No failed or
skipped operation is counted as a pass.

Claude's initial declared scope checks listed only the note and selected work
record. The required later Git-derived handoff and independent comparison cover
the complete change set, including the transported draft and evidence. The
initial caller declaration alone is not treated as proof of completeness.

The earlier Claude long-path report concerns the combined instruction-context
limit. The boundary replay above assesses that limit only. Actual native tests
use the recorded fixture paths. Hosted service behavior is outside this release;
no hosted service scenario ran.

## Remaining release criteria and next work

1. Codex Windows desktop delivery remains unverified. CLI results do not satisfy
   that criterion, and this correction approval accepts no omission.
2. The current PyPI account-side Trusted Publisher binding remains unconfirmed.
3. The [reviewed pypi environment change](../WO-RLS-040/provider-configuration-proposal.json)
   still needs separate authority. It removes only the redundant reviewer;
   provider settings have not changed.

Until these are resolved, keep qualification pending. Then finalize the exact
candidate and plugin staging commit, retain matching qualification, record
implementation completion through the released evaluator, and prepare the one
aggregate VREC. Publish the ready review before asking for human verification.
Prepare the exact release record and frozen complete-delivery plan afterward.
Merge, the complete-release decision and adoption remain separate.

## Evidence

- [Runtime archive](corrected-runtime.zip) and [byte index](corrected-runtime-index.json).
- [Native archive](corrected-native.zip) and [byte index](corrected-native-index.json).
- [Pinned build replay](corrected-build-replay.json).
- [Original failure and review](../WO-RLS-041/correction-review.md).

Archives retain actual commands, working directories, runtimes, outputs, exit
codes, identities, meaningful failures and test helpers. They exclude credential
stores and host profiles. Original bound evidence has not been overwritten.
