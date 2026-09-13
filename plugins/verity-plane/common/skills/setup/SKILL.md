---
name: setup
description: Create or repair the private SE Harness evaluator environment using an available Python installation and the selected local wheel.
---

# Set up the evaluator

Select Python 3.11 or later with venv and ensurepip. If it is unavailable,
report the missing prerequisite; do not install Python or change host settings.
Use the wheel selected for the repository's released evaluator. Plugin source
does not pin that release. A development wheel is only for disposable testing.

Read [the environment procedure](references/environment.md), then run the
plugin's setup helper. It creates or reuses one private environment, reinstalls
the wheel offline, and runs the actual checker once. Rerun the same command to
repair an interrupted installation.

Report the environment Python and actual checker result. A failed check is a
failed check even if installation succeeded. Setup does not initialize or
upgrade the repository, install the plugin into a host, or grant work authority.
