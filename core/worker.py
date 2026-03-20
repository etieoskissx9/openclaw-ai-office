from openai import OpenAI
import os
from core.memory_store import load_memory
from tools.file_tools import write_file, read_file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_worker(user_message, persona, channel):

    # 永続メモリ読み込み
    memory = load_memory()
    user_info = memory.get("user_info", {})

    # systemプロンプト
    system_prompt = f"""
あなたはDiscord上で動作するAIアシスタントです。

【人格】
{persona}

【ユーザー情報】
{user_info}

【ツール】
あなたは必要に応じてツールを使うことができます。

使用可能ツール:
write_file(filename, content)
read_file(filename)

ツールを使う場合は次の形式で出力してください。

TOOL:write_file:filename|content
TOOL:read_file:filename
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()

    # ツールコマンド解析
    if reply.startswith("TOOL:"):

        try:
            parts = reply.split(":", 2)
            tool = parts[1]
            args = parts[2]

            if tool == "write_file":
                filename, content = args.split("|", 1)
                return write_file(filename.strip(), content.strip())

            elif tool == "read_file":
                filename = args.strip()
                return read_file(filename)

        except Exception as e:
            return f"ツール実行エラー: {e}"

    return reply
