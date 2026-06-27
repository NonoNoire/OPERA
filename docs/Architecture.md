# OPERA Architecture

This document will describe the structural organisation of OPERA as a Research Operating System.

## Purpose

To define how OPERA separates, connects, and preserves the different layers of artistic research documentation.

## Core Layers

### 1. Capture Layer

Daily notes, check-ins, check-outs, quick observations, fragments, and raw documentation enter OPERA through the Capture Layer.

In v0.3, the Capture Layer also includes conversational capture: a natural exchange with ChatGPT can be converted into a structured `OPERA_EXPORT` block and then written by Codex as a Markdown note.

### 2. Processing Layer

Review routines, classification, refinement, and transformation of raw material. The Processing Layer decides what remains a daily operational trace, what becomes a research object, and what needs further development.

### 3. Conceptual Layer

Research questions, hypotheses, concepts, theoretical references, and interdisciplinary links. This layer is where captured material becomes part of the knowledge graph.

### 4. Output Layer

Thesis writing, exhibitions, papers, presentations, and public documentation.

## Conversational Workflow

```text
ChatGPT
  -> conversational prompt
  -> OPERA_EXPORT block
  -> Codex extraction
  -> Markdown capture note
  -> GitHub versioning
  -> Obsidian vault
```

This workflow is documented in `docs/Conversational-Capture.md`.

## Design Requirements

- **Traceability**: each relevant checkpoint should have a stable identifier.
- **Modularity**: templates, scripts, examples, and private vault material must remain distinguishable.
- **Privacy**: not every personal Obsidian note belongs in the shareable repository.
- **Portability**: notes should remain readable Markdown files.
- **Versioning**: meaningful changes should be preserved through Git.
- **Calendar boundary**: Calendar stores dates and reminders, not research knowledge.

## Canonical Paths

- Obsidian vault: `MicioVault/`
- Capture notes: `MicioVault/00_OPERA_Capture/`
- Entry index: `20_OPERA_Dataset/opera_entries_index.csv` and `20_OPERA_Dataset/opera_entries.jsonl`
- Capture script: `scripts/opera_capture.py`
- Legacy folder (retained, not extended): `vault/OPERA-Capture/`

## Capture ID Convention

Capture identifiers use the date-based format: `OPERA-YYYY-MM-DD-NNN`.
The sequence number `NNN` is padded to three digits and scoped to the day.
The legacy format `R-000NNN` is no longer used for new entries.

## Open Questions

- Which OPERA materials should remain private and which can become part of a future public method?
- How much automation is desirable before the method becomes too opaque?
