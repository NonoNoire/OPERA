# OPERA Studio architecture

Status: design baseline for implementation and local pilot testing.

## 1. Purpose

OPERA remains one system with two capture rhythms:

- **OPERA Capture** records the longitudinal daily research process in canonical `OPERA-*.md` entries.
- **OPERA Studio** records persistent artworks, bounded experiments, and digital or physical assets only when relevant activity occurs.

The Studio layer does not replace, duplicate, or weaken the daily checkout. It adds persistent entities that can be referenced by daily entries and queried as a relational dataset.

## 2. Canonical entity model

OPERA uses four source entity classes:

1. `entry`: chronological capture of a day, session, memo, review, observation, or event.
2. `work`: persistent artwork, series, installation, sculptural proposition, design investigation, or early work seed.
3. `experiment`: bounded practical session, test, iteration, scan, fabrication attempt, material study, or installation trial.
4. `asset`: an individual file or a batch manifest for photographs, drawings, scans, meshes, textures, video, CAD, print files, or documentation.

Relations are derived from explicit identifiers in source records. They are not a fifth source entity in the first implementation.

```text
entry -> mentions -> work
work -> developed_by -> experiment
experiment -> uses/produces -> asset
asset -> derived_from -> asset
work -> informed_by -> reading/reference
```

## 3. Source-of-truth principle

Human-readable Markdown remains the canonical source. CSV, JSONL, and SQLite are derived outputs and must be reproducible from the source records.

The official parser remains:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

Do not create a parallel parser. Studio support must be implemented as an extension of the official parser, optionally using imported helper modules.

## 4. Proposed local paths

Paths are configurable, but the initial local convention is:

```text
00_OPERA_Capture/                         canonical daily entries
OPERA/O_Opere/Records/                   work records
OPERA/E_Esplorazioni/Records/            experiment records
OPERA/A_Archivio/Asset_Manifests/        asset manifests
20_OPERA_Dataset/internal/                complete private derived outputs
20_OPERA_Dataset/research/                filtered research-facing outputs
```

Existing free-form notes and templates are not migrated automatically. Records are promoted selectively after human review.

## 5. Identifier conventions

```text
OPERA-YYYY-MM-DD-NNN     entry
WORK-YYYY-NNNN           work
EXP-YYYY-MM-DD-NNN       experiment
ASSET-YYYY-MM-DD-NNN     individual asset manifest
BATCH-YYYY-MM-DD-NNN     asset batch manifest
```

Identifiers are stable. Status changes must not require moving or renaming a record.

## 6. Work lifecycle

Recommended work statuses:

```text
seed
concept
exploration
prototyping
in_progress
paused
resolved
exhibited
archived
```

A work record is mutable and accumulative. It stores the current proposition and a revision history. It may begin as an uncertain seed and later split into multiple works or merge into a series; such transformations must be recorded explicitly.

## 7. Experiment immutability

An experiment records what happened in one bounded practical session. After validation it should be treated as append-only except for factual corrections.

The record must distinguish:

```text
technical event
-> observation
-> artistic selection
-> transformation
-> interpretation
```

This is essential for expressive 3D scanning: a tracking failure, duplicated surface, false registration, hole, or texture artefact is not retrospectively treated as intentional merely because it becomes aesthetically useful.

## 8. 3D scanning modes

Experiments may declare:

```text
instrumental   acquisition for measurement, fitting, replication, or design
expressive     acquisition artefacts and sensor/software behaviour are part of the medium
hybrid         functional acquisition and artistic selection coexist
```

Preferred conceptual language for the emerging practice includes `expressive scanning`, `productive misregistration`, `aberrant capture`, `scan as inscription`, and `error-bearing acquisition`. The informal phrase “impressionistic scanning” may remain a provisional studio label but should not imply a historical connection to Impressionism unless that relation is argued.

## 9. Asset granularity

OPERA supports three practical levels:

- **individual manifest** for a significant mesh, drawing, photograph, video, fabrication file, or selected output;
- **batch manifest** for a folder produced by one session;
- **derived asset relation** for transformations such as raw scan -> cleaned mesh -> selected fragment -> printable model -> physical print -> rescan.

The vault need not contain every heavy file. A manifest may point to `vault`, `local_archive`, `external_drive`, or `cloud_archive`. The internal dataset may preserve absolute local paths; research exports must remove or normalize them.

## 10. Provenance layers

Every derived datum should be classifiable as:

- `declared`: supplied by the researcher in the Markdown source;
- `derived`: deterministically extracted from files or paths;
- `computed`: calculated from geometry, graph structure, or dataset state;
- `inferred`: generated through AI or interpretive classification, with model/method and confidence.

The first implementation must prioritize declared and derived data. AI-based interpretation is optional and must never overwrite source statements.

## 11. Parser scopes and backward compatibility

Add a scope option while preserving current behaviour:

```text
--scope capture   current behaviour; default
--scope studio    validate/export work, experiment, and asset records
--scope all       process both layers and build relations
```

Existing commands without `--scope` must continue to produce the same capture outputs and validation semantics.

## 12. Derived outputs

Capture outputs remain unchanged. Studio support adds:

```text
opera_works.internal.csv/jsonl
opera_experiments.internal.csv/jsonl
opera_assets.internal.csv/jsonl
opera_relations.internal.csv/jsonl
opera.sqlite
```

Research-facing equivalents are generated only after privacy filtering. The SQLite database is derived and replaceable; it must never become the manually edited source of truth.

Suggested SQLite tables:

```text
entries
works
experiments
assets
asset_files
relations
```

## 13. Privacy requirements

Body scans, identifiable photographs, biometric-like geometry, local paths, and third-party images require explicit flags. Studio schemas therefore distinguish at minimum:

- personal data;
- identifiable imagery;
- body-derived data;
- third-party material;
- location/path sensitivity;
- research export default.

The research profile must never expose absolute local file paths or body-derived assets by default.

## 14. Conversational workflow

The user may discuss works naturally without filling a form. A Studio record becomes canonical only after explicit archival intent, for example:

> Archive this session in OPERA Studio.

At that point an agent should:

1. locate an existing work or create a new seed;
2. update the persistent work record;
3. create an experiment record if a bounded practical action occurred;
4. create or update asset manifests when files exist;
5. validate identifiers and links;
6. run the official parser with the relevant scope;
7. report changed files, validation, outputs, and unresolved questions.

## 15. Pilot cases

The first two pilots are deliberately contrasting:

1. **Body-fitted jewellery**: neck and shoulder scanning used instrumentally or hybridly to create jewellery that sits against the skin.
2. **Expressive aberrant scanning**: fragmented, duplicated, misregistered, or incomplete acquisitions selected and transformed as aesthetic material.

These pilots should determine which fields are genuinely useful before old artwork notes are migrated.

## 16. Acceptance criteria

The first parser implementation is acceptable only if:

- all existing capture validation tests remain unchanged;
- default capture exports remain compatible;
- Studio records validate independently;
- broken identifiers and missing linked records are reported;
- missing asset files can be configured as warning or error;
- research outputs remove absolute paths and protect body-derived data;
- SQLite is regenerated atomically;
- the two pilot cases can be queried across work, experiment, asset, and entry relations.
