# Getting started with SE Harness

<!-- Target expertise: 3/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. It explains how to run the tool; it grants no approval, verification, or release authority.

## Summary

This page takes you from an empty environment to your first useful command in a repository that SE Harness manages. You install the tool in its own environment outside the repository, confirm the repository is healthy with `doctor`, and then work in one repeating loop: run `check`, do what the result says, run `check` again. Project-specific terms are defined in the [glossary](../../GLOSSARY.md).

## Install the evaluator outside the checkout

The installed copy of SE Harness that judges a repository is called the evaluator. It must run from a Python virtual environment *outside* the repository checkout, at the exact released version the repository pins in `.engineering-harness.toml`. This separation is deliberate: the code in the checkout is the thing being judged, so the judge cannot run from inside it. Running from the checkout is refused.

For a fresh project selecting released 0.19.0, choose an absolute external
environment directory `EVAL`. Run these commands from outside the checkout:

```text
python -m venv "EVAL"
"CHECKER" -m pip install "se-harness==0.19.0"
"CHECKER" -I -m se_harness --version
```

Replace `CHECKER` with the absolute Python executable inside `EVAL`:
`EVAL/Scripts/python.exe` on Windows, or `EVAL/bin/python` on Linux and macOS.
In PowerShell, prefix a quoted executable with `&`. Use the version your repository pins
for an existing project; this example does not authorize an upgrade.

In evaluator examples, `harnessctl` means the absolute Python executable of
the repository's selected released evaluator followed by `-I -m se_harness`.
Run it from outside the checkout. `REPO` is the absolute repository path;
replace placeholders before running a command. Source-development commands
are identified separately and do not govern repository lifecycle state.

The `-I` flag isolates Python from user packages and path variables. If the
repository has no installation yet, follow [Install into a repository](harness-installation-and-upgrades.md#install-into-a-repository)
before its first health check. Plugin installation, evaluator setup and
repository adoption are separate operations; see the [plugin walkthrough](plugin-installation-guide.md).

## First health check: `doctor`

From the external working directory:

```bash
harnessctl doctor REPO
```

`doctor` prints a flat list of PASS or FAIL lines. It answers one question: do the installed managed files match what the tool expects? A clean `doctor` means the harness itself is healthy. It says nothing about your work; that is the next command's job.

## The one-change loop: `check`

`check` reads the repository and answers: what state is the selected work in, and what is the next step? Run it with no artifact and it picks the single work order that is in progress:

```bash
harnessctl check REPO
```

The result always ends with one next step: a command to run, or a decision that is due and the person who owns it. The loop is:

1. Run `check`.
2. Do exactly what the result says.
3. Run `check` again.

When the result is blocked, it names what refused and the one retry. Fix the cause in the repository, never in the result. When the result asks for a decision you do not own, stop and hand off. This loop is the whole day-to-day interface; the other commands exist for installation, inspection, and record keeping.

## Prepare and verify a record in one commit

When a work order is implemented, a verification record is prepared for it and a human decides whether it becomes verified. These two steps do not need two commits. `capture-verification` writes the record file; `transition --apply` accepts that file while it is still untracked; and neither the record nor the decision contains the hash of its own commit. After capture, the human reviews the ready record and makes the verification decision. Only then may the agent apply that recorded decision and commit both results together as one governance commit. The one rule to remember is that a record binds an earlier, already-existing commit, so it always lands in a commit *after* the work it describes.

## Where to go next

- [Glossary](../../GLOSSARY.md) for every project-specific term on this page.
- [Tier-0 overview](harness-overview.md) for what the harness governs and why.
- [`harnessctl check` explained](harnessctl-check.md) for what `check` evaluates at each checkpoint.
- [Installation and safe upgrades](harness-installation-and-upgrades.md) for the complete installation and upgrade procedure.
