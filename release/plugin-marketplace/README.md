# Verity Plane marketplace

Verity Plane brings SE Harness setup, orientation, change and evidence workflows
to Codex and Claude Code. Plugin **0.1.0** includes the published **SE Harness
0.18.0** wheel and five skills, including an explicitly requested operator brief.

## Install from Git

These commands select the `plugin-marketplace` distribution branch of
`mmzen/se_harness`. The development branch contains assembly inputs; install the
complete distribution branch. If that ref is unavailable, use a locally built
distribution below until publication is complete.

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
Plugin versions already cached by the host may require its ordinary marketplace
refresh/update command. Each host maintains its own installation.

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

Local native acceptance is checked on Windows. Package identity alone does not
prove a model-driven session, another operating system, public Git installation
or provider approval. The source repository's WO-PLG-023 evidence records actual
checks; public installation is reported separately after observing the Git ref.

Provider listings require their own review. [Submission materials](submissions/README.md)
identify the OpenAI and Anthropic routes and missing publisher inputs.
Report problems through [GitHub issues](https://github.com/mmzen/se_harness/issues).
