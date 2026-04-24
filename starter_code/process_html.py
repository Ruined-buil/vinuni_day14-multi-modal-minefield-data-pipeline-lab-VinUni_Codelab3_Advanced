from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    unified_docs = []
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue
            
        sp_id = cols[0].text.strip()
        name = cols[1].text.strip()
        category = cols[2].text.strip()
        price_raw = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip()
        
        # Clean price
        price_clean = price_raw.replace(',', '').replace(' VND', '')
        if price_clean.lower() in ['n/a', 'liên hệ']:
            price_val = 0.0
        try:
            price_val = float(price_clean)
        except:
            price_val = 0.0
            
        content = f"Product: {name} ({category}). Stock: {stock}. Rating: {rating}."
        
        doc = {
            "document_id": f"html-{sp_id}",
            "content": content,
            "source_type": "HTML",
            "author": "VinShop System",
            "timestamp": None,
            "source_metadata": {
                "product_name": name,
                "category": category,
                "price": price_val,
                "stock": stock,
                "rating": rating
            }
        }
        unified_docs.append(doc)
        
    return unified_docs

