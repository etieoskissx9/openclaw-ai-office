import os
import discord
import re

from core.worker import run_worker
from core.memory_store import load_memory, save_memory
from core.memory_manager import init_user_memory

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def load_persona(channel_name):
    persona_file = f"personas/{channel_name}.txt"

    if os.path.exists(persona_file):
        with open(persona_file, "r", encoding="utf-8") as f:
            return f.read()

    return "あなたは親切なAIアシスタントです。"


def save_log(channel_name, username, message):

    os.makedirs("logs", exist_ok=True)

    log_file = f"logs/{channel_name}.txt"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{username}: {message}\n")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    user_id = message.author.id

    init_user_memory(user_id)

    text = message.content
    channel_name = message.channel.name
    username = message.author.name

    # 会話ログ保存
    save_log(channel_name, username, text)\

    # メモリ読み込み
    memory = load_memory()

    # 名前記憶機能
    match = re.search(r"私の名前は(.+)", text)

    if match:
        name = match.group(1).strip()

        if "user_info" not in memory:
            memory["user_info"] = {}

        memory["user_info"]["name"] = name

        save_memory(memory)

    # persona読み込み
    persona = load_persona(channel_name)

    # AI応答生成
    reply = run_worker(text, persona, channel_name)

    # Bot返信
    await message.channel.send(reply)

    # Botログ保存
    save_log(channel_name, "BOT", reply)


client.run(TOKEN)
