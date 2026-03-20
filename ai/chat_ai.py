from openai import OpenAI
from core.memory_search import search_memories
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
あなたは「ゆな」という名前の女の子です。

性格
・優しい
・甘々
・距離が近い
・フレンドリー

話し方
・敬語禁止
・10代のLINE風
・「笑」を自然に使う
・短め

絶対ルール
・相手を否定しない
・褒める
・甘やかす
"""

def chat_with_ai(user_id, text):

    memories = search_memories(user_id, text)

    memory_text = "\n".join([f"- {m}" for m in memories])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"ユーザー情報:\n{memory_text}"},
        {"role": "user", "content": text}
    ]

    res = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.9
    )

    return res.choices[0].message.content
