# OPERA Architecture

This document defines the current canonical structure of OPERA as a portable Obsidian/GitHub research system.

OPERA is a methodological and computational framework for documenting, structuring, versioning, and analysing artistic and doctoral research processes. "Research Operating System" is used methodologically: OPERA is not a literal operating system, but a set of file conventions, workflows, schemas, and review practices.

## Canonical Decision

- `MicioVault/` is the canonical Obsidian vault inside this repository.
- `MicioVault/00_OPERA_Capture/` is the canonical OPERA capture archive.
- `vault/OPERA-Capture/` is legacy only.
- Legacy files are retained for migration and audit unless they are clearly safe to remove.
- The full real `MicioVault` may still live on the primary computer and can be imported later.

## Core Layers

### 1. Capture Layer

Daily notes, check-ins, check-outs, quick observations, fragments, and raw documentation enter OPERA through the Capture Layer.

In v0.3, the Capture Layer includes conversational capture: a natural exchange with ChatGPT can be converted into a structured `OPERA_EXPORT` block and then written by Codex as a Markdown note.

Canonical capture notes are stored flat in:

```text
MicioVault/00_OPERA_Capture/
```

New capture notes should use the identifier format:

```text
OPERA-YYYY-MM-DD-NNN
```

### 2. Parser and Dataset Layer

The parser layer turns structured capture material into stable Markdown. Derived indexes live in:

```text
20_OPERA_Dataset/opera_entries_index.csv
20_OPERA_Dataset/opera_entries.jsonl
```

The dataset files are indexes and analysis surfaces. They should describe canonical capture entries, not replace the Markdown archive.

### 3. Processing Layer

Review routines, classification, refinement, and transformation of raw material decide what remains a daily operational trace, what becomes a research object, and what needs further development.

### 4. Conceptual Layer

Research questions, hypotheses, concepts, theoretical references, and interdisciplinary links are developed in the Obsidian vault. This layer is where captured material becomes part of the knowledge graph.

### 5. Output Layer

Thesis writing, exhibitions, papers, presentations, and public documentation are outputs of the system. They may draw from OPERA, but they are not the same as the capture archive.

## Conversational Workflow

```text
ChatGPT
  -> conversational prompt
  -> OPERA_EXPORT block
  -> Codex extraction
  -> Markdown capture note
  -> MicioVault/00_OPERA_Capture/
  -> GitHub versioning
  -> Obsidian reading and linking
  -> dataset index refresh when appropriate
```

This workflow is documented in `docs/Conversational-Capture.md`.

## Repository Structure

```text
OPERA/
  MicioVault/
    00_OPERA_Capture/
      OPERA-2026-06-19-001.md
      OPERA-2026-06-27-001.md
  20_OPERA_Dataset/
    opera_entries_index.csv
    opera_entries.jsonl
  docs/
  scripts/
  templates/
  examples/
  assets/
  vault/
    OPERA-Capture/        # legacy only
```

## Design Requirements

- **Traceability**: each relevant checkpoint has a stable identifier.
- **Modularity**: templates, scripts, examples, canonical vault files, and legacy material remain distinguishable.
- **Privacy**: the repository must not imply that all personal Obsidian notes belong in GitHub.
- **Portability**: notes remain readable Markdown files.
- **Versioning**: meaningful changes are preserved through Git.
- **Calendar boundary**: Calendar stores dates and reminders, not research knowledge.
- **Migration safety**: legacy files are marked and redirected before any deletion is considered.

## Legacy Boundary

`vault/OPERA-Capture/` contains earlier capture material and path conventions. It should be treated as historical input for migration, not as the active archive.

Future captures should go to `MicioVault/00_OPERA_Capture/`. If a legacy item is migrated, the new canonical entry should preserve useful provenance such as `legacy_id` and `legacy_path` in front matter.

## See Also

- `docs/OPERA-v1-architecture.md` for the broader v1 draft.
- `docs/Conversational-Capture.md` for the v0.3 capture workflow.
- `docs/portable-vault-setup.md` for the portable vault setup notes.
