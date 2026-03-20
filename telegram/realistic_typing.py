import asyncio
import random


async def realistic_typing(chat, text):

    # 文字数に応じてタイピング時間を計算
    base_speed = random.uniform(0.04, 0.07)

    typing_time = min(len(text) * base_speed, 8)

    try:
        await chat.action("typing")
        await asyncio.sleep(typing_time)
    except:
        pass
