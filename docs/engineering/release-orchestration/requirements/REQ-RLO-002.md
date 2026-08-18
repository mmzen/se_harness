+++
id = "REQ-RLO-002"
type = "requirement"
title = "Bind exact distributions in machine-readable release provenance"
status = "approved"
owners = ["release-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN a Python distribution release record is prepared, THE SYSTEM SHALL bind a complete structured distribution manifest containing the candidate epoch, exact filenames, lowercase SHA-256 values, and checksum-manifest identity."
verification_method = "automated-schema-cli-and-compatibility-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Bind exact distributions in machine-readable release provenance

## Rationale

Hashes retained only in narrative evidence cannot be consumed safely by a deterministic workflow. The release decision needs immutable, validated distribution identity while historical records remain valid.

## Preconditions and trigger

Candidate qualification has produced a structured manifest for one version and candidate commit. `harnessctl prepare-release` is asked to prepare an RLS that will feed the SE Harness Python publication pipeline.

## Required response

Validate and capture a versioned distribution block containing the exact candidate commit, commit-derived source-date epoch, universal-wheel filename and hash, normalized-sdist filename and hash, deterministic `SHA256SUMS` filename and hash, and source manifest hash. Require canonical lowercase hex, safe basenames, exact version-derived names, and complete all-or-none fields.

## Failure and boundary behavior

Reject malformed, partial, unsafe, duplicate, wrong-version, wrong-candidate, wrong-epoch, or mismatched manifests. Historical RLS files without the optional block remain valid graph history, but the last-mile workflow must refuse them as insufficient publication input.

## Constraints

The preparation command may copy verified facts into a ready proposal; it does not build, approve, commit, tag, publish, deploy, or transition the record.

## Acceptance examples

An exact manifest for version `0.5.0` and the selected candidate is retained in the RLS. A manifest naming `se_harness-0.4.1.tar.gz`, an absolute path, or a different candidate is rejected without a partial RLS write.

## Open decisions

None.
