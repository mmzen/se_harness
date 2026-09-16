# Root cleanup evidence — README repair applied; acceptance blocked

## Authority and state

The owner approved VER-PLG-024 and WO-PLG-024 on 2026-09-16 after reviewing their
exact draft hashes. Released SE Harness 0.18.0 recorded both approvals and
started WO-PLG-024 under DR-015 with Codex as executor. The baseline is
`f05c478a29c39f94968fdc842a34c861d30a42ac`.

The planned cleanup and the exact two-link README repair are applied locally.
The owner authorized that repair on 2026-09-16 with: "you can include this exact
README repair in the authorized work". Its applied SHA-256 is
`240bf535c917234225d19e0efe1b48521322eb6f6504c5b7a5619a9e866546dc`.
**WO-PLG-024 remains `in_progress`: required acceptance and formal scope recording
are blocked as detailed below.** No completion, VREC, assurance decision, commit,
push or PR is claimed.

## Observed coverage

| Contract | Observation |
| --- | --- |
| C01 | Released migration preview and application passed. Exactly seven root skill files and the obsolete delegation TOML are removed. The schema-4 lock contains only the portable plugin provider choice; evaluator identity and unrelated entries are unchanged. |
| C02 | A disposable copy of 10,422 current files passed released doctor without a plugin path, same-release upgrade, repository-skill restoration, switching back, repeated switching and final doctor. Restored skills match the released templates. The real checkout was not restored or upgraded. |
| C03 | The initial 16-link review passed; the later review includes the approved README repair and evidence links. AGENTS.md's managed fragment and both historical note bodies are unchanged. Codex and Claude native discovery passed in previously disposable profiles; each package matches all 24 accepted package files. Two onboarding subtests reveal missed dependencies on root skill paths. |
| C04 | Governing doctor: 64 checks pass, including after the README repair. Governing graph: 1,654 artifacts, zero errors, 48 existing warnings. Review preflight: ready, no diagnostics. Distribution validation: 15 records pass. Candidate CLI help passes. The diff matches the original cleanup plus the owner's exact README authorization. The formal scope checkpoint fails; the completed full source run reports 1,068 tests, 12 failures and 15 skips. |

The actual installed Codex replacement used by migration has 21 identical
manifest, skill, setup and wheel files compared with the accepted package. Its
README lacks the later setup appendix, LICENSE has different line endings, and
assembly-inventory.json is absent. A broader package comparison therefore did
not establish complete package equality. These differences do not change the
native discovery/runtime inputs; no authenticity or new publication claim is made.

Native observations used Codex CLI 0.154.0-alpha.6.2 and Claude Code 2.1.269 on
Windows with Python 3.13.3. No model calls, persistent user-profile changes,
plugin installation, new platform qualification or release build occurred.

## README repair and completed regression run

The full source run observed a failure in
`PublicOnboardingTests.test_deeper_guidance_remains_directly_discoverable`.
At that point, README.md lacked direct links to `docs/notes/getting-started.md`
and `docs/notes/harness-installation-and-upgrades.md`. Both README.md and the test
were unchanged from baseline, which includes the owner's later README edits.

A focused reproduction reported two failing subtests. The exact two-line
addition under **Go further** was proposed, explicitly authorized and applied.
See [the approved diff](readme-remediation.diff). The direct-link test now passes.
The rest of the owner's README wording and marketing-document deletions remain.
No test or approved acceptance criterion has been relaxed.

The local full-suite logging wrapper also raised UnicodeEncodeError while
printing the failure. Its retained output is [the partial source log](source-suite.log);
the complete aggregate result was not captured. The wrapper now uses UTF-8.
The corrected wrapper retained the complete retry in
[source-suite-readme-repair.log](source-suite-readme-repair.log): 1,068 tests in
721.729 seconds, 12 failures and 15 skips, process exit 1. The initial diagnosis
was incomplete; the missing links were not the only failing checks.

The 12 failures cover four test methods in `PublicOnboardingTests`:

- Ten failures in three methods require the manual installation section and
  inline init/doctor examples removed by earlier owner changes. They reproduce
  in a complete disposable baseline fixture. SPEC-DST-024's PUB-START-001 and
  PUB-UPGRADE-001 still prescribe that presentation, so changing assertions
  alone would leave a contract mismatch.
- Two failures in the operator-note method require root `.agents/skills/`
  paths. They pass at baseline and fail after this cleanup. The proposal missed
  those dependencies; plugin ownership needs source/provider-aware checks and
  accurate pointers in the associated current and historical notes.

The first baseline fixture omitted LICENSE and produced an extra fixture-only
link failure. It was corrected in a separate complete fixture. Both observations
are retained; only the complete fixture supports the baseline comparison.

## Formal scope-recording blocker

The owner's README remediation authorization is present. The original recorded
approval of WO-PLG-024 still excludes README.md. The released scope check reports
`QGP-G4I-PATHS / WEX201`; see
[the actual schema-2 result](scope-after-readme-repair.json).

Inspection of the exact 0.18.0 evaluator found no CLI amendment operation and
only `implemented` or `rejected` transitions from `in_progress`. A read-only,
in-memory comparison confirms that adding README.md to current scope metadata
alone would fail `WEX-ECP-022`, because it differs from the approval snapshot.
Original approval events and formal scope are unchanged. No unsupported
transition, handwritten approval, or claimed gate pass was used.

The supported recovery needs a reviewed replacement work-order package, or a
separately governed evaluator amendment capability followed by release and
explicit adoption. Neither is authorized or implemented by the two-link repair.

## Other observations and review

- Candidate-source doctor exited 1 for its 0.19.0 router, payload and version
  disagreement with the installed 0.18.0 root. This is the boundary documented
  by AGENTS.md; the governing released doctor passes. Root managed policy was
  not replaced.
- The first disposable check helper looked for released templates in the wrong
  installation directory after successful restoration. Its failure and applied
  operation results were retained. The helper was corrected to the observed
  `share/se-harness/templates/repository/standard` location and resumed from
  the restored fixture; no completed mutation was replayed.
- One newly added historical-banner link initially named the wrong upgrade
  domain. The path was corrected before the independent 16-link review.
- The change uses the released ownership operation and existing tests. It adds
  no product mechanism, dependency, CI lane or historical archive rewrite.
  Product source, tests, templates, package/catalog inputs, old formal records,
  historical evidence and marketing-document deletions remain unchanged. README.md
  differs only by the two approved links. Both publication branches are preserved.

[checks.json](checks.json) retains command arguments, actual results, comparisons,
limits and raw-output identities. Full diagnostics and disposable trees remain
outside the checkout. Remaining acceptance blockers are the 12 onboarding failures
and recording the approved README scope through a supported workflow. Repeating
the already supplied README authorization does not resolve that evaluator gap.

## Verification-record request

The owner subsequently authorized creation of the verification record on
2026-09-16. A fresh read-only completion check is retained in
[verification-preparation-readiness.json](verification-preparation-readiness.json),
with its [command and exit status](verification-preparation-readiness.command.json).
It exits 1 on `QGP-G4I-EVIDENCE`: no bound handoff packet exists for the current
formal snapshot. It changes no lifecycle state. The known source-suite and
scope failures remain unresolved; this gate result does not waive them.

Released capture also requires the selected work order to be implemented or
later and the candidate worktree to be clean. WO-PLG-024 is still `in_progress`
and its changes are uncommitted. Capture was therefore not invoked, and
VREC-PLG-021 remains absent. The owner's preparation permission is retained;
no repeated permission is needed once the required remediation and gates pass.
