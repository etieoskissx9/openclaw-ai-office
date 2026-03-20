import time
import random

print("AI agent started")

while True:

    actions = [
        "thinking",
        "walking",
        "working",
        "coffee break"
    ]

    print("AI:", random.choice(actions))

    time.sleep(10)
