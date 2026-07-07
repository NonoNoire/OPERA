# OPERA Agent Bootstrap

Read this first.

## Read order

Read this file before inspecting the rest of the repository.

Do not inspect previous datasets to infer parser behavior.

Do not search randomly before checking the documented parser path.

Do not create fallback parsers.

If the official parser is missing, stop.

## 1. Parser location

The official OPERA parser is:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

Use this parser. Do not create another one.

## 2. How to run it

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

## 3. What NOT to do

Do not rebuild `parser_v2.py`.

Do not create alternative parsers.

Do not generate CSV or JSONL manually.

Do not infer parser behavior from old reports or existing datasets.

Do not edit JSON schemas, entry Markdown, dataset files, CSV, JSONL, or reports
unless explicitly instructed.

## 4. When to stop

Stop and ask for instructions if:

```text
parser_v2.py is genuinely missing.
The requested task requires changing parser behavior.
The requested task requires changing JSON schemas or entry format.
The requested task requires manual dataset generation.
```

## 5. Correct order

1. Locate `90_OPERA_Tools/opera_v2_draft/parser_v2.py`.
2. Read `90_OPERA_Tools/README.md`.
3. Read `90_OPERA_Tools/TOOLCHAIN.md`.
4. Read `90_OPERA_Tools/opera_v2_draft/README_OPERA_v2_draft.md`.
5. Use the official parser for validation or export.
6. Modify only files that are explicitly in scope.
