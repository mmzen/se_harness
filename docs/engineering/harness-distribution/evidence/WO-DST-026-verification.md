# WO-DST-026 verification evidence

Retained under `VER-DST-027` for the wave 5 managed template hygiene.
Measurements were taken on Windows 11 on 2026-09-08, on the branch
`wo/dst-026-managed-template`, whose base is `main` at `fd4584cc` (the merge
of `WO-CIP-007`). The governing evaluator is released 0.16.0 installed from
the wheel file in `C:/Users/mathi/se-harness-eval-0160`, run with `-I` from
outside the checkout. The consumer scenarios ran in
`C:/Users/mathi/dst026-scratch`, outside the checkout, from an ephemeral
non-promotable candidate wheel `se_harness-0.17.0-py3-none-any.whl`
(`sha256:952ec200…6bb2`, built on Windows from the tracked worktree bytes of
the candidate and not a build of record) installed in its own virtual
environment. The hosted Linux lane is the record for the suite; the Windows
readings below are the local control, labelled as such.

## Authorization

- 2026-09-08: the owner approved `REQ-DST-072` to `REQ-DST-075`,
  `SPEC-DST-027`, `VER-DST-027` and `WO-DST-026` by selecting the presented
  option "Approve all three (Recommended)" (PR #410, merged 16:17Z).
- 2026-09-08: the owner said "ok go for WO-DST-026". Start, completion and
  record preparation are the delegated executor's under
  `[delegation] class = "execution"`, each taken while the required `validate`
  check is `success` for the head, read at the base of the pull request.

## The template before and after

Before (`fd4584cc`), the header:

    # Managed by SE Harness. Runs the exact released evaluator outside the checkout:
    # work-order selection and review preflight on pull requests, then doctor,
    # validate and the dashboard. …

and three floating actions, `actions/checkout@v4`, `actions/setup-python@v5`,
`actions/upload-artifact@v4`; both `check … --json` invocations ended in
`|| true` and handed their stdout file to `json.load` with no other input.

After, the header names the steps the file runs, in the order they run:

    # Managed by SE Harness. One job runs the exact released evaluator outside the
    # checkout. Its steps: Install the exact released evaluator; on a pull request,
    # Read the live pull-request body, Select the pull-request work order, run the
    # Review preflight and Enforce the work-order scope on the pull request's diff
    # (the handoff check runs inside that step while the work order is in
    # progress); then Qualify the root with its exact released evaluator, Generate
    # Harness Explorer, and upload the Explorer with the qualification result as
    # the harness-dashboard artifact. …

The three `uses:` lines:

| Action | Tag | Commit digest |
| --- | --- | --- |
| `actions/checkout` | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` |
| `actions/setup-python` | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| `actions/upload-artifact` | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |

Each digest was resolved from its tag on 2026-09-08 under `WO-CIP-007` and is
the one the repository-owned workflows carry; the template's majors are
unchanged.

The two check steps, shell shape (DST-MWF-001):

    scope_status=0
    "$RUNNER_TEMP/se-harness-env/bin/python" -I -m se_harness check . \
      --artifact "$HARNESS_WORK_ORDER" --checkpoint scope \
      --from-git "$HARNESS_BASE_SHA" --json \
      > "$RUNNER_TEMP/scope.json" 2> "$RUNNER_TEMP/scope.stderr" || scope_status=$?
    in_progress="$("$RUNNER_TEMP/se-harness-env/bin/python" - "$RUNNER_TEMP/scope.json" \
      "$RUNNER_TEMP/scope.stderr" "$scope_status" <<'PY'

The handoff check takes the same shape with `handoff_status` and
`restitution.stderr`. Each embedded reader first echoes the captured stderr,
then tries to parse the result; on `OSError` or `ValueError` it prints
"The scope check wrote no result (exit status N)." and exits with N, or with
1 when N is 0 (DST-MWF-002). A parsed result is judged by the unchanged code
that follows (DST-MWF-003). The diff of the template is 54 lines, 41 added
and 13 removed; `git diff fd4584cc -- templates/` is the record.

## Scenario A, consumer install

`init` of an empty Git repository with the candidate wheel's evaluator:
exit 0, 42 files. The `.gitignore` written:

    # se-harness:begin
    # Generated SE Harness output
    /target/harness-dashboard/
    __pycache__/
    *.py[cod]
    # se-harness:end

`git check-ignore -v "# se-harness:begin"` and
`git check-ignore -v "<!-- se-harness:begin -->"` both exit 1 (no rule
matches); `git check-ignore -v target/harness-dashboard/x` exits 0 and names
`.gitignore:3:/target/harness-dashboard/`. The installed workflow carries the
new header and the three pins and no `|| true`. After the initial commit,
`doctor` exits 0 with 99 `PASS` lines and no failure.

## Scenario B, consumer upgrade

A Git repository with an owner `.gitignore` of two lines (`/build/`,
`/.venv/`), initialized by released 0.16.0 (`init` exit 0), whose block the
0.16.0 installer wrote between HTML comments below the owner lines; committed;
0.16.0 `doctor` exit 0. The candidate's `upgrade` plan:

    update     .engineering-harness.toml
    update     .github/workflows/engineering-harness.yml
    update     .gitignore
    update     ENGINEERING_HARNESS.md
    update     docs/engineering/QUALITY_GATES.json
    update     docs/engineering/QUALITY_GATES.md
    update     docs/engineering/TRACEABILITY.md
    update     docs/engineering/WORKFLOW.json
    update     docs/engineering/WORKFLOW.md
    update     docs/engineering/templates/README.md
    add        docs/engineering/templates/RISK.template.md
    summary: 41 files, 30 unchanged

`.gitignore` is `update`, the safe fragment rewrite; nothing is `customized`
or `conflict`. `upgrade --apply` exits 0 ("upgraded managed files to
se-harness 0.17.0"). The file afterwards:

    /build/
    /.venv/

    # se-harness:begin
    # Generated SE Harness output
    /target/harness-dashboard/
    __pycache__/
    *.py[cod]
    # se-harness:end

Measured byte for byte: the owner bytes before the block and after the block
are identical to the 0.16.0 file's, the hash markers are present and no HTML
marker remains. The managed workflow was rewritten with the new header and
pins. After the commit, the candidate's `doctor` exits 0 with 99 `PASS` lines.

## Scenario B, customized: one line edited inside the block

The same 0.16.0 fixture with `/target/harness-dashboard/` changed to
`/target/harness-dashboard/edited` inside the block, committed. The
candidate's plan reads `customized .gitignore`; `upgrade --apply` exits 1
with "customized files require manual review; no files were written:
.gitignore"; `cmp` reports the file unchanged.

## Scenario C, refusal surface

The two readers were extracted from the exported template's heredocs and run
as a consumer's runner would, with `python` and positional arguments.

| Case | Input | Output | Exit |
| --- | --- | --- | ---: |
| C1 scope | empty result, stderr `MG005: the mutation guard refused the write: runtime identity is not the released evaluator`, status 2 | the MG005 line, then `The scope check wrote no result (exit status 2).` | 2 |
| C2 handoff | the same, status 2 | the MG005 line, then `The handoff check wrote no result (exit status 2).` | 2 |
| C3 scope | empty result, empty stderr, status 0 | `The scope check wrote no result (exit status 0).` | 1 |
| C4 scope | a completed result of a work order in progress | `yes` on stdout | 0 |
| C5 scope | a blocked result | `blocked: QGP-G4I-EVIDENCE: …`, `The scope check did not complete (outcome blocked).` | 1 |
| C6 scope | `QGP-G4I-PATHS` failing | `scope: 1 path outside scope: x.py`, `The pull request's diff leaves the work order's declared scope.` | 1 |
| C7 handoff | a completed result, no declared digest | `The pull request's diff is inside the declared scope; no restitution digest was declared.` | 0 |
| C8 handoff | a completed result, declared `deadbeef` | `Declared Harness-Restitution deadbeef does not match the recomputed result_sha256 b498c4bc…` | 1 |
| C9 handoff | a blocked result | `blocked: …`, `The handoff check did not complete (outcome blocked).` | 1 |

No output of any case contains `Traceback`. C4 to C9 are the verdicts and
messages the lane printed before the change; C1 to C3 are the new failure
surface. The completed result of C4, C7 and C8 is the retained
`handoff.json` of `WO-CIP-007`, a real 0.16.0 result.

## Environment inventory

Every literal environment read under `se_harness/`, found with the pattern
`os.environ.get("NAME")`, `os.environ["NAME"]` or `os.getenv("NAME")`:

| Variable | Read in | Effect | Named in |
| --- | --- | --- | --- |
| `SE_HARNESS_REHEARSAL` | `se_harness/gate_source.py` (`load_configuration`) | equal to `1`, the `local-file` gate source loads without `W-ECP-005` | `SPEC-ECP-006` (amendment record of this work order), `SPEC-DST-027` |
| `GITHUB_TOKEN` | `se_harness/gate_source.py` | bearer token for the `github-checks` read | `SPEC-ECP-006` `ECP-DLG-004` |
| `PYTHONPATH` | `se_harness/runtime_identity.py` | `pythonpath_present` in the identity report | `SPEC-ECP-023` |

Three names, each in a specification. `SPEC-DST-027` `DST-MWF-011` says
"two today"; the third, `PYTHONPATH`, was already read and already specified
when the rule was written, and the test pins the measured three. The
allow-list copy in `candidate_acceptance.safe_environment` iterates
`os.environ.items()` against `INHERITED_ENVIRONMENT_KEYS` and reads no name
of its own; `se_harness/engine/` reads none.

## Tests

`tests/test_managed_template_hygiene.py` is new: 11 tests in three classes
(`ManagedWorkflowTemplateTests` 5, `GitignoreMarkerTests` 4,
`EnvironmentInventoryTests` 2), the module alone `OK` in 2.8 s. It is the one
test file this work order changes. The work order expected about eight
assertions to move in `test_ci_pipeline.py`, `test_harnessctl.py`,
`test_standard_repository_lifecycle.py` and `test_instruction_architecture.py`;
measured, none quoted the old header or the HTML markers of `.gitignore`
(`test_harnessctl` asserts only that an adopted ignore file keeps its owner
first line; the HTML block in `test_standard_repository_lifecycle` belongs to
a retired Markdown fragment fixture), so none moved. All four run and pass,
`test_instruction_architecture` at the Windows baseline named below.

Local control, Windows 11, `python scripts/run_tests.py --workers 4`:
1,098 tests in 96 s, 1 failure, 1 error, 23 skips; the two names are this
machine's documented baseline (`test_owner_region_stays_within_the_size_bound`,
6,024 CRLF bytes against a 6,000 bound, 5,969 as committed LF; and the
`WinError 5` `rmtree` of a temporary `.git` in `test_artifact_authoring`).
Discovered tests, base `fd4584cc` versus the branch, counted by loading both
trees: 1,087 to 1,098, the eleven of the new module; no test deleted.

## Governing readings

| Command | Result |
| --- | --- |
| `validate .` (released 0.16.0, `-I`) | PASS, 1,432 artifacts, 0 errors, 44 warnings (all `W013`, none on a path this work order touches), 0 advisories |
| `doctor .` | exit 0, 97 `PASS`, no failure; every managed path `matches distribution` |
| `preflight . --work-order WO-DST-026 --phase review` | PASS, commit-bound verification `required` |
| `scripts/validate_release_distributions.py --root .` | PASS, 13 records |
| `python -m se_harness --help` | exit 0 |

## Root managed bytes

`git diff --quiet fd4584cc -- .github/workflows/engineering-harness.yml
.gitignore .engineering-harness.lock .engineering-harness.toml
ENGINEERING_HARNESS.md AGENTS.md CLAUDE.md .gitattributes docs/engineering/WORKFLOW.md
docs/engineering/templates` reports no difference: every root managed byte is
identical to `main`. `doctor`'s managed set reads unchanged. The change set
touches `templates/`, `se_harness/installer.py`, `tests/`, two notes,
`SPEC-ECP-006`, the domain index and this evidence.

## Carried obligation

`DST-MWF-014`: the root-adoption work order of the release that carries this
change takes the new template and the hash-marked `.gitignore` block into
this repository's root, and may drop the root `.gitignore` lines that
duplicate the fragment (`__pycache__/`, `*.py[cod]`, and `/target/` covering
`/target/harness-dashboard/`). Until then the root block keeps its HTML
markers and the root workflow its old header and floating tags.

## Hosted lane

Recorded in the handoff file beside this one
(`evidence/WO-DST-026/WO-DST-026-handoff.md`) once the pull request's lanes
have run at the implementation head, and in the lifecycle events of the work
order at completion and preparation.

## Disclosures

1. The environment inventory reads three names, not the two `DST-MWF-011`
   counts; see the inventory above. The rule's operative part, pin the set
   and require a specification for each, is met for all three.
2. An empty result with a captured status of 0 fails with 1. The
   specification says "fail with the check's exit status"; a step that
   passed on an empty result would be the swallowed failure the rule
   removes, so 0 is not honoured. The message names the status seen.
3. Each reader echoes the check's captured stderr in every branch, not only
   on failure, so nothing the check said leaves the log that showed it
   before the redirect; the verdict logic after the parse is unchanged.
4. No existing test moved (see Tests). The work order's estimate of about
   eight changed assertions did not materialize.
5. `SPEC-ECP-006`'s `updated` moved to 2026-09-08 with its amendment record;
   no rule identifier, statement or relation changed.
6. The template header names the steps by their exact `name:` values so the
   header test can compare them mechanically; "Review preflight" and "Read
   the live pull-request body" therefore appear capitalized mid-sentence.
7. The failure surface was exercised by running the embedded readers, not by
   a live refusal in a consumer's lane, as `VER-DST-027`'s residual
   uncertainty anticipates; this repository's own lane runs the 0.16.0 root
   copy and cannot observe the change until the root adoption.
8. `WO-DST-026`'s "Completion report format" says "The completion decision
   is the engineering owner's" while its approval and `[delegation]` delegate
   `DR-WO-COMPLETE`; the same sentence appears in `WO-CIP-007`. This work
   order proceeds on the delegated route its lifecycle events name, and the
   owner refuses the completion by rejecting the pull request.
