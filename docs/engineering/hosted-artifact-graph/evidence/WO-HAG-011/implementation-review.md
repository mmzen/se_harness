# WO-HAG-011 implementation review

Human mmzen approved the reviewed package, required commit-bound verification
and bounded updates to draft PR #543. The released 0.22.1 evaluator approved the
three definitions and work order, then started WO-HAG-011 as Codex. Exact command
records are retained in approval-and-start.zip. The preparation review remains
historical; approval does not claim implementation verification.

## Design choices

The existing remote client gains explicit typed inputs for five existing
operations. It retains raw mode. One request stays one chosen mutation. Optional
create-document return adds only an exact revision read. The client owns byte
encoding, installed identity checks and local capture; the agent owns content,
operation, versions and retry key. No service, schema, dependency or lifecycle
rule changes are needed.

Compact views retain complete responses before displaying selected fields.
Omissions carry paths and required-reading flags. Capture failure after send
retains uncertainty and the original operation key. Unknown effects are not
silently retried. Exact document files avoid agent base64 extraction.

Instruction sections are complete copies with provenance, not summaries.
Selection stays with the agent/current procedure. The shared section reader is
also used by the native adapter on verified staged released bytes. It does not
make candidate source the governor. Fenced headings and ambiguous/missing
sections have explicit tests.

The four skill entries are reduced from 34,825 characters to about 3,300 bytes.
Details moved into task references. Shared repository selection has one reference.
Hosted drafting no longer loads repository activation or future lifecycle steps.
This reduction is not itself a claim about actual native context or duration.

The added client code handles concrete representation and failure boundaries;
there is no workflow engine or background state. The remaining cost includes
native host context, required source reading, each chosen mutation and independent
readback. Whole-task observations and content review remain required.

## Checks and remaining work

Initial focused checks passed (46 tests, 4 skips; native helper 13 tests).
Additional provenance and recovered-failure cases are included in the subsequent
checks. Retain all actual logs, skips and failures with the final assessment.
Native measurements, independent saved-document review, complete checks and
commit-bound verification are still pending. WO-HAG-009/010 qualification is
separate and remains incomplete. No release, installation or merge is claimed.

The first full source run failed two documentation assertions and one retired-term
check. Corrected the remote-operation table labels, restored conditional direct
provider-controls links in the two skill entries, and used released-evaluator
terminology. The 82 affected tests passed; the next full run passed 1,331 tests
with 24 skips. A real HTTP create/document-read/raw-replay test was then added;
the final full run is retained separately. No tests or policy were weakened.
