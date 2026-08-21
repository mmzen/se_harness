# `harnessctl` command reference

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a non-authoritative reference to command syntax, actors, and side
> effects. The standard installation's `docs/engineering/WORKFLOW.md` and
> `WORKFLOW.json` own lifecycle transitions, ordered next actions, gate IDs, and
> decision-right IDs. This reference does not restate or override those rules.

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
| `doctor` | human or agent | read-only | inspect required files, managed hashes, distribution parity, owner seeds, and scripts |
| `preflight` | coding agent or reviewer | read-only | check one work order for start or review readiness and return its reading manifest |
| `focus` | human or agent | read-only | project one selected WO, VREC, or RLS scope and return its canonical handoff |
| `check` | human or agent | read-only | evaluate one selected start, pre-action, or handoff checkpoint and emit canonical schema-2 restitution |
| `transition` | authorized operator | plan is read-only; `--apply` atomically mutates only explicitly selected artifacts | validate and record accountable lifecycle decisions without implicit related-record changes |
| `select-work-order` | managed GitHub CI | read-only | select exactly one standalone work-order declaration from a bounded pull-request event through released package logic |
| `upgrade` | repository owner or explicitly authorized agent | plan is read-only; `--apply` mutates managed content transactionally | update an initialized/adopted repository after separately updating the package |
| `scaffold-domain` | coding agent | writes owner-controlled directories and a seed index; dry-run is read-only | create the canonical organization for one engineering domain |
| `create-artifact` | coding agent | writes one incomplete `draft`; dry-run is read-only | create a formal artifact from its canonical template and path mapping |
| `renumber-artifacts` | repository owner or explicitly authorized agent | plan is read-only; `--apply` transactionally changes structured identities, typed relations, and mapped tracked paths | repair an explicit pre-assurance identifier collision and inventory semantic references for manual review |
| `identity` | CI or advanced contributor | read-only identity report/check | prove released-evaluator, candidate-source, or candidate-package runtime origin and boundary |
| `accept-candidate` | released evaluator CI | writes one derived canonical evidence manifest outside the checkout | run the verifier-owned black-box contract against an exact installed candidate wheel |
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

Inspection reuses the existing validator and Harness Explorer snapshot. It
reports `mode = repository_wide`, no selected artifact, formal validity, ready
decisions, draft definitions, active work, assurance preparation, and existing
repository findings. Human output groups repeated rule instances for
readability; `--json` retains every finding. Inspection output MUST NOT be used
as selected-iteration restitution.

The `assurance_pending` queue contains only an `implemented` work order whose explicit `[assurance]` classification is `required` and which has no direct `ready`, `verified`, or `released` VREC coverage. It suggests non-automatic preparation after one clean candidate commit; it does not select aggregate scope, create a record, or make the assurance decision. Completed legacy work without a classification and work explicitly classified `not_required` are not inferred into this queue.

The temporal reassessment observation `W-HEX-003` is deliberately narrow: it compares dates only for supported declared dependency relations whose source can still be meaningfully reassessed. It does not reopen completed work orders, reinterpret commit-bound verification or release records, or treat derived graph projections as declared dependencies.

For existing lifecycle queues and a closed set of actionable derived warning rules, inspection also reports deterministic suggested next steps. Each suggestion identifies its source, affected artifacts, action class, accountable role, and `automatic = false`. Suggestions contain no executable command and never assert eligibility or authority. Validator findings, informational observations, and unknown rules remain visible without guessed advice.

A successfully produced inspection exits zero even when formal validation failed or attention exists, so use `validate` when gate exit behavior is required. Inspection is repository-local derived evidence: it does not approve, authorize, verify, supersede, release, remediate, or independently govern the repository.

Dashboard defaults to `target/harness-dashboard/`; its generated files are derived evidence, not formal authority. The small `index.html` bootstrap verifies `dashboard-manifest.json`, then loads a summary, compact topology, readiness data, individual artifact details, and explicitly expanded evidence from digest-named static resources. Serve the directory from one HTTP origin, for example with `python -m http.server 8000 --directory target/harness-dashboard`; direct `file://` opening is intentionally rejected because progressive resource loading and integrity checks require an origin. Generation remains local and needs no application server, but publishing or sharing the directory exposes every manifest-declared artifact and evidence body; the command does not scan for secrets or redact repository material. Doctor checks the standard installed contract against `.engineering-harness.lock` and the current distribution.

## Work readiness

```text
harnessctl preflight [TARGET] --work-order WO-... [--phase start|review] [--json]
harnessctl select-work-order --event GITHUB_EVENT_PATH
```

`start` is the default phase. Preflight checks lifecycle eligibility, the governing chain, and the selected work order's explicit `[assurance]` declaration, then displays the classification, rationale, and deciding role with the reading manifest. A selected work order without a valid declaration fails even when completed legacy validation remains compatible. Passing proves structural readiness only; it does not prove comprehension, semantic scope fit, implementation correctness, the truth of the rationale or role claim, assurance, or release.

`select-work-order` is the narrow automation-facing parser used by the managed consumer workflow. It accepts one bounded GitHub event file and emits one exact `WO-...` ID only when the pull-request body contains exactly one standalone `Harness-Work-Order:` field. It does not inspect branches, diffs, commits, or artifact eligibility and grants no work authority.

## Selected-scope workflow execution

The command shapes below are stable interfaces. The candidate standard
[`WORKFLOW.md`](../../templates/repository/standard/docs/engineering/WORKFLOW.md)
defines the procedure, and
[`WORKFLOW.json`](../../templates/repository/standard/docs/engineering/WORKFLOW.json)
is the machine-readable contract loaded by `harnessctl`. Use the workflow rule
selected for the artifact's exact type, state, and direct related records. Do
not derive a new transition or next action from this reference.

```text
harnessctl focus [TARGET] --artifact WO-...|VREC-...|RLS-... \
  [--json] [--include-background] [--result-schema 1|2]
harnessctl check [TARGET] --artifact WO-...|VREC-...|RLS-... \
  --checkpoint start|pre-action|handoff \
  [--procedure PROC-...] [--changed-path PATH ...] [--changes-complete] \
  [--change-manifest PATH] [--json]
harnessctl transition [TARGET] --set ID=STATUS --decision ID=ACTOR \
  [--set ID=STATUS ...] [--decision ID=ACTOR ...] [--reason ID=TEXT ...] \
  [--apply] [--json] [--result-schema 1|2]
```

`focus` projects only the selected artifact's governing chain and direct
lifecycle dependencies. It uses the ordered recommendation registry in
`WORKFLOW.json`. For example, `WFL-WO-READY-VREC` takes precedence over
`WFL-WO-PREPARE-VREC`, so existing ready assurance coverage cannot produce a
duplicate-capture recommendation. Unrelated repository findings remain a
background count; `--include-background` expands categories without making
them selected-scope work.

`check` resolves the first matching rule, its typed `PROC-*` procedure, and its
`QG-*` gates. `pre-action` requires `--procedure`, which must equal the selected
procedure or one complete declared alternative. `--changed-path` may repeat;
`--changes-complete` asserts that the supplied set is complete, including an
empty set. The assertion is evidence, not proof from a trusted Git baseline.
Without it, path-scope predicates are `not_assessable`.

`--change-manifest` is mutually exclusive with both changed-path options. It
must be an in-repository UTF-8 JSON object containing only `schema` with value
`se-harness-change-set-v1`, Boolean `complete`, and ordered array `paths`.
Paths use `/`, exact-file or component-boundary directory-prefix matching, and
reject absolute, traversal, backslash, wildcard, drive, URI, control-character,
reserved-device, duplicate, and case-ambiguous forms.

`check` always emits `se-harness-workflow-result-v2`. Human output contains only
`Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current lifecycle
state`, `Decision required`, `Next`, `Command or response`, and conditional
`Alternatives`. Existing workflow commands default to result schema 1 during
the compatibility window; select `--result-schema 2` for canonical restitution.

`transition` resolves IDs from formal metadata and plans by default. Each
selected ID needs one actor assertion. Rejection needs a non-empty reason; VREC
supersession uses the reason as the exact successor VREC ID. A packet is
assessed as one proposed final graph. `--apply` rechecks every input byte,
stages same-filesystem replacements outside artifact discovery, and rolls back
earlier replacements if a later write fails.

The command records actor text as an assertion, not proof of authority. The
effects and non-effects for each state are defined only by the matching
`WORKFLOW.json` rule. Related artifacts require separate explicit selection,
passing gates, and authority.

Human and JSON output are rendered from the same semantic workflow result.
Schema 2 always identifies exactly one typed next step and derives its command
argument array or response from the selected procedure.

## Safe repository upgrade

```text
harnessctl upgrade [TARGET]
harnessctl upgrade [TARGET] --apply
```

The first form is a read-only plan. `--apply` is an explicit transactional repository mutation. It changes only eligible managed content and stops without a partial managed update when customization or conflict prevents a safe plan. Every repository, including the `se_harness` implementation repository, follows this transaction and uses one exact released evaluator. GitHub discovers the managed workflow beside existing repository-owned workflows, while required-check and workflow-ordering policy remains external. See [installation and safe upgrades](harness-installation-and-upgrades.md).

## Domain and artifact authoring

```text
harnessctl scaffold-domain [TARGET] --domain DOMAIN [--title TITLE] [--dry-run]
harnessctl create-artifact [TARGET] --domain DOMAIN --type TYPE --id ID [--dry-run]
```

Domain slugs, artifact identifiers, type prefixes, templates, and destinations are validated before mutation. `create-artifact` creates only an incomplete `draft`; it does not choose owners, relations, content, approval, or authority. Existing valid flat layouts remain discoverable and are not automatically migrated.

## Explicit artifact renumbering

```text
harnessctl renumber-artifacts [TARGET] \
  --map OLD=NEW [--map OLD=NEW ...] [--json] [--apply]
```

The command requires an ordinary clean Git worktree and a full `HEAD`. Every mapping is explicit, one-to-one, type-compatible, and destination-disjoint; the command does not allocate an identifier, infer a related chain, inspect other refs, or reserve the result. Plan mode is the default and writes nothing. `--apply` changes only selected formal `id` fields, parsed typed relations, and exact mapped path components through a recoverable transaction, then validates the resulting graph and leaves an uncommitted diff.

Free-form artifact bodies, documentation, source, and tests are not rewritten automatically. Human and JSON output instead separate:

- `manual_references`, with the resulting repository path, line, and column for semantic review and manual change or disposition;
- `preserved_evidence_references`, whose captured bytes remain unchanged and should not be rewritten; and
- `unsupported_references`, for binary or non-UTF-8 paths requiring manual inspection.

When manual or unsupported references remain, output sets `manual_action_required = true` and `repository_repair_complete = false` even after the structured transaction succeeds. Any selected identifier referenced by a verification or release record blocks the operation. Eligible selected artifacts are limited to `draft`, `approved`, `in_progress`, or `implemented`; later lifecycle and commit-bound history require accountable disposition rather than renumbering.

## Runtime identity

```text
harnessctl identity --role released-evaluator|candidate-source|candidate-package \
  --expected-version VERSION --expected-root PATH [options]
```

Key role-specific options are `--checkout-root`, `--candidate-commit`, `--evaluator-wheel-sha256`, `--entry-point`, `--require-isolated-python`, and `--require-entry-point`. The command verifies declared runtime origin; it does not select an evaluator or approve a candidate.

## Candidate acceptance

```text
harnessctl accept-candidate \
  --wheel PATH \
  --candidate-commit FULL_COMMIT \
  --candidate-wheel-sha256 SHA256 \
  --verifier-wheel-sha256 SHA256 \
  --output PATH \
  [--checkout-root PATH]
```

`accept-candidate` verifies the caller-selected candidate digest, snapshots those exact wheel bytes, creates a fresh environment, installs the snapshot, runs the published black-box scenario set, rejects checkout import fallback and authority substitution, and emits deterministic JSON only when every required scenario passes. Its output is evidence for human assurance review, never a VREC transition.

## Commit-bound verification preparation

```text
harnessctl capture-verification [TARGET] \
  --id VREC-... \
  --work-order WO-... \
  --verification VER-... \
  --evidence PATH \
  [--owner ROLE] [--domain DOMAIN] [--output PATH] [--json]
```

Repeat `--work-order`, `--verification`, and `--evidence` for an aggregate candidate. Every selected work order must be exactly `implemented`, the selected verification contracts must equal their declared union, and evidence must cover each work order. The command requires a clean Git worktree, derives the full `HEAD` object identity, generates the deterministic Explorer bundle, stores the SHA-256 of its recursively binding `dashboard-manifest.json` as `artifact_snapshot_sha256`, and writes only `status = "ready"`. It records `prepared_at` and `prepared_by`, never `verified_at` or `verified_by`.

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
  [--tag TAG] [--domain DOMAIN] [--output PATH] [--json]
```

Repeat `--verification-record` and `--work-order` for aggregate releases. Every included VREC must be exactly `verified`, the selected release contract must gate the work, `releases_work` must equal the included VREC coverage union, and every record must bind the same candidate commit.

The command writes only `status = "ready"` with `prepared_at` and `prepared_by`; it omits `released_at` and `authorized_by` until a separate release transition. It does not commit, push, tag, create a GitHub Release, publish to PyPI, or deploy.

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
