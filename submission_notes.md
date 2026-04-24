# Submission Note: The Multi-Modal Minefield Data Pipeline

## 🎯 Project Overview
This project implements a robust, production-ready data pipeline to ingest, clean, and unify data from multiple messy sources into a structured Knowledge Base.


## 🚀 Key Accomplishments

### 1. Multi-Modal Ingestion
- **PDF (Gemini AI)**: Integrated Gemini 1.5/2.5 Flash to extract Author, Title, and Tables from unstructured PDFs. Implemented **Exponential Backoff** to handle API rate limits (429) and robust error handling for missing models.
- **CSV Processing**: Developed a resilient parser for sales records that:
    - Cleans prices from formats like `$1200`, `250000`, and linguistic descriptions ("five dollars").
    - Normalizes 6+ different date formats into ISO `YYYY-MM-DD`.
    - Handles duplicates and missing values (`N/A`, `NULL`, `Liên hệ`).
- **HTML Scraping**: Used BeautifulSoup to target specific product catalogs while stripping out navigation bars, ads, and footers.
- **Transcript Cleaning**: Removed timestamps and audio noise. Implemented specialized regex to extract Vietnamese price words (e.g., "năm trăm nghìn").
- **Legacy Code Analysis**: Leveraged Python's `ast` module to extract business logic rules from docstrings without executing potentially unsafe legacy code.

### 2. Observability & Quality Assurance
Implemented a **Semantic Quality Gate** system that enforces:
- **Content Integrity**: Rejects documents with insufficient content (< 20 chars).
- **Security/Error Filtering**: Blocks documents containing system error strings (NullPointer, Segfault).
- **Business Logic Warnings**: Flags discrepancies, such as the VAT calculation mismatch (8% vs 10%) found in legacy code.

### 3. Orchestration & Performance (SLA)
- Built a Directed Acyclic Graph (DAG) in `orchestrator.py` to sequence all ingestion tasks.
- **SLA Performance**: The entire pipeline processes the full dataset in **~15.6 seconds** (including AI calls).

## ✅ Verification Results
Automated testing via `agent_forensic.py` yielded a perfect score:
- **[PASS]** No duplicate IDs in CSV processing.
- **[PASS]** Correct price extracted from Vietnamese audio transcript.
- **[PASS]** Quality gate successfully rejected corrupt content.

**Final Forensic Score: 3/3**

## 📂 Output Artifacts
- **Consolidated Knowledge Base**: `processed_knowledge_base.json`
- **Schema Reference**: `starter_code/schema.py`
