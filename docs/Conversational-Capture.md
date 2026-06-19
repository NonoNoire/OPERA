# Conversational Capture

Conversational Capture is the OPERA v0.3 workflow that turns a natural exchange with ChatGPT into a structured research note.

## Purpose

The goal is to avoid double entry. The researcher answers conversational prompts once; OPERA then transforms those answers into a stable Markdown record.

This workflow keeps the distinction between three roles:

- **ChatGPT** acts as the conversational interface.
- **Codex** acts as the operational engine that extracts, writes, commits, and synchronises files.
- **Obsidian** remains the primary knowledge environment where the research archive is read, connected, and developed.

GitHub functions as a versioned bridge between Codex and the Obsidian vault.

## Standard flow

1. ChatGPT asks a check-in, check-out, weekly review, or monthly review.
2. The researcher answers in ordinary language.
3. ChatGPT converts the answer into an `OPERA_EXPORT` block.
4. Codex extracts the block and generates a Markdown note.
5. The note is stored in the OPERA capture layer.
6. Git commits preserve the historical sequence of the research process.
7. Obsidian reads the updated files through Git or another synchronisation mechanism.

## Export markers

Structured exports are delimited by these markers:

```text
[OPERA_EXPORT_BEGIN]
...
[OPERA_EXPORT_END]
```

Anything outside the markers is treated as conversational context. Anything inside the markers is treated as source material for a research note.

## Daily check-out

The daily check-out is intentionally short. It is not a diary and should normally take less than five minutes.

The five questions are:

1. What did I do?
2. What remains?
3. Is anything pending?
4. Should anything go to Calendar?
5. What is the current state of the research?

The fifth question is a methodological addition. It works as a **checkpoint epistemologico**: a one-sentence record of the research phase represented by the day.

This matters because OPERA is not only a productivity system. It is a way of documenting the genealogy of a research process. The fifth field helps reconstruct, after months or years, how the project moved from theoretical framing to empirical design, fieldwork, analysis, writing, dissemination, and revision.

## Calendar boundary

Calendar should contain only dated events, deadlines, meetings, reminders, and time-specific actions. It should not become a knowledge archive. Research meaning belongs in OPERA and Obsidian.

## Obsidian boundary

Obsidian remains the primary environment for reading, linking, and developing the research archive. The GitHub repository can mirror or stage selected OPERA notes, but not every private note must become part of the shareable repository.

This distinction protects the researcher's private material while keeping the OPERA method versionable and auditable.
