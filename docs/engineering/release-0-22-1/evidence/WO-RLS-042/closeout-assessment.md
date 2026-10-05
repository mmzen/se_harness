# Public delivery verification assessment

Evaluator 0.22.1 and plugin 0.2.6 were delivered under RLS-SEH-033's unchanged
complete-release approval. The five-surface report is complete. This separate
assessment covers WO-RLS-042's retained observations under VER-RLS-038; it does
not change the binary candidate or supply a human verification decision.

| Requirement | Result | Evidence |
| --- | --- | --- |
| REQ-RLO-019 | Pass | Independently downloaded GitHub and PyPI archives have the approved hashes; isolated public wheel installation and qualification pass. Codex and Claude Code each pass fresh install and actual update from retained public 0.2.5, exact installed-content comparison, skill discovery and bundled evaluator setup. Frozen source and packaged links pass; live Pages bytes match publication provenance. |
| REQ-RLO-020 | Pass | observations.json and delivery-result.json retain every surface, exact identity and content-bound evidence. Prior failures remain in publisher.json. A preparation or publication result was never substituted for an unperformed public test. |
| REQ-RLO-022 | Pass | The trusted-main publisher reused the approved archives and staged marketplace tree. Independent readbacks confirm v0.22.1, release/0.22 and last point to the binary candidate, latest is v0.22.1, and plugin-marketplace is the approved ordinary child. Protected receipt integrations used exact checked heads and unchanged allowed paths. |

## Failures and recovery

The first marketplace attempt could not find the just-published version on the
PyPI index. Independent downloads later confirmed exact public bytes; retrying
the failed jobs succeeded. The next marker attempt refused absent committed
public observations. After PR #537 integrated those observations with passing
CI, the existing publisher promoted the markers. Its same-job report initially
still read the earlier pending marker observation. Actual marker readbacks were
retained and the final receipt-only PR integrated the complete report. No failed
check was waived and no approved payload, plan or destination was substituted.

The local whitespace check first treated CRLF line endings as trailing spaces.
The follow-up check declared CRLF as the permitted line ending and passed; all
spaces and blank-line checks remained enabled, and bound receipt bytes were
unchanged. Both command results are retained in the closeout checks archive.

## Scope and limits

The original work baseline remains the release decision commit
`baddb61881724fa65984c0e7d1d89f4edc8b1763`. Receipt-only delivery integrations
are retained separately; this later assurance commit records the actual start
and completion of WO-RLS-042, the assessment, checks and its verification record.
No repository source, template, workflow, accepted definition or package changes.

Codex Windows desktop remains unverified under accepted DEC-RLS-009 / RISK-RLS-007.
These public routes exercise native CLI installation/update and setup; they make
no desktop or live model-session claim. Hosted-service tests, adoption and HAG
pin amendments remain excluded. The release candidate's prior verification and
the already applied complete-release authorization are unchanged.
