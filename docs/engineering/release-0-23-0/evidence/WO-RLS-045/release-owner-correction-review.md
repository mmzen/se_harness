# Correct the release owner and continue the approved release

mmzen approved the complete evaluator/client 0.23.0 and plugin 0.2.7 release.
That approval remains retained. The released 0.22.1 evaluator refused its
transition preview with `WEX201` / `E009`: `authorized_by` must name a record
owner, while generated RLS-SEH-034 has `owners = ["Codex"]`.
The record remains **ready**. No release transition, merge or publication occurred.

## Exact proposed correction

Change one line in [RLS-SEH-034](../../releases/RLS-SEH-034.md):

```diff
-owners = ["Codex"]
+owners = ["mmzen"]
```

Preserve `prepared_by = "Codex"`, state, history, candidate, distributions,
relations, body and all bound evidence. The [exact patch](release-owner-correction.patch)
remains unapplied in the real checkout. This corrects a ready release input;
it changes no evaluator code, binary, plugin, test or provider setting.

## Evidence and cause

The generated owner conflates the preparation actor with the accountable release
human. `transition` offers no owner-binding parameter. The existing `decide`
owner-binding feature concerns question/deviation records, not this operation.
Recording Codex as the decision-maker would misattribute the human decision.

The same issue was recorded during the 0.22.1 release. It remains present in
the selected evaluator. I missed that known preparation condition. A passing
transition gate check did not detect it; the exact read-only transition preview
should have been performed before the final approval request.

In a separate disposable checkout of `d463e42d6c5e4386fc07b0b6173b1c43f8908237`, the proposed one-line input
passes released 0.22.1 validation and the read-only transition preview as mmzen.
No transition was applied there. The real record remains byte-identical to its
reviewed version. [Raw evidence](release-owner-correction-checks.zip) retains
the refused real preview, original bytes, exact commands and passing proposal.

Follow-up: distinguish preparer and release owner in record preparation, and
ensure the final decision preview is checked before asking for release approval.
This is an open follow-up, not a change to the already verified 0.23.0 payload.

## Bounded amendment to the reviewed base

The approved plan permits only the recorded decision after its review base.
Changing ownership therefore needs this explicit amendment. Approve the one-line
owner correction and the following precise rule for the new pre-decision base:

1. Start at the published commit containing only these three proposal files
   on top of `d463e42d6c5e4386fc07b0b6173b1c43f8908237`.
2. Add a separate commit changing only the RLS owner line shown above.
3. Use that exact resulting commit as the amended review base. Compare the
   derivation before applying the human release decision.

Keep the frozen plan bytes and SHA-256
`420b4b82891b2fe77244cc3c4a995ddab8153a11f649324f01b1f37e83e51b34` unchanged. Re-preview and record the existing complete-release decision
as mmzen, then require the publisher's normal decision-only integration check.
The original grant continues for its unchanged payloads, destinations, receipt
paths, provider checks and recovery rules. No gate is waived.

Candidate `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15`, evaluator/client 0.23.0, plugin 0.2.7 and the accepted
DEC-RLS-010/011 limitations are unchanged. Adoption and user-host updates remain
excluded. No repeat approval of the unchanged release/publication plan is requested.

**Response requested:** Approve the owner correction and continue.
Until that response, keep the real RLS ready and PR #545 draft.
