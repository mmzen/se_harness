# `harnessctl` command reference

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a non-authoritative reference to the current repository CLI. Managed workflow and decision-rights policy remain authoritative. A command's ability to write a draft or `ready` record never grants approval, verification, release, publication, or deployment authority.

## Invocation

After activating the environment that owns SE Harness:

```text
harnessctl COMMAND [arguments]
```

The equivalent interpreter-scoped form is `python -m se_harness COMMAND [arguments]`. Run `harnessctl COMMAND --help` for the exact parser help installed in the selected environment.

## Command inventory

| Command | Principal actor | State effect | Intended use |
| --- | --- | --- | --- |
| `init` | repository owner or authorized agent | writes a complete standard harness | initialize an absent or empty repository |
| `adopt` | repository owner or authorized agent | preserves existing content and writes the harness plus adoption observations | introduce the harness into an existing repository |
| `validate` | human or agent | read-only | validate formal metadata, typed relations, lifecycle, coverage, evidence paths, and provenance |
| `inspect` | human or agent | read-only | summarize existing validation, lifecycle queues, Explorer findings, and bounded next-step guidance without acting as a gate |
| `dashboard` | human or agent | writes derived output only | generate the read-only Harness Explorer |
| `doctor` | human or agent | read-only | inspect required files, managed hashes, distribution parity, owner seeds, scripts, and configured self-hosting controls |
| `preflight` | coding agent or reviewer | read-only | check one work order for start or review readiness and return its reading manifest |
| `upgrade` | repository owner or explicitly authorized agent | plan is read-only; `--apply` mutates managed content transactionally | update an initialized/adopted repository after separately updating the package |
| `reconcile-governor` | authorized self-hosting maintainer using the current released governor | plan is read-only; `--apply` performs one recoverable descriptor/configuration/workflow/lock transaction | adopt an exact published governor without executing target code or losing repository policy |
| `scaffold-domain` | coding agent | writes owner-controlled directories and a seed index; dry-run is read-only | create the canonical organization for one engineering domain |
| `create-artifact` | coding agent | writes one incomplete `draft`; dry-run is read-only | create a formal artifact from its canonical template and path mapping |
| `identity` | CI or advanced contributor | read-only identity report/check | prove governor, candidate-source, or candidate-package runtime origin and boundary |
| `accept-candidate` | released governor CI | writes one derived canonical evidence manifest outside the checkout | run the verifier-owned black-box contract against an exact installed candidate wheel |
| `capture-verification` | coding agent after an authorized clean candidate | writes one `ready` VREC | bind selected work, verification contracts, evidence, snapshot, and exact clean `HEAD` |
| `prepare-release` | coding agent after verification and release-preparation authority | writes one `ready` RLS | bind release policy, eligible VRECs, exact work coverage, version, and the same candidate commit |

## Repository setup and inspection

```text
harnessctl init [TARGET] [--project-name NAME] [--dry-run]
harnessctl adopt [TARGET] [--project-name NAME] [--dry-run]
harnessctl validate [TARGET] [--json]
harnessctl inspect [TARGET] [--json]
harnessctl dashboard [TARGET] [--output PATH]
harnessctl doctor [TARGET]
```

`TARGET` defaults to the current directory. Installation resolves the complete destination plan before writing and fails closed on ordinary conflicts, unsafe traversal, and repository escape. Adoption observations are not approved product artifacts.

Validation reports deterministic errors and warnings but does not edit artifacts. Each finding names its assessment plane: `structure`, `governance`, configured `policy`, or non-blocking `maintenance`. Planes explain the finding source; they do not change severity, pass/fail behavior, or create a score.

Inspection reuses the existing validator and Harness Explorer snapshot. It reports formal validity, ready decisions, draft definitions, approved or in-progress work, implemented work explicitly awaiting commit-bound assurance preparation, and the existing validator and Explorer findings. Human output groups repeated rule instances for readability; `--json` retains every finding.

The `assurance_pending` queue contains only an `implemented` work order whose explicit `[assurance]` classification is `required` and which has no direct `ready`, `verified`, or `released` VREC coverage. It suggests non-automatic preparation after one clean candidate commit; it does not select aggregate scope, create a record, or make the assurance decision. Completed legacy work without a classification and work explicitly classified `not_required` are not inferred into this queue.

The temporal reassessment observation `W-HEX-003` is deliberately narrow: it compares dates only for supported declared dependency relations whose source can still be meaningfully reassessed. It does not reopen completed work orders, reinterpret commit-bound verification or release records, or treat derived graph projections as declared dependencies.

For existing lifecycle queues and a closed set of actionable derived warning rules, inspection also reports deterministic suggested next steps. Each suggestion identifies its source, affected artifacts, action class, accountable role, and `automatic = false`. Suggestions contain no executable command and never assert eligibility or authority. Validator findings, informational observations, and unknown rules remain visible without guessed advice.

A successfully produced inspection exits zero even when formal validation failed or attention exists, so use `validate` when gate exit behavior is required. Inspection is repository-local derived evidence: it does not approve, authorize, verify, supersede, release, remediate, or independently govern the repository.

Dashboard defaults to `target/harness-dashboard/`; its generated files are derived evidence, not formal authority. The small `index.html` bootstrap verifies `dashboard-manifest.json`, then loads a summary, compact topology, readiness data, individual artifact details, and explicitly expanded evidence from digest-named static resources. Serve the directory from one HTTP origin, for example with `python -m http.server 8000 --directory target/harness-dashboard`; direct `file://` opening is intentionally rejected because progressive resource loading and integrity checks require an origin. Generation remains local and needs no application server, but publishing or sharing the directory exposes every manifest-declared artifact and evidence body; the command does not scan for secrets or redact repository material. Doctor checks the installed contract against `.engineering-harness.lock` and the current distribution while respecting documented repository-specific self-hosting controls.

## Work readiness

```text
harnessctl preflight [TARGET] --work-order WO-... [--phase start|review] [--json]
```

`start` is the default phase. Preflight checks lifecycle eligibility, the governing chain, and the selected work order's explicit `[assurance]` declaration, then displays the classification, rationale, and deciding role with the reading manifest. A selected work order without a valid declaration fails even when completed legacy validation remains compatible. Passing proves structural readiness only; it does not prove comprehension, semantic scope fit, implementation correctness, the truth of the rationale or role claim, assurance, or release.

## Safe repository upgrade

```text
harnessctl upgrade [TARGET]
harnessctl upgrade [TARGET] --apply
```

The first form is a read-only plan. `--apply` is an explicit transactional repository mutation. It changes only eligible managed content and stops without a partial managed update when customization or conflict prevents a safe plan. See [installation and safe upgrades](harness-installation-and-upgrades.md).

## Domain and artifact authoring

```text
harnessctl scaffold-domain [TARGET] --domain DOMAIN [--title TITLE] [--dry-run]
harnessctl create-artifact [TARGET] --domain DOMAIN --type TYPE --id ID [--dry-run]
```

Domain slugs, artifact identifiers, type prefixes, templates, and destinations are validated before mutation. `create-artifact` creates only an incomplete `draft`; it does not choose owners, relations, content, approval, or authority. Existing valid flat layouts remain discoverable and are not automatically migrated.

## Self-hosting runtime identity

```text
harnessctl identity --role governor|candidate-source|candidate-package \
  --expected-version VERSION --expected-root PATH [options]
```

Key role-specific options are `--checkout-root`, `--candidate-commit`, `--governor-wheel-sha256`, `--entry-point`, `--require-isolated-python`, and `--require-entry-point`. This command is primarily for the implementation repository's self-hosting CI. It verifies declared runtime origin; it does not promote a governor or approve a candidate.

## Self-hosting governor reconciliation and candidate acceptance

These commands apply to `se_harness` development, not ordinary consumer repositories:

```text
harnessctl reconcile-governor [TARGET] \
  --to VERSION \
  --target-commit FULL_COMMIT \
  --target-release-record RLS-... \
  --target-sha256 SHA256 \
  --work-order WO-... \
  [--target-wheel PATH] [--set DOTTED.PATH=TOML_VALUE] [--apply]

harnessctl accept-candidate \
  --wheel PATH \
  --candidate-commit FULL_COMMIT \
  --candidate-wheel-sha256 SHA256 \
  --governor-wheel-sha256 SHA256 \
  --output PATH \
  [--checkout-root PATH]
```

`reconcile-governor` must execute from the currently selected released governor outside the implementation checkout. It verifies the immutable target wheel, reads its migration and workflow contracts as data, preserves declared repository policy, and refuses unsupported schema jumps, missing decisions, consumer-workflow substitution, or undocumented workflow customization. Plan is the default. Apply changes only the governor descriptor, protected TOML, self-hosting workflow, transaction metadata, and matching lock state. The selected work order supplies authority; the command does not approve or publish the target.

`accept-candidate` verifies the caller-selected candidate digest, snapshots those exact wheel bytes, creates a fresh environment, installs the snapshot, runs the published black-box scenario set, rejects checkout import fallback and authority substitution, and emits deterministic JSON only when every required scenario passes. Its output is evidence for human assurance review, never a VREC transition.

## Commit-bound verification preparation

```text
harnessctl capture-verification [TARGET] \
  --id VREC-... \
  --work-order WO-... \
  --verification VER-... \
  --evidence PATH \
  [--owner ROLE] [--domain DOMAIN] [--output PATH]
```

Repeat `--work-order`, `--verification`, and `--evidence` for an aggregate candidate. The selected verification contracts must equal the union declared by the selected work orders, and evidence must cover each work order. The command requires a clean Git worktree, derives the full `HEAD` object identity, generates the deterministic Explorer bundle, stores the SHA-256 of its recursively binding `dashboard-manifest.json` as `artifact_snapshot_sha256`, and writes only `status = "ready"`.

An accountable assurance owner reviews the retained evidence and separately decides whether to transition the VREC to `verified`. The record lives in later governance history and continues to bind the earlier candidate commit C.

## Commit-bound release preparation

```text
harnessctl prepare-release [TARGET] \
  --id RLS-... \
  --release-contract REL-... \
  --verification-record VREC-... \
  --work-order WO-... \
  --version VERSION \
  --authorized-by ROLE \
  [--tag TAG] [--domain DOMAIN] [--output PATH]
```

Repeat `--verification-record` and `--work-order` for aggregate releases. The selected release contract must gate the work, `releases_work` must equal the included VREC coverage union, included records must be eligible, and every record must bind the same candidate commit.

The command writes only `status = "ready"`. It does not transition the record to `released`, commit, push, tag, create a GitHub Release, publish to PyPI, deploy, or promote the self-hosting governor.

## Authority summary

| Result | Meaning |
| --- | --- |
| successful check | derived observation about the inspected repository or runtime |
| generated dashboard | derived navigation and anomaly evidence |
| generated `draft` | incomplete authoring starting point |
| generated `ready` VREC/RLS | structurally prepared proposal awaiting accountable review |
| human transition to `verified` | assurance decision about the exact candidate and evidence |
| human transition to `released` | release authorization for that same candidate |

For lifecycle timing, see [operational phasing](harness-operational-phasing.md). For complete examples, see [practical SE Harness examples](harness-lineage-example.md).
