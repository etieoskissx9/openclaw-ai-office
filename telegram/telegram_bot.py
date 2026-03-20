import os
import asyncio
import random

from dotenv import load_dotenv
from telethon import TelegramClient, events, functions, types

from ai.chat_ai import chat_with_ai
from core.memory_manager import init_user_memory, save_memory

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("session", api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):

    user_id = event.sender_id
    text = event.raw_text

    print("受信:", text)  # デバッグ

    # メモリ初期化
    init_user_memory(user_id)

    # typing演出
    chat = await event.get_input_chat()

    await client(functions.messages.SetTypingRequest(
        peer=chat,
        action=types.SendMessageTypingAction()
    ))

    await asyncio.sleep(random.uniform(1, 2.5))

    # AI返信
    reply = chat_with_ai(user_id, text)

    await event.reply(reply)

    # 記憶保存
    save_memory(user_id, text)


client.start()
client.run_until_disconnected()
