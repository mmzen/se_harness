```toml
artifact = "WO-PLG-011"
checkpoint = "handoff"
formal_snapshot_sha256 = "e01c7f9452c7803408287fd7e38cc9fa10d3815df58d4c7f3425e93cf9320f00"
rebound_at = "2026-09-10T20:24:25Z"
```

# WO-PLG-011 handoff evidence

## Delivered implementation

The evidence skill and two references guide existing evidence, VREC and RLS
preparation. They retain failed or missing results, distinguish all four writing
operations from read-only checks, account for generated capture output, inspect
uncertain effects before retrying, and preserve the candidate/governance split.
External actions require their exact authority and independently demonstrated
controls. Read-only inspection retains its ordinary permissions.

## Observed validation

The independent Windows report covers EVD01–10 with 82 actual traces and zero
duplicate approval prompts. Linux replay passes 82 fixed calls. Both use the
released 0.16.0 evaluator in disposable repositories; external effects are
simulated through a separately calibrated fixture tool. Original fixture,
footprint and runner failures remain retained with corrected repeats.

Skill and distribution checks pass. Source CI passes 1,134 tests with four
skipped. Released 0.17.0 doctor, graph validation and review preflight pass.
Candidate 0.18.0 doctor reports the expected six managed-template differences;
the root's released managed files remain intact. See the evidence index for
exact commands, raw results, hashes and the focused recorder-error checks.

## Boundaries and remaining decision

The tests do not qualify native plugin activation, production external controls
or live skill migration. Recovery includes post-exit receipt loss and an injected
partial state, not an actual in-flight evaluator crash. Linux empty command spans
do not establish fresh model decisions. This handoff supplies implementation
evidence; it does not exercise assurance, release, merge or publication rights.
Live delegated completion and ready-VREC preparation are retained separately.
