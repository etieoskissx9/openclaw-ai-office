import os
import json

BASE_PATH = "memory/users"

def ensure_user_memory(user_id):

    user_path = f"{BASE_PATH}/{user_id}"

    if not os.path.exists(user_path):
        os.makedirs(user_path)

        with open(f"{user_path}/memories.json", "w") as f:
            json.dump([], f)

        with open(f"{user_path}/profile.json", "w") as f:
            json.dump({}, f)
