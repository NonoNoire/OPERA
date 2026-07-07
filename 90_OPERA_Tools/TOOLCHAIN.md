# OPERA Toolchain Architecture

This document describes the technical architecture of the OPERA local toolchain.
It is documentation only. It does not define parser behavior.

The operational source of truth is:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

## Status

Toolchain status: v2 draft / stabilization.

Official parser: `90_OPERA_Tools/opera_v2_draft/parser_v2.py`.

Supported entry schemas: v1 tolerated, v2 supported.

Export profiles: internal, research.

Canonical vault root: `C:/Users/chris/Desktop/MicioVault`.

Current goal: documentation hardening and agent discoverability.

Non-goal: parser rewrite.

## Vault structure

The vault is the local Obsidian workspace:

```text
C:/Users/chris/Desktop/MicioVault
```

Relevant OPERA areas:

```text
00_OPERA_Capture/     Canonical OPERA Markdown entries.
20_OPERA_Dataset/     Generated datasets, reports, and audits.
90_OPERA_Tools/       Parser, schema, examples, configuration, documentation.
```

The canonical source entries live in `00_OPERA_Capture/`. Dataset files are
generated artifacts and must not be treated as the source of parser behavior.

## Toolkit structure

Current toolkit structure:

```text
90_OPERA_Tools/
|-- README.md
|-- TOOLCHAIN.md
|-- AGENT_BOOTSTRAP.md
|-- MANIFEST.md
|-- opera_parse_entries.py
`-- opera_v2_draft/
    |-- README_OPERA_v2_draft.md
    |-- parser_v2.py
    |-- opera.example.toml
    |-- privacy_rules.example.json
    |-- entry_v2.md
    |-- entry.v2.schema.json
    |-- internal_export.schema.json
    `-- research_export.schema.json
```

`opera_parse_entries.py` is present in the toolkit root. The official OPERA v2
parser is `opera_v2_draft/parser_v2.py`.

## Parser

The official parser is:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

It reads canonical Markdown entries from the vault, validates required metadata
and sections, and exports datasets for the selected profile.

Supported commands:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault"
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

Do not reconstruct this parser. Do not replace it. If it is missing, stop.

## Dataset

Datasets are generated under `20_OPERA_Dataset/`.

The internal profile is a complete local export for private analysis. It can
include full metadata, sections, operational context, waiting items, calendar
actions, personal/contextual logistics, and local paths.

The research profile is conservative and filtered. It is meant as a
research-facing draft dataset, not as a publication-ready anonymized corpus.
It adds privacy audit fields and can mark entries as `safe`, `needs_review`,
`anonymize_before_use`, or `internal_only`.

## Validation

Validation checks canonical entries without manually editing them.

The validator checks common metadata and required sections for supported schema
versions. Validation warnings and errors should be handled by reviewing source
entries and parser output, not by modifying generated dataset files.

## Export

Export is performed by `parser_v2.py parse`.

Internal export writes internal JSONL/CSV records.

Research export writes research JSONL/CSV records and a privacy audit report.
Research output is filtered according to section mapping, metadata, privacy
rules, and audit logic inside the official parser.

## Internal vs research export

Internal export:

```text
Complete private working export.
Preserves operational and contextual material.
Intended for local analysis inside the vault.
```

Research export:

```text
Filtered conservative export.
Excludes operational, waiting, calendar, and personal/contextual sections by default.
Includes privacy flags, context markers, audit notes, and recommended actions.
Requires review before public or external use.
```

## Role of TOML files

`opera.example.toml` documents the expected local configuration shape:

```text
[vault]             vault, capture, and dataset locations
[parser]            parser-level defaults
[exports.internal]  internal export paths and filenames
[exports.research]  research export paths, filenames, and excluded sections
```

It is an example configuration file. Do not change it during documentation-only
maintenance unless the task explicitly concerns configuration documentation.

## Role of JSON schema files

The schema files document expected object shapes:

```text
entry.v2.schema.json          OPERA Entry v2 structure.
internal_export.schema.json   Internal export record structure.
research_export.schema.json   Research export record structure.
```

They support validation and discoverability. Do not edit schemas unless the task
explicitly authorizes a schema change.

## Full workflow

```text
Utente
->
ChatGPT
->
Codex
->
00_OPERA_Capture
->
90_OPERA_Tools/opera_v2_draft/parser_v2.py
->
20_OPERA_Dataset/internal or 20_OPERA_Dataset/research
->
Validation reports, privacy audits, and research workflows
```

The correct order is:

1. Read `AGENT_BOOTSTRAP.md`.
2. Locate `parser_v2.py`.
3. Inspect existing documentation and schema.
4. Run validation if needed.
5. Run the official parser for exports if needed.
6. Review generated reports and audits.
7. Change only the files explicitly in scope.

## Future extension points

Possible future extension points:

```text
Packaged CLI command, for example `opera validate` and `opera parse`.
Local privacy rule overrides in `privacy_rules.local.json`.
Additional export profiles, if explicitly designed and documented.
Additional schema versions, if migration rules are explicit.
Additional audit reports, if generated by the official parser.
```

Any extension must preserve existing parser behavior unless a change is explicitly
requested and reviewed.

## Architectural principles

The vault is the source of entries.

The parser is the source of operational behavior.

Datasets are generated artifacts.

Documentation improves discoverability but does not redefine behavior.

Validation must be non-destructive.

Research export must be conservative.

Privacy rules must be explicit.

Agent assumptions must be checked against the current toolkit, not inferred from
old reports.

## Errori da NON commettere

NO: Ricostruire `parser_v2.py`.

NO: Generare dataset manualmente.

NO: Cercare il parser solo nella root del vault.

NO: Modificare le entry direttamente durante la validazione.

NO: Usare report precedenti per dedurre il comportamento del parser.

NO: Trattare CSV o JSONL generati come fonte primaria.

NO: Modificare schema JSON per far passare un export.

NO: Creare un parser alternativo perche' uno script precedente sembra simile.

NO: Saltare `privacy_rules.example.json` quando si interpreta il profilo research.
