"""The evaluator's own scripts (SPEC-DST-025).

The graph validator, the Explorer generator, the inspector and the artifact
layout registry live here and ship inside the wheel. They are run as
subprocesses by path (``se_harness.installer.engine_script``) with this
directory first on ``sys.path`` so their sibling imports resolve; they are
not an import surface of the package. Folding them into importable modules
is a later work order (complexity audit item #225).
"""
