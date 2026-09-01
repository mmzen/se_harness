# Publishing the SE Harness development dashboard

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a repository-specific promotional workflow for `mmzen/se_harness`. It is not installed into consumer repositories and grants no verification, release, publication, deployment, or evaluator-adoption authority.

The public [SE Harness Explorer demonstration](https://mmzen.github.io/se_harness/) shows how SE Harness governs its own development. It is generated from the same canonical artifact graph that maintainers inspect locally, then deployed as a static GitHub Pages artifact.

The site is derived and read-only. Formal Markdown artifacts, their lifecycle states, retained evidence, exact Git records, and accountable human decisions remain authoritative.

## Why two commits are displayed

An SE Harness release has two distinct revisions:

```text
candidate commit C <- release tag vX.Y.Z
       |
       +-- later verification and release decisions
                    |
                    +-> governance commit G on main
```

`C` is the exact software payload that was tested, packaged, and released. `G` is the later main-history commit containing the completed verification and release records for that payload.

Publishing only the tag would omit those later decisions. Publishing the current moving `main` head could include unrelated work. The Pages workflow therefore resolves and reports both commits, then generates the demonstration from immutable governance commit `G`.

## Normal release behavior

After a released RLS is integrated into `main`, the release owner runs **Publish authorized SE Harness release** with that one RLS ID. Its main-context Pages stage:

1. finds exactly one matching released formal release record;
2. proves that the Git tag resolves to the record's candidate commit;
3. finds the first main first-parent commit that integrated the released record;
4. checks out that governance commit in a clean detached worktree;
5. generates the Explorer bundle using the snapshot's target-local generator;
6. checks the exact public file allowlist, schema, provenance, and hashes;
7. uploads one Pages artifact and deploys it through the `github-pages` environment.

Until `WO-REB-028` the stage also ran `qualify predecessor-view` with an independently released predecessor evaluator. That operation and the predecessor-compatible view it qualified were retired with the 0.5.0→0.6.0 bootstrap bridge (`ADR-REB-012`); the release-bound predecessor results retained under `docs/engineering/release-0-6-0/` are history, not a step the workflow still performs.

A failure stops the replacement. It does not rewrite Git history, alter the GitHub Release, transition an artifact, or intentionally delete the previous successful site.

## Replaying a deployment

Use the separate accountable manual replay for an older release or after a transient Pages failure. In GitHub, open **Actions -> Publish SE Harness Explorer demonstration -> Run workflow** on `main` and provide:

- the released formal record ID; and
- the full governance integration commit.

The workflow derives the tag and candidate from that record. It does not accept an override for either identity and has no automatic tag-ref release trigger.

For the first deployment of release 0.4.0, the inputs are:

```text
release_record:    RLS-SEH-006
governance_commit: a702d187084ba72d2c8b8b61c66b2a1be5d6f403
```

The same request can be made with GitHub CLI after deployment is explicitly authorized:

```powershell
gh workflow run publish-dashboard-pages.yml --ref main `
  -f release_record=RLS-SEH-006 `
  -f governance_commit=a702d187084ba72d2c8b8b61c66b2a1be5d6f403
```

The workflow rejects short commits, arbitrary branches, later main commits, ambiguous release records, tag mismatches, invalid graphs, unexpected upload files, and prereleases. A replay is expected to reproduce the same bundle-manifest hash and manifest-declared resource bytes.

## What is public

The Pages artifact contains only:

- `index.html`, with a bounded bootstrap plus the constant demonstration, content-disclosure, and non-authority notice;
- `dashboard-manifest.json`, which identifies every progressively loadable resource by controlled path, role, schema, byte count, and SHA-256;
- digest-named summary, topology, readiness, per-artifact detail, and retained-evidence resources declared exactly by that manifest;
- `generation-summary.json`, including publication hashes, size observations, and provenance; and
- `publication-manifest.json`, the bounded release/candidate/governance attestation for the static deployment.

Publishing the generated bundle makes every manifest-declared artifact body, evidence body, and raw evidence file public. The workflow independently rejects missing, additional, redirected, malformed, or hash-mismatched resources; it does not glob a directory into the Pages payload. It does not scan for secrets or redact content, so maintainers must keep sensitive material out of the selected governance snapshot.

Dashboards generated by releases up to 0.12.0 retain the exact unpkg dependency, CSP, timeout, and non-3D fallback accepted by `ADR-DST-008`. From the 0.13.0 candidate onward the Explorer is one self-contained document that names no remote origin (`ADR-DST-013`), so the published page requests only its own origin. GitHub Actions and GitHub Pages remain external availability and trust dependencies.

## Operational boundary

The deployment uses immutable action pins, read-only source access, a dedicated non-cancelling concurrency group, and a separate deployment job with only `pages: write` and `id-token: write`. Generated files are never committed to `main`, `gh-pages`, release branches, or work branches.

The site is a best-effort demonstration, not a production assurance service. See the formal [`OPS-DPG-001`](../engineering/dashboard-publication/operations/OPS-DPG-001.md) for failure handling, replay, security controls, and evidence retention. GitHub documents the underlying [custom Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages); repository policy remains authoritative for this implementation.

The workflow runs no predecessor evaluator and accepts no caller-selected script, omission, or expected diagnostic. The only remaining mechanism for showing that a predecessor evaluator and its successor agree is the real upgrade rehearsal described in [rehearsing the root-evaluator handover](evaluator-migration-rehearsal.md).
