# Arabic Lexical Analysis Agent (Synonyms / Antonyms / Plurals)

## Project Description
This project provides an **Arabic lexical analysis microservice** that returns **synonyms, antonyms, and plural forms** for a given Arabic word.  
It combines a **local SQLite dictionary** for instant lookups with a **fallback pipeline** that uses **Tavily web search** to build context and **Google Gemini** to generate a clean, single-word answer when the word isn’t found locally. The service is exposed via **FastAPI**. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

---

## Dataset
The service ships with a local **SQLite** database `data.db` that stores three tables: `synonyms`, `antonyms`, and `plural`.  
Each table maps a **WORD** to its target value(s). When a local entry exists, it’s returned immediately; otherwise, the service performs a web-assisted generation. :contentReference[oaicite:2]{index=2}

### Key Columns
- **WORD**: Arabic lemma (lookup key). :contentReference[oaicite:3]{index=3}  
- **SYNO_SET / ANTO_SET / PLURAL**: Stored results for synonyms, antonyms, and plural (semicolon-separated if multiple). :contentReference[oaicite:4]{index=4}

> **Provenance**: Source dictionary content was originally collected from GitHub resources (add your specific link here).

---

## Objectives
1. Provide low-latency lexical lookups from a local database. :contentReference[oaicite:5]{index=5}  
2. Fallback to **Tavily + Gemini** with prompt constraints to return **one precise word** when no local entry exists. :contentReference[oaicite:6]{index=6}  
3. Expose a simple, robust **REST API** for integration with web/mobile apps. :contentReference[oaicite:7]{index=7}

---

## Project Structure
- **`meaning.py`** → Core agent: SQLite lookup → Tavily search → Gemini generation + cleaning. :contentReference[oaicite:8]{index=8}  
- **`main.py`** → FastAPI app with `POST /analyze/` endpoint using `ai_agent(...)`. :contentReference[oaicite:9]{index=9}  
- **`data.db`** → Local SQLite database (synonyms/antonyms/plurals). :contentReference[oaicite:10]{index=10}  
- **`requirements.txt`** → Dependencies (FastAPI, Uvicorn, pandas, sqlite3, Tavily, Google Generative AI, LangChain if needed). :contentReference[oaicite:11]{index=11}

---

## Analysis Overview
### Local Lookup
- Reads from `data.db` and returns stored result if present (splits `;` lists, trims whitespace). :contentReference[oaicite:12]{index=12}

### Web-Assisted Fallback
- Queries **Tavily** for concise context, then asks **Gemini** for **a single precise word** (or “لا يوجد”).  
- Post-processes/cleans the output (remove punctuation, brackets, long phrases; restrict to ≤ 3 tokens). :contentReference[oaicite:13]{index=13}

### API Layer
- `POST /analyze/` accepts `{ "word": "...", "type": "synonyms|antonyms|plural" }` and returns `{ "source": "...", "result": ... }`. :contentReference[oaicite:14]{index=14}

---

## Project Structure (Tree)
```plaintext
arabic-lexical-analysis-agent/
├─ meaning.py
├─ main.py
├─ data.db
├─ requirements.txt
└─ README.md
