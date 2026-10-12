---
name: setup
description: Prepare or repair the SE Harness checker, connect a project to plugin skills, or carry out a requested harness upgrade using the existing tools.
---

# Set up a project

Use the selected target and requested action. Read only its route:

| Target | Read |
| --- | --- |
| Explicit hosted sandbox or test copy | [Hosted selection](references/hosted-context.md) |
| Clone, select, repair or upgrade a checkout | [Checkout setup](references/checkout.md) |

Select Python 3.11 or later with venv and ensurepip. If unavailable, report the
missing prerequisite; do not install Python or change host settings. Use the
repository's selected released evaluator. Plugin source does not pin its release.
A development wheel is only for disposable testing. Ask only for missing choices.
