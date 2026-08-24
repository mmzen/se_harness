+++
id = "WO-HBI-004"
type = "work_order"
title = "Declare byte-exact surfaces by tree, and derive the guard's inventory from the tracked set"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "This changes which bytes a Windows checkout presents for the closed phase-3 skill templates, and it replaces the mechanism `WO-HBI-003` used to decide that set. The release orchestrator qualifies the candidate inside a `git worktree` that inherits those bytes, so the change alters what qualification reads on one runner type. `WO-HBI-003` was verified against three per-extension patterns and its guard still passed while a fourth extension inside the same tree stayed converted; a wrong inventory here would reproduce exactly that outcome, so verification must bind the exact candidate commit rather than the branch."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".gitattributes",
  "docs/engineering/hash-bound-integrity/",
  "tests/test_hash_bound_integrity.py",
  "tests/test_agentic_execution.py",
]

[relations]
implements = ["REQ-HBI-001"]
specifications = ["SPEC-HBI-001"]
architecture = ["ARCH-HBI-001", "ADR-HBI-001"]
verification = ["VER-HBI-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T19:32:00Z"
decided_by = "engineering-owner"
reason = "Owner decision recorded 2026-08-24 over three measured options, selecting: 'New small work order: add the *.yaml byte rule to the owner region, and change ByteExactSurfaceTests to derive its inventory from the suite's byte-exact assertions rather than from the declared patterns, so this class cannot recur on the next new extension. Own branch, own PR, own trailer.' The same turn selected 'Same work order' for the reserved-name test-portability defect and 'Stack the fix before #138' for sequencing. Authorizes bounded local implementation, local qualification, one branch and one pull request."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T19:33:00Z"
decided_by = "engineering-owner"
reason = "The same decision authorized an immediate start, because pull request #138's Windows rehearsal job stays red until this work order merges and the owner chose to stack this fix before it."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T20:05:00Z"
decided_by = "engineering-owner"
reason = "In-scope implementation complete and locally qualified on 2026-08-24 in a `git worktree add` checkout with `core.autocrlf=true`: the full suite passes at 811 tests where the same construction at `ee8aea1` fails three, and `ByteExactSurfaceTests` fails eight assertions when the tree rule is replaced by `WO-HBI-003`'s three per-extension rules — a state the previous guard reported `OK` for. Evidence retained under this domain. Verification, VREC preparation, merge, release and publication remain separately unauthorized."
+++

# Work Order: Declare byte-exact surfaces by tree, and derive the guard's inventory from the tracked set

## Lifecycle and authorization

Approved and started on 2026-08-24 on one owner decision, recorded in the
lifecycle events above. Three questions were put together and answered in one
turn: how to fix the uncovered byte-exact surface, what to do about the
reserved-name test-portability defect, and how to sequence the fix against pull
request #138.

That decision authorizes bounded local implementation, local qualification, one
implementation branch and one pull request declaring
`Harness-Work-Order: WO-HBI-004`. Merge, `VREC` preparation or transition, tag,
release, publication, deployment, credential use, maintenance mutation and
governor adoption each remain separately unauthorized.

## What was found, and by what

`WO-HBI-003` declared seven owner-region byte rules on 2026-08-24 and merged as
pull request #141. Three of them were per-extension patterns under the closed
phase-3 skill templates: `*.json`, `*.md` and `*.py`.

`WO-HBI-003` branched from `fc97103` at 17:16:36 local. Pull request #143 landed
`284b842` at 20:19:53, twenty-three minutes before #141 merged at 20:42:13, and
added `templates/repository/standard/.agents/skills/*/agents/openai.yaml` in three
skills together with a byte-exact assertion on their bytes at
`tests/test_agentic_execution.py:143`. The paths are disjoint, so nothing
conflicted and no check fired.

Two mechanisms failed together:

- No rule covered `*.yaml`, so those three paths resolve no attribute and a
  `core.autocrlf=true` checkout materializes them as CRLF.
- `ByteExactSurfaceTests` derived its inventory from the declared patterns, so it
  asserted that each declared pattern is alive and effective and had nothing to say
  about a file no pattern matched. An extension list cannot report a file it does
  not match.

`WO-RLO-005`'s publication-rehearsal lane measured the consequence on hosted
runners: its `windows-2022` leg failed `candidate-unit-suite` with four failures,
three of them these paths. Reproduced locally in a `git worktree add` checkout at
`ee8aea1` — the orchestrator's own construction, which inherits
`core.autocrlf=true` — as 807 tests with 3 failures.

The second failure that leg reported is unrelated to line endings and is fixed
here under the same decision.
`test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths` writes
`NUL.txt` and asserts `SKM003`. On this workstation that write produces a real
enumerable file and the assertion is reached; on `windows-2022` the reserved device
basename resolves to the device, the write succeeds, nothing is left to enumerate,
and the assertion cannot be reached. It is the red `WO-HBI-003`'s evidence recorded
as unexplained.

## Objective

Make a byte-exact surface's coverage independent of its file extension, and make
the guard's inventory independent of the rules it is checking, so that a new file
inside an asserted tree is covered without a new rule and an uncovered one is a
failing test rather than a hosted-only surprise. Separately, make the reserved-name
refusal `VER-AEX-001` requires assertable on every platform.

## Relationship to `REQ-HBI-001`, stated exactly

`REQ-HBI-001` triggers on a committed text file whose bytes are bound by a recorded
SHA-256. None of the three `agents/openai.yaml` paths meets that trigger:
`build_skill_manifest` normalizes line endings before hashing, so the recorded
portable-core vectors in
`tests/fixtures/agentic_execution/phase3/portable_vectors.json` are newline-
insensitive and match on a CRLF checkout. That was measured, not assumed — the
vector test passed on the hosted Windows leg while the byte-exact assertion beside
it failed.

These paths are therefore in scope through this domain's `README.md` scope
boundary, which `WO-HBI-003` widened on 2026-08-24 with the owner's `Accept both`
to admit "committed files whose exact bytes the candidate suite compares without a
recorded digest binding them". No further widening is needed and none is made.

The two individually named `REQ-HBI-001` surfaces `WO-HBI-003` declared —
`release/build-recipe.json` and `release/build-toolchain.lock` — are unchanged in
spelling, in effect and in inventory membership.

## Two disclosed deviations from the approved framing

The framing the owner decided over said `*.yaml` rule, and said the inventory
should derive from the suite's byte-exact assertions. Implementation departed from
both, in the same direction, and neither departure is absorbed silently.

**A tree rule instead of a `*.yaml` rule.** A fourth per-extension rule removes
this instance and leaves the mechanism intact; the fifth extension would reproduce
it. The rule declared is
`templates/repository/standard/.agents/skills/** text eol=lf`, which subsumes the
three it replaces and the `*.yaml` the framing named. Measured before writing it: in
a probe repository the pattern selects every depth and every extension inside that
tree, including an unseen extension four directories down, and selects nothing
outside it. It changes no blob; every file in the tree is already `i/lf`.

**A tracked-set inventory instead of an assertion-derived one.** Deriving the
inventory from the suite's assertions means resolving the path expression in each
byte-exact assertion. The assertion that caused this defect is
`(root / "agents/openai.yaml").read_bytes()` inside a loop over `PHASE3_ROOTS`, so
its path is not statically resolvable, and a source scan that guessed at it would be
a fragile guard that fails for reasons unrelated to bytes. The inventory declared is
instead the tracked set: named files plus every tracked path under a declared tree.
That closes the measured defect class — a new extension inside an asserted tree —
and does not close a byte-exact assertion on a wholly new tree. That residual is
stated in `VER-HBI-001`'s amendment and in this work order's evidence, together with
the detector that does cover it: the full suite run in a `core.autocrlf=true`
checkout.

## In scope

- Replace the three per-extension rules in the owner-controlled region of
  `.gitattributes` with one tree rule, with a comment recording why.
- Change `ByteExactSurfaceTests` in `tests/test_hash_bound_integrity.py` to derive
  its inventory from the tracked set: `BYTE_EXACT_FILES` for named paths and
  `BYTE_EXACT_TREES` for prefixes, with a test that the inventory holds every
  tracked file under each tree and a test that a novel extension inside a tree
  resolves the rule and checks out unconverted in a fresh `core.autocrlf=true`
  clone.
- Make `test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths`
  assert its own precondition instead of assuming the reserved basename became an
  enumerable file, and add a filesystem-independent assertion of the reserved-name
  refusal, mirroring `AgentContractTests.test_portable_paths_fail_closed`.
- Amend `VER-HBI-001` with the coverage this mechanism change needs.
- Retain work-order-keyed implementation evidence under this domain's `evidence/`.
- Commit on one branch and open one pull request declaring
  `Harness-Work-Order: WO-HBI-004`.

## Out of scope

- Any product source file. `se_harness/skill_contract.py` is correct: it refuses a
  reserved component wherever one can be enumerated. The defect is in the test's
  precondition, not in the refusal.
- Adding, removing or changing a hash-bound class, the declaration data, the class
  resolver, the attribute prober, the three `doctor` checks, and every hash mode.
- Moving `build_recipe_sha256` out of `unbound_digest_fields`. That question stays
  open and is tracked as repository issue 142.
- Widening this domain's `README.md` scope boundary. It already admits these
  surfaces.
- Declaring a byte rule for `templates/repository/standard/.claude/skills/`.
  Measured: the suite reads those files with `read_text` and substring assertions,
  not byte for byte, and they pass converted. A rule there would exceed the
  inventory.
- Editing `.github/workflows/publish-pypi.yml`, the managed region of
  `.gitattributes`, the canonical template fragment, root managed files,
  `.engineering-harness.lock` and `.engineering-harness.toml`.
- Any change to `WO-RLO-005`, its packet or its branch. The sequencing decision
  merges this work order first; re-merging `main` into that branch and re-running its
  rehearsal is that work order's act, under its own authorization.
- Rewriting or repointing any recorded digest, `VREC`, `RLS`, `REL` or evidence
  fact, and converting any committed file's bytes.
- Preparing a `VREC`, merging, tagging, releasing, publishing, deploying, or any
  credential-bearing operation.

## Authorized decision envelope

Implementation may choose the tree-rule spelling that selects the intended paths,
the placement and comment wording within the owner-controlled region, the constant
and test names, how the inventory is expressed, and the representative reserved
components asserted.

It may not add a rule for a tree outside the inventory above, weaken a rule to
`text=auto`, declare a rule in the managed region, change any committed file's
bytes, change a declared hash-bound class, change product source, or edit a file
outside the execution scope. If the tree rule turns out to change a blob rather than
only a checkout, stop rather than proceeding.

## Constraints

- Python 3.11+ standard library only; the guard resolves attributes through
  `se_harness.hash_bound`, not through a second implementation.
- The rule must be effective from versioned repository content. A local
  `core.autocrlf`, a global attributes file or `.git/info/attributes` does not
  satisfy this work order.
- The guard must be green before its change is committed. `committed_attributes`
  reads `HEAD` and lags an edited rule by one commit, so the new negative test reads
  the working tree instead.
- The managed `.gitattributes` block must still match its recorded digest, and
  `doctor` must report `managed:.gitattributes: unchanged`.
- Qualify in a checkout with `core.autocrlf=true`, created with `git worktree add`
  so it reproduces the orchestrator's construction. A green suite on an LF checkout
  proves nothing here.
- Run the governing evaluator — released `se-harness==0.6.0` — from outside the
  checkout for validation and preflight.
- Preserve all unrelated changes and owner content outside managed markers.
</content>
</invoke>
