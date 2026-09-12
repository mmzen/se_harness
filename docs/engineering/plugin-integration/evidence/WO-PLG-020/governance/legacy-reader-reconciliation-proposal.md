# WO-PLG-020: proposed legacy-reader qualification amendment

Status: **proposed, not approved or applied**. WO-PLG-020 remains `in_progress`; VREC-PLG-015 is not prepared. Supplement revision 2 has already been approved and implemented. This is a separate decision arising from a newly reproduced compatibility limit.

## Decision requested

Approve the four exact applicability amendments below: SPEC-PLG-020, ARCH-PLG-003 and ADR-PLG-003 as technical-owner, and VER-PLG-020 as assurance-owner. They distinguish rejection of installation/formal-artifact mutations from the older evaluator's existing ability to generate evidence and reports. This explicitly narrows an overbroad old-reader claim; it does not count the contrary observation as a passing refusal.

After approval, append the selected text while preserving original approvals/history; record the approval under WO-PLG-020; extend the real released-0.17 acceptance probes to cover the identified mutation interfaces and report/evidence boundary; and rerun the affected acceptance on the approved OS/Python/source/package matrix. These paths already fall within WO-PLG-020's approved scope. Approval does not mark the WO implemented or the VREC verified, authorize release/adoption, or accept a failed installation-state mutation test.

The alternative is to retain the literal current criterion and keep completion blocked while an owner selects a different compatibility design. Changing candidate 0.18 code cannot retrofit a lock check into the already distributed 0.17 executable.

## Reproduced observation

PR [#462](https://github.com/mmzen/se_harness/pull/462) implements the approved revision-2 scope at head `1e062e4db06b6e7131429db15b3d6b9876e600db`. CI tested merge candidate `5e9570d0d679ce551a1c436681de51193bc1e483`; their Git trees are identical (`1b3cea0d7eb536fc8b3d948382893387e2317839`).

The focused reproduction used the actual shared CI wheel, SHA-256 `ec2421f9562096e86f1a16c4117358e836541384f0dd32bbabec8a8357479985`, installed outside the checkout. That installed candidate created and migrated a disposable fixture. The fixture has a schema-4 binding and a synthetic draft artifact chain. Candidate `doctor` passed; both candidate and released-0.17 artifact validation reported `valid=true`, zero errors and zero warnings (nonblocking authoring advisories remain separately reported).

| Actual isolated command | Exit | Observed filesystem effect |
| --- | ---: | --- |
| Candidate 0.18 `doctor <fixture> --json` | 0 | None; schema-4 ownership accepted. |
| Candidate 0.18 `validate <fixture> --json` | 0 | None; artifact graph valid. |
| Released 0.17 `validate <fixture> --json` | 0 | None; artifact graph valid. |
| Released 0.17 `doctor <fixture> --json` | 1 | None; reports unsupported lock schema. |
| Released 0.17 `evidence <fixture> --artifact WO-LEG-001 --checkpoint handoff --json` | 0 | Creates the 286-byte handoff packet and its two parent evidence directories. |
| Released 0.17 `dashboard <fixture> --json` | 0 | Creates derived dashboard files/directories under `target/harness-dashboard/`. |

The retained raw argv also includes the isolated Python flags and a deterministic fixture-only `--rebound-at` value for evidence generation. That fixture timestamp records no real lifecycle decision.

Neither successful writer modified any pre-existing path. The lock, configuration, installed files, retained-skill absence, external packages and draft lifecycle metadata were unchanged. The result is an evidence/report-writing observation, not a demonstrated ability to modify installed ownership or exercise a lifecycle decision. It nevertheless contradicts OWN07's literal “Every writing path refuses before mutation” and the broad old-reader statements it implements.

Earlier probes with an incomplete draft graph are retained separately and do not establish the valid-graph result above. This focused counterexample was observed on Windows/Python 3.13.3; it is not relabeled as an unobserved Linux result. The existing matrix directly exercised released `doctor`, default-writing `init`, applied `upgrade`, and the unknown new command; it did not execute every old writing interface.

## Exact proposed appendix: SPEC-PLG-020

### Approved applicability: migration-unaware evaluator boundary

For PLG-OWN-012 and its old-evaluator failure row, rejection before mutation applies to installed-file or lock changes and creation or state changes of formal governance artifacts through migration-unaware evaluator interfaces. Each applicable interface MUST refuse a plugin-owned schema-4 target before those mutations and identify unsupported lock format or evaluator incompatibility as the cause. An unrelated input, lifecycle or policy refusal is not evidence of that boundary. No such refusal may be replaced by a usage error, a mocked authority failure, or an observation of a different interface.

Released 0.17 has a narrower observed boundary than rejection of every filesystem-writing command: artifact-graph inspection, evidence-packet generation and derived reporting do not universally consult the installation lock parser. Retained check-result generation is an additional source-inspection concern whose actual behavior remains to be separately probed; no dynamic result for it is claimed here. They may read a schema-4 repository or write their specific evidence/report outputs. This is an explicit compatibility limitation, not installation support or governing authority. An evidence/report command's successful exit MUST NOT be treated as proof that the old evaluator accepts the installed ownership format, can govern the target, or supplies matching evaluator-bound assurance.

The candidate MUST preserve the selected ownership binding and installed bytes through the operations it supports. The distinction above grants no exception for modification of the lock, installed files, formal artifact creation or lifecycle decisions by an incompatible evaluator. PLG-OWN-013 through PLG-OWN-028 retain their existing obligations.

## Exact proposed appendix: ARCH-PLG-003

### Approved applicability: old-reader compatibility

The Compatibility section's statement that schema 4 makes old released evaluators fail closed applies to the complete class of interfaces that modify installed files/the lock or create/change formal governance artifacts, as defined in SPEC-PLG-020 and VER-PLG-020. It is not a universal filesystem write barrier. Released 0.17 can still inspect an artifact graph and generate evidence/report outputs without accepting schema 4 as an installation format. Those outputs carry no inferred authority to govern a plugin-owned target. SPEC-PLG-020's explicit legacy-reader boundary and VER-PLG-020's separately observed interface census govern this distinction.

## Exact proposed appendix: ADR-PLG-003

### Approved applicability: consequence of the versioned-lock choice

The selected schema-4 design and default schema-3 behavior remain in force. The decision drivers, option comparison and Consequences statements about old readers are qualified as follows: a versioned lock makes migration-unaware installation readers and applicable installed-state/formal-artifact mutation interfaces reject the unsupported format; it cannot make already distributed code consult a lock on paths that never did so. Released 0.17 evidence/report generation and artifact-graph inspection remain an observed exception to universal old-reader refusal. This exception authorizes no ownership mutation, lifecycle decision, evaluator adoption, release or native-host readiness claim. Acceptance MUST retain the contrary observations and apply the precise boundary in SPEC-PLG-020 and VER-PLG-020 rather than describe all old commands as refused.

## Exact proposed appendix: VER-PLG-020

### Approved applicability: OWN07 interface census and report boundary

This appendix supersedes only OWN07's unqualified “Every writing path” and universal read-only-refusal wording. Test the real isolated released 0.17 executable against a valid schema-4 fixture and retain a version check, syntactically valid argv, actual process status, diagnostics and complete before/after snapshots. Enumerate every public interface and writing mode that can modify installed files/the lock or create/change formal governance artifacts, including the applicable installer, scaffolding, artifact creation, transition/decision/risk, verification capture and release preparation interfaces. Trace shared direct/delegated entry points separately and identify any coverage inference. Every applicable protected interface MUST refuse before its mutation with an unsupported-lock or evaluator-incompatibility diagnostic. Use a valid fixture for that interface or otherwise prove that the compatibility check caused the refusal. An unrelated lifecycle/input refusal, parser usage error or candidate-only mocked guard is insufficient evidence.

Separately exercise artifact-graph validation, evidence generation, retained check-result generation and derived reporting. Record their actual refusal or successful output generation. Successful generation of the specifically observed evidence/report output may satisfy this boundary observation only when snapshots prove that pre-existing installation/configuration/lock bytes, formal artifact metadata and external provider bytes remain unchanged. It is not a passing unsupported-format refusal and MUST NOT be reported as installation compatibility, governing readiness or matching evaluator-bound assurance. Unexpected additional writes or changes remain failures.

Run the expanded OWN07 selection in the already required Python 3.11 smoke and Python 3.13 full source/package observations on Ubuntu and Windows. Preserve the original four-probe results and the newly observed contrary results; do not rewrite them. All other OWN cases, regression/package requirements, source/package authority distinctions, unavailable-mechanism rules and exact-candidate evidence obligations remain unchanged. Completion and VREC preparation remain pending until the amended observations and existing gates pass.

## Why another decision is required

The approved [verification contract](https://github.com/mmzen/se_harness/blob/1e062e4db06b6e7131429db15b3d6b9876e600db/docs/engineering/plugin-integration/verification/VER-PLG-020.md) currently requires every writing path to refuse. The [WO decision envelope](https://github.com/mmzen/se_harness/blob/1e062e4db06b6e7131429db15b3d6b9876e600db/docs/engineering/plugin-integration/work-orders/WO-PLG-020.md) says: “Do not choose a new owner decision, weaken a refusal, widen the catalog, or silently add another installer mode.” Revision 2 approved CI/CLI applicability and ten paths; it did not approve this new compatibility limitation. The executor therefore cannot apply this narrowing or declare OWN07 satisfied without the selected technical and assurance decisions.

The accepted C10/C11 limitation remains a separate unchanged decision. No current checkout migration, plugin installation, native-host activation, public release or WO-PLG-009 connection is proposed here.

## Retained review material

The [raw evidence archive](WO-PLG-020-legacy-reader-evidence.zip) contains the original probes, the final valid-graph observations and fixture inputs, raw changed-file bytes, scripts, and a verified member-hash manifest. Virtual environments and distribution files are excluded; the exact final wheel identity is retained. Archive SHA-256: `59d0edc2a8e602416b7cdcc671cc673cf68fecdae25ff785a313b831884172f7` (2,966,612 bytes; 248 hashed members plus manifest). See the [archive index](WO-PLG-020-legacy-reader-evidence-index.json).

An independent review checked the final valid-graph stream hashes, filesystem deltas and affected definition scope. The proposed test wording requires compatibility-specific refusals and leaves unobserved interfaces pending. This review is not an assurance decision.
