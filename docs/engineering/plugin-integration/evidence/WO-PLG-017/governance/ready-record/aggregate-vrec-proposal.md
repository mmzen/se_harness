# Proposed aggregate verification preparation

Prepare **VREC-PLG-010** in the ready state for **WO-PLG-011 + WO-PLG-017**, using
approved **VER-PLG-011** and clean candidate `47f7b842d395764583adbe834c39aecdc0afd521`.

The named preparation actor is `codex-preparation-actor`. Preparation records the
candidate and evidence; the assurance owner makes the later verification decision.

The [exact input manifest](aggregate-vrec-proposal.json) contains 182 explicitly
selected files, each with its size and SHA-256. Its SHA-256 is `0a8e05dbfadab5c6fa5cdc86de5b631205ea479e8d1baf96b0e16ca6d8c89f8c`.
It includes the original 95 selected WO011 paths, all 56 relocated payloads,
the two relocation maps, independent retention results, full successful repair CI
observations, and the actual delegated completion. Every selected byte matches Git.
All checks must also pass at the proposed candidate before capture.

VREC-PLG-008 and its historical candidate remain unchanged. A new ready record does
not verify or supersede that record, approve merge, or release anything. Raw linked
files remain committed; index links are not automatically added to the selection.
The two explicitly omitted whole-repository archive streams have retained hashes
and immutable-commit reproduction commands.
