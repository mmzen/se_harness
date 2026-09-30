# WO-IAR-026 cleanup review

The six reviewed stock pointers were removed after all byte, consumer and native
delivery prechecks passed. The only executable change updates the catalog test
to require their absence and resolve current guides. Supported old-release
fixtures, renderers and adapters remain unchanged.

## Assessment against VER-IAR-018

| Case | Result and evidence |
| --- | --- |
| Exact stock inputs | Pass: stock-review.json binds all six raw hashes and public 0.19.0 fixture provenance. Normalization is used only to establish stock content, never to replace approved deletion hashes. |
| Safe all-file boundary | Pass: all targets were checked as regular files inside the exact repository before any unlink; every hash rechecked before deletion. Missing evidence or a mismatch stops the transient executor. No new deletion engine. |
| Active consumers and delivery | Pass on the recorded Windows surfaces: consumers.json and native-delivery.json. Codex and Claude startup and manual compaction succeed before and after removal. Prior verified VREC-IAR-015 remains unchanged. |
| Preservation | Pass: preservation.json compares every previously tracked file. Only six removals and the catalog test differ. Owner files, root, lock, machine policy, current collection, formal history and fixtures retain exact bytes. |
| Installer reconciliation | Pass: selected released 0.20.0 preview and apply report every planned file unchanged. Repeat preview is unchanged; no pointer reappears; doctor passes. See checks.json. |
| Regression and refusal boundaries | Pass: 67 affected tests and the full suite (1,162 tests; 17 skips) cover supported migration, unsafe destinations, customized owner content and retry. Distribution validation and CLI smoke pass. See full-tests.txt and checks.json. |
| Formal consistency and handoff | Pass: artifact validation, released review preflight and Git-derived handoff pass; generated handoff.json retains the complete change set and gate results. |
| Exact candidate | Capture must rerun the full automated suite and checks in the clean committed candidate. VREC-IAR-016 records that separate result and evidence digests. |

## Review findings

The prior catalog assertion depended on a retired pointer. It now checks the
absence of all six files and current catalog, definition-link and work/evidence
destinations. Existing authority and legacy-fixture assertions remain intact.
No product logic, host settings, package versions or additional mechanism changed.

GLOSSARY.md has two stale parenthetical guide names and an outdated role
description. This owner seed is not a required read on the current instruction
route. Its correction is an independent documentation observation outside this
approved scope; the file was preserved. Historical records and dated assessments
also retain old names as evidence, not current read instructions.

## Limits and retained failures

Claude's saved default model was unavailable. The native hook delivered the
correct root even on that failed attempt. Retained retries passed with the
session-only --model opus override. No host or plugin upgrade occurred.
Codex checks use its actual-profile app-server; they do not prove delivery to
the current desktop chat, whose directory is outside the selected repository.
Local Windows checks do not establish hosted Windows/Linux CI. CI is still an
integration prerequisite. Capture preparation is not human verification.
