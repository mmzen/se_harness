# Claude release-binding correction

The functional29 Claude run approved a release contract pinned to the imported
fixture commit. Its verified disposable candidate was different. Released 0.22.1
refused release preparation with WEX404. Claude then attempted to revise the
protected contract. The original failures and incomplete result remain at
`../../WO-HAG-009/functional29/assessment.md`.

## Correction

- At contract drafting, distinguish the fixture from the future verified candidate.
  Defer its completion and approval until the final verified candidate is known;
  preserve any actual supplied constraint. Do not use an absent optional field
  to avoid the canonical template's candidate-content requirement.
- At release preparation, compare the selected contract with the final VREC.
- Stop protected-record revisions instead of trying changed content or history.
  A new draft does not replace the accepted record or supply amendment authority.
- Add the exact decision-disposition procedure and make authority prerequisites explicit.

Three plugin Markdown references change. The selected released source confirms
the optional-pin behavior; its exact source fragment and hash are retained.
No runtime, evaluator rule, schema, permissions or accepted criteria change.
This is a functional correction. Performance optimization remains deferred.

## Validation and qualification

Released section selectors resolve. Focused native support tests, the full source
suite, distribution checks, CLI smoke, scope, review preflight and released
validation pass. Exact commands and outputs are in checks.zip.
The initial focused invocation failed because the host sandbox's temporary
directory denied file access. Its output is retained; the rerun used writable
task storage. No product behavior or test criterion changed for this rerun.
The sandboxed full suite also failed on denied atomic hardlinks and loopback
sockets. It is retained alongside the ordinary host rerun in a short disposable
temporary directory. The rerun keeps every test; no assertion was weakened.

Next: package this exact clean candidate and rerun Claude's affected NQ cases
from a fresh private project, without supplied requests or operator mutations.
Retain the prior Codex pass; it does not by itself qualify the changed guidance.
No new native pass, work completion or human verification is claimed here.
