# Claude instruction demonstration — 2026-09-27

Session: `5623d905-2596-437c-bef3-6407a4434707`  
Surface: Claude Code CLI on Windows.

| Check | Native evidence |
| --- | --- |
| Startup | Debug log line 130 records successful `SessionStart:startup`; line 131 accepts 8,927 context characters. |
| Progressive discovery | Transcript lines 44 and 48 record reads of `COMMUNICATION.md` and `DEFINE_CHANGE.md`. |
| Manual compaction | Transcript line 73 records the manual compaction boundary. |
| Compaction hook | Debug log line 454 records successful `SessionStart:compact`; line 455 accepts 8,927 context characters. |
| Complete instruction file | Both hook payloads contain the complete file and match its selected SHA-256. |
| Agent response | Corrected probes at transcript lines 38 and 102 return the expected metadata. |

Instruction-file SHA-256:
`be7c525c4cc2e4ec91186453353d3c2889c25e1cfa5f47ab52902acce57c6fae`.

The compaction callback succeeds at `2026-09-27T15:49:47.255Z`, before the
post-compaction probe response at `2026-09-27T15:50:21.956Z`. The full file
comparison and native callback record support reinjection after compaction.

The original probe's `root_path` and `root_sha256` labels were ambiguous.
The corrected probe uses `instruction_file_path` and `entry_sha256`, mapped
to the delivery metadata. No product change was needed for that correction.
The earlier [startup-only observation](observation.json) is retained as recorded.

This demonstration covers one Windows Claude Code CLI session and manual
compaction. Missing or altered files and repository switching remain separate
checks. This report changes no formal artifact, acceptance or lifecycle state.

Evidence:

- [Structured observations](native-demonstration-observation.json)
- [Native hook output](native-demonstration-hook-extract.log)
- [Selected transcript records](native-demonstration-transcript-extract.json)
