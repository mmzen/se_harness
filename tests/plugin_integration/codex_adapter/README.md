# Codex adapter acceptance

Run focused transport tests explicitly; top-level discovery does not descend
into this directory:

```text
<absolute-evaluator-016-python> -I -B -m unittest discover -s tests/plugin_integration/codex_adapter -p "test_*.py" -v
```

`fixture.py prepare` initializes a fresh disposable repository using released
0.16.0, applies explicitly synthetic fixture inputs and records fresh pre-action
evidence. It records the actual accepted host executable/version/digest. It
never copies credentials. The already authenticated WO-PLG-003 disposable
profile is selected explicitly; the old probe plugin is disabled only for the
process through a documented config override.

Commit package inputs before `fixture.py assemble --revision FULL_COMMIT`.
The unchanged WO-PLG-001 builder selects the released 0.16 wheel and runs both
build and independent check. The companion Claude manifest is deliberately
inert; only the Codex package is installed and assessed here. Native marketplace
installation and `/hooks` review retain host receipts without cache edits.

All command captures use fresh evidence directories. Direct guard and script
tests are calibration. VER-PLG-005 C01-C12 additionally need retained native
discovery, actual session restoration and actual mapped tool effects, including
fault cases and independent target hashes. No missing run counts as passing.
