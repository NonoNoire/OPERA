"""Draft OPERA v2 parser.

This is a non-destructive draft parser. It reads canonical OPERA entries from an
external vault path and can validate or export internal/research datasets.
It intentionally does not replace the current OPERA parser.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import tempfile
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any


V1_REQUIRED_SECTIONS = (
    "Done",
    "Next",
    "Waiting",
    "Calendar",
    "Research state",
    "Critical note",
)

V2_REQUIRED_SECTIONS = (
    "Research-relevant content",
    "Methodological notes",
    "Operational log",
    "Next actions",
    "Waiting",
    "Calendar actions",
    "Personal/contextual logistics",
    "Critical notes",
)

RESEARCH_SECTION_MAP_V1 = {
    "Research state": "Research-relevant content",
    "Critical note": "Critical notes",
}

RESEARCH_SECTION_MAP_V2 = {
    "Research-relevant content": "Research-relevant content",
    "Methodological notes": "Methodological notes",
    "Critical notes": "Critical notes",
}

INTERNAL_CSV_FIELDS = (
    "id",
    "date",
    "schema_version",
    "type",
    "status",
    "path",
    "projects",
    "research_relevance",
    "summary",
)

RESEARCH_CSV_FIELDS = (
    "id",
    "date",
    "schema_version",
    "type",
    "status",
    "projects",
    "research_relevance",
    "research_export_status",
    "recommended_action",
    "export_privacy_flags",
    "source_privacy_flags",
    "export_context_markers",
    "source_context_markers",
    "safe_methodological_terms_detected",
    "summary",
)

DEFAULT_PRIVACY_RULES = {
    "safe_methodological_terms": [
        "interviste",
        "intervista",
        "semi-strutturata",
        "semi-strutturate",
        "codebook",
        "codifica",
        "coding",
        "CAQDAS",
        "NVivo",
        "ATLAS.ti",
        "MAXQDA",
        "Dedoose",
        "Taguette",
        "IPA",
        "interpretative phenomenological analysis",
        "narrative inquiry",
        "visual methods",
        "artifact elicitation",
        "organizational ethnography",
        "audit trail",
        "triangulation",
        "member checking",
        "saturation",
        "information power",
        "research through design",
        "practice-based research",
        "thematic analysis",
        "memo",
        "memo teorici",
        "sensitizing concepts",
        "thick description",
        "credibility",
        "transferability",
        "dependability",
        "confirmability",
    ],
    "project_labels": ["OPERA", "GRADED", "Oblivion", "tesi", "dottorato", "PhD", "dissertation"],
    "institution_terms": ["Goldsmiths", "universita", "università", "accademia", "Graduate School", "host institution"],
    "known_person_terms": ["Eshun", "Buffardi", "Cassani"],
    "role_terms": ["collega", "docente", "supervisor", "prof.", "prof.ssa", "relatore", "correlatore"],
    "third_party_escalation_terms": [
        "maltrattato",
        "valutato negativamente",
        "non ha saputo difendere",
        "conflitto",
        "problema",
        "critica",
        "rifiuto",
        "risposta privata",
        "fallimento",
    ],
    "health_terms": [
        "sintomi",
        "malessere",
        "fisic",
        "corpo",
        "corporeo",
        "gastrite",
        "reflusso",
        "nausea",
        "pelle",
        "follicolite",
        "farmaco",
        "terapia",
        "salute",
        "condizione fisica",
        "pH interno",
        "dolore",
        "febbre",
    ],
    "personal_logistics_terms": [
        "cena",
        "Pride",
        "festa",
        "impegni personali",
        "viaggio",
        "trasferta",
        "concerto",
        "partenza",
        "arrivo",
        "internet assente",
        "famiglia",
        "casa",
        "boyfriend",
        "partner",
        "fidanzato",
        "dormire",
        "sonno",
    ],
    "client_sensitive_terms": ["cliente", "client"],
    "client_escalation_terms": ["negoziazione", "pagamento", "compenso", "accettazione", "rifiuto", "commerciale"],
    "calendar_regexes": [
        "\\b\\d{1,2}[:.]\\d{2}\\b",
        "\\bore\\s+\\d{1,2}([:.]\\d{2})?\\b",
        "\\balle\\s+\\d{1,2}([:.]\\d{2})?\\b",
        "\\b\\d{1,2}\\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\\b",
        "\\b(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\\s+\\d{4}\\b",
        "\\bmet[aà]\\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\\b",
    ],
    "calendar_terms": [
        "calendar",
        "calendario",
        "scadenza",
        "deadline",
        "reminder",
        "promemoria",
        "fissare",
        "programmare",
        "partenza",
        "arrivo",
        "cancelli",
        "concerto",
        "trasferta",
        "viaggio",
        "volo",
        "treno",
    ],
    "anonymization_map": {
        "GRADED": "Partner Organization",
        "Goldsmiths": "Host Institution",
        "Eshun": "Potential Host Tutor",
        "Buffardi": "Supervisor",
        "Cassani": "Academic Contact",
        "cliente": "Client",
        "client": "Client",
    },
}

SEVERITY_ORDER = {
    "safe_methodological": 0,
    "contextual_review": 1,
    "sensitive_anonymize": 2,
    "block_internal_only": 3,
}

CONTEXT_MARKER_CATEGORIES = {
    "project_label",
    "institution",
    "role_reference",
}

ALWAYS_PRIVACY_CATEGORIES = {
    "health",
    "bodily_condition",
    "client_sensitive",
    "third_party_sensitive",
}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in {"null", "none", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def split_frontmatter(text: str, path: Path) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError(f"Missing frontmatter: {path}")
    end = normalized.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"Unclosed frontmatter: {path}")
    return normalized[4:end], normalized[end + 5 :]


def parse_frontmatter(raw: str) -> dict[str, Any]:
    """Parse the small YAML subset used by current OPERA entries."""
    data: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, data)]
    last_key_at_indent: dict[int, str] = {}

    for raw_line in raw.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if stripped.startswith("- "):
            item = parse_scalar(stripped[2:])
            if isinstance(parent, list):
                parent.append(item)
            continue

        key, separator, value = stripped.partition(":")
        if not separator:
            continue

        key = key.strip()
        value = value.strip()

        if value:
            parsed: Any = parse_scalar(value)
            parent[key] = parsed
            last_key_at_indent[indent] = key
            continue

        next_container: Any = {}
        parent[key] = next_container
        last_key_at_indent[indent] = key
        stack.append((indent, next_container))

    # Convert empty dict containers followed by list items in common OPERA fields.
    for list_key in ("projects", "tags", "constraints", "waiting", "epistemic_status"):
        if data.get(list_key) == {}:
            data[list_key] = []

    # Second pass for simple list fields, because minimal YAML parsing above cannot
    # infer list containers before seeing the first item.
    data = normalize_list_fields(raw, data)
    return data


def normalize_list_fields(raw: str, data: dict[str, Any]) -> dict[str, Any]:
    list_fields = {"projects", "tags", "constraints", "waiting", "epistemic_status"}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or line.startswith(" ") or ":" not in stripped:
            index += 1
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        if key not in list_fields or value.strip():
            index += 1
            continue
        items: list[Any] = []
        child_index = index + 1
        while child_index < len(lines):
            child = lines[child_index]
            if child.strip() == "":
                child_index += 1
                continue
            if not child.startswith(" "):
                break
            child_stripped = child.strip()
            if child_stripped.startswith("- "):
                items.append(parse_scalar(child_stripped[2:]))
            child_index += 1
        data[key] = items
        index = child_index
    return data


def parse_sections(body: str) -> dict[str, list[str]]:
    heading_pattern = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
    matches = list(heading_pattern.finditer(body))
    sections: dict[str, list[str]] = {}

    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        sections[name] = lines
    return sections


def first_meaningful_line(lines: list[str]) -> str:
    for line in lines:
        cleaned = re.sub(r"^[-*]\s+", "", line).strip()
        cleaned = re.sub(r"^\[[ xX]\]\s+", "", cleaned).strip()
        if cleaned and cleaned != "-":
            return cleaned
    return ""


def clean_phrase(line: str) -> str:
    cleaned = re.sub(r"^[-*]\s+", "", line).strip()
    cleaned = re.sub(r"^\[[ xX]\]\s+", "", cleaned).strip()
    return cleaned


def load_privacy_rules() -> dict[str, Any]:
    rules = json.loads(json.dumps(DEFAULT_PRIVACY_RULES))
    base_dir = Path(__file__).resolve().parent
    for filename in ("privacy_rules.example.json", "privacy_rules.local.json"):
        path = base_dir / filename
        if not path.exists():
            continue
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for key, value in loaded.items():
            rules[key] = value
    return rules


def contains_term(text: str, term: str) -> bool:
    if not term:
        return False
    return term.lower() in text.lower()


def add_flag(
    flags: list[dict[str, str]],
    seen: set[tuple[str, str, str]],
    category: str,
    severity: str,
    phrase: str,
    note: str = "",
) -> None:
    key = (category, severity, phrase.lower())
    if key in seen:
        return
    flags.append(
        {
            "category": category,
            "severity": severity,
            "phrase": phrase,
            "note": note,
        }
    )
    seen.add(key)


def detect_privacy_flags(text: str, rules: dict[str, Any] | None = None) -> list[dict[str, str]]:
    rules = rules or load_privacy_rules()
    flags: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    lowered = text.lower()

    for term in rules["safe_methodological_terms"]:
        if contains_term(text, term):
            add_flag(flags, seen, "safe_methodological", "safe_methodological", term)

    for term in rules["project_labels"]:
        if contains_term(text, term):
            add_flag(flags, seen, "project_label", "contextual_review", term)

    for term in rules["institution_terms"]:
        if contains_term(text, term):
            add_flag(flags, seen, "institution", "contextual_review", term)

    for term in rules["known_person_terms"]:
        if contains_term(text, term):
            add_flag(flags, seen, "third_party_name", "sensitive_anonymize", term)

    escalation = any(contains_term(text, term) for term in rules["third_party_escalation_terms"])
    for term in rules["role_terms"]:
        if contains_term(text, term):
            if escalation:
                add_flag(flags, seen, "third_party_sensitive", "sensitive_anonymize", term)
            else:
                add_flag(flags, seen, "role_reference", "contextual_review", term)

    for term in rules["health_terms"]:
        if contains_term(text, term):
            category = "bodily_condition" if term.lower() in {"fisic", "corpo", "corporeo", "condizione fisica", "ph interno"} else "health"
            add_flag(flags, seen, category, "block_internal_only", term)

    for term in rules["personal_logistics_terms"]:
        if contains_term(text, term):
            severity = "sensitive_anonymize" if term.lower() in {"viaggio", "trasferta", "concerto", "partenza", "arrivo"} else "contextual_review"
            add_flag(flags, seen, "personal_logistics", severity, term)

    client_context = any(contains_term(text, term) for term in rules["client_escalation_terms"]) or "cliente del progetto" in lowered
    for term in rules["client_sensitive_terms"]:
        if contains_term(text, term) and client_context:
            add_flag(flags, seen, "client_sensitive", "block_internal_only", term)

    for pattern in rules["calendar_regexes"]:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            add_flag(flags, seen, "calendar_detail", "sensitive_anonymize", match.group(0))

    for term in rules["calendar_terms"]:
        if contains_term(text, term):
            severity = "sensitive_anonymize" if term.lower() in {"partenza", "arrivo", "cancelli", "concerto", "trasferta", "viaggio", "volo", "treno"} else "contextual_review"
            add_flag(flags, seen, "calendar_detail", severity, term)

    return flags


def apply_metadata_privacy_flags(entry: dict[str, Any], flags: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = {(flag["category"], flag["severity"], flag["phrase"].lower()) for flag in flags}
    metadata = entry.get("metadata", {})
    privacy = metadata.get("privacy", {})
    if isinstance(privacy, dict):
        if privacy.get("contains_health_data") is True:
            add_flag(flags, seen, "health", "block_internal_only", "privacy.contains_health_data")
        if privacy.get("contains_personal_data") is True:
            add_flag(flags, seen, "personal_logistics", "contextual_review", "privacy.contains_personal_data")
        if privacy.get("contains_calendar_data") is True:
            add_flag(flags, seen, "calendar_detail", "sensitive_anonymize", "privacy.contains_calendar_data")
        if privacy.get("contains_third_party_names") is True:
            add_flag(flags, seen, "third_party_name", "sensitive_anonymize", "privacy.contains_third_party_names")
    calendar_action = metadata.get("calendar_action", {})
    if isinstance(calendar_action, dict) and calendar_action.get("has_calendar_actions") is True:
        add_flag(flags, seen, "calendar_detail", "sensitive_anonymize", "calendar_action.has_calendar_actions")
    return flags


def source_text_for(entry: dict[str, Any]) -> str:
    chunks = [str(entry.get("summary", ""))]
    for lines in entry.get("sections", {}).values():
        chunks.extend(str(line) for line in lines)
    return "\n".join(chunks)


def export_text_for(record: dict[str, Any]) -> str:
    chunks = [
        str(record.get("summary", "")),
        " ".join(str(project) for project in record.get("projects", [])),
    ]
    for lines in record.get("sections", {}).values():
        chunks.extend(str(line) for line in lines)
    return "\n".join(chunks)


def source_privacy_flags(entry: dict[str, Any]) -> list[dict[str, str]]:
    return apply_metadata_privacy_flags(entry, detect_privacy_flags(source_text_for(entry)))


def export_privacy_flags(entry: dict[str, Any], record: dict[str, Any]) -> list[dict[str, str]]:
    flags = detect_privacy_flags(export_text_for(record))
    if entry["schema_version"] == 2:
        flags = apply_metadata_privacy_flags(entry, flags)
    return flags


def flag_categories(flags: list[dict[str, str]], include_safe: bool = False) -> list[str]:
    categories = {
        flag["category"]
        for flag in flags
        if include_safe or flag["severity"] != "safe_methodological"
    }
    return sorted(categories)


def is_privacy_flag(flag: dict[str, str]) -> bool:
    category = flag["category"]
    severity = flag["severity"]
    if category in ALWAYS_PRIVACY_CATEGORIES:
        return True
    if category == "third_party_name":
        return True
    if category in {"calendar_detail", "personal_logistics", "institution"}:
        return severity in {"sensitive_anonymize", "block_internal_only"}
    return severity == "block_internal_only"


def is_context_marker(flag: dict[str, str]) -> bool:
    category = flag["category"]
    severity = flag["severity"]
    if category == "safe_methodological":
        return False
    if is_privacy_flag(flag):
        return False
    if category in CONTEXT_MARKER_CATEGORIES:
        return True
    if category in {"calendar_detail", "personal_logistics"} and severity == "contextual_review":
        return True
    return severity == "contextual_review"


def unique_flag_labels(flags: list[dict[str, str]], predicate: Any) -> list[str]:
    labels = {
        flag["category"]
        for flag in flags
        if predicate(flag)
    }
    return sorted(labels)


def privacy_flag_labels(flags: list[dict[str, str]]) -> list[str]:
    return unique_flag_labels(flags, is_privacy_flag)


def context_marker_labels(flags: list[dict[str, str]]) -> list[str]:
    return unique_flag_labels(flags, is_context_marker)


def safe_methodological_labels(flags: list[dict[str, str]]) -> list[str]:
    return sorted(
        {
            flag["phrase"]
            for flag in flags
            if flag["category"] == "safe_methodological"
        }
    )


def max_severity(flags: list[dict[str, str]]) -> str:
    if not flags:
        return "safe_methodological"
    return max((flag["severity"] for flag in flags), key=lambda severity: SEVERITY_ORDER.get(severity, 0))


def recommendation_from_export_flags(
    flags: list[dict[str, str]],
    schema_version: int,
    has_research_content: bool = True,
) -> tuple[str, str]:
    privacy_flags = [flag for flag in flags if is_privacy_flag(flag)]
    severity = max_severity(privacy_flags)

    if not has_research_content:
        return "internal_only", "exclude_from_research_export"
    if not privacy_flags:
        if schema_version == 1:
            return "needs_review", "manual_review"
        return "safe", "keep"
    if severity == "block_internal_only":
        return "internal_only", "internal_only"
    if severity == "sensitive_anonymize":
        return "anonymize_before_use", "anonymize"
    return "needs_review", "manual_review"


def anonymization_suggestions(flags: list[dict[str, str]]) -> dict[str, str]:
    rules = load_privacy_rules()
    mapping = rules.get("anonymization_map", {})
    suggestions: dict[str, str] = {}
    for flag in flags:
        phrase = flag["phrase"]
        for source, target in mapping.items():
            if phrase.lower() == source.lower():
                suggestions[source] = target
    return suggestions


def ignored_methodological_terms(text: str) -> list[str]:
    rules = load_privacy_rules()
    return sorted(
        {
            term
            for term in rules["safe_methodological_terms"]
            if contains_term(text, term)
        }
    )


def entry_schema_version(metadata: dict[str, Any]) -> int:
    raw = metadata.get("schema_version")
    if raw in (None, ""):
        return 1
    if raw == 2 or raw == "2":
        return 2
    raise ValueError(f"Unsupported schema_version: {raw}")


def canonical_paths(vault_root: Path) -> list[Path]:
    capture_dir = vault_root / "00_OPERA_Capture"
    if not capture_dir.exists():
        raise FileNotFoundError(f"Capture archive not found: {capture_dir}")
    return sorted(capture_dir.glob("OPERA-*.md"))


def validate_common(path: Path, metadata: dict[str, Any], errors: list[str]) -> None:
    for field in ("id", "date", "type", "status", "source"):
        if not metadata.get(field):
            errors.append(f"{path.name}: missing required field '{field}'")
    entry_id = str(metadata.get("id", ""))
    if entry_id and not re.fullmatch(r"OPERA-\d{4}-\d{2}-\d{2}-\d{3}", entry_id):
        errors.append(f"{path.name}: id is not canonical OPERA format")


def validate_v1(path: Path, sections: dict[str, list[str]], warnings: list[str]) -> None:
    missing = [name for name in V1_REQUIRED_SECTIONS if not sections.get(name)]
    if missing:
        warnings.append(f"{path.name}: v1 missing or empty sections: {', '.join(missing)}")


def validate_v2(
    path: Path,
    metadata: dict[str, Any],
    sections: dict[str, list[str]],
    warnings: list[str],
    errors: list[str],
) -> None:
    for field in (
        "projects",
        "research_relevance",
        "export_profile",
        "privacy",
        "calendar_action",
        "legacy",
    ):
        if field not in metadata:
            errors.append(f"{path.name}: v2 missing required field '{field}'")

    if metadata.get("research_relevance") not in {"none", "low", "medium", "high"}:
        errors.append(f"{path.name}: invalid research_relevance")

    missing = [name for name in V2_REQUIRED_SECTIONS if not sections.get(name)]
    if missing:
        errors.append(f"{path.name}: v2 missing or empty sections: {', '.join(missing)}")

    privacy = metadata.get("privacy")
    if isinstance(privacy, dict):
        if privacy.get("research_export_default") not in {"include", "filtered", "exclude"}:
            errors.append(f"{path.name}: invalid privacy.research_export_default")
    else:
        errors.append(f"{path.name}: privacy must be a map")

    export_profile = metadata.get("export_profile")
    if not isinstance(export_profile, dict):
        errors.append(f"{path.name}: export_profile must be a map")

    if not sections.get("Personal/contextual logistics"):
        warnings.append(f"{path.name}: v2 has no contextual logistics content")


def build_entry(path: Path, vault_root: Path, warnings: list[str], errors: list[str]) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8-sig")
        raw_frontmatter, body = split_frontmatter(text, path)
        metadata = parse_frontmatter(raw_frontmatter)
        sections = parse_sections(body)
        schema_version = entry_schema_version(metadata)
        validate_common(path, metadata, errors)
        if schema_version == 1:
            validate_v1(path, sections, warnings)
        elif schema_version == 2:
            validate_v2(path, metadata, sections, warnings, errors)
    except Exception as exc:
        errors.append(f"{path.name}: {exc}")
        return None

    summary = ""
    if schema_version == 1:
        summary = first_meaningful_line(sections.get("Research state", []))
    else:
        summary = first_meaningful_line(sections.get("Research-relevant content", []))

    return {
        "id": metadata.get("id", ""),
        "date": metadata.get("date", ""),
        "schema_version": schema_version,
        "type": metadata.get("type", ""),
        "status": metadata.get("status", ""),
        "path": path.relative_to(vault_root).as_posix(),
        "metadata": metadata,
        "summary": summary,
        "sections": sections,
    }


def projects_for(entry: dict[str, Any]) -> list[str]:
    projects = entry["metadata"].get("projects", [])
    if isinstance(projects, list):
        return [str(item) for item in projects if item]
    if isinstance(projects, str):
        return [projects]
    return []


def research_relevance_for(entry: dict[str, Any]) -> str:
    relevance = entry["metadata"].get("research_relevance")
    if relevance:
        return str(relevance)
    if entry["schema_version"] == 1:
        return "medium" if entry["sections"].get("Research state") else "low"
    return "none"


def include_in_research(entry: dict[str, Any]) -> bool:
    metadata = entry["metadata"]
    if entry["schema_version"] == 2:
        export_profile = metadata.get("export_profile", {})
        privacy = metadata.get("privacy", {})
        if isinstance(export_profile, dict) and export_profile.get("research") is False:
            return False
        if isinstance(privacy, dict) and privacy.get("research_export_default") == "exclude":
            return False
        return research_relevance_for(entry) != "none"
    return True


def internal_record(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry["id"],
        "date": entry["date"],
        "schema_version": entry["schema_version"],
        "profile": "internal",
        "type": entry["type"],
        "status": entry["status"],
        "path": entry["path"],
        "metadata": entry["metadata"],
        "summary": entry["summary"],
        "sections": entry["sections"],
    }


def research_record(entry: dict[str, Any]) -> dict[str, Any]:
    if entry["schema_version"] == 1:
        record = {
            "id": entry["id"],
            "date": entry["date"],
            "schema_version": entry["schema_version"],
            "profile": "research",
            "type": entry["type"],
            "status": entry["status"],
            "projects": [],
            "research_relevance": research_relevance_for(entry),
            "summary": "V1 entry requires manual review before research-facing use.",
            "sections": {},
            "audit_scope": "export_content_audit",
        }
        source_flags = source_privacy_flags(entry)
        exported_flags = export_privacy_flags(entry, record)
        export_status, action = recommendation_from_export_flags(
            exported_flags,
            entry["schema_version"],
            has_research_content=True,
        )
        record["research_export_status"] = "needs_review" if export_status == "safe" else export_status
        record["recommended_action"] = "manual_review" if action == "keep" else action
        record["source_privacy_flags"] = privacy_flag_labels(source_flags)
        record["export_privacy_flags"] = privacy_flag_labels(exported_flags)
        record["source_context_markers"] = context_marker_labels(source_flags)
        record["export_context_markers"] = context_marker_labels(exported_flags)
        record["safe_methodological_terms_detected"] = safe_methodological_labels(source_flags + exported_flags)
        record["audit_notes"] = [
            "V1 entries are exported as review stubs because source sections are not privacy-separated."
        ]
        record["anonymization_suggestions"] = anonymization_suggestions(source_flags + exported_flags)
        return record

    section_map = RESEARCH_SECTION_MAP_V2
    filtered_sections: dict[str, list[str]] = {}
    for source_name, export_name in section_map.items():
        filtered_sections[export_name] = entry["sections"].get(source_name, [])

    record = {
        "id": entry["id"],
        "date": entry["date"],
        "schema_version": entry["schema_version"],
        "profile": "research",
        "type": entry["type"],
        "status": entry["status"],
        "projects": projects_for(entry),
        "research_relevance": research_relevance_for(entry),
        "summary": entry["summary"],
        "sections": filtered_sections,
        "audit_scope": "export_content_audit",
    }
    source_flags = source_privacy_flags(entry)
    exported_flags = export_privacy_flags(entry, record)
    has_research_content = bool(record["summary"] or any(record["sections"].values()))
    export_status, action = recommendation_from_export_flags(
        exported_flags,
        entry["schema_version"],
        has_research_content=has_research_content,
    )
    record["research_export_status"] = export_status
    record["recommended_action"] = action
    record["source_privacy_flags"] = privacy_flag_labels(source_flags)
    record["export_privacy_flags"] = privacy_flag_labels(exported_flags)
    record["source_context_markers"] = context_marker_labels(source_flags)
    record["export_context_markers"] = context_marker_labels(exported_flags)
    record["safe_methodological_terms_detected"] = safe_methodological_labels(source_flags + exported_flags)
    record["audit_notes"] = []
    metadata = entry["metadata"]
    privacy = metadata.get("privacy", {})
    if isinstance(privacy, dict) and privacy.get("research_export_default") == "filtered" and export_status == "safe":
        record["research_export_status"] = "needs_review"
        record["recommended_action"] = "manual_review"
        record["audit_notes"].append("Entry is explicitly marked for filtered research export.")
    record["anonymization_suggestions"] = anonymization_suggestions(source_flags + exported_flags)
    return record


def safe_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


def safe_write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, delete=False) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flattened = dict(row)
            if "projects" in flattened and isinstance(flattened["projects"], list):
                flattened["projects"] = ";".join(flattened["projects"])
            for flag_field in (
                "source_privacy_flags",
                "export_privacy_flags",
                "source_context_markers",
                "export_context_markers",
                "safe_methodological_terms_detected",
            ):
                if flag_field in flattened and isinstance(flattened[flag_field], list):
                    flattened[flag_field] = ";".join(flattened[flag_field])
            if "metadata" in flattened:
                flattened.pop("metadata")
            if "sections" in flattened:
                flattened.pop("sections")
            writer.writerow({field: flattened.get(field, "") for field in fieldnames})
        temp_name = handle.name
    os.replace(temp_name, path)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    content = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    safe_write_text(path, content + ("\n" if content else ""))


def backup_existing_outputs(paths: list[Path]) -> list[Path]:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return []

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = existing[0].parent / f"_backup_before_research_export_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backups: list[Path] = []
    for path in existing:
        backup_path = backup_dir / path.name
        backup_path.write_bytes(path.read_bytes())
        backups.append(backup_path)
    return backups


def audit_phrase_lines(entry: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    texts: list[tuple[str, str]] = [("summary", str(entry.get("summary", "")))]
    for section_name, lines in entry.get("sections", {}).items():
        for line in lines:
            texts.append((section_name, clean_phrase(str(line))))

    for section_name, text in texts:
        for flag in detect_privacy_flags(text):
            rows.append(
                {
                    "section": section_name,
                    "category": flag["category"],
                    "severity": flag["severity"],
                    "phrase": flag["phrase"],
                    "text": text,
                }
            )
    return rows


def audit_record_phrase_lines(record: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    texts: list[tuple[str, str]] = [
        ("summary", str(record.get("summary", ""))),
        ("projects", " ".join(str(project) for project in record.get("projects", []))),
    ]
    for section_name, lines in record.get("sections", {}).items():
        for line in lines:
            texts.append((section_name, clean_phrase(str(line))))

    for section_name, text in texts:
        for flag in detect_privacy_flags(text):
            rows.append(
                {
                    "section": section_name,
                    "category": flag["category"],
                    "severity": flag["severity"],
                    "phrase": flag["phrase"],
                    "text": text,
                }
            )
    return rows


def summarize_hits(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["section"], row["category"], row["severity"], row["phrase"])
        if key not in grouped:
            grouped[key] = {
                "section": row["section"],
                "category": row["category"],
                "severity": row["severity"],
                "phrase": row["phrase"],
                "count": 0,
            }
        grouped[key]["count"] += 1
    return sorted(
        grouped.values(),
        key=lambda item: (
            item["section"],
            SEVERITY_ORDER.get(item["severity"], 0),
            item["category"],
            item["phrase"].lower(),
        ),
    )


def format_hit(hit: dict[str, Any]) -> str:
    count = f" - {hit['count']} occurrence" + ("" if hit["count"] == 1 else "s")
    return f"* `{hit['phrase']}` - `{hit['category']}` - `{hit['severity']}` - `{hit['section']}`{count}"


def build_research_privacy_audit(
    paths: list[Path],
    entries: list[dict[str, Any]],
    exported_rows: list[dict[str, Any]],
    excluded_entries: list[dict[str, Any]],
) -> str:
    exported_by_id = {row["id"]: row for row in exported_rows}
    v1_review_count = sum(1 for row in exported_rows if row["schema_version"] == 1 and row["research_export_status"] == "needs_review")
    v2_count = sum(1 for entry in entries if entry["schema_version"] == 2)
    entries_with_export_privacy = [
        row for row in exported_rows if row.get("export_privacy_flags")
    ]
    entries_with_source_only_privacy = [
        row
        for row in exported_rows
        if row.get("source_privacy_flags") and not row.get("export_privacy_flags")
    ]
    entries_with_only_context = [
        row
        for row in exported_rows
        if not row.get("source_privacy_flags")
        and not row.get("export_privacy_flags")
        and (row.get("source_context_markers") or row.get("export_context_markers"))
    ]
    ignored_terms: Counter[str] = Counter()
    anonymization_map: dict[str, str] = {}

    for row in exported_rows:
        for term in ignored_methodological_terms(export_text_for(row)):
            ignored_terms[term] += 1
        anonymization_map.update(row.get("anonymization_suggestions", {}))

    for entry in entries:
        source_flags = source_privacy_flags(entry)
        for term in ignored_methodological_terms(source_text_for(entry)):
            ignored_terms[term] += 1
        anonymization_map.update(anonymization_suggestions(source_flags))

    lines = [
        "# OPERA Research Privacy Audit",
        "",
        "## Summary",
        "",
        f"* Audit date: {date.today().isoformat()}",
        f"* Total entries: {len(paths)}",
        f"* Exported entries: {len(exported_rows)}",
        f"* v1 entries requiring review: {v1_review_count}",
        f"* v2 entries: {v2_count}",
        f"* Entries with exported privacy flags: {len(entries_with_export_privacy)}",
        f"* Entries with source-only privacy flags: {len(entries_with_source_only_privacy)}",
        f"* Entries with only context markers: {len(entries_with_only_context)}",
        f"* Entries excluded: {len(excluded_entries)}",
        "",
        "## Exported content audit",
        "",
    ]
    lines.append("This section describes only content actually emitted in the research export.")
    lines.append("")
    for row in exported_rows:
        export_privacy = ", ".join(row.get("export_privacy_flags", [])) or "none"
        export_context = ", ".join(row.get("export_context_markers", [])) or "none"
        lines.extend(
            [
                f"### {row['id']} ({row['date']})",
                "",
                f"* Status: {row.get('research_export_status', 'unknown')}",
                f"* Recommended action: {row.get('recommended_action', 'unknown')}",
                f"* Export privacy flags: {export_privacy}",
                f"* Export context markers: {export_context}",
                "",
            ]
        )

    lines.extend(["", "## Source content audit", ""])
    lines.append("This section audits full original entries. Source-only flags do not automatically change exported status.")
    lines.append("")
    for entry in entries:
        rows = audit_phrase_lines(entry)
        source_flags = source_privacy_flags(entry)
        source_privacy = ", ".join(privacy_flag_labels(source_flags)) or "none"
        source_context = ", ".join(context_marker_labels(source_flags)) or "none"
        source_safe = ", ".join(safe_methodological_labels(source_flags)) or "none"
        export_status = exported_by_id.get(entry["id"], {}).get("research_export_status", "excluded")
        recommended = exported_by_id.get(entry["id"], {}).get("recommended_action", "exclude_from_research_export")
        lines.extend(
            [
                f"### {entry['id']} ({entry['date']})",
                "",
                f"* Schema version: {entry['schema_version']}",
                f"* Research export status: {export_status}",
                f"* Recommended action: {recommended}",
                f"* Source privacy flags: {source_privacy}",
                f"* Source context markers: {source_context}",
                f"* Safe methodological terms detected: {source_safe}",
                "",
            ]
        )
        summarized = summarize_hits(rows)
        if summarized:
            for hit in summarized:
                lines.append(format_hit(hit))
        else:
            lines.append("* No source keyword phrases found.")
        lines.append("")

    lines.extend(["", "## False positive control", ""])
    if ignored_terms:
        for term, count in sorted(ignored_terms.items()):
            lines.append(f"* `{term}` downgraded to safe methodological term: {count}")
    else:
        lines.append("* No safe methodological terms were detected.")

    lines.extend(["", "## Anonymization suggestions", ""])
    if anonymization_map:
        for source, target in sorted(anonymization_map.items()):
            lines.append(f"* `{source}` -> `{target}`")
    else:
        lines.append("* None")

    lines.extend(
        [
            "",
            "## Remaining risks",
            "",
            "* Keyword-based detection cannot fully understand narrative context.",
            "* V1 entries remain manual-review stubs until explicitly approved or rewritten as v2.",
            "* Add new real names or institution aliases to `privacy_rules.local.json` as they appear.",
            "",
        ]
    )
    return "\n".join(lines)


def build_validation_report(
    vault_root: Path,
    paths: list[Path],
    entries: list[dict[str, Any]],
    warnings: list[str],
    errors: list[str],
) -> str:
    ids = [entry["id"] for entry in entries]
    duplicates = sorted(entry_id for entry_id, count in Counter(ids).items() if entry_id and count > 1)
    if duplicates:
        errors.append(f"Duplicate IDs: {', '.join(duplicates)}")

    legacy_count = len(list((vault_root / "00_OPERA_Capture").rglob("*r-*.md")))
    lines = [
        "# OPERA v2 Draft Validation Report",
        "",
        f"* Validation date: {date.today().isoformat()}",
        f"* Vault root: {vault_root}",
        f"* Canonical OPERA entries scanned: {len(paths)}",
        f"* Entries parsed: {len(entries)}",
        f"* Legacy R-style files detected but not scanned: {legacy_count}",
        f"* v1 entries: {sum(1 for entry in entries if entry['schema_version'] == 1)}",
        f"* v2 entries: {sum(1 for entry in entries if entry['schema_version'] == 2)}",
        f"* Warnings: {len(warnings)}",
        f"* Errors: {len(errors)}",
        "",
        "## IDs",
        "",
    ]
    lines.extend(f"* {entry_id}" for entry_id in sorted(ids))
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"* {warning}" for warning in warnings) if warnings else lines.append("* None")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"* {error}" for error in errors) if errors else lines.append("* None")
    lines.extend(["", "## Status", "", "* OK" if not errors else "* ERROR", ""])
    return "\n".join(lines)


def load_entries(vault_root: Path) -> tuple[list[Path], list[dict[str, Any]], list[str], list[str]]:
    paths = canonical_paths(vault_root)
    warnings: list[str] = []
    errors: list[str] = []
    entries: list[dict[str, Any]] = []
    for path in paths:
        entry = build_entry(path, vault_root, warnings, errors)
        if entry is not None:
            entries.append(entry)
    entries.sort(key=lambda entry: (str(entry["date"]), str(entry["id"])))
    return paths, entries, warnings, errors


def export_entries(vault_root: Path, profile: str, entries: list[dict[str, Any]]) -> list[Path]:
    dataset_root = vault_root / "20_OPERA_Dataset" / profile
    written: list[Path] = []

    if profile == "internal":
        rows = [internal_record(entry) for entry in entries]
        jsonl_path = dataset_root / "opera_entries.internal.jsonl"
        csv_path = dataset_root / "opera_entries.internal.csv"
        write_jsonl(jsonl_path, rows)
        safe_write_csv(csv_path, rows, INTERNAL_CSV_FIELDS)
        written.extend([jsonl_path, csv_path])
        return written

    if profile == "research":
        rows = [research_record(entry) for entry in entries if include_in_research(entry)]
        excluded = [entry for entry in entries if not include_in_research(entry)]
        jsonl_path = dataset_root / "opera_entries.research.jsonl"
        csv_path = dataset_root / "opera_entries.research.csv"
        audit_path = dataset_root / "opera_privacy_audit.research.md"
        report_path = dataset_root / "opera_validation.research.md"
        backup_existing_outputs([jsonl_path, csv_path, audit_path, report_path])
        write_jsonl(jsonl_path, rows)
        safe_write_csv(csv_path, rows, RESEARCH_CSV_FIELDS)
        audit = build_research_privacy_audit(canonical_paths(vault_root), entries, rows, excluded)
        safe_write_text(audit_path, audit)
        written.extend([jsonl_path, csv_path, audit_path])
        return written

    raise ValueError(f"Unsupported profile: {profile}")


def resolve_vault_root(args: argparse.Namespace) -> Path:
    root = args.vault_root or os.environ.get("OPERA_VAULT_ROOT")
    if not root:
        raise SystemExit("Provide --vault-root or set OPERA_VAULT_ROOT.")
    return Path(root).expanduser().resolve()


def cmd_validate(args: argparse.Namespace) -> int:
    vault_root = resolve_vault_root(args)
    paths, entries, warnings, errors = load_entries(vault_root)
    report = build_validation_report(vault_root, paths, entries, warnings, errors)
    print(report)
    return 1 if errors else 0


def cmd_parse(args: argparse.Namespace) -> int:
    vault_root = resolve_vault_root(args)
    paths, entries, warnings, errors = load_entries(vault_root)
    report = build_validation_report(vault_root, paths, entries, warnings, errors)
    if errors:
        print(report)
        return 1

    written = export_entries(vault_root, args.profile, entries)
    report_path = vault_root / "20_OPERA_Dataset" / args.profile / f"opera_validation.{args.profile}.md"
    if args.profile != "research":
        backup_existing_outputs([report_path])
    safe_write_text(report_path, report)
    written.append(report_path)

    print(report)
    print("Files written:")
    for path in written:
        print(f"* {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Draft OPERA v2 parser")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate canonical OPERA entries without writing exports")
    validate.add_argument("--vault-root", help="External Obsidian vault root")
    validate.set_defaults(func=cmd_validate)

    parse = subparsers.add_parser("parse", help="Validate and export OPERA datasets")
    parse.add_argument("--vault-root", help="External Obsidian vault root")
    parse.add_argument("--profile", choices=("internal", "research"), required=True)
    parse.set_defaults(func=cmd_parse)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
