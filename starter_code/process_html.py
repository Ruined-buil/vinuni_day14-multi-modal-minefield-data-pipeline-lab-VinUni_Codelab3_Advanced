import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

import re

def extract_logic_from_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # Use AST to find docstrings
    tree = ast.parse(source_code)
    docstrings = []
    
    # Module docstring
    if ast.get_docstring(tree):
        docstrings.append(f"Module Level: {ast.get_docstring(tree)}")
        
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            ds = ast.get_docstring(node)
            if ds:
                docstrings.append(f"{node.name} Docstring: {ds}")
                
    # Use regex for business rules in comments
    business_rules = re.findall(r'# (Business Logic Rule \d+:.*)', source_code)
    discrepancies = re.findall(r'# (WARNING: .*|IMPORTANT: .*)', source_code)
    
    content = "\n".join(docstrings + business_rules + discrepancies)
    
    doc = {
        "document_id": "legacy-code-001",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "timestamp": None,
        "source_metadata": {
            "original_file": "legacy_pipeline.py",
            "rule_count": len(business_rules),
            "warnings_found": len(discrepancies)
        }
    }
    
    return doc

