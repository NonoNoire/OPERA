# Vault

This directory is legacy.

The canonical repository-backed Obsidian vault is now:

```text
MicioVault/
```

The canonical OPERA capture archive is now:

```text
MicioVault/00_OPERA_Capture/
```

## Legacy Status

`vault/` and `vault/OPERA-Capture/` are retained only for historical reference, migration checks, and audit trails. They should not receive new OPERA captures during normal work.

Do not delete legacy files unless a future migration pass confirms that the material is safely preserved, intentionally excluded, or no longer needed.

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
