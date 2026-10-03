# Capacity and publication correction review

The approved correction now uses exactly 4,194,304 topology bytes. One constant
and two test assertions changed; the released legacy-root assertion is preserved.
The existing strict boundary test passes below, at and above the target.

The implementation branch and assessed PR merge both measure 2,101,199 topology
bytes, leaving 2,093,105 bytes of headroom. Each repeat is byte-identical.
Both contain 1,885 artifacts and 7,189 relations. No data was removed.

Windows and Linux each pass the 115 focused tests (one Windows skip). The full
Windows suite passes 1,259 tests with 22 skips. Hosted Linux source passes the
same suite with two skips. The CI wheel was installed into an isolated disposable
environment; its installed target and boundary behavior pass. This is a test
wheel, not a replacement for the approved release archive.

All eleven archived predecessor hashes and amended-file links match. The manual
exception records mmzen's actual instruction; it does not claim native evaluator
revision support. Old rollout measurements in the revised files remain historical,
as their dated revision sections explain. VER-DST-030 governs this correction.

Seven protected release inputs match their original hashes. RLS-SEH-032 remains
bound to abbec12ac5524c8adfb28693f846dd59de88f759. The earlier publication resolver,
Pages rehearsal and exact archive replay remain retained under WO-RLO-018.

The original 2 MiB failure remains retained. This evidence also retains the
incorrect multi-ID scope invocation, the Linux clone-origin fixture failure and
the hosted missing-handoff failure. The corrected local combined PR check passes.
All hosted checks at e72ebc26f26dfde646835c2cb7fa0047776d828a now pass, including governance, both upgrade rehearsals, both integration-package installations and publication replay. See completion.json. No human assurance is inferred.

Design review: a fixed value and the existing boundary tests meet the approved
capacity need. No sharding, serializer, workflow, hard budget or dependency change
is needed. A further increase requires a new decision. The complete original
predecessors are in accepted-predecessors.zip; amendment.json links their hashes.

See execution.json for commands, runtimes, commits, results, measurements,
availability and preservation hashes. VREC-RLO-015 preparation follows the completion transitions and a fresh test of the exact committed candidate. Its later record supplies that exact candidate and result.
