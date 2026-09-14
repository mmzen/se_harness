# What the tests should protect

Tests should catch a broken user action or a real packaging or file-safety failure.
A helper rename, a different local variable or a moved internal function should
not require updating an expected list of source names.

WO-KIS-007 removes the internal module/function inventories, source-spelling
checks and function-object identity assertions covered by K32. Public CLI entry
points still run. The package and repository build tools remain independent;
one import-boundary check covers that packaging constraint. Tests also retain
the useful performance requirement that a command does not repeat validation.

For K33, small byte examples check LF/CRLF equivalence. One real Git checkout
uses the normal setting for the running OS: `true` on Windows, `input` elsewhere.
It checks raw historical evidence, canonical lock identity and the resulting
doctor assessment. The three-setting clone matrix and aggressive Git garbage
collection are gone. The separate Git attributes override test remains because
it exercises a different supported input.

For K34, tests use a real external Python environment and a real directory link
(a junction on Windows). They check the selected entry point and actual imported
package origin. One unavailable-path-resolution case checks a useful failure;
missing paths, checkout origins and paths outside the selected environment still
fail. WO-KIS-003 already removed the original eight-capability interpreter
matrix. This work removes the remaining eight-code fabricated identity-failure
loop and retains one wrong-origin propagation check.

The existing Linux source job runs the full suite. A small step in the existing
Windows upgrade job runs the real checkout and interpreter-path tests. Existing
Linux/Windows wheel installation checks remain. There is no new job or platform
matrix. Raw results follow the [evidence retention policy](evidence-retention.md).

Atomic-write failures still preserve the old file. Unsafe destinations, changed
evidence, wrong checker versions and wrong package origins remain tested.
Historical specifications and bound evidence keep their original bytes;
[SPEC-KIS-001](../engineering/harness-simplification/specifications/SPEC-KIS-001.md)
states the replacements that apply to current development.
