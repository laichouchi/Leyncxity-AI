import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), 'memory.json')

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {
        "user_fullname": "Ryan Laichouchi",
        "username": "Leyn.cx",
        "preferences": {}
    }

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_memory(key, value):
    data = load_memory()
    data[key] = value
    save_memory(data)
