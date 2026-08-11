# se-harness 0.2.0 Release Packet

This packet governs qualification and GitHub publication of the first `se-harness` release, version `0.2.0` with tag `v0.2.0`.

The accountable repository and release owner initially confirmed the version, nine-work-order payload, and GitHub-only publication scope on 2026-08-11 with the instruction `ok, then let's go` after reviewing why the release requires one final aggregate verification record.

During qualification, two raw setuptools sdists contained identical source payloads but different generated timestamps. The accountable owner authorized a bounded deterministic sdist correction on 2026-08-11 with the instruction `implement the deterministic sdist fix`. Because the correction adds release tooling to the source distribution, `WO-RLS-001` is the tenth release-bearing work order. It does not change the package runtime or installed harness.

## Exact payload

`WO-AGR-001`, `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-PMI-001`, `WO-REV-001`, `WO-RLS-001`, and `WO-VSP-001`.

Governance-only `WO-REV-002..005` and `WO-PUB-*` records remain auditable but are excluded from the software payload. The GPLv3 `LICENSE` is repository-administration metadata included in the source release and explicitly recorded in release evidence; it is not silently represented as a software work order.

## Planned lineage

1. `WO-RLS-001` qualifies the final repository candidate and distribution artifacts.
2. `VREC-SEH-001` captures the exact ten-work-order aggregate at the clean candidate commit.
3. An accountable quality decision later transitions `VREC-SEH-001` from `ready` to `verified`.
4. `RLS-SEH-001` is prepared as `ready` for version `0.2.0`, tag `v0.2.0`, under `REL-DST-001`.
5. An accountable release decision later transitions `RLS-SEH-001` to `released` and authorizes tagging and GitHub publication.

## Deterministic source distribution

Build the raw wheel and sdist with the approved build environment, then normalize the sdist using an explicit candidate-derived Unix timestamp:

```powershell
python -m build --wheel --sdist --no-isolation --outdir <raw-output> .
python scripts/normalize_sdist.py `
  <raw-output>/se_harness-0.2.0.tar.gz `
  <release-output>/se_harness-0.2.0.tar.gz `
  --epoch <candidate-commit-unix-timestamp>
```

The helper sorts members and normalizes container metadata while preserving file bytes and modes. It refuses an existing output and rejects unsafe, duplicate, symlink, hard-link, device, FIFO, and other special members. Reproducibility is established by normalizing two independent raw builds with the same explicit epoch and comparing their SHA-256 hashes and payload manifests.

The recorded release-build runtime and compression implementation are part of the reproducibility environment. Python runtime compatibility for consumers remains `>=3.11`, but byte-identical gzip streams are qualified against the recorded builder toolchain; a different zlib implementation may produce an equivalent archive with different compressed bytes.

## Distribution outputs

- `se_harness-0.2.0-py3-none-any.whl`
- normalized `se_harness-0.2.0.tar.gz`
- `SHA256SUMS`
- GitHub-generated source archives associated with `v0.2.0`

No PyPI publication, deployment, moving tag, alternate installation profile, or unreviewed scope change is authorized.
