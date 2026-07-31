# OPERA Studio conversational protocol

## Purpose

This protocol defines how a natural conversation about an artwork becomes a canonical OPERA Studio update without forcing the researcher to complete a form during ideation.

## 1. Default state: exploratory conversation

A conversation about an artwork, material, drawing, scan, sculpture, installation, or technique is exploratory by default. The agent may help develop the idea, identify assumptions, compare alternatives, or formulate experiments, but it must not silently create canonical records.

## 2. Archival trigger

Canonical writing begins only after explicit archival intent, for example:

- `Archivia questa idea in OPERA Studio.`
- `Aggiorna la scheda dell'opera.`
- `Registra questa prova come esperimento.`
- `Indicizza questi file come asset.`

The user may also request archival and analysis in the same message.

## 3. Classification

At archival time, classify the material into one or more operations:

```text
create_work
update_work
create_experiment
create_asset_manifest
link_entry
link_reading
split_work
merge_work
change_status
```

Do not create an experiment when only an idea was discussed. Do not create an asset manifest when no real file or storage location exists.

## 4. Minimal questioning rule

Do not convert the conversation into an exhaustive interview. Use information already present. Ask only when a missing fact would make the record materially false or structurally invalid.

Minor uncertainty must be represented explicitly:

```text
provisional
unknown
not_recorded
not_applicable
```

Never invent materials, dimensions, software versions, asset paths, or completed actions.

## 5. Work matching

Before creating a work record:

1. search existing work IDs, titles, aliases, and propositions;
2. identify the strongest candidate;
3. update it when the identity is clear;
4. create a new `seed` when the idea is materially distinct;
5. preserve ambiguity when it is unclear whether two ideas belong to one work or a series.

Possible future split or merge decisions belong in `Open questions` until explicitly resolved.

## 6. Experiment boundary

Create an experiment when there is a bounded practical action with at least:

- a date;
- an intent or question;
- an actual procedure or event;
- an observation or result.

An experiment may be failed, aborted, or technically incomplete. Failure is a valid state and must not be rewritten as success.

## 7. Technical event versus artistic selection

For scans and other computational media, archive in this order:

1. technical event;
2. probable or known cause;
3. whether it was deliberately produced;
4. whether it was artistically selected;
5. subsequent transformation;
6. provisional interpretation.

This prevents accidental artefacts from being retroactively described as intended while preserving their aesthetic productivity.

## 8. Asset handling

When files are involved:

- use an individual manifest for a significant selected file;
- use a batch manifest for a session folder;
- record storage tier and path;
- calculate file metadata and hashes deterministically;
- never infer semantic meaning from an image or mesh without marking it as inferred;
- never expose absolute local paths in research-facing exports.

## 9. Transaction preview

Before local writing, the agent should formulate an internal transaction plan:

```text
records_to_create
records_to_update
relations_to_add
asset_paths_to_verify
privacy_flags
validation_commands
```

If the intended operation would overwrite a conflicting record, stop and report the conflict.

## 10. Idempotent write

The archival operation must be idempotent:

- do not duplicate an existing relation;
- do not create a second record for the same experiment;
- preserve existing prose not contradicted by the new material;
- append a dated revision-history line to changed work records;
- preserve validated experiment records except for explicit factual correction.

## 11. Post-write validation

After writing:

1. run parser validation for `studio`;
2. run parser validation for `all`;
3. regenerate internal outputs;
4. regenerate research outputs only when privacy behaviour is under test or requested;
5. verify new IDs appear exactly once;
6. verify linked IDs resolve;
7. verify asset paths according to their configured strictness;
8. report changed files and validation status.

## 12. Relation to daily checkout

The daily checkout may mention Studio IDs, but archival independence is preserved:

- a Studio update does not automatically create a daily checkout;
- a daily checkout does not automatically rewrite a work record;
- when both occur, explicit IDs connect them;
- the same event may be represented narratively in the entry and structurally in the experiment without duplicating the full text.

## 13. Recommended user interaction

The user can speak normally throughout the creative process. A concise archival command at the end is sufficient. The agent is responsible for converting the conversation into the smallest valid set of persistent records while preserving uncertainty and provenance.
