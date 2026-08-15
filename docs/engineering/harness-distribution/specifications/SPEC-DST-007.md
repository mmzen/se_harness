+++
id = "SPEC-DST-007"
type = "specification"
title = "Concise public entry point and relocated reference contract"
status = "approved"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-15"

[relations]
specifies = ["REQ-DST-024", "REQ-DST-025", "REQ-DST-026", "REQ-DST-027", "REQ-DST-028"]
+++

# Specification: Concise public entry point and relocated reference contract

## Scope

Transform the 523-line root README from a combined public page and operating manual into a concise human-facing entry point, while relocating still-useful operational and contributor detail to expertise-labeled notes. Preserve current behavior, authority boundaries, version facts, and the progressive documentation system created by `WO-DOC-007`.

## Reader and information budget

`README.md` remains `Target expertise: 6/10` and must contain no more than 200 physical UTF-8 text lines, including blank lines and fenced content. Its primary readers are repository owners, evaluators, adopters, assurance/release stakeholders seeking orientation, and contributors seeking the correct deeper route.

The recommended root structure is:

1. title, expertise label, concise value proposition, and project links;
2. `Install or upgrade`;
3. `Start using it`;
4. `What this looks like in practice`;
5. `What you get`;
6. `Who does what`;
7. `Known limitations`;
8. `Learn more`;
9. `Developing SE Harness`.

Exact headings may vary only to improve plain-language navigation. Keep at most nine level-two sections. The final order must let a new reader understand value and start safely before encountering deeper architecture or contributor detail.

## Installation and upgrade contract

The root provides a minimal released-PyPI path using Python 3.11 or later, a virtual environment, `python -m pip install se-harness`, and an exact-version example synchronized with package metadata. It may use one platform-neutral example and link platform-specific activation and launcher locations to `docs/notes/harness-installation-and-upgrades.md`.

Within the same `Install or upgrade` section, a short existing-installation notice must state:

- updating the package in a virtual environment does not modify an initialized or adopted repository;
- repository-managed-content upgrade is a separate planned and explicitly applied operation;
- customization preservation and transactional failure behavior are explained in the linked note.

Do not place the detailed `upgrade --apply` sequence in the root README.

## Human-facing command contract

Fenced root examples may use these ordinary target-repository subcommands:

```text
harnessctl init
harnessctl adopt
harnessctl doctor
harnessctl validate
harnessctl inspect
harnessctl dashboard
```

They must explain `doctor` as installed-integrity inspection, `validate` as the gate-oriented formal graph check, `inspect` as a derived non-gating terminal summary of lifecycle attention, existing findings, and bounded non-authoritative suggestions, and `dashboard` as generation of a derived read-only Explorer. Successful inspection-report production does not imply graph validity, verification, or approval. Setup may additionally use `harnessctl --version`; it is not a repository subcommand.

The root must not include syntax for `preflight`, `upgrade`, `scaffold-domain`, `create-artifact`, `identity`, `capture-verification`, or `prepare-release`. These commands remain current and discoverable through notes. Their names may appear in concise explanatory prose only when necessary to identify the agent's lifecycle, but prefer role-level language over a list of mechanics.

## Public value demonstration

Retain one short user-centered example based on a realistic bounded change. It must show:

1. a human requests and reviews an outcome;
2. the agent drafts the engineering definition and waits for approval;
3. the agent implements only approved work, performs checks, and retains evidence;
4. the exact candidate commit is the subject of later assurance;
5. accountable verification and release are separate human decisions.

Replace the current large graph with one compact Mermaid graph containing no more than nine conceptual nodes. It must include human-approved outcome, definition, approved work, agent implementation, evidence plus exact candidate commit, human verification, human release, and Harness Explorer observation. Adjacent prose and labels must preserve meaning without Mermaid rendering or color.

## Responsibility boundary

Include one compact responsibility table or equivalent visual distinction:

| Participant | Root-level responsibility |
| --- | --- |
| Human owners | Intent, scope, significant decisions, evidence judgment, verification, release, and external authorization. |
| Coding agent | Drafting, preflight, implementation within scope, repository checks, evidence retention, and ready-record preparation. |
| Repository policy and hosting controls | Commands, Git strategy, required checks, permissions, deployment, and operating constraints selected by accountable owners. |

State that automation produces observations or proposals and never grants product, verification, release, publication, or deployment authority.

## Explorer and limitations

Describe Explorer by the questions it helps answer: why work exists, whether definition is connected, where anomalies exist, which revision is covered, and what derived readiness observations are available. Do not reproduce the complete formal gate table in the root.

Retain concise disclosure of both current 0.2.2 tensions:

- managed `QUALITY_GATES.md` and Explorer reuse G0-G5 for different groupings;
- typed architecture policy rejects fabricated routine coverage while the validator requires a non-empty work-order `architecture` relation.

Link detailed explanation to the relevant notes and identify managed policy as authoritative where applicable. Documentation must not imply either behavior is corrected by this work.

## Relocated documentation contract

Create these non-authoritative notes:

| Note | Expertise | Owned content |
| --- | --- | --- |
| `docs/notes/harness-installation-and-upgrades.md` | 5/10 | Windows, Linux, and macOS virtual-environment setup; launcher ownership; exact-version install; package versus repository upgrade; plan/apply/doctor sequence. |
| `docs/notes/harnessctl-reference.md` | 7/10 | All current subcommands, principal actor, read/write classification, intended phase, key options, authority boundary, and links to examples/policy. |
| `docs/notes/developing-se-harness.md` | 8/10 | Source and editable install, repository structure, checks, self-hosting governor/candidate-source/candidate-package planes, build/release boundary, and contributor routes. |

Each note must carry its exact `Target expertise: N/10` label and explain that the score describes expected reader knowledge, not document quality or complexity.

Update `docs/notes/README.md` so the primary 4/10-to-7/10 learning path remains comprehensible and the operator, command-reference, and contributor routes are separately discoverable. Reuse or tighten existing notes rather than copying their complete examples or policy explanations.

## Authority and source-of-truth rules

- `README.md` and `docs/notes/` explain; they do not authorize.
- `ENGINEERING_HARNESS.md` and its routed managed policy remain the governance sources.
- `REPOSITORY_CONTEXT.md` and product artifacts remain repository-owned.
- Implementation and tests remain inspected behavior evidence.
- If a fact was obsolete or duplicated rather than useful, record its intentional retirement in work-order evidence instead of relocating it mechanically.

## Content disposition

| Current root material | Required disposition |
| --- | --- |
| Platform launcher and activation detail | Move to installation/upgrade note. |
| `scaffold-domain` and `create-artifact` examples | Move to command reference; retain conceptual agent drafting only in root. |
| Five-minute command workflow | Root becomes a short responsibility narrative; detailed timing remains in operational phasing. |
| Full artifact model | Link simplified UML; retain only the compact value graph. |
| Full commit-bound VREC/RLS procedure | Link practical example and operational phasing. |
| Complete command reference | Move to `harnessctl-reference.md`. |
| Installed directory tree | Move to installation or contributor reference as appropriate. |
| Pull-request/self-hosting mechanics | Link branching and development notes. |
| Distribution source-install/check commands | Move to development note. |
| Release integrity detail | Summarize trust boundary and route to development/phasing material. |

## Verification and tests

Update focused standard-library tests to assert:

- root line count is at most 200 and level-two section count is at most nine;
- the expertise label, public links, PyPI install, exact synchronized version, virtual environment, init/adopt, doctor/validate/inspect/dashboard distinctions, scenario, compact Mermaid, responsibility boundary, Explorer value, known limitations, and deeper routes remain;
- fenced root command examples contain no agent-only harness subcommands;
- exactly one root Mermaid block exists and it has no more than nine declared conceptual nodes;
- all three new notes exist with exact expertise labels and required topic markers;
- every current CLI subcommand appears in the command reference and matches `se_harness.cli.build_parser()` choices;
- notes-index and local Markdown links resolve;
- removed headings and obsolete copied material do not reappear;
- all public Markdown is free of mojibake, placeholders, unbalanced fences, unsafe inline script, and false authority claims.

Run focused tests, the complete unit suite, formal artifact validation, doctor, start and review preflight after work-order approval, CLI help for all commands, deterministic Explorer generation, link inspection, `git diff --check`, and a protected-path audit.

## Explicitly unspecified decisions

Exact prose, Markdown wrapping, diagram style and colors, link wording, and allocation of content between existing and new notes are delegated within this contract. CLI behavior, managed policy, Explorer computation, templates, workflows, package metadata/version, release records, governor selection, Git configuration, external hosting controls, and consumer repositories are outside scope. This current contract was revised under `WO-DOC-012`; retained evidence and commit-bound records for earlier candidates remain historical facts and are not rewritten.
