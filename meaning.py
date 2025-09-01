import pandas as pd
import sqlite3
import google.generativeai as genai
import requests
import re
import os


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")
conn = sqlite3.connect(db_path)



def load_table_to_dict(table_name, value_column):
    df = pd.read_sql_query(f"SELECT WORD, {value_column} FROM {table_name}", conn)
    return dict(zip(df["WORD"].str.strip(), df[value_column]))

syn_dict = load_table_to_dict("synonyms", "SYNO_SET")
ant_dict = load_table_to_dict("antonyms", "ANTO_SET")
plur_dict = load_table_to_dict("plural", "PLURAL")



def lookup(word, type_):
    word = word.strip()
    
    if type_ == "synonyms":
        raw = syn_dict.get(word)
    elif type_ == "antonyms":
        raw = ant_dict.get(word)
    elif type_ == "plural":
        raw = plur_dict.get(word)
    else:
        return None

    if raw:
        # إزالة المسافات الزائدة وتقسيم على ;
        items = [item.strip() for item in raw.split(";") if item.strip()]
        return items if len(items) > 1 else items[0]
    return None


def clean_generated_result(text, type_):
    if not text:
        return None

    # إزالة الرموز والفواصل والسطور الزائدة
    text = text.strip()
    text = re.sub(r"[:؛،\"“”]", "", text)
    text = re.sub(r"\n.*", "", text)
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # فلترة الجمل الطويلة
    words = text.split()
    if len(words) > 3:
        return None

    return text



def generate_with_gemini(word, context, type_):
    prompt_map = {
        "synonyms": f"""أعطِ مرادفًا دقيقًا وواضحًا للكلمة '{word}' في اللغة العربية الفصحى، بشرط أن يكون المرادف مساويًا لها في المعنى وليس قريبًا فقط.
    تجاهل التشكيل إن وُجد، ولا تعطِ أكثر من كلمة واحدة. إذا لم يوجد مرادف صحيح للكلمة، قل "لا يوجد".""" ,
        
        "antonyms": f"""أعطِ ضدًا دقيقًا وواضحًا للكلمة '{word}' في اللغة العربية الفصحى، بشرط أن يكون عكسًا مباشرًا وصحيحًا في المعنى.
    تجاهل التشكيل إن وُجد، ولا تعطِ أكثر من كلمة واحدة. إذا لم يوجد ضد صحيح للكلمة، قل "لا يوجد".""" ,
    
        "plural": f"""أعطِ جمعًا صحيحًا وواضحًا للكلمة '{word}' في اللغة العربية الفصحى.
    تجاهل التشكيل إن وُجد، ولا تعطِ أكثر من كلمة واحدة. إذا لم يكن للكلمة جمع معروف، قل "لا يوجد".""" ,
    }

    prompt = f"""أنت مساعد لغوي محترف في اللغة العربية.
{prompt_map.get(type_, 'فسّر الكلمة')} \n\n{context}"""

    try:
        response = model.generate_content(prompt)
        cleaned = clean_generated_result(response.text, type_)
        return cleaned
    except Exception as e:
        return f"❌ حدث خطأ أثناء توليد الإجابة: {str(e)}"




def web_search_ai_agent(word, type_):
    print(f"🔍 Web searching for: {word} ({type_})")
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
            json={
                "query": f"ما {type_} كلمة {word}",
                "search_depth": "basic",
                "include_answer": False,
                "max_results": 3
            }
        )
        data = response.json()
        results = data.get("results", [])
        context = "\n".join([res["content"] for res in results])
        return generate_with_gemini(word, context, type_)
    except Exception as e:
        return f"❌ حدث خطأ أثناء البحث: {str(e)}"



def ai_agent(word, type_):
    if len(word.strip().split()) > 1:
        return {"source": "validation", "result": "❌ الرجاء إدخال كلمة واحدة فقط."}
    
    local_result = lookup(word, type_)
    if local_result:
        return {"source": "lookup", "result": local_result}
    else:
        web_result = web_search_ai_agent(word, type_)
        return {"source": "web_search", "result": web_result}

