import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import time

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = genai.upload_file(path=file_path)
    except Exception as e:
        print(f"Failed to upload file to Gemini: {e}")
        return None
        
    prompt = """
    Analyze this document and extract the Title, Author, a 3-sentence summary, and any important tables.
    Output exactly as a JSON object matching this schema:
    {
        "document_id": "pdf-doc-001",
        "content": "Summary: [Summary text here]",
        "source_type": "PDF",
        "author": "[Author Name]",
        "timestamp": null,
        "source_metadata": {
            "title": "[Document Title]",
            "tables": "[Extracted tables as text or list]",
            "original_file": "lecture_notes.pdf"
        }
    }
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Generating content from PDF using Gemini (Attempt {attempt + 1})...")
            response = model.generate_content([pdf_file, prompt])
            content_text = response.text
            
            # Simple cleanup if the response is wrapped in markdown json block
            content_text = content_text.strip()
            if content_text.startswith("```json"):
                content_text = content_text[7:]
            if content_text.endswith("```"):
                content_text = content_text[:-3]
            if content_text.startswith("```"):
                content_text = content_text[3:]
                
            extracted_data = json.loads(content_text.strip())
            return extracted_data
        except Exception as e:
            if "429" in str(e):
                wait_time = 2 ** attempt
                print(f"Rate limited (429). Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"Failed to extract PDF data: {e}")
                break
    return None
