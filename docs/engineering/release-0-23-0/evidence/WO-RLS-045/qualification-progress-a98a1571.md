# Qualification after the smaller native tool entry

**The approved input-size correction works. All focused drafting cases pass.
The full hosted workflows work, but instruction timing and remaining delivery
evidence prevent release readiness.**

Tested candidate: `a98a1571292f5bbf34cd2c7cff0af793d00fa12f`. WO-RLS-053 and the other preparation work orders remain
`in_progress`; no aggregate verification or release record is ready. Git remains
authoritative. Released 0.22.1 governs real work and the service; tested client
0.23.0 and plugin 0.2.7 are separate candidate components.

## What changed and passed

The initial test tool guide is 5,303 bytes, down from 8,684. Its raw/lifecycle
detail moved unchanged into the existing execution guide. No fixture, task,
permission, model, content criterion or 64 KiB refusal was weakened.
Actual complete positive entries fit: Claude 64,190 bytes; Codex 64,962 bytes.
The original 12 source files (5,490 bytes) remain complete. This does not prove
that every possible path length will fit.

| Focused case | Independent result | Wall time | Calls | Peak input context |
| --- | --- | ---: | ---: | ---: |
| Claude missing-input diagnostic | Pass; asks for missing outcome/measure and makes no hosted change | 138.534 s | 6 | 40,766 |
| Codex missing-input diagnostic | Pass; required saved report and honest capture limits | 102.329 s | at least 5 | unavailable |
| Claude verification draft 1 | Pass | 180.987 s | 15 | 63,296 |
| Claude verification draft 2 | Pass | 192.288 s | 13 | 60,510 |
| Claude verification draft 3 | Pass | 188.455 s | 11 | 57,865 |
| Codex verification draft | Pass | 211.466 s | at least 13 | unavailable |

Separate HTTP readback confirms the authored bytes and unchanged imported
history. Each positive record remains draft, links REQ-P3-900, derives its expected
result from that requirement, and plans the check and retained evidence without
claiming an executed test. Claude used opus-4-6 for these focused cases; Codex
used the unchanged configured selection. The three Claude attempts have median
188.455 s and range 180.987–192.288 s. They meet the call goal but miss the
under-180-second and under-40,000-token goals. Codex misses duration; its call
total and context goals are unassessed. These are observations, not a general
benchmark; separate fresh projects ran concurrently for some independent cases.

## Full hosted workflows

| Host | Independent functional result | Cost and limits |
| --- | --- | --- |
| Claude Code 2.1.296, opus-5-5 | 12 accepted lifecycle operations replayed; both native exports reconstructed; all seven MCP tools exactly match independent HTTP | 1,328.248 s (22m 8s), 188 calls, 136 model turns, 640,246 reported peak input-context tokens |
| Codex CLI 0.162.0-alpha.17.2 | 12 accepted lifecycle operations replayed; four native exports reconstructed, including earlier/later snapshots; all seven MCP tools exactly match independent HTTP | 1,866.185 s (31m 6s), 276 visible tool items as a lower bound; exact calls, turns and context unavailable |

Both native agents selected their operations without supplied corrective steps.
They completed test work, recorded a risk and mitigation decision, verified test
evidence and recorded a test release. Both recovered a deliberately dropped reply
using the original key, proved identical retry without a duplicate effect, and
retained changed-key, stale-preview and actual evaluator scope refusals. The first
protected-path refusal is distinct from the later scope check. Original source
and imported records, candidate bindings, real repository and inspected host
settings are unchanged. Test records grant no actual verification or release.

Full-run costs include many artifacts, decisions, refusals, reads and exports;
they are not the cost of creating one artifact. They remain high. These full runs
use a different Claude model from the focused drafting sequence.

**R23-NATIVE-009 remains open:** the first explanation precedes the communication
read in both streams (Claude events 25/182; Codex 23/54). Codex disclosed this in
its report; independent review found it in Claude's trace too. Functional cases
NQ-02 through NQ-05 pass. NQ-01 remains incomplete, so there is no combined
five-case pass. Later reading does not repair the earlier timing.

The existing hosted selection route is read before those first explanations,
but has no direct early pointer to this prerequisite. [WO-RLS-054's proposal](../WO-RLS-054/preparation-review.md)
adds one paragraph there. It leaves the policy in its released file and reuses
already supplied content. Its 347 added bytes must be included in the next
input-size check. The proposal and linked release amendment are unapplied.

## Packages, service and delivery

| Area | Current evidence |
| --- | --- |
| Windows source | 1,339 tests, 24 skips, exit 0 |
| Linux source | 1,339 tests, 2 skips, exit 0; CI merge 79076bd82e91821334e60836dbafcb837fccf46e has the exact candidate tree |
| Reproducible archives | Two pinned builds match exactly |
| Installed packages | Windows/Linux exact wheel and index-selected sdist, CLI/init/doctor and ten released-verifier scenarios pass |
| Plugin packages | Both exact host archives staged; 47 portable tests pass with 2 skips |
| Private service | Packaged walkthrough, 64 boundary observations, restart and consistent restore pass; restored graph and logical store equal the source backup |
| Native instruction delivery | Both CLIs pass parent startup, activation after cloning, resume, manual compaction and actual automatic compaction |
| Session isolation | Codex native two-release/parallel/switch/clear/missing-checkout/restoration cases pass |
| Setup/adapter failures | Real concurrent setup, same-identity lock refusal, different-release setup and immutable reuse pass. Interrupted setup is refused; atomic selection keeps the old record; missing resources fail and restore correctly |
| Offline observation | Cached adapter delivery succeeds with test-process socket connects denied; this is adapter evidence, not a native offline-host claim |
| Local proposal boundary | Codex created one completed draft; independent readback confirms no implementation, no lifecycle decision, and unchanged accepted records. Three recovered lookup failures remain in its trace; the full execution-to-delivery cycle is pending |
| Candidate CI | All 17 executed checks passed; ready-release and complete-delivery legs skipped. A later evidence-only head has separate CI |
| Released validation | 2,010 artifacts, zero errors, 63 existing warnings after preparing WO-RLS-054 |

Delivery setup failures remain visible: the initial long Claude test profile
caused a Windows venv-path error; the first isolated Codex profile had an untrusted
hook. New ordinary short profiles resolved the path issue. The exact Codex hook
was reviewed and trusted through its normal CLI screen, then read back. No trust
bypass, current-app restart or global setting change occurred. Temporary driver
path/quoting errors and the first sandbox TEMP refusal did not count as native
passes. Package identities and command records identify every successful rerun.

## What remains

1. Review the bounded WO-RLS-054 correction, required verification and exact
   linked release-membership amendment; then qualify changed instructions.
2. Complete the local work-to-delivery cycle on two disposable checkouts. The
   reused historical fixture's approved note work uses a stale `not_required`
   classification, which conflicts with the current policy. Do not execute that
   fixture as a valid happy path. Preserve it; prepare fresh fixtures with required
   assurance and retain the delivery-authority boundary. No real push/PR is allowed
   from those tests.
3. Obtain separate Codex Windows desktop evidence. It is unverified; the prior
   release's omission supplies no waiver. Workstation availability remains unanswered.
4. Complete exact marketplace review staging, final qualification/handoff and
   aggregate VREC preparation. Human verification, merge and the exact complete
   release decision remain separate.

## Exact package identities and retained evidence

- Wheel: `f2fbc394a65da29fcdb02eb6994dc08e7bc8ad6248b8ddad440021c68e583e16`.
- Sdist: `246a31941b9b7be6dd86bf87ff1527fe841cc9d77f6baaf555ad19021bba7039`.
- Claude archive: `1dd86622f0b249129cfeea280c03ef550445fe0a67c61775699439986eeda9b5`.
- Codex archive: `baade3dff402e2da52b8bf0b4607a00476e63661405384f99f6523091d5a7c72`.
- Base combination: `sha256:ddc6d3dc0a0fddd510985ae4661e9302b8668e4fe794a767867a20a6fd9e35f1`.

[The evidence index](candidate-a98a1571-evidence-index.json) lists bounded archives
and digests. Individual native assessments are under WO-RLS-046. Every archive
has a file inventory and publication method. Credentials, private reasoning,
runtime profiles, images and database backups are excluded. Visible calls,
results, failures, submitted tasks and bounded exports are retained. Historical
evidence and verdicts are preserved. No lifecycle completion or acceptance is
inferred from this report.
