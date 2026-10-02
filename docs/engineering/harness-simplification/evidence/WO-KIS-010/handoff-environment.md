# Handoff environment correction

The first released check-pr invocation returned exit 2:

```text
harnessctl: pull-request check: changed path is outside every selected work order: docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/readiness-fixture-inputs/synthetic-inputs/docs/engineering/readiness-probe/specifications/SPEC-PROBE-001.md.txt
```

Git without Windows long-path support reported that historical long path as
changed. The same complete diff with core.longpaths=true had no change under
docs/engineering/plugin-integration. No historical file was edited or removed.

The retry used process-local Git configuration:

```text
GIT_CONFIG_COUNT=1
GIT_CONFIG_KEY_0=core.longpaths
GIT_CONFIG_VALUE_0=true
```

The selected released 0.21.0 evaluator then returned a passing combined-scope
handoff for WO-KIS-010 and WO-KIS-011 and the original complete Git baseline
ccbfbdec811d722974336924125b070d91f111f4. Retained output:
combined-handoff-longpaths.json. No global Git setting or baseline was changed.

The local event selects the two work orders; it is a local input to check-pr,
not evidence of an actual GitHub PR or publication.
