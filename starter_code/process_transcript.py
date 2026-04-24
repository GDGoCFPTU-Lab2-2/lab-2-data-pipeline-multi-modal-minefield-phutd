import re
import os
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------

    # Remove common noise tokens
    text = re.sub(r"\[(?:Music|inaudible|Laughter|Applause)\]", "", text, flags=re.IGNORECASE)
    # Remove timestamps like [00:05:12] or 00:05:12
    text = re.sub(r"\[?\d{1,2}:\d{2}:\d{2}\]?", "", text)
    # Remove extra bracketed tags
    text = re.sub(r"\[[^\]]+\]", "", text)
    # Collapse multiple whitespace
    cleaned = re.sub(r"\s+", " ", text).strip()

    # Try to extract a short title from the first line
    title = None
    first_line = cleaned.split('\n', 1)[0].strip()
    if len(first_line) > 0 and len(first_line) < 120:
        title = first_line

    document_id = os.path.basename(file_path)

    # Detect a Vietnamese-written price like "năm trăm nghìn" -> 500000 (simple rule)
    detected_price = None
    if re.search(r"năm\s+trăm\s+nghìn", cleaned, flags=re.IGNORECASE):
        detected_price = 500000

    meta = {"path": file_path}
    if detected_price is not None:
        meta['detected_price_vnd'] = detected_price

    return {
        "document_id": document_id,
        "title": title,
        "content": cleaned,
        "source_type": "Video",
        "author": "Unknown",
        "timestamp": datetime.now().isoformat(),
        "source_metadata": meta,
    }

