+++
id = "SPEC-TST-002"
type = "specification"
title = "Wave 4 test-suite hygiene: mixins, shared support modules, one retired-surface table, cited pins"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Every defined test runs once, each fixture need has one shared helper, retired names are asserted absent in one table, and every prose pin names its rule."

[relations]
specifies = ["REQ-TST-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T12:53:14Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all four (Recommended)', given after the wave 4 packet for issue #379 (code health assessment 2026-09-07, section 5 and the wave 4 plan) was presented: one run per test, shared support modules, one retired-surface table, cited pins. Approval of a definition authorizes no work."
+++

# Specification: Wave 4 test-suite hygiene: mixins, shared support modules, one retired-surface table, cited pins

## In plain words

One work order. Mixins replace test inheritance, five support modules
replace copied helpers, one table replaces the tombstones, and un-cited pins
become structural checks.

## Scope

The modules under `tests/` and the suite step of the `candidate-evidence`
lane. The runner, the scale marker and the fixture cache stay under
`SPEC-TST-001`; product code is out of scope. Every rule carries an
identifier a test can cite.

## Terms

- **Re-run.** A test method executed again because a class carrying it is
  subclassed.
- **Support module.** A module under `tests/` without tests of its own that
  test modules import.
- **Tombstone.** An assertion that a retired name, path or command is
  absent.
- **Prose pin.** An assertion that a sentence appears in a note, a router or
  a managed fragment.
- **Cited pin.** A prose pin whose test names the specification rule that
  fixes the wording.

## Rules

**TST-HYG-001.** A class under `tests/` that defines test methods MUST NOT be
subclassed; shared setup MUST live in a mixin or a test-free base class.

**TST-HYG-002.** A suite test MUST assert that the loader's discovered count
equals the number of `test_` methods defined under `tests/`.

**TST-HYG-003.** `tests/artifact_support.py` MUST hold the artifact and chain
helpers of `test_revision_provenance.py`, and no test module MAY import
another test module.

**TST-HYG-004.** `tests/cli_support.py` MUST provide one `invoke` that
captures both streams and converts `SystemExit` to an exit code; every
command-line call in a test MUST go through it.

**TST-HYG-005.** `tests/git_support.py` MUST provide `git(root, *args)`,
decoding UTF-8 with identity by environment and `commit.gpgsign` off, and
`init_repository(root)`; every Git launch in a test MUST go through them.

**TST-HYG-006.** `tests/artifact_support.py` MUST hold one `write` and one
`formal`; no test module MAY define either.

**TST-HYG-007.** `mutation_guard_support.patch_mutation_authority(case)` MUST
replace every inline mutation-authority patch block under `tests/`.

**TST-HYG-008.** `root_identity_support.load_evaluator_module(name)` MUST
replace every by-path module load, and no test module MAY insert into
`sys.path` at import time.

**TST-HYG-009.** One table-driven `tests/test_retired_surface.py` MUST hold
every tombstone, and no other module MAY assert the absence of a name that
exists nowhere.

**TST-HYG-010.** A test MUST NOT read another test module's source as text.

**TST-HYG-011.** A test that reads product source as text MUST name, in its
docstring or its message, the specification rule it pins.

**TST-HYG-012.** A prose pin on `docs/notes/*.md`, a router or a managed
fragment MUST be a cited pin.

**TST-HYG-013.** An un-cited prose pin MUST become a structural check: the
heading exists, the command parses, the link resolves.

**TST-HYG-014.** Every pin a specification cites MUST remain, including the
README budget, the expertise labels and the reference-covers-parser test.

**TST-HYG-015.** The managed-file count per root MUST derive from
`template_files()` and the lock; no test MAY pin a file count as a literal.

**TST-HYG-016.** A test MUST NOT assert the length of a tuple defined in its
own module.

**TST-HYG-017.** Every test module MUST call `unittest.main()` at most once,
inside a final `__main__` guard.

**TST-HYG-018.** A fixture that needs only a fresh standard repository MUST
call `fixture_support.standard_repository` with the default project name; a
test MAY pass another name only to assert on it.

**TST-HYG-019.** The `candidate-evidence` suite step MUST pass a timings path
to the runner and preserve that file across runs.

**TST-HYG-020.** The suite's failure set MUST equal the baseline, and its
wall time on the Linux lane MUST be recorded before and after in the
evidence packet.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| a class subclasses a test-carrying class | the loader-count test fails and names the class (TST-HYG-002) | none |
| a test module imports another test module | the import test fails and names both modules (TST-HYG-003) | none |
| a command-line call or a Git launch bypasses its support module | the reading names the site (TST-HYG-004, TST-HYG-005) | none |
| a tombstone appears outside the table | the reading names the module (TST-HYG-009) | none |
| a prose pin names no rule | review converts it to a structural check or rejects it (TST-HYG-012, TST-HYG-013) | none |
| the failure set differs from the baseline | the work order stops and reports (TST-HYG-020) | none |

## Examples

**Given** the candidate after this change, **when** the loader discovers
`tests/`, **then** the discovered count equals the defined count
(TST-HYG-001, TST-HYG-002).

**Given** a workstation with `commit.gpgsign` enabled globally, **when** the
suite commits inside a fixture, **then** every commit succeeds because the
one Git helper turns signing off (TST-HYG-005).

**Given** a wording change in `docs/notes/harness-overview.md`, **when** the
suite runs, **then** no test fails unless a specification rule fixed that
sentence (TST-HYG-012, TST-HYG-013).

**Given** a root that ships a different managed-file count, **when** the
suite runs, **then** no test table needs an edit (TST-HYG-015).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TST-004` | TST-HYG-001, TST-HYG-002, TST-HYG-003, TST-HYG-004, TST-HYG-005, TST-HYG-006, TST-HYG-007, TST-HYG-008, TST-HYG-009, TST-HYG-010, TST-HYG-011, TST-HYG-012, TST-HYG-013, TST-HYG-014, TST-HYG-015, TST-HYG-016, TST-HYG-017, TST-HYG-018, TST-HYG-019, TST-HYG-020 |

## Not decided here

- Mixins versus deleting inherited tests in `__init_subclass__`, provided
  TST-HYG-001 and TST-HYG-002 hold.
- Helper names beyond those the rules fix, and any split of
  `tests/artifact_support.py`.
- How the timings file persists on the hosted lane: an actions cache or a
  committed derived file.
- Whether `tests/skill_contract_support.py` shrinks to the shipped contract
  versions; a later work order may take it.
- The order of edits and the number of commits.
