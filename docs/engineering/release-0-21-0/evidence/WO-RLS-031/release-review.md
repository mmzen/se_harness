# RLS-SEH-031 release decision review

Human mmzen verified VREC-SEH-031 with “I verify VREC-SEH-031”. The released
0.20.1 evaluator recorded that decision. The candidate and every bound evidence
file matched the reviewed inputs before the transition.

RLS-SEH-031 is now **ready**, not released. It binds:

- Version and selected tag: **0.21.0 / v0.21.0**.
- Candidate: **4031f0fa4b5c4a95651bd928a110d8b2d94f9775**.
- Contract: REL-SEH-033; verified coverage: VREC-SEH-031.
- Work: exactly the thirteen approved release members.
- Ready record SHA-256: `063a260cd9737e82c27ff9e6d6f122423b7e750b38aef56d5020a67af0e7721c`.
- Evaluator evidence SHA-256: `e5148d268c5741a14613a371672929daa845983733cf8ee1439f3f3b60b4bb8b`.

## Build binding and replay

The final build manifest and record bind the same schema-2 recipe:

| Distribution | SHA-256 |
| --- | --- |
| se_harness-0.21.0-py3-none-any.whl | 13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789 |
| se_harness-0.21.0.tar.gz | f1db9d80acf8ee86ea53b53c64c0f4d25db6fd99c58f903dd841d13f95cca98b |

[Bound-record replay](https://github.com/mmzen/se_harness/actions/runs/36965921824)
passed from review commit 6461f18e8c5717850fe7f6625114d2c70445c810. Both clean
builds reproduce the candidate and hashes in RLS-SEH-031. The downloaded full
receipt is bound-record-replay.json. This read-only workflow created no tag,
release, index entry, deployment or lifecycle decision.

Graph validation, all 21 distribution-bearing records, PR scope checks and the
release-transition gates pass. release-preparation.json retains the actual
commands and results, including two harmless binder refusals for absolute paths
before the required repository-relative paths were supplied. Neither refusal
changed the record. No implementation or accepted definition changed.

## Accepted limitation and recovery

Codex Windows desktop remains unverified. DEC-RLS-001 and RISK-RLS-001 retain
mmzen's limited acceptance for this release. CLI evidence does not establish
desktop support. Revisit before a later release, a verified desktop-support
claim, or adoption that relies on desktop replacement delivery.

Before publication, a failed check requires bounded correction. Changed candidate
bytes require fresh build and verification. After publication, preserve immutable
archives and tags; correct defects in a separately reviewed version. Inspect
uncertain external effects before any retry.

## Next human decision

**I authorize release record RLS-SEH-031.**

This is the reserved exact-record release decision. The original request to
publish v0.21.0 remains retained for its matching publication after integration
and provider controls. This review does not supply merge or protected-environment
approval. Marketplace publication, public observation, latest/last markers and
separate repository adoption retain their own work and required decisions.
