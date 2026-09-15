# Installation and upgrades

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Installing the Python package makes a checker available. Updating a repository
is a separate, explicit `harnessctl upgrade --apply` operation.

This guide describes behavior released in 0.18.0 from WO-KIS-003. An existing
repository keeps its installed evaluator and lock until an explicit upgrade.
The SE Harness development repository adopted released 0.18.0 under WO-HUP-019.

## What is kept under control

| Files | Treatment |
| --- | --- |
| `ENGINEERING_HARNESS.md`, machine `WORKFLOW.json` and `QUALITY_GATES.json` | Locked machine policy and router. Actual changes fail integrity checks. |
| Marked blocks in `AGENTS.md`, `CLAUDE.md`, `.gitignore` and `.gitattributes` | Only the supplied block is locked. Owner text around it is preserved. |
| Human policy guides, artifact templates, CI workflow and `.engineering-harness.toml` | Editable files, supplied on first installation and kept on later upgrades. |
| Repository skill copies | Editable supplied files when using repository ownership; disposable when switching to the plugin. |

The installed evaluator owns executable policy. Its selected version must match
both `[harness].tool_version` and the installation record. Editing that setting
does not select a different checker or perform an upgrade.

## Install into a repository

Use an external Python environment containing the selected released package:

```text
python -m se_harness init /path/to/repository
python -m se_harness doctor /path/to/repository
```

An existing repository keeps its editable files. The installer inserts the
bounded instruction/ignore fragments and records observations in an adoption
report. It does not overwrite an existing CI workflow or configure GitHub
permissions, branch protection or publishing credentials.

The evaluator's executable scripts ship inside its package. No executable
copies are installed under the target's `scripts/` directory.

## Review and apply an upgrade

Install the new released package in the external environment, review the
read-only plan, apply it, then check the result:

```text
python -m pip install --upgrade se-harness
python -m se_harness upgrade /path/to/repository
python -m se_harness upgrade /path/to/repository --apply
python -m se_harness doctor /path/to/repository
```

Installing the package does **not** silently rewrite a repository.

Guidance, templates, CI and owner settings are kept by default, including edits
made while an older lock treated them as managed files. To take a supplied
replacement, name that file explicitly:

```text
python -m se_harness upgrade /path/to/repository --replace-file docs/engineering/WORKFLOW.md
python -m se_harness upgrade /path/to/repository --apply --replace-file docs/engineering/WORKFLOW.md
```

Repeat `--replace-file` for each editable file to replace. An intentionally
removed editable file stays removed unless explicitly selected. The upgrade
updates the selected checker version while preserving other owner settings.
Replacing customized machine policy remains a separate repair decision.

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

The first release after 0.15.0 retires the eight `scripts/` paths named under
"Two things are installed". A repository initialized by 0.15.0 or earlier
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
