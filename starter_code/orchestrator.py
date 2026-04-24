import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # ----------------------------------------------

    # 1. Process PDF (Gemini)
    doc_pdf = extract_pdf_data(pdf_path)
    if doc_pdf and run_quality_gate(doc_pdf):
        final_kb.append(doc_pdf)

    # 2. Process Transcript
    doc_trans = clean_transcript(trans_path)
    if doc_trans and run_quality_gate(doc_trans):
        final_kb.append(doc_trans)

    # 3. Process HTML Catalog
    docs_html = parse_html_catalog(html_path)
    for doc in docs_html:
        if run_quality_gate(doc):
            final_kb.append(doc)

    # 4. Process CSV Sales
    docs_csv = process_sales_csv(csv_path)
    for doc in docs_csv:
        if run_quality_gate(doc):
            final_kb.append(doc)

    # 5. Process Legacy Code
    doc_code = extract_logic_from_code(code_path)
    if doc_code and run_quality_gate(doc_code):
        final_kb.append(doc_code)

    # Validate all items against UnifiedDocument schema
    validated_kb = [UnifiedDocument(**doc).model_dump() for doc in final_kb]

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(validated_kb, f, ensure_ascii=False, indent=4)

    end_time = time.time()
    print("-" * 30)
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print(f"Total valid documents stored: {len(validated_kb)}")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
