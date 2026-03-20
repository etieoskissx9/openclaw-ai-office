import json
import os

def search_memories(user_id, query):

    file = f"memory/users/{user_id}/memories.json"

    if not os.path.exists(file):
        return []

    with open(file, "r") as f:
        memories = json.load(f)

    results = []

    for m in memories:
        if any(word in m for word in query.split()):
            results.append(m)

    return results[:5]
