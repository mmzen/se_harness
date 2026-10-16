# Repository context

Use the selected entry returned by activation in the current context. If no
checkout is active, follow the [checkout activation](checkout.md#activate-the-checkout) with the actual
checkout path and host/session values delivered by the hook. After switching or
compaction, validate the selected checkout again. Read applicable owner instructions.
AGENTS.md is not a plugin installation or instruction-delivery requirement.

For a `released-resources-v1` selection, use the exact evaluator's
`resources ABSOLUTE_REPOSITORY --resource RESOURCE_ID --content --json` to read one
required instruction or checklist. Resolve returned resource locations outside
the checkout; formal artifact paths stay relative to the checkout. Do not require
repository copies of ENGINEERING_HARNESS.md or docs/engineering/harness/.
For a legacy selection, use its validated repository entry and task router.

When a result includes `instruction_discovery`, require `status = "available"`.
Read its current step's exact file and heading and each prerequisite whose
condition applies. Read the selected formal records separately. The
`evaluator_only_inputs` are not normal agent reading. An incompatible result
stops the affected action; report the version/discovery gap.

For a released result without this field, use that installed root's procedure
router and reading manifest. Do not apply candidate instructions to an older
selected release. A manual root read does not prove automatic host delivery.

