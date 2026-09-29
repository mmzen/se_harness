# Repository host adapters for SE Harness skills

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. Installed managed files, the
> exact released evaluator, formal artifact state, and accountable decisions
> remain authoritative.

## Repository provider and plugin provider

The repository provider supplies two portable skill cores:
`harness-orient` and `harness-operator-brief`. Codex discovers their copies in
`.agents/skills/`. The supplied Claude Code adapter is for `harness-orient`;
it loads the same-name canonical core instead of duplicating its procedure.

| Surface | Supplied path | Purpose |
| --- | --- | --- |
| Repository core | `.agents/skills/harness-orient/SKILL.md` | Read-only orientation |
| Repository core | `.agents/skills/harness-operator-brief/SKILL.md` | Explicitly requested operator brief |
| Repository Claude adapter | `.claude/skills/harness-orient/SKILL.md` | Load the repository orientation core |

The Verity Plane plugin is a separate host installation. It supplies these two
skills plus `setup`, `change` and `evidence`; host-discovery metadata controls
which skills are offered. A directory present in a package is not proof that
the host exposes it. Check the installed host's actual discovery.

Plugin native hooks deliver the selected repository's compact instructions at
supported startup and compaction events. Repository skill adapters do not
install those hooks. Hook delivery does not enforce every tool invocation.
See the [plugin walkthrough](plugin-installation-guide.md) for tested routes and limits.

## Activation and loading

`harness-orient` is read-only and eligible for matching read-only requests.
`harness-operator-brief` requires an explicit request naming the skill and its
bounded source inputs. Neither grants implementation or decision authority.

The Claude orientation adapter resolves `.agents/skills/harness-orient/` from
the selected repository. It reads that complete core and its contract, then
follows the core's evaluator and integrity checks. It does not search another
repository or substitute a plugin when the selected core is absent.
Missing or incompatible inputs stop the affected skill operation.

## Installation and upgrades

Under repository ownership, these skill copies are editable supplied files.
The selected released installer maintains their inventory; existing repositories
receive changes through the explicit upgrade procedure. They are not additional
locked lifecycle policies.

The released `skill-ownership` command switches the provider. Selecting the
plugin removes disposable repository copies after checking the selected plugin;
restoring repository ownership writes the selected release's supplied copies.
Ordinary upgrades preserve the provider choice. This operation does not install
a host plugin, change the evaluator version or approve any engineering work.

Follow [contributor setup and restoration](developing-se-harness.md#agent-skills-for-this-checkout)
and [installation and safe upgrades](harness-installation-and-upgrades.md).
The selected repository's [provider procedure](../engineering/harness/SKILL_PROVIDER.md)
governs the change.

## Retired writing skills

`harness-draft-change`, `harness-execute-work-order` and
`harness-prepare-assurance`, with their Claude adapters, were retired from the
template on 2026-08-29 under WO-ECP-006. Their explicit-only activation contracts
describe that former delivery. The [single-agent skills MVP](agentic-execution-skills-mvp.md)
is retained history, not the current installation procedure.
