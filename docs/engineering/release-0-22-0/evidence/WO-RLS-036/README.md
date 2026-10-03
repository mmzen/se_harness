# Public delivery of evaluator 0.22.0 and plugin 0.2.5

Plugin 0.2.5 is published at [`7d30907f15bd7e06fb632e1ebf4e88e01b68726c`](https://github.com/mmzen/se_harness/commit/7d30907f15bd7e06fb632e1ebf4e88e01b68726c).
Human mmzen verified package qualification in VREC-PLG-032. The ordinary marketplace
push preserved its expected parent. Independent public download matches all 69
qualified files, including both host packages and the exact public evaluator wheel.

| Check | Result |
| --- | --- |
| Codex CLI fresh install | Passed; all 29 installed files match the qualified package. |
| Codex CLI update from public 0.2.4 | Passed; prior public revision and installed bytes checked first. |
| Offline setup on both routes | Passed; evaluator identity, two-file initialization, doctor, resources and reuse. |
| Codex CLI native qualification | Reused verified VREC-PLG-032 evidence after exact package and host-version comparison. No fresh-profile model session claim. |
| Claude Code installation/update and native sessions | Not tested / unverified, under DEC-RLS-005/006. |
| Codex Windows desktop | Not tested / unverified, under DEC-RLS-005/006. |
| PyPI identities | Current wheel and sdist digests match RLS-SEH-032. |
| Pages provenance | Current public manifest matches the released candidate and governance commit. |
| Documentation and release markers | In progress; no complete-delivery claim. |

Read [public route observations](public-routes.json), [publication receipt](publication-receipt.json)
and [independent public readback](public-readback.json). [Raw evidence](public-routes-raw.zip)
retains actual commands and outputs. Setup's initial nonzero exit is the expected
missing-selection report in an empty fixture; subsequent initialization and checks
passed. The publication helper's initial gate-result lookup error stopped before
any external write and is retained with its correction.

RISK-RLS-006 remains an unfixed evaluator limitation discovered during qualification;
its tested workaround and original failure remain in the VREC-PLG-032 evidence.
The accepted host omissions do not claim that defect is fixed or separately accepted.

Normal host profiles and repository selection remain unchanged. This repository
still uses released evaluator 0.21.0. Public package bytes and previous bound
evidence are preserved. Documentation verification, merge/readback and authorized
latest/last promotion remain before overall delivery can be complete.
