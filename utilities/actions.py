from config import root
import os.path as path
import json


def record(chat_id, action):
    action_path = path.join(root, "storage", "actions.json")
    with open(action_path, "r") as reader:
        actions = json.load(reader)

    actions[chat_id] = action

    with open(action_path, "w") as writer:
        json.dump(actions, writer)
