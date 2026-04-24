import ast
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------

    parsed = ast.parse(source_code)
    module_doc = ast.get_docstring(parsed)

    functions = []
    for node in ast.walk(parsed):
        if isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            functions.append({
                'name': node.name,
                'doc': func_doc,
            })

    # Find inline comments that look like business rules
    import re
    rules = re.findall(r"#\s*(Business Logic Rule[^\n]*)", source_code, flags=re.IGNORECASE)

    content = {
        'module_docstring': module_doc,
        'functions': functions,
        'business_rules': rules,
    }

    return {
        "document_id": os.path.basename(file_path),
        "title": None,
        "content": str(content),
        "source_type": "Code",
        "author": "Unknown",
        "timestamp": None,
        "source_metadata": {"path": file_path},
    }

