+++
id = "VER-PLG-029"
type = "verification"
title = "Verify public marketplace 0.2.2 and final delivery claims"
status = "approved"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[relations]
verifies = ["REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:31:39Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 470ee9fe58336c8705bf0516ea953a9b18ece20b090034bd82ed23d0f0026086; approval input SHA-256 470ee9fe58336c8705bf0516ea953a9b18ece20b090034bd82ed23d0f0026086. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
+++

# Verify public marketplace 0.2.2 and final delivery claims

## Independence

Compare public observations with the reviewed distribution commit and inventories
accepted under VER-PLG-028. Compare evaluator bytes with the released 0.20.0 RLS.
Do not copy a mismatched public identity into the expected plan to make it pass.
The released 0.19.0 evaluator governs this work until separate repository adoption.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-019 | demonstration, inspection | Public immutable ref, both fresh/update routes, native delivery traces, claims review and links | Actual public bytes and installed content match the reviewed 0.2.2 package and public 0.20.0 wheel. Documentation matches observed availability and bounded support. |
| REQ-RLO-020 | test, inspection | Final report for all five surfaces, missing-marketplace and wrong-ref controls | Complete only with released RLS and matching retained evidence for every surface; the two negative cases remain incomplete. |

## Qualification after marketplace publication

Resolve `https://github.com/mmzen/se_harness#plugin-marketplace` to its immutable
public commit. Compare every declared package identity with the reviewed
assembly, including PACKAGE-IDENTITY.json, host manifests, catalogs, inventories,
wheel and archives. Test both public routes on each claimed Windows CLI:

1. Fresh installation from the public Git branch in a disposable profile.
2. Update from the observed public plugin 0.2.1 source to 0.2.2.

Record starting source/version, resolved commit, host/version, loaded plugin
path, installed-content inventory, evaluator identity and actual command results.
A local directory, cache listing or equal version label cannot replace a public
route. Recheck native delivery using the installed public content; if earlier
native evidence is reused, retain the exact input comparison and its limits.

Reconcile the current source README, installation/publication guides, host
READMEs and marketplace-root README with the observations. Check source links
in their source context and packaged links in the assembled context. Historical
versions may remain when clearly labelled. Retain the exact documentation commit.

Prepare the final delivery VREC at its clean candidate after public observations
and documentation corrections. It includes the retained pre-publication evidence
and actual public results; it does not rewrite the earlier VREC.

## Final closeout

After the separately authorized documentation integration, retain an append-only
public documentation readback and final delivery report. These delivery receipts
are outside the already bound candidate evidence. Observe Pages provenance and
the separately authorized latest/last targets. Run `scripts/check_release_delivery.py`
with the reviewed plan, observations and evidence root. Require exit 0 and
`complete`; retain the missing-marketplace and wrong-revision negative results.
No new assurance loop is required solely to integrate the final receipt.

## Evidence retention

Use `docs/engineering/release-0-20-0/evidence/WO-PLG-031/`. Keep failed attempts,
exact argument arrays, source revisions, runtime identities, observation times,
file digests and subsequent results. Evidence reuse identifies the original
observation and why its exact inputs still apply. Do not retain credentials,
real user profiles, virtual environments or complete disposable repositories.

## Residual uncertainty

Public success is established only by these observations at their recorded
times. Publication permission, availability and native authentication cannot be
guaranteed in advance. Real user profile adoption, repository upgrade and stock
guide removal are separate actions and do not follow from these test results.
