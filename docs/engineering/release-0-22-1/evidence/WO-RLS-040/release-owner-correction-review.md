# Correct the release owner and continue the approved release

mmzen has approved the complete evaluator 0.22.1 / plugin 0.2.6 release under
RLS-SEH-033. That decision remains valid evidence. Applying it failed before
any write: released evaluator 0.22.0 returns `WEX201` / `E009` because the release
record has `owners = ["Codex"]`, while `authorized_by` must belong to that list.
The record remains **ready**. No merge or public release action occurred.
The earlier transition gate check passed, but it did not construct and validate
the proposed final record. The exact transition preview should have run before
the final approval request; that preparation omission is retained here.

## Exact correction

Change one line in [RLS-SEH-033](../../releases/RLS-SEH-033.md):

```diff
-owners = ["Codex"]
+owners = ["mmzen"]
```

Keep `prepared_by = "Codex"`. mmzen is the accountable release human; Codex
remains the actual preparation agent. Preserve status, lifecycle history,
candidate, distributions, relations, body and all bound evidence. The exact
[patch](release-owner-correction.patch) is unapplied in the real checkout.

This is a correction of a ready release input under the existing release
preparation scope, not a product or evaluator implementation. No new binary,
test change or replacement release record is proposed.

## Diagnosis and checks

The released `transition` command has no owner-binding or ownership-edit option.
The separately implemented HAG decision fix applies to `decide` question/deviation
dispositions, not to RLS authorization. Running unreleased source as governor or
recording Codex as the human release decision-maker would not be a valid recovery.

In a separate disposable checkout at the exact review head, the one-line proposal
passes released 0.22.0 validation and a **read-only** release transition preview
as mmzen. No transition was applied there. [Raw evidence](release-owner-correction-checks.zip)
includes the original failed real preview, unchanged original RLS bytes, exact
commands and the passing proposal preview. Disposable-checkout setup first met
Windows path-length and line-ending issues; the retained recovery enabled long
paths and restored exact Git-blob bytes before validation. This proves the proposed input removes
the observed owner mismatch; it does not supply authority to apply it.

## Bounded amendment to the existing approval

Approve only this ownership correction and the following review-base update.
After approval, make a separate correction commit containing only the RLS line
above, on top of this published proposal. The resulting full commit becomes the
new pre-decision review base. Preserve the already approved frozen plan bytes and
SHA-256 `50c97db22f33cdcf0eb44b229b5e1ab7d5afca887cca6ffb4a9e380bc8c3641b`.

The corrected review base consists only of the previously reviewed release,
these three proposal/evidence files and the exact owner correction. Compare that
derivation before binding it. Then re-preview and apply the existing complete-
release decision through released evaluator 0.22.0 as mmzen, append the normal
release event, and bind the same plan to that corrected review base. The existing
publisher must accept the decision-only diff from that base.

This is an explicit amendment of the reviewed RLS ownership/base, not a silent
change or a gate waiver. The existing complete-release grant continues for all
unchanged payloads, destinations, receipt paths, recovery conditions and public
checks. Candidate `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`, evaluator 0.22.1,
plugin 0.2.6, the desktop limitation and adoption exclusions are unchanged.
Do not ask again for the unchanged release/publication authority.

**Response requested:** “Approve the owner correction and continue.”
Until that response, preserve the real RLS as ready and keep PR #536 draft.
