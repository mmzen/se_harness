# Retained orientation and briefing

This implementation adapts the two existing read-only skills to plugin paths.
The helper scripts, contracts and output schemas are retained. The instructions
require verified evaluator inputs and trusted plugin helpers; repository doctor
does not authenticate plugin copies. Briefing remains explicitly requested.

- [Core comparison](retained-core-comparison.json): exact unchanged helper and contract hashes.
- [Instruction review](instruction-review.md): preserved boundaries and the narrow current-state wording correction.
- `governance/start/`: actual released 0.17.0 delegated start and live check.
- `checks/initial/`: actual initial checks and expected candidate/released differences.

Independent acceptance is in progress. It will separate actual helper operations,
model instruction observations, and the test-only interception boundary. It will
not qualify native plugin activation, production controls or live skill migration.
WO-PLG-012 remains in_progress; no assurance decision is made here.
