import os.path as path
import config
import json

crypto_path = path.join(config.root, "data", "crypto.json")


def record(data):
    with open(crypto_path, "w") as writer:
        json.dump(data, writer)


def get():
    with open(crypto_path, "r") as reader:
        data = json.load(reader)

    return data
