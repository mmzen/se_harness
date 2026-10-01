```toml
artifact = "WO-RLS-029"
checkpoint = "handoff"
formal_snapshot_sha256 = "3d76dedd053933cca5af76827fd89d5964e2fe8581ff56927837da61aa5a7ce8"
rebound_at = "2026-10-01T10:05:08Z"
```

# WO-RLS-029 handoff evidence

Public fresh installation and updates from preserved 0.2.2 installations pass
on both Windows CLIs. All installed bytes, four offline evaluator identities
and qualified native-evidence applicability match plugin 0.2.3 / evaluator 0.20.1.
See publication.json, public-routes.json, public-evaluator-identities.json,
public-native-recheck.json and requirement-assessment.json.

Current documentation and its independent public identity tests are updated.
The 46 relevant tests have 45 passes and one existing Windows symlink-permission
skip. All changed-document links pass. review.json records the findings and
corrections. The symlink limitation is not reported as a pass.

Overall delivery remains incomplete: documentation integration/readback and
separate latest/last decisions/readback remain outstanding. The closeout result
and both required negative controls are retained. No publication, marker action,
repository adoption or human verification is inferred from these checks.
