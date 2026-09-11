# Missing-enforcement observations

WO-PLG-006 remains in progress. The C10 and C11 experiments completed their
required observations, but enforcement failed and the affected routes remain
unqualified. This does not turn the successful C09 running-handler observations
into a universal guarantee or authorize a case waiver.

[C10](C10/observations.json) records native cancellation at 60.161 seconds,
no denial, and one successful exact Write. [C11](C11/observations.json) records
successful exact Writes after launch failure, empty output, invalid output and
removal of the inline binding after a previously verified startup. The removal
experiment uses a subsequent native activation; it claims no continuous-session
hot reload. Every effect has a correlated tool result and independent target hash.

The official [timeout documentation](https://code.claude.com/docs/en/hooks#timeouts)
says timed-out command hooks leave PreToolUse to ordinary permissions. The
[exit-code documentation](https://code.claude.com/docs/en/hooks#other-exit-codes)
describes launch failures and missing/invalid output without a blocking result as
nonblocking. These pages were inspected on 2026-09-11 and corroborate the captures.

The shorter inner deadline addresses C09 while the guard is running. It cannot
emit a denial when the guard or its output is lost. No documented native option
that closes that gap within the accepted inline command route was found in this
inspection. An SDK callback or an independent permission boundary requires its
own approved architecture and qualification; neither is implemented here.

The engineering owner must disposition this bounded result before completion.
No supported production profile, VREC, lifecycle transition, definition amendment,
release or installation outside the disposable fixtures is claimed.
