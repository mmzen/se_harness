# Release qualification — candidate 6fa4d1a6

**Final qualification is blocked by R23-REHEARSAL-001.** The existing instruction findings remain open, and Codex Windows desktop remains deferred and unverified. No final VREC or release record has been prepared from this candidate.

Candidate: `6fa4d1a645660cd8022dfc5c3ee7ba35bda3d162`. Earlier native-qualified source: `bb0890045f462343ecae66ca30b20b06cf6e8ae6`. The later review commit contains only release-domain evidence, index updates and draft WO-RLS-055. It does not replace this candidate or change product code. Released evaluator 0.22.1 remains the governor.

## Observed checks

| Check | Observation |
| --- | --- |
| Windows source suite | Exit 0; 1,339 tests, 24 skips; 353.003 seconds in the runner. |
| Linux source suite | Exit 0; 1,339 tests, 2 skips; 70.301 seconds. CI tested `a261ddc0d17ad622cd4fea2e56b9fc9074846d69`; its complete tree equals candidate C. |
| Pinned release build | Two independent producer runs produced byte-identical wheel and sdist. Manual GitHub candidate replay produced the same complete bundle manifest. |
| Installed packages | Windows wheel and exact index-selected sdist passed. Linux wheel/sdist and released independent verifier passed. Direct archive-path PEP 610 sdist installation is not claimed. |
| Portable plugin checks | 47 tests, 2 skips, exit 0. Exact local staging succeeded; no marketplace review ref or public ref was pushed. |
| Real upgrade rehearsals | Two Windows runs passed with the same semantic digest `32f0ab2bff6808f3f85b96adaa63bea588efff7f372fafe83a435cb5c13efb1c`. PR Linux/Windows upgrade checks also passed. |
| Private hosted combination | Fresh exact packaged client walkthrough, live boundary checks, restart and restore passed. Command-level expected refusals remain in evidence. No deployment or public service is claimed. |
| PR CI at candidate C | 17 successful checks; 2 intentionally skipped rehearsal legs. Skips are not passes. |
| Required manual rehearsal | Candidate replay and simulated complete-delivery/recovery passed. Historical RLS-SEH-033 qualification failed before build: `approved documentation differs: README.md`. Overall run failed. |
| Draft WO-RLS-055 | Released validation: 2,015 artifacts, zero errors, 63 warnings. All planned paths covered; the work order remains draft. |

## Exact identities and reuse

Wheel SHA-256: `b6d654c8543e2c665550dbe346dae53415d98807d2c8bfc1383125c0a180cd87`.
Source archive SHA-256: `de30c5299cb294e2bd285268572226f4c70c38712ba4e1a8770c097d385d2194`.
Hosted combination: `sha256:395fcb39130c32635102f9a8ba12852701a31649963081592b7d112a030aa97a`.

The retained [source/package comparison](candidate-6fa4d1a6-source-package-reuse-comparison.json) checks all changed source paths, all 127 expanded wheel members, plugin inventories and unchanged historical records/evidence. Hooks, scripts, resources, native fixtures and criteria are unchanged. Plugin archive/inventory and bundled archive provenance differ and remain explicit.

The [service comparison](candidate-6fa4d1a6-service-runtime-reuse-comparison.json) records equal expanded server runtime and dependency identities. Image/configuration/archive identities differ; fresh packaged walkthrough, boundary and recovery checks qualify those inputs. Historical native content, lifecycle, graph-read and delivery observations are reused only for unchanged inputs and remain at source `bb089004`; they are not described as fresh runs on C. No old failure becomes a pass.

## Open items and next authority

| Item | Current treatment | Follow-up |
| --- | --- | --- |
| R23-NATIVE-010 | Open. Separate Codex read-only trial explained before its communication-policy read. Functional reads passed. DEC-RLS-010 carries this instruction finding for this release only. | Correct and requalify before claiming the criterion passes; mmzen owns follow-up. |
| R23-NATIVE-011 | Open. Both new-work draft proposals omitted generated verification destinations; they remain unapproved drafts. Separate seeded execution does not repair them. Same DEC-RLS-010 limit. | Correct drafting guidance/behavior and rerun the affected case; mmzen owns follow-up. |
| Codex Windows desktop | Not run / unverified. DEC-RLS-011 records mmzen's release-only deferral and RISK-RLS-009. | Revisit before the next plugin release or a desktop support claim. CLI results are not desktop evidence. |
| Duration/context observations | Open improvement items; missed goals and unavailable metrics remain recorded. | Separate performance work; no new acceptance threshold inferred. |
| R23-REHEARSAL-001 | Open and blocking final qualification. Not covered by DEC-RLS-010/011. | Review [WO-RLS-055](../WO-RLS-055/preparation-review.md); implement only after approval and rerun the real rehearsal. |

The [failed run](https://github.com/mmzen/se_harness/actions/runs/38895333553) and local reproduction show that current main's legitimate documentation changes prevent the historical resolver from accepting the old release. The proposed correction retains live current-main consistency and validates historical inputs at their immutable recorded commits. The exact linked REL amendment adds only WO-RLS-055; it remains unapplied with original bytes preserved.

The evaluator reports WO-RLS-045 implemented, with next step `PROC-WO-PREPARE-VREC / STEP-WO-PREPARE-VREC-CAPTURE`. Capture is not performed while required final evidence is incomplete. WO-RLS-055 is draft; its implementation needs a new human approval because resolver/workflow paths are outside the approved work orders. Human verification, merge and exact complete-release approval remain separate.

## Retained evidence

[Evidence index](evidence-index-6fa4d1a6.json) binds the package/CI, combination and service archives plus direct identity and reuse reports. Commands retain exact arguments, runtime paths, exits, timings and output. Temporary source exports, profiles, credentials, database backups and package/image payloads are excluded. No private-reasoning blocks were present in the published final-candidate files. Original native evidence and earlier failures remain unchanged.
