# Native qualification evidence consolidation

WO-HAG-009 and WO-HAG-010 have passing native qualification evidence under
VER-HAG-007. This consolidation links that evidence to the current branch and
prepares the formal handoff. It does not record implementation completion or
human verification.

## Assessed result

| Required case | Claude CLI | Codex CLI | Retained evidence |
| --- | --- | --- | --- |
| NQ-01: instruction discovery and correct context | Pass | Pass | Each native archive: assessment/instruction-read-trace.json and assessment/independent-assessment.json |
| NQ-02: complete synthetic lifecycle | Pass | Pass | Each native archive: replay/assessment.json; 12 accepted operations replayed per host |
| NQ-03: refusals, recovery and seven MCP reads | Pass | Pass with disclosed read-only supplement | Independent assessments and codex-421-reads-evidence.zip |
| NQ-04: lost reply and idempotent retries | Pass | Pass | Exact requests, responses and independent receipt replay |
| NQ-05: exact export and preserved candidate | Pass | Pass | Two Claude exports and four Codex exports independently reconstructed |

The native archives and their inventories are in [final44-result](final44-result/).
[consolidation.json](consolidation.json) records their digests, checks every
inventory member, and retains exact component identities and evidence references.
Both agents supplied their own requests. There were no corrective prompts,
operator workflow mutations or scripted completion.

Codex's read result combines five tools from the original run with two tools from
a separate read-only session on the same fixed baseline. The independent observer
initially watched old trial directories; four delayed Codex comparisons returned
stale HTTP 409 responses. Those failures remain recorded and do not count as
matches. The supplement changed no graph state. The original C44 assessment
explains this recovery and all other qualification limits.

## Exact candidate and reuse

- Native tests: `2f6ecb1433ef98cf643e0f604ed2c4258a2261e2`.
- Branch inspected for this consolidation: `9fc3f4e2aa857e32ead50da8fa00fdca8e5e639a`.
- Complete PR comparison base: `55caaada508495bea7d97effd27644d1ce8373da`.
- Governor: separately installed released evaluator 0.22.1.
- Native candidate client: 0.22.2; candidate plugins: 0.2.7.

Exact Git blob and mode comparisons establish that the service, client, plugin
instructions, test drivers, build helpers and package definition are unchanged
from the native test candidate. Later changes outside formal artifacts/evidence
are only the two IPK archive-cap correction files. No native run is repeated or
represented as a run against this new evidence commit.

The later source checks passed 1,339 tests with 24 skips, distribution validation
and CLI smoke. Their commands, runtime, outputs, original long-path failures and
successful retry remain in the IPK local-check archive. Source/package checks at
`039443f333bea8aaa135526a99d7d4ead9c1e295` have no subsequent code changes. Its matching CI merge and package
identities are retained in the [IPK assessment](../../../integration-package/evidence/WO-IPK-002/verification-assessment.md).

At the inspected PR head, all source, package, upgrade, deterministic build,
Windows/Linux installation and retention jobs pass. Harness validation fails;
the current handoff checks will retain its exact remaining findings. Three
conditional release rehearsals are skipped, not passed.

## WO-HAG-010 routing correction

The approved bootstrap/setup correction routes an explicitly selected hosted
request before local checkout activation. Its original checks and failed Claude
trial remain in [WO-HAG-010](../WO-HAG-010/). The final native runs qualify the
unchanged packaged guidance for both hosts. The new digest references supersede
the old report's pending-trial observation without editing that historical report.

## Separate unfinished work

WO-HAG-011 has two focused Claude drafting failures under VER-HAG-008: one omits
a known evaluator version; another gives contradictory readiness conclusions
and invents a type-check obligation. Those results do not become passes here.
The full lifecycle checks above use VER-HAG-007. The evaluator reports no declared
dependency from WO-HAG-009/010 to WO-HAG-011. Combined PR acceptance remains pending.

The old C44 report records the then-unresolved archive-size failure and grouped
work status. WO-IPK-002 has since corrected that limit and VREC-IPK-002 is verified.
This report preserves the original report and distinguishes the separate work.

## Handoff and boundaries

Generated packets retain the evaluator-owned formal snapshot bindings. The
complete multi-work-order PR is checked against its original base with released
check-pr, which checks the scope union before each selected handoff. Individual
checks use the corresponding work-order paths in handoff-change-set.json; these
declarations do not replace the full PR scope check.

The handoff-check archive retains the exact individual schema-2 results, full
command records and combined PR result. check-pr does not write individual
handoff.json sidecars; no such generated output is claimed. A passing gate does
not itself complete or verify a work order.

Git remains authoritative. Synthetic decisions grant no real authority. Desktop,
automatic startup/compaction, public publication, production operation,
authentication/database ACL work and real authority cutover remain excluded.
RISK-HAG-001 and RISK-HAG-002 are not accepted or closed by this consolidation.


## Recorded handoff outcome

Both individual released handoff checks **pass**, with no blocking predicate.
Both review preflights pass. Released repository validation reports 1,994
artifacts, zero errors, 63 existing warnings and no authoring advisories.
The full PR scope check reaches WO-HAG-011 after passing WO-HAG-009/010,
then stops at its missing QGP-G4I-EVIDENCE handoff packet.

WO-HAG-009 and WO-HAG-010 remain `in_progress`. The individual handoff results
select `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-PREVIEW`: preview their transition
to `implemented` under the existing execution grant. No new human decision is
required for that preview. Completion and real verification were not applied
in this evidence-consolidation step.
