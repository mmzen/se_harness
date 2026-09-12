# Retained native path calibration output

`stdout.raw-bytes.json` is the authoritative lossless container for the original `stdout.txt` capture. Base64 decoding reproduces all original bytes, including the double-CR newline sequences. `stdout-byte-mapping.json` records the original filename, byte count and SHA-256, the container path, and the separate readable projection hash. Decoded bytes were compared with the current original file before replacement.

`stdout.txt` is now an explicitly labeled readable projection. Its whitespace/newline normalization must not be mistaken for the original output bytes. `actions.txt`, `observations.json` and `stderr.txt` remain unchanged source evidence. This formatting change introduces no new execution, test result, effect or lifecycle decision.
