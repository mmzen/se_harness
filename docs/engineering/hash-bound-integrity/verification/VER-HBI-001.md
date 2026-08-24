+++
id = "VER-HBI-001"
type = "verification"
title = "Hash-bound class declaration, checkout-byte and mode-consistency assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-HBI-001", "REQ-HBI-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T08:27:00Z"
decided_by = "quality-owner"
+++

# Verification Contract: Hash-bound class declaration, checkout-byte and mode-consistency assurance

## Amendment, 2026-08-24 — pending owner acceptance

Amended under `WO-HBI-003`. `WO-RLO-005`'s publication-rehearsal lane executed on
hosted runners for the first time and measured the release orchestrator failing
candidate qualification on `windows-2022`: the orchestrator creates the checkout it
qualifies with `git worktree add`, which inherits `core.autocrlf=true`, and eleven
byte-exact assertions read converted bytes there.

This contract's coverage of `REQ-HBI-001` was complete for declared classes and
silent about committed surfaces the suite compares byte for byte without a recorded
digest binding them. The row, scenario and property added below close that gap. The
amendment adds obligation and relaxes no pass condition; no approved `statement`
field changed. It awaits the owner's acceptance.


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
| `REQ-HBI-001` | Fail-closed matrix | Unreadable `.gitattributes`, unavailable Git, attribute resolution failure, untracked declared path | Every case is a failing named check with the exact reason; none passes and none is advisory |
| `REQ-HBI-001` | Byte-rule completeness beyond declared classes | Every tracked path selected by the byte-exact inventory in `tests/test_hash_bound_integrity.py`, resolved through `se_harness.hash_bound` and cross-read with `git ls-files --eol` | Every pattern selects at least one tracked file, every selected path resolves `text` set and `eol=lf`, and no selected path is converted in the working tree; a missing rule fails naming the path and the conversion observed |
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
  tree. A declared pattern that selects no tracked file fails rather than passing
  vacuously.

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
