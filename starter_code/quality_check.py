# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # Reject documents with too-short content
    content = document_dict.get('content') or ''
    if isinstance(content, (list, dict)):
        content_str = str(content)
    else:
        content_str = content

    if len(content_str.strip()) < 20:
        return False

    # Reject known toxic/error strings
    toxic_markers = [
        'Null pointer exception',
        'Traceback (most recent call last)',
        'ERROR',
        'FATAL',
    ]
    for t in toxic_markers:
        if t.lower() in content_str.lower():
            return False

    # Simple discrepancy detector example: look for conflicting percentage mentions
    import re
    percents = re.findall(r"(\d+)%", content_str)
    if len(set(percents)) > 1 and len(percents) >= 2:
        # conflicting percentage values found; flag as failure
        return False

    return True
