# OPERA Toolchain Manifest

## Identity

- Project: OPERA
- Component: local research toolchain
- Status: v2 draft / stabilization
- Canonical parser: `90_OPERA_Tools/opera_v2_draft/parser_v2.py`

## Canonical paths

- Vault root: `C:/Users/chris/Desktop/MicioVault`
- Capture archive: `00_OPERA_Capture`
- Dataset folder: `20_OPERA_Dataset`
- Toolchain folder: `90_OPERA_Tools`

## Supported schemas

- v1 entries: tolerated / review stubs in research export
- v2 entries: supported

## Export profiles

- internal: complete private export
- research: conservative filtered export

## Agent policy

- agents must read `AGENT_BOOTSTRAP.md` first
- agents must use the official parser
- agents must stop if the parser is missing
- agents must not reconstruct parser behavior from reports or datasets

## Source of truth

- Markdown entries are the source data
- `parser_v2.py` is the operational source of truth
- JSONL/CSV/report files are generated artifacts
- documentation improves discoverability but does not redefine behavior

## Future release target

- Possible future package/CLI: `opera validate`, `opera parse`
- Possible future stable folder: `opera_v2`
- Current instruction: do not rename folders during this documentation pass
