```toml
artifact = "WO-DPG-002"
checkpoint = "handoff"
formal_snapshot_sha256 = "e0b0dfa2473fd25d058100464f8eb441cd1a61612f41b12e3b80042edf2562f7"
rebound_at = "2026-09-02T10:31:23Z"
```

# WO-DPG-002 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The Pages packager finds its notice boundary in the designed self-contained
Explorer. `.github/scripts/publish_dashboard.py` now carries an ordered
registry of accepted boundaries, `<main class="hx-main">` (the designed
page) and `<div class="workspace">` (the previous page, for replays of older
released records), and inserts the constant demonstration notice after the
one boundary that occurs exactly once; zero, several or both fail closed
with the unchanged message. The notice text did not change. No workflow,
template or managed path moved. The recovery publication of `RLS-SEH-023`
at governance commit `66e71f8` is a separate act after this work order
merges.

## Evaluators

- Governing: released `se-harness 0.13.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0130`), `-I`, wheel-installed, for every
  reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/dpg-002-notice-boundary` off `main`
  at `66e71f8`; implementation commit `a94104c`.

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.13.0 | Artifacts: 1247 | Errors: 0 | Warnings: 69 | Advisories: 0 |
| `doctor` | exact 0.13.0 | 0 FAIL |
| review preflight `--work-order WO-DPG-002` | exact 0.13.0 | PASS |
| `python -m unittest tests.test_dashboard_publication` | candidate, Windows 11, `PYTHONUTF8=1` | 25 tests OK, including the two added: the real root and canonical templates each carry exactly one accepted boundary; packaging inserts the notice after either boundary and rejects a page with none, with two of one, or with both |
| end-to-end packaging | candidate | the 0.13.0 root generator run from a detached worktree named `governance` at `a94104c` (1,247 artifacts, 0 errors); `package_dashboard` with a provenance naming `RLS-SEH-023` and that governance commit inserts the notice directly after `<main class="hx-main">`; published `index.html` 432,017 bytes, four fixed files, zero remote references |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 66e71f8` | exact 0.13.0 | section below |

### The Windows suite

Recorded when the run completes.

### Handoff check

Recorded with its self-binding result beside this packet.

## Root cause and why the test missed it

`WO-DST-023` replaced the canonical template and declared the Pages
workflow out of scope; the packager's boundary was a hardcoded element of
the previous page, and `PayloadPackagingTests` fed the packager a synthetic
page that still carried it. The first real generation from a 0.13.0 root,
the `publish-pypi.yml` run 33618394672 for `RLS-SEH-023`, generated PASS and
failed in packaging; PyPI, the tag and the GitHub Release completed and the
deploy was skipped. The new template-bound test fails on the next redesign
before a publication does.

## Material non-effects

No notice text, workflow, resolver, payload allowlist, template, managed
file, release record, tag, package or deployment changed.

## Hosted lanes

Recorded when the lanes complete at the pull request's head.
