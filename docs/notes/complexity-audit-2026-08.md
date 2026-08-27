# Complexity audit: machinery that should not become permanent

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Repository-owned note. It records a read-only audit of the tree at `f0ecd9b`
(2026-08-27; 771 commits; v0.2.0 to v0.7.1 in sixteen days) looking for
complexity that accumulated to handle past, temporary, or circumstantial
situations and that should not become part of the permanent architecture. It
grants no approval, verification, or release authority, changes no lifecycle
state, and proposes no work order by itself. Every deletion it recommends that
touches an approved artifact is an amendment under this repository's own rules.

Measured sizes: package 22,571 lines; repository tooling about 8,300; installed
scripts about 7,000; tests 27,896; 1,156 formal artifacts.

## Question this note answers

Where has SE Harness accumulated code, abstractions, or workflows whose
maintenance cost, cognitive load, or usability friction exceeds their long-term
value, and what is the simplest alternative that keeps the guarantees that
matter: correctness, traceability, determinism, authority separation,
repository portability, still-required backward compatibility, and safety?

## Executive summary

The core is proportionate and should stay: the artifact graph and its
validator, explicit human transitions, commit-bound records with hashed
evidence, a released evaluator that governs instead of the checkout, the
transactional installer, and the reproducible container build. The unnecessary
complexity sits in three strata that grew around that core.

1. **The 0.6.0 bootstrap era leaked into the product.** Between 08-20 and
   08-24 the repository had to release itself while governed by an evaluator
   that could not parse its own new records. The bridge built for that
   (predecessor-view adapters, the evaluator-transition lane, the
   governance-migration rehearsal, the recovery rehearsal, the
   `accept-candidate` alias, lock schema 1) is still live code, and parts of
   it ship to consumers. `hash_bound_classes.json` and the managed
   `.gitattributes` fragment reference `se_harness/governance_migration*.py`,
   so **`harnessctl init`, then `git commit`, then `harnessctl doctor` exits 1
   in every fresh repository** (reproduced in-tree; the 0.7.1 wheel carries
   identical bytes). `qualify predecessor-view` in the wheel imports
   `repository_tools`, which is not packaged. Six `RLS-SEH-*` identifiers of
   this repository's own releases are hard-coded in three generic files.

2. **Phase 4 agentic execution (8,766 lines, 39% of the package) was built in
   72 hours, cut mid-way into 0.7.0, and has never been activated in any
   target.** No `[agentic_delegation]` table exists anywhere; `REL-SEH-015`
   calls it inert. Its authority envelope carries nonces, five-minute
   lifetimes, revocation, and double-observation stability checks for a token
   that never leaves the process that minted it. About 1,800 lines of Phase 1
   and 2 predecessors (`agent_contract` v1 constructors, all of
   `skill_contract.py`, `agent_contract.json`, `effect_contract.json`) have
   zero product callers.

3. **Duplication in the workflow core and in primitives.** Two result
   envelopes with a lossy projection between them and inconsistent defaults;
   two rule engines for "what next"; three implementations of transition
   preconditions; every CLI command re-derives the same validation and scope;
   eight atomic writers, seven front-matter parsers, six Git wrappers, five
   canonical-JSON implementations, five validator invokers with different
   isolation policies; and five JSON "contracts" that carry no information
   beyond a checksum of the Python that reads them.

A recurring pattern deserves its own name: **JSON mirrors of Python constants,
validated for equality by tests** (`agent_contract.json`,
`effect_contract.json`, `interpreter_safety.json`,
`governance_migration_contract.json` with its own `implementation_sha256`, and
the `agentic_operations` block of `workflow_contract.json`). No non-Python
consumer reads any of them as data; each doubles every edit.

Plausible reduction while keeping every guarantee above: roughly 9,000 to
11,000 lines of product and tooling code plus about 5,000 lines of tests, and
13 to about 7 CI jobs per pull request.

## Method

Seven independent read-only passes, one per subsystem (CLI and workflow core;
agent-facing instruction surface; provenance, identity, and release
qualification; repository-owned release tooling; installation, upgrade, and
migration; delegated execution; installed scripts and dashboard). Each pass
read its modules in full, used `git log -S` to learn why each mechanism was
added, and counted callers to separate product use from test-only use. The
highest-impact claims were then re-verified by hand: the consumer `doctor`
failure was reproduced from a fresh `init`; the unpackaged import at
`release_qualification.py:634`, the zero-invocation scripts, the dead Phase 2
constructors, the absence of any `skill_contract` product caller, and the
`--result-schema` default disagreement were each confirmed by grep.

Priorities: **P0** major architectural complexity or severe usability impact;
**P1** meaningful simplification with clear long-term benefit; **P2**
worthwhile cleanup with limited structural impact; **P3** minor. Verdicts:
REMOVE, SIMPLIFY, CONSOLIDATE, KEEP.

## P0 findings

### P0-1. Self-hosting residue shipped to every consumer breaks `doctor`

- **Where:** `se_harness/hash_bound_classes.json:19-32` (class
  `governance-migration-protocol`),
  `templates/repository/standard/gitattributes.fragment:4-6`,
  `se_harness/hash_bound.py:454-457` and `:485-499`.
- **What it does:** declares hash-bound patterns for files that exist only in
  this repository. The checker fails any class whose pattern matches no tracked
  path, and fails any `repository`-region pattern found only in the template
  region. The `evaluator-evidence` pattern also fails on a fresh repository
  until its first verification record exists.
- **Evidence:** reproduced with the in-tree 0.7.1 code: `init`, `git init`,
  commit, `doctor` prints `FAIL hash-bound-class-declared: ...
  se_harness/governance_migration*.py matches no tracked path` and
  `FAIL hash-bound-attribute-effective: ... is declared in template; requires
  the repository region`, exit code 1. `git diff v0.7.1 HEAD` on the two files
  is empty. `candidate_acceptance.py` never runs `git init` in its target and
  `preflight.py:131-132` skips these checks outside a worktree, so the
  acceptance lane is structurally blind to the failure.
- **Impact:** portability broken for the primary audience; a green `init`
  followed by a red `doctor`.
- **Verdict:** REMOVE the class and the three fragment lines; treat "pattern
  matches nothing" as a warning, or apply it only to `repository`-region
  classes. Pin this repository's own LF bytes in its own `.gitattributes`
  outside the managed block.
- **Lost:** nothing for consumers. It is a managed-file change, so consumers
  see an `update` on their next upgrade.

### P0-2. The predecessor bootstrap bridge (0.5.0 to 0.6.0) is still live in the wheel, in CI, and in the consumer validator

- **Where:** `repository_tools/predecessor_preparation.py`,
  `predecessor_publication.py`, `predecessor_assessment.py`,
  `release_bootstrap.py` (3,851 lines together);
  `scripts/prepare_predecessor_release.py`,
  `assess_predecessor_evaluator.py`, `bind_release_bootstrap.py`,
  `validate_predecessor_publication_view.py`; about 2,250 lines of tests;
  `publish-pypi.yml:119-161` and `pages-publication.yml:1016-1064` (inline
  Python deciding "bootstrap tuple or exclusion");
  `se_harness/release_qualification.py:623-691` (`qualify predecessor-view`,
  importing the unpackaged `repository_tools` at line 634);
  `scripts/check_portable_release_surface.py:603-612` (requires
  `predecessor-view` to appear in `--help`); the template validator's
  `_validate_predecessor_view_evidence` (325 lines, `:1135-1460`);
  ARCH-REB-002/004/005/006 and SPEC-REB-003/005/006/007.
- **What it does:** builds a sparse Git view omitting the rejected
  `RLS-SEH-009` so the released 0.5.0 evaluator could validate the 0.6.0
  record, records view evidence, and replays it at publication.
- **Evidence:** `predecessor_assessment.py:44-49` hard-codes
  `EXPECTED_LEGACY_ERROR` as E009 at `RLS-SEH-009.md`; `_derive_history`
  requires exactly one rejected bootstrap record in the whole repository; only
  REL-SEH-008 to 011 ever carried a `[bootstrap]` tuple; the 0.7.0 and 0.7.1
  records have none; `developing-se-harness.md` already titles the section
  "Historical one-release predecessor bootstrap";
  `bind_release_bootstrap.py` and `prepare_predecessor_release.py` are invoked
  by nothing.
- **Impact:** about 6,000 lines plus four ARCH, four SPEC, and about twelve
  work orders to understand before touching release code; a shipped
  subcommand that can only print "service unavailable" in a consumer; a
  consumer validator spending 19% of its lines on this repository's release
  mechanics.
- **Verdict:** REMOVE the adapters, scripts, workflow branches, the
  `predecessor-view` role, and the surface-checker pin. Gate or relocate the
  validator's predecessor-view rules; they must still accept RLS-SEH-014 and
  015 as history.
- **Lost:** re-validation of RLS-SEH-012 by 0.5.0, a published release whose
  evidence stays tracked and hash-bound. Needs one repair work order and a
  superseding ADR.

### P0-3. `validate_governor_transition.py` refuses the upgrade the owner wants

- **Where:** `scripts/validate_governor_transition.py` (741 lines);
  `.github/workflows/predecessor-evaluator-assessment.yml`, run on every pull
  request.
- **What it does:** its positive path demands an `implemented` work order
  carrying `[evaluator_upgrade]` with `authorized_by`, an
  `-evaluator-upgrade.json` evidence file, `distribution.schema == 1`, and a
  non-null `archive_sha256`.
- **Evidence:** SPEC-REB-012 (approved 08-27, commit `8dcd561`) retired exactly
  the packet gates MG004 and MG007; every record since RLS-SEH-014 is schema
  2; `archive_sha256 = null` is now legal. The next 0.6.0 to 0.7.x root move
  is refused on three independent counts. What the lane contributes today is
  a lock-drift guard (`:456-462`) and `git diff --exit-code`.
- **Verdict:** REMOVE the script and the lane; keep the drift guard as one
  `git diff --quiet <base> HEAD -- .engineering-harness.lock
  .engineering-harness.toml` step in `candidate-evidence.yml`.
- **Lost:** nothing; the lane cannot pass a real transition.

### P0-4. The governance-migration rehearsal asserts two booleans against a toy graph, under a self-hashing contract

- **Where:** `se_harness/governance_migration.py` (870),
  `governance_migration_contract.py` (453) and its JSON;
  `candidate-evidence.yml:294-420` (about 130 lines, two platforms, two runs
  each); `tests/test_governance_migration.py` (544); fixtures.
- **What it does:** 129 `MIG*` codes. Probes two interpreters, then runs nine
  stages against `state/graph.json` in a temporary directory. The validation
  step, `_proposal_validation()` at `:373-382`, checks `schema == 3` and
  `evaluator_evidence is True`. The predecessor interpreter is never asked to
  do anything beyond printing its identity. The contract JSON embeds the
  module's own `implementation_sha256` six times, so every edit is a two-file
  change, and the `.gitattributes` pins of P0-1 exist to keep that hash
  stable.
- **Evidence:** born in `ca275ac` (08-23) immediately after the 0.6.0
  handover; `MIG404`'s boundary is hard-coded to 0.6.0's own rule; `MIG211`
  coupled the scenario to the `pyproject` version and silently skipped four
  CI jobs until WO-REB-023.
- **Verdict:** REMOVE the stage machine. Replace it with a rehearsal that runs
  the real `harnessctl upgrade --apply` of the successor against a throwaway
  copy of the repository holding the real predecessor lock: about 80 lines
  that exercise the installer. Keep the N-1 identity derivation in
  `predecessor_facts.derive`.
- **Lost:** the ritual, not the property. "N-1 stays selected until adopt" is
  enforced by `mutation_guard` and the lock.

### P0-5. A decision, not a deletion: is Phase 4 a product or an experiment?

- **Where:** `delegated_workflow.py` (1,784), `effect_broker.py` (1,215),
  `delegated_authority.py`, `change_bundle.py`, `repository_state.py`,
  `runtime_state.py` (770), `agent_contract.py` (2,581), `skill_contract.py`
  (1,086): 8,766 lines; 68 artifacts under `agentic-execution`; five shipped
  skills.
- Every P1 finding below tagged **[AEX]** is a sub-item of this one. If the
  owner treats Phase 4 as a bet, quarantine it behind one feature boundary
  (the `delegated-workflow` subcommand and the three writing skills) and prune
  it as a unit later. If it is the product's future, do the [AEX]
  simplifications now, before the design hardens. Either way, decide this
  before spending P1 effort inside it.

### P0-6. Two result envelopes, two rule engines, and three precondition implementations in the workflow core

- **Where:** `workflow.py:99-142` (schema 1 `handoff`),
  `workflow_result.py:68-119` (schema 2 `restitution`),
  `workflow_result.py:210-285` (`legacy_to_schema2`, which fabricates
  `PROC-COMPATIBILITY` and `shlex.split`s prose back into argv);
  `cli.py:999`, `:1042`, `:1241`, `:1323` (`--result-schema` defaults to 2 on
  `focus` and to 1 on `transition`, `capture-verification`, and
  `prepare-release`; `focus --result-schema 1` prints a warning telling the
  user not to use it). `workflow.py:355-399` `_recommend` versus
  `workflow_contract.py:554-595` `select_rule` (same table, two context
  builders computing `successor_id` differently). `workflow.py:685-750`
  `_validate_preconditions` (hard-coded) versus the `transition` checkpoint in
  `quality_gates_contract.json` (never evaluated: `check_workflow` refuses
  `transition` at `workflow_compliance.py:990`) versus
  `ensure_governed_checkpoint` at `workflow_compliance.py:1335-1374` (matches
  predicate identifiers as strings). The preflight-diagnostic filters differ
  (`workflow.py:668-682` and `workflow_compliance.py:844-853`), so
  `transition` and `check` can disagree on the same work order.
- **Evidence:** schema 1 was the only format for two days (08-21 to 08-25);
  `legacy_to_schema2` has no test importer; the template CI consumes only
  `check --json` (schema 2); `result_sha256` binds only schema 2.
- **Verdict:** CONSOLIDATE. Schema 2 only; `_recommend` delegates to
  `select_rule`; `plan_transition` evaluates the contract gates for the
  `transition` checkpoint through `_gate_results` and keeps only
  graph-structural checks in Python.
- **Lost:** nothing, provided `result_sha256` stays defined over the schema-2
  block (it is). The released evaluator is version-pinned, so no
  cross-version JSON contract exists.

## P1 findings

| # | Finding | Where | Verdict and alternative | Lost |
| --- | --- | --- | --- | --- |
| P1-1 | `qualify candidate-package`, `public-install`, and `candidate_acceptance.py` (446 lines) qualify se-harness by name (`Name: se-harness` at `candidate_acceptance.py:335-353`; `public-install` asserts this repository's RLS distribution table and greps its own `--help`). The `accept-candidate` alias, the `candidate-evidence.yml:225-307` fallback, and `predecessor_facts.LEGACY_ACCEPTANCE_CONTRACT_SHA256` exist for a "one bootstrap cycle" that expired with 0.7.0. | `release_qualification.py:525-578`, `:746-830`; `cli.py:722-728`, `:1218-1228` | CONSOLIDATE: keep `released-root` and `complete-candidate` as the consumer-usable `qualify`; move the two self-checks to `repository_tools`; delete the alias with the root upgrade. | None; ADR-REB-009's "five operations" needs an amendment. |
| P1-2 | Six `RLS-SEH-*` identifiers hard-coded in three generic files, and SPEC-LRE-001 rule 14 mandating two implementations kept equal by a fixture. | `legacy_release_evidence.py:30-36` (327 lines); template validator `:73-78`, `:1755-1830`; `.github/scripts/publish_dashboard.py:76`; `installer.py:495-520`; `cli.py:149-176` | SIMPLIFY: declare the six through the specification's own rule-5 mechanism in an approved SEH upgrade work order; delete the constant everywhere; let the package call the template's resolver through the module it already loads. | None; the same records stay exempt, through data. |
| P1-3 [AEX] | The authority envelope defends a token that never crosses a trust boundary: a five-minute `MAX_ENVELOPE_LIFETIME`, a nonce ledger, `revoked` (passed by product code zero times), `retry_ordinal` (always 0), and the "two byte-identical observations" rule. | `delegated_authority.py:25`, `:206`, `:262`, `:343`; `runtime_state.py:368-434`; `repository_state.py:375-418` | SIMPLIFY to `resolve_delegation` narrowing plus one observation before and one after. | Replay protection for externally supplied envelopes; none exist. Re-add when skills submit envelopes. |
| P1-4 [AEX] | About six full-tree hash-and-validate passes and three broker snapshots per bundle; `_file_manifest` runs three times and digests each file twice; `phase4_operation_catalog()` re-validates the contract three or four times per operation. | `repository_state.py:274-372`; `effect_broker.py:867`, `:913`, `:923`, `:1096`; `delegated_workflow.py:184-642` | SIMPLIFY: digest once and derive the manifests; one observation on each side. | None; the exclusive lock already serialises writers. |
| P1-5 [AEX] | Dead Phase 2 machinery: v1 envelope constructors, `assess_admission`, `render_decision_packet`, the catalog parser (about 700 lines, zero product callers); `agent_contract.json` (68 KB) is read only by tests asserting it equals the Python. | `agent_contract.py:911-985`, `:1724-2230`, `:2410-2544`; `pyproject.toml:31` | REMOVE. Keep `_bounded_walk`, `_parse_json_bytes`, and the portable-path validation, which are live. | None. |
| P1-6 [AEX] | `skill_contract.py` (1,086 lines) has zero product callers and three frozen schema generations (v1 orient, v2 operator-brief, v3 Phase 4) with per-skill closed instances copied verbatim from the JSON; a fifth copy of `canonical_json_bytes`. | `skill_contract.py:15-17`, `:236-570`, `:723-1010` | SIMPLIFY: one schema with structural validation only, or a SHA-256 pin test per contract. | The frozen Phase 3 vectors need regeneration; history, not behaviour. |
| P1-7 [AEX] | The shipped skill helpers inject a stub `client=lambda ...` and print `"evaluator_invoked": False`, while SKILL.md says they invoke the evaluator; the agent then re-issues the command by hand. | `harness-execute-work-order/scripts/check_scope.py:180-203`; `check_prepare.py:165-186` | SIMPLIFY: run the evaluator as a subprocess for real, or cut each helper to a 30-line scope check; consolidate the three copy-pasted guards. | None; today they enforce nothing. |
| P1-8 | `interpreter_safety`: the rule itself (`evaluate()`, about 150 lines, fixing RC-060-06) is justified; the 440 lines of declaration bookkeeping are not. The JSON's cases carry no logic; ISD117 asserts the JSON order equals `EVALUATION_ORDER`; a call-site registry and a corpus inventory live in data; and a near-identical second copy in `repository_tools` is justified by an import barrier that `release_bootstrap.py:19` already violates. | `se_harness/interpreter_safety.py:127-360`; `repository_tools/interpreter_safety.py`; `tests/test_interpreter_safety.py` (1,445) | SIMPLIFY: keep `evaluate` and the EPS codes; delete the JSON, the loaders, the boundary registry, and one copy (its only callers vanish with P0-2). | The "declaration is data" wording of WO-REB-021; no consumer reads it. |
| P1-9 | `recovery_rehearsal.py` (304 lines, a CLI subcommand, 125 test lines) builds a fake wheel and a fake lock with `"1"*64` digests, runs its own private transaction with `fail_after=2`, and asserts its own rollback. It exercises none of `installer.apply_changes`, hard-codes this repository's workflow names, and has no CI caller. | `recovery_rehearsal.py`; `cli.py:215-229`, `:1067-1075` | REMOVE; keep the runbook prose. | SPEC-REB-002 rule 14's "disposable rehearsal"; satisfy it with a real installer test. |
| P1-10 | `renumber.py` (1,316 lines, 81 codes) for a feature never applied in this repository: a Git-index inventory with byte caps, reserved names, case-fold and hard-link checks, `check-ignore` per destination, a private recovery directory, and a bespoke TOML span parser, while leaving the result uncommitted, so Git is already the rollback. | `renumber.py:37-45`, `:408-455`, `:531-618`, `:712-722`, `:918-947`, `:1301` | SIMPLIFY to about 250 lines: mapping checks, the `_render_draft`-style rewrite, `git mv`. | The "resulting hash equals plan hash" postcondition; the validator postcondition stays. |
| P1-11 | Self-hosting skew handling inside evaluator logic: `I001 distribution:*` and `lock-entry:*` are skipped by path prefix in two divergent filters; `doctor` runs a second validator subprocess only to print W013; `inspect_installation`'s distribution checks are meaningful only here. | `workflow.py:668-682`; `workflow_compliance.py:836-853`; `cli.py:317-339`; `preflight.py:136-239` | SIMPLIFY: one documented skew policy instead of two string filters. | Nothing; authority separation improves. |
| P1-12 | Lock schema 1 support: no release ever shipped it (schema 2 landed in `505e889` on day one); schema-1 locks exist only in tests; the installer can still write schema 1 at `:575`. | `integrity.py:59-70`, `:522-523`, `:570-581`, `:660-694`; `installer.py:293-299`, `:575`; `hash_bound.py:278-294`; `preflight.py:216-223` | REMOVE the schema-1 paths; keep the schema-2 read path, since 0.2 to 0.5 consumers exist. | None in the wild. |
| P1-13 | No shared repository snapshot: `validate`, `doctor`, `preflight`, `focus`, `check`, and `inspect` each re-derive validation, catalog, and scope; `focus_schema2` runs the validator twice; `focus` is `check` without gates; `doctor` is a subset of `preflight`; five validator invokers apply different interpreter hygiene (`renumber` isolates site-packages, `provenance` does not). | `cli.py:322-335`; `provenance.py:91-97`; `release_qualification.py:323-329`; `renumber.py:385-395`; `preflight.py:242-260` | CONSOLIDATE: one loader and one invoker with one environment policy; `focus` becomes `check --checkpoint focus`; `doctor` becomes `preflight --installation-only`. | Nothing; determinism improves. |
| P1-14 | CI runs 13 jobs, 7 candidate builds, and 3 full test-suite passes per pull-request push. `rehearse-record` replays the already published 0.7.1 recipe on every pull request; `integration-package-*` (3 jobs, a 1,002-line script) builds a three-day artifact nobody consumes; the "prove no checkout change" block is copied seven times. | `.github/workflows/*` (1,894 YAML lines) | SIMPLIFY to about 7 jobs, 3 builds, 2 suite passes; run `rehearse-record` and integration packages on dispatch or `push: main`. | None. |
| P1-15 | Two whole-tree snapshot digests bind the same thing: verification records bind `sha256(dashboard-manifest.json)`, which moves with HEAD, the checkout basename, and clone depth, while the agentic lane binds `formal_snapshot_digest`. | `provenance.py:315-327`; `workflow_compliance.py:185`; `repository_state.py:258-271` | CONSOLIDATE on the formal digest as the producer; keep the field name; do not rewrite the 138 historical documents. | The manifest binding of dashboard readiness resources; needs a REV amendment. |

## P2 findings

| # | Finding | Verdict |
| --- | --- | --- |
| P2-1 | Five JSON mirrors that only checksum Python: `effect_contract.json` (read by no product code), the `agentic_operations` block (`workflow_contract.py:67-72`, `:445-472` demand that the JSON reproduce a tuple), `interpreter_safety.json`, `governance_migration_contract.json`, `agent_contract.json` (the last three already appear above). | REMOVE the mirrors; Python is the source. |
| P2-2 | Lifecycle registry rows carry six fields of which three are unread: `transitionable` equals `bool(transitions_to)`, `must_remain_visible` is required to be `true` everywhere, `predecessor_adapter` has no reader; about ten states with empty edges that no artifact uses. | SIMPLIFY to `transitions_to`, `grants_authority`, `reserves_version`. |
| P2-3 | Procedure typing exceeds its use: 17 procedures, 12 of them a single `decision` step; parameter `type`, `cardinality`, `source`, and reference-cycle checks for zero `reference` steps; `select_current_step` sniffs argv for `preflight` and `check`; corrective forms are repeated verbatim three times. | SIMPLIFY; keep the corrective-form requirement itself. |
| P2-4 | `check --change-manifest`, `--pull-request-body`, and `focus --include-background` have no consumer outside documentation and one test; the CR check duplicates `select-work-order`. | REMOVE. |
| P2-5 | About fifteen diagnostic families (WEX, QGP, MG, MIG with 129 codes, REN with 81, SKC and SKM with 49, ISD, EPS, and ISC with 46, AEX families with 69, E, W, and W-AUT, W-HEX, W-REB, and W-REV in the dashboard's second rules engine, package W0xx); W013 means different things in two of them; no catalog exists; `_repository_workflow_error` classifies failures by substring-matching messages. | CONSOLIDATE as a by-product of the deletions above; typed exceptions instead of message sniffing. |
| P2-6 [AEX] | The broker re-validates its own writes (`_validate_journal`, 95 lines, with a `plan_sha256` self-checksum); `validate_effect_receipt` is a 160-line hand-written schema; `_DEFAULT_DENIED` hard-codes 18 managed paths instead of deriving them from the installer manifest; `change_bundle._read_file` and `effect_broker._file_state` are 70-line near-duplicates; dry-run receipts are built twice per operation; `candidate_commit_stop` duplicates completion's own packet; `refuse_prohibited_action` (88 lines, 13 strings) has no caller; the assurance classification drives only the shape of one error and all 22 work orders say `required`. | CONSOLIDATE or REMOVE. |
| P2-7 | The receipt `phase1` legacy branch keeps eight `legacy_sets` deviation shapes because `orient.py` was never moved to the full form (Phases 1 and 3 landed the same day). | SIMPLIFY: fix `orient.py`, delete the flag. |
| P2-8 | Repository-local instruction tests pin a 6,000-byte owner-region budget found in no product code, thirteen prose substrings, a managed-path count of exactly 30, and a 40-entry allow-list of files permitted to mention a retired file; `check_portable_release_surface.py` forbids one English word in README and notes and pins that `predecessor-view` exists, turning a leak check into a feature freeze. | SIMPLIFY: keep the managed-block digest test and the true leak checks. |
| P2-9 | `preflight.REQUIRED_PATHS` and `POLICY_PATHS` restate the template manifest by hand; `effect_broker.py:57-70` and `repository_state.py:353` list it again. | CONSOLIDATE: derive from `template_files()`. |
| P2-10 | `.engineering-harness.toml` writes `schema_version = 2` that nothing reads; `tool_version` is duplicated with the lock, and `MG003` exists only to police that duplication. | SIMPLIFY: the lock is authoritative. |
| P2-11 | `pyproject.toml:40-112` enumerates 61 template files one by one, `MANIFEST.in` repeats the tree, `template_root()` probes two locations, and six tests hard-code the `data/data/share` prefix. | CONSOLIDATE: `se_harness/_templates/**` as package data with one glob; update `PACKAGED_SURFACE_PREFIXES` in the same change. |
| P2-12 | `migrate_verification_methods.py` is a migration never applied (266 requirements still hold strings, none hold arrays); it is blocked until the root upgrade and is then a one-shot. | APPLY inside the upgrade work order, then REMOVE. |
| P2-13 | Primitive duplication: eight atomic writers (three `os.link`, five `os.replace`), seven TOML front-matter parsers with different BOM, CRLF, and size rules, six Git wrappers with timeouts of 30, 60, 120, and 180 seconds, five canonical-JSON implementations, two safe-environment builders with different allow-lists, three launcher finders, including six copies inside `repository_tools` after `json_bytes.py` was created to be the one definition. | CONSOLIDATE into `integrity.py`, a `front_matter.py`, and `json_bytes.py`. |
| P2-14 | The upgrade-evidence JSON carries retired packet fields as `null` (commit `8dcd561`, 08-27). | Bump to a v2 without the nulls; textbook residue about to become permanent. |
| P2-15 | `scripts/` mixes nine hash-locked 0.6.0 payload files with twelve repository-only tools, nothing in the tree says which is which, and the packaging boundary is a deny-list rather than placement. | SIMPLIFY: move repository tools to `tools/`; add a header to the managed copies. |
| P2-16 | The dashboard's `import_experiments` (about 110 lines plus the `harness-experiment-result-v1` schema) has no producer anywhere. | REMOVE. |

## P3 findings

`workflow_procedures.ensure_validated` (no caller); `load_lifecycle_registry`
re-loaded at import in three modules; `DEFINITION_TYPES` defined three times;
`identity_sha256` computed over a dictionary of SHA-256 values;
`QualificationResult.authority` prose in every JSON; the `release_distribution`
V1 write path; `build-recipe.json` carrying 100 lines the interpreter refuses
to vary; `orient.py`'s 0.5.0 `--help`-sniffing fallback while skill contracts
already floor at 0.6.0; hand-written `.claude` adapters and `openai.yaml` that
could be generated from the contract (and `operator-brief` lacks both);
`select_harness_work_order.py` installed into every consumer but called by no
template workflow; `runtime_state.py` keeping two lock files and two journals
for one single-process caller (fold session, recovery, and revocations into
one file; keep the OS lock and the nonce ledger).

## Complexity that looks unnecessary but should be kept

- **Root `scripts/*` lagging the template by about 860 lines.** Not drift:
  they are the pinned 0.6.0 evaluator's payload, hash-bound in the lock.
  Editing them is an evaluator upgrade. Add a header saying so.
- **The container double build, `normalize_sdist.py`, declared source modes,
  and the workspace hand-back** in `release_build.py`. Each maps to a recorded
  failure: RLS-SEH-014 was rejected because a Windows-built wheel agreed with
  itself and was wrong in 83 line-ending and 69 mode facts. Keep; run it fewer
  times (P1-14).
- **The installer's transactional core**: plan-refresh re-check, pre-write
  snapshot and rollback, seed, managed, and fragment ownership, and the
  REQ-LRE-002 refusal before an identity transition. Proportionate for a tool
  that rewrites `.github/workflows` and `AGENTS.md` in someone else's
  repository.
- **`mutation_guard` MG001 to MG006** (minus MG003): the single enforcement
  point of "the released evaluator governs, not the checkout".
- **`runtime_identity`, `evaluator_identity`, `evaluator_evidence`** as three
  layers: observation, payload identity (the only thing an index install can
  prove), and the privacy-normalised committed artifact. The surface is
  frozen; only the duplicate `repository_state.EvaluatorIdentity` dataclass is
  waste.
- **`interpreter_safety.evaluate()`** itself: it fixes a real symlinked-venv
  incident (RC-060-06).
- **The `hash_bound.py` core and its "no default mode" rule**: this is what
  fixed the Windows CRLF evidence-digest fault. Only the third class and the
  every-pattern-must-match strictness are the defect (P0-1).
- **`result_sha256` and `select-work-order --field restitution-digest`**: the
  only mechanism binding an agent's stated restitution to a measured snapshot;
  the template CI recomputes it at the pull-request head.
- **`TransitionPlan`'s staged write and rollback with stale-input checks over
  every artifact**: what makes a multi-artifact `--apply` atomic.
- **Corrective forms (ADS-RST-001) and "a corrective must not repeat the
  evaluated command"**: they prevent the agent loop of re-running the failing
  command. Keep the rule; de-duplicate the per-step repetition.
- **Journaled bundle apply, rollback, and `human-recovery-stop`** with the
  fault-injection tests: the only thing making an agent's multi-file write
  safe on Windows, where `os.replace` can fail mid-bundle. This is the piece
  of Phase 4 to keep whatever P0-5 decides; likewise `resolve_delegation`
  narrowing (60 lines) and the intent of `_DEFAULT_DENIED`.
- **The dashboard manifest, `verify_serialized_bundle`, and `ContentBudget`**:
  every verified record binds this digest; removing it orphans history. Change
  the producer (P1-15) only going forward.
- **The workflow-v4 lifecycle registry loader**: it replaced four hard-coded
  status sets with one source of truth; the strictness is what makes
  authority a data property. Trim fields (P2-2), not the loader.
- **The legacy-release-evidence declaration mechanism (rules 1 to 10)**:
  real 0.5.0-and-earlier consumers exist and 0.6.0 froze them; only the
  hard-coded set and the double implementation are residue.
- **Windows skip guards and `run_tests.py`**: each guards a reproducible host
  difference; the Linux lane runs with zero skips.
- **The N-1 to N migration rehearsal on both platforms as a lane**: the
  Windows leg has caught real defects. What should change is what the lane
  runs (P0-4), not that it exists.
- **The stdlib-only, no-`se_harness`-import rule in skill scripts**:
  consumers run a pinned evaluator that may differ from the checkout. Keep
  the rule; de-duplicate within the template tree.

## Top five simplifications

1. **Evict self-hosting from the shipped product.** Drop the
   `governance-migration-protocol` hash-bound class and the three
   `.gitattributes` fragment lines (this fixes the consumer `doctor`
   failure); move `predecessor-view`, `candidate-package`, `public-install`,
   and `candidate_acceptance.py` out of the wheel into `repository_tools`;
   replace the six hard-coded `RLS-SEH` identifiers with a rule-5
   declaration; gate the validator's predecessor-view rules; split `scripts/`
   into managed payload and `tools/`. Preserved: everything; consumers gain
   portability and this repository keeps its history through data.

2. **Delete the 0.6.0 bootstrap era.** The predecessor adapters, scripts, and
   workflow branches (about 6,000 lines); `validate_governor_transition.py`
   and its lane, which would block the wanted upgrade; the
   governance-migration stage machine, replaced by an 80-line real
   `upgrade --apply` rehearsal; `recovery_rehearsal.py`; the
   `accept-candidate` alias and its legacy CI branch; the lock schema-1 paths;
   `migrate_verification_methods.py` after one application. One repair work
   order with a superseding ADR each. Preserved: every published record and
   its evidence stays tracked and hash-bound.

3. **Decide Phase 4, then cut it to its guarantee.** Keep journaled apply and
   rollback, `resolve_delegation`, one observation before and one after, and
   `mutation_guard` gating. Remove the envelope's nonce, lifetime, revocation,
   and stability apparatus, the dead Phase 2 constructors,
   `skill_contract.py`'s closed instances, `agent_contract.json` and
   `effect_contract.json`, proof re-verification, the stop and refuse packets,
   and the dry-run receipts; make the skill helpers call the evaluator for
   real. Roughly 3,900 to 2,300 lines in the execution chain and about 1,800
   fewer in its client surface. Preserved: scope enforcement, traceability of
   what the agent changed, crash-safe apply.

4. **One result schema, one rule selector, one precondition engine, one
   repository snapshot.** Schema 2 everywhere; `_recommend` delegates to
   `select_rule`; `plan_transition` runs the contract's `transition` gates
   instead of its own hard-coded copy; a single validation-and-scope loader
   and a single validator invoker with one isolation policy shared by
   `doctor`, `preflight`, `focus`, `check`, `transition`, `capture`, and
   `prepare`. Preserved: `result_sha256` and fail-closed transitions, now
   single-sourced so that `transition` and `check` cannot disagree.

5. **Stop mirroring Python in JSON and consolidate primitives.** Remove the
   five checksum-only JSON contracts and the `agentic_operations` tuple check;
   collapse eight atomic writers, seven front-matter parsers, six Git
   wrappers, and five canonical-JSON implementations into `integrity.py`,
   `front_matter.py`, and `json_bytes.py`; derive the managed-path lists from
   `template_files()`; make the lock the single carrier of `tool_version`.
   Preserved: determinism improves, because divergent timeouts, BOM rules,
   and isolation policies are silent behaviour differences today.

## Two caveats on the ranking

P0-1 to P0-4 are cheap relative to their weight; P0-5 is the expensive one and
is a decision before it is work. Several deletions touch verified
specifications (SPEC-LRE-001 rule 11, ADR-REB-009's five operations,
SPEC-REB-002 rule 14, the REV binding of the manifest digest). Under this
repository's own rules those are amendment work orders, so the cost is
governance sequencing rather than code.

## Know what is authoritative

This note observes and recommends. Formal artifacts under `docs/engineering/`
and the accountable owners named in `DECISION_RIGHTS.md` decide. If this note
and an approved artifact disagree, the artifact governs and the note is the
thing to correct.
