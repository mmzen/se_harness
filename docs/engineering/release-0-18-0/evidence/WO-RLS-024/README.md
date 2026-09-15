# Release preparation evidence

Baseline: main fa493ceb1c78a1bf79dadab3560cb36167557ce1. Checker source is
0.18.0; the isolated repository-selected evaluator remains 0.17.0.

## Prepared and checked

- Both native manifests select verity-plane 0.1.0. The production plan selects
  all 19 tracked common files plus each host's own manifest and README. Existing
  plan/path/content validation passed; no final release archive is claimed.
- The full Windows source suite passed. Distribution validation, portable
  source checks, CLI help, released graph and doctor, and review preflight pass.
  [Actual local commands and results](local-checks.json) retain the suite count,
  skips and the evaluator used. Existing historical-layout warnings remain.
- Independent review checked the complete release packet, its 39 work orders,
  exact 31-contract union and every coverage link; no blocking issue was found.
  [Coverage](coverage.md) reuses the existing member evidence.

The initial start preflight identified an omitted applicable architecture link.
Selecting existing ARCH-PLG-004 and ADR-PLG-004 resolved it before execution.
Legacy VER-DST-001 adoption coverage uses current init for existing repositories,
as established by SPEC-ECP-022 ECP-DEL-015–019 and WO-ECP-029. The retired adopt
alias is not a release requirement. Current KISS amendments govern current
behavior; historical records keep their original meaning.

## Hosted candidate qualification

Exact source candidate: 02d7958d61821a6fca20eab0173bf9b33be961aa.
The branch-push [candidate workflow](https://github.com/mmzen/se_harness/actions/runs/34935510844)
passed: source qualification, the full Linux suite, candidate package acceptance,
and both Windows and Linux predecessor-upgrade/plugin checks. The
[job results](hosted-ci.json) retain actual step conclusions, including skips.

The manual [publication rehearsal](https://github.com/mmzen/se_harness/actions/runs/34935534971)
passed. Its two pinned Linux builds produced identical checker wheel and source
archive bytes. The [build summary](build-summary.json) identifies the exact run,
candidate, recipe and digests; [candidate-bundle.json](candidate-bundle.json)
retains the original bundle manifest. This is unbound preparation evidence.
It must not be silently rebound to a later verification candidate.

This workstation has no Docker. Its earlier non-promotable native wheels were
not used as the release build. The released-record leg in the same rehearsal
checked existing RLS-SEH-026; it is not a replay of a new 0.18.0 release record.

## Completion and aggregate verification preparation

The owner approved completion of WO-RLS-024 and requested the verification
record. The [instruction](owner-completion.md) records the actual request.
WO-RLS-024 is implemented. No new aggregate verification decision has been made.

The final preparation candidate adds this completion decision and evidence to
the checked preparation head 8b82153d00af8ab9119494880f4999fff00c81be. Its product
and build inputs remain unchanged from the qualified source candidate above.
The aggregate record covers all 39 selected work orders and 31 verification
contracts, with one existing evidence path for each. Historical member evidence
retains its stated candidate and limitations.

The record binds the clean completion candidate. Before presenting it for
verification, check that candidate's existing hosted qualification and obtain
its matching recipe replay. Retain those run identities in the accompanying
preparation note; do not change the earlier bundle manifest or claim it is bound
to this later candidate. New release-record preparation follows actual
verification. Final plugin assembly still needs the released checker and its
public wheel. Root evaluator 0.17.0 and live installations remain unchanged.

Raw local attempts remain outside Git in work/release018-checks. No tag,
release, publication, live installation or root upgrade was performed.
