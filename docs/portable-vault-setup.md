# OPERA portable vault setup

OPERA should be usable from more than one computer without relying on Obsidian Sync.

The basic model is simple:

- GitHub stores the repository.
- Obsidian opens the local folder as a vault.
- The stable vault folder is `MicioVault`.
- The stable capture folder is `MicioVault/00_OPERA_Capture`.

## Secondary computer

On a second computer, clone the repository from GitHub. Then open Obsidian and choose the local `MicioVault` folder as a vault.

Suggested local path after cloning:

`OPERA/MicioVault`

## Working habit

At the beginning of a work session, update the local repository from GitHub.

At the end of a work session, save changes, commit them, and push them back to GitHub.

## Primary computer migration

When using the primary computer again, copy the existing local `MicioVault` into the `OPERA` repository so that the repository contains the canonical version of the vault.

After that point, avoid maintaining two independent versions of the vault.

## Critical rule

The repository-backed `MicioVault` should become the single source of truth. Any other copy should be treated as temporary or historical.
