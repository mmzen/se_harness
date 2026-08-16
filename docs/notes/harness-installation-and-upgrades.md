# Installing and safely upgrading SE Harness

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. It does not approve repository changes. Follow `ENGINEERING_HARNESS.md`, repository policy, and accountable owner decisions when operating an installed harness.

## Two things are installed

SE Harness has two related but separate installation surfaces:

1. the released Python package and `harnessctl` launcher inside a selected Python environment;
2. the managed and owner-seeded files written into a target repository by `init`, `adopt`, or an explicitly applied upgrade.

Updating the Python package changes the CLI and canonical distribution available in that environment. It does **not** silently rewrite a repository that was initialized or adopted earlier.

## Windows PowerShell

SE Harness requires Python 3.11 or later. From the directory where you want to own the tool environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install se-harness
harnessctl --version
```

For an exact released version:

```powershell
python -m pip install "se-harness==0.4.0"
```

Activation adds `.venv\Scripts` to command discovery for the current shell. The launcher remains `.venv\Scripts\harnessctl.exe`; activation does not move it. Without activation:

```powershell
.\.venv\Scripts\harnessctl.exe --version
```

If the Python launcher reports that a requested runtime is absent, install an available Python 3.11-or-later runtime first. Do not assume a version-specific alias exists merely because `python` is installed.

## Linux and macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install se-harness
harnessctl --version
```

The launcher is `.venv/bin/harnessctl` and can be invoked directly:

```bash
.venv/bin/harnessctl --version
```

On every platform, the selected interpreter can invoke the package without relying on launcher discovery:

```powershell
python -m se_harness --version
```

## Initialize or adopt a repository

Choose one operation:

```powershell
harnessctl init C:\path\to\new-repository --project-name my-project
harnessctl adopt C:\path\to\existing-repository --project-name my-project
```

- `init` expects an absent or empty target.
- `adopt` preserves ordinary existing content, inserts bounded managed fragments where supported, and writes `docs/engineering/ADOPTION_REPORT.md` with observations.
- `--dry-run` resolves and reports the complete plan without writing.
- Neither operation invents approved product facts. Curate `docs/engineering/REPOSITORY_CONTEXT.md` and establish the first formal chain through accountable review.

After installation:

```powershell
harnessctl doctor C:\path\to\repository
harnessctl validate C:\path\to\repository
harnessctl inspect C:\path\to\repository
harnessctl dashboard C:\path\to\repository
```

## Upgrade an existing installation

First upgrade the package in the environment selected to operate the repository:

```powershell
python -m pip install --upgrade se-harness
```

Then inspect the repository upgrade as a read-only plan:

```powershell
harnessctl upgrade C:\path\to\repository
```

Review that plan. The `--apply` form is an explicitly owner-authorized transactional mutation. Only after an accountable owner authorizes it, apply the plan and recheck integrity:

```powershell
harnessctl upgrade C:\path\to\repository --apply
harnessctl doctor C:\path\to\repository
```

The apply operation is transactional: customized, missing, conflicting, or ambiguous managed content blocks the operation without a partial managed-file update. Owner-controlled content and managed fragments outside their bounded markers are preserved.

Schema-2 locks compare canonical UTF-8 text hashes so ordinary LF/CRLF checkout representation does not create false customization. This portability rule does not excuse a real content mismatch.

## Ownership and safety

- Prefer one explicit virtual environment owner rather than relying on an unknown global launcher.
- Pin an exact package version when reproducibility matters.
- Treat `--apply` as a repository change requiring owner authorization and review.
- Do not interpret a successful install, upgrade, `doctor`, validation, inspection report, or dashboard as product approval or commit-bound verification. In particular, successful `inspect` report production can still describe an invalid graph or unresolved attention.
- Installation does not configure branch protection, permissions, required checks, publishing environments, or deployment systems on an external host.

See the [complete command reference](harnessctl-reference.md) for command actors and side effects, and the [Tier-0 overview](harness-overview.md) for the governance model.
