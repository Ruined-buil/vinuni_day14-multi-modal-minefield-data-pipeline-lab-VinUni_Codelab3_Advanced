from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!

class UnifiedDocument(BaseModel):
    document_id: str
    content: str
    source_type: str # e.g., 'PDF', 'HTML', 'CSV', 'Transcript', 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[str] = None # Using string to avoid ISO format issues during serialization
    source_metadata: dict = Field(default_factory=dict)
