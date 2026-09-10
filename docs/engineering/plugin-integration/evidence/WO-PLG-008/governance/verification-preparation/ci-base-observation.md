# CI comparison base during preparation

Run 34507662552 checked the synthetic merge of candidate `1daf4e3ecf3a46a3cb8ad385a11b6cfa39e4549d` into parent `bf0a2b4705617e735357842872edd068ce2ed610`, while its event supplied the earlier parent `692407030f30aed7e462e7cac9760e256d7a7f5d` as `HARNESS_BASE_SHA`. The scope gate rejected `docs/engineering/plugin-integration/README.md` (WEX201).

The topic diff from `692407030f30aed7e462e7cac9760e256d7a7f5d` to `1daf4e3ecf3a46a3cb8ad385a11b6cfa39e4549d` does not change this file. The mismatch includes parent changes in the child scope check. The failure is retained; the selected scope is not broadened. Delivery will refresh PR #436's existing `work/plugin-session-context` base after the parent record is published, before pushing this record commit. Subsequent hosted checks must use the refreshed base. Neither candidate will be rewritten.
