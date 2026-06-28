# OPERA export block

Use this block when a conversational check-in or check-out must be captured by Codex and transformed into a Markdown note.

```text
[OPERA_EXPORT_BEGIN]

ID: OPERA-YYYY-MM-DD-NNN
Date: YYYY-MM-DD
Type: check-out

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

Critical note:
- ...

[OPERA_EXPORT_END]
```

The block is designed as a bridge between natural conversation and structured research documentation. ChatGPT can generate it at the end of a conversation; Codex can extract it and write it into the OPERA capture layer.
