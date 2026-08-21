+++
id = "SPEC-IAR-012"
type = "specification"
title = "Owner instruction region contract for the se_harness repository"
status = "implemented"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-IAR-020"]
+++

# Specification: Owner instruction region contract for the se_harness repository

## Scope

The owner-controlled region of the repository-root `AGENTS.md`, meaning all content outside the `<!-- se-harness:begin -->` and `<!-- se-harness:end -->` markers. Out of scope: the managed fragment, `CLAUDE.md`, every managed policy module, the packaged `templates/repository/standard/AGENTS.md.fragment`, and portable SE Harness behavior.

## Actors and external systems

- Coding agents that load `AGENTS.md` directly or through the `CLAUDE.md` import.
- `se_harness.installer`, which treats `AGENTS.md` as `fragment` mode and tracks only the extracted managed block.
- The released 0.5.0 evaluator invoked by `doctor`, `preflight`, and the managed CI workflow.

## Inputs

- The current `AGENTS.md` bytes.
- `.engineering-harness.lock`, which is the authoritative record of per-path ownership mode and the expected fragment digest.
- `docs/engineering/REPOSITORY_CONTEXT.md`, the repository-owned, owner-curated source of commands and required checks. This specification treats it as ordinary owner content and depends on no harness property of it.

## Outputs

A revised `AGENTS.md` whose owner region satisfies the behavioral rules below and whose extracted managed block is unchanged.

## State model

`AGENTS.md` has exactly two regions. The managed block is integrity-tracked and owner-immutable. The owner region is owner-mutable and not integrity-tracked. `installer.tracked_content` returns only the managed block for `fragment` mode, so owner-region edits never alter the recorded digest.

## Behavioral rules

1. **Managed-block invariance.** `canonical_sha256(tracked_content("fragment", agents_bytes))` shall equal `files["AGENTS.md"].sha256` in `.engineering-harness.lock`. The block, including both markers, shall be reproduced byte-for-byte; `utf8-text-lf-v1` canonicalizes line terminators only, so any other whitespace or content change alters the digest.
2. **Marker well-formedness.** Exactly one begin marker and one end marker shall be present, in order. `installer._extract_block` raises on missing, duplicated, or out-of-order markers.
3. **Operational entry point.** The owner region shall carry the setup, test, graph-validation, additional-required-verification, lint-or-format, and entry-point facts inline so that no second read is needed for an ordinary operational task. It shall also name `docs/engineering/REPOSITORY_CONTEXT.md` as the repository-owned file holding the build, release-binding, and publication sequences, and direct the reader there before any such step, without duplicating those sequences. It shall describe that file by what it contains, not by any harness status: it shall not state that the file is preflight-required, harness-seeded, or otherwise required by the harness. `REQ-DST-065` retires both properties, and an owner region that asserts them would become false on that change while remaining a correct statement of ordinary owner content either way.
4. **Test command.** The owner region shall state `python -m unittest discover -s tests -p "test_*.py"` and shall state that no formatter or linter gate exists and none is to be introduced.
5. **Governed-invariant deferral.** The owner region shall not restate an obligation already carried by a governed requirement. It shall instead state that product invariants are governed requirements and point to `docs/engineering/README.md`.
6. **Managed-path enumeration.** The owner region shall identify all 28 hash-locked managed paths: `.engineering-harness.toml`; `ENGINEERING_HARNESS.md`; `docs/engineering/WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`; every file in `docs/engineering/templates/`; `.github/workflows/engineering-harness.yml`; and exactly these eight under `scripts/`: `validate_engineering_artifacts.py`, `generate_harness_dashboard.py`, `inspect_engineering_artifacts.py`, `select_harness_work_order.py`, `artifact_layout_registry.py`, `check_engineering_harness.sh`, `check_engineering_harness.ps1`, `harness_explorer/index.template.html`. It shall name `.engineering-harness.lock` as authoritative and state that editing a managed path breaks `doctor` and the CI gate.
7. **Owner-editable disambiguation.** The owner region shall state that the remaining files in `scripts/` — `bind_release_distribution.py`, `check_portable_release_surface.py`, `create_release_bundle_manifest.py`, `normalize_sdist.py`, `validate_release_distributions.py` — are repository-owned and may change under an approved work order. A blanket claim over `scripts/` is prohibited.
8. **Candidate-source direction.** The owner region shall name `templates/repository/standard/` as candidate source for the eight managed scripts and the managed policy documents, shall state that root copies are the released evaluator and intentionally lag until publication, and shall direct changes to the template. It shall state that an in-tree `doctor` reports that skew as `FAIL` and that the result is boundary evidence rather than authorization to overwrite root managed files. It shall further state that the candidate CLI is ahead of the released CLI, naming at least one command that exists only in the candidate, so that an agent does not put an unreleased command into an instruction the released gate must satisfy.
9. **Pull-request field.** The owner region shall state that every pull-request body needs a standalone `Harness-Work-Order: WO-...` field, and that CI reads it from the stored event payload so a later body edit remains red until the next push.
10. **Evaluator isolation.** The owner region shall state that the released evaluator runs from outside the checkout, and that a local `se-harness` on the import path makes candidate-source runtime identity fail with `RID018`.
11. **Retained agent constraints.** The owner region shall retain the deterministic boundary-and-failure-test obligation, the prohibition on building promotable release distributions without an approved release work order, untrusted handling of target paths, repository content, lock data, artifact metadata, and pull-request text, and preservation of unrelated changes and historical `VREC-*` and `RLS-*` facts.
12. **Bounded size.** The owner region shall remain under 6,000 bytes. It states local facts and pointers and shall not duplicate managed policy text.
13. **Authority neutrality.** The owner region shall approve nothing, shall record no product intent, and shall not claim precedence over `docs/engineering/`.

## Error and recovery behavior

- A digest mismatch on the managed block is unrecoverable within this specification: restore the block byte-exactly from `git show HEAD:AGENTS.md` or from `templates/repository/standard/AGENTS.md.fragment` wrapped by the installer's marker form.
- A managed-path list that disagrees with `.engineering-harness.lock` is a defect in the owner region, not a lock error. The lock wins.
- If `REPOSITORY_CONTEXT.md` is absent or incomplete, the pointer resolves to nothing and the reader must ask the repository owner. The owner region does not compensate for that; it only points at the file. This specification asserts no harness diagnostic for that case, because `REQ-DST-065` withdraws the one that exists today.

## Data and interface contracts

No new file, command, flag, schema, or machine-readable output. The only changed artifact surface is the owner region of one repository-root Markdown file.

## Security and privacy properties

The region continues to instruct that target paths, repository content, lock data, artifact metadata, and pull-request text are untrusted. The added pull-request guidance describes a required field; it does not weaken the strict selection performed by `se_harness.github_ci`.

## Performance and capacity

The always-loaded instruction surface stays under 6,000 bytes, against 2,160 bytes today. The intent is to shorten the total path to a correct first action, not to shorten this file.

## Observability

`harnessctl doctor` and `preflight` report managed integrity. No new observability surface is introduced.

## Compatibility and migration

Repository-local and self-contained. Consumer repositories are unaffected because the packaged fragment does not change. The revision is a single-file edit with no data migration.

## Examples and counterexamples

- **Conforming.** "Candidate source for the eight managed scripts is `templates/repository/standard/scripts/`. The root copies are the released 0.5.0 evaluator and intentionally lag until publication."
- **Counterexample, rule 7.** "…and files under `scripts/`." Over-broad; forbids editing the release-build tooling.
- **Counterexample, rule 1.** Splitting the managed paragraph after "before engineering work." Digest becomes `624cc67e…5648` against the recorded `bcf46d13…405f1c`.
- **Counterexample, rule 5.** Retaining "Preserve Python 3.11+ standard-library runtime behavior," which `REQ-DST-006` and related requirements already own.

## Explicitly unspecified decisions

Section order and headings within the owner region, wording of each fact, whether the managed block is relocated above the owner sections, and whether paths are listed inline or as a bulleted list are delegated to the implementation agent within rules 1 through 13.
