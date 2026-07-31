# Codex implementation brief: OPERA Studio

Use this brief from the canonical local vault/repository:

```text
C:/Users/chris/Desktop/MicioVault
```

## Mission

Extend the official OPERA parser to support persistent artworks, bounded experiments, and asset manifests while preserving every existing Capture behaviour.

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

## Codex operating rules

Work locally in the repository opened from the folder above. Use the terminal available to Codex when needed.

- Inspect before editing.
- Keep the user informed of consequential findings.
- Do not stage, commit, push, merge, or alter unrelated files unless explicitly instructed.
- Stop before any destructive operation.
- Treat the local MicioVault as the private source of truth; do not copy private artwork records or asset paths into the public repository.

## Safety and baseline

1. Run `git status -sb` and report any unrelated or uncommitted changes.
2. Record current branch, current commit, parser SHA-256, capture count, v1/v2 count, warnings, errors, and hashes of current derived outputs.
3. Run the existing commands before editing:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault"
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

4. Preserve reports and output hashes as the Capture baseline.
5. Create or use branch `agent/opera-studio-records`.
6. Do not edit existing `00_OPERA_Capture/OPERA-*.md` files.
7. Do not regenerate datasets manually.

## Phase A: source paths and templates

Create these local source directories if absent:

```text
OPERA/O_Opere/Records/
OPERA/E_Esplorazioni/Records/
OPERA/A_Archivio/Asset_Manifests/
```

Copy or adapt the shareable templates into the local Obsidian template area only if this does not overwrite existing files:

```text
templates/studio-work.md
OPERA/_Templates/Template_studio_work.md

templates/studio-experiment.md
OPERA/_Templates/Template_studio_experiment.md

templates/studio-asset-manifest.md
OPERA/_Templates/Template_studio_asset_manifest.md
```

Compare and report conflicts rather than overwriting.

## Phase B: parser extension

Modify the official parser. Clearly bounded Studio helpers may be extracted into imported modules, but `parser_v2.py` must remain the sole CLI entrypoint.

### CLI compatibility

Add:

```text
--scope capture|studio|all
```

Rules:

- default is `capture`;
- commands without `--scope` retain current behaviour;
- `capture` produces current outputs and validation semantics;
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

Do not support lists of nested maps in Studio v1 records.

### Validation

Implement explicit validators for the three Studio entity types. JSON schemas are normative documentation; runtime validation may remain manual if adding `jsonschema` would create an unwanted dependency.

Validate:

- required metadata and Markdown sections;
- entity type and identifier pattern;
- allowed statuses and enums;
- duplicate IDs across Studio scope;
- work, experiment, entry, and asset references;
- self-reference in `derives_from`;
- missing asset paths when `verify_exists: true`;
- manifest kind/path-kind consistency;
- body-derived and identifiable-image privacy flags.

Broken references are errors for `all`. For `studio`, unresolved entry links may be warnings when Capture scope is not loaded.

### Asset indexing

For each asset manifest:

- resolve `root_path` according to storage tier;
- index a single file or the declared directory globs;
- derive relative path, extension, byte size, modified timestamp, and SHA-256;
- never modify source assets;
- do not perform image recognition or mesh interpretation;
- keep absolute paths internal only;
- use deterministic ordering.

### Relations

Derive normalized relations only from explicit identifiers:

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

## Phase C: derived outputs

Keep Capture filenames unchanged. Add Studio outputs under the selected profile:

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

Use Python standard-library `sqlite3`. Suggested tables:

```text
entries
works
experiments
assets
asset_files
relations
```

Use stable primary keys. Store rich metadata and sections as JSON text where further normalization is not useful. SQLite is derived and replaceable.

### Research profile

Research outputs must:

- remove absolute paths;
- exclude or manually review body-derived and identifiable-image records by default;
- preserve only safe descriptive metadata;
- add explicit export status and recommended action;
- never expose raw body scans or local file locations.

## Phase D: tests

Add tests using a temporary synthetic vault. Do not use private captures as fixtures.

Minimum tests:

1. existing Capture command works without `--scope`;
2. Capture output structure remains unchanged;
3. valid work record;
4. valid 3D scanning experiment;
5. valid batch asset manifest;
6. duplicate Studio ID;
7. missing work reference;
8. missing asset path with `verify_exists: true`;
9. asset derivation self-cycle;
10. body-derived asset excluded or flagged in research profile;
11. SQLite contains expected rows and relations;
12. deterministic rerun produces equivalent Studio datasets.

Prefer `unittest` unless the repository already standardizes another framework.

## Phase E: private pilot records

After parser tests pass, create only these two work seeds in the private local vault. Do not add them to the public repository.

### WORK-2026-0001

Working title: `Body-fitted jewellery from neck and shoulder scans`

Status: `exploration`

Core proposition: use scans of the researcher's neck and shoulders to generate jewellery that adheres closely to bodily topography. Treat the scan as both an instrumental fitting surface and a possible source of formal transformation.

Privacy defaults:

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

Preserve this distinction:

```text
technical event
-> observation
-> artistic selection
-> transformation
-> interpretation
```

Do not claim accidental artefacts were intentionally produced. Do not create an experiment or asset record without a specific dated session and file path.

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

- Capture counts and IDs are unchanged;
- default Capture behaviour is preserved;
- existing Capture output structure has not drifted;
- Studio validation is OK;
- both work IDs appear exactly once;
- no fabricated experiments or asset paths exist;
- internal SQLite opens and contains the two work rows;
- research outputs protect body-derived data;
- all tests pass.

## Final report

Return:

- branch and commit;
- parser SHA before and after;
- files created and modified;
- Capture baseline comparison;
- Studio counts by entity type;
- warnings and errors;
- tests run and results;
- SQLite tables and row counts;
- privacy/export status of both pilot works;
- any field or behaviour that remains provisional.

Do not merge automatically. Leave the work on the reviewable branch and stop for human review.
