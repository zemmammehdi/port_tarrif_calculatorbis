import os
import json

def load_tariff_rule(tariff_name: str, port: str) -> dict:
    base_path = "tariffs"
    folder = "common" if tariff_name in ["light_dues", "port_dues", "vts_dues"] else port.lower().replace(" ", "_")
    path = os.path.join(base_path, folder, f"{tariff_name}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"No rule found for {tariff_name} in {port}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_tariff_rule(tariff_rule: dict, vessel_info: dict, model) -> dict:
    prompt = f"""
Apply the following rule to this vessel and return:
- tariff_name
- calculated_amount (in ZAR)
- brief explanation

TARIFF:
{json.dumps(tariff_rule, indent=2)}

VESSEL:
{json.dumps(vessel_info, indent=2)}

Return valid JSON only. No markdown.
"""
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)
