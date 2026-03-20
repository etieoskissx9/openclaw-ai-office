import os
from datetime import datetime

LOG_DIR = "logs"

def save_log(username, channel, user_message, bot_response):

    os.makedirs(LOG_DIR, exist_ok=True)

    filename = f"{LOG_DIR}/{channel}.txt"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_text = f"""
[{now}]
User: {username}
Message: {user_message}

Bot:
{bot_response}
------------------------
"""

    with open(filename, "a", encoding="utf-8") as f:
        f.write(log_text)
