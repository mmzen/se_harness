# Installation and upgrades

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Installing the Python package makes a checker available. Updating a repository
is a separate, explicit `harnessctl upgrade --apply` operation.

SE Harness 0.22.0 and plugin 0.2.5 are public. This repository remains on
released evaluator 0.21.0 and the external-resource layout adopted under
WO-HUP-003. That adoption retired 44 selected resource copies. Publication
does not change the selection; adopting 0.22.0 requires separate approved work.
See the [current public observations](../engineering/release-0-22-0/evidence/WO-RLS-036/README.md),
including untested Claude Code and Codex Windows desktop routes.

<a id="minimal-installation-successor-candidate"></a>

## Minimal installation (0.21.0)

The selected wheel holds the entry, procedures, policy and templates outside
the checkout. Default `init` writes exactly `.engineering-harness.toml` and
`.engineering-harness.lock`. It creates no instruction copies, example domain,
glossary, local skills or adoption report. Existing owner files stay untouched.

Run from outside the checkout. `CHECKER` is the absolute Python executable in
the selected environment; `REPO` is the absolute checkout path. PowerShell needs
`&` before a quoted executable. Preview, inspect the two paths, then apply:

```text
"CHECKER" -I -m se_harness init "REPO" --project-name "Project" --dry-run --json
"CHECKER" -I -m se_harness init "REPO" --project-name "Project" --json
"CHECKER" -I -m se_harness resources "REPO" --resource ENGINEERING_HARNESS.md --content --json
```

The lookup returns the selected release, content, paths and byte identities.
Read only the requested instructions. It also works without a plugin and offline
when the exact wheel is already installed. Missing resources require explicit
setup. Source code and a newer plugin are never substitute policy sources.

### Read selected instructions

Run the selected released evaluator from outside the checkout. `CHECKER` and
`REPO` have the meanings given above. To read the compact entry:

```text
"CHECKER" -I -m se_harness resources "REPO" --resource ENGINEERING_HARNESS.md --content --json
```

For a procedure, replace `RESOURCE` with its exact resource ID, for example
`docs/engineering/harness/ARTIFACTS.md`:

```text
"CHECKER" -I -m se_harness resources "REPO" --resource RESOURCE --json
```

Read the returned file path and the heading named by the referring guide.
A resource ID is not a path inside this checkout. Resolve instruction links
relative to the returned resource location. Formal artifacts remain repository
files. Read only the material needed for the selected task. Missing or invalid
resources require explicit setup; do not substitute checkout source templates.

### Optional repository integrations

Add a repeatable `--integration` to `init`, or use `upgrade` on an installed
external-resource repository. Each selected file appears in the plan:

| Selection | Repository output |
| --- | --- |
| `--integration git` | Managed evidence byte-preservation block in `.gitattributes`. |
| `--integration ci` | Editable `.github/workflows/engineering-harness.yml` and the generated-output block in `.gitignore`. |
| `--integration pr` | Editable `.github/PULL_REQUEST_TEMPLATE.md`. |

For example, establish Git evidence attributes before producing hash-bound
evidence. Review the preview and apply the same choice:

```text
"CHECKER" -I -m se_harness upgrade "REPO" --integration git --json
"CHECKER" -I -m se_harness upgrade "REPO" --integration git --apply --json
"CHECKER" -I -m se_harness doctor "REPO" --json
```

The effective rule remains `docs/engineering/**/evidence/*.json text eol=lf`.
An equivalent owner rule is valid. Missing or overriding rules are readiness
findings; checks do not relax hashing. Use `scaffold-domain` and `create-artifact`
for requested formal content, rather than copying the template collection.

### Migrate a repository-copy installation

Use the target evaluator for this explicitly authorized upgrade. Preserve the
prior wheel selected by the current lock as `PRIOR_WHEEL`; the installer reads
it as data and verifies its payload and any recorded archive digest. This is
needed because old seed entries record presence, not stock content hashes.

```text
"CHECKER" -I -m se_harness upgrade "REPO" --external-resources --prior-wheel "PRIOR_WHEEL" --json
```

The plan classifies every tracked leaving file. Recognized managed instructions
are removed. Stock editable seeds are preserved unless named with a repeatable
`--retire-file PATH`. Customized authoring guidance or templates stop migration;
move their owner-specific rules into reviewed owner files first. The installer
does not merge policy or execute the old wheel. It preserves historical records
and existing integrations. Paths outside the checkout and linked destinations
are refused before writes.

Rehearse the replacement entry with the exact target wheel in a disposable
checkout. Review real native startup and post-compaction traces. The existing
[delivery receipt](#review-and-apply-an-upgrade) binds the real target repository,
its prior lock and the complete replacement entry. For external resources,
`entry_sha256` binds the rendered `resources --content` text under `utf8-text-lf-v1`.
Then repeat the reviewed plan with its selected retirements and receipt:

```text
"CHECKER" -I -m se_harness upgrade "REPO" --external-resources --prior-wheel "PRIOR_WHEEL" --retire-file docs/engineering/ARTIFACT_AUTHORING.md --instruction-delivery-evidence "RECEIPT" --apply --json
```

That example retires only the named editable seed. Add every other explicitly
selected seed to both preview and apply. No receipt means no retirement of the
local entry. The existing atomic transaction restores file contents after a
failed write or postcondition. Recheck after interruption before retrying;
successful repeated setup changes nothing.

| Former repository material | External-resource destination |
| --- | --- |
| `ENGINEERING_HARNESS.md` | `resources --resource ENGINEERING_HARNESS.md --content --json` |
| `docs/engineering/harness/*.md` | Same resource ID; read the returned local path and heading. |
| `docs/engineering/ARTIFACT_AUTHORING.md` | Same resource ID; standard checklist comes from the wheel. |
| `docs/engineering/templates/*` | Same resource ID; `create-artifact` consumes it directly. |
| `WORKFLOW.json`, `QUALITY_GATES.json` | Selected evaluator inputs; agents use returned lifecycle results. |
| Formal artifacts and evidence | Remain in the repository with unchanged historical bytes. |

See [session activation](plugin-installation-guide.md#clone-activate-and-resume)
for cloning after startup, repeated work and parallel sessions.

## Existing 0.20.1 installation

The remainder of this guide describes the supported repository-copy layout.
An existing repository keeps that layout until an explicit resource migration.

## What is kept under control

| Files | Treatment |
| --- | --- |
| `ENGINEERING_HARNESS.md`, `docs/engineering/harness/`, machine `WORKFLOW.json` and `QUALITY_GATES.json` | Locked entry, conditional instructions and machine policy. Actual changes fail integrity checks. |
| Marked blocks in `.gitignore` and `.gitattributes` | Only the supplied block is locked. Owner text around it is preserved. |
| `AGENTS.md` and any owner-created `CLAUDE.md` | Repository-owned. The harness installs no entry block in these files. |
| Artifact templates, CI workflow and `.engineering-harness.toml` | Editable supplied files; customized content needs an explicit migration decision. |
| Existing compatibility pointers | Owner files preserved on upgrade; 0.20.0 no longer creates them on a fresh installation. |
| Repository skill copies | Editable supplied files when using repository ownership; disposable when switching to the plugin. |

The installed evaluator owns executable policy. Its selected version must match
both `[harness].tool_version` and the installation record. Editing that setting
does not select a different checker or perform an upgrade.

## Install into a repository

Use an external Python environment containing the selected released package.
`CHECKER` is its absolute Python executable; `REPO` is the absolute repository
path. Replace both placeholders and run from outside the checkout. In PowerShell,
prefix a quoted executable with `&`. The `harnessctl` shorthand elsewhere means
this same absolute executable followed by `-I -m se_harness`:

```text
"CHECKER" -I -m se_harness init "REPO"
"CHECKER" -I -m se_harness doctor "REPO"
```

An existing repository keeps its editable files. The installer inserts the
bounded ignore/attribute fragments and records observations in an adoption
report. It does not overwrite an existing CI workflow or configure GitHub
permissions, branch protection or publishing credentials.

The compact root needs native delivery through a compatible, enabled and trusted
host plugin. A successful installation or doctor check does not prove that the
host injected it. Use the selected release's `docs/engineering/harness/SETUP.md`
procedure. For the external-resource layout, follow [resource lookup](#read-selected-instructions).

The evaluator's executable scripts ship inside its package. No executable
copies are installed under the target's `scripts/` directory.

## Review and apply an upgrade

Select the exact authorized release first. The example below targets 0.20.1;
an existing 0.20.1 repository needs no upgrade merely because 0.21.0 is public.
Install the selected released package in the external environment,
review the read-only plan, apply the authorized changes, then check the result:

```text
"CHECKER" -m pip install "se-harness==0.20.1"
"CHECKER" -I -m se_harness upgrade "REPO"
"CHECKER" -I -m se_harness upgrade "REPO" --apply
"CHECKER" -I -m se_harness doctor "REPO"
```

Installing the package does **not** silently rewrite a repository.

Editable guidance, templates, CI and owner settings are kept by default, including edits
made while an older lock treated them as managed files. To take a supplied
replacement, name that file explicitly:

```text
"CHECKER" -I -m se_harness upgrade "REPO" --replace-file docs/engineering/templates/WORK_ORDER.template.md
"CHECKER" -I -m se_harness upgrade "REPO" --apply --replace-file docs/engineering/templates/WORK_ORDER.template.md
```

Repeat `--replace-file` for each editable file to replace. An intentionally
removed editable file stays removed unless explicitly selected. The upgrade
updates the selected checker version while preserving other owner settings.
Replacing customized machine policy remains a separate repair decision.

Before retiring an old AGENTS.md or CLAUDE.md block, rehearse the exact planned
root and review native startup and post-compaction traces. Pass the resulting
repository-bound receipt with `--instruction-delivery-evidence PATH` on apply.
Missing or stale evidence leaves the old blocks unchanged. Canonical old guides
become compatibility pointers; customized guides require an explicit plan.
Resolve `docs/engineering/harness/UPGRADE.md` with `harnessctl resources REPO --resource docs/engineering/harness/UPGRADE.md --json`, then read `legacy-entry-delivery-evidence` at the returned path.
The installer preserves owner bytes outside the old blocks. An approved separate
owner edit is needed to remove harness prose previously copied into that region.

Use `--evidence-output docs/engineering/<domain>/evidence/upgrade.json` when the
repository needs a retained transaction record. The SE Harness development
repository requires that record for its root upgrade workflow.

Writes stay inside the selected repository. Atomic replacement and bounded
rollback protect against ordinary write failures. A fresh plan is required if
the files changed after planning.

## Which identity checks run

Ordinary writes check the actual imported checker origin and version. They do
not reread the complete installed package, hash the Python binary, require an
unused console launcher or reject an ignored `PYTHONPATH`. A linked external
environment is allowed; importing candidate source as the released checker is
still refused.

Installation, upgrade, release preparation, `doctor` and explicit `identity`
inspection check the full checker payload. Release preparation accepts an index
installation with no receipt for the checker's original wheel. It still checks
the installed payload and the release's required artifacts.

New evaluator evidence uses schema v2 and hashes its validated canonical values.
Equivalent JSON whitespace has the same identity; duplicate fields, changed
required values and a wrong checker still fail. Legacy v1 evidence keeps its
original canonical-byte rule. Published archive hashes remain byte hashes.

There is no registry of every metadata field ending in `_sha256`. The format
that consumes a checksum validates it. Git attributes are assessed by their
effective values, wherever their rule is written.

## Published release and candidate differences

Released 0.20.0 omits the six obsolete guide seeds from fresh installations.
An upgrade preserves existing stock pointers and custom owner text. Current work
resolves `ENGINEERING_HARNESS.md` through `harnessctl resources`, then resolves
the selected guide from the same released wheel. Those older pointers
are navigation aids, not separate policy authorities.

This repository adopted 0.21.0 under WO-HUP-003 after 0.20.1 under WO-HUP-025
and 0.20.0 under WO-HUP-024. The six legacy pointers were removed through
separate cleanup work; the resource migration preserves their absence. Development source
remains 0.21.0; its version alone does not change any repository's selected
evaluator.

## Earlier migrations and retained history

Schema 3 remains the lock floor; schema 4 selects plugin-provided skills. Old
release and verification records retain their recorded meaning. The following
notes describe earlier migrations; they do not restore the retired restrictions
for new operations.

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

The first release after 0.15.0 retires the eight evaluator script copies
that earlier installers placed under repository `scripts/`. A repository initialized by 0.15.0 or earlier
sees eight `remove` actions in its upgrade plan, and none of them is
reinstalled afterwards.

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
