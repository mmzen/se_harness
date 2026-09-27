# Proposed packaging scope correction

Selected work: WO-IAR-015, already in progress. No additional implementation
path is authorized by this proposal.

The existing development builder in `repository_tools/plugin_distribution.py`
rejects every package containing a `hooks/` path or a hooks manifest field.
`scripts/build_plugin_archives.py`, which WO-IAR-015 permits, delegates to that
builder. Changing only the wrapper would leave direct callers and acceptance
checks inconsistent.

Authorize one additional bounded work order, reusing REQ-IAR-026,
SPEC-IAR-014, ARCH-IAR-011, ADR-IAR-011 and VER-IAR-014, for:

- `repository_tools/plugin_distribution.py`: accept the reviewed startup and
  compaction instruction-delivery assets; validate their event configuration and
  referenced packaged script before writing archives.
- The existing `tests/plugin_integration/package_assembly/` and
  `tests/plugin_integration/test_simple_plugin.py` paths: verify accepted delivery
  packages and refusal of malformed, missing or unsupported hook assets.
- The new work order's own record and evidence directory.

Retain wheel identity checks, release/development separation, output ownership,
and refusal before writes. No package publication, real user configuration
change, new lifecycle authority or release decision is included.

The current source is unchanged. The proposed work removes a packaging barrier
to the already approved host-delivery design; it does not establish native host
qualification by itself.
