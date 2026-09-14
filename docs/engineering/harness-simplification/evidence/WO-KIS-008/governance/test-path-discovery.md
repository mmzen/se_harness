# Test paths discovered during the accepted modification

The full suite found two existing expectations affected by the approved template and
router changes: `tests/test_artifact_catalog.py` compares the work-order template with
the released root, and `tests/test_context_routing_retirement.py` fixes the routing-table
label. These exact files are added to the implementation path list to update those
expectations. This is necessary verification work within the owner's accepted modification;
it introduces no additional product behavior, lifecycle decision or approval claim.

The earlier failed run also overlapped a policy wording edit. Three fixture comparisons
failed with the old cached policy. Retain that failed result and rerun against settled files.
