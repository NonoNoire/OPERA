"""Generate OPERA datasets and validation reports from Markdown entries."""

from __future__ import annotations

import csv
import json
import os
import re
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / "00_OPERA_Capture"
DATASET_DIR = ROOT / "20_OPERA_Dataset"
CSV_PATH = DATASET_DIR / "opera_entries_index.csv"
JSONL_PATH = DATASET_DIR / "opera_entries.jsonl"
VALIDATION_PATH = DATASET_DIR / "opera_validation_report.md"

LIST_FIELDS = {
    "projects",
    "constraints",
    "waiting",
    "tags",
    "epistemic_status",
}

REQUIRED_METADATA = (
    "id",
    "date",
    "type",
    "source",
    "status",
)

REQUIRED_SECTIONS = (
    "Done",
    "Next",
    "Waiting",
    "Calendar",
    "Research state",
    "Critical note",
)

SUMMARY_OVERRIDES = {
    "R-000001": "Revisione semestrale completata e avvio della progettazione delle interviste.",
    "R-000002": "Malessere fisico e osservazione esplorativa di possibili variabili ambientali.",
    "R-000003": "Continuità creativa e raccolta di materiali durante un rallentamento dovuto alla salute.",
    "R-000004": "Continuità minima, routine quotidiana e acquisizione di un riferimento letterario.",
    "R-000005": "Ripresa metodologica orientata alla costruzione concreta della traccia di intervista.",
}


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def split_frontmatter(text: str, path: Path) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError(f"Frontmatter mancante: {path}")

    end = normalized.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"Frontmatter non chiuso: {path}")

    return normalized[4:end], normalized[end + 5 :]


def parse_frontmatter(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in raw.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if not raw_line.startswith(" "):
            key, separator, value = raw_line.partition(":")
            if not separator:
                continue
            key = key.strip()
            value = value.strip()
            current_key = key

            if value:
                data[key] = parse_scalar(value)
            elif key == "phase":
                data[key] = {}
            elif key in LIST_FIELDS:
                data[key] = []
            else:
                data[key] = ""
            continue

        stripped = raw_line.strip()
        if current_key in LIST_FIELDS and stripped.startswith("- "):
            data[current_key].append(parse_scalar(stripped[2:]))
        elif current_key == "phase":
            key, separator, value = stripped.partition(":")
            if separator:
                data["phase"][key.strip()] = parse_scalar(value)

    for field in LIST_FIELDS:
        data.setdefault(field, [])
    data.setdefault("phase", {})
    return data


def parse_sections(body: str) -> dict[str, list[str]]:
    sections = {name: [] for name in REQUIRED_SECTIONS}
    heading_aliases = {
        "Done": "Done",
        "Next": "Next",
        "Waiting": "Waiting",
        "Calendar": "Calendar",
        "Research state": "Research state",
        "Critical note": "Critical note",
        "Operational log": "Done",
        "Next actions": "Next",
        "Calendar actions": "Calendar",
        "Research-relevant content": "Research state",
        "Critical notes": "Critical note",
    }
    heading_pattern = re.compile(
        r"^## (Done|Next|Waiting|Calendar|Research state|Critical note|Operational log|Next actions|Calendar actions|Research-relevant content|Critical notes)\s*$",
        re.MULTILINE,
    )
    matches = list(heading_pattern.finditer(body))

    for index, match in enumerate(matches):
        name = heading_aliases[match.group(1)]
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if sections.get(name):
            continue
        sections[name] = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

    vnext_map = {
        "done": "Done",
        "next": "Next",
        "waiting": "Waiting",
        "calendar": "Calendar",
        "research state": "Research state",
        "critical note": "Critical note",
    }
    vnext_heading_pattern = re.compile(
        r"^(## \[[^\]]+\]|### (Done|Next|Waiting|Calendar|Research State|Critical Note))\s*$",
        re.MULTILINE,
    )
    vnext_matches = list(vnext_heading_pattern.finditer(body))
    for index, match in enumerate(vnext_matches):
        raw_heading = match.group(1)
        if raw_heading == "## [CALENDAR]":
            section_name = "Calendar"
        elif raw_heading.startswith("## "):
            continue
        else:
            section_name = vnext_map.get(raw_heading[4:].strip().lower())
        if not section_name or sections.get(section_name):
            continue
        start = match.end()
        end = vnext_matches[index + 1].start() if index + 1 < len(vnext_matches) else len(body)
        content = body[start:end].strip()
        sections[section_name] = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

    return sections


def first_meaningful_line(lines: list[str]) -> str:
    for line in lines:
        cleaned = re.sub(r"^[*-]\s+", "", line).strip()
        if cleaned:
            return cleaned
    return ""


def filename_date(path: Path) -> str:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    return match.group(1) if match else ""


def build_entry(path: Path, warnings: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    raw_frontmatter, body = split_frontmatter(text, path)
    metadata = parse_frontmatter(raw_frontmatter)
    sections = parse_sections(body)
    relative_path = path.relative_to(ROOT).as_posix()

    missing_fields = [
        field for field in REQUIRED_METADATA if not metadata.get(field)
    ]
    if missing_fields:
        raise ValueError(
            f"Campi obbligatori mancanti in {relative_path}: {', '.join(missing_fields)}"
        )

    missing_sections = [
        name for name in REQUIRED_SECTIONS if not sections.get(name)
    ]
    if missing_sections:
        warnings.append(
            f"{relative_path}: sezioni mancanti o vuote: {', '.join(missing_sections)}"
        )

    entry_id = metadata["id"]
    entry_date = metadata["date"]
    file_date = filename_date(path)
    if file_date and file_date != entry_date:
        warnings.append(
            f"{relative_path}: data filename {file_date} diversa da frontmatter {entry_date}"
        )
    elif not file_date:
        warnings.append(f"{relative_path}: data non riconosciuta nel nome file")

    summary = SUMMARY_OVERRIDES.get(
        entry_id,
        first_meaningful_line(sections["Research state"]),
    )

    return {
        "id": entry_id,
        "date": entry_date,
        "type": metadata["type"],
        "source": metadata["source"],
        "status": metadata["status"],
        "path": relative_path,
        "projects": metadata["projects"],
        "phase": metadata["phase"],
        "constraints": metadata["constraints"],
        "waiting": metadata["waiting"],
        "tags": metadata["tags"],
        "epistemic_status": metadata["epistemic_status"],
        "summary": summary,
        "sections": sections,
    }


def list_value(values: list[str]) -> str:
    return ";".join(values)


def safe_write_text(path: Path, content: str, newline: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline=newline,
        dir=path.parent,
        delete=False,
    ) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


def safe_write_csv(path: Path, entries: list[dict[str, Any]]) -> None:
    fieldnames = [
        "id",
        "date",
        "type",
        "status",
        "path",
        "projects",
        "research_phase",
        "dissertation_phase",
        "opera_phase",
        "constraints",
        "waiting",
        "tags",
        "epistemic_status",
        "summary",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        delete=False,
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            phase = entry["phase"]
            writer.writerow(
                {
                    "id": entry["id"],
                    "date": entry["date"],
                    "type": entry["type"],
                    "status": entry["status"],
                    "path": entry["path"],
                    "projects": list_value(entry["projects"]),
                    "research_phase": phase.get("research", ""),
                    "dissertation_phase": phase.get("dissertation", ""),
                    "opera_phase": phase.get("opera", ""),
                    "constraints": list_value(entry["constraints"]),
                    "waiting": list_value(entry["waiting"]),
                    "tags": list_value(entry["tags"]),
                    "epistemic_status": list_value(entry["epistemic_status"]),
                    "summary": entry["summary"],
                }
            )
        temp_name = handle.name
    os.replace(temp_name, path)


def write_csv(entries: list[dict[str, Any]]) -> list[str]:
    safe_write_csv(CSV_PATH, entries)
    return [entry["id"] for entry in entries]


def write_jsonl(entries: list[dict[str, Any]]) -> list[str]:
    lines = [
        json.dumps(entry, ensure_ascii=False)
        for entry in entries
    ]
    content = "\n".join(lines) + ("\n" if lines else "")
    safe_write_text(JSONL_PATH, content, newline="\n")
    return [entry["id"] for entry in entries]


def markdown_list(items: list[str], empty: str = "None") -> str:
    if not items:
        return f"* {empty}"
    return "\n".join(f"* {item}" for item in items)


def build_validation_report(
    paths: list[Path],
    entries: list[dict[str, Any]],
    csv_ids: list[str],
    jsonl_ids: list[str],
    warnings: list[str],
    errors: list[str],
    read_error_count: int,
) -> str:
    ids = [entry["id"] for entry in entries]
    counts = Counter(ids)
    duplicate_ids = sorted(entry_id for entry_id, count in counts.items() if count > 1)
    missing_ids = [
        entry["path"] for entry in entries if not entry.get("id")
    ]
    missing_dates = [
        entry["path"] for entry in entries if not entry.get("date")
    ]
    missing_required_sections = [
        warning for warning in warnings if "sezioni mancanti o vuote" in warning
    ]
    filename_date_mismatches = [
        warning for warning in warnings if "data filename" in warning
    ]
    csv_jsonl_match = csv_ids == jsonl_ids
    silent_skip_count = len(paths) - len(entries) - read_error_count

    duplicate_message = f"ID duplicati: {', '.join(duplicate_ids)}"
    if duplicate_ids and duplicate_message not in errors:
        errors.append(f"ID duplicati: {', '.join(duplicate_ids)}")
    if not csv_jsonl_match:
        errors.append("Gli ID esportati in CSV e JSONL non coincidono.")
    if silent_skip_count != 0:
        errors.append(
            f"Possibile salto silenzioso: {silent_skip_count} entry non esportate senza errore di lettura."
        )

    parser_status = "OK" if not errors else "ERROR"
    unique_ids = sorted(set(ids))

    return "\n".join(
        [
            "# OPERA Validation Report",
            "",
            f"* Validation date: {date.today().isoformat()}",
            f"* Entries scanned: {len(paths)}",
            f"* Entries exported to CSV: {len(csv_ids)}",
            f"* Entries exported to JSONL: {len(jsonl_ids)}",
            f"* Unique IDs found: {len(unique_ids)}",
            "",
            "## Unique IDs found",
            "",
            markdown_list(unique_ids),
            "",
            "## Duplicate IDs",
            "",
            markdown_list(duplicate_ids),
            "",
            "## Missing IDs",
            "",
            markdown_list(missing_ids),
            "",
            "## Missing dates",
            "",
            markdown_list(missing_dates),
            "",
            "## Filename/date mismatches",
            "",
            markdown_list(filename_date_mismatches),
            "",
            "## Missing required sections",
            "",
            markdown_list(missing_required_sections),
            "",
            "## CSV/JSONL ID consistency",
            "",
            f"* {'OK' if csv_jsonl_match else 'Mismatch'}",
            "",
            "## Warnings",
            "",
            markdown_list(warnings),
            "",
            "## Errors",
            "",
            markdown_list(errors),
            "",
            "## Parser status",
            "",
            f"* {parser_status}",
            "",
        ]
    )


def main() -> None:
    if not CAPTURE_DIR.exists():
        raise SystemExit(f"Archivio non trovato: {CAPTURE_DIR}")

    paths = sorted(CAPTURE_DIR.rglob("*.md"))
    entries: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []
    read_error_count = 0

    for path in paths:
        try:
            entries.append(build_entry(path, warnings))
        except Exception as exc:
            read_error_count += 1
            errors.append(f"{path.relative_to(ROOT).as_posix()}: {exc}")

    entries.sort(key=lambda entry: (entry["date"], entry["id"]))

    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        duplicated = sorted(
            entry_id for entry_id, count in Counter(ids).items() if count > 1
        )
        errors.append(f"ID duplicati: {', '.join(duplicated)}")

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    csv_ids = write_csv(entries)
    jsonl_ids = write_jsonl(entries)
    report = build_validation_report(
        paths,
        entries,
        csv_ids,
        jsonl_ids,
        warnings,
        errors,
        read_error_count,
    )
    safe_write_text(VALIDATION_PATH, report, newline="\n")

    print(f"Entry scansionate: {len(paths)}")
    print(f"Entry esportate: {len(entries)}")
    print(f"CSV generato: {CSV_PATH}")
    print(f"JSONL generato: {JSONL_PATH}")
    print(f"Report validazione generato: {VALIDATION_PATH}")
    print(f"Warning: {len(warnings)}")
    print(f"Errori: {len(errors)}")
    print("Parser status: OK" if not errors else "Parser status: ERROR")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
