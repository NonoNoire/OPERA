# Local Register Sync

This note documents a practical issue discovered during OPERA v0.3 testing.

The structured capture note for `R-000001` was correctly saved in:

```text
vault/OPERA-Capture/2026/06/2026-06-19-r-000001.md
```

However, the operational Obsidian registers used in the daily workflow may live outside the shareable OPERA repository, for example:

```text
01_Registro_giornaliero.md
03_Next_actions.md
04_Attese_Follow-up.md
06_Registro_GRADED.md
```

This means that a checkpoint can exist as a capture note without appearing in the practical daily dashboard.

## Fix

Run the local sync script from the root of the actual Obsidian/OPERA vault:

```bash
python scripts/opera_sync_r000001_registers.py
```

The script is conservative and idempotent:

- it updates only the known operational register files;
- it skips files that are not present;
- it does not overwrite existing content;
- it marks the inserted block with `OPERA:R-000001` so it will not duplicate the entry if run twice.

## Methodological lesson

OPERA needs two related but distinct archival levels:

1. **Capture notes**, which preserve stable research checkpoints.
2. **Operational registers**, which make those checkpoints visible in the daily workflow.

Future OPERA automation should update both levels.
