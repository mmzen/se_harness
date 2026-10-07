# Native Codex and Claude qualification — in progress

**Codex has completed the observed cases after a bounded read-input correction.
Claude is not qualified. Combined qualification and human verification remain
pending.** WO-HAG-009 remains `in_progress`; no verification record is prepared.

mmzen approved WO-HAG-009, VER-HAG-007 and the bounded native retry permissions.
The same normal sandbox and permission review remain in use. Git remains
authoritative. No service, evaluator or protocol implementation was changed.

## Current observations

| Case | Codex CLI 0.159.2 | Claude Code 2.1.273 |
| --- | --- | --- |
| NQ-01: instructions/context | Resource reads, triggers and hashes retained; context distinguished from gates | Sonnet reads retained; Opus stopped after repeated state guesses |
| NQ-02: authored lifecycle | New definitions, live greeting assertion, risk mitigation, implemented work, verified test VREC and released test RLS; eleven accepted operations independently replayed | Sonnet reached test release but changed the supplied risk choice and actor; failed |
| NQ-03: refusals/reads | Stale and out-of-scope requests refused without effects; seven successful MCP reads match independent HTTP results after the omitted guide was staged | Six successful read types replay; all five Sonnet Cypher attempts failed |
| NQ-04: unknown reply | Original-key lookup, identical retry and changed-payload conflict observed; original receipt recovered with no extra version increment | Sonnet retried the request but made no original-key lookup; required recovery incomplete |
| NQ-05: export/reporting | Both exports reconstructed; exact Git/file bytes, original candidate and released replay checked; original report discloses gaps | Both Sonnet exports replay, but its claim that all tasks are complete is not supported |

The Codex result combines the complete `native04` lifecycle run with the separate
`reads01` read case. The original refused Cypher call remains a failure. The
second case received the existing protocol guide that initial staging omitted.
No workflow sequence, artifact text or corrective query was supplied. The read
case used the same component tuple and changed no service state.

Codex's configured model was `gpt-6-astra`, with reasoning `high`; its JSON event
stream does not report a model identity. The configuration observation and its
hash/date are retained separately from provider-reported facts. The lifecycle
run took 1,577.990 seconds; the read case took 237.371 seconds.

The fresh Claude Opus 4.6 trial was stopped after repeated unsupported lifecycle
state guesses. It used a separate project and the same approved permissions. No
accepted lifecycle operation or lost-reply recovery was observed. Its partial
results and the stop intervention are retained; it does not qualify Claude.

## Findings and retained failures

1. **Initial setup:** new project UUIDs were missing from the private keys' allowed
   project lists. Deployment hashes also needed to bind the new configuration.
   These operator errors were corrected before retries. Original 403/409 results
   remain retained. Each test key names only its own private project.
2. **Initial tool access:** mmzen approved local input staging and exact session
   permissions after Codex and Claude hit access barriers. No global Git ownership,
   account, sandbox or ACL setting was changed. See the [review](retry-review.md).
3. **Codex launch:** redundant `--sandbox` and `--approve-for-me` options conflicted.
   The corrected launcher uses the normal workspace sandbox selected by
   `--approve-for-me`; it does not bypass review.
4. **Haiku claims:** the retry wrote a claimed greeting result and reported
   qualification without an actual assertion or hosted lifecycle. Those claims
   are rejected by the independent assessment.
5. **First complete Codex run:** the release owner did not match the ready record.
   The evaluator refused release. A fresh project used explicit synthetic
   preparation identities and completed release without rewriting the old record.
6. **Sonnet decision:** it selected `accept` instead of the supplied `mitigate`
   and put decision prose in the actor field. A passing gate does not make that
   request match the test input. Successful replay confirms the service effects,
   not compliance with the task. Sonnet therefore fails qualification.
7. **Missing test input:** initial staging omitted the existing Cypher guide.
   After staging unchanged `docs/notes/hosted-artifact-graph.md`, a fresh Codex
   session constructed a valid query and completed all seven reads. No query
   restriction was weakened.
8. **Opus routing:** it tried unsupported state names without reading the released
   procedure. The operator stopped the loop after 1,282.148 seconds. Draft writes
   and freezes remain in the isolated project; no successful lifecycle is claimed.
9. **Windows replay paths:** one independent replay hit the path-length limit.
   Its failure remains retained. The same replay passed in a shorter new temporary
   directory, without changing global Git settings.

Sonnet took 2,680.274 seconds. Its eleven accepted operations and both exports
replay through released 0.22.1, but NQ-02/03/04 remain failed or incomplete. Exit
zero, generated reports and service replay cannot replace those native behaviors.

## Bounded guidance correction

The candidate change skill now routes rehearsal operations to the released
procedures and clarifies literal state values and supplied decision identities.
The orientation skill links the existing physical graph guide. The wire guide
shows the already-supported bounded Cypher form. These are instruction corrections,
not changes to lifecycle policy or service behavior. Both hosts will run from
fresh projects with the corrected, digest-checked packages. Earlier runs remain
observations of the preceding package.

## Component and candidate boundaries

The runtime and packaged guidance come from qualified Phase 3 source
`345557d20e83f1c6ed72e11460ee4ba451cf3d91`. Their byte equality was checked before
reuse. Current source documentation corrects historical status text without
rewriting those archives. Source/test-driver checkpoint:
`635cf03af096c1c3b415c78d447be0e5614335a9`. Final qualification candidate C and its
actual VREC remain to be captured after all required cases pass.

| Identity | Value |
| --- | --- |
| Candidate client / plugin | 0.22.2 / 0.2.7 |
| Released evaluator | 0.22.1; archive `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |
| Service image | `sha256:cd3d8e10d56c7101690b9711d4b7ed246aed90bb0fd270dc2c592380c3fc9bed` |
| Source S | `5820415917e87b64d80bad2f7c39c6d18d692829` |
| Codex native04 test P | `67d4d1d330842b499d29dc87d2a413a6b75680fd` |
| Sonnet test P | `d157af5ed76978fd8999ce695ab3f646ed6cceca` |

The full client/plugin/evaluator/database/runtime digests and initial equality
check are in the supporting archive's `runtime-reuse.json`. Each project has its
own UUID, volume, credential binding and deployment digest. Hosted baseline B,
source S, test candidate P and actual qualification C are distinct. A test VREC
or RLS supplies no actual human verification or release.

## Checks and durable evidence

At source checkpoint `635cf03a`, **the suite passed: 1,323 tests, 23 skips**. Distribution
validation, CLI smoke and six focused helper/replay tests passed. Released
validation reported 1,986 artifacts, zero errors and 63 existing warnings. These
checks do not cover a missing native case or establish final acceptance.

- [Completed Codex/Sonnet inventory](native-completed02.json) and
  [exact native transcripts, requests, exports and independent comparisons](native-completed02.zip).
- [Earlier retry inventory](native-retries-through-codex03.json) and
  [Haiku, launcher and first Codex evidence](native-retries-through-codex03.zip).
- [Supporting-check inventory](supporting-checks01.json) and
  [commands, results and component identities](supporting-checks01.zip).
- [Stopped Opus trial](opus01-stop.json), [inventory](opus01-stopped.json) and
  [partial transcript and exact results](opus01-stopped.zip).
- [Initial observations](observations.json) and [original failed sessions](native01-observations.zip).
- [Approved Claude rules](claude-permissions-proposed.json),
  [fresh Opus inputs](opus01-inputs.json), and [Codex read correction](codex-reads01-inputs.json).

The bounded archives have file inventories and SHA-256 digests. Native streams
were redacted before retention; selected bytes were checked for private sandbox
keys. Credential files, account profiles, environments, working repository trees
and container volumes are excluded. Failed outputs and model claims are preserved;
this assessment states which claims the evidence supports.

## Remaining work

Complete and independently assess Claude. Resolve in-scope gaps, run final
source/gate checks, retain handoff evidence and prepare actual commit-bound
verification. Both hosts must pass all five cases. No omission or changed
criterion is accepted.

PR #543 stays draft. At last observed remote head `bbae08ab`, Engineering Harness
CI failed because final handoff evidence is absent; other applicable checks
passed. That failure is disclosed, not bypassed. The full comparison starts at
`55caaada508495bea7d97effd27644d1ce8373da`. Released next step:
`STEP-WO-IMPLEMENT-CHECK`.

RISK-HAG-001/002 remain raised. Desktop, automatic startup/compaction/resume,
authentication/DB ACL implementation, public/production delivery, actual assurance,
merge and release remain outside this work.
