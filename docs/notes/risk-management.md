# Risk management

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Non-authoritative operator guidance. The installed harness, the exact released
> evaluator, the formal artifacts, and accountable decisions remain authoritative.

A `risk` is a formal artifact that records one thing that could go wrong at a
declared stage of the process, how likely and how bad it is, and what an
accountable human decided about it. Anyone can identify one; repository policy
decides whether it must be raised; only the owner of the stage it threatens
disposes it; and a release names the risks it ships with.

## Identify

```powershell
harnessctl raise-risk . --domain <domain> --id RISK-<DOMAIN>-001 `
  --title "A stacked pull request orphans the ready record" `
  --stage implementation --category process --likelihood 4 --impact 3 `
  --threatens WO-<DOMAIN>-001 --cause "..." --effect "..."
```

`raise-risk` is preparation. It writes one file at
`docs/engineering/<domain>/risks/RISK-<DOMAIN>-001.md`, computes
`score = likelihood x impact` on the 5x5 scale, copies the acceptance level in
force, and sets the status: `raised` when the score reaches the level,
`identified` otherwise. The comparison is recorded as a computed event
(`decided_by = "harnessctl"`); it is not a decision.

A new `identified` or `raised` risk file is always an admitted changed path,
whatever the work order's execution scope says. An agent mid-implementation
can raise a risk without widening its scope. A disposed risk is not covered by
that exception; disposing is a transition, not a file edit.

Stages and the artifacts they may threaten: `definition` (INT, CAP, REQ),
`architecture` (SPEC, ARCH, ADR), `implementation` (WO), `verification` (VER,
VREC), `release` (REL, RLS), `operation` (OPS). Categories: safety, security,
compliance, process, schedule, quality.

## Policy

```toml
[risk]
acceptance_level = 1          # 1..25; a score at or above it must be raised
scale = "5x5"
release_requires_disposition = true
```

The default when the section is absent is `acceptance_level = 1`: every
identified risk is raised. A repository lowers the bar deliberately in its
hash-locked installation file under an approved change. A later policy change
never reclassifies a stored risk; each risk carries the level that was in force.

## What a raised risk blocks

One gate predicate, `undisposed_risks_threatening_scope`, sits in seven gates.
A `raised` risk that threatens the selected artifact or its governing chain
fails definition approval, work start, work completion, the assurance decision,
and both release gates. A `mitigating` risk fails only the release gates. An
empty register passes. `harnessctl check` renders the blocker with the risk,
its score and level, and the disposing role; the corrective form is an
escalation to `DR-RISK-DISPOSE`.

`harnessctl risks . --artifact WO-...` lists the register for one artifact and
its chain; `inspect` queues every raised risk under "Decision required" as
`dispose-risk`.

## Dispose

The disposing role follows the stage: product or domain owner, technical
owner, engineering owner, assurance owner, release owner, service owner. The
transition names the artifact, the target, the actor, and a reason:

```powershell
harnessctl transition . --set RISK-X-001=mitigating --decision RISK-X-001=engineering-owner `
  --reason "RISK-X-001=mitigated_by WO-X-002: add the orphan diagnostic" --apply
harnessctl transition . --set RISK-X-001=avoided --decision RISK-X-001=technical-owner `
  --reason "RISK-X-001=avoided_by ADR-X-003" --apply
harnessctl transition . --set RISK-X-001=accepted --decision RISK-X-001=engineering-owner `
  --reason "RISK-X-001=accepted: the diagnostic lands next release" --apply
harnessctl transition . --set RISK-X-001=mitigated --decision RISK-X-001=engineering-owner `
  --reason "RISK-X-001=residual 2x3 accepted by the engineering owner" --apply
```

- `mitigating` needs `mitigated_by` naming work orders, requirements,
  verification contracts, or operating contracts; the risk keeps blocking
  release until every named work order is covered by a verified record.
- `mitigated` needs `residual LxI`; a residual score at or above the level must
  say it is `accepted`.
- `avoided` needs exactly one `avoided_by ADR-...`.
- `withdrawn` is for duplicates and non-risks; it is terminal, like the others.
- A wrong actor, a missing reason, or a missing relation is refused before
  anything is written; a disposition changes only the risk.

## Release

`prepare-release` refuses while any `raised` or `mitigating` risk threatens the
released work, and derives `lists_risks` — every `accepted` or `mitigated` risk
that does — into the ready record and its body. That list is what an
attestation that "risks were identified and mitigated or accepted" rests on.

## Skills and doctor

`harness-draft-change` and `harness-execute-work-order` may raise a risk they
notice, under the `risk-raise` effect class, which admits only a new risk
artifact path; `harness-prepare-assurance` runs `harnessctl risks` for each
selected work order and includes the register in its packet. No skill
disposes a risk. `harnessctl doctor` reports `C-RSK-001` when the `[risk]`
section of the installation file is invalid; `raise-risk` runs under its own
mutation-guard operation.

## Boundaries

Scoring is ordinal and the scale is 5x5; there is no quantitative model, no
per-category level, and no dedicated risk-owner role. The harness does not
check that the raiser and the disposer are different people; a solo owner
still records which right was exercised and why. Risks in this repository's
own root appear only after its released evaluator is upgraded to a release
carrying this capability.
