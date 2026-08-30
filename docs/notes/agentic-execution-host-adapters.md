# Repository host adapters for SE Harness skills

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. Installed managed files, the
> exact released evaluator, formal artifact state, and accountable decisions
> remain authoritative.

SE Harness uses one canonical skill core for each workflow. Provider-specific
files make that core discoverable; they do not define another workflow.

| Host | Discovery surface | What runs |
| --- | --- | --- |
| Codex | `.agents/skills/<name>/` | The canonical skill directly |
| Claude Code | `.claude/skills/<name>/SKILL.md` | A thin adapter loads `.agents/skills/<name>/`, then yields to the canonical skill |

The shipped name is `harness-orient`; `harness-draft-change`,
`harness-execute-work-order` and `harness-prepare-assurance` were retired
from the template on 2026-08-29 under `WO-ECP-006` (`REQ-ECP-014`), and their
adapters with them.

## Why Claude uses an adapter

Claude Code discovers repository skills under `.claude/skills`, while the
portable SE Harness cores live under `.agents/skills`. Copying the whole skill
would create two procedure bodies that could drift. Linking the directories
would be unreliable across wheels, Git checkouts, and Windows installations.

The adapter therefore contains only:

- the same skill name and a short discovery description;
- the fixed same-name canonical `.agents` path;
- explicit-only provider policy for a writing skill; and
- fail-closed instructions to load and validate the complete canonical core.

It contains no helper, contract copy, lifecycle rule, tool grant, model choice,
hook, subagent, shell command, remote reference, or external permission.

## Activation behavior

The three writing skills are user-explicit-only in their portable contracts.
Their Codex metadata disables implicit invocation, and their Claude adapters
set `disable-model-invocation: true`. A broad request to discuss, explain, or
write something does not activate them.

`harness-orient` is different: it is read-only and remains eligible for normal
matching. Its canonical v1 core is unchanged and has no Codex policy file. Its
Claude adapter omits the writing-only activation field.

Provider policy is defense in depth, not engineering authority. Even if a host
selects a writing skill incorrectly, the canonical skill still requires exact
explicit activation and stops before an effect.

## Loading and failure behavior

A Claude adapter resolves exactly `.agents/skills/<same-name>` from the project
root. It must read the complete canonical `SKILL.md`, validate the matching
contract and managed integrity, and load relative resources from that canonical
directory. It does not search the user profile, another repository, a plugin,
the network, or the current `PATH`.

If the core is missing, renamed, damaged, mismatched, outside the repository,
or not loadable, the adapter stops before a helper or repository effect. A host
may need a fresh session after a new top-level discovery directory is installed;
that restart is an operational discovery step, not a harness lifecycle action.

## Installation and upgrades

All canonical files, Codex policy files, and Claude adapters are package
inventory and managed-lock entries. Fresh `init` and `adopt` operations install
them atomically. Existing repositories receive them only through a reviewed,
explicitly authorized upgrade. Customized or conflicting destinations block
the transaction and preserve the previous repository bytes.

The repository-local design intentionally does not install user-wide skills or
provider plugins. It makes skills available by default inside an applicable
managed repository while keeping repository integrity and ownership visible.

See [single-agent workflow skills MVP](agentic-execution-skills-mvp.md) for the
workflow boundaries and [installation and safe upgrades](harness-installation-and-upgrades.md)
for the repository update procedure.
