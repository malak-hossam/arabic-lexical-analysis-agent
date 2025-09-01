# arabic-lexical-analysis-agent

**Arabic Lexical Analysis Agent — Synonyms / Antonyms / Plurals**

---

## 📘 Project Description

This repository provides an **Arabic lexical analysis microservice** that returns **synonyms**, **antonyms**, and **plural forms** for a given Arabic word.

It uses a **local SQLite database (`data.db`)** for instant lookups and offers an **optional fallback** (search + LLM) when an entry is missing. The service is built with **FastAPI** and is easy to integrate with web or mobile applications.

---

## 📚 Dataset

The service uses a local SQLite database file: `data.db`.

- **Source**: [ArabicLT by mdanok](https://github.com/mdanok/ArabicLT) (MIT License)
- **Core Tables**:
  - `synonyms (WORD, SYNO_SET)`
  - `antonyms (WORD, ANTO_SET)`
  - `plural (WORD, PLURAL)`

When a local entry exists, it is returned instantly. If not, the fallback (LLM) can be optionally used to generate a short response.

---

## 🎯 Objectives

- Provide **low-latency** lookups from a local database.
- Offer an **optional fallback** (web search + Gemini API).
- Expose a clean **REST API** for developers.

---

## 🗂️ Project Structure

```
arabic-lexical-analysis-agent/
├── meaning.py           # Core agent logic (lookup + optional fallback)
├── main.py              # FastAPI app with /analyze/ endpoint
├── data.db              # SQLite dictionary database
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/<malak-hossam>/arabic-lexical-analysis-agent.git
cd arabic-lexical-analysis-agent
```

### 2. Create and activate a virtual environment

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Place the database file

- Download `data.db` from [ArabicLT](https://github.com/mdanok/ArabicLT)
- Put it in the root of the project (same folder as `main.py`)
- If you move it elsewhere, update the path in `meaning.py`

### 5. (Optional) Set API keys for fallback

**macOS / Linux:**

```bash
export GEMINI_API_KEY="your_key_here"
export TAVILY_API_KEY="your_key_here"
```

**Windows (PowerShell):**

```powershell
$env:GEMINI_API_KEY="your_key_here"
$env:TAVILY_API_KEY="your_key_here"
```

---

## ▶️ Running the App

```bash
uvicorn main:app --reload
```

App will be available at:

```
http://127.0.0.1:8000/
```

---

## 🔌 API Usage

### Endpoint

```
POST /analyze/
```

### Request Example

```json
{
  "word": "سعيد",
  "type": "antonyms"
}
```

### Response Example

```json
{
  "source": "lookup",
  "result": "حزين"
}
```

### Accepted `type` values:

- `synonyms`
- `antonyms`
- `plural`

### `source` field:

- `"lookup"` → found in local SQLite database  
- `"fallback"` → generated via Tavily + Gemini (optional)  
- `"validation"` → invalid or multi-word input

---

## 🐳 Docker (Optional)

### 1. Build the image

```bash
docker build -t arabic-lexical-analysis-agent .
```

### 2. Run the container

```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY="your_key" \
  -e TAVILY_API_KEY="your_key" \
  -v $(pwd)/data.db:/app/data.db \
  arabic-lexical-analysis-agent
```

---

## 🛡️ Configuration & Security

- Never commit sensitive API keys — use `.env` or CI/CD secrets.
- Validate all user inputs — especially `type` and `word` fields.
- If you don’t want the fallback, you can disable Gemini/Tavily integration and rely only on local data.

---

## 📦 Requirements

```
fastapi
uvicorn
requests
google-generativeai
pandas
# sqlite3 (built-in with Python)
```

---

## 📝 License & Acknowledgments

- The local dictionary database (`data.db`) was sourced from the [ArabicLT GitHub repository](https://github.com/mdanok/ArabicLT), licensed under the **MIT License**.
- This repo provides attribution and does not modify the original dataset.
- Any external APIs (Gemini, Tavily) must be used under their respective terms.

---

## 👤 Author

**Malak Hossam**  
AI Engineer — Natural Language Processing & Educational AI
