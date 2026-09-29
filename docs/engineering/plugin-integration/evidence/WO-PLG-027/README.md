# Current guidance correction evidence

WO-PLG-027 implements REQ-PLG-040 under SPEC-PLG-023 and VER-PLG-026.
The [file-by-file review](review.json) assesses all 12 selected documents and
both changed test files against MP-03 and MP-06.

## Observed checks

- Focused Windows/Python 3.14.6 suite: **92 tests passed** across onboarding,
  progressive documentation, marketplace composition, package assembly,
  independent identity/link checks and instruction architecture.
- Runnable examples parse against the isolated released **0.19.0** parser,
  invoked through its absolute Python path from outside the checkout.
- Source links and headings resolve. Composed-package links retain their
  separately tested layout from WO-PLG-026.
- Diff whitespace check passes. No managed instruction, accepted definition,
  historical evidence, evaluator selection or real profile was changed.

[Commands and outputs](commands.json) include two failed test runs followed by
the successful run. The first extractor parsed a non-command diagram line;
the second treated successful `--version` termination as an error. Both were
corrected in the approved documentation test file. No failed run is counted as a pass.

## Combined candidate and package evidence

[Package comparison](package-evidence-mapping.json) maps retained native checks
to unchanged assembly inputs and every actual distribution-file digest. The
archive source remains `ce6d5fa4080e2ef0904446aa0b066d907532b63c`. The later combined
VREC binds the clean preparation commit containing both completed work orders,
the reviewed guidance and this retained evidence.

The execution-entry base is `cc6901a215b6f23febb1d918591c0c4ddc6a3d08`; it follows
completed WO-PLG-026. The shared proposal base remains
`c4d9036fdaab378f08fe2db68978126f66ab961e`. No earlier documentation implementation
is excluded. The exact combined diff is checked against the two approved scopes.

## Review and limits

Corrections use the existing guides and test modules. The current route points
to task-specific instructions; historical diagrams and accepted records remain.
The source-development guide preserves the merged five-surface release-delivery
procedure. Released 0.19.0 behavior and unreleased 0.20.0 seed retirement are distinct.

Native qualification limits remain in [WO-PLG-026](../WO-PLG-026/README.md):
Windows CLIs, manual compaction and disposable profiles. Parser success is not
execution or authority. Human verification, public publication, real-profile
adoption and public-route confirmation have not occurred.
