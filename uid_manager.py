import json
import os

FILE = "uid_map.json"

def load_uid_map():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)

def save_uid_map(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(uid, name):
    data = load_uid_map()
    data[uid] = name
    save_uid_map(data)
    print(f"[✔] UID {uid} mapped to {name}")