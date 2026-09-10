# WO-DST-027 verification evidence

Retained under `VER-DST-028` for the issue #433 managed-template leftovers.
Measurements were taken on Windows 11 on 2026-09-10, on the branch
`wo/dst-027-managed-templates` in the worktree
`C:/Users/hok/repos/se_harness_dst027`, whose base is `main` at `f36c8bf1`
(the merge of #437). The governing evaluator is released 0.17.0 installed
from the wheel file in `C:/Users/hok/se-harness-eval-0170`, run with `-I`
from outside the checkout. The hosted Linux lane is the record for the
suite; the Windows readings below are the local control, labelled as such.

## Authorization

- 2026-09-10: the owner approved `REQ-DST-076`, `REQ-DST-077`,
  `SPEC-DST-028`, `VER-DST-028` and `WO-DST-027` by selecting the presented
  option "Approve both packets (Recommended)" (PR #437, merged by the owner).
- Start, completion and record preparation are the delegated executor's
  under `[delegation] class = "execution"`, each taken while the required
  `validate` check is `success` for the head, read at the base of the pull
  request (#440).

## The rule before and after

Before (`main` at `f36c8bf1`, template lines 121 to 124; the root copy is
identical):

    `TRC-008` - `ARCH.constrains` is compatibility-only. A validator MAY classify
    an unambiguous completed historical relation and MUST report the migration. It
    MUST reject a mixed or ambiguous target set. Installation and upgrade MUST NOT
    rewrite repository-owned artifacts.

After (template only):

    `TRC-008` - `ARCH.constrains` is retired. A validator MUST refuse every
    `constrains` relation with `E016`, whatever the architecture's status; it
    classifies no historical relation and reports no migration. `ARCH.addresses`
    and `ARCH.conforms_to` are the only form. Installation and upgrade MUST NOT
    rewrite repository-owned artifacts.

`grep -rn constrains templates/repository/standard/docs/engineering/TRACEABILITY.md`
returns the two lines of this rule and nothing else; `compatibility-only`,
`MAY classify` and `report the migration` are absent from the file
(DST-TPL-001, DST-TPL-002). The diff of the template against `main` is this
paragraph and no other line (DST-TPL-003).

## The template guidance

Before, the file ended with the bare heading `## Completion report format`.
After:

    ## Completion report format

    State what the report carries. The completion decision follows from the
    front matter, not from this section: it is the engineering owner's, or the
    `delegated-executor`'s under `[delegation] class = "execution"` while the
    required pull-request check is `success`.

The diff of the template against `main` is this paragraph (DST-TPL-004).

## The note before and after

Before (`docs/notes/harness-uml-model.md`):

    Older completed artifacts may still carry the compatibility-era
    `constrains` relation. New authoring uses `addresses` and `conforms_to`.
    Historical records are not rewritten to modernize their words.

After:

    The compatibility-era `constrains` relation is retired: the validator refuses
    it with `E016`, and every architecture declares `addresses` and `conforms_to`.
    Historical records are not otherwise rewritten to modernize their words.

(DST-TPL-005.)

## The parity test

`tests/test_artifact_catalog.py`,
`test_released_policy_copies_match_with_declared_candidate_exceptions`:
after reading each pair it declares the two candidate changes. For the
work-order template it asserts the guidance paragraph is present in the
candidate and strips it when the released root lacks it; for the
traceability policy it asserts the retired rule is present in the candidate
and substitutes the compatibility-only rule when the released root carries
that reading. The existing branches then compare as before. Under this
repository's 0.17.0 root both substitutions apply and the test passes; a
root carrying both changes leaves the candidate untouched and takes the
existing equality branches (DST-TPL-006).

## The pins

`tests/test_managed_template_texts.py` (new, DST-TPL-007):

| Test | Rule | Reading |
| --- | --- | --- |
| `RetiredRelationRuleTests.test_the_rule_names_the_relation_retired_and_refused` | DST-TPL-001 | ok |
| `RetiredRelationRuleTests.test_the_rule_names_the_typed_pair_and_promises_no_migration` | DST-TPL-002 | ok |
| `RetiredRelationRuleTests.test_the_rule_keeps_its_installation_sentence_and_its_neighbours` | DST-TPL-003 | ok |
| `CompletionDeciderGuidanceTests.test_the_heading_carries_guidance_naming_both_deciders` | DST-TPL-004 | ok |
| `CompletionDeciderGuidanceTests.test_the_guidance_gives_completion_to_no_single_decider` | DST-TPL-004 | ok |
| `UmlNoteTests.test_the_note_says_the_relation_is_retired_and_refused` | DST-TPL-005 | ok |
| `DraftedWorkOrderTests.test_a_drafted_work_order_carries_the_guidance_and_no_copied_sentence` | scenario B | ok |

`python -m unittest tests.test_managed_template_texts -v`: 7 tests, OK.
`python -m unittest tests.test_artifact_catalog`: OK.

## Scenarios

Scenario A, the shipped rule: covered by the three `RetiredRelationRuleTests`
above on the template text.

Scenario B, the drafted work order: `DraftedWorkOrderTests` initializes a
scratch repository from the candidate, scaffolds a domain, creates
`WO-SCR-001` with `create-artifact`, and reads the drafted file: the
section under "Completion report format" names the engineering owner and
the `delegated-executor`, and the sentence "the completion decision is the
engineering owner's" is absent. The test runs through the suite's
`patch_mutation_authority` and `invoke` helpers because the candidate CLI
from the source tree refuses writes (`MG005`) and the released evaluator
refuses a candidate-initialized target (`RID002`, `RID021`); a plain
`python -m se_harness init` from the candidate into
`C:/Users/hok/se-harness-scratch/dst027-scenario-b/target` did succeed and
installed the template with the guidance (41 files).

Scenario C, parity under the released root: the parity test passes on this
checkout by the declared-exception branch, both substitutions applied.

## Inspections

- Issue #433 acceptance 1: the grep names the relation retired and refused;
  see "The rule before and after".
- Issue #433 acceptance 3: the drafted work order of scenario B carries no
  sentence giving completion to the engineering owner.
- Root (DST-TPL-008): `git diff origin/main --stat` over
  `docs/engineering/TRACEABILITY.md`, `docs/engineering/templates/`,
  `.engineering-harness.lock`, `.engineering-harness.toml` and
  `ENGINEERING_HARNESS.md` is empty; no existing work order is in the change
  set.

## Evaluator readings

| Command | Reading |
| --- | --- |
| `validate .` | PASS; 1,485 artifacts, 0 errors, 46 warnings (all `W013`), 0 advisories |
| `doctor .` | 99 `PASS`, no `FAIL` |
| `preflight . --work-order WO-DST-027` | PASS, phase `start`, `WO-DST-027` `in_progress`, commit-bound verification `required` |

## Test files changed

- `tests/test_artifact_catalog.py` (two declared exceptions)
- `tests/test_managed_template_texts.py` (new)

## Local suite (control)

`python scripts/run_tests.py --workers 4` on Windows 11 with Python 3.13, in
the worktree at `8b68d8ab`: 1,132 tests, 1 error, 23 skipped. The error is
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
the Windows baseline PermissionError on a temporary `.git` object. The
hosted Linux lane at the completion head is the record.

## Adoption obligation carried forward

`DST-TPL-009`: the root-adoption work order of the carrying release takes
the rewritten `TRC-008` into `docs/engineering/TRACEABILITY.md` and the
guidance into `docs/engineering/templates/WORK_ORDER.template.md`; the
parity test then takes its equality branches.
