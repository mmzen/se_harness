---
name: setup
description: Prepare or repair the SE Harness checker, connect a project to plugin skills, or carry out a requested harness upgrade using the existing tools.
---

# Set up a project

Select Python 3.11 or later with venv and ensurepip. If it is unavailable,
report the missing prerequisite; do not install Python or change host settings.
Use the wheel selected for the repository's released evaluator. Plugin source
does not pin that release. A development wheel is only for disposable testing.

Use the target and action already requested; ask only for a missing choice.

- For checker setup or repair, follow [the environment procedure](references/environment.md).
- To initialize a project or switch it to plugin skills, follow [project connection](references/repository.md).
- For a requested version upgrade or a mismatched checker, follow [maintenance](references/maintenance.md).

The helper reuses one private environment and reports the actual checker result.
A plugin update alone does not upgrade any project. Replace the named disposable
skill copies through the existing installer; preserve unrelated owner files.

Report what changed, the selected checker/version and its final check result.
Follow the project's installed instructions for governed work and retain existing
authorization for the requested action. These instructions install no host plugin
and grant no assurance or release decision.
