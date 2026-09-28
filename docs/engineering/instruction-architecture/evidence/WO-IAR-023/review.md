# Test correction review

WO-IAR-023 applies the exact reviewed patch in applied.patch. The before/after
digests and passing pre-approval disposable probe remain in
../../proposals/instruction-cleanup/test-correction-review.json.

The catalog test now checks the shared architecture, relations and scope
contract on installed and candidate templates. It checks the candidate's human
identity prompt and authority route directly. It no longer requires adoption
of unreleased source merely to make template metadata equal.

The migration test normalizes fixture CRLF before constructing a requested
line ending. Original owner-byte assertions and migration refusal checks remain.
The former CRLF case produced CR-CR-LF and failed on the unchanged baseline too;
the installer correctly refused that unrecognized input. No installer behavior
or historical fixture bytes were changed.

Both focused cases pass after application. Shared full Windows/Linux results
and original failures are retained under WO-IAR-021/checks/. checks.json points
to those results; no skipped or unrun check is represented as passed.
