import os
import json

def extract_tariff_section(full_text: str, keyword: str, window: int = 6000) -> str:
    """Extracts a relevant section around the given keyword using fuzzy matching."""
    import re

    # Normalize
    cleaned_text = full_text.lower()

    # Fuzzy synonyms mapping
    synonyms = {
        "light_dues": ["light dues", "lightdues", "light due"],
        "port_dues": ["port dues", "port fees on vessels", "vessel port dues", "port fee"],
        "vts_dues": ["vts dues", "vessel traffic services", "vts charges"],
        "pilotage_dues": ["pilotage dues", "pilotage fee", "pilotage charges"],
        "towage_dues": ["towage dues", "towage charges"],
        "running_of_vessel_lines_dues": ["running of vessel lines dues", "mooring", "unmooring"],
    }

    # Search all possible variants
    patterns = synonyms.get(keyword, [keyword.replace("_", " ")])
    matches = []
    for pattern in patterns:
        idx = cleaned_text.find(pattern.lower())
        if idx != -1:
            matches.append(idx)

    if not matches:
        return full_text[:window]

    best_idx = matches[0]
    start = max(0, best_idx - 1000)
    return full_text[start:start + window]


def is_valid_tariff_json(data: dict, required_keys=None, context="") -> bool:
    required_keys = required_keys or ["tariff_name", "currency", "unit", "notes"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"⚠️ [{context}] Missing keys: {missing}")
        data["_status"] = "incomplete"
        data["_missing_keys"] = missing
        log_extraction_error(context, missing)
    if "charged_per_movement" not in data:
        data["charged_per_movement"] = False
    return len(missing) == 0

def log_extraction_error(context, missing_keys):
    with open("extraction_errors.log", "a", encoding="utf-8", errors="replace") as logf:
        logf.write(f"{context} → Missing keys: {missing_keys}\n")

def save_tariff(data, save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved: {full_path}")
