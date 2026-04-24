# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(doc):
    # doc can be a dictionary or a UnifiedDocument object
    content = doc.get('content', '') if isinstance(doc, dict) else doc.content
    
    # 1. Reject documents with 'content' length < 20 characters
    if len(content.strip()) < 20:
        print(f"Rejected doc {doc.get('document_id')}: Content too short.")
        return False
        
    # 2. Reject documents containing severe error strings
    error_keywords = ['null pointer exception', 'segmentation fault', 'database connection failed']
    content_lower = content.lower()
    for kw in error_keywords:
        if kw in content_lower:
            print(f"Rejected doc {doc.get('document_id')}: Contains critical error string '{kw}'.")
            return False
            
    # 3. Flag/Log toxic phrases or discrepancies
    toxic_warnings = ['rác vào, rác ra']
    for kw in toxic_warnings:
        if kw in content_lower:
            print(f"Warning: Doc {doc.get('document_id')} contains toxic-sounding phrase: '{kw}'.")
    # This is more of a logging/flagging step than a rejection step in some cases,
    # but we'll implement it as requested.
    if "tax says 8%" in content_lower and "code says 10%" in content_lower:
         print(f"Warning: Discrepancy found in {doc.get('document_id')}: VAT mismatch.")
         # We might still allow it but flag it in metadata. 
         # For this lab, let's just warning and return True.
    
    return True
