# Test-copy qualification assessment

**The correction still fails content review and failure reporting.** Further
native trials on this candidate stopped under VER-HAG-008. WO-HAG-011 remains
in progress. No completion or human verification is claimed.

Candidate: `f834c76a153466c3db557282c9610cb05ff0314d`.
Governor: released 0.22.1, used outside the checkout.
Executor: Codex under mmzen's existing WO-HAG-011 and draft-PR authority.

## Change and observed result

Three sentences in `setup/references/hosted-context.md` clarify that synthetic
drafts must meet the normal type checklist and that imported drafts may be
incomplete. The addition is 234 bytes. The task, fixture, model, permissions,
driver and acceptance criteria remain unchanged.

| Case | Result | Seconds | Calls | Peak input tokens |
| --- | --- | ---: | ---: | ---: |
| Claude EFF-04A, claude-141 | Content and reporting fail | 225.493 | 12 | 58,920 |
| Codex EFF-04A | Not run after the failure | — | — | — |
| All EFF-04B cases | Not run after the failure | — | — | — |

Claude Code 2.1.273 used `claude-opus-4-6` and candidate plugin 0.2.7.
Its live authentication probe passed. The host's installed plugin was unchanged.

The saved intent invents an absence of recorded confirmation and an effect on
downstream verification and release. It uses inspecting the greeting as its
success measure. The report acknowledges that this is an engineering check,
then treats the synthetic fixture as an exception to an operational observation.
Both report and final reply claim complete content and no missing inputs.
These claims fail the unchanged EFF-04A criterion.

There was also one failed tool call: the helper rejected `create-artifact
--dry-run` with exit 2. The report and final reply incorrectly claim no failed
calls. The agent did not call the available observations operation before making
that exhaustive claim. No permission denial was observed.

Independent service reads confirm the exact submitted bytes, one new draft at
project version four, seven unchanged imported records and unchanged staged
inputs. No lifecycle decision was exercised. The two owned containers were
stopped after identity checks; their volumes remain preserved.

## Cost and checks

The exact 63,039-byte entry reached stdin. It contained all 12 fixture files,
nine released instruction sections and four selected references. Both host
archives contain the committed guidance. This establishes explicit test-input
delivery; it does not qualify startup or compaction.

Entry content: 21,262 instruction bytes, 18,810 reference bytes, 5,490 fixture
bytes, 13,305 selection/provenance/label bytes and 4,172 other task bytes.
Initial context was 32,898 tokens. The agent then reread the selection and read
the full authoring file despite receiving the applicable sections. Visible tool
results add 43,926 characters. Captured client commands total 7.557 seconds;
remaining native time is unclassified. These byte, character and token measures
are different quantities.

Build, packaging and client installation took **392.469 seconds**. The source
suite separately took **167.76 seconds**. Neither includes all preparation time.
The negative test meets the call goal and misses the time and context goals used
for comparison. It is not a faster successful authoring result. Single runs from
different candidates do not establish a performance improvement.

- 31 focused tests pass; source suite: 1,336 tests, 24 skips, exit zero.
- Distribution, CLI smoke, scoped checks and review preflight pass.
- Released validation: 1,991 artifacts, zero errors, 63 existing warnings.
- Two builds match. Wheel SHA-256:
  `1535d83ee10abc82b7643f779892eb36bc8bbee9d4270e77cddaa21eddc511b5`.
  Source archive SHA-256:
  `fdb096a5cd7f4f0f62f37207fe27f41e1fcbf9ef70f18d1b2896414d87f63278`.
- All 127 wheel member payloads match candidate15. EFF-02/03 reuse is limited
  to those identical runtime contents, not changed plugin/native behavior.

## Diagnosis and proposed next direction

Three consecutive wording candidates have failed the missing-input case. More
prohibitions have not established reliable behavior. The content defect remains
real under the accepted contract; changing that verdict is not proposed.

Two competing cues warrant review before another expensive candidate:

1. The request asks for an intent about confirming a greeting, and the imported
   intent uses observing that greeting as its outcome. The assessor correctly
   applies the stricter missing-operational-outcome criterion, but the input also
   demonstrates the engineering activity as an intent. The new warning did not
   resolve this tension.
2. Released local authoring instructions show a creation preview with `--dry-run`.
   The remote tool table has no such option. This run combined the two interfaces.
   The retained call establishes the mismatch; it does not prove its internal cause.

The next proposal should separate task correctness from transport efficiency:

- Keep a missing-input test, but review a linked VER amendment with a new,
  unambiguous change request. For example: an operator requests a French-language
  greeting alongside the existing English greeting; prepare one intent draft from
  that request and the fixture. Do not supply the expected missing answer. Keep
  the same requirement to identify an unsupported operational outcome or measure.
  Preserve the original test and every failed result as historical evidence.
- Present one remote command route while retaining the canonical content rules.
  Make local command applicability explicit. Retain complete evidence in files;
  show concise findings and exact file pointers to the agent. Do not add another
  review layer or duplicate checklist.
- Review redundant entry metadata and repeated reads before adding instructions.
  Treat reproducible package preparation as a separate cost and assess whether
  unchanged components can be reused under the existing identity rules.

These are proposals, not applied changes or an amendment approval. Changing the
approved diagnostic task requires a linked artifact revision and mmzen's authority.
Any change to canonical instructions or component-identity rules also needs its
own bounded scope. Existing acceptance thresholds remain unchanged.

## Continuation and review status

The released result remains `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`.
The failed native criterion prevents a completion claim. WO-HAG-009/010's full
NQ qualification also remains incomplete.

PR #543 remains draft, source `codex/hosted-agent-qualification`, target `main`.
At the preceding published head `ec4dda0e3ece1e86a00919282731f6264ccb1c91`,
harness CI fails because WO-HAG-009 lacks handoff evidence for formal snapshot
`43ac4367bd99feaa6fe71b6ecd5aad9d04420ecc5cbab612b51068641670935f`.
New-head CI must be assessed separately. No replacement handoff packet is created
to conceal incomplete qualification.

- [Independent assessment](claude-141-assessment.json)
- [Visible transcript](claude-141-visible.md)
- [Native evidence](claude-141-evidence.zip) and [inventory](claude-141-inventory.json)
- [Commands and comparisons](candidate20-checks.zip) and [inventory](candidate20-checks-inventory.json)
- [Publication checks](candidate20-publication-checks.zip)

The archives retain exact selected evidence. Private reasoning, raw native event
streams and credential files are omitted. Original private evidence is preserved.
Known sandbox tokens and provider-token prefixes were checked absent.
