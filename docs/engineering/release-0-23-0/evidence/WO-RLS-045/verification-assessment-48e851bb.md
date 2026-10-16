# Final release verification assessment — 0.23.0 / plugin 0.2.7

The candidate is ready for the human verification decision, subject to the
existing release-only dispositions below. No verification decision is supplied
by this assessment. The later review commit contains this evidence and the
generated VREC; it does not replace the assessed candidate.

Candidate: `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15`. Selected governor: released **0.22.1**, outside the checkout.
The private hosted service remains source-built; Git remains authoritative.
The final record covers exactly **20 implemented work orders and 11 contracts**
declared by REL-SEH-036. The [coverage file](candidate-48e851bb-final-coverage.json)
lists every ID and path. Delivery WO-RLS-047 remains approved and unstarted.

## Observed final checks

| Check | Result and exact applicability |
| --- | --- |
| Windows source | 1,346 tests, 24 skips, exit 0 at `c740d49e30da74bab27ad29bb59fef2e785a6eae`. Reused with an [explicit comparison](candidate-48e851bb-windows-source-applicability.json): only seven release completion/evidence files changed afterward. The initial sandbox access failure is retained. |
| Linux source | 1,346 tests, 2 skips, exit 0 at CI subject `b058eb29500e96ffa5844eaf69da44e5bb0af748`. Its entire Git tree equals C. |
| Reproducible build | Two pinned local producer runs match byte-for-byte. The independent [exact-head GitHub replay](https://github.com/mmzen/se_harness/actions/runs/38903274786) has the identical full bundle manifest. Historical RLS-SEH-033 and complete-delivery/recovery rehearsals also pass. |
| Installed archives | Exact final wheel and index-selected sdist pass on Windows and Linux. Released independent package checks pass. No direct archive-path PEP 610 sdist claim is made. |
| Upgrade | Two real Windows 0.22.1-to-0.23.0 runs pass with matching semantic digest. Both CI platform upgrade jobs pass. |
| Plugin assembly | 47 portable tests, 2 skips; both 0.2.7 packages contain the exact final wheel. All 89 staged Git blobs match the qualified files. |
| Hosted combination | Fresh final packaged walkthrough: 18 commands, including expected refusals. Restart and consistent restore pass. Fixed evaluator remains 0.22.1. |
| Unchanged service boundaries | Reused from candidate `6fa4d1a6`, explicitly compared in [the reuse record](candidate-48e851bb-service-boundary-reuse.json). Server runtime, dependencies, fixed source fixture and operational policy inputs match. These are not fresh boundary runs. |
| Integration package | All 19 CI checks pass at C, including deterministic integration build and independent same-byte Windows/Linux installs. The exact source TAR is 602,767,360 bytes; expanded file total 590,043,102 bytes; 17,735 members. All remain within fixed 1 GiB / 20,000-entry limits. The non-promotable PR package is distinct from the release archives. |

## Contract assessment

| Contract | Evidence and assessment |
| --- | --- |
| VER-HAG-001 | Original import/immutability/atomicity/graph outcomes in preserved VREC-HAG-004 and its bound evidence; current server/client byte comparisons, fixed imported Git bytes, final walkthrough and recovery corroborate integration. Unchanged service boundaries are reused as labelled. |
| VER-HAG-004 / VER-HAG-005 | VREC-HAG-003 and exact unchanged evidence retain evaluator-pin reconciliation, stacked-branch adoption assessment and history preservation. The final combination independently names the pinned released evaluator and actual component identities. |
| VER-HAG-006 | VREC-HAG-005 retains private lifecycle parity, authority/operation boundaries, rollback/staleness/retry, exact export/replay and compatibility. New final archive admission, packaged walkthrough and restore pass; unchanged mechanisms and their original results are compared explicitly. |
| VER-HAG-007 / VER-HAG-008 | VREC-HAG-006/007 retain their accepted contract scope. Native and independent replay/read observations at `bb089004` are reused through exact runtime/instruction/fixture comparisons. Original failures and the two release findings stay visible; this does not convert failed drafting/content cases into passes. |
| VER-HUP-025 | Preserved VREC-HUP-028 and its exact candidate-bound evidence; fresh final two-run upgrade qualification and both CI platform jobs assess current integration. |
| VER-IAR-021 | Preserved native bootstrap, selection, resume/compaction, isolation and delivery-gap evidence at `bb089004`, including actual host/session identities. Portable assembly/selection tests run again. Desktop is unverified under the new bounded disposition; CLI results do not cover it. |
| VER-IPK-002 | Fresh final integration CI build/Windows/Linux receipts, source size/count/hash, full source suites and preserved hostile-input regressions. Prior VREC-IPK-002 stays unchanged. |
| VER-RLS-039 | Final membership, source/package/build/upgrade observations, exact manual rehearsal, archive/staging identity and preserved governing records. WO-RLS-055 resolves the historical-rehearsal blocker with actual qualification. Later ready-RLS replay and complete-release authority remain separate procedures. |
| VER-RLS-040 | Both final plugin inventories and public-parent staging readback; actual coordinated image/configuration; fresh final walkthrough/recovery; explicit native/service reuse. The accepted native findings and desktop omission remain limits. |

The [source/package comparison](candidate-48e851bb-source-package-reuse-comparison.json)
checks all 127 expanded wheel members, both host inventories and nine historical
verification records with their bound evidence. The [service comparison](candidate-48e851bb-service-runtime-reuse-comparison.json)
checks all 27 expanded server members and fixed dependencies. C54-to-C6 comparisons
are retained unchanged; C6-to-C comparisons extend that evidence chain. Archive,
inventory, source and image identities differ and are assessed separately.

The release census remains advisory: it reports missing singular trailers for
some first-parent commits, including combined work-order declarations. This is
not an exemption or a passing census claim. REL-SEH-036's reviewed 20-work-order
membership supplies formal scope; earlier 0.22.1 publication records remain
historical and are not reclassified as new product work.

## Open items carried into the decision

- **R23-NATIVE-010 remains open:** the separate Codex read-only trial explained
  before reading communication policy. Functional reads passed; the instruction
  failure did not. DEC-RLS-010 / RISK-RLS-008 accepts this release-only carry.
- **R23-NATIVE-011 remains open:** both proposed work orders omitted generated
  verification paths. Separate seeded execution does not repair those drafts.
  The same bounded disposition applies.
- **Codex Windows desktop remains not run / unverified**, under DEC-RLS-011 /
  RISK-RLS-009. Complete desktop qualification before the next plugin release or
  a verified-desktop claim.
- Duration/context improvements remain separate. RISK-HAG-001/002 retain the
  private-sandbox and deferred database-control boundaries.

These decisions do not mark failures or unrun cases passed. Historical native
indexes retain the readiness statements from when they were written; the later
DEC-RLS-010/011 records provide the actual bounded human dispositions.
R23-REHEARSAL-001 is resolved; its original failures remain under WO-RLS-055.

## Exact delivery inputs

Wheel SHA-256: `ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c`.
Source archive SHA-256: `777c9c1f518f6db1d3beb013f9bbb908544c482598ee399767fd789414f2ccfa`.
Hosted combination: `sha256:70890d365551c04d38eb74afb8f815cf30c5eb61d09e9ac7d1e322b9b657de0a`.
Plugin review ref: `refs/heads/codex/plugin-0-2-7-staging` at `d04776866046b60b14ffef14ced1453c4aafa7d9`.
The public marketplace tip remains `85ae003769f53908addbdcf46c820a8af530ac24`.

The [evidence index](evidence-index-48e851bb.json) identifies current archives and
direct receipts. Capture also explicitly binds the reused native archives,
assessments, historical records/evidence, open-item dispositions and correction
results; it does not rely on following index links. New archives contain no
credential or private-reasoning payload. Existing protected bytes are preserved.

Human verification accepts this assessed candidate and its disclosed limits.
Merge, the exact complete-release decision, public delivery, repository adoption
and host updates remain separate. No public package, tag or marketplace was
promoted during this verification preparation.

## Capture runtime recovery

The initial capture refused `RID018`: the system Python resolved distribution
metadata outside the temporary candidate checkout. No VREC was written. A fresh
source-test environment contains no installed se-harness metadata; the same
identity and candidate checks run unchanged there. The original refusal and
sandbox ensurepip failure are retained in capture-runtime-recovery-48e851bb.zip.
This recovery changes the test environment, not product code or acceptance rules.

## Post-candidate evidence binding

The clean runtime passed all candidate checks. The second capture then refused
WEX304 because newly produced final evidence is absent from the older candidate
commit. No record was written. The committed-candidate procedure is retained:
direct evidence paths name only unchanged files present at C; the candidate test
checks every final and reused evidence digest against one exact receipt. Its
SHA-256 is an explicit test argument retained in the generated VREC, as in the
previous release. The byte-identical receipt and final observations are retained
in the later review commit. No new candidate or rebuilt payload is substituted.
The refusal is retained in capture-receipt-recovery-48e851bb.zip.
