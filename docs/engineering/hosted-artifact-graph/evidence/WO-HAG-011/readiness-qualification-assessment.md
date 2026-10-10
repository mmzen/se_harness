# Draft readiness qualification — 10 October 2026

WO-HAG-011 remains **in progress**. This is an unfinished-work assessment, not
verification or permission to merge. Candidate: `9d4034dc293b6f1de7919400d6f8cc1bda356dbd`.

## What changed

The client now labels draft validation as a shape-and-link check, with content
review still unassessed. Raw evaluator results stay unchanged. The existing report
starts with content readiness. The existing guarded file reader accepts up to
eight explicitly selected independent files with a 64 KiB output bound. No new
service endpoint, lifecycle policy, semantic grader, dependency or host setting.

## Native results

| Trial | Candidate | Result | Seconds | Calls | Peak input context |
| --- | --- | --- | ---: | ---: | ---: |
| Codex71, missing-input case | `4ce7ffd09d0b991d29311a1164b1fa029a64a83e` | Blocked by sandbox localhost networking | 95.232 | 17 visible items; exact total unavailable | Unavailable |
| Claude81, missing-input case | `9d4034dc293b6f1de7919400d6f8cc1bda356dbd` | Content review failed | 279.029 | 19 | 56,057 |

Claude now reports **incomplete**, which fixes the misleading completion claim.
Its saved draft nevertheless invents an unconfirmed operational benefit and a
missing-confirmation problem. It identifies missing input only after submitting
that interpretation. Existing INT/REQ/SPEC were read; existing VER was not read
before claiming missing independent confirmation. The independent review fails
EFF-04A. The saved bytes match a separate service read; all seven imported records
remain unchanged. No failed native call was observed. Positive-case repetitions
were not run on this failed candidate. Earlier failures remain failures.

See [assessment](claude-81-assessment.json), [visible transcript](claude-81-visible.md)
and [exact bounded evidence](claude-81-evidence.zip). Private reasoning, raw host
events and credentials are excluded; the inventory identifies the omission method.

Codex can now run sandboxed file commands after the earlier MXC host repair.
The two service readiness calls still fail. A read-only probe records
`CODEX_SANDBOX_NETWORK_DISABLED=1` and Windows error 10013 for localhost.
The service works outside that sandbox, and its project remains at version zero.
No import or draft mutation occurred. See [assessment](codex-71-assessment.json)
and [network probe](codex-71-network-probe.json). No desktop-app process was stopped.

## Efficiency and simplicity

The changed guide grew from 888 to 906 words. The new batch-read capability was
not used: Claude81 made eleven Read calls. No repeated file paths were observed.
The new negative-case cost is not a positive-authoring performance result.

For the earlier comparable positive candidate, Claude72–74 took 240–258 seconds,
21–24 calls and 56,782–60,090 peak input tokens. All three content reviews passed;
all efficiency goals were missed. In Claude73 only 6.963 seconds were recorded in
client commands. The remaining wall time is unclassified, not a measured provider
or model duration. Ten known-path reads remain a practical reduction target.

The readiness label improved reporting but did not prevent invented content.
Another layer of warnings is not evidence of a solution. The next bounded
correction should make input sufficiency the first authoring decision and remove
conflicting read guidance, then repeat the original negative case unchanged.
Accepted checklist meanings and test criteria remain fixed.

## Checks and limits

Source suite: 1,336 tests, 24 skips, exit 0. Native-support checks: 24 passed.
Focused client checks: 15 tests, one skip, passed. Distribution checks, CLI smoke,
released validation (1,991 artifacts, zero errors, 63 warnings), scope and review
preflight passed. Exact reproducible build and packaged installation passed.
The check archive retains actual commands and recovered local preparation errors.

These checks do not establish native correctness. Changed client presentation
still needs its applicable installed-client/service EFF-02/03 evidence. Full
VER-HAG-007 NQ-01–05 qualification remains separate and incomplete. No new VREC
or work-completion transition has been prepared.

## Codex proposal requiring a new decision

[Review the bounded permission proposal](codex-permissions-20261010/review.md).
It is **unapplied**. Existing accepted VER-HAG-008 retains normal permissions;
changing that environment requires a linked amendment, not a hidden retry.
The proposal preserves workspace file protections, blocks external destinations
through a managed proxy and permits the owned local service. It explicitly
discloses that MXC can allow other localhost services; this is not port isolation.
The exact invocation and boundary probes must pass before any native rerun.

## PR state and next step

PR #543 stays draft, targeting main, under existing review-publication authority.
At refresh of remote `6ee08642651600298439cd9a3ca00b372c9e8806`, Engineering Harness
`validate` fails on WO-HAG-009 handoff evidence at formal snapshot
`4bf8b06a095c371ef09b36488e2117c6a7a204237ccc7bae47d2d9ed9234b291`.
Other completed source/package, upgrade and CodeQL checks passed. The draft is
not merge-ready. Preserve that blocker and the full comparison base.

The released evaluator selects `STEP-WO-IMPLEMENT-CHECK` for WO-HAG-011.
Continue independent in-scope corrections and retain actual results. Apply no
permission amendment until its human decision is recorded. Prepare verification
only after the required checks and independent content reviews pass.
