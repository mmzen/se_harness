# Source README size correction

The source suite at review c7be3ce0e3f28dc19b13691e00bdf2ab93474dde ran
1,346 tests, with one failure and two skips. The root README contained 679
words, above the existing 650-word limit. Downstream package checks were skipped.

WO-RLS-047 shortens only its new release summary to retain the qualification,
open-item, public-evidence and private-service boundaries. The README now has
643 words. Existing onboarding, documentation and identity/link checks pass.
An intermediate local attempt still had 655 words and two sandbox temporary
directory access errors. The corrected run outside that sandbox passes all 47 tests.
The test and its limit are unchanged. Original CI failure and correction results
are retained in [the observations](source-guide-bound-correction.zip).

The binary candidate, archives, staged marketplace and ready RLS bytes are
unchanged. The successful ready-record replay remains applicable to those exact
inputs. The draft delivery plan's documentation hash must use the corrected
source commit before human review; the earlier unreviewed drafts are preserved
outside the repository. New CI must pass before complete-release approval.
