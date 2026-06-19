#!/usr/bin/env python3
"""Sync checkpoint R-000001 into the operational Obsidian registers.

Run this script from the root of the local Obsidian/OPERA vault.

It is intentionally conservative:
- it updates only known operational register files;
- it does not overwrite existing content;
- it inserts marked blocks so the operation is idempotent;
- if a file does not exist, it is skipped.
"""

from __future__ import annotations

from pathlib import Path


CHECKPOINT_ID = "R-000001"
START = f"<!-- OPERA:{CHECKPOINT_ID}:START -->"
END = f"<!-- OPERA:{CHECKPOINT_ID}:END -->"


DAILY_REGISTER = """\
{start}

## 2026-06-19

### Fatto

- Completata, firmata e consegnata la revisione semestrale del dottorato dopo l'approvazione della prof.ssa Buffardi e del prof. Cassani.
- Collegato GitHub a Codex per integrare meglio Obsidian e iniziare a costruire un workflow con AI agents.
- Ricevuto l'ok della prof.ssa Buffardi sul documento programmatico della tesi; prossimo passo indicato: elaborazione della prima traccia delle interviste semistrutturate.
- Avviata OPERA v0.3 come workflow di cattura conversazionale: ChatGPT → OPERA_EXPORT → Codex → Markdown → GitHub/Obsidian.

### Decisioni

- Usare Obsidian come fonte primaria della ricerca.
- Usare ChatGPT come interfaccia conversazionale per check-in, check-out e revisioni.
- Usare Codex/GitHub come ponte operativo e sistema di versionamento.
- Integrare nei check-out il campo “Stato della ricerca” come checkpoint epistemologico.

### In attesa

- Risposta della Goldsmiths riguardo al periodo visiting.

### Prossime azioni

- Scrivere una prima versione della traccia di intervista semistrutturata per la ricerca qualitativa della tesi.
- Rivedere il documento operativo relativo allo stage GRADED.
- Riprendere il documento programmatico di 30-40 pagine come seme della dissertation.

### Calendar

- Nessuna nuova scadenza da inserire.

### Stato della ricerca

- Il progetto entra nella fase empirica: si passa dalla definizione teorico-metodologica alla progettazione dello strumento di raccolta dati attraverso le interviste semistrutturate.

{end}
""".format(start=START, end=END)


NEXT_ACTIONS = """\
{start}

## R-000001 — 2026-06-19

- [ ] Scrivere una prima versione della traccia di intervista semistrutturata per la ricerca qualitativa della tesi.
- [ ] Rivedere il documento operativo relativo allo stage GRADED.
- [ ] Riprendere il documento programmatico di 30-40 pagine come seme della dissertation.

{end}
""".format(start=START, end=END)


FOLLOW_UP = """\
{start}

## R-000001 — 2026-06-19

- [ ] Goldsmiths: attendere risposta sul periodo visiting abroad.
- [x] Buffardi: ok ricevuto sul documento programmatico della tesi; passare alla stesura delle domande per le interviste semistrutturate.

{end}
""".format(start=START, end=END)


GRADED_REGISTER = """\
{start}

## 2026-06-19

- Prossima azione: rivedere il documento operativo relativo allo stage GRADED e riallinearlo alla fase attuale del dottorato.
- Nota metodologica: mantenere GRADED come asse applicativo e documentale del progetto, evitando collegamenti retorici troppo diretti con Oblivion se non sostenuti da un protocollo chiaro.

{end}
""".format(start=START, end=END)


TARGETS = {
    "01_Registro_giornaliero.md": DAILY_REGISTER,
    "03_Next_actions.md": NEXT_ACTIONS,
    "04_Attese_Follow-up.md": FOLLOW_UP,
    "06_Registro_GRADED.md": GRADED_REGISTER,
}


def append_once(path: Path, block: str) -> str:
    if not path.exists():
        return f"skipped missing: {path}"

    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        return f"already synced: {path}"

    separator = "\n\n" if text.strip() else ""
    path.write_text(text.rstrip() + separator + block.rstrip() + "\n", encoding="utf-8")
    return f"updated: {path}"


def main() -> int:
    root = Path.cwd()
    for filename, block in TARGETS.items():
        print(append_once(root / filename, block))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
