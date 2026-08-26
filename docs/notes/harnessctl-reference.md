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
| `focus` | human or agent | read-only | project one selected WO, VREC, or RLS scope and return its authoritative structured handoff |
| `check` | human or agent | read-only | evaluate one selected start, pre-action, or handoff checkpoint and emit the authoritative schema-2 result |
| `transition` | authorized operator | plan is read-only; `--apply` atomically mutates only explicitly selected artifacts | validate and record accountable lifecycle decisions without implicit related-record changes |
| `select-work-order` | managed GitHub CI | read-only | select exactly one standalone work-order declaration from a bounded pull-request event through released package logic |
| `upgrade` | repository owner or explicitly authorized agent | plan is read-only; `--apply` mutates managed content transactionally | update an initialized/adopted repository after separately updating the package |
| `rehearse-recovery` | maintainer or CI rehearsal | writes only a fresh disposable directory outside the operational repository | prove bounded evaluator recovery and rollback without credentials, network, or external action |
| `rehearse-migration` | maintainer or candidate CI | writes only a fresh disposable directory outside the operational repository | prove the complete predecessor-to-successor handover without changing root authority or performing a release |
| `scaffold-domain` | coding agent | writes owner-controlled directories and a seed index; dry-run is read-only | create the canonical organization for one engineering domain |
| `create-artifact` | coding agent | writes one incomplete `draft`; dry-run is read-only | create a formal artifact from its canonical template and path mapping |
| `renumber-artifacts` | repository owner or explicitly authorized agent | plan is read-only; `--apply` transactionally changes structured identities, typed relations, and mapped tracked paths | repair an explicit pre-assurance identifier collision and inventory semantic references for manual review |
| `release-unit` | release owner or coding agent drafting a release contract | read-only | measure a release unit's work-order census from the commit trailers between the previous release tag and a candidate commit, and compare it with a contract (`E-CIP-001`) |
| `identity` | CI or advanced contributor | read-only identity report/check | prove released-evaluator, candidate-source, or candidate-package runtime origin and boundary |
| `qualify` | release CI, maintainer, or released evaluator | read-only except for one exclusive evidence output outside the inspected repository | run one of five fixed evaluator/target qualification roles and emit provenance-bound, non-authoritative evidence |
| `accept-candidate` | released evaluator CI | writes one derived canonical evidence manifest outside the checkout | run the verifier-owned black-box contract against an exact installed candidate wheel |
| `delegated-workflow` | delegated implementation worker under an exact evaluator envelope | `catalog` is read-only; `execute` performs only declared repository effects and lifecycle transitions before returning a Git stop packet; `prepare-vrec` writes one undecided ready VREC | run the closed Phase 4 start, brokered-effect, completion, and assurance-preparation operations without inheriting approval, assurance, Git, or external-action authority |
| `capture-verification` | coding agent after an authorized clean candidate | writes one `ready` VREC plus canonical evaluator evidence | bind selected work, verification contracts, evidence, evaluator identity, snapshot, and exact clean `HEAD` |
| `prepare-release` | coding agent after verification and release-preparation authority | writes one `ready` RLS plus canonical evaluator evidence | bind release policy, eligible VRECs, exact work coverage, released evaluator wheel identity, version, and the same candidate commit |

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
  [--change-manifest PATH] [--pull-request-body PATH] [--json]
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

`check` always emits `se-harness-workflow-result-v2`. That structured result is
authoritative. The deterministic direct human renderer uses `Outcome`, `Done`,
`Not done`, conditional `Blocked by`, `Current lifecycle state`, `Decision
required`, `Next`, `Command or response`, and conditional `Alternatives` in
that order. Exact-format consumers must use this renderer directly rather than
ask a model to transcribe it. `focus` defaults to result schema 2; passing
`--result-schema 1` prints `WEX-ADS-002` on standard error because that
projection is not restitution. `transition`, `capture-verification`, and
`prepare-release` still default to schema 1 during the compatibility window.

When `check` is blocked, `Next` and `Command or response` carry the corrective
form the contract declares for the first failing predicate: a command that
differs from the evaluated one (for example the handoff check with
`--changed-path` and `--changes-complete`), an escalation naming a decision
right, or a response describing the evidence to retain. The evaluated command
is never rendered as its own retry. Every schema-2 result carries
`result_sha256`, the SHA-256 of the canonical human block (UTF-8, LF, no
trailing whitespace); a pull-request body may declare it on one standalone
`Harness-Restitution:` line for CI to recompute. At `handoff`, a work order
whose `ready` verification record binds a commit no longer reachable from
`HEAD` is blocked with `W-ADS-002`; `--pull-request-body` additionally reports
`W-ADS-001` when the work-order trailer ends with a carriage return.

An agent-facing handoff may adapt wording, ordering, headings, and relevant
explanation or omit empty fields. It remains conforming only when it preserves
actual artifact IDs, outcome, observed effects, incomplete work, material
non-effects, blockers, final lifecycle state, the accountable decision,
command argument boundaries or suggested-response meaning, and exactly one
recommended next action. Workflow-declared alternatives remain separate from
that recommendation. Agent prose never becomes lifecycle authority.

`transition` resolves IDs from formal metadata and plans by default. Each
selected ID needs one actor assertion. Rejection needs a non-empty reason; VREC
supersession uses the reason as the exact successor VREC ID. A packet is
assessed as one proposed final graph. `--apply` rechecks every input byte,
proves the locked released-evaluator authority before writing, stages
same-filesystem replacements outside artifact discovery, and rolls back earlier
replacements if a later write fails.

The command records actor text as an assertion, not proof of authority. The
effects and non-effects for each state are defined only by the matching
`WORKFLOW.json` rule. Related artifacts require separate explicit selection,
passing gates, and authority.

Direct human and JSON output are rendered from the same semantic workflow
result. Schema 2 always identifies exactly one typed next step and derives its
command argument array or response from the selected procedure. Adaptive agent
presentation consumes that result; it does not replace or recompute it.

## Safe repository upgrade

```text
harnessctl upgrade [TARGET]
harnessctl upgrade [TARGET] --apply
harnessctl upgrade [TARGET] --apply --work-order WO-... --evidence-output docs/engineering/DOMAIN/evidence/WO-...-evaluator-upgrade.json
```

The first form is a read-only plan. `--apply` is an explicit transactional repository mutation. Same-identity managed repair needs no new lifecycle packet. When the installed target evaluator differs from the standard lock, apply additionally requires a distinct approved or in-progress work order with an exact `[evaluator_upgrade]` packet and a work-order-keyed JSON evidence path. The packet binds the prior lock SHA-256 and exact immutable target archive/payload identity with `scope = "standard-root-only"`; a product release decision cannot substitute for it.

Apply requires the already-published target evaluator installed from exact wheel bytes outside the checkout, changes only eligible managed content, and stops without a partial managed update when identity, authority, customization, or conflict prevents a safe plan. Transition evidence, managed files, and the lock share the recoverable transaction, and successful replay must be a no-op. Every repository, including the `se_harness` implementation repository, follows this transaction and uses one exact released evaluator. GitHub discovers the managed workflow beside existing repository-owned workflows, while required-check and workflow-ordering policy remains external. See [installation and safe upgrades](harness-installation-and-upgrades.md).

## Disposable recovery rehearsal

```text
harnessctl rehearse-recovery OUTPUT --repository REPOSITORY --candidate-commit FULL_COMMIT [--target-version SYNTHETIC_VERSION]
```

The output must be absent or empty and outside the operational repository. The command refuses recognized production publication credential signals, uses no network client, creates only a synthetic local archive and simulated publication, rejects candidate contamination and stale identity, stops synthetic conflicting chains without selection, injects an interrupted root migration, proves exact rollback, restores the normal standard workflows and absence invariants, and writes canonical `rehearsal-report.json`. It grants no real recovery or external-action authority. See the [bounded evaluator recovery runbook](evaluator-recovery-runbook.md).

## Predecessor-to-successor migration rehearsal

```text
harnessctl rehearse-migration OPERATIONAL_ROOT --scenario CANONICAL_JSON --predecessor-python EXTERNAL_PYTHON --successor-python EXTERNAL_PYTHON --output EXTERNAL_DIRECTORY [--json]
```

The command validates the packaged `se-harness-governance-migration-v1` contract and runs its exact nine stages through two isolated external runtimes. The historical scenario pins the public predecessor wheel digest; every scenario binds its fixture, attributed rejection/adoption decisions, adapter/view selection, and closed stage order. The predecessor remains selected until the final simulated adoption stage. Release and publication are plans only, all writes remain disposable, later stages do not run after the first failure, and the canonical result proves source and Git identities unchanged. See [rehearsing an evaluator migration](evaluator-migration-rehearsal.md).

## Domain and artifact authoring

```text
harnessctl scaffold-domain [TARGET] --domain DOMAIN [--title TITLE] [--dry-run]
harnessctl create-artifact [TARGET] --domain DOMAIN --type TYPE --id ID [--dry-run] [--quiet]
```

Domain slugs, artifact identifiers, type prefixes, templates, and destinations are validated before mutation. `create-artifact` creates only an incomplete `draft`; it does not choose owners, relations, content, approval, or authority. After creation it prints the created type's checklist from the installed `docs/engineering/ARTIFACT_AUTHORING.md`; `--quiet` suppresses it. Existing valid flat layouts remain discoverable and are not automatically migrated.

Non-dry-run authoring uses the common pre-write mutation guard. The invoking environment must match the schema-3 released-evaluator identity locked by the target repository; candidate source and editable or contaminated installs fail without creating the requested path.

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

## Release unit derivation

```text
harnessctl release-unit [TARGET] --from TAG --to COMMIT [--exempt SHA ...] [--contract REL-ID] [--json | --toml]
```

Measures a release unit (`WO-CIP-004`, `ADR-CIP-002`): walks the first-parent history from the previous release tag to the candidate commit, reads the `Harness-Work-Order` trailers — a merge contributes the trailers of the commits it merged — and reports one row per work order with its lifecycle status and whether its execution scope touches the packaged surface (`se_harness/`, `templates/repository/standard/`, `pyproject.toml`). A commit with no trailer is `untraced`. The command exits 1 when a commit is untraced and not `--exempt`ed, when a listed work order is not `implemented`, or, with `--contract`, when the contract's `candidate_commit`, `previous_release_tag` or `gates` differ from the measurement (`E-CIP-001`). `--toml` prints only the `gates` array to paste into the contract. It mutates nothing, needs no network, and freezes nothing: the release owner's approval of the contract does that.

## Runtime identity

```text
harnessctl identity --role released-evaluator|candidate-source|candidate-package \
  --expected-version VERSION --expected-root PATH [options]
```

Key role-specific options are `--checkout-root`, `--candidate-commit`, `--evaluator-wheel-sha256`, `--entry-point`, `--require-isolated-python`, and `--require-entry-point`. The command verifies declared runtime origin; it does not select an evaluator or approve a candidate.

Runtime identity also observes the running interpreter's own entry-point path through the declared interpreter-safety rule and records three additional facts: whether the entry point is a symbolic link, which position class its resolved target occupies relative to the expected and checkout roots, and the target's SHA-256. The schema identifier stays `se-harness-runtime-identity-v3`, because consumers require a subset of the identity rather than an exact field set. The observation is recorded for every role, but only the two environment-bounded roles — `released-evaluator` and `candidate-package` — turn a refusal into the `RID024` diagnostic; `candidate-source` has no environment boundary, because its expected root is the checkout itself. `RID004` and `RID006` keep their existing meanings unchanged.

## Role-specific release qualification

```text
harnessctl qualify released-root [ROOT] [--output PATH] [--json]
harnessctl qualify predecessor-view [ROOT] --release-record RLS-... --evaluator-python PATH [--view-output PATH] [--output PATH] [--json]
harnessctl qualify complete-candidate [ROOT] --candidate-commit FULL_COMMIT [--output PATH] [--json]
harnessctl qualify candidate-package --candidate-wheel PATH --candidate-commit FULL_COMMIT --candidate-wheel-sha256 SHA256 --verifier-wheel-sha256 SHA256 [--checkout-root PATH] [--output PATH] [--json]
harnessctl qualify public-install [ROOT] --release-record RLS-... --public-wheel PATH --public-wheel-sha256 SHA256 --payload-sha256 SHA256 [--output PATH] [--json]
```

The five subcommands are separate closed parsers. They bind evaluator identity, target identity, fixed checks, and one independence class before reporting a result. They do not accept a general evaluator, validator, script, omission, or diagnostic-allowlist option. `--output` must name a new external file; the command never overwrites it or writes qualification evidence inside the inspected repository.

`--evaluator-python` is judged by the declared interpreter-safety rule before anything is spawned. Supply the environment's own lexical entry point — `bin/python` on POSIX, `Scripts/python.exe` on Windows — not the resolved system interpreter it points at. The environment root is derived from that lexical path, so an interpreter reached through a linked or junctioned parent directory is refused, as is one inside the inspected checkout or whose resolved target lands inside it. The terminal interpreter link itself is permitted, which is what makes an ordinary `python -m venv` environment usable on POSIX.

All operations emit `se-harness-release-qualification-v1`. The result identifies the operation, completion, outcome, evaluator, target, ordered checks, independence boundary, and its evidence-only authority. `complete-candidate` is always `candidate-controlled`, even when it passes. See [release qualification roles](release-qualification-roles.md) for the workflow map and the bounded public-0.6.0 bootstrap exception.

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

In a newly built version, `accept-candidate` is a one-cycle compatibility alias for `qualify candidate-package` and emits the typed qualification result. Exact public 0.6.0 predates the `qualify` namespace; its immutable command still emits `se-harness-functional-acceptance-v1` and is accepted only as explicitly labeled bootstrap evidence in the initial candidate workflow. That historical output is not converted into or described as canonical qualification evidence.

The verifier checks the caller-selected candidate digest, snapshots those exact wheel bytes, creates a fresh environment, installs the snapshot, runs the published black-box scenario set, and rejects checkout import fallback and authority substitution. Its output is evidence for human assurance review, never a VREC transition.

## Delegated Phase 4 workflow

```text
harnessctl delegated-workflow catalog [--json]

harnessctl delegated-workflow execute [TARGET] \
  --runtime-root PATH \
  --evaluator-package PACKAGE \
  --evaluator-version VERSION \
  --evaluator-payload-sha256 SHA256 \
  --evaluator-launcher-sha256 SHA256 \
  --work-order WO-... \
  --baseline-workspace PATH \
  --proposed-workspace PATH \
  --object-store PATH \
  --changed-path PATH \
  --start-gates JSON \
  --effect-gates JSON \
  --completion-gates JSON \
  --prepare-gates JSON \
  --tests JSON \
  --evidence-bindings JSON \
  --effect-deviations JSON \
  [--delete-path PATH] [--delegate ID] [--execution-profile PROFILE] \
  [--residual-uncertainty TEXT]

harnessctl delegated-workflow prepare-vrec [TARGET] \
  --runtime-root PATH \
  --evaluator-package PACKAGE \
  --evaluator-version VERSION \
  --evaluator-payload-sha256 SHA256 \
  --evaluator-launcher-sha256 SHA256 \
  --work-order WO-... \
  --id VREC-... \
  --verification VER-... \
  --evidence PATH \
  --output PATH \
  --domain DOMAIN \
  --gates JSON \
  --completion-proof JSON \
  [--owner ROLE] [--delegate ID] [--execution-profile PROFILE] \
  [--residual-uncertainty TEXT]
```

Repeat `--changed-path`, `--delete-path`, `--verification`, `--evidence`, and
`--residual-uncertainty` where applicable. JSON options name retained input
files, not trusted assertions: the coordinator re-observes live state, checks
the exact released-evaluator identity and nonce-bound delegation envelope,
requires successful gates and tests, and rejects receipt gaps or path drift.
`execute` derives and applies one change bundle through the separately guarded
effect broker, advances only the declared work order, and returns the canonical
candidate-commit decision packet instead of running Git. Its start and
completion outputs retain the receipt, envelope, and before/after observations
as one lifecycle proof. `prepare-vrec` starts only from that complete proof and
a clean exact candidate commit; it
prepares an undecided `ready` record and returns an assurance decision packet.
Neither command approves work, decides assurance, commits, pushes, opens a pull
request, releases, publishes, deploys, or uses credentials.

## Commit-bound verification preparation

```text
harnessctl capture-verification [TARGET] \
  --id VREC-... \
  --work-order WO-... \
  --verification VER-... \
  --evidence PATH \
  [--owner ROLE] [--domain DOMAIN] [--output PATH] [--json]
```

Repeat `--work-order`, `--verification`, and `--evidence` for an aggregate candidate. Every selected work order must be exactly `implemented`, the selected verification contracts must equal their declared union, and evidence must cover each work order. Before any derived output or record write, the command proves the locked released evaluator. It then requires a clean Git worktree, derives the full `HEAD` object identity, generates the deterministic Explorer bundle, stores the SHA-256 of its recursively binding `dashboard-manifest.json` as `artifact_snapshot_sha256`, writes canonical normalized evaluator evidence under the selected domain's `evidence/` directory, and binds that file's repository-relative path and SHA-256 in the `status = "ready"` VREC. The record contains `prepared_at` and `prepared_by`, never `verified_at` or `verified_by`.

An accountable assurance owner reviews the retained evidence and separately decides whether to transition the VREC to `verified`. The record lives in later governance history and continues to bind the earlier candidate commit C.

If a later verified or released VREC fully covers a prepared ready record, the assurance owner may instead apply the declared `ready -> superseded` transition and name that successor with `--reason`. The command preserves `prepared_at` and `prepared_by`, adds only the supersession decision fields, typed successor relation, lifecycle event, status, and update date, and does not add `verified_at` or `verified_by`. Supersession means the proposal was retired, not verified. Historical superseded VRECs without preparation fields may retain the older valid `verified_at` capture shape; validation does not rewrite them or fabricate `verified_by`.

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

Before writing, the command proves the locked released evaluator including its wheel filename and SHA-256. It writes canonical normalized evaluator evidence and binds the evidence path and digest in the `status = "ready"` RLS. The record contains `prepared_at` and `prepared_by`; it omits `released_at` and `authorized_by` until a separate release transition. The managed `.gitattributes` fragment applies exactly `docs/engineering/**/evidence/*.json text eol=lf`, preserving canonical evidence bytes across supported checkouts so the raw SHA-256 survives. Independent validation and publication replay reject missing, changed, noncanonical, candidate-role, host-path-leaking, or lock-mismatched evidence. A rejected predecessor-bootstrap contract can support only its exact rejected RLS as terminal history and remains invalid for preparation, binding, release, publication, or credential-bearing use. The command does not transition the record to `released`, commit, push, tag, create a GitHub Release, publish to PyPI, or deploy.

Only `ready` and `released` release records claim a version. Valid rejected records remain immutable audit history and do not prevent one correctly bound active successor for an unpublished version; a second active record still fails. In the repository-specific schema-2 bootstrap case where released 0.5.0 cannot parse one exact rejected RLS/contract pair, `scripts/prepare_predecessor_release.py` runs predecessor `prepare-release` only inside a contract-derived exact-commit sparse view. Its canonical sidecar proves the two omissions and exact command; the adapter imports only the predecessor-generated proposal, and the existing bootstrap binder remains the separate evaluator-evidence step. This compatibility path does not alter generic `harnessctl prepare-release`, the root evaluator, or historical artifacts.

For this repository's transitional hosted qualification, `scripts/assess_predecessor_evaluator.py` reuses that exact view derivation. It separately records the immutable 0.5.0 full-checkout `E009`, requires `doctor`, `validate`, and dashboard generation to pass in the view, validates the complete candidate graph before and after, and optionally creates one canonical evidence file outside the checkout. It accepts no omission or expected-error arguments and performs no `harnessctl` lifecycle action.

For the repository-specific publication gate, `qualify predecessor-view` calls the fixed production predecessor-publication service. It selects one exact released RLS, replays its preparation-view and evaluator sidecars against current Git history, validates the complete clean governance graph before and after, and requires the exact external predecessor `doctor` and JSON `validate` to pass in a detached view that omits only the bound rejected REL/RLS pair. The public parser accepts no omission, expected-error, entry-point, wheel, or script input; it derives the fixed external files from the selected interpreter and governed release evidence. It does not claim that the predecessor parsed omitted history and grants no publication or lifecycle authority.

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
