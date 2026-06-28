# Vault — Legacy Folder

> **This folder is legacy.** New captures must not be written here.
>
> The canonical Obsidian vault is `MicioVault/` at the repository root.
> The canonical capture directory is `MicioVault/00_OPERA_Capture/`.

This directory was the original capture destination before the migration to the `MicioVault` structure. It is preserved for historical continuity, migration checks, and audit trails. It should not receive new OPERA captures during normal work.

Do not delete legacy files unless a future migration pass confirms that the material is safely preserved, intentionally excluded, or no longer needed.

## OPERA-Capture (legacy)

`vault/OPERA-Capture/` contains early OPERA capture notes from the period before the canonical structure was established. Notes here use the legacy `R-000NNN` identifier format and a year/month subdirectory layout (`2026/06/...`).

The active capture flow is documented in `docs/Conversational-Capture.md`.

The canonical capture destination is `MicioVault/00_OPERA_Capture/` using the `OPERA-YYYY-MM-DD-NNN.md` filename convention.

## Contents

- `2026/06/2026-06-19-r-000001.md`: first OPERA capture note (legacy format). Migrated content is available at `MicioVault/00_OPERA_Capture/OPERA-2026-06-19-001.md`.
- `2026/06/2026-06-24-r-000005.md`: daily check-out / interim checkpoint (legacy format). Migrated content is available at `MicioVault/00_OPERA_Capture/OPERA-2026-06-24-001.md`.

Legacy entries may remain here for historical reference even after migration. Any legacy entries not explicitly migrated may remain unindexed unless a future migration pass decides otherwise.

## Future Capture Flow

New structured captures should follow this path:

```text
ChatGPT conversation
  -> OPERA_EXPORT block
  -> Codex extraction
  -> Markdown note in MicioVault/00_OPERA_Capture/
  -> dataset index refresh when appropriate
  -> Git commit
  -> Obsidian reading and linking
```

This keeps Obsidian as the primary research environment while allowing OPERA to preserve a versioned sequence of methodological checkpoints.
