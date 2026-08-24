# `WO-HBI-004` implementation evidence

Retained under `WO-HBI-004`. Every figure below was produced by running the command
named beside it in a checkout created with `git worktree add`, which inherits
`core.autocrlf=true` on this workstation and is the construction
`.github/workflows/publish-pypi.yml` uses to qualify a release candidate. A green
suite in an LF checkout proves nothing about this work order, because the defect is
invisible there.

Branch checkout: `C:\Users\mathi\se_harness-hbi004`, created from `origin/main` at
`ee8aea1d32584d9cf9c9cbda1aeef3dc3207bc3f`.
Control checkout: `C:\Users\mathi\hbi004-control`, `git worktree add --detach
origin/main`, the same commit with none of this work order's changes.

## The silent pass, measured rather than argued

This is the finding this work order exists for, and it is stated first because it is
the one that is easy to lose. In the control checkout, at plain `origin/main`, with
`WO-HBI-003` merged and its guard present:

```
i/lf w/crlf attr/    templates/repository/standard/.agents/skills/harness-draft-change/agents/openai.yaml
i/lf w/crlf attr/    templates/repository/standard/.agents/skills/harness-execute-work-order/agents/openai.yaml
i/lf w/crlf attr/    templates/repository/standard/.agents/skills/harness-prepare-assurance/agents/openai.yaml
```

```
python -m unittest discover -s tests -p "test_hash_bound_integrity.py" -k ByteExactSurfaceTests
Ran 3 tests in 0.073s
OK
```

Three committed files whose exact bytes the suite compares resolve no attribute, are
materialized converted, and `ByteExactSurfaceTests` reports `OK`. The guard was not
wrong about anything it asserted. Its inventory was the declared patterns, so the
three paths were not in the set it asserted over, and a set derived from the rules
cannot contain a file the rules miss.

The same checkout's full suite does fail, on the assertion itself:

```
python -m unittest discover -s tests -p "test_*.py"
Ran 807 tests in 302.093s
FAILED (failures=3, skipped=22)

FAIL: test_closed_phase3_contracts_and_manifests_validate (skill='harness-draft-change')
FAIL: test_closed_phase3_contracts_and_manifests_validate (skill='harness-execute-work-order')
FAIL: test_closed_phase3_contracts_and_manifests_validate (skill='harness-prepare-assurance')
AssertionError: b'policy:\n  allow_implicit_invocation: false\n'
             != b'policy:\r\n  allow_implicit_invocation: false\r\n'
```

So the detector that worked was the byte-exact assertion in a CRLF checkout, and the
detector that was built to catch a missing rule did not. That asymmetry is recorded in
`VER-HBI-001`'s second amendment as the residual this work order narrows rather than
closes.

## Why no recorded digest binds these paths

`REQ-HBI-001` triggers on a file whose bytes a recorded SHA-256 binds. These three do
not meet that trigger, and the reason was measured rather than assumed.
`se_harness/skill_contract.py:671` normalizes `\r\n` and `\r` to `\n` before hashing,
so `build_skill_manifest`'s per-file and manifest digests are newline-insensitive. The
retained portable-core vectors in
`tests/fixtures/agentic_execution/phase3/portable_vectors.json` therefore match on a
CRLF checkout, and `test_all_four_portable_cores_match_retained_phase3_vectors` passed
on the hosted `windows-2022` leg in the same run in which the byte-exact assertion
beside it failed. Four failures, two names, and this is why the manifest test is not
one of them.

They are in scope through this domain's `README.md` scope boundary, which
`WO-HBI-003` widened on 2026-08-24 with the owner's `Accept both` to admit committed
files whose exact bytes the candidate suite compares without a recorded digest binding
them. No further widening was needed and none was made.

## The rule, measured before it was written

The framing the owner decided over named a `*.yaml` rule. A fourth per-extension rule
removes this instance and leaves the mechanism that produced it, so the rule declared
is the tree:

```
templates/repository/standard/.agents/skills/** text eol=lf
```

Measured first, in a throwaway probe repository at `C:\Users\mathi\hbi004-pattern-probe`
carrying only that one rule, committed LF, then re-materialized under
`core.autocrlf=true`:

| Probe path | `git ls-files --eol` |
|---|---|
| `…/skills/harness-draft-change/agents/openai.yaml` | `i/lf w/lf attr/text eol=lf` |
| `…/skills/harness-draft-change/SKILL.md` | `i/lf w/lf attr/text eol=lf` |
| `…/skills/harness-draft-change/scripts/guard.py` | `i/lf w/lf attr/text eol=lf` |
| `…/skills/harness-draft-change/skill-contract.json` | `i/lf w/lf attr/text eol=lf` |
| `…/skills/deep/a/b/c/thing.toml` | `i/lf w/lf attr/text eol=lf` |
| `templates/repository/standard/.agents/other.yaml` | `i/lf w/crlf attr/` |

The pattern reaches every depth and every extension inside the tree, including an
extension no rule has ever named four directories down, and reaches nothing one
directory outside it. That last row is the one that matters for scope: the rule does
not leak.

Applied to this repository and the tree re-materialized with `rm` plus
`git checkout --`, all fifteen tracked files under it report
`i/lf w/lf attr/text eol=lf`, where the control reports twelve of those and three
`i/lf w/crlf attr/`.

**No blob changed.** `git diff --name-only origin/main` lists no path under
`templates/`, and every file in that tree was already `i/lf`. The rule changes what a
checkout presents, not what the repository stores. That was the stated stop condition
in `WO-HBI-004`'s decision envelope and it did not trigger.

## The guard's inventory, and the deviation from the framing

The framing said the inventory should derive from the suite's byte-exact assertions.
It does not, and this is the second disclosed deviation.

Deriving from the assertions means resolving the path expression in each one. The
assertion that caused this defect is

```python
self.assertEqual(
    b"policy:\n  allow_implicit_invocation: false\n",
    (root / "agents/openai.yaml").read_bytes(),
)
```

at `tests/test_agentic_execution.py:143`, inside `for name, root in PHASE3_ROOTS.items()`.
`root` is a loop variable over a dictionary comprehension. No static scan resolves it
without guessing, and a guard that guesses fails for reasons that have nothing to do
with bytes. That was the measurement behind rejecting the framing's mechanism, not a
preference.

What replaced it is the tracked set. `BYTE_EXACT_FILES` holds the four named paths
`WO-HBI-003` declared individually; `BYTE_EXACT_TREES` holds one prefix; the inventory
is the named files that are tracked plus every tracked path under a prefix, read from
`hash_bound.tracked_paths` and never from `.gitattributes`.

What that closes: a file of any extension added anywhere inside a declared tree is in
the inventory the moment it is tracked, so it needs no new rule and an uncovered one
is a failing test. That is exactly the case that produced this work order.

What it does not close: a byte-exact assertion on a path in no declared tree and no
named file. `VER-HBI-001`'s residual-uncertainty section states this and names the
detector that does cover it — the full suite in a `core.autocrlf=true` checkout, which
is what caught this instance and what scenarios 8 and 9 require.

One further change the guard needed. `committed_attributes()` reads
`HEAD:.gitattributes`, deliberately, so a CRLF checkout cannot feed converted
attribute bytes into a synthetic repository. A test *of the rules* cannot use it: read
from `HEAD`, the new negative case reported the previous commit's coverage and went red
until the rule change was committed. That was observed, not predicted —
`test_a_novel_extension_in_a_byte_exact_tree_needs_no_new_rule` failed with
`'set' != 'unspecified'` on both probe paths on its first run. It now reads the working
tree through a new `working_tree_attributes()` helper, which normalizes newlines and
leaves `committed_attributes()` untouched for every other case in the module.

## The negative case: the new guard against the old rules

`VER-HBI-001` scenario 9, measured before the scenario was written. The tree rule was
replaced with `WO-HBI-003`'s three per-extension rules, the tree re-materialized, and
the class run:

```
python -m unittest discover -s tests -p "test_hash_bound_integrity.py" -k ByteExactSurfaceTests
Ran 6 tests in 0.586s
FAILED (failures=8)
```

Eight failing assertions across three of the six tests, against the same repository
state that the old guard reported `OK` for:

| Test | Failures | What each names |
|---|---|---|
| `test_a_novel_extension_in_a_byte_exact_tree_needs_no_new_rule` | 2 | `'set' != 'unspecified'` for the probe `.yaml` and the unseen extension |
| `test_every_surface_resolves_the_required_attribute` | 3 | each `agents/openai.yaml` path, `{'text': 'unspecified', 'eol': 'unspecified'}` |
| `test_no_surface_is_converted_in_this_working_tree` | 3 | each `agents/openai.yaml` path, `is crlf` |

The tree rule was then restored and the tree re-materialized before any other
measurement was taken.

## The reserved-name defect, fixed under the same decision

`test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths` writes
`NUL.txt` into a copied skill tree and asserts `SKM003`. On this workstation, Windows 11
build 26200 with CPython 3.14.6, that write produces a real file that `iterdir()`
enumerates, `_portable_files` sees the entry, and the refusal is reached. On hosted
`windows-2022` with CPython 3.11 the reserved device basename resolves to the device:
the write succeeds, no `OSError` is raised, nothing is left to enumerate, and the
assertion cannot be reached. The `try`/`except OSError`/`else` shape treated a
successful write as proof the entry existed, which is true on one image and false on
the other.

The product is not changed. `se_harness/skill_contract.py:612` refuses a reserved
component wherever one can be enumerated, and that is correct: on `windows-2022` such a
file cannot appear in a skill tree at all. The defect is the test's precondition.

Two changes, and the coverage moves up rather than down:

- The filesystem branch now asserts its own precondition —
  `reserved.name in {entry.name for entry in root.iterdir()}` — and exercises the
  enumeration path only where the entry is a real file.
- `test_reserved_path_components_are_refused_on_every_platform` asserts the refusal
  directly against `_validate_component` for `NUL.txt`, `nul`, `CON`, `PRN.md`,
  `aux.json`, `COM1.py` and `lpt9.yaml`, and asserts that `openai.yaml`, `SKILL.md`,
  `skill-contract.json` and `nullable.py` are accepted so the test cannot pass
  vacuously. It mirrors `AgentContractTests.test_portable_paths_fail_closed`, which
  already asserts the same class of refusal for agent contracts without touching a
  filesystem.

Before this work order the reserved-name refusal was asserted on exactly one component
and only where a reserved basename can exist as a file. After it, seven components are
asserted on every platform and one is still asserted through the enumeration path where
that is possible. `VER-AEX-001` already requires reserved-name paths to be exercised;
this brings the suite into conformance with that pass condition and adds none, so no
`VER-AEX-001` amendment was needed or made.

What is not measured here: the hosted image itself. This workstation cannot reproduce
the `windows-2022` behaviour, because on it the write produces a real file. The fix is
verified locally in the branch where the precondition holds, and the branch where it
does not is measured by `WO-RLO-005`'s rehearsal lane on the runner. That is stated as
a bounded gap rather than claimed as proof.

## Measured on this branch

| Measurement | Control at `ee8aea1` | This branch |
|---|---|---|
| Full suite, `git worktree` checkout, `core.autocrlf=true` | 807 tests, 3 failures, 22 skipped | **811 tests, OK, 22 skipped** |
| `tests/test_hash_bound_integrity.py` | 99 tests, OK, 1 skipped | 102 tests, OK, 1 skipped |
| `tests/test_agentic_execution.py` | 27 tests, 3 failures, 2 skipped | 28 tests, OK, 2 skipped |
| `ByteExactSurfaceTests` | 3 tests, OK — while three surfaces are `w/crlf` | 6 tests, OK — no surface converted |
| Tracked files under the skills tree resolving `text eol=lf` | 12 of 15 | 15 of 15 |
| Byte-exact inventory size | 4 named + 12 by pattern | 4 named + 15 by tree |
| Governing validator, released `0.6.0` evaluator from outside the checkout | — | PASS, 822 artifacts, 0 errors, 50 maintenance warnings |
| Candidate validator | — | PASS, same 822 / 0 / 50 |
| Governing preflight | — | PASS at phase `start` while `in_progress`, and PASS at phase `review` once `implemented` |
| Governing `doctor` | — | exit 0, 87 checks, 0 `FAIL`, `managed:.gitattributes: unchanged` |
| In-tree `doctor` | 81 `PASS` / 28 `FAIL` | 81 `PASS` / 28 `FAIL`, byte-identical `FAIL` set |
| `validate_release_distributions.py --root .` | — | PASS, 1 distribution-bearing record |

The four extra tests are three new methods in `ByteExactSurfaceTests` and one new
method in `SkillContractTests`. The in-tree `doctor` `FAIL` set is inherited
candidate-versus-released boundary skew: `diff` over the two `FAIL` lists is empty, so
this work order neither caused nor repaired any of it. The governing run, which is the
one that carries a verdict, has none.

## What this predicts for the hosted lane, and what it does not

`WO-RLO-005`'s rehearsal on `windows-2022` failed `candidate-unit-suite` with four
failures over 928 tests, reported as two names. Three were the `agents/openai.yaml`
sub-cases and one was the reserved-name test. Both causes are fixed here.

The prediction is therefore that the Windows leg reports `REHEARSED` once this work
order is on `main` and `WO-RLO-005`'s branch has merged it. That prediction is stated
as a prediction. It is not measured by this work order, which opens one pull request and
runs no rehearsal, and the sequencing decision that puts this work order first is what
makes it measurable at all. The suite count will differ from 811 there: the rehearsal
runs the candidate suite inside its own derived checkout and reported 928, and the hosted
legs report 10 skips where this workstation reports 22, so a skip or test count from this
evidence should not be carried across.

## Actions explicitly not performed

No `VREC` was prepared, transitioned or bound. `WO-HBI-004`'s
`commit_bound_verification` is `required` and unmet.

No merge, no tag, no GitHub Release, no PyPI publication, no Pages deployment, no
environment approval, no orchestrator workflow dispatch, no promotable distribution
build, no governor adoption, no credential use, and no maintenance mutation.

No product source file was changed. No committed file's bytes were converted. No
recorded digest, `VREC`, `RLS`, `REL` or evidence fact was rewritten or repointed. No
hash-bound class was added, removed or changed, and `build_recipe_sha256` remains in
`unbound_digest_fields` with repository issue 142 still open over it.

`WO-RLO-005`, its packet and its branch are untouched. Re-merging `main` into
`feat/rlo-004-publication-rehearsal` and re-running its rehearsal are that work order's
acts under its own authorization, and the owner's sequencing decision places them after
this work order merges — which is the owner's act, not authorized here.

No byte rule was declared for `templates/repository/standard/.claude/skills/`. Measured:
the suite reads those four `SKILL.md` files with `read_text` and substring assertions
rather than byte for byte, they are `i/lf w/crlf` in the control and in this branch, and
the suite passes over them converted. Declaring a rule there would exceed the inventory
this work order authorizes.
</content>
