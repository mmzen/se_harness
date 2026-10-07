# Make the created document readable

Opus08 found the authoring instructions but used a receipt key for an artifact
read. After the refusal it created more templates without inspecting the first.
The new correction addresses that concrete operation, under WO-HAG-009's existing
guidance and test-driver scope. Historical trials and accepted policy stay unchanged.

## Changes

- Put the existing one-artifact drafting sequence beside hosted creation guidance.
  Link directly to the revision-read route. A failed read stops that drafting step.
- Describe the exact hosted read inputs and response fields in harness-orient:
  the creation result's view, artifact/revision IDs, the revision request schema,
  complete response, canonical document bytes and their digest. Receipt lookup is
  a different operation. No populated request or lifecycle answer is supplied.
- Extend the existing exact schema views to read operations; retain shared allOf
  requirements and the closed-property boundary. Stage actual per-operation CLI help.
- Add bounded exact-basename search to the native test helper. Return up to 20
  verified paths, completeness and total matches. The agent chooses a path; missing
  or ambiguous names do not select a file or trigger whole-inventory loading.
- Let the existing JSON field reader decode one explicitly selected base64 string
  to exact UTF-8, retaining byte length and digest. Reject invalid encoding, secrets
  and oversized output. It writes no file and completes no template.

## Diagnostic

Build the exact candidate packages. Use a fresh Claude project to prepare one
definition for the existing greeting outcome. Observe the chosen creation,
revision read, decoded template inspection, authored completion and retained
revision. The agent receives the outcome and current tool paths, not a completed
artifact, request or hidden sequence. Preserve normal hooks and permission rules.

This diagnostic is deliberately smaller than full VER-HAG-007 qualification.
A successful result permits a later complete lifecycle rerun; it does not replace
that run or qualify earlier Codex evidence against changed instructions. Retain
all failures, interventions and actual context measurements. No efficiency
percentage may be inferred from differently sized tasks.

## Checks

Test filename ambiguity, incomplete results, path/digest refusal, exact UTF-8 and
newline preservation, invalid/noncanonical base64 and credential refusal. Check
read-schema constraints with the service's validator. Run the required source,
plugin, distribution and CLI checks and released validation. Publish the exact
proposal and findings in draft PR #543; no completion or verification is implied.
