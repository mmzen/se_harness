# Distributing SE Harness skills as a coding-agent plugin

<!-- Target expertise: 5/10. This score describes the knowledge expected from the reader, not the document's complexity or quality. -->

> This is a non-authoritative exploration note. It approves nothing, authorizes
> no implementation, delegates no decision, and changes no lifecycle state.
> Formal authority comes from `ENGINEERING_HARNESS.md`, its managed policies,
> and approved artifacts under `docs/engineering/`.

## Why this note exists, and why it is not a roadmap phase yet

Today SE Harness makes its agent skills available by installing them into a
repository. Both supported hosts, Codex and Claude Code, now also have their own
way to install and update software directly: a **plugin**. A plugin is installed
once on a machine or account and is then available in every project, and it
updates on its own schedule instead of through a repository upgrade.

The obvious question is whether SE Harness should ship as a plugin. This note
records what such a move would involve, so the question can be answered later
from written analysis rather than from memory.

It is deliberately **not** part of the
[agentic execution roadmap](agentic-execution-roadmap.md). Three reasons:

- The repository-scoped path it would replace was only just built, and the
  approved decision that built it says plugin distribution stays a separate
  opt-in choice made **after** the repository-scoped path is proven. Very little
  operating experience exists yet.
- The largest piece of work is not the plugin itself. It is a second way of
  publishing software, and today the project has exactly one carefully governed
  publication path.
- Host plugin features are young and still changing. Any plan written now would
  need re-checking against the hosts before it could be trusted.

So: worth understanding, too soon to schedule.

## What the current design does

Four skills exist: `harness-orient` for read-only understanding, and three
explicit-only writing skills for drafting, implementing an approved work order,
and preparing assurance material. The
[skills MVP note](agentic-execution-skills-mvp.md) describes what each one does
and where it stops.

Each skill is installed into the repository as a managed file, and its exact
bytes are recorded in the repository lock. `doctor` then notices if anything
changed. Codex reads the skills directly; Claude Code reads a small same-named
file that points at them, as described in the
[host adapters note](agentic-execution-host-adapters.md).

Three properties of that design matter here, because they decide how expensive a
plugin would be.

**The skills hold no authority.** They read repository state and run the
released evaluator, which is the exact published version of the tool installed
outside the checkout. The evaluator decides what is legal and what the next step
is. The skills only carry out a procedure and report the result. A plugin would
inherit no authority either, so no part of the authority model has to be
redesigned.

**The evaluator is already outside the repository.** Every skill is *given* the
command that starts the evaluator, along with the version and location it should
be. No skill is allowed to look for one inside the checkout or on the system
search path. A plugin changes who supplies that command, not what the skill
expects.

**Skill integrity does not depend on the repository.** The tool can already take
any folder of skill files and produce a single fingerprint for it, with no need
for Git, the lock, or even a repository. The lock is simply where that
fingerprint happens to be written down today. This is the most useful fact in
the whole note: it means a plugin can keep the same integrity guarantee without
inventing a new one.

## What the two hosts now offer

Both hosts have arrived at nearly the same plugin shape: a small manifest file
in a host-specific folder, skills in a `skills/` folder, and optional **hooks**,
which are commands the host runs at fixed moments, such as just before a file is
written. Both hosts can let a hook refuse the action. Both also let a plugin
carry tool servers. Both require the user to trust a plugin's hooks explicitly
before they run, and both warn that hooks are a useful guard rather than a
complete barrier.

Two limits are helpful rather than annoying:

- Neither host lets a plugin grant itself permissions. A plugin cannot widen
  what the agent is allowed to do. The current design asks for that in prose;
  the hosts now enforce it.
- Claude Code reads a plugin's own settings only from user-level configuration,
  not from per-project files. So per-repository values cannot be supplied
  through plugin settings.

The practical consequence is that one set of skill files plus two small
manifests could serve both hosts.

Because these features are new, treat every statement in this section as
something to re-verify before use, not as a fixed fact.

## The four things a plugin would invert

| What changes | Why it matters |
| --- | --- |
| **Who installs the skills.** Today the harness writes them into the repository and locks their bytes. A plugin is written by the host, outside the repository, and updates on its own. | The repository lock and `doctor` would no longer see the skills. Something has to check them instead. The fingerprint mechanism already exists; what is missing is a command that verifies a folder the tool did not install. |
| **One plugin, many repositories.** Each repository pins one exact evaluator version. A single installed plugin faces many repositories pinning many versions. | The skills must work out which evaluator a given repository needs, then find or fetch it. Today a person supplies that. This is the hardest problem in the whole idea. |
| **Where the skills appear.** Installed in a repository, they appear only where the harness is installed. As a plugin, they appear everywhere, including projects that have no harness. | The skills need to notice a project that is not a harness repository and quietly decline, with no error noise and no effect. |
| **What the channel can carry.** Today the host-specific files grant nothing at all. A plugin can also carry hooks and tool servers. | This is both the prize and the risk. See below. |

### The prize, and the line that protects it

A hook that can refuse a file write is the first mechanism available to this
project that *prevents* work outside an approved scope, instead of asking an
agent not to do it. The roadmap wants that in a later phase and cannot get it
from written procedure alone.

The risk is that a plugin carrying skills, hooks, and a tool server starts to
look like a second control plane, deciding things the evaluator is supposed to
decide. One rule keeps that from happening, and it should be written down before
any code is:

> A plugin may carry, display, and enforce a decision the evaluator made. It
> may never make one itself.

A hook that works out for itself whether a path is in scope has moved lifecycle
judgement out of the tool, which the harness contract forbids. A hook that asks
the evaluator and then acts on the answer has not.

A related rule: a plugin should not put an evaluator-like command on the system
search path. The skills are specifically forbidden from picking up an evaluator
that way, because it is impossible to tell which one you got. Adding one would
recreate exactly the confusion the tool's identity checks exist to catch.

## What it would touch

Governance is the larger half, and the current approved text rules a plugin out
on purpose. That text was written knowing this question would return.

| Area | Situation today | What would be needed |
| --- | --- | --- |
| The decision that chose repository-scoped adapters | Considered global and plugin distribution and rejected it for now | A new decision record revisiting that choice on new evidence. A verified decision is not edited. |
| The requirement behind the installed skills | States that plugin-marketplace installation is outside its scope | A companion requirement, not a change to the existing one |
| The specification behind them | Says plugin distribution may be proposed later, and must either keep the exact skill names or resolve the naming change on purpose | The naming question has to be settled first, because one host prefixes plugin skill names with the plugin name |
| The architecture for agentic execution | Leaves open whether the first distributed integration is repository files, a plugin, or both | This is the decision being made |
| The roadmap's own adapter phase | Proposes generating host files *into* the repository | A different answer to the same question. One has to be chosen; doing both recreates two sources of truth. |

Roughly: one decision record, a couple of requirements and specifications, their
verification contracts, and three or four bounded work orders with their
evidence and verification records.

On the software side:

| Area | Effect |
| --- | --- |
| Skill contract handling | Add the ability to verify a skill folder that lives outside a repository. Small, because the fingerprint logic is already independent of location. |
| Command line | Two new commands: verify a skill folder, and report which evaluator a repository needs. |
| Installer and lock | The bigger question. Either the skills leave the lock, and `doctor` stops covering them, or they stay and are covered twice. Changing what the lock covers is a format migration. **This is the riskiest item.** |
| Publication | A plugin is a **second** release channel, with its own versioning and its own trust model. Today every governed publication is a Python package or the published Explorer demonstration. Nothing in the release tooling knows about anything else. **This is the largest genuinely new piece.** |
| Tests | Six existing test files mention the skills or the host files, plus the recorded fingerprints and the recorded list of expected host files. New tests are also needed for real host behaviour, not only for file contents. |
| Line-ending rules | The skill folder would gain new file types. The repository's byte-exactness rules have to name them, or a Windows checkout silently presents different bytes. This has caught the project before. |

What would **not** change is worth stating plainly: the artifact graph and its
validator, the workflow contract and its canonical restitution, the quality
gates, the decision rights, the evaluator's own identity checks, and how
verification and release records bind an exact commit. That containment is the
whole reason this is a change at the edge rather than a rewrite.

## One choice that keeps the cost small

The exact bytes of the read-only orientation skill are pinned by three approved
artifacts at once. Its published identity cannot drift without a governed
decision to retire it.

That points at a specific design: **keep all four skill files byte-identical**,
and put every plugin-specific concern in the manifests, the hooks, a small
resolver script inside the plugin, and one new command in the tool. This works
because the skills already require the evaluator command to be *supplied by
whoever calls them*. A resolver that reads the repository's own configuration
and looks up a matching evaluator in the plugin's data folder is neither a
checkout search nor a system-path search, so it stays within the current rules.

Chosen deliberately, this collapses the fingerprint, contract-version, and
re-verification work to almost nothing. Discovered late, it is a re-verification
of every skill.

## A possible order of work

Each stage ends at a decision, not at a deliverable.

**Stage 0 — decide, build nothing.** One decision record answering five
questions: whether the plugin is installed per user or committed per project;
who holds the integrity record; which plugin features are allowed at all;
how the right evaluator is found and who may install it; and how the skill names
survive the host's naming rules. Cost: a review packet.

**Stage 1 — the near-free version.** Both hosts can treat an existing skills
folder as a plugin by adding a small manifest beside it. Nothing leaves the
repository, nothing leaves the lock. In exchange the project gains a manifest
check it can run in CI, and per-project switching off. This is where the real
degree of similarity between the two hosts gets measured, before a release
channel depends on it.

**Stage 2 — publish it, keep authority where it is.** One skills folder, two
manifests, distributed through each host's plugin channel. Requires the three
new pieces: verifying a folder the tool did not install, working out the right
evaluator per repository, and declining quietly outside a harness repository. No
hooks yet. Gate: does a plugin-supplied skill produce the same result as a
repository-installed one, on both hosts, on Windows and on Linux?

**Stage 3 — migrate existing repositories.** One-way order only: the plugin is
available and proven first, and only then does an explicitly authorized upgrade
remove the repository copy. Never the other way round. The project already has a
no-network rehearsal for handovers between tool versions; reuse it.

**Stage 4 — the enforcement hooks.** Refuse writes outside an approved scope by
asking the evaluator and acting on its answer. This is the point of the whole
exercise. The claim must stay modest, because both hosts describe hooks as a
guard rather than a barrier.

**Stage 5 — pilot, then self-host,** in the order the roadmap already sets out:
throwaway repositories, then low-risk real ones, then repositories with their own
policies, then both hosts side by side, and this repository last.

## What would make this a bad idea

- **Finding the right evaluator may not be solvable cleanly.** If a plugin
  cannot reliably locate and verify a version-correct evaluator on Windows and
  Linux without silently installing one, which the current specifications
  forbid, then the plugin is only prose telling the user to run the tool by
  hand. That is no better than today, and it is no longer covered by the lock.
  Prove this before Stage 2, not during it.
- **A second control plane by accident.** Skills, hooks, and a tool server in
  one package drift toward deciding things. The carry-never-decide rule has to
  be an approved constraint, not a habit.
- **An under-governed second channel.** Publishing to a plugin channel is easy;
  making it reproducible and bound to an exact commit is not. The failure mode
  is a plugin that is less governed than the package it fronts.
- **"It works right after installing" stops being true** once hooks are
  involved, because both hosts ask the user to trust hooks first. Any promise
  about default availability has to be restated feature by feature.
- **Host features move.** Anything written here about plugin behaviour needs
  re-checking at the time of use.

## Where this sits

The roadmap's adapter phase asks the same question and currently prefers
generating host files into the repository. This note describes the alternative.
Neither is approved. Choosing between them is Stage 0 above, and it belongs to
accountable owners working from formal artifacts, not to this note.

## See also

- [Agentic execution roadmap](agentic-execution-roadmap.md) — the staged plan
  this note is not yet part of
- [Single-agent workflow skills MVP](agentic-execution-skills-mvp.md) — what the
  four skills do and where they stop
- [Repository host adapters](agentic-execution-host-adapters.md) — how the two
  hosts find the skills today
- [Installation and safe upgrades](harness-installation-and-upgrades.md) — the
  repository upgrade path a plugin would sit beside
