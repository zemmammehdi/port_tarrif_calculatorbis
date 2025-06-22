def build_prompt_port_tariff(section_text, port, tariff):
    return f"""
You are a maritime tariff rule extractor.

Extract a JSON rule for:
- Tariff: {tariff}
- Port: {port}

Return:
- tariff_name, port, base_rate or tonnage_bands or fixed_fee, unit, currency, notes, calculation_method, charged_per_movement

--- TEXT ---
{section_text}
--- END ---

Return only valid JSON. No markdown. If info missing, put "not found" in 'notes'.
"""

def build_prompt_common_tariff(section_text, tariff):
    return f"""
You are a port tariff rule extractor.

Extract the COMMON rule for tariff: {tariff}

Return:
- tariff_name, base_rate, unit, currency, validity_conditions, exceptions, alternate_modes, notes, calculation_method, charged_per_movement

--- TEXT ---
{section_text}
--- END ---

Return valid JSON only. No markdown.
"""