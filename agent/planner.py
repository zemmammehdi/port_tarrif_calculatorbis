import json
from agent.parser import extract_vessel_info_from_query
from agent.calculator import load_tariff_rule, apply_tariff_rule
from gemini_client import model

def run_tariff_agent(user_query, tariffs_requested):
    print("🔎 Parsing and calculating tariffs from user input...")
    vessel_info = extract_vessel_info_from_query(user_query, model=model)

    print(f"📦 Extracted vessel info:\n{json.dumps(vessel_info, indent=2)}\n")
    results = []

    for tariff in tariffs_requested:
        try:
            rule = load_tariff_rule(tariff, vessel_info.get("port", "unknown"))
            result = apply_tariff_rule(rule, vessel_info, model=model)
            results.append(result)
        except Exception as e:
            results.append({
                "tariff_name": tariff,
                "calculated_amount": None,
                "explanation": f"❌ {str(e)}"
            })

    print("📊 Tariff Results:")
    for r in results:
        print(f"\n🧾 {r['tariff_name'].upper()}")
        print(f"💰 Amount: {r.get('calculated_amount', 'N/A')}")
        print(f"🧠 Explanation: {r.get('explanation', '')}")

    return results
