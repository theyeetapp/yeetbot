from config import root
import os.path as path
import json

def record(chat_id, action):
    action_path = path.join(root, 'data', 'actions.json')
    with open(action_path, 'r') as reader:
        actions = json.load(reader)

    if actions[chat_id] is None:
        actions[chat_id] = action
    else:
        del actions[chat_id]
        actions[chat_id] = action

    with open(action_path, 'w') as writer:
        json.dump(actions, writer)


