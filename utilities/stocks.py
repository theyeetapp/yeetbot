import os.path as path
import config
import json

stocks_path = path.join(config.root, "data", "stocks.json")


def record(data):
    with open(stocks_path, "w") as writer:
        json.dump(data, writer)
