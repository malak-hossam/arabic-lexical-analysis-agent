from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

from meaning import ai_agent

app = FastAPI()

# ✅ route أساسي يطمن إن الـ API شغالة
@app.get("/")
def root():
    return {"status": "Word meaning API is running."}

# ✅ route الأساسي اللي بيحلل الكلمة
class Query(BaseModel):
    word: str
    type: Literal["synonyms", "antonyms", "plural"]

@app.post("/analyze/")
def analyze_word(query: Query):
    result = ai_agent(query.word, query.type)
    return result
