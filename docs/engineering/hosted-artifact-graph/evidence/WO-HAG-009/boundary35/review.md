# Native output-boundary correction

## Problem and change

Claude 291 wrote five command records and stdout siblings in `native/` instead
of the task's allowed `native/work/`. The helper checked only the wider native
workspace, while its observation index scanned work files. Those historical
files are retained unchanged in context34-result.

One shared `work_output` guard now constrains command records, stdout files,
compact evidence directories, exports and observation captures to new paths
inside `work/`. It reuses the existing containment, link and overwrite checks.
Invalid output paths stop before a child command or observation runs. The tool
index states the common write/read boundary and relative-path meaning.

No lifecycle decision, next step, request value or retry is selected by this
guard. The client, service, released evaluator, task meanings and host permissions
are unchanged. This is a test-driver correction under WO-HAG-009's existing scope.

## Validation and review

- 47 focused native tests pass; one host-dependent symlink-creation case skips.
  The new deterministic link-refusal test still runs on this host.
- Tests cover invalid records for remote calls, assertions and observations;
  export and compact-evidence destinations; absolute/relative valid outputs;
  traversal, linked paths and preserving existing captures.
- Fresh analogues of all five actual misplaced Claude capture locations refuse
  before any command runs. No original evidence is modified.
- The first focused attempt failed while creating fixtures in the sandbox's
  default temporary directory. The exact failure is retained. A dedicated
  temporary directory allowed the suite to run successfully without changing
  product or host security settings.
- Full source, distribution, CLI smoke, scope, review preflight and released
  validation results are in the accompanying checks archive. Commit preparation
  requires their successful results; native qualification is separate.

This is one small guard in the existing helper, with no new command layer or
workflow engine. A native diagnostic will exercise procedure use and the actual
scope/changed-draft cases before another full qualification. A focused pass does
not repair earlier failed full runs or satisfy the whole verification contract.

WO-HAG-009/011 remain in progress. No completion, human verification, merge,
release, adoption or plugin installation is performed by this correction.
