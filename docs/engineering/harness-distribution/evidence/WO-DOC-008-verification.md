# Verification Evidence: WO-DOC-008

## Authorization and boundary

The repository owner agreed with the concise-root proposal, requested its formal packet, and explicitly instructed `go for implementation` on 2026-08-12 after reviewing `REQ-DST-024..028`, `SPEC-DST-007`, `ARCH-DST-007`, `ADR-DST-007`, `VER-DST-007`, and `WO-DOC-008`.

Work remained in the existing `C:\Users\mathi\RustroverProjects\se_harness` checkout. It changed public/explanatory documentation, focused documentation tests, this packet's lifecycle, the harness-distribution owner index, and retained evidence only. No runtime, CLI behavior, validator, Explorer generator, installer, managed policy, canonical template, workflow, lock, package metadata/version, governor descriptor, historical formal record, external repository, build, commit, push, pull request, tag, release, publication, deployment, or hosting configuration was changed.

`WO-DOC-007` and its evidence remain completed history and were not reopened.

## Baseline and implemented information architecture

The initial `README.md` had 523 physical lines and 16 level-two sections. The implemented root has 123 physical lines and 8 level-two sections, below the approved maximums of 200 and 9.

| Public document | Target expertise | Responsibility |
| --- | --- | --- |
| `README.md` | 6/10 | Concise value, installation/upgrade distinction, five human repository commands, practical story and graph, responsibility boundary, Explorer value, limitations, and routes. |
| `docs/notes/harness-installation-and-upgrades.md` | 5/10 | Platform environments and launchers, exact-version install, init/adopt, separate package and repository upgrades, explicit plan/apply safety. |
| `docs/notes/harnessctl-reference.md` | 7/10 | Exact inventory of all 12 CLI subcommands with actor, state effect, phase, key options, and authority boundary. |
| `docs/notes/developing-se-harness.md` | 8/10 | Source setup, repository structure, checks, three self-hosting planes, build/release constraints, and governor promotion. |
| `docs/notes/README.md` | 4/10 | Primary progressive path plus separate operator and contributor routes. |

## Content disposition ledger

| Former root responsibility | Disposition |
| --- | --- |
| Learning path | Condensed to `Learn more`; complete paths owned by the notes index. |
| Platform activation and launcher locations | Moved to the installation/upgrade note. |
| PyPI and exact-version install | Kept in concise root form and expanded in the installation note. |
| `init`, `adopt`, `doctor`, `validate`, `dashboard` | Kept and distinguished in `Start using it`. |
| Domain scaffolding and artifact creation examples | Moved to the command reference; root retains agent drafting responsibility only. |
| User-perspective rate-limit story | Kept and shortened without losing approval, evidence, candidate, assurance, or release boundaries. |
| Large 18-node artifact graph | Replaced with one 8-node value/authority graph; detailed model remains in the UML note. |
| Feature inventory and Explorer questions | Consolidated into `What you get`; formal gate detail remains in policy/phasing. |
| Agent instruction and five-minute operating workflow | Consolidated into `Who does what`; timing and commands remain in phasing/reference notes. |
| Full engineering artifact model | Routed to the UML note. |
| Full commit-bound VREC/RLS procedure | Routed to operational phasing, practical examples, and command reference. |
| Complete command reference | Moved to `harnessctl-reference.md`. |
| Safety and authority list | Condensed into responsibility prose and command-result boundaries; managed policy remains authoritative. |
| Installed repository tree | Moved to the contributor note where implementation structure is relevant. |
| Detailed safe-upgrade sequence | Moved to the installation note; root preserves the crucial two-stage distinction. |
| Release integrity, PR enforcement, and self-hosting bootstrap | Routed to development, branching, and phasing notes. |
| Source installation and distribution checks | Moved to the development/self-hosting note. |

No useful current responsibility was orphaned. Duplicated formal gate tables, full artifact catalogs, and repeated no-side-effect command lists were intentionally retired from the root rather than copied again.

## Requirement results

| Requirement | Result | Evidence |
| --- | --- | --- |
| `REQ-DST-024` | PASS | 123-line/8-section root retains value, safe start, authority, limitations, and routes at 6/10. |
| `REQ-DST-025` | PASS | Fenced root examples contain exactly `init`, `adopt`, `doctor`, `validate`, and `dashboard`; agent responsibilities remain explicit without agent-only syntax. |
| `REQ-DST-026` | PASS | Three expertise-labeled notes own installation/upgrade, complete CLI, and contributor/self-hosting detail; existing notes retain model, timing, Git, and examples; all local links resolve. |
| `REQ-DST-027` | PASS | Root states package update does not update managed repository content; the 5/10 note gives platform setup and read-only plan -> authorized apply -> doctor ordering. |
| `REQ-DST-028` | PASS | Short scenario, 8-node colored/fallback graph, responsibility table, Explorer value, two known limitations, and contributor route remain. |

## Exact automated verification

### Focused public documentation

```text
python -B -m unittest tests.test_public_onboarding tests.test_progressive_documentation
```

PASS: 27 tests, 0 failures, 0 errors. Assertions cover the line/section budgets, exact root headings, audience fit and assurance caveats, package/version metadata, five-command allowlist, agent-command exclusion, graph node budget and fallback, authority boundary, limitations, hidden expertise metadata, repository-relative internal root links, link graph, exact CLI inventory, safe-upgrade order, three self-hosting planes, current typed model, fictional-example boundary, and Markdown hygiene.

### Complete suite

```text
python -B -m unittest discover -s tests -p "test_*.py"
```

PASS: the final audience-integrated run completed 140 tests in 48.147 seconds, with 3 host-dependent skips, 0 failures, and 0 errors on Python 3.14.6. A local Python 3.11 runtime was not available, so no unsupported claim of a local 3.11 execution is made; project metadata remains `>=3.11`.

### Formal graph and installed integrity

```text
python -B scripts/validate_engineering_artifacts.py --root .
python -B -m se_harness doctor .
```

PASS: 263 artifacts, 0 errors, and the same 38 classified historical warnings (9 `W013` layout advisories, 14 `W014` legacy decision-assessment advisories, and 15 `W015` compatibility-relation advisories). Doctor passed required, distribution, managed, lock, seed, runtime, and self-hosting checks; the independently selected governor remains 0.2.1.

### Preflight

```text
python -B -m se_harness preflight . --work-order WO-DOC-008 --phase start --json
python -B -m se_harness preflight . --work-order WO-DOC-008 --phase review --json
```

Start preflight passed with the approved work order and complete 19-file manifest. Review preflight passed during implementation and was repeated with `WO-DOC-008` in `implemented`, the same manifest, and no diagnostics. Preflight remained derived read-only evidence.

### CLI, Markdown, Explorer, and diff

Help passed for `init`, `adopt`, `validate`, `dashboard`, `doctor`, `preflight`, `upgrade`, `scaffold-domain`, `create-artifact`, `identity`, `capture-verification`, and `prepare-release`. The reference table exactly equals the parser's subcommand choices.

Static scan found no Mokiterions marker, stale current-version claim, authority inversion, `ARCH.constrains` current-authoring claim, mojibake, replacement character, placeholder, TODO, or FIXME in the root and notes. All fences and local links passed focused tests.

Final Explorer generation passed with 263 artifacts, 891 relations, 0 errors, and 39 warnings: the 38 formal compatibility warnings plus the pre-existing stale-ready derived observation. The implemented-state snapshot is `387bab9d3701df1a3766b7b5dd7b4d842ccb8fee60025ab4cdb69af405464029`.

`git diff --check` passed. A direct diff across `.engineering-harness.toml`, `.engineering-harness.lock`, the workflow, managed router/policies, canonical templates, package/runtime source, and scripts produced no content. Windows LF/CRLF notices and the sandbox user's unavailable global ignore file were terminal-environment warnings, not content failures.

## Manual assessments

- **Public scan (6/10):** purpose, installation, new/existing repository choice, inspection commands, value, accountable roles, limitations, and next routes are discoverable without scanning an operating manual.
- **Human command surface:** the five root subcommands are memorable and have distinct outcomes; setup/version commands are clearly package operations.
- **Agent transparency:** the root still says that the agent drafts, runs preflight, implements approved scope, performs checks, retains evidence, and prepares ready records; it never suggests self-approval.
- **Upgrade safety (5/10):** the root prevents the package-equals-repository misconception, while the detailed guide makes apply explicitly owner-authorized and transactional.
- **Command reference (7/10):** every parser subcommand and key option has an actor, state-effect classification, and no-authority statement.
- **Contributor route (8/10):** released governor, candidate source, and candidate package are distinct; current 0.2.2 candidate versus 0.2.1 governor lag is explicit.
- **Graph accessibility:** eight labeled nodes, decision shapes, dotted observations, prose fallback, and supplementary-only color preserve meaning without rendered Mermaid.
- **Authority:** notes repeatedly route normative questions to managed policy and do not become a competing workflow.

## Deviations and residual risks

There is no approved requirement deviation. The final root is materially below, rather than close to, the 200-line ceiling; this preserves room for small essential updates without inviting a return to a manual.

After implementation, the repository owner requested that links from the root README to repository-owned notes use relative Markdown targets rather than absolute GitHub URLs. The six internal targets were changed and a focused regression assertion was added; external PyPI, repository, issue, and release destinations remain absolute. Relative links are correct inside the repository but may resolve under `pypi.org` when the same long description is rendered on PyPI, so package-index navigation remains a known presentation risk under the requested convention.

The repository owner then classified expertise scores as internal documentation metadata. Every public/notes score remains deterministically available in an HTML comment immediately below its title but is absent from rendered prose and notes-index tables. The root learning link now says `overview` rather than `4/10 overview`; focused tests strip comments and reject any visible score notation.

The repository owner subsequently approved a concise `Who it is for` section. It identifies agentic, audited or high-impact, cross-repository governance, and long-lived-project audiences; states that throwaway or requirement-discovery experiments may not justify the discipline; distinguishes solo traceability from independent assurance; and explicitly rejects any claim that the harness itself certifies regulatory compliance. Its 5/10 reader metadata remains hidden in an HTML comment.

Scanability and persuasion remain qualitative despite structural tests. GitHub and PyPI may render Mermaid differently. External project state can change. The managed-gates/Explorer grouping mismatch and routine-architecture/work-order-schema tension remain unresolved behavior risks and are still disclosed. Future CLI additions require a synchronized command-reference test update. The line guard could encourage over-compression, so reader review remains necessary.
