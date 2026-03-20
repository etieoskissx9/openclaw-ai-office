from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"


def judge_importance(text):

    prompt = f"""
次の会話を記憶すべきか判定してください。

保存すべきもの
・名前
・仕事
・趣味
・価値観
・人間関係
・重要な出来事

保存不要
・挨拶
・一時的な話題


{text}

回答は必ず
YES
NO
のみ
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer = res.choices[0].message.content.strip()

    return answer == "YES"
