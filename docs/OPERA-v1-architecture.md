# OPERA v1 Architecture Draft

## Executive Summary

OPERA is a methodological and computational framework for documenting, structuring, versioning, and analysing artistic and doctoral research processes.

Its practical form is deliberately modest: Markdown files, an Obsidian vault, explicit capture schemas, lightweight parsing scripts, derived dataset indexes, and GitHub versioning. Its methodological ambition is larger: to preserve the genealogy of research decisions, uncertainties, observations, revisions, and outputs so that artistic research can be reconstructed as a process rather than only presented as a finished result.

The canonical repository-backed vault is `MicioVault/`. The canonical OPERA capture archive is `MicioVault/00_OPERA_Capture/`. The older `vault/OPERA-Capture/` path is legacy only.

## Problem Definition

Doctoral and artistic research often produces knowledge through scattered fragments: studio notes, readings, interviews, failed attempts, administrative milestones, conceptual revisions, and informal conversations. These traces are easy to lose because they sit across notebooks, calendars, chat systems, drafts, folders, and memory.

OPERA addresses this by defining a portable capture and versioning method. It does not claim to solve the intellectual work of research. Instead, it makes the research process easier to document, inspect, cite internally, and analyse over time.

The core problem is therefore not "where should notes be stored?" but "how can a research process remain traceable without becoming bureaucratic?"

## What OPERA Is Not

OPERA overlaps with existing tools, but it is not equivalent to them.

### OPERA and Obsidian

Obsidian is the primary knowledge environment for reading, linking, and developing notes. OPERA defines the methodological structure around what enters the vault, how capture entries are identified, how they are versioned, and how selected material becomes dataset-ready.

Obsidian is the interface. OPERA is the method, schema, and repository workflow.

### OPERA and Notion

Notion is a flexible workspace and database tool. OPERA avoids dependence on a proprietary workspace model by using local Markdown, Git, and explicit schemas. The priority is long-term portability rather than all-in-one interface convenience.

### OPERA and Logseq

Logseq is an outliner and knowledge graph environment. OPERA can learn from graph-based workflows, but it is not primarily an outliner. Its center is the research capture entry as a versioned methodological unit.

### OPERA and Zotero

Zotero manages bibliographic sources. OPERA may refer to Zotero records, citations, and reading notes, but it does not replace reference management. Bibliographic authority should remain in a dedicated tool.

### OPERA and ELN/LIMS Systems

Electronic Lab Notebooks and Laboratory Information Management Systems are designed for laboratory protocols, samples, instruments, and regulated scientific workflows. OPERA borrows the seriousness of traceability, but its domain is artistic and doctoral research, where ambiguity, reflection, interpretation, and evolving methods are central.

### OPERA and Jupyter

Jupyter notebooks combine code, computation, and explanation. OPERA may produce datasets that can later be analysed in Python or notebooks, but OPERA entries are not computational notebooks. The canonical record remains Markdown capture plus derived indexes.

### OPERA and CAQDAS Tools

CAQDAS tools support qualitative data coding and analysis. OPERA can prepare material for qualitative analysis and preserve methodological context, but it does not replace specialist coding environments. If interview coding becomes central, OPERA should interoperate with CAQDAS workflows rather than pretend to be one.

## Naming Ambiguity

"OPERA" may be confused with the Opera web browser. In this repository, OPERA names the research framework only. When writing public-facing material, use phrasing such as "the OPERA research framework" or "OPERA Research Operating System" where needed to avoid ambiguity.

## Research Operating System

"Research Operating System" is a methodological phrase, not a claim that OPERA is a literal operating system. OPERA does not manage hardware, applications, permissions, or runtime processes.

The phrase means that OPERA coordinates research inputs, workflows, identifiers, storage conventions, review cycles, and version history. It is a system for operating a research process.

## Canonical Repository Structure

```text
OPERA/
  README.md
  docs/
    Architecture.md
    Conversational-Capture.md
    OPERA-v1-architecture.md
    portable-vault-setup.md
  MicioVault/
    00_OPERA_Capture/
      OPERA-2026-06-19-001.md
      OPERA-2026-06-27-001.md
  20_OPERA_Dataset/
    opera_entries_index.csv
    opera_entries.jsonl
  scripts/
    opera_capture.py
  templates/
  examples/
  assets/
  vault/
    OPERA-Capture/        # legacy only
```

The repository should not imply that the complete private research vault is already present. The current `MicioVault/` tree is the canonical repository-backed location, but the full working vault may be imported later from the primary computer.

## Canonical Entry Schema

Each canonical capture entry is a Markdown file with YAML front matter and structured sections.

Required front matter:

```yaml
---
id: OPERA-YYYY-MM-DD-NNN
date: YYYY-MM-DD
type: check-in | check-out | weekly-review | monthly-review | note | migration
status: captured | migrated | reviewed | superseded
archive_path: MicioVault/00_OPERA_Capture
---
```

Optional front matter:

```yaml
source: ChatGPT conversational checkout
legacy_id: R-000001
legacy_path: vault/OPERA-Capture/2026/06/2026-06-19-r-000001.md
opera_version: v0.3
privacy: private | shareable | anonymised
```

Recommended sections:

```text
# OPERA-YYYY-MM-DD-NNN - Title

## Done
## Next
## Waiting
## Calendar
## Research state
## Critical note
```

The schema should remain simple until repeated use proves that additional fields are necessary.

## Identifier Policy

Canonical entries use:

```text
OPERA-YYYY-MM-DD-NNN
```

Where:

- `OPERA` identifies the framework.
- `YYYY-MM-DD` records the entry date.
- `NNN` is a three-digit sequence for multiple entries on the same date.

Examples:

```text
OPERA-2026-06-19-001
OPERA-2026-06-27-001
OPERA-2026-06-27-002
```

Legacy identifiers such as `R-000001` should not be reused for new entries. When legacy material is migrated, preserve the old identifier in `legacy_id` and, when useful, preserve the old path in `legacy_path`.

## Parser and Dataset Layer

The parser layer converts structured conversational exports into Markdown capture notes. The default target is:

```text
MicioVault/00_OPERA_Capture/
```

The dataset layer provides machine-readable views of the canonical archive:

```text
20_OPERA_Dataset/opera_entries_index.csv
20_OPERA_Dataset/opera_entries.jsonl
```

The CSV supports quick inspection, sorting, and spreadsheet workflows. The JSONL supports programmatic analysis, search, and future dashboard experiments.

The dataset layer must remain derived from the canonical Markdown entries. If inconsistencies appear, the Markdown archive is the source of truth unless a migration note explicitly says otherwise.

## GitHub Portability Workflow

The portable workflow is:

```text
Primary computer or secondary computer
  -> open the OPERA repository
  -> work inside MicioVault/
  -> create or update captures in MicioVault/00_OPERA_Capture/
  -> refresh dataset indexes when appropriate
  -> commit changes with Git
  -> push to GitHub
  -> pull on the other computer
  -> open MicioVault/ in Obsidian
```

GitHub is the versioned transport and audit trail. Obsidian remains the reading, linking, and writing environment. The repository must stay portable enough that a second computer can clone it, open `MicioVault/`, and continue the workflow.

## Threshold for a Future App or Dashboard

OPERA should not become an app prematurely. A dashboard becomes justified only when repeated use demonstrates needs that Markdown, Obsidian search, Git history, CSV, and JSONL cannot handle comfortably.

Possible thresholds:

- more than 100 canonical capture entries;
- repeated need to filter by type, status, project, or research phase;
- repeated need for timeline or graph visualisation;
- repeated manual dataset refresh work;
- clear separation between private data and shareable method.

Until then, the priority is stability of the method, not interface expansion.

## Risks

### Over-Engineering

Too much structure can make daily capture feel like administrative work. New fields, scripts, and dashboards should be added only when they reduce actual friction.

### Premature App Design

An app could freeze the method before the doctoral workflow is mature. OPERA should continue as Markdown-first until real usage patterns justify a dedicated interface.

### False Precision

Schemas can create the illusion that research states are more stable or measurable than they are. OPERA should preserve ambiguity where ambiguity is methodologically honest.

### Privacy Leakage

The repository may contain method, templates, selected captures, and derived indexes. It should not automatically contain sensitive personal notes, unpublished research material, private reflections, or confidential interview data.

### Duplicated Vaults

The old `vault/` directory and the canonical `MicioVault/` directory can create confusion. Future captures must go to `MicioVault/00_OPERA_Capture/`. Legacy paths should be marked, migrated, or left as historical records.

## Roadmap

### v0.4 Knowledge Graph

- Define stable relations between captures, research questions, concepts, sources, projects, and outputs.
- Keep graph conventions readable in plain Markdown.
- Avoid ontology work that does not improve research practice.

### v0.5 Automation

- Automate only repeated, low-risk operations.
- Candidate automations: capture creation, dataset refresh, consistency checks, and periodic review prompts.
- Preserve manual review before public sharing or deletion.

### v0.6 Stable Beta

- Test OPERA across sustained doctoral work.
- Validate the canonical vault structure across at least two computers.
- Confirm the migration boundary between `vault/OPERA-Capture/` and `MicioVault/00_OPERA_Capture/`.
- Document privacy and publication rules.

### v1.0 Public Release

- Publish a stable architecture and workflow guide.
- Provide templates, example entries, and scripts that do not expose private research content.
- Decide licensing for code, documentation, and examples.
- Clarify the distinction between OPERA as method and any future software component.

## Current v1 Principle

The durable unit of OPERA is not an app screen, a database row, or a dashboard card. It is a traceable research entry that remains readable, versionable, portable, and methodologically meaningful.
