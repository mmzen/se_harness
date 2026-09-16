<p align="left">
  <img src="docs/images/verity-plane-logo.png" alt="Verity Plane" width="360">
</p>

## SE Harness / Verity Plane

<h4 align="center"><em>Delegate the work. Keep the authority.</em></h4>

SE Harness is an **open source harness for AI coding agents**. It connects intent, requirements, design, code, and evidence through engineering records stored in your repository.

The **`harnessctl` checker** checks the installed policy, traceability, and approved work scope. The **Verity Plane plugin** gives Codex and Claude Code skills to set up the harness, understand a project, carry out approved changes, and prepare evidence.

**Agents operate within bounded authority. Verification stays independent. Decisions stay human.**

[Get started](#get-started) · [Live demo](https://mmzen.github.io/se_harness/) · [Documentation](docs/notes/README.md) · [PyPI](https://pypi.org/project/se-harness/)

## Get started

Requires **Python 3.11+**. The checker runs on Windows, Linux, and macOS using the Python standard library. No hosted service is required for the checker.

### With Codex or Claude Code

Install from the project's published Git marketplace using your host's CLI:

**Codex**

```sh
codex plugin marketplace add mmzen/se_harness --ref plugin-marketplace
codex plugin add verity-plane@se-harness
```

**Claude Code**

```sh
claude plugin marketplace add mmzen/se_harness@plugin-marketplace
claude plugin install verity-plane@se-harness
```

Start a new task or session, then invoke **verity-plane:setup** with your project path and a persistent data directory outside it.

Plugin **0.1.0** bundles released **SE Harness 0.18.0**. Running setup installs that wheel **offline** into a private environment; it does not download the harness from PyPI. Plugin installation alone does not initialize or upgrade a project. Python must include `venv` and `ensurepip`.

See the [plugin setup guide](https://github.com/mmzen/se_harness/tree/plugin-marketplace#prepare-the-checker-for-a-project).

### With the CLI

Create a tool environment **outside your repository** and install the released package:

```sh
# Linux / macOS
python3 -m venv se-harness-env
source se-harness-env/bin/activate
python -m pip install se-harness
```

```powershell
# Windows PowerShell
python -m venv se-harness-env
.\se-harness-env\Scripts\Activate.ps1
python -m pip install se-harness
```

Initialize a project and check its installation:

```sh
harnessctl init my-project --project-name my-project
harnessctl doctor my-project
```

The same `init` command adopts an existing project: it preserves your files and records what it finds in `docs/engineering/ADOPTION_REPORT.md`. Follow the [getting-started guide](docs/notes/getting-started.md) to prepare your first work order.

**Already using SE Harness?** Use the released version pinned by that repository. Updating the Python package leaves its managed files unchanged; follow the [repository upgrade procedure](docs/notes/harness-installation-and-upgrades.md).

## How it works today

1. **Define the change.** Record the desired outcome, requirements, design, and verification approach.
2. **Approve the work.** A human approves a work order: a bounded plan for what may change.
3. **Implement and check.** An agent works within that scope and retains evidence from the required checks.
4. **Verify, then release.** An assurance owner judges the evidence for the exact candidate commit. A release owner makes a separate release decision.

Independent assurance requires separation between implementation and verification. Automated checks support the human decisions.

## A Virtual Twin of your Software

Our vision is an **authoritative model of the intended software** connecting requirements, behavior, architecture, and evidence. **Code is its implementation.**

We are building toward a contract where agents implement approved changes to that model and independent verification provides evidence of conformity. Automatic propagation from model to code remains a vision.

## See the whole change

Verity Plane Explorer shows the connections between requirements, work, evidence, and decisions. This repository uses it to document its own development.

**Lineage**

[![Verity Plane Explorer showing a work order linked to its purpose, requirements, and decision history](docs/images/harness-explorer-lineage.png)](https://mmzen.github.io/se_harness/)

**Virtual Twin**

[![Virtual Twin showing the artifact graph clustered by domain, with connections between engineering records](docs/images/harness-explorer-virtual-twin.png)](https://www.verityplane.ai/?view=graph)

## Go further

- [Understand the model](docs/notes/harness-overview.md)
- [Follow a complete example](docs/notes/harness-lineage-example.md)
- [Look up a command](docs/notes/harnessctl-reference.md)
- [Develop and contribute](docs/notes/developing-se-harness.md)

[Report an issue](https://github.com/mmzen/se_harness/issues) · [Releases](https://github.com/mmzen/se_harness/releases) · [License](LICENSE)
