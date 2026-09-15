+++
id = "VER-PLG-016"
type = "verification"
title = "Verify the installation guide against actual use"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
verifies = ["REQ-PLG-027"]
+++

# Verify the installation guide against actual use

## Checks and pass conditions

1. Follow the claimed development or released installation route in a disposable
   project on each host claimed in the guide. Confirm discovery of the intended
   skills, setup/connection and one useful explicit check. Reuse existing evidence
   for unchanged steps; run the remaining steps. Identify the actual versions.
2. Inspect prerequisite, compatibility and repair guidance against existing setup
   and installer results. Missing prerequisites have a useful next step; repair
   uses the existing environment and does not silently upgrade the project.
3. Read the guide as a new user. It says which route was checked and which release
   is actually available. No hooks, helper agents, benchmarks or additional CI
   framework are prerequisites. Any observed confusing prompt or delay is reported.

All three checks cover REQ-PLG-027. A real released-install claim requires a real
released-install walkthrough; local packages prove only the documented development
route. If a host cannot be exercised, mark it unverified and narrow the claim.
Keep one short walkthrough summary with evidence references, not a folder per
scenario or a copied repository. Run required repository checks for the diff.
Actual changes to host settings require the existing owner authorization for the
named action; planning this work does not perform installation or publication.
