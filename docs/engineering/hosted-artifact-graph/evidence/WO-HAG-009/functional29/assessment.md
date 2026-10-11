# Hosted service functional qualification — 11 October 2026

**Codex passes all five VER-HAG-007 scenarios. Claude is not qualified.**
Claude completed test work and verification, but its release contract named the
wrong commit. The evaluator refused release preparation. I stopped the native
session after repeated unsuccessful recovery attempts. The remaining Claude
cases are incomplete, not passes.

This run focuses on the remote service and graph. Further performance
improvements are deferred. No service runtime, evaluator policy, acceptance
criterion or permission was changed for these tests.

## Results

| Required scenario | Codex `codex-241` | Claude `claude-241` |
| --- | --- | --- |
| NQ-01: instructions and selected context | Pass. Exact packaged reads, triggers and released sections retained. | Incomplete. Some returned prerequisites lack observed reads; no final host report. |
| NQ-02: agent-driven lifecycle | Pass. Definitions, work, risk/decision, handoff, verification and test release. | Failed at release preparation. Eight accepted operations through verification replayed successfully. |
| NQ-03: refusal recovery and seven MCP reads | Pass. Required stale/scope refusals; eight immediate HTTP comparisons cover all seven actual MCP tools. | Incomplete. Required stale-after-edit and scope cases were not demonstrated; no actual MCP reads occurred. |
| NQ-04: unknown reply and retry | Pass. Original receipt recovered; identical retry made no duplicate change; changed payload conflicted. | Pass. The same three checks and version comparisons passed. |
| NQ-05: exports and honest limits | Pass. Four native exports reconstructed; exact Git bytes and original candidate binding checked. | Incomplete. One native export reconstructed; the later export and final report are absent. |

The Codex run exited normally after **1,482.773 seconds (24m 43s)**. Independent
released-evaluator replay confirmed **11 accepted lifecycle operations** and
**four native exports**. The eight MCP responses exactly matched independent
HTTP reads for their selected views. Its report identifies the expected refusals,
two incidental helper syntax errors, synthetic decisions and remaining limits.

The Claude run lasted **2,336.698 seconds (38m 57s)**, with **168 native tool calls**
and **166,547 peak input tokens**. Peak context is not total billed tokens.
Codex's corresponding call/context metrics were unavailable from the retained
summary; they are not inferred. These measurements are observations, not a claim
that the separate efficiency goals passed.

## Claude's release failure

Claude authored and approved `REL-P3-001` with:

```toml
candidate_commit = "5820415917e87b64d80bad2f7c39c6d18d692829"
```

That is the original fixture source **S**. The captured and verified test
candidate **P** was `59a30811eba95515c3dc57fe4b815a9be9a6ab1e`.
Release preparation returned:

```text
WEX404: the final verification does not identify the release contract's candidate commit
```

The mismatch came from authored test content. This observation does not establish
a service implementation defect. The evaluator's refusal preserved the binding
between release and verification.

Several attempted contract revisions first failed locally with `not_sent`.
A later request reached the service and returned `HAG_REMOTE_PROTECTED_FIELD`:
the accepted record could not be rewritten through draft revision. These are
different failure paths and remain separately recorded. Claude then created a
separate `REL-P3-002` draft, but its proposed content failed admission.

I stopped only the owned Claude child process after the repeated refusals.
This was a recorded proctor intervention, **not the 3,600-second timeout**.
Whether Claude could eventually recover through a valid separate proposal was
not tested. No corrective command or operator mutation was supplied during the
native run. Two denied shell-listing attempts also remain in its transcript;
permissions were not widened.

The independent replay passed all eight accepted operations, then failed its
full-export assertion because only one native export existed. Its retained
`assessment.json` is the last running checkpoint; `failure.json` is the terminal
result. A separate terminal assessment explains this distinction without editing
either original file. No synthetic RLS was prepared or assessed.

## What this establishes about the service and graph

Both hosts independently authored new records, executed the greeting assertion,
and reached verified test work. Accepted lifecycle results agreed with ordinary
released 0.22.1 replay, including the exact affected file paths. Both recovered a
dropped accepted reply without a duplicate operation. Codex also demonstrated
the complete release rehearsal, graph reads and exported Git history.

The existing core qualification under **VREC-HAG-005** remains separate. A direct
comparison found all **27 service-wheel members identical** to that verified
package. Evaluator, runtime, database, schema, protocols and dependency-lock
identities also match. Only service documentation changed. Archive, image and
source identities differ and remain explicit; unchanged content does not make
their container/archive hashes identical. Restart/restore and other unchanged
service scenarios were reused on this basis, not claimed as newly executed.

## Candidate, environment and boundaries

- Implementation/package candidate C: `dfcf1e976123836f00354a228c8e72a833f2e3cf`.
- Review checkout at test start: `ad1fbc2dea2649cfd25bceb617a50183ec7ad6ce`.
- Client: 0.22.2; session-selected candidate plugin: 0.2.7; service: 0.1.0.dev1.
- Released governor: separately installed 0.22.1, archive SHA-256
  `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
- Codex CLI: 0.162.0-alpha.2. Its model identity was not extracted from the native
  schema and is left unavailable. Claude Code: 2.1.273; reported model:
  `claude-opus-4-6`.

Fresh live authentication probes passed before launch. The hosts used separate
projects and volumes from the same source fixture. Neither inherited the other's
work. Only the previously approved Codex session-level loopback permission was
used, after its boundary probes passed.

Staged input hashes and monitored repository/host settings were unchanged for
both sessions. Both test container sets are stopped with volumes preserved.
The active Codex desktop application and installed host plugin were unchanged.
Git remains authoritative. Automatic startup/compaction delivery, production
authentication, database ACL enforcement, public deployment and real release
remain outside this qualification.

## Evidence

- Codex: [visible transcript](codex-241-visible.md), [records and replay](codex-241-evidence.zip), [hash inventory](codex-241-inventory.json).
- Claude: [visible transcript](claude-241-visible.md), [records and replay](claude-241-evidence.zip), [hash inventory](claude-241-inventory.json).
- Setup, identities, boundary probes and service reuse: [provenance archive](provenance.zip), [inventory](provenance-inventory.json).
- Publication checks: [archive](report-checks.zip), [inventory](report-checks-inventory.json).

The native archives retain exact request/result bytes, instruction-read traces,
exported files and bundles, independent assessments and actual command records.
Private reasoning, raw provider streams, credentials and account stores are
excluded. Known test tokens were checked absent. Earlier failed runs remain
unchanged at their original evidence paths.

## Remaining work

The next functional correction should make the distinction between fixture S and
verified candidate P explicit at release-contract authoring, and require the
current procedure's prerequisites before each action. The recovery route must
preserve accepted records. Then rerun the affected Claude lifecycle, refusal,
read and export cases from a recorded clean point. Do not count a correct Codex
result as a substitute for those cases or waive a case to finish the PR.

This evidence update makes no implementation correction and grants no new
authority. Performance work remains deferred. **WO-HAG-009, WO-HAG-010 and
WO-HAG-011 remain `in_progress`; no real VREC is prepared or accepted.**
The released evaluator's current step remains
**PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK**: retain and assess the implementation
evidence before the Git-derived handoff check.

PR #543 remains an unfinished-work draft targeting `main`, with the original
comparison base. Its missing WO-HAG-009 handoff evidence remains disclosed.
No merge, release, deployment or authority cutover is requested.
