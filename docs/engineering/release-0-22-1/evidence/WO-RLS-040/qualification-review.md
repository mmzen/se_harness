# Evaluator 0.22.1 preparation review

Status: qualification in progress. No final verification or release is requested.
WO-RLS-040 and WO-RLS-041 remain in progress; WO-RLS-042 remains approved.
Released evaluator 0.22.0 governs this checkout.

The tested preparation source is `89c69748fcc5fc2578acef5cbf48f0734ef1b732`,
based on main `82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`.
It includes the two approved HAG evaluator corrections and main's 4 MiB
dashboard correction. All 124 transported HAG records/evidence files retain
their exact source bytes. The unfinished hosted service is excluded.

## Observed checks

| Check | Result |
| --- | --- |
| Windows full source suite, Python 3.14.6 | Passed: 1,287 tests, 22 reported skips. |
| Ubuntu full source suite, Python 3.12.3 | Passed: 1,287 tests, 2 reported skips. |
| Distribution and CLI checks | Passed; 22 distribution records. |
| Pinned Linux/amd64 build, CPython 3.11.9 | Two independent builds produced identical wheel and sdist bytes. |
| Windows/Linux installed wheel and index-selected sdist | Initialization, doctor and validation passed. |
| Installed HAG corrections | Draft-admission decisive cases and actual human/owner decision mapping passed on both platforms, including refusals and unchanged-byte checks. |
| Installed topology limit | Exactly 4,194,304 bytes; below/equal/above boundary passes on both platforms. |
| Actual complete candidate topology | 2,170,877 bytes; repeated bundles identical; all eleven predecessor revisions preserved. |
| Actual 0.22.0 to 0.22.1 upgrade | Two runs on each platform passed with the same semantic digest. |
| Plugin 0.2.6 package assembly | Both platform builders and their own independent check-stage passed. Expanded contents/inventories match; compressed ZIP bytes differ across runtimes. |
| Native host delivery | See [plugin review](../WO-RLS-041/qualification-review.md). |
| Hosted CI rehearsals | Not yet run for this preparation branch. |

The wheel digest is `0a9f87f235839689dbbca3b10013b5df2a71dc134b53795248f78de8e1cfec49`.
The sdist digest is `c495536e19c9d9021c3de5b6e51ce316a7847af95ebd2920d9eab420f420d48f`.
[The retained bundle](bundle.json) records the exact source, recipe and identities.
These are preparation inputs, not a frozen final release candidate or publication.

## Retained failures and limits

- The first Linux container attempt had no Git and stopped before tests. The
  Ubuntu run used full history and passed; the failed attempt remains retained.
- The first Windows upgrade fixture hit Git's path limit. A process-local
  `core.longpaths=true` corrected the test environment; both reruns passed.
- An isolated invocation of a source-only test module failed to import its test
  support. The supported standalone installed-package CLI probe passed; no
  checkout imports were added to the candidate environment.
- An additional whole-ZIP cross-runtime equality assertion failed. Detailed
  comparison confirms equal member bytes, metadata and inventories. The exact
  Windows staged tree is selected for this preparation. Cross-runtime compressed
  byte reproducibility is not claimed. The existing publisher checks frozen blobs.
- Source/installed tests do not verify the hosted service. No hosted scenario ran.

## Provider readiness

The live `pypi` environment still requires reviewer `mmzen`. Its allowed ref is
only `main`; workflow defaults remain read-only. Main is protected by active
ruleset 20693381, including PRs, the required `validate` check, deletion and
non-fast-forward protection. The legacy branch-protection endpoint's 404 does
not mean main is unprotected. Only merge commits are allowed by that ruleset.

[The exact configuration proposal](provider-configuration-proposal.json) removes
only the redundant pypi reviewer. This has not been applied or authorized by this
release-preparation approval. PyPI's current account-side Trusted Publisher
binding remains unverified; historical success is not a current settings readback.
The complete-release route must not be reported executable until both items
are resolved. No provider settings, release tags, public packages or adoption
records were changed.

## Evidence and continuation

[Raw qualification observations](qualification-initial.zip) retain commands,
outputs, failures and relevant helpers; [the archive index](qualification-archive.json)
binds their exact bytes. Native evidence is retained separately. Temporary test
profiles and credentials are excluded.

Finish required walkthrough/desktop and CI evidence. Resolve provider activation
through its separate reviewed change. Then capture the final aggregate VREC,
publish its review, obtain human verification, prepare the exact RLS and freeze
the complete delivery plan. Earlier HAG verifications retain their original scope.
