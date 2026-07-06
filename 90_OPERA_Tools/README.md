# OPERA Toolchain

`90_OPERA_Tools/` contains the local OPERA toolchain: tools, configuration,
schemas, and operational documentation used to validate vault entries and export
datasets.

This folder is not the vault, is not the dataset, and does not contain canonical
entries. It is the toolkit that works on the vault.

## Purpose

The toolchain makes OPERA entries machine-readable, validates canonical Markdown
captures, and generates internal or research-facing datasets.

## Start here

Agents must read these files in this order:

1. `90_OPERA_Tools/AGENT_BOOTSTRAP.md`
2. `90_OPERA_Tools/README.md`
3. `90_OPERA_Tools/TOOLCHAIN.md`
4. `90_OPERA_Tools/opera_v2_draft/README_OPERA_v2_draft.md`

Do not infer toolchain behavior from old reports, CSV files, JSONL files, or
previous exports.

## Official parser

The official OPERA parser is:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

Use this parser. Do not create another one. Do not replace it. Do not rebuild it.

If `parser_v2.py` is not available:

1. stop;
2. do not invent a fallback parser;
3. ask for instructions.

## Main commands

Validate without writing exports:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault"
```

Generate internal export:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
```

Generate research export:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

## Documentation map

`AGENT_BOOTSTRAP.md` is the first operational file for agents.

`TOOLCHAIN.md` describes the extended technical architecture.

`MANIFEST.md` identifies the current toolchain state, canonical paths, export
profiles, and agent policy.

`opera_v2_draft/README_OPERA_v2_draft.md` documents the OPERA v2 draft parser
layer after the bootstrap file has been read.

## Hard rules for agents

Do not reconstruct `parser_v2.py`.

Do not create alternative parsers.

Do not generate CSV or JSONL manually.

Do not use generated datasets as the source of parser behavior.

Do not modify parser, schemas, entries, datasets, CSV, JSONL, or reports unless
explicitly instructed.
