# Release preparation progress — 2026-10-12

This records unfinished WO-RLS-045 work, not a qualified candidate or human
verification. WO-RLS-045/046 remain in progress; WO-RLS-047 is unstarted.

## Implemented under WO-RLS-045

Core source is 0.23.0. The sandbox helper checks the client against committed
source, wheel metadata and both replayed build digests. For release plugins it
uses the existing full stage checker and retains the exact checked ZIP bytes.
The original development assembler remains available. Current guidance separates
bundled 0.23.0 from the service's unchanged evaluator 0.22.1.

## Actual checks

[Command captures](progress-checks-01.zip) include working directory, exact
arguments, exit status, duration and output. The source was a working tree;
these checks are not final commit-bound qualification.

| Check | Observed result |
| --- | --- |
| Helper boundary tests | 12 passed after the initial sandbox temporary-directory refusal. |
| Progressive documentation | 20 passed. |
| CLI help | Passed. |
| Distribution surface | Passed, 23 distribution-bearing records. |
| Packaged installation guidance | 10 run, one remaining failure: checkout.md is absent from the fixed assembly map. The earlier obsolete activation-heading failure is also preserved. |

## Diff review and remaining work

The helper reuses the existing staging checker instead of defining another
package acceptance policy. The new boundary tests cover wrong source/version,
replay and archive identities, incomplete inputs and the retained development
route. Actual checked-stage integration and service/container tests remain
required; synthetic passes are not substitutes.

Review found two omitted paths: the runtime's client-version check and the
fixed plugin assembly map. The [revised correction proposal](../WO-RLS-048/review.md)
is pending. The runtime, assembly map and accepted release contract remain
unchanged. The packaging failure is not waived or weakened.

Full Windows/Linux source suites, installed archives, pinned builds, staged
plugin/native checks, service walkthrough and recovery, release rehearsals,
and final aggregate assurance remain pending. Codex Windows desktop evidence
is separate and pending. No release, publication, adoption or host update occurred.
