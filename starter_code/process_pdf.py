import os
from datetime import datetime

# Try to use PyPDF2 for local extraction if available. The student guide suggests Gemini,
# but offline we provide a reasonable fallback.
def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------

    text = None
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            pages = []
            for p in reader.pages:
                try:
                    pages.append(p.extract_text() or '')
                except Exception:
                    pages.append('')
            text = '\n'.join(pages).strip()
    except Exception:
        # PyPDF2 not available or failed; try a simple binary-read fallback
        try:
            with open(file_path, 'rb') as f:
                raw = f.read(4096)
                # try decode heuristically
                text = raw.decode('utf-8', errors='ignore')
        except Exception:
            text = None

    if not text:
        text = "[PDF content could not be extracted locally — Gemini or PyPDF2 required for full extraction]"

    # crude title: first non-empty line
    title = None
    for line in text.splitlines():
        s = line.strip()
        if s:
            title = s[:120]
            break

    return {
        "document_id": os.path.basename(file_path),
        "title": title,
        "content": text,
        "source_type": "PDF",
        "author": "Unknown",
        "timestamp": datetime.now().isoformat(),
        "source_metadata": {"path": file_path},
    }

