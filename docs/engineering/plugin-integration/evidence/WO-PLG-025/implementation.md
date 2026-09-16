# Repository cleanup implementation checks

## Result

The complete cleanup from baseline
`f05c478a29c39f94968fdc842a34c861d30a42ac` removes exactly eight files: the obsolete
delegation TOML and seven root skill copies (61,153 Git blob bytes). The schema-4
lock selects `skill_ownership.provider = "plugin"`. Evaluator 0.18.0 and all
unrelated lock entries are unchanged. Product templates, runtime, package inputs
and both marketplace publication refs are preserved.

The owner's exact two-link README repair is unchanged, with SHA-256
`240bf535c917234225d19e0efe1b48521322eb6f6504c5b7a5619a9e866546dc`.
The previously deleted value-proposition documents remain absent.

## Authority and replacement

The owner approved SPEC-DST-029, VER-PLG-025, WO-PLG-025 and the explicit replacement
disposition of WO-PLG-024 with "i approve" on 2026-09-16. The released evaluator
compared the four reviewed byte hashes and applied those decisions atomically.
WO-PLG-024 is rejected as replaced; its original body, scope and lifecycle events
are preserved. Its approved VER and all eight retained evidence files remain
unchanged. This does not claim the first work order passed acceptance.

Codex started WO-PLG-025 after passing start preflight and its transition preview.
Its approval records the complete 30-path scope. After passing the Git-derived
handoff and completion preview, Codex recorded WO-PLG-025 as implemented. The
ready VREC is prepared after the local candidate commit for the assurance owner.
VREC-PLG-021 remains absent. VREC-PLG-022 selects only WO-PLG-025 and VER-PLG-025.

## Corrections and review

- Onboarding tests compare four native installation commands and their arguments
  with the retained Git marketplace instructions. They check explicit setup,
  Python prerequisites, the published plugin/checker identities, offline wheel
  installation and the boundary between installation and project mutation.
- Linked manual guidance is checked where it lives. The installation examples
  must contain both init and doctor and parse against the existing CLI. The
  expected example counts prevent empty command selections from passing.
- Skill-note checks require actual retained plugin/template SKILL.md files.
  Current technical-communication guidance points to those sources and the
  contributor restoration guide. Only the Phase 4 historical banner changed;
  all three affected historical note bodies remain intact.
- The approved addendum replaces the obsolete inline manual-setup obligation.
  Other README presentation, link, image and authority checks remain in place.

The implemented-change review applied ARTIFACT_AUTHORING.md. Existing tests,
guides and released ownership commands satisfy this bounded change. No new
framework, runtime behavior, configuration mode or evaluator workaround was
introduced. The review checked 39 new local links before adding this report;
the final diff review passed with 50 local links including the evidence links.

## Observed acceptance

Windows, Python 3.13.3; candidate source 0.19.0 and governing evaluator 0.18.0.

| Check | Actual result |
| --- | --- |
| Focused onboarding suite | 15 tests pass. |
| Full source suite | 1,068 tests, zero failures, 15 skips; 544.008 test seconds, 545.838 wrapper seconds; 171 classes and 8 workers. |
| Distribution validator | 15 distribution-bearing records pass. |
| Candidate CLI help | Exit 0. |
| Candidate doctor | Exit 1 for the documented router, payload and selected-version skew between source 0.19.0 and installed root 0.18.0. |
| Released doctor | All 64 checks pass. |
| Released graph | 1,657 artifacts, zero errors, 48 existing warnings. |
| Review preflight | Ready; no diagnostics or skew. |
| Scope and preservation review | Complete diff covered; eight exact deletions; README, managed AGENTS fragment, old evidence and history preserved. |

The [full suite log](source-suite.log) retains the actual aggregate result.
Its `--workers must be at least 1` line comes from the suite's argument-rejection
test; the full run exited 0. [checks.json](checks.json) retains command arrays,
working directories, statuses, timings, runtime versions and raw-output digests.
The released Git-derived handoff is retained separately in this directory.

## Reused evidence and limits

[implementation-review.json](implementation-review.json) compares current inputs
with the original migration and portability observations. It confirms unchanged
source/template/plugin/release inputs, the same lock and released payload,
unchanged installed replacement files and all 24 files in each disposable native
host package. Those observations remain in [the original evidence](../WO-PLG-024/README.md)
and [checks](../WO-PLG-024/checks.json), which are explicitly selected for capture.

Reused observations cover plugin-independent doctor and same-release upgrade,
repository-skill restoration, switching back, repeat convergence and native
discovery. Hosts were Codex CLI 0.154.0-alpha.6.2 and Claude Code 2.1.269. Codex
briefing was explicit-only. These are earlier observed checks, not fresh host runs.
The real installed package still has the previously recorded README, LICENSE
and missing assembly-inventory differences; only its 21 runtime/discovery files
matched the accepted package. No full-package equality or new authenticity claim
is made.

The earlier 1,068-test run with 12 failures and 15 skips is preserved. Ten failures
concerned the old inline setup contract; two required root skill paths. The
approved addendum and four corrected test methods resolve them. The initial
partial suite, bad baseline fixture, failed scope and preparation checks remain
historical observations. Two local helper mistakes in this turn are also retained:
an invalid unqualified reason argument (no transition) and a nonexistent local
marketplace ref (read-only comparison). Their corrected invocations passed.

The first commit attempt stopped before creating a commit: staged whitespace
inspection flagged two space-only context lines in the original
`WO-PLG-024/readme-remediation.diff`. Those are retained raw diff content. Its
reviewed hash still matches. Whitespace inspection of every other staged path
passes; the exact raw evidence is preserved rather than reformatted.
A staging retry then named already-staged deleted files, which Git refused as
missing pathspecs. Inspection confirmed no commit and the expected staged
deletions. Resumption stages only remaining existing/indexed paths and checks
the complete staged inventory before committing.

No persistent host profile, remote CI result, public catalog listing, push, PR,
merge or release is established by these local checks. Completion and VREC
preparation leave the assurance decision to the owner.
