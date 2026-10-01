# External lock evidence correction

WO-IAR-039 updates one validator to accept a valid schema-5 selection.
The existing lock validator checks its layout and identity before evidence
comparison. Schemas 3 and 4 retain their existing behavior.

Both new regressions failed with E012 before the correction. The focused
resource/provenance tests and full suite passed after it. Full raw results,
review and authorization are in implementation.json. No inspection-policy,
installed harness, authority or acceptance rule was changed.

Installed package and final aggregate qualification follow at the committed
candidate; this report does not declare the work implemented or verified.
