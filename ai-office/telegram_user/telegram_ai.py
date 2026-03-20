import os
import json
import asyncio
import random

from core.memory_manager import (
    init_user_memory,
    is_important,
    extract_memory,
    save_memory,
    load_memories
)
from telethon import TelegramClient, events
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# .env 読み込み
# -----------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# -----------------------------
# OpenAIクライアント
# -----------------------------
ai = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# Telegramクライアント
# -----------------------------
client = TelegramClient("session", api_id, api_hash)

# -----------------------------
# 会話メモリ
# -----------------------------
MEMORY_FILE = "memory.json"
MAX_HISTORY = 20

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# -----------------------------
# ChatGPTに送る関数
# -----------------------------
def chat_with_ai(user_id, text, memories):
memory[user_id].append({
    "role": "user",
    "content": text
})

    # 履歴圧縮（トークン節約）
    history = memory[user_id][-MAX_HISTORY:]

    # メモリを文字列化
    memory_text = ""
    for m in memories:
        memory_text += f"- {m['content']}\n"

    messages = [
        {
            "role": "system",
            "content":f"""
	あなたは優しい甘々の雑談相手です。フレンドリーに話してめちゃくちゃ甘やかしてください。敬語は不要です。10代の若者がLINEで会話している感じを真似してください。例えば文末に適切なタイミングで「笑」を付けるなどしてください。"
        ユーザーについて知っている情報
	{memory_text}
	"""

	 }
    ] + history

    response = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply

# =========================
# typingリアル化
# =========================

async def realistic_typing(chat, text):

    # 文字数からtyping時間を計算
    length = len(text)

    typing_time = min(max(length * 0.15, 1.5), 6)

    async with client.action(chat, "typing"):
        await asyncio.sleep(typing_time)

# -----------------------------
# Telegramメッセージ受信
# -----------------------------
@client.on(events.NewMessage)
async def handler(event):

    try:

        # 自分の発言は無視
        if event.out:
            return

        text = event.text

        if not text:
            return

        user_id = str(event.sender_id)

	init_user_memory(user_id)

	# 重要情報なら記憶
	if is_important(text):

	    memory = extract_memory(text)

	    try:
        	memory_json = json.loads(memory)
        	save_memory(user_id, memory_json)
   	 except:
   	     pass
        
	chat = await event.get_chat()

        print(f"[{user_id}] {text}")\

        # AI生成
	memories = load_memories(user_id)

	reply = chat_with_ai(user_id, text, memories)
        
	# typing演出
        await realistic_typing(chat, reply)

        await event.reply(reply)

    except Exception as e:

        print("ERROR:", e)

        try:
            await event.reply("ごめん、ちょっと調子悪いみたい…もう一回送って？")
        except:
            pass

# -----------------------------
# 起動
# -----------------------------
async def main():
    print("Telegram AI started")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
