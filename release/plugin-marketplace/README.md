# Verity Plane marketplace

Verity Plane brings SE Harness setup, orientation, change and evidence workflows
to Codex and Claude Code. Plugin **0.2.5** targets **SE Harness 0.22.0** and five
shared skills, including an explicitly requested operator brief.

This source is part of the approved 0.22.0 release preparation. It does not prove
public availability. A released assembly must contain the exact independently
public evaluator wheel. Its PACKAGE-IDENTITY.json and assembly inventories record
the actual source, wheel and package digests. Use those identities when comparing
the installed package. Plugin updates do not adopt a repository's evaluator.

## Install from Git

These commands select the `plugin-marketplace` distribution branch of
`mmzen/se_harness`. The development branch contains assembly inputs; install the
complete distribution branch. Check that
the branch's `PACKAGE-IDENTITY.json` reports plugin 0.2.5, evaluator 0.22.0 and
the expected qualified source commit before claiming this new delivery.
Package installation, native session delivery and repository adoption are separate.

**Codex**

```text
codex plugin marketplace add mmzen/se_harness --ref plugin-marketplace
codex plugin add verity-plane@se-harness
```

**Claude Code**

```text
claude plugin marketplace add mmzen/se_harness@plugin-marketplace
claude plugin install verity-plane@se-harness
```

Start a new task or session after installation so the host loads the skills.
Each host maintains its own installation. For an existing Git installation:

**Codex**

```text
codex plugin marketplace upgrade se-harness --json
codex plugin add verity-plane@se-harness --json
codex plugin list --marketplace se-harness --json
```

**Claude Code**

```text
claude plugin marketplace update se-harness
claude plugin update verity-plane@se-harness --json
claude plugin list --json
```

Confirm the configured marketplace source first. A local marketplace with the
same name can select another tree. Restart the host, inspect the loaded plugin
path and compare its manifest and file hashes with `PACKAGE-IDENTITY.json`.
An existing cache directory alone does not prove which plugin the session uses.

## Install a local distribution

Replace `MARKETPLACE_DIRECTORY` with this directory's absolute path:

```text
codex plugin marketplace add "MARKETPLACE_DIRECTORY"
codex plugin add verity-plane@se-harness
```

```text
claude plugin marketplace add "MARKETPLACE_DIRECTORY"
claude plugin install verity-plane@se-harness
```

## Instruction delivery

This package includes native startup and post-compaction instruction hooks.
Plugin 0.2.5 resolves the entry from its exact selected wheel for the
external-resource layout, while retaining the repository-copy route for older
selections. It bootstraps an unselected session and activates the actual checkout
after cloning. Follow the packaged activation procedure for
[Codex](packages/codex/verity-plane/skills/setup/SKILL.md#activate-the-checkout) or
[Claude Code](packages/claude/verity-plane/skills/setup/SKILL.md#activate-the-checkout).
Native host qualification belongs to this exact release's evidence. Confirm
startup, compaction and resume for the actual loaded inputs. CLI observations
do not establish desktop support; older release-specific omissions do not apply.
Both routes reject missing, changed or incompatible selected input. They grant no lifecycle authority and do not
enforce all tool calls. Python must be available to the hook launcher; Codex
requires review and trust of the current hook definition. Confirm delivery
before governed work. Repository-only skills do not install these hooks.

## Prepare the checker for a project

You need Python 3.11+ with `venv` and `ensurepip`, and a host that can run local
shell commands. Invoke **verity-plane:setup** with your project and a persistent
data directory outside it. The skill explains the initialization or connection
steps and uses the project's selected evaluator for existing repositories.

Installing the plugin installs its files. Running setup installs the supplied
wheel **offline** into a private environment; it does not fetch SE Harness from
PyPI. Plugin installation alone does not initialize or upgrade a project.
On an empty project, the helper initially reports a missing harness; the setup
skill then follows the requested initialization and runs doctor.

For direct commands and repair, see the packaged setup references:

- [Codex setup](packages/codex/verity-plane/skills/setup/SKILL.md)
- [Claude setup](packages/claude/verity-plane/skills/setup/SKILL.md)

## Contents and support

`PACKAGE-IDENTITY.json` identifies the source commit, released wheel and every
distribution file other than the identity file itself. Native archives and
their source inventories are under `packages/`. Each native plugin is complete
inside its own directory; neither host needs the other host's files.

Native qualification targets disposable Windows profiles on both hosts. Package identity alone does not
prove a model-driven session, another operating system, public Git installation
or provider approval. Consult the source repository's WO-PLG-030 qualification
evidence and WO-PLG-031 public-route evidence for this package's actual results.
Neither a local result nor
this guide establishes successful public installation. Desktop UI, automatic
threshold compaction and other platforms require their own observations.

Provider listings require their own review. [Submission materials](submissions/README.md)
identify the OpenAI and Anthropic routes and missing publisher inputs.
Report problems through [GitHub issues](https://github.com/mmzen/se_harness/issues).
