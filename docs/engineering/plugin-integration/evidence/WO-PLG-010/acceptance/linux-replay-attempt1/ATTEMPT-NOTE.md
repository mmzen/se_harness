# Retained runner defect

The first Linux replay retained 47 real command records through the work-order
handoff. Its final extra commit-count assertion used `main..HEAD`. This fixture
commits on local `main`, so the observed count was correctly zero. The test
assertion was wrong; this is not a change-skill or evaluator failure.

The runner was corrected to compare `origin/main..HEAD`, because setup fixes
that remote-tracking ref at the disposable baseline. A new full run in sibling
`plugin-linux-change-replay-20260910-attempt2` completed successfully and observed
two commits. This first directory and its raw results remain unchanged.
