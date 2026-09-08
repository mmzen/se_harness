"""The evaluator's engine: the graph validator, the Explorer generator and the inspector.

An import surface of the package since WO-ECP-034 (SPEC-ECP-024 ECP-ENG-001 to
ECP-ENG-003): the CLI, preflight, the workflow, provenance and qualification import
these modules; the modules import their siblings and the package by name; each entry
module also runs as ``python -m se_harness.engine.<name>`` with its arguments, output
formats, exit codes and diagnostic codes unchanged (SPEC-DST-025 DST-ENG-007). The
layout tables live in ``se_harness.artifact_layout``.
"""
