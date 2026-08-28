+++
id = "VER-HBI-001"
type = "verification"
title = "Hash-bound class declaration, checkout-byte and mode-consistency assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-28"

[relations]
verifies = ["REQ-HBI-001", "REQ-HBI-002", "REQ-HBI-003", "REQ-HBI-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "quality-owner"
+++

# Verification Contract: Hash-bound class declaration, checkout-byte and mode-consistency assurance

## Third amendment, 2026-08-28 — accepted

Proposed under `WO-HBI-005` for repository issue #207 and accepted on
2026-08-28 by the accountable owner ("I accept SPEC-HBI-001/VER-HBI-001 and I
approve WO-HBI-005"). The contract below reads with this amendment applied.

Acceptance scenario 7 states that a consumer installation "inherits the
`template` classes and none of this repository's `repository`-region rules".
No case in the matrix derives that expectation from the shipped surface, and
the one test that looked at the fragment
(`test_candidate_fragment_promotion_of_repository_patterns_is_pinned`) pinned
the divergence as known rather than refusing it. Separately, no scenario runs
`doctor` in the state every adopter meets first — installed, committed once,
no `VREC` — so the "untracked declared path" row's fail-closed obligation was
never measured against `evaluator-evidence` in a repository that cannot yet
satisfy it.

The amendment adds four matrix rows and three scenarios, and restates one
row. The `REQ-HBI-001` fail-closed row keeps "untracked declared path" for a
`repository`-region class and gains its complement for a `template`-region
class. Every other pass condition is unchanged; the amendment adds obligation
on the shipped surface and relaxes only the one condition `REQ-HBI-003`
withdraws, and it does so by naming the substitute obligation
(`hash-bound-attribute-effective` on rule presence) in the same row.

## Second amendment, 2026-08-24 — accepted

Amended under `WO-HBI-004`. The first amendment below closed a coverage gap and
introduced a mechanism that carried one of its own: `ByteExactSurfaceTests` derived
its inventory from the declared patterns, so it asserted that every declared pattern
is alive and effective and had nothing to say about a committed file no pattern
matched. Pull request #143 added
`templates/repository/standard/.agents/skills/*/agents/openai.yaml` with a byte-exact
assertion twenty-three minutes before `WO-HBI-003` merged; the guard passed and the
release orchestrator's `windows-2022` candidate qualification failed on three tests.

The amendment moves the inventory's source. It is now the tracked set — named files
plus every tracked path under a declared tree — so coverage no longer depends on a
file's extension. The `REQ-HBI-001` byte-rule-completeness row below is restated
accordingly, one row and one scenario are added, and one property bullet is added.
The amendment adds obligation and relaxes no pass condition: the liveness obligation
on each declared pattern is preserved as a liveness obligation on each named file and
each declared tree, and the effectiveness and non-conversion obligations are
unchanged over a strictly larger inventory. No approved `statement` field changed.

The accountable repository owner decided this amendment's substance on 2026-08-24 by
selecting, over three measured options: "New small work order: add the *.yaml byte
rule to the owner region, and change `ByteExactSurfaceTests` to derive its inventory
from the suite's byte-exact assertions rather than from the declared patterns, so
this class cannot recur on the next new extension. Own branch, own PR, own trailer.
The rule is one line; the guard change is the real work and needs `VER-HBI-001`
coverage for it." Implementation departed from that framing twice, deliberately and
in the same direction — a tree rule rather than a `*.yaml` rule, and a tracked-set
inventory rather than an assertion-derived one — and `WO-HBI-004` discloses both with
the measurements they rest on. Scenario 9 was measured before this text was written,
not after. The acceptance authorizes no verification, merge, release, publication or
deployment.

The reserved-name test-portability defect fixed under the same work order is not
covered here. It is `VER-AEX-001`'s existing security check, "Exercise absolute,
traversal, dot-component, alternate-separator, drive, device, URI, wildcard,
symlink/junction escape, case-collision, reserved-name, control-character, and
invalid-encoding paths", which that fix brings into conformance on every platform
rather than only where a reserved basename can exist as a file. No `VER-AEX-001`
amendment is needed and none is made.

## Amendment, 2026-08-24 — accepted

Amended under `WO-HBI-003`. `WO-RLO-005`'s publication-rehearsal lane executed on
hosted runners for the first time and measured the release orchestrator failing
candidate qualification on `windows-2022`: the orchestrator creates the checkout it
qualifies with `git worktree add`, which inherits `core.autocrlf=true`, and eleven
byte-exact assertions read converted bytes there.

This contract's coverage of `REQ-HBI-001` was complete for declared classes and
silent about committed surfaces the suite compares byte for byte without a recorded
digest binding them. The row, scenario and property added below close that gap. The
amendment adds obligation and relaxes no pass condition; no approved `statement`
field changed.

The accountable repository owner accepted this amendment and the companion scope
widening in this domain's `README.md` on 2026-08-24 through the statement
`Accept both`, taken over the framing: "VER-HBI-001 gains one REQ-HBI-001 matrix row
(byte-rule completeness beyond declared classes), acceptance scenario 8, and one
property bullet. The hash-bound-integrity README scope boundary admits committed
files whose exact bytes the suite compares without a recorded digest binding them,
guarded by a test rather than a doctor check." Scenario 8 was measured before the
decision, not after: removing one owner-region rule and re-materializing the path
fails `ByteExactSurfaceTests` with two assertions, one naming
`se_harness/agent_contract.json is crlf`. The acceptance authorizes no verification,
merge, release, publication or deployment, and the manual acceptances this contract
requires from the security, quality and repository owners remain separate.

## Independence

Assurance selects its own checkout matrices, its own tamper cases and its own
attribute-override cases. It computes SHA-256 over bytes it reads itself and never
over a value the implementation reports. It derives the expected hash-bound
inventory from recorded digest fields in governed artifacts, not from the
declaration under test, so a class missing from the declaration is visible rather
than definitionally absent. Attribute effectiveness is confirmed by reading the
bytes a fresh checkout actually produces, not only by the resolved attribute the
implementation prints.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-HBI-001` | Inventory reconciliation | Recorded digest fields across governed artifacts versus declared classes | Every hash-bound committed path resolves to exactly one class; any unmatched path fails `hash-bound-class-declared` naming it |
| `REQ-HBI-001` | Fresh-checkout matrix | Isolated clone per class per `core.autocrlf` value `true`, `input`, `false` | For each `raw` class the checked-out bytes equal the committed blob and the bound digest matches in all three configurations |
| `REQ-HBI-001` | Attribute-absent case | Declared `raw` class with its attribute removed from both regions | `hash-bound-attribute-effective` fails naming the class and the required value; `doctor` exit status is non-zero |
| `REQ-HBI-001` | Attribute-override case | More specific conflicting `-text` and `eol=crlf` rules over a declared pattern | Check fails naming the class, the resolved attribute and the conflict |
| `REQ-HBI-001` | Unversioned-source negative | Requirement satisfied only via `.git/info/attributes`, global attributes or local `core.autocrlf=false` | Class is still reported ineffective; configuration never satisfies the requirement |
| `REQ-HBI-001` | Region placement | `template` class present only in owner content, and `repository` class present only in the managed block | Each misplacement is reported ineffective |
| `REQ-HBI-001` | Template parity | Candidate `templates/repository/standard/gitattributes.fragment` versus declared `template` classes | Byte-identical for every `template`-region class; a divergence fails a static check |
| `REQ-HBI-001` | Fail-closed matrix | Unreadable `.gitattributes`, unavailable Git, attribute resolution failure, untracked declared path of a `repository`-region class | Every case is a failing named check with the exact reason; none passes and none is advisory |
| `REQ-HBI-003` | Vacuous template class | Git working tree in which a `template`-region class covers no tracked path, with its rule present in the managed region | `hash-bound-class-declared` passes with a detail naming the class and `0 tracked paths`; `doctor` exit status is 0 |
| `REQ-HBI-003` | Vacuous class, rule absent | The same tree with the class's rule removed from the managed region | `hash-bound-attribute-effective` fails naming the class and the missing region; coverage of zero paths does not hide the absence |
| `REQ-HBI-004` | Shipped-surface portability | Every pattern in `se_harness/hash_bound_classes.json` and every rule in `templates/repository/standard/gitattributes.fragment`, enumerated statically | No pattern or rule begins with `se_harness/`, `tests/` or `repository_tools/`; no `repository`-region pattern appears in the fragment; a violation fails naming the pattern and the declaring file |
| `REQ-HBI-004` | Fresh consumer | `harnessctl init` into a temporary directory, `git init`, `add -A`, `commit`, then `doctor`, on an LF checkout and a `core.autocrlf=true` checkout | Exit status 0; all three `hash-bound-*` checks present and passing; on Linux and Windows |
| `REQ-HBI-001` | Byte-rule completeness beyond declared classes | The byte-exact inventory in `tests/test_hash_bound_integrity.py`, derived from the tracked set as named files plus every tracked path under a declared tree, resolved through `se_harness.hash_bound` and cross-read with `git ls-files --eol` | Every named file is tracked, every declared tree holds a tracked file, the inventory holds every tracked path under each declared tree, every inventory path resolves `text` set and `eol=lf`, and none is converted in the working tree; a missing rule fails naming the path and the conversion observed |
| `REQ-HBI-001` | Extension independence of a byte-exact tree | A fresh `core.autocrlf=true` clone of a probe repository carrying this checkout's own `.gitattributes`, holding a file with an unseen extension inside a declared tree and a file outside it | The unseen extension resolves `text` set and `eol=lf` and its checked-out bytes contain no CR, the path outside the tree resolves unspecified, and a per-extension rule set fails this case |
| `REQ-HBI-002` | Mode-divergence detection | One declared class hashed under both modes across callers | Test fails naming the class and both observed modes |
| `REQ-HBI-002` | Lock mode convergence | `upgrade_authorization` and `release_bootstrap` compare a lock digest on LF and CRLF checkouts | Both compute the same canonical digest and reach the same verdict in both checkouts |
| `REQ-HBI-002` | Legacy recognition | `WO-HUP-002`'s recorded `prior_lock_sha256` against canonical-mode comparison | Comparison succeeds through documented newline-variant recognition, reports the legacy match distinctly, and the recorded field is unchanged on disk |
| `REQ-HBI-002` | Encoding cases per class | LF, CRLF, CR, invalid UTF-8, and single-byte tamper | LF, CRLF and CR agree for canonical classes; tamper fails for every class; invalid UTF-8 fails closed with a bounded path-level detail |
| `REQ-HBI-002` | Producer newline cases | Every call site writing committed hash-bound text, exercised on a CRLF-default platform | Written bytes contain no CR; a platform-default write is a failing test |
| Both | Unmodified-behaviour regression | Full suite plus graph, release-surface and `doctor` gates | Existing digests, comparisons, upgrade classification, customization protection and safety checks are unchanged |

## Acceptance scenarios

1. On a fresh Windows clone with `core.autocrlf=true`, all three declared classes
   assess correctly and every evidence digest still matches its bound value.
2. A newly added committed text file whose SHA-256 is recorded in a work order
   makes `hash-bound-class-declared` fail naming that exact path.
3. Removing `docs/engineering/**/evidence/*.json text eol=lf` from the managed
   fragment makes `hash-bound-attribute-effective` fail; restoring it passes.
4. `.engineering-harness.lock` on a CRLF checkout passes all three checks with no
   attribute declared for it and with no worktree byte changed.
5. An evaluator-upgrade authorization that succeeded before the mode change still
   succeeds afterwards, and the report states that a legacy newline variant
   matched.
6. Setting `core.autocrlf=false` locally does not turn any ineffective class into
   an effective one.
7. A consumer installation created from the canonical template inherits the
   `template` classes and none of this repository's `repository`-region rules.
8. On a checkout with `core.autocrlf=true` the full suite passes. Removing any one
   of the owner-region byte rules that `WO-HBI-003` declares makes
   `ByteExactSurfaceTests` fail, naming that path and the `crlf` it observed, and
   restoring it passes.
9. In a checkout created with `git worktree add` and `core.autocrlf=true`, replacing
   the declared tree rule with `WO-HBI-003`'s three per-extension rules and
   re-materializing the tree makes `ByteExactSurfaceTests` fail, naming each
   `agents/openai.yaml` path and the `crlf` it observed and failing the
   extension-independence case; restoring the tree rule passes. A file with an
   extension no rule has ever named, added anywhere inside a declared tree, needs no
   new rule.

10. A repository created by `harnessctl init` and committed once, holding no
   `VREC`, passes `doctor` with exit status 0 on Linux and on Windows, and the
   `hash-bound-class-declared` detail names `evaluator-evidence` with
   `0 tracked paths`.
11. The same repository with the `docs/engineering/**/evidence/*.json` rule
   removed from its managed block fails `hash-bound-attribute-effective`;
   restoring the rule passes.
12. A `repository`-region class whose pattern matches no tracked path still
   fails `hash-bound-class-declared` naming the pattern, and a
   `repository`-region class declared only in the template region still fails
   `hash-bound-attribute-effective` when its pattern does match tracked paths.

## Property and invariant tests

- Assessment is deterministic: identical working tree, tracked set and attribute
  state yield identical check results and identical details.
- Assessment is read-only: no file, lock, index or Git configuration changes, and
  a byte-level before/after comparison of the working tree proves it.
- Exactly one class resolves for any covered path; equal-specificity overlap
  between two classes fails closed rather than choosing.
- Mode resolution is total or errors: it never returns a default.
- For a canonical-mode class, digests over LF, CRLF and CR forms of the same
  content are equal; for a `raw` class they are distinct.
- Ordering independence: enumerating classes or paths in any order does not change
  results.
- No recorded digest field in any governed artifact changes across the whole
  suite.
- Every committed path whose exact bytes the suite compares resolves an effective
  versioned byte rule from repository content, and none is converted in the working
  tree. A declared name or tree that selects no tracked file fails rather than passing
  vacuously.
- The byte-exact inventory is closed under adding a file: a tracked file inside a
  declared tree is in the inventory whatever its extension, so coverage cannot be
  narrower than the tree. The inventory is read from the tracked set, never from the
  rules under test, and the rules are read from the working tree rather than from
  `HEAD`, so an edited rule is assessed in the commit that makes it and not in the
  next one.

## Static and architecture checks

- Trace both requirements through `SPEC-HBI-001`, `ARCH-HBI-001`, `ADR-HBI-001`,
  `WO-HBI-001` and `WO-HBI-002`.
- Assert the declaration contains no import path, expression, shell command or
  named executable, and is loaded as data.
- Assert no hashing caller for a declared class chooses a mode locally.
- Assert the three check names are present, spelled exactly, and emitted in the
  order `hash-bound-class-declared`, `hash-bound-attribute-effective`,
  `hash-bound-mode-consistent`, and that no new diagnostic code family is
  introduced.
- Confirm root managed files and the lock have zero diff, and that the managed
  `.gitattributes` block still matches its recorded digest.
- Confirm `ADR-REB-003`'s selected mechanism and rejected options are unchanged.

## Security and privacy checks

- Exercise symbolic links, junctions, case aliases, path escapes, unsafe
  basenames, duplicate case variants and hostile `.gitattributes` content as
  declared or covered paths; each is refused without executing anything.
- Confirm no repository content reaches a shell and no repository-provided code
  executes during assessment.
- Confirm details are bounded and contain no credentials, tokens, usernames, home
  paths or environment dumps.
- Confirm exact-byte trust is preserved for every `raw` class: no class is
  relaxed to canonical mode to make a check pass.

## Performance and resilience checks

Run the full suite and the assessment on Python 3.11 and the current
qualification runtime. Measure `doctor` runtime before and after on this
repository and confirm no measurable regression. Inject faults during attribute
resolution and mid-enumeration and confirm the run fails closed, leaves the
working tree unchanged, and reports the exact failed predicate.

## Manual assessments

- Security owner accepts that `standard-lock` moves from raw to canonical
  comparison and that legacy recognition, not a rewrite, preserves history.
- Quality owner reviews the independently computed digests, the fresh-checkout
  matrices and the fail-closed evidence.
- Repository owner accepts the stated limit that these checks do not bind this
  repository's required CI gate until a separately authorized governor upgrade.

## Evidence retention

`WO-HBI-001` and `WO-HBI-002` evidence retains: the reproduction of `RC-060-02`
including the committed blob digest and the CRLF worktree digest of
`.engineering-harness.lock`; the derived hash-bound inventory with its source
artifact field for each entry; per-class fresh-checkout results for all three
`core.autocrlf` values with independently computed digests; `git check-attr`
output for every declared pattern; every negative case with its exact failing
check line; before-and-after `doctor` output; full test, graph and
release-surface results; the unchanged state of every recorded digest field; and
the explicit list of actions not performed.

## Residual uncertainty

Git versions outside the supported range may resolve attributes differently, and
that is outside this correction. Checkouts produced by tools other than Git, and
consumer repositories that override the managed fragment after installation,
remain outside the assessed set. Binary and generated content, uncommitted
release-bundle text, and validator-plane enforcement remain out of scope. Whether
the validator plane should also carry this rule is `INT-HBI-001`'s open decision
and is not settled by this contract.

One residual is named exactly, because the second amendment narrowed the gap rather
than closing it. A byte-exact assertion added on a path in no declared tree and in no
named file is still uncovered by `ByteExactSurfaceTests`, which cannot see an
assertion it has no inventory entry for. Deriving the inventory from the assertions
themselves was measured and rejected in `WO-HBI-004`: the assertion that caused this
amendment resolves its path from a loop variable, so no source scan can name it
without guessing. The detector that does cover this residual is the full suite run in
a `core.autocrlf=true` checkout created with `git worktree add`, which is the
orchestrator's own construction and which scenarios 8 and 9 require. It reports the
failure at integration time on the pull request rather than on publication day, and
it is the only mechanism this contract relies on for a surface no rule names.
