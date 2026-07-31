---
schema_version: 1
entity_type: asset
id: BATCH-YYYY-MM-DD-NNN
date: YYYY-MM-DD
manifest_kind: batch
status: declared
source:
  kind: filesystem-index
  agent: Claude Code
  captured_by: Christian
work_ids:
  - WORK-YYYY-NNNN
experiment_ids:
  - EXP-YYYY-MM-DD-NNN
asset_role: raw_capture
media_type: 3d_scan
storage:
  tier: local_archive
  root_path: C:/PATH/TO/ASSET/FOLDER
  path_kind: directory
  verify_exists: true
file_globs:
  - "*.obj"
  - "*.ply"
  - "*.stl"
  - "*.png"
  - "*.jpg"
derives_from:
privacy:
  contains_personal_data: false
  contains_identifiable_images: false
  contains_body_derived_data: false
  contains_third_party_material: false
  contains_sensitive_local_path: true
  research_export_default: exclude
---

# BATCH-YYYY-MM-DD-NNN

## Description

- Contenuto del file o del batch e sua funzione nella ricerca.

## Selection rationale

- Perché questo asset o batch è stato registrato, selezionato o mantenuto.

## Transformations

- Operazioni applicate o previste; collegare gli asset sorgente tramite `derives_from`.

## Technical notes

- Formati, compatibilità, integrità, geometria, texture e software pertinenti.

## Rights and restrictions

- Titolarità, persone riconoscibili, materiali di terzi e limiti di condivisione.

## Preservation notes

- Copie, supporti, rischi di perdita, migrazioni di formato e priorità di conservazione.
