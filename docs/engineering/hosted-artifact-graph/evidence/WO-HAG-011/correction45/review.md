# Review: correct known draft omissions and report saved facts

WO-HAG-011 remains in progress. This correction changes only the existing
hosted-drafts.md reference under its approved instruction scope.

C44's two failed Claude positive cases remain in [their assessment](../focused44-result/assessment.md).
One omitted a supplied evaluator version and stopped, then confused response
metadata and read results with artifact content and accepted mutations. Another
gave contradictory readiness conclusions and invented a required type assertion.

The guidance now distinguishes a missing input from an omission that can be
corrected from confirmed inputs. It requires reviewing the corrected saved
revision, tracing pass conditions to definitions, and reporting one readiness
conclusion with reads and mutations separated. It supplies no test answer,
operation sequence, new required check or automatic content verdict.

This replaces existing paragraphs in the canonical plugin reference rather than
adding another checklist or tool. The file changes from 9709 to 10109
bytes. Existing package/source checks cover packaging; native qualification must
assess whether the revised guidance corrects the observed behavior. No test that
merely asserts the new wording was added.

Source tests, distribution validation, CLI smoke, released validation, scope and
review preflight passed; exact commands and outputs are in checks.zip. Preparation
used process-local Git long-path support and a new temporary directory. Global
settings are unchanged. No native pass is claimed at this preparation commit.

Next: package the exact candidate, verify source/component identities, run the
unchanged missing-input cases, then the required fresh positive sequence. Keep
the Opus4.6 drafting contract separate from Opus5.5 lifecycle qualification.
Efficiency goals are reported separately; they introduce no lifecycle gate.

VREC-HAG-006 and its bound candidate/evidence remain unchanged. That prior
verification covers WO-HAG-009/010 at its recorded candidate; it does not verify
this correction. No merge, release, host update or risk acceptance is granted.
