# Clear technical communication for operators and artifacts

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

SE Harness installs one managed technical-communication policy. It helps agents
write direct English prose without changing engineering authority or technical
meaning.

The policy uses selected clarity principles based on ASD-STE100. SE Harness does
not claim compliance, certification, approval, or endorsement. The agent does
not download or try to reproduce the external standard.

## What the policy changes

For eligible prose, an agent uses consistent terms, identifies responsible
actors, states conditions and results directly, and avoids vague references.
The agent can use two profiles:

- `operator-communication` for concise, action-first explanations; and
- `technical-artifact-writing` for narrative parts of draft requirements,
  specifications, architecture, work orders, and verification contracts.

The profiles guide composition. They are not automatic formatters. They do not
authorize a style-only rewrite of approved or historical artifacts.

## What the policy protects

Exact protected content stays byte-identical. Examples include code, commands,
paths, identifiers, hashes, versions, machine data, logs, evaluator results,
quotations, and canonical lifecycle blocks.

Semantically protected content is not automatically paraphrased. Examples
include normative obligations, lifecycle meanings, acceptance thresholds,
safety qualifications, formulas, and established project terms.

If the boundary is unclear, the agent preserves the source and asks for one
meaning or terminology decision. A readability improvement never justifies a
weaker requirement or a changed command.

## Using `harness-operator-brief`

The installed portable core is
`.agents/skills/harness-operator-brief/`. Invoke it by exact name and supply:

- the repository and exact released-evaluator identity;
- one requested explanation and its non-effects;
- a current structured harness result or bounded technical text;
- the source digest and ordered protected-content declaration; and
- optional repository-approved project terms.

The skill checks evaluator identity and installed integrity. It composes one
English brief under `operator-communication`, then validates every protected
binding with `scripts/check_brief.py`.

The result and execution receipt are returned inline. The skill changes no
repository path and retains no target evidence.

Use `harness-orient` when the requested brief needs current repository or
artifact state but no current structured evaluator result was supplied.

## Boundaries

The policy and brief skill do not:

- decide or apply lifecycle transitions;
- approve, implement, verify, integrate, or release work;
- mutate the repository or Git;
- use credentials, a network, or an external service;
- prove that prose is technically correct or semantically equivalent; or
- claim ASD-STE100 compliance.

The managed policy at
`docs/engineering/TECHNICAL_COMMUNICATION.md` is authoritative for these
communication rules. The skill and this note only explain and apply that policy.

## Contributor checks

When changing this capability:

1. keep the canonical policy and skill under
   `templates/repository/standard/`;
2. preserve the existing four skill cores byte for byte;
3. test installation and upgrade in isolated targets;
4. run protected-byte, activation, offline, package, and no-write tests; and
5. review representative output for unchanged actor, condition, force, scope,
   qualification, and result.

Human review remains necessary for meaning. It does not certify the external
standard.
