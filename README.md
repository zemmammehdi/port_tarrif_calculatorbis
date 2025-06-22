# 📄 South African Port Tariff Rule Extractor & Calculator

This project automates the extraction of tariff rules from the official South African port tariff document (2024–2025) and uses them to calculate dues based on a user's vessel query.

---

## 🧠 Approach

The solution is designed to be fully automated and agent-driven, based on the following pipeline:

### 1. PDF Parsing and Section Detection

To automate the processing of the official tariff document, we first parse the PDF using a document parser.  
The **most critical step** is accurately **segmenting the document by sections**, which allows us to isolate rules related to specific tariff types (light dues, port dues, towage dues, etc.).

### 2. Gemini-Based Rule Extraction

Once sections are detected and extracted, we use **Gemini LLM** to convert the unstructured text into structured **JSON rule files**, one for each port and each tariff type.  
This enables us to represent all tariffs programmatically, without hardcoding logic into the codebase.

### 3. User Input Parsing

A natural language query describing the vessel (e.g., size, draft, DWT, activity, port) is parsed using another Gemini model to extract structured parameters.

### 4. Intelligent Orchestration

A reasoning agent reads both:
- The structured user input  
- The extracted JSON rules

It then directly applies the correct formulas and logic from the rules to compute the tariffs.

---

## ▶️ How to Run

### ✅ Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Execute the pipeline

```bash
python main.py
```

This will:
1. Parse the tariff PDF and extract all relevant sections.
2. Generate JSON rule files using Gemini.
3. Accept a vessel input and parse its parameters.
4. Calculate all applicable tariffs using the extracted rules.


## 🔧 Tech Stack

- Python 3.10+  
- PyMuPDF / PDFPlumber (for PDF parsing)  
- Gemini (Google Generative AI)  
- JSON-based rule storage  
- Modular Python functions for tariff logic  

---

Let me know if you want to include an example output or a sample vessel input file.
