# OPERA export block

Use this block when a conversational check-in or check-out must be captured by Codex and transformed into a Markdown note.

```text
[OPERA_EXPORT_BEGIN]

ID: R-000001
Date: 2026-06-19
Type: Daily Check-out

Done:
- ...

Next:
- ...

Waiting:
- ...

Calendar:
- none

Research state:
- ...

[OPERA_EXPORT_END]
```

The block is designed as a bridge between natural conversation and structured research documentation. ChatGPT can generate it at the end of a conversation; Codex can extract it and write it into the OPERA capture layer.
