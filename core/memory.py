import os

LOG_DIR = "logs"

def load_recent_memory(channel, limit=50):

    path = f"{LOG_DIR}/{channel}.txt"

    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    recent = lines[-limit:]

    return "".join(recent)

