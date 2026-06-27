# OPERA

> **Early Research Prototype**
>
> OPERA is an evolving research prototype. Its structure, vocabulary, and workflows are expected to change as the doctoral research process develops.

OPERA is a provisional Research Operating System designed to support the daily documentation of artistic research, thesis development, and methodological reflection.

The project originates within a doctoral research context in artistic research. It is not conceived as a finished note-taking template, but as an experimental infrastructure for tracing how research knowledge is observed, formulated, tested, revised, and connected over time.

## Philosophy

OPERA is based on the assumption that research is not produced only through final outputs. It also emerges through hesitation, partial observations, failed attempts, conceptual shifts, annotations, and the gradual reorganisation of experience.

For this reason, OPERA treats documentation as a methodological act. The system aims to preserve the genealogy of ideas rather than only their polished formulation.

## Objectives

The initial objectives of OPERA are:

- to document artistic research as an ongoing process;
- to distinguish observations, questions, hypotheses, experiments, reflections, and references;
- to support the reconstruction of conceptual development over time;
- to make interdisciplinary connections explicit and traceable;
- to provide a rigorous structure for reflective research diaries;
- to prepare selected research materials for possible future sharing without exposing the private research vault.

## Project Status

OPERA is currently in its earliest phase of development. The present repository represents a Genesis Snapshot: a first methodological scaffold intended to document the development of the system itself.

The repository is private at this stage because the method is still experimental, incomplete, and connected to an ongoing doctoral project. A future open-source or open-research release may be considered once the system reaches a stable form and the boundaries between personal research material and shareable methodology are clearly defined.

### Checkpoint — 18 giugno 2026

The first operational checkpoint records the completion and official submission of the doctoral semester review, confirmed by prof.ssa Buffardi and prof. Cassani; the creation of the OPERA GitHub repository; and the reorganisation of the Obsidian vault.

This marks the transition from administrative consolidation to active dissertation work, with three immediate priorities: GRADED, interview traces, and the transformation of an existing 30–40 page document into the seed of the dissertation.

See: `docs/2026-06-18-genesis-checkpoint.md` and `docs/next-actions-graded-interviews-dissertation.md`.

### Checkpoint — 19 giugno 2026

OPERA v0.3 introduces Conversational Capture: a workflow where a natural ChatGPT exchange can be converted into a structured `OPERA_EXPORT` block, processed by Codex, versioned on GitHub, and synchronised with Obsidian.

The first daily check-out capture was stored as `vault/OPERA-Capture/2026/06/2026-06-19-r-000001.md` and has since been migrated to the canonical location: `MicioVault/00_OPERA_Capture/OPERA-2026-06-19-001.md`.

## Synthetic Roadmap

- **v0.1 Genesis**: initial repository, conceptual scaffold, and documentation structure.
- **v0.2 Daily Workflow**: definition of daily note routines, recurring prompts, and review procedures.
- **v0.3 Conversational Capture**: conversion of check-ins/check-outs from natural conversation into structured Markdown records.
- **v0.4 Knowledge Graph**: development of ontological relations and graph-based research navigation.
- **v0.5 Automation**: integration of selected automations for reminders, reviews, and archival routines.
- **v0.6 Stable Beta**: testing of the system across sustained research activity.
- **v1.0 Public Release**: possible release of a stable, documented, shareable version.

## Repository Structure

- `MicioVault/`: the canonical Obsidian vault. Open this folder in Obsidian on any computer after cloning.
  - `00_OPERA_Capture/`: canonical location for all new OPERA capture notes.
- `20_OPERA_Dataset/`: structured index of all capture entries as CSV and JSONL.
- `docs/`: methodological and architectural documentation.
- `templates/`: OPERA templates, separated from any personal vault.
- `examples/`: future anonymised examples of use.
- `assets/`: shareable diagrams, images, and visual documentation.
- `scripts/`: lightweight utilities for capture, export, and maintenance.
- `vault/`: legacy folder retained for historical continuity. New captures do not go here.
- `.github/`: future repository governance and workflow files.

## Licensing Note

This repository currently uses an **All Rights Reserved** notice as a temporary protective measure. This does not exclude a future open-source or open-research license. Rather, it acknowledges that OPERA is still a research prototype and that its methodological, academic, and personal boundaries require further definition before public release.

Possible future options include:

- an open-source license such as MIT or Apache 2.0 for software components;
- a Creative Commons license for documentation and methodological materials;
- a dual-license model separating code, documentation, and research examples.

The licensing model should be revisited before any public release.
