# Minimal package checkout

The owner approved the proposed fix with "ok go" on 2026-09-13: give the package job only the script it uses, keep full source/governance checkouts, and rerun acceptance.
This is an owner-directed prerequisite under WO-PLG-021. It does not activate execution delegation before the approved packet reaches main.
The larger plugin simplification is not completed by this CI change.

The original failure was CP002 in Candidate package evidence: the released verifier snapshots at most 262,144,000 bytes.
Base main already contained 264,032,596 eligible tracked bytes. Old retained evidence remains in Git and in the source/governance jobs.

Local validation: 39 CI workflow tests pass. A sparse checkout of the actual prior candidate materializes one 9,955-byte script; the unmodified released 0.17.0 snapshot succeeds and Git stays clean.
Graph, review preflight, diff scope and 14 release-distribution records pass. Hosted acceptance is the remaining observation.
