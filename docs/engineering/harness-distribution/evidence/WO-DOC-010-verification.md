# Verification evidence for WO-DOC-010

Date: 2026-08-13

## Authorization and lineage boundary

The accountable repository owner reviewed the documentation gap and the implementation corrections, then instructed `ok go`. `WO-DOC-010` authorizes this follow-up documentation change. Work occurs on local branch `docs/verification-refusal-path`, based on governance commit `b413570694808a05f9b38614cfee485add809684`, so open PR 33 and its remote `docs/update-readme` branch remain unchanged. Candidate `1e3790f746e0a8fa75a00ab6b0db371a39a63675` and ready `VREC-DST-006` retain their original scope and bytes.

After reviewing the completed result, the owner instructed `ok, push to PR`. This separately authorizes the clean follow-up candidate commit, normal branch push, and one new pull request. While PR 33 remains open, the follow-up PR is intentionally stacked against `docs/update-readme`; it can be retargeted to `main` after PR 33 merges without changing the original candidate or VREC.

## Implemented result

- `docs/notes/harness-operational-phasing.md` adds one proportionate, cross-linked `When verification is refused` section after the phase table.
- Refusal is a withheld `ready -> verified` decision, not a fabricated `rejected` VREC; the completed work order remains `implemented`.
- Formal work-order and release gates are distinguished from the ability to prepare a non-eligible ready RLS.
- Uncommitted generated VRECs, committed ready VRECs, supporting evidence, supersession, replacement candidates, and definition-artifact rejection are distinguished.
- Coverage-based `W-REV-004` behavior is described as derived and non-authoritative.
- The current retained-ready-RLS limitation is reported rather than resolved in prose.
- `docs/notes/harness-branching-model.md` adds only the Git-topology consequence after Phase 3, with no diagram: `main` remains append-only, a correction is a later bounded candidate, and a severe-defect revert is itself a candidate.
- `tests/test_progressive_documentation.py` adds stable assertions for those distinctions and preserves exactly two `gitGraph` occurrences.

## Independently inspected implementation and policy facts

| Fact | Inspected source | Result |
| --- | --- | --- |
| VREC status vocabulary excludes `rejected` | `scripts/validate_engineering_artifacts.py:495-502` and `docs/engineering/WORKFLOW.md:18,24` | Confirmed: `ready`, `verified`, `released`, or `superseded` only |
| `implemented` records completed work and evidence | `docs/engineering/WORKFLOW.md:16` | Confirmed; it is not a correctness claim |
| work-order assurance coverage | `scripts/validate_engineering_artifacts.py:646-664` | Confirmed: a `verified` or `released` work order requires a verified or released VREC |
| RLS/VREC identity and release eligibility | `scripts/validate_engineering_artifacts.py:822-860` | Confirmed: commits and object formats agree; a released RLS requires every included VREC to be verified or released |
| early release proposal behavior | `se_harness/provenance.py:336-434` | Confirmed: `prepare-release` accepts ready, verified, or released VRECs and writes a ready RLS |
| evidence is not a formal status-bearing artifact | `scripts/validate_engineering_artifacts.py:93,203-218` | Confirmed: `evidence` directories are excluded from formal artifact discovery |
| VREC supersession constraints | `scripts/validate_engineering_artifacts.py:503-539,757-786` and `docs/engineering/WORKFLOW.md:24` | Confirmed: only explicit accountable supersession to one covering verified or released VREC is eligible; captured provenance stays unchanged |
| stale-ready Explorer observation | `scripts/generate_harness_dashboard.py:669-690` | Confirmed: `W-REV-004` requires an already covering verified or released record and performs no transition |
| rejection and active coverage | `scripts/validate_engineering_artifacts.py:40-58,697-718` | Confirmed: `rejected` is global vocabulary but excluded from active coverage; active dependants must be reconciled |

## Current-model limitation retained explicitly

The CLI and validator allow a ready RLS proposal to include a ready VREC, even though the managed workflow orders release preparation after accountable verification. If that RLS is committed and the VREC is later refused, changing the VREC to `superseded` makes the active RLS reference invalid, while the RLS lifecycle provides only `ready` and `released`. The documentation therefore recommends not retaining the RLS until the VREC is verified and directs an existing case to stop and escalate. This work does not invent an RLS rejection or supersession transition and does not change behavior.

## Checks and retained results

| Check | Result |
| --- | --- |
| `python -B -m unittest tests.test_progressive_documentation tests.test_public_onboarding` | PASS: 28 tests |
| `python -B -m unittest discover -s tests -p "test_*.py"` | PASS: 141 tests with 3 conditional skips |
| `python -B -m se_harness validate .` after final `implemented` transition | PASS: 269 artifacts, 0 errors, 38 classified historical warnings |
| `python -B -m se_harness doctor .` | PASS: required, distributed, managed, and pinned-governor integrity checks passed; existing location advisories remained nonblocking |
| start preflight for `WO-DOC-010` | PASS while the work order was `approved`; complete governing manifest returned |
| review preflight for `WO-DOC-010` | PASS both while `in_progress` and after the final `implemented` transition; complete governing manifest returned |
| `python -B -m se_harness --help` | PASS: current command surface includes `capture-verification` and `prepare-release` |
| Markdown links and note structure | PASS through focused progressive-documentation tests |
| branching diagrams | PASS: exactly two `gitGraph` occurrences; no refusal-path diagram added |
| protected managed/runtime path diff | PASS: no protected path changed |
| `git diff --check` | PASS after final evidence retention |
| final deterministic Explorer generation twice | PASS twice: 269 artifacts, 944 relations, 0 errors, 39 derived warnings, identical snapshot `ad725245d3e17dd42836ff7cd581a453328db0006f094340094b26a6914a64f7` |

The 38 formal warnings are pre-existing legacy architecture and canonical-location compatibility findings. This documentation change neither causes nor resolves them.

## Manual reader review

At the 6/10 operational level, the section answers the first refusal questions in lifecycle order without copying managed policy: what refusal means, why the work order remains implemented, what blocks release, what differs before and after VREC commit, how later supersession works, and why a new candidate is needed. It cross-links the conceptual relation and Git consequence.

At the branching guide's 6.5/10 document level, the added paragraph stays limited to topology. It preserves the sole illustrative trunk-based model, explains append-only correction and revert behavior, and delegates lifecycle mechanics back to operational phasing.

## Authority boundary

This evidence records implementation completion for `WO-DOC-010`. At evidence completion, it did not verify a commit, transition or supersede a VREC, prepare or approve an RLS, modify PR 33, commit, push, merge, rewrite history, tag, publish, or deploy. The later `ok, push to PR` instruction authorizes only the clean candidate commit, normal push of `docs/verification-refusal-path`, and one new pull request; it does not authorize VREC capture or transition, merge, release activity, tag, publication, or deployment.
