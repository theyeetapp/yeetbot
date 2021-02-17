import os.path as path
import config
import json

users_path = path.join(config.root, 'data', 'users.json')

def get():
    with open(users_path, 'r') as reader:
        data = json.load(reader)
    return data

def set(key, value):
    data = get()
    data[key] = value
    with open(users_path, 'w') as writer:
        json.dump(data, writer)