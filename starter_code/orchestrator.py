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

def _append_if_valid(final_kb, doc):
    try:
        if doc is None:
            return
        # If processor returned a list, iterate
        if isinstance(doc, list):
            for d in doc:
                if run_quality_gate(d):
                    # Validate with Pydantic
                    ud = UnifiedDocument(**d)
                    final_kb.append(ud.to_dict())
        else:
            if run_quality_gate(doc):
                ud = UnifiedDocument(**doc)
                final_kb.append(ud.to_dict())
    except Exception as e:
        print(f"Warning: dropped document due to validation error: {e}")


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

    # Process PDF
    pdf_doc = extract_pdf_data(pdf_path)
    _append_if_valid(final_kb, pdf_doc)

    # Process Transcript
    trans_doc = clean_transcript(trans_path)
    _append_if_valid(final_kb, trans_doc)

    # Process HTML catalog
    html_docs = parse_html_catalog(html_path)
    _append_if_valid(final_kb, html_docs)

    # Process CSV
    csv_docs = process_sales_csv(csv_path)
    _append_if_valid(final_kb, csv_docs)

    # Process legacy code
    code_doc = extract_logic_from_code(code_path)
    _append_if_valid(final_kb, code_doc)

    # Save results
    try:
        with open(output_path, 'w', encoding='utf-8') as out_f:
            json.dump(final_kb, out_f, ensure_ascii=False, indent=2, default=str)
        print(f"Saved processed knowledge base to {output_path}")
    except Exception as e:
        print(f"Failed to save output: {e}")

    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print(f"Total valid documents stored: {len(final_kb)}")


if __name__ == "__main__":
    main()
