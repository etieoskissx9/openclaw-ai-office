from pathlib import Path
import json

BASE_PATH = Path("memory/users")

def init_user_memory(user_id):
    user_path = BASE_PATH / str(user_id)
    user_path.mkdir(parents=True, exist_ok=True)

    files = {
        "profile.json": {},
        "memories.json": [],
        "relations.json": {}
    }

    for filename, default_data in files.items():
        file_path = user_path / filename

        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)

from openai import OpenAI

client = OpenAI()

IMPORTANT_KEYWORDS = [
    "私は",
    "僕は",
    "好き",
    "嫌い",
    "趣味",
    "仕事",
    "出身",
    "住んで",
    "大学",
    "会社",
    "彼女",
    "彼氏",
    "結婚"
]


# STEP3
def is_important(text):

    for word in IMPORTANT_KEYWORDS:
        if word in text:
            return True

    return False


# STEP4
def extract_memory(text):

    prompt = f"""
次の発言から長期的に覚えるべき情報だけ抽出してください。

条件
・客観情報のみ
・短い文章
・雑談は除外

JSON形式

例
{{
"type":"hobby",
"content":"釣りが趣味"
}}

発言:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


# STEP5
def save_memory(user_id, memory):

    path = BASE_PATH / str(user_id) / "memories.json"

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    data.append(memory)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# STEP6
def load_memories(user_id):

    path = BASE_PATH / str(user_id) / "memories.json"

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    texts = []

    for m in data:
        if isinstance(m, dict):
            texts.append(m.get("content", ""))

    return "\n".join(texts)
