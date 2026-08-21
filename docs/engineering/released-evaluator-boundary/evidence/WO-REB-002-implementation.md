# WO-REB-002 Implementation Evidence

Date: 2026-08-21

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, deploy, or authorize `WO-REB-003`.

## Implemented boundary

One shared guard now runs inside every public installed-root mutator before its first write. The registered operations are:

- `upgrade --apply` through `installer.apply_changes`;
- non-dry-run `scaffold-domain` and `create-artifact`;
- `renumber-artifacts --apply`;
- `capture-verification`;
- `prepare-release`; and
- a low-level installed-root apply invoked outside initial `init` or first adoption.

The guard requires schema 3 for ordinary mutation, exact config/lock version agreement, exact installed payload agreement, the locked archive digest when present, one external environment for the interpreter, package, templates, and launcher, disabled user site, absent `PYTHONPATH`, and checkout exclusion. Upgrade apply additionally requires PEP 610 identity for already-selected wheel bytes and a freshly recomputed upgrade plan. Release preparation requires the lock's wheel name and SHA-256. Stable failures use `MG001` through `MG006` and retain the underlying bounded `RID*` subject where applicable.

Candidate source, editable or foreign origins, schema-2 ordinary mutation, stale upgrade plans, payload/archive mismatch, entry-point substitution, enabled user site, `PYTHONPATH`, and checkout contamination fail before target writes. `init`, first adoption, dry runs, plans, doctor, validation, inspection, identity, preflight, and dashboard generation retain their existing non-authoritative boundaries.

## Evaluator evidence and readiness binding

`capture-verification` and `prepare-release` create canonical compact UTF-8 JSON using schema `se-harness-evaluator-evidence-v1`, then bind its repository-relative path and lowercase SHA-256 in the ready VREC or RLS. Evidence contains only:

- the released-evaluator role, version, payload manifest/digest, and paired archive identity;
- interpreter, module, distribution, template, and entry-point paths normalized below `<evaluator-root>`;
- Boolean isolation, user-site, `PYTHONPATH`, entry-point, and checkout-exclusion results; and
- an empty ordered diagnostic list for authoritative evidence.

The package parser, candidate standard validator, dashboard publisher, and release publisher reject duplicate keys, unknown fields, noncanonical bytes, unsafe or traversing paths, absolute origins, invalid sizes or hashes, candidate roles, contaminated environment facts, missing ready-release archive identity, changed evidence bytes, and ready-record mismatch with the current lock. Released or verified historical records preserve their captured identity across later evaluator upgrades. Only the explicit immutable release allowlist `RLS-SEH-001`, `RLS-SEH-002`, and `RLS-SEH-004` through `RLS-SEH-007` may omit the new binding. Publication replay validates retained evidence at main head against the lock at the release integration commit.

The candidate standard also owns a bounded `.gitattributes` fragment that forces evaluator-evidence JSON to LF on checkout, preserving canonical bytes and the record-bound SHA-256 on Windows, Linux, and macOS.

## Zero-write and negative evidence

`tests/test_mutation_guard.py` factors the matrix through the one guard and separately proves every registered public mutator reaches it before mutation. The test suite injects:

- missing or legacy lock, config/lock version mismatch, missing upgrade archive, and missing release archive;
- `RID002`, `RID003`, `RID006`, `RID008`, `RID009`, `RID010`, `RID021`, and `RID022` runtime failures;
- candidate role, host-absolute and `..` origins, noncanonical JSON, duplicate keys, and contaminated Boolean evidence; and
- an unregistered operation and a caller-supplied stale upgrade plan.

For all seven registered operations, the test compares recursive path, kind, link-target, and file-byte snapshots after injected rejection. Every before/after map is identical.

A separate real candidate-source attempt against the disposable final schema-3 consumer returned exit `2` with `MG005` (`RID003`, `RID004`, `RID009`, and `RID022`). Its recursive target-manifest SHA-256 was identical before and after:

`442bbb173881ea4a2edf4b9aef4ff9eca485e4880587acd97d13b40086909f17`

Publisher fixtures additionally reject an absent binding, changed evidence bytes, evidence/lock mismatch, unsafe evidence, and malformed identity. They preserve immutable release replay after a later evaluator lock upgrade while still detecting current-head evidence mutation.

## Positive disposable candidate-package evidence

This is candidate evidence only, not released-evaluator authority for the real checkout. A wheel was built outside the checkout, installed from exact local bytes in a new external virtual environment, and observed through PEP 610:

- wheel: `se_harness-0.5.0-py3-none-any.whl`;
- wheel SHA-256: `744af98dddb95b1cf82654dcba023dd6b85e73914f3c9de4092e432b625b888f`;
- installed payload manifest: `se-harness-installed-payload-v1`;
- installed payload SHA-256: `6b31f7d7182b841780b539ea503915cf40faea88f2bfc35d73f69575a17f5871`;
- external identity: PASS with no diagnostics, disabled user site, absent `PYTHONPATH`, exact archive agreement, resolved launcher, and checkout exclusion.

The final disposable evaluator successfully executed upgrade apply, verification capture, and release preparation; preceding package replays of the same candidate implementation also exercised domain scaffold, artifact creation, and renumber apply. The installed candidate validator then passed the resulting 24-artifact graph with zero errors and warnings. Ready release `RLS-REB-903` bound canonical evidence SHA-256 `0e8cf22defb33d453106b75af4ae2f0265e1b0682036e6d271b3f535c96f9b15`; its JSON contained only normalized `<evaluator-root>` origins and the exact payload/archive identity above.

## Released-evaluator and regression checks

The exact public 0.5.0 evaluator remained outside the checkout. Its previously reconciled public wheel SHA-256 is `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.

- External released-evaluator identity: PASS with no diagnostics, external interpreter/package/template/entry-point origins, disabled user site, absent `PYTHONPATH`, and checkout exclusion.
- `harnessctl doctor <checkout>` from that evaluator: PASS for every managed and distribution item.
- `harnessctl validate <checkout>` from that evaluator: PASS; 565 artifacts, 0 errors, and 44 existing maintenance warnings.
- `harnessctl preflight <checkout> --work-order WO-REB-002 --phase review`: PASS with the approved REB manifest.
- `python -m unittest discover -s tests -p "test_*.py"`: PASS; 298 tests, 4 skipped.
- Focused mutation, provenance, publication, release-orchestration, documentation, and lifecycle suites: PASS.
- Candidate standard validator tamper, current-lock, historical-lock-rotation, and missing released-binding scenarios: PASS.
- `git diff --check`: PASS.

## Changed implementation surface

- Guard and evidence: `se_harness/mutation_guard.py`, `se_harness/evaluator_evidence.py`.
- Mutators: `se_harness/installer.py`, `se_harness/artifact_layout.py`, `se_harness/renumber.py`, `se_harness/provenance.py`.
- Validation and replay: candidate standard artifact validator plus `.github/scripts/publish_dashboard.py` and `.github/scripts/publish_release.py`.
- Contract and operator material: candidate VREC/RLS templates, candidate workflow policy, bounded `.gitattributes` fragment and package surface, README, installation guidance, and CLI reference.
- Tests: common trusted-authority fixture; dedicated mutation-guard coverage; authoring, renumbering, provenance, publication, lifecycle, instruction, and architecture regressions.

The installed root's released 0.5.0 managed copies were intentionally not replaced with candidate templates. The exact released evaluator therefore continues to report root integrity PASS.

## Remaining lifecycle work

- No commit was created for `WO-REB-002`.
- No commit-bound VREC for `WO-REB-002` was prepared or verified.
- No real release record, root evaluator upgrade, tag, push, pull request, publication, or deployment was performed.
- `WO-REB-003` remains draft and none of its conflict-inspection or recovery-rehearsal scope was implemented.
- Because commit-bound verification is `required`, the next accountable action is review and separate authorization of a clean candidate commit for `WO-REB-002`; only after that commit may an authorized actor prepare its ready VREC.
