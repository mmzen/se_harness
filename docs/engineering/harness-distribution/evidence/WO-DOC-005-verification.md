# WO-DOC-005 implementation verification

- Date: 2026-08-11
- Work order: `WO-DOC-005`
- Verification contract: `VER-DST-004`

## Authorization and scope

The repository owner first authorized preparation of the packet with `go for the artifact packet`, reviewed the resulting `REQ-DST-014`, `SPEC-DST-004`, `ARCH-DST-004`, `ADR-DST-004`, `VER-DST-004`, and `WO-DOC-005`, then explicitly authorized implementation with `go for implementation` on 2026-08-11.

The implementation is limited to the public root README, focused static tests, this packet and acceptance/index support, and this retained evidence. It does not change CLI or runtime behavior, package metadata, version, dependencies, entry points, Python support, canonical installed templates, lock data, workflows, action or CI pins, historical artifacts, releases, tags, published files, or external configuration. No distribution was built and no commit, verification capture, push, pull request, release, publication, deployment, merge, force push, or history rewrite was performed.

## Implemented outcome

| Contract | Retained result |
| --- | --- |
| User-perspective value | `README.md` places exactly one `What this looks like in practice` section after `Quick start` and before `What it provides`. |
| Representative interaction | A repository owner requests backward-compatible per-customer rate limiting, approves bounded work, assesses evidence, and requests a pull request without operating routine harness commands. |
| Agent execution | The coding agent prepares the engineering chain, runs preflight and repository checks, retains evidence, commits a clean candidate, prepares commit-bound verification, and opens the later governance pull request only after human decisions. |
| Human authority | Intent, work scope, assurance, and release decisions remain explicit human responsibilities; release is downstream and separately authorized. |
| Traceability graph | One inline Mermaid flowchart connects approved outcome, intent, capability, requirement, design, verification, authorized work, agent implementation, evidence, exact candidate commit, ready record, human assurance, verified record, human release decision, and released revision. |
| Explorer value | Dotted observation edges expose traceability and anomalies, scope and evidence, and commit provenance without granting authority. |
| Renderer fallback | The prose before and after the fence contains the complete value statement, and labeled nodes, decision diamonds, class names, and readable relations remain useful when Mermaid is displayed as source. |

The illustrative API scenario creates no API product artifacts and makes no claim that this distribution repository implements rate limiting.

## Red-to-green focused contract

The two new `tests.test_public_onboarding` methods were added before the README section.

Initial command:

```text
python -m unittest tests.test_public_onboarding -v
```

Initial result: expected failure. Ten tests ran in 0.025 seconds; the eight existing onboarding tests passed and the two new tests failed because `## What this looks like in practice` did not exist.

After implementation, the same command passed all ten tests in 0.003 seconds. An intermediate run correctly detected case-sensitive prose and overly literal Mermaid-edge assertions; the implementation removed ambiguity between human acceptance and the agent's `validate` operation, while the tests were tightened around the intended semantic declarations rather than invalid shorthand.

The focused tests now prove section ordering, scenario terms, human authority, agent attribution for `doctor`, `preflight`, `validate`, `dashboard`, and `capture-verification`, representative graph nodes and relations, three decision diamonds, ten semantic classes, node-to-class assignments, textual fallback, absence of external images or executable styles/scripts, existing metadata and version synchronization, upgrade separation, source-development placement, UTF-8 hygiene, and local-link integrity.

## Full supported-runtime suites

| Runtime and command | Result |
| --- | --- |
| Python 3.14.6: `python -m unittest discover -s tests -p "test_*.py"` | PASS: 80 tests in 37.888 seconds, 2 expected conditional Windows symlink skips |
| Python 3.11.9: `.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"` | PASS: 80 tests in 37.633 seconds, 2 expected conditional Windows symlink skips |

Both runs exercised the same working tree. No symlink implementation changed.

## Harness and repository checks

| Command or assessment | Result |
| --- | --- |
| `python -m se_harness preflight . --work-order WO-DOC-005` | PASS in start phase with the complete approved manifest |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS: 187 artifacts, 0 errors, 0 warnings before evidence completion |
| `python -m se_harness --help` | PASS: all ten expected subcommands present |
| `python -m se_harness doctor .` | PASS: required routes, distribution copies, managed files, schema-2 lock, repository seeds, scripts, and Python 3.14.6 runtime checks |
| `python -m se_harness dashboard .` twice before evidence completion | PASS twice: 187 artifacts, 648 relations, 0 errors, 1 warning, identical snapshot `c37b96262f7b5ecf4828cf9594642c9107ecc6917e223c5f5239096eda043f7d` |
| `git diff --check` | PASS before evidence completion |

The sole Explorer warning is the pre-existing derived observation that `VREC-AGR-001` remains `ready` while later verified or released records fully cover its work. It is unrelated to `WO-DOC-005` and does not affect formal validation.

Final implemented-state results after this evidence file and lifecycle transition exist:

| Command | Result |
| --- | --- |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS: 187 artifacts, 0 errors, 0 warnings |
| `python -m se_harness preflight . --work-order WO-DOC-005 --phase review` | PASS for implemented `WO-DOC-005` with the complete governing manifest |
| `python -m se_harness dashboard .` twice | PASS twice: 187 artifacts, 648 relations, 0 errors, 1 unrelated warning, identical snapshot `31a32a8988c3301ee3e7f0c14676779e063ab63ee86f3533984f270d05113a00` |
| `git diff --check` | PASS |

## Manual README and accessibility review

- The section is immediately discoverable after installation and repository quick start, before the long feature and governance reference.
- User blockquotes contain desired outcomes and accountable decisions, not `harnessctl` operations.
- Narrative and graph both preserve the later governance-commit boundary around a commit-bound ready verification record.
- Architecture, assurance, and release decisions use diamonds. Explorer relations are dotted. Labels and prose duplicate the semantic distinctions carried by color.
- Every fixed fill against white text exceeds a 5.0:1 contrast ratio: human 6.70:1, intent 7.10:1, design 5.47:1, work 5.02:1, execution 7.58:1, evidence 5.02:1, provenance 7.90:1, verified 5.48:1, release 6.04:1, and Explorer 10.35:1.
- The Mermaid source contains no JavaScript, external CSS, image, generated fragment, or network dependency.
- Existing install, upgrade, artifact-model, Explorer, provenance, release, safety, layout, CI, and development guidance remains present.

## Changed and protected surfaces

Intended paths:

- `README.md`;
- `tests/test_public_onboarding.py`;
- `docs/engineering/harness-distribution/README.md`;
- `docs/engineering/harness-distribution/acceptance/pypi-onboarding.feature`;
- `REQ-DST-014`, `SPEC-DST-004`, `ARCH-DST-004`, `ADR-DST-004`, `VER-DST-004`, and `WO-DOC-005` packet files;
- this evidence file.

Confirmed unchanged: `pyproject.toml`, `se_harness/`, canonical `templates/repository/standard/`, `.engineering-harness.lock`, `.github/`, managed root instructions and scripts, historical work orders and evidence, verification and release records, version and release facts, Git tags, release assets, and external services.

## Deviations and residual risk

No approved-scope deviation occurred. The prose was tightened from the initial proposal, and the user says `accept the change` rather than `validate the change` so the human assurance decision is not confused with the agent-operated `validate` command.

Static tests do not prove visual rendering in every Markdown consumer. GitHub Mermaid rendering remains a later pull-request observation, and package-index rendering remains deferred to a separately authorized release inspection. Renderers that do not visualize Mermaid may show the fenced source; the complete surrounding prose and labeled graph source are the accepted fallback. No release build is authorized under this work order.

`WO-DOC-005` is implemented, not commit-bound verified or released. A clean candidate commit and `VREC-*` may be prepared only after separate authorization.
