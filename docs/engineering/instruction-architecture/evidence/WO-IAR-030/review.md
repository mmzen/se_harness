# Minimal installation implementation progress

## Implemented behavior

Default init selects one external released resource set and writes the config
and lock. Git, CI and PR integrations are explicit. The existing transaction
handles migration, owner preservation, rollback and repeat execution. Migration
recognizes stock bytes from the exact prior wheel, read once into a bounded
snapshot. It requires native delivery evidence before retiring a local entry.
Editable stock resources retire only when selected; customized resources refuse.

Retained integration seeds deleted by their owner stay deleted unless requested
again. A retirement request for a retained integration is refused. Unknown
external integration entries and inappropriate prior-wheel inputs refuse.
Prospective evidence attributes are assessed before the first evidence file.

Packaged setup/upgrade/provider instructions and active public guides describe
the new interface. The source acceptance runner handles both legacy and external
layouts. It explicitly selects a Git integration for the managed-content refusal
scenario, leaving minimal default initialization separately assessed.

## Review and simplicity

Reuse ResourceSet, the old installer transaction, the existing wheel identity
and current test helpers. No new profile, policy registry or overlay is added.
Legacy fixtures are explicit and do not intercept the production CLI. The source
checkout and governing 0.20.0 installation remain separate.

## Observed checks and limitations

- Installer/hash boundaries: 34 tests passed, one Windows symlink skip.
- Resource/procedure/legacy group: 127 tests passed, two skips.
- Distribution validation: passed for 18 distribution-bearing records.
- Exploratory installed-wheel smoke: passed on Windows and Ubuntu WSL, including
  the two-file default, empty validation, explicit Git readiness, stock 0.20.0
  migration preview and unchanged files after missing delivery evidence.
  Linux also exercised a real symlink refusal and customized-seed refusal.
- The stable broad run executed 1201 tests: eight failures, one error, 19 skips.
  Six failing/error cases need the five files proposed under WO-IAR-036. Three
  additional diagnostic-index cases were corrected under WO-IAR-035 and passed
  with the later 36-test focused run. No broad green result is claimed.
- A separate exploratory acceptance-runner invocation was invalid as final
  qualification: its synthetic commit lacked the required checkout context,
  and the handcrafted fixture wheel omitted dashboard assets. Both failures
  are retained. Use the actual build route and exact committed candidate for
  final qualification; do not promote this fixture or its synthetic identity.

These results are progress evidence. The Windows/Linux wheel fixture precedes
the final validator diagnostic adjustment and LF cleanup. Final verification
must use the final committed bytes. No final native delivery is claimed here.

## Integration dependency

The published 0.20.0 acceptance runner unconditionally reads the local
ENGINEERING_HARNESS.md and its lock entry. Minimal init intentionally creates
neither. Changing this candidate's runner cannot update that immutable verifier.
The current CI workflow takes the verifier identity from the selected predecessor.
A separately governed compatible-verifier release and selection is needed before
that lane can accept this layout. Do not bypass the lane or adopt candidate source
as the governing evaluator. No release or CI change is included in this progress.

## Outstanding

WO-IAR-036 approval and implementation, the final full suite, proper packaged
qualification and required native scenarios, complete Git-derived handoff for
the combined work, exact candidate commit, and VREC-IAR-020 capture. Work orders
remain in progress. No push, PR, release or adoption occurred.
