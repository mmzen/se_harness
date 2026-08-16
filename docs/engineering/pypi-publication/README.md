# Governed PyPI Publication

This packet governs a repository-specific GitHub Actions publisher for the `se-harness` PyPI project. It promotes the exact wheel and normalized source distribution already retained on an authorized GitHub release; it never rebuilds in the credential-bearing publication job.

The initial approved work order configures and verifies the publication path only. It does not authorize a workflow run, PyPI upload, replacement of version `0.2.0`, a new tag, or a new software release. Those actions require a separate accountable release-owner decision referencing exact artifact hashes.

Validate the packet and implementation with:

```powershell
python scripts/validate_engineering_artifacts.py --root .
python -m unittest tests.test_pypi_publishing
```

`OPS-PYP-001` was separately reviewed and approved through `WO-OCA-001` on 2026-08-16. It accepts the continuing controls for exact released-asset selection, least-privilege Trusted Publishing, no-rebuild promotion, explicit human authorization, and retained publication evidence. `REL-PYP-001` remains a draft release proposal; the operating contract does not authorize a workflow dispatch or PyPI upload.
