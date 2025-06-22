import os
import json

from gemini_client import model
from extractors.pdf_parser import extract_all_pdf_text
from extractors.tariff_parser import (
    extract_tariff_section,
    is_valid_tariff_json,
    save_tariff,
    log_extraction_error,
)
from utils.prompts import build_prompt_port_tariff, build_prompt_common_tariff
from agent.planner import run_tariff_agent

# === CONFIGURATION ===
ports = ["Durban", "Saldanha", "Richards Bay"]
port_tariffs = ["towage_dues", "pilotage_dues", "running_of_vessel_lines_dues"]
common_tariffs = ["light_dues", "port_dues", "vts_dues"]

# === EXTRACTION LOGIC ===
def extract_tariff(full_text, prompt, save_dir, filename, context=""):
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(text)
        parsed["source_text"] = full_text[:1000] + "..."
        if is_valid_tariff_json(parsed, context=context):
            save_tariff(parsed, save_dir, filename)
        else:
            save_tariff(parsed, save_dir, filename)
    except Exception as e:
        print(f"❌ Error for {context}: {e}")
        log_extraction_error(context, [str(e)])

def generate_port_tariff(full_text, port, tariff):
    section = extract_tariff_section(full_text, f"{port} {tariff}")
    prompt = build_prompt_port_tariff(section, port, tariff)
    path = os.path.join("tariffs", port.lower().replace(" ", "_"))
    filename = f"{tariff}.json"
    extract_tariff(full_text, prompt, path, filename, context=f"{port}/{tariff}")

def generate_common_tariff(full_text, tariff):
    section = extract_tariff_section(full_text, tariff)
    prompt = build_prompt_common_tariff(section, tariff)
    path = os.path.join("tariffs", "common")
    filename = f"{tariff}.json"
    extract_tariff(full_text, prompt, path, filename, context=f"common/{tariff}")

# === MAIN EXECUTION ===
def main():
    print("📄 Extracting full PDF text...")
    full_text = extract_all_pdf_text("Port Tariff.pdf")

    print("\n🏙️ Generating port-based tariffs...")
    for port in ports:
        for tariff in port_tariffs:
            print(f"🔁 {port} → {tariff}")
            generate_port_tariff(full_text, port, tariff)

    print("\n🌍 Generating global/common tariffs...")
    for tariff in common_tariffs:
        print(f"🔁 common → {tariff}")
        generate_common_tariff(full_text, tariff)

    print("\n✅ All extraction complete.")

    # Run intelligent calculation agent
    print("\n🧠 Parsing and calculating tariffs from user input...")
    user_input = """
    Calculate the different tariffs payable by the following vessel berthing at the port of Durban:

    Vessel Name: SUDESTADA
    GT: 51,300
    LOA: 229.2m
    Stay: 3.39 days
    Cargo: 40,000 MT
    Operations: 2
    Activity: Exporting Iron Ore
    """
    tariffs = [
        "light_dues", "port_dues",
        "towage_dues", "vts_dues",
        "pilotage_dues", "running_of_vessel_lines_dues"
    ]
    run_tariff_agent(user_input, tariffs_requested=tariffs)

if __name__ == "__main__":
    main()
