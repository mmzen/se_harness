# WO-HBI-001 Verification Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation and local-qualification
evidence. This file does not approve an artifact, authorize a diff, verify work,
release, publish, deploy, or authorize `WO-HBI-002`. It records what was measured
on one Windows workstation at one candidate state.

Work order: `WO-HBI-001`, assurance classification `commit_bound_verification =
"required"` decided by the engineering owner. Because verification must bind an
exact candidate commit, the figures below describe the working tree that became
the candidate commit; a later `VREC` is a separate, separately authorized act and
is not prepared here.

## Environment

| Item | Value |
|---|---|
| Platform | `Windows-11-10.0.26200-SP0` |
| Python | 3.14.6 |
| Git | 2.45.1.windows.1 |
| Checkout | `C:\Users\mathi\se_harness_explore_921` |
| Branch | `proposal/rca-060-02-hash-bound-integrity` |
| Base commit | `2f73a0f10b21ace456fbecfec4e8eed5bcbb194d` (the governing packet) |
| `core.autocrlf` in the checkout | `true` |
| Governing evaluator | released `se-harness==0.6.0` in `C:\Users\mathi\se_harness_eval_060`, outside the checkout |

Linux was not exercised. Only the Windows lane is measured here; the Linux lane
is a hosted check that runs only after separately authorized pull-request
creation, and no such authority was given.

## Released-evaluator identity

`.engineering-harness.toml` records `tool_version = "0.6.0"`, so `0.6.0` is the
governing version. The evaluator wheel was installed from a local direct
reference so PEP 610 records its archive digest:

```text
{"archive_info": {"hash": "sha256=2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7",
 "hashes": {"sha256": "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"}},
 "url": "file:///C:/Users/mathi/eval_wheel_060/se_harness-0.6.0-py3-none-any.whl"}
```

`.engineering-harness.lock` records `evaluator.archive_sha256 =
"2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"` and
`evaluator.payload_sha256 =
"c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42"`. Both match
the installed distribution exactly.

```text
python -I -m se_harness identity --role released-evaluator --expected-version 0.6.0
  --expected-root C:/Users/mathi/se_harness_eval_060 --checkout-root .
  --entry-point C:/Users/mathi/se_harness_eval_060/Scripts/harnessctl.exe
  --evaluator-wheel-sha256 2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7
  --evaluator-payload-sha256 c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42
  --require-isolated-python --require-entry-point
```

Result: `passed = true`, `diagnostics = []`, schema
`se-harness-runtime-identity-v3`. Module, distribution, template, entry-point and
interpreter origins all resolved inside the evaluator environment and outside the
checkout; `isolated_python` true, `pythonpath_present` false, `user_site_enabled`
false.

One earlier read-only identity attempt passed the package directory rather than
the environment root as `--expected-root` and reported `RID003` and `RID004`. It
was an argument error on my side, changed nothing, and is recorded so the
transcript is not mistaken for a boundary finding.

## Preflight

- Start preflight, run after the owner's approval and before implementation:
  `PASS`, phase `start`, `WO-HBI-001 (approved)`, 17-item reading manifest,
  `Commit-bound verification: required`.
- Review preflight, run after implementation and before the lifecycle
  transition: `harnessctl preflight . --work-order WO-HBI-001 --phase review` →
  `PASS`, phase `review`, `WO-HBI-001 (in_progress)`, 16-item reading manifest,
  exit 0.
- Review preflight re-run with the governing `0.6.0` evaluator after the
  transition: `PASS`, phase `review`, `WO-HBI-001 (implemented)`, same assurance
  classification `required` decided by `engineering-owner`.

## RC-060-02 reproduction

The incident is reproduced on this checkout without changing anything:

| Measurement | Value |
|---|---|
| `.engineering-harness.lock` committed blob size | 6,184 bytes |
| Committed blob SHA-256 | `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79` |
| Worktree size under `core.autocrlf=true` | 6,343 bytes |
| Worktree raw SHA-256 | `978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e` |
| Carriage returns in the worktree copy | 159 |
| `utf8-text-lf-v1` digest of the worktree copy | `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79` |

The raw digests differ; the canonical digest of the worktree copy equals the
committed blob digest. That is exactly the failure `standard-lock`'s declared
`utf8-text-lf-v1` mode addresses, and exactly why no `raw` class may rely on a
checkout configuration.

## Declared classes

| Class | Mode | Region | Required attribute | Patterns | Bindings |
|---|---|---|---|---|---|
| `evaluator-evidence` | `raw` | `template` | `text eol=lf` | `docs/engineering/**/evidence/*.json` | `evaluator_evidence_sha256`, `preparation_view_evidence_sha256` |
| `governance-migration-protocol` | `raw` | `repository` | `text eol=lf` | `se_harness/governance_migration*.py`, `se_harness/governance_migration_contract.json`, `tests/fixtures/governance_migration/*.json` | `implementation_sha256` |
| `standard-lock` | `utf8-text-lf-v1` | `template` | none | `.engineering-harness.lock` | `from_lock_sha256`, `prior_lock_sha256` |

These are exactly the three classes `SPEC-HBI-001` rule 2 fixes. No class was
added, removed, renamed, or had its mode or required attribute changed.

## Derived hash-bound inventory

The inventory is derived independently of the declaration, from `*_sha256` front
matter fields recorded in governed artifacts under `docs/engineering/`. Every
observed field name must be claimed either by a class's `bindings` or by
`unbound_digest_fields` with a stated reason; an unclaimed field fails
`hash-bound-class-declared`. Adding a new hash-bound committed file necessarily
introduces or reuses such a field, which is what makes the check a completeness
detector rather than a restatement of the declaration.

| Digest field | Source | Disposition |
|---|---|---|
| `evaluator_evidence_sha256` | `VREC`/`RLS` records | bound to `evaluator-evidence` |
| `preparation_view_evidence_sha256` | `RLS-SEH-012` | bound to `evaluator-evidence` |
| `from_lock_sha256` | upgrade work orders and records | bound to `standard-lock` |
| `prior_lock_sha256` | `WO-HUP-002` | bound to `standard-lock` |
| `implementation_sha256` | `se_harness/governance_migration_contract.json` | bound to `governance-migration-protocol` |
| `artifact_snapshot_sha256` | dashboard records | unbound: generated manifest, not committed text |
| `checksums_sha256` | release records | unbound: uncommitted release-bundle text |
| `source_manifest_sha256` | release records | unbound: uncommitted release-bundle text |
| `evaluator_archive_sha256` | lock and release records | unbound: binary wheel archive |
| `target_archive_sha256` | upgrade records | unbound: binary wheel archive |
| `wheel_sha256` | release records | unbound: binary wheel archive |
| `sdist_sha256` | release records | unbound: binary source archive |
| `target_payload_sha256` | upgrade records | unbound: installed payload manifest digest, not a committed file |

`implementation_sha256` is the one binding recorded in harness data rather than
in a governed artifact: `se_harness/governance_migration.py` is re-hashed at
runtime by `_implementation_identity` and compared against the contract, raising
`MIG215` on mismatch. The artifact-field scan therefore cannot see it, and
`bindings` is a superset of what the scan reconciles. That was checked directly:
the committed blob digest of `se_harness/governance_migration.py` is
`bcdaf2078e4161b4f18749f48560d9f3045a6cbab10363da9c8ca154179c6231`, equal to the
`implementation_sha256` recorded in
`se_harness/governance_migration_contract.json`.

No hash-bound path was found that the three declared classes cannot cover, so no
pattern was broadened beyond its bindings.

## Covered tracked paths and resolved attributes

`git check-attr text eol` over every tracked path the declaration covers, in this
checkout, changing no configuration:

```text
.engineering-harness.lock                                                       text=unspecified eol=unspecified
docs/engineering/release-0-6-0/evidence/RLS-SEH-009-evaluator.json               text=set eol=lf
docs/engineering/release-0-6-0/evidence/RLS-SEH-012-evaluator.json               text=set eol=lf
docs/engineering/release-0-6-0/evidence/RLS-SEH-012-preparation-view.json        text=set eol=lf
docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-003-evaluator.json text=set eol=lf
docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-004-evaluator.json text=set eol=lf
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json text=set eol=lf
se_harness/governance_migration.py                                              text=set eol=lf
se_harness/governance_migration_contract.json                                   text=set eol=lf
se_harness/governance_migration_contract.py                                     text=set eol=lf
tests/fixtures/governance_migration/historical-0.5.0-to-0.6.0.json              text=set eol=lf
tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json               text=set eol=lf
```

`.engineering-harness.lock` intentionally resolves to no attribute: its declared
mode is canonical and rule 2 gives it no requirement.

Blob-versus-worktree comparison in this checkout, computed by reading the bytes
directly rather than by trusting the implementation: all eleven `raw`-class paths
are byte-identical to their committed blobs with zero carriage returns, and
`.engineering-harness.lock` differs raw (159 CRs) while agreeing canonically.

## Fresh-checkout matrix

Three isolated clones of this repository at `2f73a0f` were made with
`git -c core.autocrlf=<value> clone`, one per value, each with 1,082 tracked
paths. Digests were computed by this evidence pass over bytes read from the clone
and from `git cat-file blob`, never from a value the implementation reported.

| `core.autocrlf` | `evaluator-evidence` (6 paths) | `governance-migration-protocol` (5 paths) | `standard-lock` (1 path) |
|---|---|---|---|
| `true` | bound digest holds | bound digest holds | bound digest holds; worktree 159 CRs, raw `978cebb7824b`, canonical `abcb1fe70b0e` |
| `input` | bound digest holds | bound digest holds | bound digest holds; worktree 0 CRs, raw `abcb1fe70b0e`, canonical `abcb1fe70b0e` |
| `false` | bound digest holds | bound digest holds | bound digest holds; worktree 0 CRs, raw `abcb1fe70b0e`, canonical `abcb1fe70b0e` |

All three checks passed in all three clones with identical details. The `raw`
classes survive a CRLF-defaulting checkout because their committed attribute
overrides the configuration; the canonical class survives because its mode
normalizes line endings.

The test suite additionally runs the same matrix against synthetic repositories
built from this repository's committed `.gitattributes` bytes, so the matrix is
re-run on every future test invocation rather than only once here.

## Named checks on this repository

```text
PASS hash-bound-class-declared: 3 classes cover 12 tracked paths; 8 digest fields declared out of scope
PASS hash-bound-attribute-effective: 2 raw classes effective for 11 tracked paths
PASS hash-bound-mode-consistent: one mode per class: evaluator-evidence=raw, governance-migration-protocol=raw, standard-lock=utf8-text-lf-v1
```

The three lines are emitted in the order `hash-bound-class-declared`,
`hash-bound-attribute-effective`, `hash-bound-mode-consistent`, through the
existing `InstallationCheck` convention and the existing `doctor` exit status. No
new diagnostic code family was introduced.

## Negative cases and their exact failing lines

Each case was constructed in an isolated committed repository and the exact
rendered detail is recorded verbatim.

```text
[attribute absent: the evidence rule removed from both regions]
FAIL hash-bound-attribute-effective: evaluator-evidence: docs/engineering/x/evidence/a.json resolves text=unspecified, eol=unspecified; requires text eol=lf; evaluator-evidence: pattern docs/engineering/**/evidence/*.json is declared in no region; requires the template region

[attribute override: more specific -text]
FAIL hash-bound-attribute-effective: evaluator-evidence: docs/engineering/x/evidence/a.json resolves text=unset, eol=lf; requires text eol=lf

[attribute override: more specific text eol=crlf]
FAIL hash-bound-attribute-effective: evaluator-evidence: docs/engineering/x/evidence/a.json resolves text=set, eol=crlf; requires text eol=lf

[region placement: template class present only in owner content]
FAIL hash-bound-attribute-effective: evaluator-evidence: pattern docs/engineering/**/evidence/*.json is declared in repository; requires the template region

[region placement: repository class present only in the managed block]
FAIL hash-bound-attribute-effective: governance-migration-protocol: pattern se_harness/governance_migration*.py is declared in template; requires the repository region; governance-migration-protocol: pattern se_harness/governance_migration_contract.json is declared in template; requires the repository region; governance-migration-protocol: pattern tests/fixtures/governance_migration/*.json is declared in template; requires the repository region

[unversioned sources only: .git/info/attributes plus core.autocrlf=false plus core.eol=lf]
FAIL hash-bound-attribute-effective: evaluator-evidence: pattern docs/engineering/**/evidence/*.json is declared in no region; requires the template region; governance-migration-protocol: pattern se_harness/governance_migration*.py is declared in no region; requires the repository region; governance-migration-protocol: pattern se_harness/governance_migration_contract.json is declared in no region; requires the repository region (+1 more)

[.gitattributes absent]
FAIL hash-bound-attribute-effective: .gitattributes is absent

[.gitattributes unreadable: invalid UTF-8]
FAIL hash-bound-attribute-effective: cannot read .gitattributes: 'utf-8' codec can't decode byte 0xff in position 29: invalid start byte

[managed markers unbalanced]
FAIL hash-bound-attribute-effective: .gitattributes managed markers are unbalanced

[managed markers duplicated]
FAIL hash-bound-attribute-effective: .gitattributes managed markers are duplicated

[untracked declared path]
FAIL hash-bound-class-declared: governance-migration-protocol: pattern tests/fixtures/governance_migration/*.json matches no tracked path

[new hash-bound digest field recorded in a work order]
FAIL hash-bound-class-declared: docs/engineering/x/WO-XXX-001.md: digest field novel_payload_sha256 resolves to no declared class
```

Additional fail-closed cases asserted by the suite: unavailable Git (`git
executable is unavailable` on both Git-dependent checks), failed attribute
resolution, failed enumeration, unterminated artifact front matter, invalid UTF-8
in an artifact, and every malformed-declaration fixture. In every case the check
is reported as `FAIL`; none is reported as a pass and none carries the word
`warn` or `advisory`. The unversioned-source case confirms rule 7 directly: a
local `core.autocrlf=false`, a local `core.eol=lf` and a full set of rules in
`.git/info/attributes` do not make any class effective.

## Static and architecture checks

- The declaration is data. Its top-level keys are exactly `schema`, `classes`,
  `unbound_digest_fields`; each class entry has exactly the six declared fields;
  no operative leaf string contains an import separator, expression, command
  metacharacter or executable suffix; the file is loaded with `json.loads` and
  never evaluated. Duplicate JSON keys are rejected.
- The three check names are exact and their emission order is asserted directly
  against the rendered `doctor` list.
- No new diagnostic code family: the module contains no identifier matching a
  code shape, and `preflight.py` still raises `PreflightDiagnostic("I001", ...)`
  for every failed check.
- `template`-region parity: `docs/engineering/**/evidence/*.json text eol=lf`
  appears in `templates/repository/standard/gitattributes.fragment` exactly as
  declared. `standard-lock` is `template`-region with no attribute, so it has
  nothing to compare.
- No repository content reaches a shell: every Git call uses a fixed argument
  vector with `shell=False`; the module contains no `shell=True`, `os.system`,
  `os.popen`, `importlib` or `__import__`. Hostile `.gitattributes` content
  including `$(...)`, backticks and quoted `;` separators was assessed with the
  working tree unchanged and nothing executed.
- Unsafe declared pattern shapes (absolute, `..`-bearing, newline-bearing,
  `;`-bearing) are refused by the loader.
- `ADR-REB-003`'s selected mechanism and rejected options are unchanged; this
  work adds assessment only.

## Read-only and determinism proof

- `assess` on this repository twice returns identical results and identical
  details.
- `.gitattributes`, `.engineering-harness.lock` and `.engineering-harness.toml`
  are byte-identical before and after assessment, and `git status --porcelain`
  is unchanged across it.
- A byte-level snapshot of every non-`.git` file in a synthetic repository is
  equal before and after assessment, including the hostile-attribute case.
- Equal-specificity overlap between two classes fails closed rather than
  choosing, and resolution never returns a default: every uncovered path raises.
- Enumerating classes in reverse order does not change any resolution.

## Unchanged state

- Root managed files, the lock and the templates have zero diff:
  `git diff --stat` over `.engineering-harness.toml`,
  `.engineering-harness.lock`, `.gitattributes`, `ENGINEERING_HARNESS.md`,
  `.github/workflows/engineering-harness.yml`, the four managed
  `docs/engineering/` policy documents, `docs/engineering/templates/`,
  `scripts/` and `templates/` is empty.
- No `*_sha256` line changed anywhere in the candidate: the diff contains no
  added or removed line matching a digest field.
- The managed `.gitattributes` block still matches its recorded lock digest:
  recorded `fba4cf22b45939f8c705f2a9c3bd964408b5003d0599993e72735ce865b97e3b`,
  recomputed `fba4cf22b45939f8c705f2a9c3bd964408b5003d0599993e72735ce865b97e3b`.
  This is also asserted by the suite so a later change cannot pass silently.
- No `VREC`, `RLS`, `REL`, `WO` or evidence fact from earlier work was edited.

## Gates

| Gate | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | PASS; 555 tests, 10 skipped |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS; 718 artifacts, 0 errors, 50 maintenance warnings |
| `python scripts/validate_release_distributions.py --root .` | PASS; 1 distribution-bearing record |
| `python -m se_harness --help` | exit 0; `doctor` and `preflight` listed |
| Governing 0.6.0 `validate .` | PASS; 718 artifacts, 0 errors, 50 warnings |
| Governing 0.6.0 `doctor .` | 87 PASS, 0 FAIL, exit 0 |
| Governing 0.6.0 `preflight . --work-order WO-HBI-001 --phase review` | PASS |

The suite grew from 487 tests with 9 skips to 555 with 10 skips: 68 new tests and
one new skip. The new skip is the symbolic-link safety case, which needs a
privilege this workstation does not grant; it is a genuine coverage gap on this
platform, not a passing assertion. Artifact count grew from 708 to 718, the ten
artifacts of this packet. The 50 maintenance warnings are the pre-existing
`W013`/`W014`/`W015` set and are unchanged.

## Doctor before and after

Measured with the candidate CLI in the checkout, before via an isolated clone at
`2f73a0f` and after in the working tree:

| | Before | After |
|---|---|---|
| `PASS` lines | 83 | 86 |
| `FAIL` lines | 4 | 4 |
| `WARN` lines | 21 | 21 |
| exit status | 1 | 1 |

The four failures are identical before and after and are pre-existing
candidate-versus-released skew:

```text
FAIL distribution:.gitattributes: differs from distribution template
FAIL distribution:docs/engineering/WORKFLOW.json: differs from distribution template
FAIL distribution:docs/engineering/WORKFLOW.md: differs from distribution template
FAIL distribution:scripts/validate_engineering_artifacts.py: differs from distribution template
```

That skew is boundary evidence, not authorization to overwrite a root managed
file, and nothing was overwritten. The governing evaluator run from outside the
checkout reports 87 PASS and 0 FAIL, which is the verdict that counts.

### Runtime

`doctor` wall-clock, three samples each: before `1.435 / 1.352 / 1.361` s, after
`1.461 / 1.479 / 1.469` s. The assessment itself measures `0.170 / 0.156 /
0.157` s on this repository, dominated by the front-matter scan of the 718
tracked artifacts plus two Git invocations.

This is a small but real regression of roughly 0.09 s, about six percent, not the
"no measurable regression" `VER-HBI-001` asks for. It is reported rather than
rounded away. Two reductions were already applied after first measurement: the
artifact scan reads a bounded 8 KiB front-matter prefix instead of whole files
and runs over the tracked set rather than the working tree, and the tracked set
and compiled patterns are computed once and shared, which took the assessment
from 0.364 s to 0.157 s. Deciding whether the remaining cost is acceptable, or
whether the scan should read committed blobs in one batched Git call, is an owner
call and is left open.

## Interpretations recorded for owner confirmation

Three points where the specification admitted more than one faithful reading.
Each was resolved conservatively and is flagged rather than buried.

1. **Rendered check order versus the sorted check list.**
   `inspect_installation` ends in `sorted(checks)`, and the required order
   `declared, effective, consistent` is not alphabetical. Rather than change the
   renderer or reorder existing output, the three checks are appended after the
   sorted set, so the rendered order is the specified order and no existing line
   moved. If the owner prefers a globally sorted list, rule 8's ordering clause
   needs amending instead.

2. **Targets that are not Git working trees.**
   Rule 9 makes unavailable Git fail closed, which read literally would make
   `doctor` fail for every consumer installation without a `.git` directory. A
   target that is not a Git working tree has no tracked set to assess, so the
   three checks are omitted there, following the file's existing conditional
   emission convention for `claude-import`. Omission is never a pass. When the
   target *is* a Git working tree and Git or attribute resolution then fails, the
   checks are emitted and fail. A test pins the omission so it cannot drift into
   a silent pass.

3. **A pattern present in both attribute regions.**
   Rule 10 makes a class "present in the wrong region" ineffective, and
   `VER-HBI-001` phrases the case as present *only* in the wrong region.
   Presence in the required region plus a duplicate identical rule in the other
   region is therefore treated as effective, since a duplicate identical rule
   cannot change what Git resolves. Absence from the required region fails,
   whichever region does carry it.

## Forward divergence worth an owner decision

`templates/repository/standard/gitattributes.fragment` in the candidate already
carries the three `governance-migration-protocol` patterns, while
`SPEC-HBI-001` rule 2 declares that class `repository`-region and this
repository's root `.gitattributes` keeps those rules in owner content outside the
managed markers. Nothing in scope has to change: the root managed block belongs
to released `0.6.0`, the class is present in its required region today, and all
three checks pass. But a separately authorized governor upgrade that rewrites the
managed block from that fragment would put those patterns in the `template`
region, and the class's declared region would then need re-assessment. The
divergence is pinned by an assertion rather than left to a skipped test, so a
change to either side fails the suite and forces the question to be answered. No
attribute and no managed fragment was edited.

## CI binding limit

These three checks do not bind this repository's required CI gate. The gate runs
the governing released `0.6.0` evaluator, which has no knowledge of them. They
bind only after a separately authorized governor upgrade adopts a version that
contains them. Until then they are candidate-side assurance, and this evidence
file plus the test suite are the only places they are enforced.

## Lifecycle transition

Planned read-only first with the candidate CLI:

```text
python -m se_harness transition . --set WO-HBI-001=implemented --decision WO-HBI-001=implementer
Workflow transition: PLANNED
Planned 1 explicit lifecycle transition(s); no files were written.
WO-HBI-001 is implemented.
```

The same command with `--apply` from the in-tree candidate CLI is refused, and
the refusal is recorded rather than worked around:

```text
Blocked by
- WEX201: mutation guard MG005 (transition-apply): RID003 module_origin: origin is outside the expected
  runtime root; RID003 template_origin: origin is outside the expected runtime root; RID006 module_origin:
  installed runtime resolves inside the checkout; RID006 template_origin: installed runtime resolves inside
  the checkout; RID007 sys.path: effective import search contains the checkout; RID009 user_site: runtime
  enables user site-packages; RID021 evaluator_payload_sha256: installed payload digest differs from the
  expected evaluator payload; RID022 evaluator_wheel_sha256: installed PEP 610 archive digest differs from
  the expected evaluator wheel
```

That is the mutation guard working as designed: an in-tree candidate runtime may
not mutate governed state. Applied instead with the governing released `0.6.0`
evaluator from outside the checkout, whose identity passes every one of those
checks:

```text
C:/Users/mathi/se_harness_eval_060/Scripts/python -I -m se_harness transition .
  --set WO-HBI-001=implemented --decision WO-HBI-001=implementer --apply --result-schema 2
Outcome: Completed.
Applied 1 explicit lifecycle transition(s) atomically.
WO-HBI-001 is implemented.
Next: prepare verification record.
```

The write is surgical: `status = "in_progress"` became `status = "implemented"`
and one `[[lifecycle_events]]` entry was appended
(`from = "in_progress"`, `to = "implemented"`,
`decided_at = "2026-08-24T09:04:34Z"`, `decided_by = "implementer"`). Nothing
else in the artifact changed and the file remains LF-only. No hand edit of the
status field was needed.

The recommended next step, `capture-verification`, is not taken here: preparing a
`VREC` is a separate authorized act and the assurance decision belongs to the
assurance owner.

## Changed paths

```text
M  docs/engineering/README.md
M  docs/engineering/hash-bound-integrity/architecture/ARCH-HBI-001.md
M  docs/engineering/hash-bound-integrity/architecture/adr/ADR-HBI-001.md
M  docs/engineering/hash-bound-integrity/capabilities/CAP-HBI-001.md
M  docs/engineering/hash-bound-integrity/intent/INT-HBI-001.md
M  docs/engineering/hash-bound-integrity/requirements/REQ-HBI-001.md
M  docs/engineering/hash-bound-integrity/requirements/REQ-HBI-002.md
M  docs/engineering/hash-bound-integrity/specifications/SPEC-HBI-001.md
M  docs/engineering/hash-bound-integrity/verification/VER-HBI-001.md
M  docs/engineering/hash-bound-integrity/work-orders/WO-HBI-001.md
M  pyproject.toml
M  se_harness/preflight.py
A  docs/engineering/hash-bound-integrity/evidence/WO-HBI-001-verification.md
A  se_harness/hash_bound.py
A  se_harness/hash_bound_classes.json
A  tests/fixtures/hash_bound/bound-and-unbound.json
A  tests/fixtures/hash_bound/canonical-with-attribute.json
A  tests/fixtures/hash_bound/duplicate-binding.json
A  tests/fixtures/hash_bound/duplicate-key.json
A  tests/fixtures/hash_bound/overlapping-classes.json
A  tests/fixtures/hash_bound/raw-without-attribute.json
A  tests/fixtures/hash_bound/unknown-class-field.json
A  tests/fixtures/hash_bound/unknown-mode.json
A  tests/test_hash_bound_integrity.py
```

Every path is inside `WO-HBI-001`'s `[execution_scope].paths`. `MANIFEST.in`
already carried `include se_harness/*.json` and needed no change.
`se_harness/cli.py` was listed in the scope only in case check surfacing required
it; it is unchanged, which was the expected outcome. No file outside the scope was
touched. All new files are LF-only: 0 carriage returns in each, verified with
`tr -dc '\r' | wc -c` rather than a `grep` pattern that silently matches every
line.

## Manual assessments still outstanding

`VER-HBI-001` requires three manual acceptances that only their owners can give,
and none is claimed here:

- Security owner acceptance that `standard-lock` moves from raw to canonical
  comparison and that legacy newline recognition, not a rewrite, preserves
  history. That comparison change is `WO-HBI-002`'s surface and is not
  implemented.
- Quality owner review of the independently computed digests, the fresh-checkout
  matrices and the fail-closed evidence above.
- Repository owner acceptance of the CI binding limit stated above.

## Not performed

Deliberately not done, for want of separate authority: commit of this candidate
was made locally on the branch only; no branch push; no pull request; no merge;
no `VREC` or `RLS` preparation, capture or transition; no tag; no publication; no
deployment; no credential use; no promotable distribution build; no governor
adoption or upgrade; no maintenance mutation; no root managed file or lock write;
no `WO-HBI-002` work. `REQ-HBI-002` is unimplemented by design: every
mode-determination and caller change belongs to `WO-HBI-002`, which remains
`draft` and unapproved.
