# Claude Code implementation brief: OPERA Studio

Use this brief from the canonical local vault/repository:

```text
C:/Users/chris/Desktop/MicioVault
```

## Mission

Extend the official OPERA parser to support persistent artworks, bounded experiments, and asset manifests while preserving every existing capture behaviour.

The operational source of truth remains:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

Do not create a parallel parser and do not migrate existing artwork notes automatically.

## Required reading order

Before changing anything, read:

1. `90_OPERA_Tools/AGENT_BOOTSTRAP.md`
2. `90_OPERA_Tools/README.md`
3. `90_OPERA_Tools/TOOLCHAIN.md`
4. `90_OPERA_Tools/opera_v2_draft/README_OPERA_v2_draft.md`
5. `docs/opera-studio-architecture.md`
6. `docs/opera-studio-conversational-protocol.md`
7. `90_OPERA_Tools/opera_v2_draft/work.v1.schema.json`
8. `90_OPERA_Tools/opera_v2_draft/experiment.v1.schema.json`
9. `90_OPERA_Tools/opera_v2_draft/asset_manifest.v1.schema.json`

## Safety and baseline

1. Run `git status -sb` and do not stage unrelated changes.
2. Record the current branch, current commit, parser SHA-256, and the counts in the latest internal validation report.
3. Run the existing commands before editing:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault"
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

4. Preserve the reports and output hashes as the capture baseline.
5. Create or use branch `agent/opera-studio-records`.
6. Do not edit existing `00_OPERA_Capture/OPERA-*.md` files.
7. Do not regenerate datasets manually.

## Phase A: paths and source records

Create these local source directories if absent:

```text
OPERA/O_Opere/Records/
OPERA/E_Esplorazioni/Records/
OPERA/A_Archivio/Asset_Manifests/
```

Copy or adapt the repository templates into the local Obsidian template area only when doing so does not overwrite existing templates:

```text
templates/studio-work.md
OPERA/_Templates/Template_studio_work.md

templates/studio-experiment.md
OPERA/_Templates/Template_studio_experiment.md

templates/studio-asset-manifest.md
OPERA/_Templates/Template_studio_asset_manifest.md
```

If an existing local template has the target name, compare and report instead of overwriting.

## Phase B: parser extension

Modify the official parser, preferably by extracting clearly bounded Studio helpers into an imported module while keeping `parser_v2.py` as the sole CLI entrypoint.

### CLI compatibility

Add:

```text
--scope capture|studio|all
```

Rules:

- default is `capture`;
- commands without `--scope` retain current behaviour;
- `capture` produces the current outputs and validation semantics;
- `studio` handles work, experiment, and asset source records;
- `all` handles both and generates cross-entity relations.

### Source discovery

Use configurable relative paths with these defaults:

```text
works_dir = OPERA/O_Opere/Records
experiments_dir = OPERA/E_Esplorazioni/Records
assets_dir = OPERA/A_Archivio/Asset_Manifests
```

Do not scan arbitrary Markdown files outside these directories.

### Frontmatter support

The current YAML subset parser supports nested maps and simple scalar lists. Extend its recognized list fields for Studio schemas without adding a mandatory third-party dependency.

At minimum include:

```text
projects
practice_domains
medium
related_entries
related_experiments
related_assets
related_readings
work_ids
assets_used
assets_produced
experiment_ids
file_globs
derives_from
```

Do not support lists of nested maps in v1 Studio records.

### Validation

Implement explicit validators for the three Studio entity types. JSON schemas are normative documentation, but runtime validation may remain manual if introducing `jsonschema` would add an unwanted dependency.

Validate:

- required metadata;
- entity type;
- identifier pattern;
- allowed statuses and enums;
- required Markdown sections;
- duplicate IDs across the whole Studio scope;
- work, experiment, entry, and asset references;
- self-reference in `derives_from`;
- missing asset paths when `verify_exists: true`;
- manifest kind/path-kind consistency;
- body-derived and identifiable-image privacy flags.

Broken references should be errors for `all`. For `studio`, unresolved entry links may be warnings when capture scope was not loaded.

### Asset indexing

For each asset manifest:

- resolve `root_path` according to storage tier;
- for a file manifest, index the single file;
- for a directory manifest, apply the declared `file_globs` non-recursively in v1 unless explicitly documented otherwise;
- derive relative path, extension, byte size, modified timestamp, and SHA-256;
- never modify source assets;
- do not perform image recognition or mesh interpretation;
- keep absolute paths internal only.

Use deterministic ordering.

### Relations

Derive normalized relations from identifiers:

```text
entry mentions work
work developed_by experiment
work has_asset asset
work informed_by reading
experiment uses asset
experiment produces asset
asset derived_from asset
```

Do not infer relations from prose in the first implementation.

## Phase C: outputs

Keep capture filenames unchanged. Add Studio outputs under the selected profile:

```text
opera_works.<profile>.csv
opera_works.<profile>.jsonl
opera_experiments.<profile>.csv
opera_experiments.<profile>.jsonl
opera_assets.<profile>.csv
opera_assets.<profile>.jsonl
opera_relations.<profile>.csv
opera_relations.<profile>.jsonl
opera_studio_validation.<profile>.md
```

For `internal`, also generate atomically:

```text
20_OPERA_Dataset/internal/opera.sqlite
```

Use Python standard-library `sqlite3`.

Suggested tables:

```text
entries
works
experiments
assets
asset_files
relations
```

Use stable primary keys. Store rich metadata/sections as JSON text where normalization is not useful. The database is derived and replaceable.

### Research profile

Research outputs must:

- remove absolute paths;
- exclude asset file hashes when they could enable unintended identification unless explicitly justified;
- default body-derived and identifiable-image records to excluded or manual review;
- preserve only safe descriptive metadata;
- add explicit export status and recommended action;
- never expose raw body scans or local file locations.

## Phase D: tests

Add tests using a temporary synthetic vault. Do not use private captures as fixtures.

Minimum tests:

1. existing capture command works without `--scope`;
2. capture output structure remains unchanged;
3. valid work record;
4. valid 3D scanning experiment;
5. valid batch asset manifest;
6. duplicate Studio ID;
7. missing work reference;
8. missing asset path with `verify_exists: true`;
9. asset derivation self-cycle;
10. body-derived asset excluded or flagged in research profile;
11. SQLite contains expected rows and relations;
12. deterministic re-run produces equivalent Studio datasets.

Prefer `unittest` unless the repository already standardizes another framework.

## Phase E: local pilot records

After parser tests pass, create only these two work seeds in the private local vault. Do not add them to the public repository.

### WORK-2026-0001

Working title: `Body-fitted jewellery from neck and shoulder scans`

Status: `exploration`

Core proposition: use scans of the researcher’s neck and shoulders to generate jewellery that adheres closely to bodily topography. Treat the scan as both an instrumental fitting surface and a possible source of formal transformation.

Privacy:

```text
contains_personal_data: true
contains_identifiable_images: possible/true according to source
contains_body_derived_data: true
research_export_default: exclude
```

Do not create an experiment or asset record unless an actual dated session and real file path are available.

### WORK-2026-0002

Working title: `Expressive aberrant scanning`

Status: `exploration`

Core proposition: investigate 3D scanning as an inscription process in which tracking loss, fragmentation, false acquisition, duplicated surfaces, omissions, and reconstruction artefacts may be selected and transformed as aesthetic material rather than automatically corrected.

Key distinction to preserve:

```text
technical event
-> observation
-> artistic selection
-> transformation
-> interpretation
```

Do not claim that accidental artefacts were intentionally produced. Do not create an experiment or asset record without a specific dated session and file path.

## Phase F: verification

Run:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault" --scope capture
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault" --scope studio
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault" --scope all
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal --scope all
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research --scope all
```

Confirm:

- capture counts and IDs are unchanged;
- capture default behaviour is preserved;
- existing capture output structure has not drifted;
- Studio validation is OK;
- both work IDs appear exactly once;
- no fabricated experiments or asset paths exist;
- internal SQLite opens successfully and contains the two work rows;
- research outputs protect body-derived data;
- all tests pass.

## Final report

Return:

- branch and commit;
- parser SHA before and after;
- files created and modified;
- capture baseline comparison;
- Studio counts by entity type;
- warnings and errors;
- tests run and results;
- SQLite tables and row counts;
- privacy/export status of both pilot works;
- any field or behaviour that remains provisional.

Do not merge automatically. Leave the work in a reviewable branch or draft pull request.
