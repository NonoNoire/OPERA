# OPERA v2 Draft

Agents should not start from this file.

The operational entry point for agents is:

```text
90_OPERA_Tools/AGENT_BOOTSTRAP.md
```

This document explains the OPERA v2 draft parser layer after the agent has read
the bootstrap file.

This folder is a non-destructive draft toolkit layer for OPERA v2.

It does not replace the current parser and it does not convert existing entries.
Existing `OPERA-*.md` files in `00_OPERA_Capture` are treated as canonical v1 entries.
Future entries may use `schema_version: 2`.

## Intended workflow

```text
User talks to ChatGPT
-> ChatGPT structures the OPERA checkout
-> Codex writes Markdown in the local Obsidian vault
-> Obsidian Sync synchronizes the vault
-> OPERA parser validates and exports datasets
```

## Stable local paths

```text
Vault root: C:/Users/chris/Desktop/MicioVault
Capture archive: C:/Users/chris/Desktop/MicioVault/00_OPERA_Capture
Dataset folder: C:/Users/chris/Desktop/MicioVault/20_OPERA_Dataset
```

## Draft commands

Run validation without writing exports:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py validate --vault-root "C:\Users\chris\Desktop\MicioVault"
```

Generate internal export:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
```

Generate research-facing filtered export:

```powershell
py 90_OPERA_Tools\opera_v2_draft\parser_v2.py parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

The eventual packaged CLI target is:

```powershell
opera validate --vault-root "C:\Users\chris\Desktop\MicioVault"
opera parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile internal
opera parse --vault-root "C:\Users\chris\Desktop\MicioVault" --profile research
```

## Privacy rule

The research export excludes calendar, waiting, operational, and personal/contextual logistics by default. These sections remain available in the internal export.

## Export privacy policy

The internal export is complete and private. It includes all sections, full
metadata, operational context, calendar actions, waiting items, personal context,
and local paths. It is intended for local analysis inside the user's own vault.

The research export is filtered and conservative. It is intended as a draft
research-facing dataset, not as a publication-ready anonymized corpus.

Existing v1 entries are not considered research-clean by default. Because v1
entries do not separate research material from personal, calendar, waiting, and
logistical context, the research export writes them as review stubs:

```json
"research_export_status": "needs_review"
```

For v1 entries, the research export keeps minimal metadata and a conservative
summary. It does not include full section text unless a future explicit review
policy is added.

Future v2 entries can become research-clean only through explicit metadata:

```yaml
export_profile:
  research: true
privacy:
  contains_personal_data: false
  contains_health_data: false
  contains_calendar_data: false
  contains_third_party_names: false
  research_export_default: include
research_relevance: high
```

When `privacy.research_export_default` is `filtered`, the entry may still appear
in the research export, but it is marked as filtered. When privacy flags or
sensitivity keywords are detected, the entry is marked `needs_review`.

Running the research export also creates:

```text
20_OPERA_Dataset/research/opera_privacy_audit.research.md
```

The audit report lists scanned entries, exported entries, entries needing review,
excluded entries, flags by category, flagged phrases, and recommended actions.

## Export audit vs source audit

The privacy audit has two layers:

* `export_content_audit` checks only text that is actually emitted in the
  research JSONL/CSV. This layer determines `research_export_status` and
  `recommended_action`.
* `source_content_audit` checks the full original entry for internal awareness.
  Source-only flags do not automatically make a research export unsafe when the
  flagged text is not exported.

Research JSONL records include:

```json
"source_privacy_flags": [],
"export_privacy_flags": [],
"source_context_markers": [],
"export_context_markers": [],
"safe_methodological_terms_detected": [],
"research_export_status": "safe",
"recommended_action": "keep",
"audit_scope": "export_content_audit",
"audit_notes": [],
"anonymization_suggestions": {}
```

Supported research export statuses:

* `safe`
* `needs_review`
* `anonymize_before_use`
* `internal_only`

Supported recommended actions:

* `keep`
* `manual_review`
* `anonymize`
* `internal_only`
* `exclude_from_research_export`

## Privacy rules

Default privacy rules are documented in:

```text
90_OPERA_Tools/opera_v2_draft/privacy_rules.example.json
```

For local overrides, create:

```text
90_OPERA_Tools/opera_v2_draft/privacy_rules.local.json
```

The parser loads the example rules and then applies local overrides when present.

## Detection classes

The audit separates three classes of detection:

* `privacy_flags`: actual privacy or sensitivity risks, such as health,
  bodily condition, client-sensitive material, third-party-sensitive narrative,
  named people, or detailed calendar/travel/personal logistics.
* `context_markers`: useful context that is not private by default, such as
  project labels, generic institutions, role references, and generic deadline
  markers.
* `safe_methodological_terms_detected`: method vocabulary that should not be
  treated as sensitive, such as interviews, codebook, coding, memo, audit trail,
  credibility, transferability, dependability, and confirmability.

Research export status depends on `export_privacy_flags`, not on source-only
flags, context markers, or safe methodological terms.

The Markdown privacy audit is intentionally concise. It deduplicates repeated
hits inside the same entry and section, and reports occurrence counts instead of
printing the same term repeatedly.

## Privacy behavior examples

False positives to avoid:

* `interviste` should be `safe_methodological`, not `project_sensitive`.
* `ore` alone should not be `calendar_detail`.
* `online` alone should not be `personal_logistics`.
* `prof.` alone should be `role_reference`, not `third_party_sensitive`.
* `GRADED` alone should be `project_label` or institution/context, not automatically `internal_only`.

True positives:

* `malessere fisico` should be `health` / `bodily_condition`.
* `concerto a Firenze il 15 luglio alle 20:30` should flag calendar/travel/personal context.
* `collega valutato negativamente` should be `third_party_sensitive`.
* `cliente del progetto editoriale` should be `client_sensitive`.
* `Eshun` should be `third_party_name`.
* `Goldsmiths` should be `institution`.

## Agent bootstrap

This folder contains the official OPERA parser:

```text
90_OPERA_Tools/opera_v2_draft/parser_v2.py
```

Agents must always use this parser before considering any reconstruction of the
toolchain behavior.

If `parser_v2.py` is genuinely missing, stop the work and ask for instructions.

Do not create alternative parsers.

Do not infer parser behavior from previous reports, generated datasets, CSV files,
JSONL files, or summaries.

Do not generate CSV or JSONL outputs without using the official parser.
