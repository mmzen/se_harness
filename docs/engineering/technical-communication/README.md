# Technical Communication Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes one managed technical-communication policy and the first
portable skill that consumes it. The policy uses selected ASD-STE100-based
clarity principles. It does not claim ASD-STE100 compliance, bundle or download
the standard, or permit writing style to change engineering authority or
technical meaning.

## Draft definition packet

- `INT-TCM-001`: make agent communication clear without weakening precision or authority.
- `CAP-TCM-001`: let supported agents produce clear operator briefs and readable technical prose from one managed policy.
- `REQ-TCM-001`: distribute one managed ASD-STE100-based communication policy.
- `REQ-TCM-002`: preserve protected content and technical meaning.
- `REQ-TCM-003`: apply distinct operator and technical-artifact profiles.
- `REQ-TCM-004`: provide the explicit read-only `harness-operator-brief` skill.
- `SPEC-TCM-001`: define the policy, profile, skill, installation, and failure contracts.
- `ARCH-TCM-001`: separate managed communication authority from replaceable skill and runtime execution.
- `ADR-TCM-001`: select one managed policy consumed by non-authoritative skills.
- `VER-TCM-001`: verify integrity, protected-content preservation, skill boundaries, meaning, and usability.
- `WO-TCM-001`: implement the complete bounded first increment after approval and an explicit start decision.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, network access, standard download, or
external action.

`REQ-TCM-005`, `SPEC-TCM-002`, `VER-TCM-002` and `WO-TCM-003` are drafted and approved on 2026-08-31 for [issue #281](https://github.com/mmzen/se_harness/issues/281) item #281b, the last piece of the functional assessment's FA-2: a generated diagnostic-code index. `repository_tools/diagnostic_code_index.py` parses the candidate source's string literals (comments and identifiers never contribute), keeps a curated registry of the diagnostic prefixes, derives the run-time-composed record-preparation codes from the same source facts, and renders `docs/notes/diagnostic-codes.md` deterministically; `tests/test_diagnostic_code_index.py` fails the suite on any drift. Artifact and specification identifiers, which share the code shape, are excluded by construction. The page is linked from the notes index and beside the `check` note's small refusal table. The hash-locked root `scripts/` copies are the released evaluator's files and are not scanned.

`WO-TCM-004` (2026-09-04) registers the `E-DCM` and `W-DCM` families that `WO-DCM-001` added to the validator, under the existing `REQ-TCM-005`, `SPEC-TCM-002` and `VER-TCM-002`, regenerates the index, and adds the unregistered-family guard that closes the residual uncertainty `VER-TCM-002` recorded: a hyphenated diagnostic family present in the source but absent from the registry now fails `--check` and the pinning test. The approved work order is on main (PR #331); its execution travels the delegated route on the branch `wo/tcm-004-execution`, where the delegated start follows once the required check is green at the branch head.

## Reader-first requirements and the repository-owned glossary (2026-09-04)

The assessment `docs/notes/assessment-requirement-readability-2026-09-04.md`
measured the 328 requirements and the owner's questions on it settled three
points: the `Open decisions` section goes away now that decisions are
artifacts; a requirement carries one acceptance condition, not a criteria
list, which lives in the verification contract; the glossary is repository
content, generated from the repository's own corpus and never distributed.
This packet carries them.

- `REQ-TCM-006`: a requirement the reader understands on first reading;
  draft-time advisories for shape and word budgets.
- `REQ-TCM-007`: a repository-owned glossary, seeded empty, grown from the
  corpus, reported when it lags, never carried by the distribution.
- `REQ-TCM-008`: pending decisions are read from the decision graph; the
  `Open decisions` section is retired from the templates and the gate.
- `SPEC-TCM-003`: rules `TCM-RFR-001` to `TCM-RFR-010`.
- `VER-TCM-003`: the evidence contract for the three requirements.
- `WO-TCM-005`: the template shape, the advisories, the Explorer rendering,
  the section's retirement and the `SPEC-DCM-001` rule 11 amendment.
- `WO-TCM-006`: the glossary seed, the `inspect` vocabulary report, the
  distribution-boundary test and this repository's glossary.

The three requirements are written in the reader-first shape they propose.
They still end with `Open decisions` reading `None` because the root gate of
0.14.0 requires it; that line is the last one of its kind.

On 2026-09-04 the repository owner approved all seven artifacts with the
instruction "i approve the packet, the work orders can be start with
execution delegation" (PR #335). Both work orders carry the delegation
class, so once the packet is on `main` the execution travels the delegated
route: `WO-TCM-005` first, then `WO-TCM-006`, each on its own branch, each
started, completed and recorded by the delegated executor while the
required `validate` check is green at the exact head. The verification
decisions on the records, the merges, the release and the adoption stay
human.

One redundancy is accepted on the record. The blocking of a transition by
an open decision is `REQ-DCM-001`'s obligation, implemented by
`WO-DCM-001`; the first half of `REQ-TCM-008`'s statement restates that
mechanism. The obligation `REQ-TCM-008` adds is the second half only: the
authoring gate requires no `Open decisions` section, the templates drop
it, and `SPEC-DCM-001` rule 11 becomes a legacy rule. The owner reviewed
the alternative on 2026-09-04, rejecting `REQ-TCM-008` and folding the
retirement into `REQ-TCM-006` at the cost of amendment records on
`SPEC-TCM-003`, `VER-TCM-003` and `WO-TCM-005`, and chose to keep the
requirement as approved ("ok for option 1").

`WO-TCM-005` executes on the branch `wo/tcm-005-execution` (PR #336),
opened on 2026-09-04 from `main` after the packet merged. It ships the
reader-first `REQUIREMENT.template.md`, the requirement checklist of
`ARTIFACT_AUTHORING.md`, the advisories `W-AUT-003` (30 words) and
`W-AUT-005` to `W-AUT-010` on drafts, the Explorer's plain-words line
beneath the statement, and the `SPEC-DCM-001` rule 11 amendment that makes
the `Open decisions` section a legacy rule. The authoring gate needed no
code change: it already read the section only where the heading existed.
Its evidence packet is `evidence/WO-TCM-005/`.

`WO-TCM-006` executes on the branch `wo/tcm-006-execution` (PR #337),
opened on 2026-09-04 from `main` after `WO-TCM-005` merged with
`VREC-TCM-005` verified. It ships the glossary seed
`GLOSSARY.md.seed`, installed once per repository at the repository root
and never rewritten (the owner moved it there from `docs/notes/` on
2026-09-04; `SPEC-TCM-003` carries the amendment record); the `inspect` vocabulary section with its harness-term and
English stoplists and the bounded `--vocabulary-threshold`; the upkeep
paragraph of `ARTIFACT_AUTHORING.md`; this repository's glossary grown by
the nine terms the assessment named, each citing the artifact that fixes
its meaning; and the distribution-boundary test that keeps every glossary
entry out of the templates. Its evidence packet is `evidence/WO-TCM-006/`.
The work order carries one amendment record: on 2026-09-04 the owner
confirmed adding `pyproject.toml` to its execution scope, because the
template root is packaged as an explicit file list and the seed needs its
own data-files line. The question was first drafted as `DEC-TCM-001`; the
governing 0.14.0 evaluator refused the file (`E002`, unknown artifact type),
so the decision went through the owner's chat channel and is recorded in
the evidence packet. Decision artifacts become usable in this repository at
the 0.15.0 adoption.

## Reader-first intents and the Explorer's outcome line (2026-09-04)

The assessment `docs/notes/assessment-intent-readability-2026-09-04.md`
measured the 33 intents with the method of the requirement assessment: a
median body of 312 words at reading grade about 16, three template
generations and nine ad hoc shapes, a checklist of four paragraphs against
a template of seven sections, success measures that are acceptance checks
observed "every CI run", no advisory on an intent, and an Explorer that
renders nothing intent-specific. This packet carries its proposal, on the
recommendations the note records: the outcome as a front-matter field,
success measures observed in operation only, advisories first and a later
owner decision on blocking.

- `REQ-TCM-009`: an intent the reader understands on first reading; the
  `outcome` field, the four-section shape and draft-time advisories.
- `REQ-TCM-010`: a success measure outlives the work order; a row observed
  by a CI run, test, validator, verification or implementation review is
  reported as an acceptance check.
- `REQ-TCM-011`: the Explorer shows an intent's outcome and plain words
  beneath its title and derives the G0 intent-quality condition from them.
- `SPEC-TCM-004`: rules `TCM-RFI-001` to `TCM-RFI-007`.
- `VER-TCM-004`: the evidence contract for the three requirements, with the
  33 approved intents as a negative control.
- `WO-TCM-007`: the template, the field, the advisories, the checklist, the
  Explorer rendering and condition, and the regenerated diagnostic index.

The three requirements are written in the reader-first shape. Every
artifact is `draft`; the work order carries the delegation class, so
approving it is the owner's act of delegating its start, completion and
record preparation while the required check is green. No approved intent
is rewritten; the next intent adopts the shape, and an approved one only
when amended for another reason.

On 2026-09-04 the repository owner approved all six artifacts with the
instruction "i appprove the packet" (PR #340). The work order carries the
delegation class, so once the packet is on `main` its execution travels the
delegated route on its own branch, started, completed and recorded by the
delegated executor while the required `validate` check is green at the
exact head. The verification decision on the record, the merge, the release
and the adoption stay human.

`WO-TCM-007` executes on the branch `wo/tcm-007-execution`, opened on
2026-09-04 from `main` after the packet merged (PR #340). Its evidence
packet is `evidence/WO-TCM-007/`.

It ships the reader-first `INTENT.template.md` with the `outcome` field
and the four sections, the intent checklist of `ARTIFACT_AUTHORING.md`
with the two sentences on when a new intent is warranted, the advisories
`W-AUT-011` to `W-AUT-015` and the shared `W-AUT-005`, `W-AUT-007`,
`W-AUT-008` and `W-AUT-009` on intent drafts with the intent budgets, the
`E-AUT-002` refusal of an empty `outcome`, the Explorer's outcome and
plain-words rendering on the record panel and the lineage card, and the G0
`intent_quality` condition derived from an outcome with at least one
success-measure row. The 33 approved intents are unchanged and raise no
advisory. Its evidence packet is `evidence/WO-TCM-007/`.
