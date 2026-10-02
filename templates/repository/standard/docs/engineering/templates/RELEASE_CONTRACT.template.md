+++
id = "REL-xxx"
type = "release_contract"
title = "<Promotion decision>"
status = "draft"
owners = ["<release owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
# Choose the final candidate and the work to release.
# `harnessctl release-unit . --from <tag> --to <commit>` gives advisory history.
candidate_commit = "<full commit id, 40 or 64 hex>"
previous_release_tag = "v<version>"

[relations]
gates = ["WO-xxx", "VER-xxx"]
+++

# Release Contract: <title>

## Release unit

Name the final candidate commit and the work the release owner approves in
`gates`. Use `harnessctl release-unit` to inspect history if useful; missing
trailers and differences from this scope do not require exemptions.

One explicitly verified final-candidate VREC must cover every released work
order and its required verification contracts. Its evidence may cite earlier
records at different commits, but must demonstrate testing of the final
integration. The RLS binds that final VREC at the exact candidate commit.

## Required evidence

## Compatibility and migration

## Security and provenance

## Promotion policy

Select complete release delivery or the existing separately authorized route.
For complete delivery, name the frozen delivery plan and its review location.
List every deliverable, immutable payload identity, destination, required check,
recovery condition and moving-marker target. Include any required release-only
integration, with its allowed paths and rule for deriving governance commits.
Complete required preparation and human verification before the release request.

## Human approval triggers

For the explicitly selected complete-release route, one human response covers
the exact release record and listed external actions. Retain that decision and
the reviewed plan digest. Reuse it for unchanged valid actions and retries;
changed inputs or scope need a new decision. Required checks remain required.
Old release-only approvals do not acquire delivery authority retrospectively.

## Rollback criteria and procedure

Stop if the final candidate lacks complete verified coverage or release approval.

## Post-release observation window
