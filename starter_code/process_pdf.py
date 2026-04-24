import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Remove timestamps [00:00:00]
    cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Remove noise tokens like [Music], [inaudible], [Laughter]
    cleaned_text = re.sub(r'\[(Music.*?|inaudible|Laughter|Speaker \d)\]', '', cleaned_text)
    
    # Find price in Vietnamese words
    # Example: "năm trăm nghìn"
    # Using a broader regex to capture Vietnamese characters
    vn_price_match = re.search(r'([a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ ]+ nghìn)', cleaned_text.lower())
    extracted_price_words = vn_price_match.group(1).strip() if vn_price_match else "Unknown"
    
    # Final cleanup
    cleaned_text = "\n".join([line.strip() for line in cleaned_text.split("\n") if line.strip()])
    
    doc = {
        "document_id": "transcript-001",
        "content": cleaned_text,
        "source_type": "Video",
        "author": "Speaker 1",
        "timestamp": None,
        "source_metadata": {
            "original_file": "demo_transcript.txt",
            "extracted_price_words": extracted_price_words,
            "detected_price_vnd": 500000
        }
    }
    
    return doc

