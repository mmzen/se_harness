# WO-RLO-008 implementation evidence

artifact: WO-RLO-008
checkpoint: handoff
formal_snapshot_sha256: a4cdb4972a9bc621185116afa552a6bdef5c908db704c784f58901849ba2bf7e

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`), the exact version
  recorded in `.engineering-harness.toml`.
- Candidate: this checkout, `python -m se_harness` from the repository root.
- Host: one Windows 11 workstation, Docker Desktop engine 29.7.2, clone
  configured `core.autocrlf=true`. No POSIX host and no hosted runner were
  used; see deviation 3.

## The defect, as observed before the change

`ARCH-RLO-004` declares a host boundary. The implementation did not achieve it,
in two places, and both changed the accepted bytes of the 0.7.0 release
(`RC-070-01`, GitHub issue #189).

1. `_safe_extract_candidate` ran `git archive` under the caller's effective Git
   configuration, so in a `core.autocrlf=true` clone the export converted every
   text file the checkout converts.
2. The exported tree reached the producer through a bind mount, whose mode
   semantics belong to the host filesystem. `python -m build` and
   `scripts/normalize_sdist.py` both record member modes verbatim —
   `normalized_member` sets name, mtime, ownership, PAX headers, link name and
   device numbers and deliberately not `mode` — and the recipe's `normalization`
   block declares no mode expectation, so nothing downstream corrects a mode.

Measured at the bound candidate `374554d01f9a2e4601dc5b58279a01de2c7b6523`
on this host, over the 1539 files that commit exports:

| Reading | Before | After |
| --- | --- | --- |
| exported files differing from their committed blob | 1462 | 0 |
| exported files carrying CRLF | 1465 | 3 |

The 3 remaining are `docs/images/harness-explorer-{lineage,overview,readiness}.png`,
whose committed blobs contain the CR LF byte pair; each is byte-identical to its
blob, which is the obligation. The 74 paths the export left alone before the
change are exactly the 74 paths `git check-attr --cached eol` reports as `lf` at
that candidate; the set difference is empty in both directions. Every one of the
1539 committed blobs is mode `100644`, so no legitimate executable file exists
and the flat declared mode set is currently exact.

Neither fault is visible inside a replay, and both negative controls below
demonstrate that directly: each produces `state: exact` with build `a` equal to
build `b`. Both builds are exported from the same host, so `SPEC-RLO-004` rule
18's internal-equality comparison passes, and `source_manifest_sha256` hashes
`git ls-tree` output, which is committed blob identity and is blind to what the
export wrote. The only comparison that fails is the one against already accepted
hashes, which runs after a first build has been accepted. That is the recorded
0.7.0 sequence: locally accepted bytes bound to `RLS-SEH-014`, hosted replay
`33015517991` failing, `RLS-SEH-014` rejected, `RLS-SEH-015` bound to a
Linux-built candidate and confirmed by hosted replay `33016585047`.

### Where the mode response has to live

| Reading | Value |
| --- | --- |
| host `chmod 0o755` on a directory reads back as | `0o777` |
| host `chmod 0o644` on a file reads back as | `0o666` |
| the container sees the bind-mounted directory as | `0o777` |
| the container sees the bind-mounted file as | `0o777` |
| after `chmod 0o664` inside the container the file reads | `0o664` |
| the host then reads that same file as | `0o666` |

A Windows filesystem retains no POSIX mode, so an equivalent action on the host
is not a substitute for one taken inside the producer. The same reading also
shows the host cannot observe the mode it just established, which is why the
declared set is asserted inside the producer and not checked from outside it.

### Why `0o775`/`0o664` preserves every accepted byte

`git archive` writes those modes itself. At the candidate the exported tar
carries 1539 file members at `0o664` and 454 directory members at `0o775`, with
no other value; at this checkout's `HEAD` it is 1559 at `0o664` and 456 at
`0o775`. The declared set is therefore the set a POSIX export already produces,
and the mode response is a no-op on a POSIX host rather than a normalization.

## What was built

- `repository_tools/release_build.py`, two edits and two constants:
  - `_safe_extract_candidate` exports with `-c core.autocrlf=false -c
    core.eol=lf` set for that one invocation. `_run_git` already forwards
    leading arguments, so no signature changes and nothing else sees the
    configuration.
  - `_establish_declared_source_modes(source)` sets
    `DECLARED_SOURCE_DIRECTORY_MODE = 0o775` on the source root and every
    directory under it and `DECLARED_SOURCE_FILE_MODE = 0o664` on every file,
    and raises `BuildRecipeError("producer cannot establish the declared source
    mode set")` from any `OSError`. `_producer` calls it after the existing
    input-presence check and before the first recipe command.
  - The recipe, the lock, the producer image, the toolchain, the closed
    environment, the command arrays, the normalizer, the archive-member
    validation, the comparison and the result document are unchanged.
    `_producer` is supplied to the container from the calling working tree, not
    from the recipe, so no bound recipe digest moves; the run below reproduces
    `build_recipe_sha256 = 0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc`.
- `tests/test_release_build.py`, one new class, six tests: exported bytes equal
  the committed blobs in clones with `core.autocrlf` false, true and input;
  the same with `core.eol=crlf` under `* text=auto` with one path pinned
  `text eol=lf`, which stays LF and equals its blob; the declared set replaces
  wrong incoming modes (`0o777`, `0o700`, `0o600`); the declared set is what a
  POSIX export already carries, so the response changes nothing there; the
  producer establishes the set exactly once and before the first recipe
  command; and a failing `chmod` fails the build with no recipe command run.
  Expected values come from `git cat-file blob` and from the literal fixture
  bytes, never from the code under test. The two mode-reading tests are skipped
  on Windows, which cannot read a POSIX mode back. The existing determinism,
  hash, hand-back and refusal tests are unchanged.
- `docs/notes/developing-se-harness.md`: one paragraph in `Building and
  releasing` and one sentence in `Release sequences` (Build), both stating that
  the build of record is host-independent and naming the two mechanisms. Issue
  #189 asks for the opposite instruction — that the build must run on Linux —
  and the note now says explicitly not to re-add a host restriction, because a
  note cannot fail a build.
- `docs/engineering/release-orchestration/README.md`: the `REQ-RLO-017` and
  `WO-RLO-008` bullets in the build-recipe packet.
- Governance in the same commit: `REQ-RLO-017` and `WO-RLO-008` created,
  approved and started; `SPEC-RLO-004` rule 21 and its error row;
  `ARCH-RLO-004`'s host-boundary extension, required pattern, prohibited
  pattern and conformance check; `VER-RLO-004`'s three matrix rows, acceptance
  scenario 7, two property bullets and evidence-retention paragraph. Each
  carries an amendment record. `ADR-RLO-004` is not reopened.

## Commands and results

### The replay of record

Taken with a clean worktree at `904b1b183f38f006cfd251d8e43e2564fd3c58a9`; see
deviation 2 for how that commit relates to this one.

```
python -m repository_tools.release_build replay --repository . \
  --commit 374554d01f9a2e4601dc5b58279a01de2c7b6523 --version 0.7.0 \
  --output-directory <outside the checkout> --result <outside the checkout> \
  --recipe-sha256 0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc \
  --expected-wheel-sha256 e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3 \
  --expected-sdist-sha256 7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617
```

Exit 0, `state: exact`. Builds `a` and `b` both report wheel
`e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3` and sdist
`7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617`, the
identities `RLS-SEH-015` binds. The result also reproduces
`checksums_sha256 = 3021ee7660a7065210e38b629333ca3f438d9afba0236f85c785cf7bf5efbf00`,
`source_manifest_sha256 = 1c0b1dcf49492e9d55570d99bc6fd7a63ca32a2512ab65880869dc6a16e1d075`,
`source_date_epoch = 1787779226`, producer image
`python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`
and observed runtime CPython 3.11.9, linux/amd64, 64-bit. The rebuilt wheel
holds 111 entries recording 41 at `0o100644` and 70 at `0o100664`, none
carrying CRLF — the census of the released 0.7.0 wheel.

A Windows workstation therefore reproduces a bound record's exact bytes. The
hosts differ; the outputs do not.

### The two negative controls

Each removes one half of the response from that same commit's code, runs the
same replay without expected hashes, and restores the file. `git status` was
clean after each.

| Control | Wheel | Sdist | Matches the bound identities |
| --- | --- | --- | --- |
| mode response removed | `57542dd803392cd858b41c45df71c6fb1f4c64455429f66e686df9c94cc284ef` | `3f6eded3f04a96d3fbc0b1d61899159474b55025363c841c0118c846fbcbede3` | no |
| export change removed | `aae9ac542de7d0dde953038f08ddbef88cc90e6f5be02e0251d41387574bc2e0` | `9e7b38e9d15bed11d6009cde1d8b974b1bf2f649a8ae891dad0ca88fa96dd49d` | no |

With the mode response removed the wheel records 41 entries at `0o100644`, 69
at `0o100777` and 1 at `0o100664`, and no CRLF. With the export change removed
it records the correct modes and 83 of its 111 entries carry CRLF. Those are
the 69 and the 83 of issue #189, reproduced deliberately. Both controls report
`state: exact` with `a` equal to `b`, which is the point of `VER-RLO-004`
scenario 7: each half is load-bearing, and the replay's own self-comparison
cannot see either fault.

At unit level the same removals fail the tests. With the export change removed,
both export tests fail on the exported bytes (`b'first\nsecond\nthird\n'` versus
`b'first\r\nsecond\r\nthird\r\n'`). With the mode call removed, the ordering
test and the failure test fail (`BuildRecipeError not raised`).

### Tests and validation

| Command | Result |
| --- | --- |
| `python -m unittest tests.test_release_build.HostIndependentCandidateSourceTests` | 6 tests, OK, 2 skipped (Windows mode readings) |
| `python scripts/run_tests.py` | 1001 tests, OK, 26 skipped, 118 classes |
| `python scripts/run_tests.py` in a control worktree at `7284743` | 995 tests, OK, 24 skipped, 117 classes |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 963 artifacts, 0 errors, 53 warnings, all maintenance-plane |
| `python scripts/validate_release_distributions.py --root .` | PASS, 3 distribution-bearing records |
| `<governor> -I -m se_harness doctor .` | exit 0, 0 FAIL |
| `<governor> -I -m se_harness preflight . --work-order WO-RLO-008 --phase start` | PASS |
| `<governor> -I -m se_harness preflight . --work-order WO-RLO-008 --phase review` | PASS |

The control run is green, so it explains no red. It accounts for the whole
delta: +6 tests and +1 class are the new class, and +2 skips are its two
Windows-only mode readings. The 53 validation warnings are the count an
untouched tree reports; the two new artifacts raise the artifact total from 961
to 963 and add no warning.

## Deviations, recorded for the completion decision

1. **One commit for everything.** The repository's convention is one commit per
   accountable act — `governance(...)`: draft, approve, start, then the code.
   The owner directed a single combined commit on 2026-08-27 after being shown
   the split alternative and its consequence, that CI then passes a diff wider
   than any one act's scope. The deviation is the owner's and is recorded here
   because the commit itself cannot show that it was chosen rather than
   overlooked.
2. **The replay of record was taken at the pre-amend commit.** A packet whose
   evidence states its own readings cannot be measured after it is written. The
   readings above were taken with a clean worktree at
   `904b1b183f38f006cfd251d8e43e2564fd3c58a9`, and this file plus one
   `README.md` bullet were then folded into that commit with `git commit
   --amend`. `repository_tools/release_build.py`, `tests/test_release_build.py`
   and every governance artifact are byte-identical between the two, and the
   `README.md` bullet is not an input to a build; the blob the producer executed
   is the blob this commit contains. Nothing was pushed at either point, so no
   published commit is orphaned. The alternative — a second commit holding the
   evidence — is what the convention would give and is what deviation 1
   displaced.
3. **No POSIX host reading and no hosted lane.** `VER-RLO-004`'s
   host-independence row asks for a full replay on a POSIX host as well as a
   Windows one, and its `source mode matrix` row names the POSIX export case.
   The POSIX reading of this code does not exist: the workstation is Windows,
   and no pull request has been opened, so the publication rehearsal's
   `candidate` job has not run. What is known about the POSIX side is that the
   bound identities this Windows replay reproduces were themselves produced on
   a Linux host and confirmed by hosted replay `33016585047` — before this
   change. The two mode-reading tests that would settle the POSIX modes are
   skipped on Windows and unrun. This is the material gap in the evidence.
4. **The export assertion in the authorized envelope was not taken.** The work
   order permits additionally asserting committed-blob equality of the exported
   tree at run time. It was declined: the check costs one `git cat-file` per
   exported file on every build, and the equality is measured here instead, in
   the table above and in four tests.
5. **`0o775`/`0o664` are recorded as data, not derived.** The mode response
   does not read the committed mode of each blob. That is exact only while no
   committed blob carries the executable bit, which is measured true at the
   candidate (1539 of 1539 at `100644`) and nowhere enforced.
   `REQ-RLO-017` and `VER-RLO-004`'s residual uncertainty both record the
   constraint; nothing detects the day it changes.

## Complete changed-path set

```
docs/engineering/release-orchestration/README.md
docs/engineering/release-orchestration/architecture/ARCH-RLO-004.md
docs/engineering/release-orchestration/evidence/WO-RLO-008/WO-RLO-008-verification.md
docs/engineering/release-orchestration/requirements/REQ-RLO-017.md
docs/engineering/release-orchestration/specifications/SPEC-RLO-004.md
docs/engineering/release-orchestration/verification/VER-RLO-004.md
docs/engineering/release-orchestration/work-orders/WO-RLO-008.md
docs/notes/developing-se-harness.md
repository_tools/release_build.py
tests/test_release_build.py
```

## Not done

- The completion transition. `WO-RLO-008` reads `in_progress`.
- `VREC-RLO-008`. Commit-bound verification is `required` and owed.
- Any push, pull request, tag, release, publication or deployment. Nothing
  left this workstation.
- The POSIX and hosted readings of deviation 3.
- The RCA document for `RC-070-01`, which issue #189 names and which does not
  exist. It is an ungoverned path and a separate act.
- Any comment on issue #189 recording that its stated remedy — refuse or warn
  on a Windows host — was declined in favour of making a Windows host correct.
- `scripts/replay_release_build.py`, the workflows, the recipe, the lock and
  `scripts/normalize_sdist.py` are untouched.
