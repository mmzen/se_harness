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
