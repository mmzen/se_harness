+++
id = "DEC-HAG-002"
type = "decision"
title = "Bounded linked revision of the hosted evaluator selection"
status = "decided"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
kind = "question"
question = "Should the exact two-file HAG evaluator amendment use an explicitly authorized bounded manual linked revision, or wait for a released amendment mechanism?"
raised_by = "Codex"
recommendation = "bounded-manual-revision"

[[options]]
id = "bounded-manual-revision"
label = "Explicitly authorize only the reviewed SPEC-HAG-003 and VER-HAG-001 replacements, preserving accepted bytes and recording the human decision and manual activation."

[[options]]
id = "released-mechanism"
label = "Keep accepted HAG definitions unchanged and prepare a separately approved released amendment capability before resuming dependent work."

[relations]
concerns = ["SPEC-HAG-003", "VER-HAG-001", "WO-HAG-001", "WO-HAG-005", "VER-HAG-004"]
blocks = ["WO-HAG-005"]

[disposition]
option = "bounded-manual-revision"
label = "Explicitly authorize only the reviewed SPEC-HAG-003 and VER-HAG-001 replacements, preserving accepted bytes and recording the human decision and manual activation."
decided_by = "mmzen"
decided_at = "2026-10-05T12:40:28Z"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-005 / VER-HAG-004 request, including DEC-HAG-002 bounded-manual-revision for the exact SPEC-HAG-003 and VER-HAG-001 replacements, required commit-bound verification, and ordinary updates to draft PR #535 in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs, including ready-record review and the later separately supplied verification decision. The review binding SHA-256 is 2dd5104adee7a1f8cc94df384ae62f6cbc0169448d91dae738dedb7292acab0a. Earlier accepted bytes and lifecycle history are preserved. This is an explicit bounded manual amendment authorization; it grants no general amendment mechanism, verification acceptance, risk acceptance, merge, release or deployment. No machine lifecycle rule or required gate is waived."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-05T12:40:28Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-005 / VER-HAG-004 request, including DEC-HAG-002 bounded-manual-revision for the exact SPEC-HAG-003 and VER-HAG-001 replacements, required commit-bound verification, and ordinary updates to draft PR #535 in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs, including ready-record review and the later separately supplied verification decision. The review binding SHA-256 is 2dd5104adee7a1f8cc94df384ae62f6cbc0169448d91dae738dedb7292acab0a. Earlier accepted bytes and lifecycle history are preserved. This is an explicit bounded manual amendment authorization; it grants no general amendment mechanism, verification acceptance, risk acceptance, merge, release or deployment. No machine lifecycle rule or required gate is waived."
+++

# Bounded linked revision of the hosted evaluator selection

## Facts and proposed change

Released 0.22.1 includes the independently verified draft-admission and actual
decision-maker fixes. Main has adopted it. The HAG branch and its two accepted
definitions still pin 0.22.0. DEC-HAG-001's extend-evaluator choice is already
given; this question does not ask for that choice again.

The released AMEND_DEFINITIONS procedure requires a linked revision, retained
accepted bytes and a recorded human decision/activation. Both 0.22.0 and 0.22.1
still lack the supported revision command and relation. Ordinary work approval
cannot be treated as an amendment exception. Replacement text stays transient
and the two accepted files are unchanged pending explicit instruction.

The proposal selects public evaluator 0.22.1, fixes its wheel and payload digests,
uses unpublished client/plugin identities, and re-runs the independent oracle.
All twelve scenarios, historical source, image pins, scope and Cypher risk remain.

## Exact reviewed versions

Accepted source commit: `64b4feb0cbaff06111876a1d4c0cc35a6c814415`.

- SPEC-HAG-003: accepted SHA-256 `e6ea2418a6e4a734dc160c30676742b4afa11cf7784bbe010ce69118b9025499`; proposed replacement SHA-256 `411ea506a1ce9ee8de0bf6b34ba095dc0ce39186acac7796f4e2bad2ff3975bb`; preserved path `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-005/SPEC-HAG-003-accepted-before.txt`.
- VER-HAG-001: accepted SHA-256 `744ca93c38acbed841db2047c15017d417bbfb95efead8a41ccdd911b7653dac`; proposed replacement SHA-256 `7e717148ddee865126b2ffb935b3e348a56321654007ce9abf19d3f2d8df6f6d`; preserved path `docs/engineering/hosted-artifact-graph/evidence/WO-HAG-005/VER-HAG-001-accepted-before.txt`.

The amendment proposal includes the complete before/after files and patch.
Previous bytes will be retained as `.txt` evidence, avoiding duplicate formal
artifact IDs. The replacements link those exact bytes and this decision. No
new typed relation or fabricated lifecycle event is proposed.

## Options and recommendation

`bounded-manual-revision` requests an explicit one-time user instruction to
depart from the missing-command stop in the amendment procedure for these
exact replacements. Record the actual human answer using released `decide`.
Under approved WO-HAG-005, preserve the originals, apply the reviewed bytes,
and retain an amendment record with the actual decision, old/new digests,
affected work and activation time. Earlier evidence keeps its original binding.
All lifecycle transitions, validation, scope and verification gates still apply.
This is not an implementation of a general harness exception or amendment API.

`released-mechanism` keeps the HAG amendment pending while a new bounded product
package defines, implements, qualifies and releases the missing capability.
That avoids a manual operation but adds a product/release/adoption dependency.
No implementation or release of that option is authorized by this proposal.

Recommend the exact manual route for this two-file dependency, following the
preservation pattern used for REL-SEH-035. That earlier authorization does not
authorize this one; mmzen must decide explicitly. This decision does not verify
work, accept RISK-HAG-001, or authorize public release, deployment or merge.
