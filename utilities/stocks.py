import os.path as path
import config
import json

stocks_path = path.join(config.root, "storage", "stocks.json")


def record(data):
    print(data)
    with open(stocks_path, "w") as writer:
        json.dump(data, writer)


def add(data):
    stocks = get()
    stocks.update(data)
    record(stocks)


def get():
    with open(stocks_path, "r") as reader:
        data = json.load(reader)

    return data
