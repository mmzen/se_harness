# Canonical entry conditions and exact observation-file pointer

## Problem and change

Claude301 read selected lifecycle steps but omitted their file's entry conditions
and required authority references. It also treated an extensionless observation
record as a directory. The earlier failures remain unchanged in boundary35-result.

The public section reader now includes the same file's `Read this when` and
`Before this action` sections with a narrower selected section. It copies their
complete canonical bytes, keeps source/release/digest/line identity, and marks
automatically included entry sections. A selected parent already containing an
entry condition prevents duplication. It follows no links and selects no action.
Ambiguous entry headings fail instead of selecting one silently.

The plugin's current-action table places existing authority references beside
their action. The native observation result keeps its existing record path and
adds `record_type: file` and mechanical `read_arguments`. The tool index explains
that this path is a file even without an extension. No filename is invented.

## Design and authority review

SPEC-HAG-008 HAG-EFF-001 permits assembling canonical shared prerequisites in a
section view. The implementation uses the existing public reader under
WO-HAG-011. The adapter still calls that installed reader; it adds no separate
section algorithm. The helper change supplies a file pointer, not a content
assessment. All paths fit the existing WO-HAG-011 grant; native qualification
also follows WO-HAG-009 and VER-HAG-007.

This is a small extension of two existing results. It adds no selector option,
registry, dependency, workflow runner, evaluator-policy rule or service change.
The actor still selects the current step and applicable linked prerequisites.
Including at most two entry sections costs some context, but avoids requiring
another discovery call for prerequisites in the same file. No performance claim
is made. The full task remains a native observation, not scripted completion.

The selected released instruction files are unchanged. Five direct comparisons
against released 0.22.1 verify the exact returned content, line ranges and hashes.
The resource tests cover overlap, missing/ambiguous headings and fenced examples.
The native pointer test reads back the exact retained extensionless file,
including its original refusal, through the returned arguments.

## Checks and native limits

Focused results: 28 resource tests with two skips, 48 native-driver tests with
one skip, and 11 plugin tests with one skip; all exit 0. Required source,
distribution, CLI, scope, review-preflight and released-validation results are
retained in checks.zip before this implementation commit is created.

The next diagnostic uses the previous focused task bytes unchanged, with fresh
paths/project and final packaged guidance. It must be independently assessed.
Do not claim that entry delivery establishes comprehension, an evaluator gate
proves an executed assertion, or any refused request proves the requested scope
test. Keep the complete task's no-hints boundary and declared 20-minute limit.

WO-HAG-009/011 remain in progress. No completion, actual verification decision,
merge, release, deployment or host-plugin update occurs here. The current
released next step is `STEP-WO-IMPLEMENT-CHECK`.
