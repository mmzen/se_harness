# Installing and safely upgrading SE Harness

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is non-authoritative operator guidance. It does not approve repository changes. Follow `ENGINEERING_HARNESS.md`, repository policy, and accountable owner decisions when operating an installed harness.

## Two things are installed

SE Harness has two related but separate installation surfaces:

1. the released Python package and `harnessctl` launcher inside a selected Python environment;
2. the managed and owner-seeded files written into a target repository by `init`, `adopt`, or an explicitly applied upgrade.

Updating the Python package changes the CLI and canonical distribution available in that environment. It does **not** silently rewrite a repository that was initialized or adopted earlier.

The repository-managed surface includes two portable skill cores under
`.agents/skills/`: the read-only `harness-orient` orientation skill and the
explicit-only `harness-operator-brief` communication skill. Each core's
`SKILL.md`, strict `skill-contract.json`, and standard-library helper are
managed files, and a thin Claude Code adapter for `harness-orient` is
installed under `.claude/skills/`. Every file is upgraded through
the same ownership-aware transaction as other managed template content;
installing only the Python package does not add them to an existing repository.

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

Codex discovers the canonical skills directly under `.agents/skills`. Claude
Code discovers thin adapters under `.claude/skills`, which load the matching
canonical core and stop if that binding is invalid. The orientation skill
requires a structured launcher for the exact external released evaluator and
returns its execution receipt inline; it does not install an evaluator or
retain evidence in the target. See
[read-only agent orientation](harness-orient.md) for the complete procedure.

`harness-operator-brief` is an explicit-only, single-agent communication
skill: on an explicit request it produces one decision-ready operator brief
from a bounded supplied source under the managed technical-communication
policy, and it changes no repository path. See
[clear technical communication](technical-communication.md). The earlier
`harness-draft-change`, `harness-execute-work-order`, and
`harness-prepare-assurance` writing skills were retired and are no longer
installed; the retained
[Phase 4 writing-skill integration](agentic-execution-phase4-skills.md) and
[Phase 3 MVP contract](agentic-execution-skills-mvp.md) notes record that
design. The [repository host adapter guide](agentic-execution-host-adapters.md)
explains why the Claude files are discovery-only.

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

This rule also covers every managed `.agents/skills/` core, Codex policy file,
and `.claude/skills/` adapter. If a repository edits a managed skill surface,
the upgrade plan reports it as customized and preserves the bytes. Move
repository-specific instructions outside the managed surface or restore the
exact locked content before reviewing a fresh upgrade plan.

Installing candidate package bytes alone changes nothing in an existing
repository: its installed skills, managed files and lock stay as the lock
records them. A newer managed surface reaches a repository only through a
separately governed release, an exact external evaluator installation of
that release, and an explicit transactional repository upgrade. Until then,
the current installed contract and lock remain authoritative; do not copy
candidate files into place.

The managed consumer workflow follows the same upgrade transaction; there is no separate consumer CI reconciliation command. An unmodified older workflow advances to the newly installed package version. A customized workflow blocks apply: move repository-specific behavior into another workflow, restore or remove the managed destination, review a fresh plan, and retry. GitHub continues running the previously committed workflow until the upgrade changes are reviewed, committed, pushed, and merged.

The managed workflow runs `qualify released-root`. That command derives the expected evaluator version, archive digest, and installed-payload digest from the repository lock, proves the current environment owns those exact bytes, and then performs managed-file and complete-graph checks. A candidate template may carry newer behavior before the installed root adopts it; template availability does not itself change root authority.

The lock compares canonical UTF-8 text hashes so ordinary LF/CRLF checkout representation does not create false customization. This portability rule does not excuse a real content mismatch.

Schema 3 is the floor: a lock whose schema is 1 or 2 is not read by any operation, including `doctor` and `upgrade` (`WO-HUP-012`, on the owner's decision of 2026-08-30). The one diagnostic names the route — remove the stale `.engineering-harness.lock` and re-adopt the repository with `adopt`, whose existing non-overwrite behavior protects customized files. Ordinary mutation requires exact agreement with the schema-3 lock. `capture-verification` writes a canonical normalized evaluator-evidence JSON file beside the ready VREC; `prepare-release` does the same for the ready RLS and requires the locked archive name and SHA-256. Retain each evidence file with its record—editing or removing it invalidates the binding.

### Managed files that leave the managed set are removed on upgrade

A release may retire a managed file entirely, so the new template no longer
names a path the repository lock manages. The upgrade plan classifies such a
path as `remove` when its bytes still match the locked digest: `--apply`
deletes the file inside the same transaction, prunes the directories the
deletion leaves empty, and drops the lock entry. A retired path the owner
edited is reported as `customized` and blocks apply, exactly like an in-set
customization; owner seed content and owner bytes around a managed fragment
block are never deleted. With `--evidence-output`, the `remove` actions are
recorded in the transaction evidence beside the updates.

Repositories that upgraded 0.10.0 to 0.11.0 did so before this rule existed:
the 0.11.0 release retired three skills, and that upgrade left their fifteen
files on disk while the rewritten lock no longer names them, so no later
evaluator can retire them mechanically. Delete these orphans by hand in such
a repository:

- `.agents/skills/harness-draft-change/` (SKILL.md, agents/openai.yaml, scripts/guard.py, skill-contract.json)
- `.agents/skills/harness-execute-work-order/` (SKILL.md, agents/openai.yaml, scripts/check_scope.py, skill-contract.json)
- `.agents/skills/harness-prepare-assurance/` (SKILL.md, agents/openai.yaml, scripts/check_prepare.py, skill-contract.json)
- `.claude/skills/harness-draft-change/SKILL.md`, `.claude/skills/harness-execute-work-order/SKILL.md`, `.claude/skills/harness-prepare-assurance/SKILL.md`

### The managed `.gitattributes` block changes at the first release after 0.7.1

`WO-HBI-005` (repository issue #207) removed from the canonical `.gitattributes` fragment the three `se_harness/governance_migration*` rules that only the SE Harness repository itself could satisfy, and stopped shipping the matching `governance-migration-protocol` hash-bound class. In a repository initialized or adopted with 0.7.1 or earlier, `harnessctl doctor` fails `hash-bound-class-declared` and `hash-bound-attribute-effective` after the first commit for that reason alone; there is no owner-side workaround, because the block between the `se-harness` markers is hash-locked. The `upgrade` plan for the first release that carries the change classifies `.gitattributes` as `update` in `fragment` mode: `--apply` rewrites only the managed block, and every rule the owner keeps outside the markers is preserved. A `template`-region class whose pattern matches no tracked path yet — evidence before the first verification record — is then reported as vacuously declared with `0 tracked paths` rather than failed.

### Release records cut before evaluator evidence existed

A released release record can never be rewritten, so a record cut before
evaluator-evidence enforcement existed can never carry the binding. Under
the evaluator-evidence floor (`WO-LRE-002`, on the owner's decision of
2026-08-30), validation simply does not assess such a record: a released
record carrying neither `evaluator_evidence_path` nor
`evaluator_evidence_sha256` raises nothing, requires no declaration, and
blocks no upgrade. A record carrying exactly one of the two fields is still
an error, and a record carrying both keeps every binding check.

The earlier declaration mechanism — the optional
`legacy_releases_without_evaluator_evidence` array in an authorizing work
order's `[evaluator_upgrade]` packet, the per-record `W024` debt warning,
and the pre-apply upgrade refusal — is retired. A historical work order
that carries the array stays valid; the value is inert data.

## Ownership and safety

- Prefer one explicit virtual environment owner rather than relying on an unknown global launcher.
- Pin an exact package version when reproducibility matters.
- Treat `--apply` as a repository change requiring owner authorization and review.
- Do not interpret a successful install, upgrade, `doctor`, validation, inspection report, or dashboard as product approval or commit-bound verification. In particular, successful `inspect` report production can still describe an invalid graph or unresolved attention.
- Installation does not configure branch protection, permissions, required checks, publishing environments, or deployment systems on an external host.

See the [complete command reference](harnessctl-reference.md) for command actors and side effects, and the [Tier-0 overview](harness-overview.md) for the governance model. When upgrading across the release that withdraws the repository-context scaffold, read the [migration note](harness-migration-repository-context-retirement.md) first.
