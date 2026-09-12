# Released 0.17 interface census — review draft

This is preparation for OWN07 review, not a completeness or qualification verdict.
It records the discovered public interfaces, inspected call paths, bounded actual
observations, and remaining cases. The two protected-output failures remain open.
No proposed or approved criterion is changed by this document.

All source references use this exact installed released-package prefix:

`R = C:/Users/hok/Documents/Codex/2026-09-12/clo/work/evaluator-017/Lib/site-packages/se_harness`

Thus `R/cli.py:150` means that absolute file at one-based line 150, not candidate
checkout source. The real `evaluator-017/Scripts/python.exe -I -B` reported
`0.17.0`; runtime introspection of `build_parser`, `PUBLIC_MUTATION_OPERATIONS`
and `ARTIFACT_PREFIXES` returned the 22 commands, ten operations and 14 types below.
Membership is an interface inventory, not evidence that every route was exercised.

## Public CLI commands

The handler reference identifies the direct CLI entry; writing paths are traced
in the following sections. “Read” describes inspected application behavior, not
a blanket promise about Git stat caches, interpreter caches or caller redirection.

| Command | Released handler/source | Modes and relevant effects |
| --- | --- | --- |
| `init` | `R/cli.py:150` | Writes installation, fragments/adoption report and lock by default; `--dry-run` plans only. No `--apply` option. Existing schema-4 lock fails during planning. |
| `upgrade` | `R/cli.py:182` | Plan by default; `--apply` writes managed files/lock; `--evidence-output` can additionally retain upgrade evidence. |
| `scaffold-domain` | `R/cli.py:660` | Creates domain structure; `--dry-run` suppresses writes. |
| `create-artifact` | `R/cli.py:682` | Creates one formal draft, explicit `--id` or Git-aware ID allocation; `--dry-run` suppresses writes, `--quiet` changes presentation. All 14 types below. |
| `raise-risk` | `R/cli.py:599` | Creates a risk and optionally a paired decision (`--with-decision`); explicit/allocated IDs; `--dry-run` suppresses writes. |
| `transition` | `R/cli.py:532` | Plan by default; `--apply` changes one or more explicitly selected formal lifecycle states. Human and delegated actors take distinct guard paths. |
| `decide` | `R/cli.py:563` | Plan by default; `--apply` chooses `--option`, `--defer`, or `--withdraw`; paired risks may also move. `--mitigated-by`/`--avoided-by` add risk-disposition inputs. |
| `capture-verification` | `R/cli.py:452` | Creates a ready VREC plus evaluator evidence; default/domain/explicit `--output` placement; ordinary or delegated `--owner`. Does not verify the record. |
| `prepare-release` | `R/cli.py:480` | Creates a ready RLS plus evaluator evidence; default/domain/explicit `--output`, optional tag; does not release the record. |
| `evidence` | `R/cli.py:395` | Creates/rebinds a packet at start, pre-action, transition or handoff. Fixed domain/WO path; optional rebound timestamp. Report writing is not guarded by the mutation registry. |
| `check` | `R/cli.py:359` | Projection without checkpoint reads only (`R/cli.py:342`). Checkpoints are start/pre-action/transition/handoff/scope. `--from-git` plus handoff plus WO can rebind a packet before checking, and retain `handoff.json` after a completed result. Declared/manifest change sets do not enable this retention. |
| `dashboard` | `R/cli.py:293` | Generates a directory bundle; default `target/harness-dashboard` or `--output`. Existing output directory is replaced transactionally. No lock/authority guard. |
| `qualify` | `R/cli.py:778` | Four roles: released-root, complete-candidate, candidate-package, public-install. Each optional `--output` writes a qualification result; both passed and failed results can be retained. Candidate-package also makes disposable package-test installations. |
| `validate` | `R/cli.py:856` | Reads artifact graph through engine validation; JSON/advisories change presentation. Does not validate installed-lock compatibility merely by validating the graph. |
| `inspect` | `R/cli.py:242` | Reads repository attention/lifecycle queues; vocabulary threshold is an analysis input. |
| `doctor` | `R/cli.py:270` | Reads installed integrity; unsupported schema produces failure, without repairing anything. |
| `preflight` | `R/cli.py:316` | Reads start/review readiness and installation integrity; `R/preflight.py:537`, installation loop at 550. |
| `pr-body` | `R/cli.py:410` | Emits a suggested pull-request body to stdout; does not publish it or change files. |
| `select-work-order` | `R/cli.py:440` | Emits selected-WO information; no retained selection mutation. |
| `risks` | `R/cli.py:642` | Reads risks threatening the selected artifact/chain. |
| `release-unit` | `R/cli.py:715` | Reads Git history and optional release contract; JSON/TOML output is stdout, not a contract write. |
| `identity` | `R/cli.py:758` | Reads runtime identity for three roles; `--entry-point` and root options identify inputs, not output destinations. |

The 14 authoring types are `intent`, `capability`, `requirement`, `specification`,
`architecture`, `adr`, `verification`, `work_order`, `verification_record`,
`release_contract`, `release_record`, `operating_contract`, `decision`, and `risk`.
CLI authoring/parser references: `R/cli.py:1054`, `R/artifact_layout.py:457`.
The released parser has no `skill-ownership` command. Its absence is command
compatibility evidence, not a protected-writing probe.

## Ten registered operations and direct/delegated paths

Registry construction is at `R/mutation_guard.py:26` and 39. The seven human
operations are joined with three contract-defined delegated operations
(`R/workflow_contract.json:16`, 17, 18; loader `R/workflow_contract.py:224`).

The common authority function at `R/mutation_guard.py:133` reads the lock before
configured/runtime identity; lock-read failures become MG001 at 150. The lock
reader is `R/installer.py:224`; schema 4 fails `R/integrity.py:199` with
`unsupported lock schema`. A registered operation can still be unreachable from
a given CLI fixture because an earlier guard or precondition refuses first.

| Registry operation | Inspected direct API / guard position | Schema-4 distinction |
| --- | --- | --- |
| `installed-root-apply` | `installer.apply_changes`, `R/installer.py:512`; guard at 560 when prior tool version or installed config exists | Normal CLI `init` already fails `plan_install` lock read at 265. Direct installed-root apply must be considered separately. |
| `upgrade-apply` | Same API, replan at 524, guard at 534 with `allow_upgrade_transition=True` | Schema-4 replan refuses before this guard. Caller-supplied changes/old lock do not skip replan. |
| `scaffold-domain` | `artifact_layout.scaffold_domain`, `R/artifact_layout.py:246`; guard at 276 before directory creation | Domain/template/path validation precedes authority. |
| `create-artifact` | `artifact_layout.create_artifact`, `R/artifact_layout.py:457`, guard at 505; also `risks.raise_risk`, `R/risks.py:332`, guard at 452 | Both single risk and paired risk/decision share this guard. Valid template/ID/domain/input preparation is needed. |
| `transition-apply` | `workflow.plan_transition`, `R/workflow.py:433`, then `apply_transition` at 627; guard first at 628 | Human routes validate current/proposed graph and gates before invoking apply. Direct `apply_transition(plan)` guards before inspecting/writing planned inputs. |
| `capture-verification` | `provenance.capture_verification`, `R/provenance.py:351`, common guard at 372 | Initial ID/owner/nonempty argument checks precede guard; graph/state/output/Git provenance follow it. |
| `prepare-release` | `provenance.prepare_release`, `R/provenance.py:495`, guard at 518, archive required | Initial argument checks precede guard; release-artifact/output/provenance checks follow. |
| `delegated-work-order-start` | `workflow.plan_transition`, delegated dispatch `R/workflow.py:503`, authority at 513 | Approved→in_progress. Class must be declared at current and base, configured gate must pass for actual HEAD. Dedicated guard precedes generic transition-gate evaluation. |
| `delegated-work-order-complete` | Same path and authority location | In_progress→implemented; same prerequisites and ordering. |
| `delegated-vrec-prepare` | `provenance.capture_verification`, nested guard `R/provenance.py:401` | CLI enters the common capture guard at 372 first. On schema 4, that refusal preempts this nested guard; a CLI result cannot honestly be attributed to the nested guard. |

Delegation admission is `R/gate_source.py:237`, with class-at-base and current
HEAD gate checks before return. A controlled local-file gate is a synthetic
fixture input, not an evaluator-authority double.

Decision CLI dispatches `risks.dispose_decision_with_risks`
(`R/risks.py:575`), which calls `plan_transition`; direct
`decisions.dispose_decision` (`R/decisions.py:159`) does likewise. Risk option,
withdrawal, and deferral paths can produce different multi-artifact plans even
though all writing converges on guarded `apply_transition`.

`--output` for VREC/RLS is interpreted after common authority and checked through
`R/provenance.py:233`; record/evidence create-once writers are at 265, 275 and 308.
Upgrade evidence path validation is `R/installer.py:450`; use a valid example
`docs/engineering/legacy-probe/evidence/upgrade-observation.json`, not a root-level
JSON filename, when probing that mode. Guard precedence alone does not establish
the later path checks. Low-level `integrity.atomic_write_bytes`/`atomic_create_bytes`
are file primitives, not intrinsically guarded governance APIs (`R/integrity.py:111`,
126); calling the registry with each operation name is not a census of their callers.

## Report/evidence writers and output boundaries

**Evidence and retained check.** `workflow_compliance.write_evidence_packet`
(`R/workflow_compliance.py:129`) validates selections/header and writes at 188,
without installed-lock or mutation-authority checks. Fixed path construction is
`R/workflow_evidence_packet.py:55`. Existing packet leaf checks are at
`R/workflow_compliance.py:171`; parent paths are not equivalently checked.

`check_workflow` starts at `R/workflow_compliance.py:492`. Its
`_resolve_change_set` at 394 rebinds an existing handoff packet at 413 before Git
change-set derivation and generic readiness checks. Rebinding
(`R/workflow_evidence_packet.py:93`) preserves the owner body and checks the existing
leaf, but not the entire parent chain. Completed self-binding results are retained
at `R/workflow_compliance.py:678` via `retain_handoff_result`
(`R/workflow_evidence_packet.py:129`), whose atomic write has no equivalent leaf
check. An exit-1 check can therefore already have written a packet.

**Dashboard.** `generate_bundle` is `R/engine/generate_harness_dashboard.py:131`,
with output transaction at 200. `resolve_output_root`
(`R/engine/dashboard_snapshot.py:177`) resolves paths before checking the leaf,
rejects repository/ancestor and artifact-root overlap, but does not exclude
installed `.github` or retired discovery directories. The transaction
(`R/engine/dashboard_bundle.py:700`) builds a temporary tree, renames existing
output to a backup at 752, promotes the replacement, and deletes the backup.
Ordinary existing directory contents can therefore be removed as part of a
successful report write. Parent/leaf aliases require separate observation.

**Qualification.** Role functions are `R/release_qualification.py:401`, 470,
506, and 603. `write_qualification_result` at 216 requires an existing resolved
parent and an absent leaf; it uses exclusive creation. Existing or dangling
leaf symlinks are refused at 240. Parent resolution at 228 follows aliases before
the symlink check. Successful role return assigns the inspected root exclusion in
`R/cli.py:778`; an exception before assignment leaves `forbidden_roots=()` and
the handler still attempts output at 825. A returned failed result is different
from an exception: normal return still assigns exclusions. Candidate-package
internally catches some candidate failures at `R/release_qualification.py:540`;
those do not establish that every exception path has the same boundary.
Its disposable package installations are under `R/candidate_acceptance.py:255`
(temporary directory at 283), separate from explicit result publication.

## Actual observations retained so far

All current fixture-design subprocesses used actual isolated released 0.17, with
no authority or preflight mock. These Windows observations do not replace the
final candidate/OS/Python/source/package matrix.

| Evidence | Actual observation | Qualification limit |
| --- | --- | --- |
| `agent-fixtures/run-dd09dc0a` | Valid graphs; ordinary draft-intent rejection and decide option/defer/withdraw each exit 2, MG001 `transition-apply`, unsupported schema, zero changed paths | Four actual routes; no paired-risk disposition coverage. |
| `agent-fixtures/delegation-4d2f544d` | Valid graphs; delegated start and completion each exit 2 with their dedicated MG001 operation, zero changed paths including Git | Synthetic class/base/gate fixture; not live CI or later handoff-gate qualification. |
| `agent-fixtures/check-7c5da381/draft-handoff` | Valid draft-WO graph; check handoff `--from-git HEAD` exits 0/completed, rebinds packet and creates `handoff.json`; repeat exits 0 and updates retained JSON only | Demonstrates real report writes without lifecycle change. Uses an earlier retained valid fixture, not the latest wheel. |
| `agent-fixtures/check-7c5da381/in-progress-handoff` | Valid in_progress-WO graph; exits 1/blocked on unsupported-lock review preflight, but packet header was rebound first; no retained JSON. Repeat makes no changes | Failed process does not mean no writes. First call also refreshed `.git/index`; raw bytes retained. Independent index parsing found the same 54 paths/modes/blob IDs/flags, with stat metadata changed. |
| `output-probes/qualification-retired-core/released-protected-output.json` | Actual 0.17 exits 1/RQ001 but creates absent `.agents/skills/harness-orient/SKILL.md` | Confirmed protected-output failure; parent directory was preserved by owner content. |
| `output-probes/dashboard-installed-workflow/released-protected-output.json` | Actual 0.17 exits 0 and `--output .github` replaces that directory, deleting installed workflow and pull-request template | Confirmed protected-output failure; successful process still violates the preservation boundary. |

The last two fixtures were built with exact candidate wheel SHA256
`50ad9892255aaf881f643c52e07e237022090393c82054b7983d9cbca58735fe` and passed candidate
doctor and released graph validation before their probes; setup/result files were
inspected, not rerun here. Earlier `legacy-writer-probe/final-valid` evidence also
observed default evidence/dashboard creation with no pre-existing path changes.
Those observations apply to the paths actually selected, not all report options.

Minimal retained-check construction is in `agent-fixtures/check_probe.py`:
copy a valid schema-4 fixture; initialize/commit Git; create the WO handoff packet
with actual `evidence`; append an innocuous body comment to move the formal
snapshot; invoke `check ROOT --artifact WO-ID --checkpoint handoff --from-git HEAD --json`.
Use a draft WO for the observed completed route. The separate in_progress fixture
demonstrates rebind-before-refusal. Both keep formal status and installed bytes
unchanged during the invocation. Full argv, process status, snapshots, hashes and
changed before/after bytes are retained; projected `mutation.writes` is not the
sole filesystem observation.

## Remaining observations and review decisions

- Run and retain the new permanent census cases against the selected candidate.
  Inspection of a test definition is not a passed observation. Include source
  and isolated installed authority distinctions and unavailable mechanisms.
- Exercise actual installed 0.17 direct API callers, not only a loop over registry
  names or source tests with mocked guards. Include crafted installed-root apply
  plans and ordinary direct transition/decision callers; preserve guard precedence.
- Cover auto-ID allocation where relevant and paired-risk accept/avoid/mitigate,
  defer/withdraw, aggregate transitions, and capture/release output variants with
  syntactically valid inputs. The four ordinary probes do not prove all plans.
- Qualification still needs retained output observations for complete-candidate,
  candidate-package and public-install, covering normal return, returned failure,
  exceptions before exclusion assignment, existing/absent leaf, missing parent,
  and protected/external destinations. Do not infer all four roles behave like the
  dynamically observed released-root exception.
- Exercise parent and leaf aliases/reparse points for evidence, retained JSON,
  dashboard and qualification; distinguish unsupported OS mechanisms from passes.
  The inspected resolve/parent behavior is a concern, not a dynamically established
  alias exploit in this draft. Hardlink behavior also needs its own observation.
- Extend retained check with absent/headerless/foreign/stale packets, failed Git
  base resolution after rebind, ordinary versus aliased parent, and retained JSON
  collisions. The new draft/completion and in_progress/refusal probes establish
  two real paths only. Record incidental Git metadata separately from protected
  installed/formal bytes, without silently dropping it from snapshots.
- Read/projection and dry-run modes need any preservation claims matched to their
  actual snapshots. Generic stdout redirection by a caller is not a CLI output
  option. No claim of complete route coverage, safe reporting, or overall OWN07
  acceptance follows from the command/operation counts in this draft.


## Subsequent focused candidate observations

The eight permanent cases now ran locally in both source and isolated installed
candidate modes on Windows/Python 3.13: six passed and the two protected-output
cases failed in each mode, without errors or skips. Default evidence/report and
draft retained-check output preserved protected bytes. Installer/authoring,
ordinary decision/transition and delegated start/completion cases refused for the
unsupported lock. All 14 artifact types and the capture/release output variants
in the test definition were included. The first authoring attempt's root-level
upgrade-evidence argument was corrected to a governed destination and the entire
authoring case was repeated successfully in both modes; both attempts are retained.

The source run uses the pre-existing candidate authority double only. Every
old-reader subprocess invokes actual isolated released 0.17, and installed
candidate migration uses the exact optimized CI wheel without authority mocks.
The test sources, six run summaries and every case event are retained in
`legacy-reader-expanded-observations.zip` and indexed separately. These results
partly answer the draft's first remaining item; direct API, additional variant
and cross-platform observations remain pending. The census is not complete and
the protected-output failures prevent acceptance.
