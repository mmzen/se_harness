+++
id = "SPEC-DST-020"
type = "specification"
title = "Four-mebibyte topology acceptance amendment"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-10-03"

[relations]
specifies = ["REQ-DST-062", "REQ-DST-063", "REQ-DST-064"]
+++

# Specification: Four-mebibyte topology acceptance amendment

## Scope

Raise the SE Harness compact-topology acceptance target from 524,288 to exactly 4,194,304 UTF-8 bytes, align the existing progressive-bundle definitions and tests, and preserve all other product, governor, integrity, publication, and release boundaries.

This is a capacity-headroom amendment to the bundle-v2 design selected by `ARCH-DST-010` and `ADR-DST-010`; it does not introduce topology sharding or a new schema.

## Actors and external systems

- Candidate source and package template define future installed product behavior.
- The independently installed public 0.5.0 evaluator continues to govern the repository root.
- Local Windows/default and Python 3.11 test lanes exercise candidate behavior.
- GitHub push and pull-request workflows expose exact branch and integration-history behavior.
- Accountable product, technical, assurance, repository, and release owners retain lifecycle decisions.

## Inputs

- Merged baseline `af0eaa0ff0b44f887a01278de821c9be5b7fc086`.
- Current observed graph: 539 artifacts and 1,944 relations.
- Current compact topology: 525,689 UTF-8 bytes.
- Existing target: 524,288 bytes.
- Existing `REQ-DST-055`, `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-017`, and `VER-DST-017` numeric references.
- Existing canonical candidate template and acceptance tests.

## Outputs

- Candidate distribution contract with `TOPOLOGY_ACCEPTANCE_BYTES = 4_194_304`.
- Aligned existing governing definitions naming 4,194,304 bytes while preserving their statuses and all noncapacity meaning.
- Focused assertions for the exact target, current repository, deterministic repeat generation, and integration-history evidence.
- Retained implementation evidence under `docs/engineering/harness-distribution/evidence/WO-DST-020-verification.md` after separate authorization.
- No active-root managed change, release artifact, or external mutation.

## State model

`draft amendment -> accountable approval -> released-evaluator start preflight -> candidate-only implementation -> local and hosted integration qualification -> implemented evidence -> candidate commit -> ready VREC -> assurance decision -> merge -> later aggregate release -> later supported root upgrade`

No state transition is implied by this specification.

## Behavioral rules

1. Define the candidate product target as the integer 4,194,304 in the canonical standard repository generator template.
2. Keep `topology_target_exceeded` equal to `topology_bytes > 4_194_304`; preserve its schema, name, boolean type, summary placement, and observational meaning.
3. Keep topology serialization, included fields, relations, findings, revision provenance, ordering, hashing, and manifest descriptors byte-for-byte unchanged except for values naturally caused by the governed repository artifacts.
4. Preserve every non-topology limit and the difference between hard generation bounds and the current-repository topology acceptance target.
5. Amend only the obsolete 524,288 numeric statements in `REQ-DST-055`, `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-017`, and `VER-DST-017`; preserve their existing approved scope, relations, decision history, and other text.
6. Add focused tests that assert the exact constant and that current repository topology is at or below it without replacing the existing deterministic/partitioning assertions.
7. Use hosted pull-request candidate-source execution as the integration-history observation; do not treat a green branch push as a substitute for a failing merge ref.
8. Keep the active root `scripts/generate_harness_dashboard.py` and schema-2 lock unchanged because they belong to the installed public 0.5.0 governor.
9. Prove the candidate package installs the 4 MiB target into a disposable standard repository while the verifier/governor runtime remains outside the checkout.
10. Do not change package version, build a promotable distribution, prepare a release record, or update the root governor under this work order.

## Error and recovery behavior

- Wrong target, partial definition alignment, root managed drift, unexplained repeat difference, or any failed required test stops implementation.
- A topology larger than 4 MiB remains generatable and observable for ordinary consumers, but fails this repository's acceptance assertion.
- Recovery before commit uses the reviewed candidate diff and ordinary Git history; no managed root is repaired from checkout bytes.

## Data and interface contracts

The only executable contract change is the candidate distribution constant:

```python
TOPOLOGY_ACCEPTANCE_BYTES = 4_194_304
```

All bundle schemas, JSON properties, resource paths, SHA-256 descriptors, content limits, CLI commands, and return-code semantics remain unchanged.

## Security and privacy properties

The amendment adds no input, output, dependency, origin, privilege, credential, persistence, network request, or publication path. Existing untrusted-content, path-containment, manifest integrity, same-origin, and disclosure properties remain mandatory.

## Performance and capacity

- Topology repository acceptance target: 4,194,304 UTF-8 bytes before compression.
- Current observed usage: 525,689 bytes, approximately 25.1% of the proposed target.
- Initial absolute headroom: 1,571,463 bytes.
- Shell, summary, per-document, and total-content limits remain 262,144, 262,144, 262,144, and 16,777,216 bytes respectively.
- Topology remains deferred until Overview or Lineage requires it.

## Observability

Generation summary continues to expose actual topology bytes, target, exceedance boolean, role counts/totals, largest resource, and manifest digest. Verification records branch, pull-request merge-ref, and merged-main observations when available.

## Compatibility and migration

Consumer repositories installed from public 0.5.0 retain the 524,288 observation until a later release and supported `harnessctl upgrade`. The candidate remains compatible because the bundle schema and behavior are unchanged. Historical generated bundles and evidence remain immutable.

## Examples and counterexamples

- Valid: candidate template uses 4,194,304; active public-0.5.0 root still uses 524,288 and passes doctor.
- Valid: a 600 KiB consumer topology generates and reports `topology_target_exceeded = false` under the future candidate package.
- Invalid: copying the candidate generator into the active root before release.
- Invalid: deleting provenance or relations to remain below the target.
- Invalid: increasing shell, summary, per-document, or total-content limits in the same change.
- Invalid: treating 4 MiB as a formal-repository validity or assurance threshold.

## Explicitly unspecified decisions

Implementation may choose focused test names and concise alignment wording. It may not choose another target, shard topology, change schemas, alter included data, update the active governor, or broaden lifecycle/release scope.

## Manual capacity revision — 2026-10-03

mmzen authorized the 4 MiB target and the bounded manual amendment after reviewing
the two-file correction and the affected definitions. This records the human's
exception to the selected 0.21.0 amendment procedure's unsupported-command stop;
it is not a revision operation performed by harnessctl. Lifecycle states,
original decision history and all noncapacity rules are preserved.

The exact accepted predecessor is the member `docs/engineering/harness-distribution/specifications/SPEC-DST-020.md` of
[accepted-predecessors.zip](../evidence/WO-DST-028/accepted-predecessors.zip),
SHA-256 `f868b0b35705b706ad99b1da3219e173a59c913daceb32cdee5e7fb1f098907e`. The
[amendment manifest](../evidence/WO-DST-028/amendment.json) links both versions
and retains the owner's instruction. Earlier work keeps its original Git-bound
definitions and evidence.

The current target is 4,194,304 uncompressed UTF-8 bytes. Measurements and
0.5.0/0.5.1 rollout statements from the earlier amendment describe its historical
context. New work uses selected released 0.21.0 and the checks in VER-DST-030
under WO-DST-028. All other payload budgets, complete topology data, integrity
checks and publication boundaries remain unchanged. RLS-SEH-032's approved
candidate and archives are not amended.
