# Single-agent workflow skills MVP

<!-- Target expertise: 5/10. This score describes the knowledge expected from the reader, not the document's complexity or quality. -->

> This is non-authoritative operator guidance. The installed harness, exact
> released evaluator, formal artifact state, repository instructions, and
> accountable decisions remain authoritative.

SE Harness installs four portable agent skills. `harness-orient` is the
unchanged read-only entry point. Three explicit-only writing skills provide the
Phase 3 MVP:

| Skill | Use it for | Mandatory stop |
| --- | --- | --- |
| `harness-draft-change` | Create a declared planning note and complete formal drafts, or revise explicitly selected current drafts | Accountable content review, before approval or implementation |
| `harness-execute-work-order` | Implement one selected work order that is already `in_progress`, run repository checks, and retain declared evidence | Engineering-owner completion decision, before a lifecycle transition or Git action |
| `harness-prepare-assurance` | Prepare one exact-candidate `ready` verification record through the existing evaluator operation | Assurance-owner decision, before verification or delivery |

The skills complement `harnessctl`; they do not replace it. A skill supplies a
portable procedure and guardrails for an agent. The exact released evaluator
still supplies integrity checks, formal-state projections, lifecycle legality,
canonical destinations, gates, and preparation operations.

## Activation and inputs

Writing requires the operator to name the exact skill and one unambiguous
target. Discussion, explanation, or a general request does not activate a
writing skill. Every invocation uses a structured evaluator launcher array and
expected evaluator version and root. It also records the requested outcome and
declared non-effects.

Each skill validates its retained `skill-contract.json` and portable-core
digest, establishes evaluator identity and integrity, checks current formal
state, builds a closed effect plan, and repeats the applicable checks
immediately before a controlled effect. Paths must be repository-relative,
portable, and admitted by the selected draft plan, work-order execution scope,
or evaluator-derived VREC destination.

## What the MVP does not do

No Phase 3 skill approves an artifact, starts or completes work, verifies a
record, selects delivery, releases software, mutates Git, uses credentials,
accesses the network, or performs an external action. All three use one agent;
they do not spawn workers. Their receipts and packets are evidence, not
accountable decisions.

The skill procedures cannot force a hostile runtime to obey them. Runtime-
enforced autonomy envelopes and multi-agent execution belong to later work.

## Installed files and upgrades

Canonical sources live only at
`templates/repository/standard/.agents/skills/<skill-name>/`. A repository
installation receives one managed copy at `.agents/skills/<skill-name>/`.
Codex discovers that copy directly. The three writing cores include a small
`agents/openai.yaml` policy that disables implicit invocation; the unchanged
orientation core has no Codex policy file.

Claude Code discovers one managed same-named adapter at
`.claude/skills/<skill-name>/SKILL.md`. That adapter contains discovery and
loading instructions only. It resolves the canonical `.agents` directory from
the repository root, stops on a missing or invalid binding, and then yields to
the canonical procedure. It does not copy the procedure, contract, or helper.
Writing adapters disable model invocation, so the user must invoke those
skills explicitly; orientation remains available for normal read-only matching.

`init`, `adopt`, and the ownership-aware upgrade transaction handle all four
cores and adapters. Customized installed bytes block an ambiguous upgrade
instead of being overwritten. Installing a newer Python package alone does not
rewrite an existing repository; its owner must review and explicitly apply the
repository upgrade.

See [installation and safe upgrades](harness-installation-and-upgrades.md) for
the package and repository update procedure, and
[repository host adapters](agentic-execution-host-adapters.md) for the Codex
and Claude discovery mapping, and
[read-only agent orientation](harness-orient.md) for the unchanged orientation
workflow.
