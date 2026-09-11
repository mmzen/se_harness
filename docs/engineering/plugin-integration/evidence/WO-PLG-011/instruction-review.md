# Independent instruction review

The separate reviewer read the candidate skill and references against approved
SPEC-PLG-011, VER-PLG-011, SPEC-PLG-010, the managed router and installed workflow
and decision rights. The review reported one actionable ambiguity beyond the
capture-footprint finding already under correction.

## External mutation versus read-only inspection

The initial `references/external-actions.md` required matching action authority
before "any external tool call" and then said not to dispatch the tool when it
was absent. Read literally, this could prevent a read-only PR/commit/registry
inspection used to establish authority or resolve an uncertain earlier effect.

The correction limits that gate and refusal to the selected external mutation.
Read-only inspection keeps its existing host/network permissions and does not
need merge or publication authority. The action, candidate, evidence and
destination comparisons and independent enforcement requirement remain intact.

Corrected reference SHA-256:
`ec0fd8f071f2bb0d5ae294594df7f118a817d0c62c8616c26e22285281acbb69`.

## Capture footprint

The independent Windows observation separately exposed generated writes under
`target/harness-dashboard/` during released 0.16.0 capture. The original oracle's
record/evaluator-only path expectation was too narrow, and the candidate table
did not disclose the generated footprint. Both limitations remain recorded;
the original observation is not replaced by a pass.

The corrected `references/records.md` accounts for installed generated and
ignored output paths before dispatch and retains actual effects, including
leftovers from a failed operation. Its SHA-256 is
`0c266bef118b904030e1982318763021bdfd699e34b353d4f38e5d9f2f43a20b`.
Corrected fixture expectations and applicable authority are fixed before a
separate repeat; ignored paths must not be silently dropped from observations.

## Review limits

The reviewer reported that the documented capture, release-preparation and
evidence arguments match installed 0.17.0 help and found no further concrete
authority or recovery defect. This was a read-only instruction review, with no
lifecycle action, network access, fixture execution or assurance decision.
Behavioral acceptance and its raw evidence are separate.
