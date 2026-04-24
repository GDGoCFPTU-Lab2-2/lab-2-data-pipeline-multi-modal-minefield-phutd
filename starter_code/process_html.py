from bs4 import BeautifulSoup
import os
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------

    table = soup.find('table', id='main-catalog')
    if table is None:
        table = soup.find('table')

    results = []
    if table:
        # Extract headers
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if not cells or all(c == '' for c in cells):
                continue
            # If headers present, map them
            if headers and len(cells) == len(headers):
                record = dict(zip(headers, cells))
            else:
                record = {f'col_{i}': v for i, v in enumerate(cells)}

            doc_id = record.get('id') or record.get('ID') or os.path.basename(file_path) + f"_{len(results)}"
            content = str(record)
            results.append({
                "document_id": str(doc_id),
                "title": record.get('name') or record.get('title'),
                "content": content,
                "source_type": "HTML",
                "author": "Unknown",
                "timestamp": datetime.now().isoformat(),
                "source_metadata": {"path": file_path},
            })

    return results

