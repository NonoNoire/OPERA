# Vault

The personal Obsidian vault remains conceptually separate from this repository.

This directory documents the relationship between OPERA as a shareable research method and the private working vault used during doctoral research.

The repository should contain only material that is suitable for sharing, revision, or future publication. Personal notes, sensitive data, private reflections, and unpublished research materials should remain outside the repository unless they have been deliberately anonymised and approved for inclusion.

## OPERA-Capture

`vault/OPERA-Capture/` is a controlled bridge for structured capture notes produced through the OPERA workflow.

It may contain selected check-ins, check-outs, and review notes that the researcher deliberately chooses to version. This is not a full mirror of the private Obsidian vault.

The intended flow is:

```text
ChatGPT conversation
  -> OPERA_EXPORT block
  -> Codex extraction
  -> Markdown note in vault/OPERA-Capture
  -> Git commit
  -> Obsidian synchronisation
```

This keeps Obsidian as the primary research environment while allowing OPERA to preserve a versioned sequence of methodological checkpoints.
