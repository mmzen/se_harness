# Retained runner assertion defect

All nine original setup commands and sixteen correction/capture commands ran
with their expected exit statuses and observed mutation paths. This includes
the original fixture's invalid verification-method enum refusal and the later
successful real Linux capture of a ready VREC.

The additional Python assertion after capture incorrectly looked for
`revision.commit`; the actual released VREC stores `commit` at the top level.
The resulting `KeyError: revision` is a runner defect, not a candidate skill or
evaluator failure. The raw capture result and actual prepared files are retained.
The assertion was corrected to the observed schema, and a new full replay starts
in sibling `plugin-linux-evidence-replay-20260911-attempt2`.
