+++
id = "CAP-RSK-010"
type = "capability"
title = "Record a threat, size it, and answer it before the stage moves"
status = "approved"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
ability = "Anyone can record a measured threat against governed work under any stage, and have the accountable owner answer it before that stage moves."

[relations]
derives_from = ["INT-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "product-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. Anyone working may record a measured threat, and the accountable owner answers it before the stage moves."
+++

# Capability: Record a threat, size it, and answer it before the stage moves

## In plain words

Anyone may write a threat down at any moment. The note carries how likely and
how damaging it is, and the accountable owner answers it.

## Actor and need

The actor is whoever is working: a reviewer, an implementer, or an agent
mid-execution. They need somewhere to put a threat that will not be lost. The
owner needs it in front of them, sized, when the stage asks to move.

## Not decided here

- The shape of the file and the arithmetic of the size.
- Which mechanism stops the stage.
- What closing a threat requires as proof.
- Whether a small threat may stop nothing.
