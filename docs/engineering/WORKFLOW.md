# Workflow

1. Capture the problem and accountable actors in an intent.
2. Derive capabilities and observable normative requirements.
3. Specify exact behavior, architecture constraints, and independent verification.
4. Approve one bounded work order referencing the complete governing chain.
5. Implement, validate, and run repository-specific quality checks.
6. Retain evidence keyed to the work-order ID.
7. Commit the clean candidate source and evidence, then run `harnessctl capture-verification`; commit the resulting ready verification record in a later governance commit.
8. Have the assurance owner review and transition the verification record to `verified`.
9. Run `harnessctl prepare-release`, have the release owner review it, and separately create any authorized tag against the candidate commit.
10. Evaluate operating contracts through accountable humans.

Lifecycle values are `draft`, `ready`, `approved`, `in_progress`, `implemented`, `verified`, `released`, `superseded`, and `rejected`. A status change records authority; it is not a confidence estimate.

A record cannot contain the hash of its own commit. The verified or released candidate commit therefore precedes the later governance commit containing `VREC-*` or `RLS-*`.
