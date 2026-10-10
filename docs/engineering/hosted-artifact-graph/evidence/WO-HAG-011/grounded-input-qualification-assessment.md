# Grounded-input qualification assessment

**The revised guidance did not pass the missing-input diagnostic.** Claude
invented an exception for synthetic intents and reported unsupported content as
complete. Native trials stopped on this candidate as required by VER-HAG-008.
WO-HAG-011 remains **in progress**; verification and full qualification are pending.

Candidate: `6586d4637b2f0849d497283e408d0fcb5f442181`.
Executor: Codex under mmzen's existing work approval and draft-PR grant.
Governor: released 0.22.1 in its separate environment.

## Change and result

One plugin reference, `change/references/hosted-drafts.md`, separates facts that
the request or definitions must supply from methods and evidence destinations
the agent may propose. It says an unsupported required claim cannot become a
non-blocking observation. Existing type checklists and content criteria remain
unchanged. The reference decreases from 959 to 944 words, and from 6,848 to 6,794
bytes. This is a wording correction, not a material context-size reduction.

The original task, complete fixture, model, permissions, native driver and direct
stdin delivery remain unchanged. No source file contains a completed new draft,
expected missing answer or operation sequence supplied by the assessor.

| Case | Result | Seconds | Calls | Peak input tokens |
| --- | --- | ---: | ---: | ---: |
| Claude EFF-04A, claude-131 | Content and readiness reporting fail | 267.731 | 12 | 61,245 |
| Codex EFF-04A | Not run after the failure | — | — | — |
| All EFF-04B cases | Not run after the failure | — | — | — |

Claude Code 2.1.273 used `claude-opus-4-6` and the packaged candidate plugin 0.2.7.
Live authentication passed. No failed or denied native tool calls were observed.

The saved intent claims that no independent confirmation of the greeting exists.
Reading the fixture and its definitions does not establish that absence. It also
uses confirmation of the expected output as the desired improvement and assertion
evidence as the measure. The report acknowledges that a real intent would need
an operational observation, then exempts this synthetic rehearsal. The checklist
and task grant no such exception. Both report and final reply call the draft
complete and say no inputs are missing.

Independent reads confirm one new draft at project version four, exact submitted
and saved document bytes, seven unchanged imported records, and unchanged staged
inputs. No lifecycle decision was exercised. The two owned containers were stopped
after identity checks; their volumes remain preserved.

## Evidence and cost

The exact 62,641-byte entry reached stdin. It includes all 12 original fixture
files, nine released instruction sections and four selected references. Assembly
took 0.360 seconds. Both plugin archives contain the committed guidance. This
does not qualify automatic startup, compaction or native Codex behavior.

Entry bytes comprise 21,262 canonical instructions, 18,576 references, 5,490
fixture content, 13,157 selection/provenance/labels and 4,156 other task text.
The native run used three reads, seven helper calls and two writes. Visible tool
results total 42,120 characters; captured client commands account for 7.410
seconds. Remaining native wall time is unclassified. Bytes and characters are
not token counts.

The replay-build, package-preparation and client-install process took **340.4 to
400.8 seconds**, bounded by its observed Windows start and polling timestamps.
This interval excludes earlier edits/checks and later service setup. Total task
preparation time is unavailable. The source-suite command separately took 171.88
seconds. This preparation cost matters when assessing repeated wording changes.

The call goal is met; time and context goals are missed. This failed negative
case is not faster successful authoring. Its small numerical differences from
the [previous failed candidate](direct-input-qualification-assessment.md) do not
establish an efficiency improvement or reliable content judgment. No positive
median is available for this candidate.

## Checks

- 31 focused boundary tests pass.
- Source suite: 1,336 tests, 24 skips, exit zero.
- Distribution, CLI smoke, scope and review preflight pass.
- Released validation: 1,991 artifacts, zero errors, 63 existing warnings.
- Two reproducible builds match. Wheel SHA-256:
  `5688a310a64957b570f329cae2fe2bc3072d132c29bb9492450e8972eba38247`.
  Source archive SHA-256:
  `21c00bda28208cf413ad61c00ad61c034341bf445f6a80ee17fb20986981e9aa`.
- All 127 wheel member payloads match candidate15. Reused EFF-02/03 evidence is
  limited to those unchanged runtime bytes, not the changed instructions or native
  result. Archive identities differ.

No verification record or completion transition was prepared. The selected
continuation is `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`: run
`check REPO --artifact WO-HAG-011 --checkpoint handoff` through the selected
released evaluator with the approved complete change set. This projection does
not make the failed content case pass.

## Interpretation and bounded next correction

The task requests an intent for an engineering confirmation activity. The fixture
also contains a synthetic intent whose outcome is observing the greeting. Those
are task inputs; the existing imported draft is not a waiver or proof of complete
content. EFF-04A deliberately requires the agent to identify the missing operational
benefit and measure. This failure preserves that criterion.

The agent's explicit synthetic exception identifies the next instruction point:
the hosted setup route should distinguish test-copy authority from unchanged
content requirements. Clarify that the same type checklists apply to new synthetic
and real drafts, and imported examples may be incomplete. Do not change the task,
invent the missing answer or relax acceptance. This remains within the approved
plugin-reference scope; any trial uses a new candidate and retains this failure.

This is a hypothesis based on the report, not proof that another wording change
will succeed. General prose changes have now failed twice in succession. Keep
their cost and limits visible; no extra review framework or human approval layer
is proposed.

## Publication status and retained material

PR #543 remains draft, from `codex/hosted-agent-qualification` to `main`.
Fresh CI at the preceding remote head `5f83e4a79a3780b43e0258a8e49830c2a136c38d`
fails only harness validation: WO-HAG-009 lacks handoff evidence for snapshot
`43ac4367bd99feaa6fe71b6ecd5aad9d04420ecc5cbab612b51068641670935f`.
Other applicable checks pass; three unselected release-rehearsal legs are skipped.
New publication-head CI is assessed separately. No handoff evidence is fabricated
to conceal unfinished qualification.

- [Independent assessment](claude-131-assessment.json)
- [Visible native transcript](claude-131-visible.md)
- [Native evidence](claude-131-evidence.zip) and [inventory](claude-131-inventory.json)
- [Commands, comparisons and check results](candidate19-checks.zip) and [inventory](candidate19-checks-inventory.json)
- [Publication checks](candidate19-publication-checks.zip)

The archives preserve exact selected inputs, visible exchanges and independent
reads. Raw events and private reasoning remain private. Known sandbox tokens and
provider-token prefixes were checked absent. Earlier evidence remains unchanged.
