# Installing and safely upgrading SE Harness

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. It does not approve repository changes. Follow `ENGINEERING_HARNESS.md`, repository policy, and accountable owner decisions when operating an installed harness.

## Two things are installed

SE Harness has two related but separate installation surfaces:

1. the released Python package and `harnessctl` launcher inside a selected Python environment;
2. the managed and owner-seeded files written into a target repository by `init`, `adopt`, or an explicitly applied upgrade.

Updating the Python package changes the CLI and canonical distribution available in that environment. It does **not** silently rewrite a repository that was initialized or adopted earlier.

The repository-managed surface includes the portable `harness-orient` core at
`.agents/skills/harness-orient/`. Its `SKILL.md`, strict
`skill-contract.json`, and standard-library runner are managed files. They are
installed and upgraded through the same ownership-aware transaction as other
managed template content; installing only the Python package does not add them
to an existing repository.

After initial installation, mutating commands use the repository's `.engineering-harness.lock` as the expected released-evaluator identity. Run them from a dedicated environment outside the target checkout. The guard rejects a source checkout, editable install, wrong payload or archive, unresolved or foreign launcher, enabled user site, inherited `PYTHONPATH`, and other ambiguous origins before it creates a directory, temporary file, or formal record. Read-only planning and inspection remain available when mutation authority is unavailable.

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
python -m pip install "se-harness==0.4.1"
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
- Neither operation invents approved product facts. Record build, test, verification, ownership, and boundary facts in the owner-controlled region of `AGENTS.md`, and establish the first formal chain through accountable review.

For GitHub repositories, both operations install one dedicated managed `.github/workflows/engineering-harness.yml`. GitHub automatically discovers it beside zero or more existing workflows; SE Harness does not edit unrelated workflow files. Workflow presence does not configure branch protection, required checks, deployment ordering, or any other hosting policy.

If that exact destination already contains unknown content, installation reports a conflict and writes nothing. Preserve repository-specific CI under another workflow filename, then rerun installation. GitHub does not assign execution meaning to the filename itself.

After installation:

```powershell
harnessctl doctor C:\path\to\repository
harnessctl validate C:\path\to\repository
harnessctl inspect C:\path\to\repository
harnessctl dashboard C:\path\to\repository
```

Explorer is a progressive static bundle. Serve `target/harness-dashboard/` over HTTP rather than opening `index.html` directly; for example, run `python -m http.server 8000 --directory target/harness-dashboard` from the repository and open `http://localhost:8000/`.

Supported agents can load `.agents/skills/harness-orient/SKILL.md` for a
read-only orientation. The skill requires a structured launcher for the exact
external released evaluator and returns its execution receipt inline; it does
not install an evaluator or retain evidence in the target. See
[read-only agent orientation](harness-orient.md) for the complete procedure.

## Upgrade an existing installation

The package-only shorthand remains useful for obtaining read-only planning and inspection behavior:

```powershell
python -m pip install --upgrade se-harness
```

That index install alone is not archive proof for an applied repository upgrade. Before apply, acquire the already-published target wheel into a directory outside the repository, independently check the digest selected by the release process, and install those exact local bytes into the external evaluator environment. A direct wheel install preserves the archive identity needed by upgrade apply and release preparation:

```powershell
python -m pip download --only-binary=:all: --no-deps "se-harness==VERSION" --dest C:\path\to\download
Get-FileHash C:\path\to\download\se_harness-VERSION-py3-none-any.whl -Algorithm SHA256
python -m pip install --upgrade C:\path\to\download\se_harness-VERSION-py3-none-any.whl
```

Use the equivalent `sha256sum` and path syntax on Linux or macOS. Do not treat a version string, an unverified index install, or candidate wheel as the selected archive proof.

Then inspect the repository upgrade as a read-only plan:

```powershell
harnessctl upgrade C:\path\to\repository
```

Review that plan. The `--apply` form is an explicitly owner-authorized transactional mutation. Only after an accountable owner authorizes it, apply the plan and recheck integrity:

```powershell
harnessctl upgrade C:\path\to\repository --apply
harnessctl doctor C:\path\to\repository
```

The command above remains sufficient for same-identity managed repair. If apply would change evaluator identity, it stops unless a separate approved or in-progress evaluator-upgrade work order binds the exact prior lock and immutable target identity. After reviewing the plan, the authorized transition uses a work-order-keyed evidence destination:

```powershell
harnessctl upgrade C:\path\to\repository --apply --work-order WO-... --evidence-output docs/engineering/DOMAIN/evidence/WO-...-evaluator-upgrade.json
```

Product implementation or release authorization does not authorize this later root adoption. See the [bounded evaluator recovery runbook](evaluator-recovery-runbook.md) for the maintainer-only deadlock procedure and disposable rehearsal.

The apply operation is transactional: customized, conflicting, or ambiguous managed content blocks the operation without a partial managed-file update. A missing unmodified managed file may be restored when the reviewed plan classifies it as `add`. Owner-controlled content and managed fragments outside their bounded markers are preserved.

This rule also covers `.agents/skills/harness-orient/`. If a repository edits a
managed skill file, the upgrade plan reports it as customized and preserves the
bytes. Move repository-specific instructions outside the managed core or
restore the exact locked content before reviewing a fresh upgrade plan.

The managed consumer workflow follows the same upgrade transaction; there is no separate consumer CI reconciliation command. An unmodified older workflow advances to the newly installed package version. A customized workflow blocks apply: move repository-specific behavior into another workflow, restore or remove the managed destination, review a fresh plan, and retry. GitHub continues running the previously committed workflow until the upgrade changes are reviewed, committed, pushed, and merged.

After a future upgrade installs a release containing the role-specific qualification interface, the managed workflow runs `qualify released-root`. That command derives the expected evaluator version, archive digest, and installed-payload digest from the repository lock, proves the current environment owns those exact bytes, and then performs managed-file and complete-graph checks. The candidate template can contain this behavior before the current root adopts it; template availability does not itself change root authority.

Schema-2 locks compare canonical UTF-8 text hashes so ordinary LF/CRLF checkout representation does not create false customization. This portability rule does not excuse a real content mismatch.

Schema-1 and schema-2 roots remain inspectable but cannot run ordinary mutations under the enforcing release. Their single transition path is the reviewed `upgrade --apply` above, from an already-published target evaluator. Once schema 3 is installed, ordinary mutation requires exact agreement with the lock. `capture-verification` writes a canonical normalized evaluator-evidence JSON file beside the ready VREC; `prepare-release` does the same for the ready RLS and requires the locked archive name and SHA-256. Retain each evidence file with its record—editing or removing it invalidates the binding.

### Release records cut before evaluator evidence existed

Schema 3 requires an evaluator-evidence binding on every `ready` and `released` release record, and a released record can never be rewritten to add one. A repository that released under an earlier schema therefore holds records that can never satisfy the enforcing rule. Those records are declared, not rewritten.

The declaration is one optional array in the authorizing work order's own `[evaluator_upgrade]` packet, listing the pre-enforcement records by identifier:

```toml
[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "..."
target_version = "VERSION"
target_payload_sha256 = "..."
target_archive_name = "se_harness-VERSION-py3-none-any.whl"
target_archive_sha256 = "..."
publication = "immutable"
authorized_by = "repository-owner"
legacy_releases_without_evaluator_evidence = ["RLS-XYZ-001"]
```

A declaration is honoured only for a record that is `released`, carries neither binding field, and was released strictly before the declaring work order was approved. It can never reach a release cut after that approval, and a partially bound record is never exempt. An unresolvable member is an error on the declaring work order, so a typo fails closed rather than widening the exemption.

A declaration is a permanent historical fact. Once an authority-granting work order declares a record, later upgrades need no fresh declaration: the same packet keeps answering for those records. Add the array only to the work order that first crosses into enforcement, and only for records that already existed.

Each accepted exemption raises one `W024` maintenance warning naming the record and its declarer, so the outstanding binding stays visible. Validation passes; the warning is the debt.

`upgrade --apply` refuses an evaluator identity transition before writing anything when the repository holds a released record with no binding and no declaration, and names the records and the packet field to declare them in. Read-only `harnessctl upgrade` prints the same list as a planning notice and still exits successfully, so the declaration can be prepared before the apply.

This repository's own pre-enforcement releases predate the mechanism and stay in a frozen, closed compatibility set rather than a declaration.

## Ownership and safety

- Prefer one explicit virtual environment owner rather than relying on an unknown global launcher.
- Pin an exact package version when reproducibility matters.
- Treat `--apply` as a repository change requiring owner authorization and review.
- Do not interpret a successful install, upgrade, `doctor`, validation, inspection report, or dashboard as product approval or commit-bound verification. In particular, successful `inspect` report production can still describe an invalid graph or unresolved attention.
- Installation does not configure branch protection, permissions, required checks, publishing environments, or deployment systems on an external host.

See the [complete command reference](harnessctl-reference.md) for command actors and side effects, and the [Tier-0 overview](harness-overview.md) for the governance model. When upgrading across the release that withdraws the repository-context scaffold, read the [migration note](harness-migration-repository-context-retirement.md) first.
