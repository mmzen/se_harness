# WO-REV-001 Verification Evidence

Verified on 2026-08-11 for the commit-bound revision provenance implementation in `se_harness`.

## Artifact graph

- The governing chain is `INT-REV-001` → `CAP-REV-001` → `REQ-REV-001..008` → `SPEC-REV-001` / `ARCH-REV-001` / `ADR-REV-001` → `WO-REV-001` → `VER-REV-001` → `REL-REV-001` → `OPS-REV-001`.
- The validator accepts the final repository graph with no errors or warnings.
- Candidate dashboard snapshot SHA-256: `b3eabcc746322ca1a4a00f11888b322f783b110c88435a7eb90af9d8664bcbc3`.

## Automated verification

- `python -m unittest discover -s tests -v`: 26 tests executed, 24 passed, 2 skipped because this Windows host does not grant the privilege needed to create test symlinks.
- The executable cases cover SHA-1 and SHA-256 identities, malformed and inconsistent records, typed relations, evidence containment, legacy compatibility, checkout comparison, Git cleanliness and HEAD failures, ready-only output, atomic non-overwrite, installation, migration, and dashboard generation.
- Source validator, dashboard generator, and Explorer template are byte-identical to their managed standard-template copies.

## Installed-wheel lineage exercise

- Wheel: `target/wheel/se_harness-0.2.0-py3-none-any.whl`.
- Wheel SHA-256: `a4853e770ebe055b5fd876cde36ccdf5a342ad68083296f3c63c7c0b17a4ddc6`.
- Candidate commit: `401bff5df7d1de71a171ec5f9b18857e1f6cabcd`.
- Later verification-governance commit: `5002bb7719b60e6019d15e210bacb4dc9ad57b6c`.
- The ready `VREC-001` and ready `RLS-001` both declare the original candidate commit, the candidate is available locally, and the Explorer reports the expected `different` checkout state after the governance commit.
- The installed validator reports 12 artifacts, 18 relations, 0 errors, and 0 warnings; `doctor` and `pip check` pass.
- Neither provenance command created a commit or Git tag; the fixture tag list remained empty.

## Explorer acceptance

- The generated self-contained HTML contains both revision record nodes and two structured provenance entries, reports the candidate commits as locally available, and has no external script or stylesheet.
- Embedded snapshot JSON parses successfully and the application JavaScript passes Node syntax validation.
- Direct interactive `file://` browser navigation was blocked by the in-app browser safety policy. No alternate browser driver was used; functional behavior remains covered by the dashboard tests and installed-wheel fixture.

## Boundaries

- When this implementation evidence was first produced, the new repository had no initial Git commit and therefore no honest source commit ID to record.
- `WO-REV-002` separately authorizes creation of the candidate and governance commits and the owner's verification decision. `VREC-REV-001` is the authoritative record of the resulting candidate commit.
- No release record, tag, release authorization, package publication, remote push, or remote publication is authorized. Automation only prepares `ready` records and never grants verification or release authority.
