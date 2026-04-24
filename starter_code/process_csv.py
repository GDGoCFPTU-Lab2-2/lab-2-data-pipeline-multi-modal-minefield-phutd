import pandas as pd
import re
import os
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def _parse_price(val):
    if pd.isna(val):
        return None
    s = str(val)
    # Remove currency symbols and commas
    s_clean = re.sub(r"[,$€£]", "", s)
    # Try to extract first numeric token
    m = re.search(r"-?\d+[\d,.]*", s_clean)
    if m:
        num = m.group(0).replace(',', '')
        try:
            return float(num)
        except ValueError:
            return None
    return None

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    # If there's an 'id' column use it to drop duplicate ids
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'])

    # Clean price
    if 'price' in df.columns:
        df['price_clean'] = df['price'].apply(_parse_price)
    else:
        df['price_clean'] = None

    # Normalize dates
    if 'date_of_sale' in df.columns:
        df['date_iso'] = pd.to_datetime(df['date_of_sale'], errors='coerce').dt.strftime('%Y-%m-%d')
    else:
        df['date_iso'] = None

    results = []
    for idx, row in df.iterrows():
        raw_id = row.get('id', f'sales_row_{idx}')
        doc_id = f"csv-{raw_id}"
        content = {
            k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()
        }
        results.append({
            "document_id": doc_id,
            "title": None,
            "content": str(content),
            "source_type": "CSV",
            "author": "Unknown",
            "timestamp": datetime.now().isoformat(),
            "source_metadata": {"path": file_path, "row_index": int(idx)},
        })

    return results

