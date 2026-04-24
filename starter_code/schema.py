from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    # v1 UnifiedDocument schema
    document_id: str
    title: Optional[str] = None
    content: str
    source_type: str  # e.g., 'PDF', 'Video', 'HTML', 'CSV', 'Code', 'Transcript'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None

    # Source-specific metadata (file path, original record id, raw fields)
    source_metadata: Dict[str, Any] = Field(default_factory=dict)

    # Optional short summary extracted from source
    summary: Optional[str] = None

    # Helper: export as plain dict (Pydantic provides .dict(), keep for clarity)
    def to_dict(self) -> Dict[str, Any]:
        return self.dict()
