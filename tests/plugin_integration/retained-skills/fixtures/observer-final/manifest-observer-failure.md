# Retained observer failure

The original acceptance manifest and provisional C05 receipt omitted the LF at the end of the retained canonical JSON serializer. Their portable_core_sha256 fields therefore fail the retained manifest contract. Original files and scripts remain unchanged. This is an observer implementation defect, not an observed product defect. All independently fixed raw SKILL/helper/contract/YAML identities were verified correctly before execution, and all actual evaluator/helper invocations used those exact sources.

The correction follows the preexisting `_json_bytes` rule in the retained orient helper: compact sorted UTF-8 JSON plus one final LF. It is not derived from the helper's observed digest alone. Corrected accepted manifest identity and C05 execution receipt use separate filenames; no actual call is relabeled as a new run. The ordinary model-selected brief and four protected-binding checker result are unchanged.
