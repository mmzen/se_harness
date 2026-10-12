# Native lifecycle discovery and reporting correction

Existing authority: WO-HAG-009 and WO-HAG-011, both `in_progress`.
Released evaluator 0.22.1 returned `STEP-WO-IMPLEMENT-CHECK` on recovery.
The [round 26 assessment](../../WO-HAG-009/lifecycle26/assessment.md) records the
failures and incomplete qualification that prompted this change.

The correction uses the existing test helper and instruction route:

- Pointer-based tasks name the selected setup skill as the discovery entry.
  Complete-input tasks keep their existing reuse rule.
- Claude's recovery file shows the literal approved shell prefix. It leaves
  `-I` unquoted and rejects unsafe display characters; permissions do not change.
- Result displays retain exact JSON fields and pointers. Failed sub-commands
  appear before successful commands use the display budget. The top-level
  outcome remains visible. No new lifecycle verdict is calculated.
- The lifecycle guide distinguishes source provenance from the retained test
  Git base. It explains the effect of a refused multi-command action.
- The existing mechanical summary records successful visible read metadata.
  It copies no source content and does not reread files. Failed native reads
  remain attempts. Missing capture remains unknown.
- `observations --record` writes one new file under the test work directory and
  returns field pointers. It preserves the existing inline form for compatibility.

This adds no workflow automation, typed lifecycle interface, new dependency or
permission. A pointer alone was insufficient for the failed sub-command and
read-trace cases: the agent had to expand large arrays or reconstruct earlier
reads. Exact field selection and the existing event capture address those costs
without a second policy engine or a separate reporting framework.

Regression tests cover failed final commands after successful commands, exact
pointer equality, malformed/large results, shell-prefix spelling, incomplete
read traces, private-content exclusion and new-file boundaries. Forty focused
tests pass. The first sandboxed attempt could not write ordinary temporary test
files. The retained unrestricted run exposed one test sentinel that matched the
summary's own explanatory text; a unique sentinel corrected that assertion.
Both failed observations are disclosed; no production permission was widened.

Full checks and released scope/preflight results are retained in `checks.zip`
with its inventory. Native qualification of the corrected package is still
pending at this implementation checkpoint. Fresh trials must capture the selected
noncredential settings hashes before and after launch. Previous native results
keep their original candidate and evidence bindings.
