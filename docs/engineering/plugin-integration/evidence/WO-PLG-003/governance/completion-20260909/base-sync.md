# Synchronization after completion

The completion transition was applied under the branch's released 0.16.0
evaluator. Main had meanwhile advanced to
`c63282b746e7a16a48b18c05606dcca57076a795`, whose managed root uses 0.17.0.

The first Codex PR checks compared a merge containing that newer root against
the old base `4ea947be4fb94e4d0ff137e8f0a3cf6148e3ba3a`. The
[scope check](https://github.com/mmzen/se_harness/actions/runs/34383069688)
reported `.engineering-harness.lock` outside the probe's scope; the
[predecessor assessment](https://github.com/mmzen/se_harness/actions/runs/34383069641)
also could not resolve the newer release from that old base.

The probe branches were synchronized with current main. Managed files come
from those existing main commits, without a local installer upgrade or scope
waiver. Fresh repository checks use the exact released 0.17.0 evaluator.

The original host probes and completion decision still describe their recorded
0.16.0 evaluator. Their evidence is preserved; checking the synchronized
repository does not claim a new live-host probe of 0.17.0 or another completion
decision.
