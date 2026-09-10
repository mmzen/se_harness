+++
id = "DEC-PKG-001"
type = "decision"
title = "Message punctuation"
status = "open"
owners = ["engineering-owner"]
created = "2026-09-10"
updated = "2026-09-10"
kind = "question"
question = "Should the message end with a period?"
raised_by = "fixture-author"
recommendation = "period"

[[options]]
id = "period"
label = "Use a period"

[[options]]
id = "plain"
label = "Use no punctuation"

[relations]
concerns = ["WO-PKG-001"]
blocks = ["WO-PKG-001"]
+++

# Decision: Message punctuation

The engineering owner selects the punctuation before approving the work order.
