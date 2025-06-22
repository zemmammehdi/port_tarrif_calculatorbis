import json

def extract_vessel_info_from_query(query: str, model) -> dict:
    prompt = f"""
Extract structured fields from vessel description:

- gt, loa, stay_days, port
- is_self_propelled, is_research, is_pleasure, is_coaster
- number_of_operations
- requires_two_pilot_transits, requires_tow_in_out

Description:
{query}

Return valid JSON only. No markdown.
"""
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    vessel_info = json.loads(text)

    for field in ["gt", "loa", "stay_days"]:
        if field in vessel_info and isinstance(vessel_info[field], str):
            try:
                vessel_info[field] = float(vessel_info[field].replace(",", "").strip())
            except:
                pass

    return vessel_info
