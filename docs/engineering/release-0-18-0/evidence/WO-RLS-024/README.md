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

## Decision boundary

WO-RLS-024 is in progress. The owner selected and started this bounded release
preparation through the delegated route on 2026-09-15; no result-specific
completion, new aggregate verification or release decision has been recorded.
The installed 0.17.0 evaluator still determines those lifecycle steps. Root
adoption of the candidate's simpler route is a later explicit upgrade.

After completion, prepare one aggregate VREC for all 39 members, using their
existing evidence and this integration summary. Its accountable verification
precedes release-record preparation and binding. The final selected commit must
have matching hosted build evidence. Final plugin assembly consumes the checker
only after its released record and public wheel are available.

Raw local attempts are retained outside Git in work/release018-checks. Hosted
artifacts have their workflow's retention period; retain the concise build
manifest and run identity in this packet before they expire. No tag, release,
publication, live installation or root upgrade was performed.
