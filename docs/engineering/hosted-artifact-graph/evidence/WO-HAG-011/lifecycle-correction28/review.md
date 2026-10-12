# Hosted lifecycle guidance correction, candidate28

Claude's previous full run timed out after wrong instruction headings, decision
fields and handoff inputs caused repeated recovery. Codex also loaded whole
procedure files after a missing section selector. The slowness RCA remains at
`../../WO-HAG-009/slowness-rca-20261011/RCA.md`.

## Change

- Replace broad procedure-file references with exact current-action sections.
- Point evidence preparation back to that one routing table.
- Clarify the paired decision target, actor field and retained scope boundary.
- Point to existing action schemas for recovery without rereading all actions.
- State the test helper's actual rehearsal spelling and file-encoding operation.

Only two plugin references and the existing native tool index change. No new
command, service behavior, evaluator rule, permission or acceptance criterion is
introduced. The agent still chooses every action and authors its own requests.
The guide is longer because it now names exact destinations; this is a bounded
navigation correction, not a claim of lower overall context or duration.

## Checks and next test

All 15 released resource selectors and nine schema pointers resolve against the
selected 0.22.1 resource and unchanged v2 schema. The 40 focused native tests,
full source suite, distribution checks, CLI smoke, scope, review preflight and
released validation pass; exact outputs are in `checks.zip`.

The first focused invocation failed in the host sandbox's inaccessible temporary
directory. The failure is retained. The authorized rerun used task-local scratch
storage and passed; no product code changed in response.
The first full suite reported one Git fixture error. An isolated attempt from
the tests directory then failed module import; the correct repository-root
invocation passed in a shorter temporary directory. The repeated full suite
also passed there. These preparation failures remain in the archive; no test
was changed or skipped to obtain the passing result.

Next run a separately labelled native Claude diagnostic using a fresh private
project and the already-defined greeting fixture. Its desired result is risk
mitigation and a passed handoff for the supplied work, rather than reauthoring
seven definitions. Keep actual calls, content, failures and independent replay.
This diagnostic is not the full NQ run or a comparable EFF performance sample.
No native pass is claimed by this preparation review. Required full qualification
and human verification remain pending. No accepted criterion is changed.
