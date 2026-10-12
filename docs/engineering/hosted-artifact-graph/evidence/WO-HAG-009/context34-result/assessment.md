# Hosted qualification after the instruction-pointer correction

Codex passes this independent native assessment. Claude completes the synthetic
lifecycle, but does not pass the instruction, refusal-case and reporting checks.
Combined qualification remains incomplete. No actual verification or release
decision is made by these synthetic records.

## Exact candidate and changes

Candidate C: `01476073cb2fa0a86aaec11c70b0b2d605e8e878`.

The correction preserves evaluator-returned instruction pointers for every
subcommand in a lifecycle response. The command-record index now discovers
extensionless captures and retains exact outcome, receipt, version and error
fields. Guidance tells the agent to preserve the original handoff base and
distinguish receipt lookup, identical retry and changed-request refusal.
The [implementation review and checks](../context34/review.md) remain separate
from this native assessment. These changes do not redefine lifecycle policy.

Candidate client: 0.22.2, wheel SHA-256
`dec1473a0a2b52b79eaafa04400d8dd859f25efb7184f79e7c60731e8ad0e715`.
Candidate plugin: 0.2.7, loaded from disposable packaged resources.
Released governor: 0.22.1, archive SHA-256
`cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
The exact image, both plugin archives, runtime, dependency locks and source
identities are in [provenance.zip](provenance.zip).

All 27 service-wheel members and the pinned evaluator/runtime/database/protocol
components match the prior service qualification. The comparison and historical
chain to VREC-HAG-005 are retained. Archive and image identities differ; this is
reuse of unchanged service behavior, not a claim that the whole package is equal.
Restart and restore were not rerun in these native sessions.

## Results

| Check | Codex 291 | Claude 291 |
| --- | --- | --- |
| Session result | Exit 0, no timeout | Exit 0, no timeout |
| Duration | 24 min 33 sec | 40 min 12 sec |
| Calls | 249 observed tool items; complete native count unavailable | 170 native calls |
| Native failed tool items | 7 | 20 |
| Peak input context | Unavailable | 180,225 tokens reported |
| Accepted lifecycle operations independently replayed | 12 passed | 10 passed |
| Native exports independently reconstructed | 4 passed | 2 passed |
| MCP/HTTP comparison | 8 exact matches; all seven tools succeed | 10 exact matches; six tools succeed, four Cypher requests refused |
| Original handoff base | Preserved | Preserved |
| Unknown reply / identical retry / changed-key refusal | Pass | Pass |
| Required instructions and content review | Pass | Fail |
| Specified scope and changed-draft refusal cases | Pass | Fail |
| Overall native qualification | Pass for this Codex run | Incomplete |

Both hosts ran independently in fresh projects from the same source fixture.
Their sessions overlapped, so these are observed durations, not a controlled
speed comparison. Performance work remains deferred. This is a full lifecycle
exercise, not the single-artifact performance case.

The source fixture S is `5820415917e87b64d80bad2f7c39c6d18d692829`.
Codex's test candidate P is `3148e23665f19e4dbfc8b2d78ca4d5a1c45614e8`;
Claude's is `5fd7b0430fad3e8334f5a9da0c45357b8e68c1c5`.
Each exported VREC and RLS retains its own P. Source bytes and imported `-900`
artifacts are unchanged. Each archive identifies its hosted input baseline B.
C above is the actual implementation candidate; none of these identities are
interchangeable.

## What improved

Both hosts now preserve the complete handoff comparison base from the first
accepted lifecycle receipt. Both recover the deliberately dropped reply, obtain
the accepted receipt and perform an identical retry. The lookup and retry have
the same exact response bytes; a changed request under that key is refused.

Codex uses the required procedure sections, completes a valid out-of-scope case,
changes a selected draft to invalidate its preview and performs a successful
constrained Cypher read. The stale-project guard acts before digest evaluation;
this is not a separate digest-tampering test. Its report preserves that limit.

The independent replay confirms all accepted effects and each exported snapshot
for both hosts. A native exit code of zero is not used as the qualification verdict.

## Remaining Claude failures

1. **Procedure reads remain incomplete.** The read trace has no required
   entry-condition reads for authorization/start and no subsequent handoff,
   completion, verification or release procedure reads. The required Cypher
   references are also absent. Returning exact pointers did not make the agent
   follow them.
2. **The scope test never reaches the scope check.** Request
   `work/requests/handoff-outofscope-001.json` declares ten bytes for nine actual
   bytes and supplies an all-zero digest. Record `work/031-handoff-oos` refuses
   the malformed binding. The native report incorrectly calls this a scope
   result and says the request selected WO-P3-900; it selected WO-P3-001.
3. **The stale case uses the wrong trigger.** Record
   `work/038-stale-preview-demo` follows a completion transition. It is a valid
   stale-version refusal, but not the required preview invalidated by a changed
   selected draft.
4. **There is no successful Cypher read.** All four attempts return HTTP 400
   with `HAG_REMOTE_QUERY_SYNTAX`. Independent HTTP responses match. The report
   says three attempts and does not establish the required successful read.
5. **Release preparation and reporting remain inaccurate.** REL is approved
   with the initial package, despite guidance to defer it until the verified P
   is known. The report omits the separate full S/P/C identities. Stored VREC/RLS
   bindings replay correctly, but do not repair those instruction failures.
6. **The test helper permits misplaced records.** Records `048`, `055`, `056`,
   `057` and `058`, plus their stdout files, were written under `native/` instead
   of the task's permitted `native/work/`. They remain inside the disposable
   workspace, but violate its narrower task boundary. The work-only index omits
   them. The archive retains all ten files at their actual paths, with a
   supplement: 48 indexed records plus five extra records, and six plus three
   nonzero command exits.

Claude also used Write placeholders to create export parent directories after
a shell mkdir denial. The denial and subsequent actions remain visible. This
observation does not establish compliance with the test's stop-after-denial rule.
The proctor did not change permissions or supply corrective commands to the agent.

## Limits and next correction

No native procedural hints or direct operator graph mutations were supplied.
Both monitored before/after repository and host-setting snapshots match; all
staged input digests match. This comparison covers the selected monitored files,
not every file on the machine. The misplaced test records are disclosed above.
Both completed test container pairs are stopped; their volumes are preserved.

Before another full run, correct the helper's write boundary and record inventory,
then use a focused Claude diagnostic for instruction use and the two refusal
cases. Preserve the task's meanings, exact evaluator results and agent-selected
steps. Do not supply a hidden script that completes the workflow, weaken the
criteria or mark malformed-input refusals as the required scope test. More
repeated policy text alone is not supported as a remedy by this result.

The Codex bulk command-record view exceeded the reader's 64 KiB limit; selected
row reads worked. This is retained as a usability observation. It is not a new
performance workstream or a claim of reduced context.

WO-HAG-009/010/011 remain in progress. The released next step for the selected
implementation work is `STEP-WO-IMPLEMENT-CHECK`. No actual VREC is prepared or
verified. PR #543 stays draft, targets main and keeps comparison base
`55caaada508495bea7d97effd27644d1ce8373da`.

At the preceding remote head, Engineering Harness CI fails
`QGP-G4I-EVIDENCE`: WO-HAG-009 has no matching handoff evidence. All other completed
checks pass; three conditional release checks are skipped. This report does not
manufacture completion evidence to remove that failure. New-head CI is reported
separately after publication.

## Review material

- [Codex visible transcript](codex-291-visible.md),
  [evidence archive](codex-291-evidence.zip),
  [file inventory](codex-291-inventory.json).
- [Claude visible transcript](claude-291-visible.md),
  [evidence archive](claude-291-evidence.zip),
  [file inventory](claude-291-inventory.json).
- [Build, setup and observer provenance](provenance.zip),
  [inventory](provenance-inventory.json).

Each host archive includes the unchanged native report, independent assessment,
read trace, requests, exact command results, replay commands and selected export
bytes. Private reasoning, raw account-authentication events, credentials and
whole environments are excluded. Known test tokens are checked absent. Original
private event streams remain unchanged and are identified by digest.

Proctor failures are also disclosed: the initial Codex HTTP observer used an
already-existing output directory and stopped before making requests; the first
Claude final-status read lacked loopback permission and failed before recovery.
Neither was a native intervention. The provenance record distinguishes these
from the actual native failures.
