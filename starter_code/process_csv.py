import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

import re
from datetime import datetime

def parse_price(price_str):
    if pd.isna(price_str) or str(price_str).lower() in ['n/a', 'liên hệ', 'null']:
        return 0.0
    
    s = str(price_str).lower()
    
    # Handle text numbers
    word_to_num = {'five': 5, 'ten': 10} # Add more if needed
    for word, num in word_to_num.items():
        if word in s:
            return float(num)
            
    # Remove currency symbols and commas
    s = re.sub(r'[^\d\.-]', '', s)
    try:
        return float(s)
    except:
        return 0.0

def normalize_date(date_str):
    if pd.isna(date_str):
        return None
    
    s = str(date_str).strip()
    
    # Try common formats
    formats = [
        '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', 
        '%B %dth %Y', '%B %dst %Y', '%B %dnd %Y', '%B %drd %Y',
        '%d %b %Y'
    ]
    
    # Pre-process some strings to make them easier to parse
    s = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', s) # Remove st, nd, rd, th
    
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except:
            continue
    return s # Return as is if failed

def process_sales_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Remove duplicates based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    unified_docs = []
    for _, row in df.iterrows():
        price = parse_price(row['price'])
        date = normalize_date(row['date_of_sale'])
        
        content = f"Sale record for {row['product_name']} ({row['category']}). Price: {price} {row['currency']}."
        
        doc = {
            "document_id": f"csv-sale-{row['id']}",
            "content": content,
            "source_type": "CSV",
            "author": f"Seller {row['seller_id']}",
            "timestamp": date,
            "source_metadata": {
                "product_name": row['product_name'],
                "category": row['category'],
                "price": price,
                "currency": row['currency'],
                "stock": row['stock_quantity'] if not pd.isna(row['stock_quantity']) else 0
            }
        }
        unified_docs.append(doc)
        
    return unified_docs

