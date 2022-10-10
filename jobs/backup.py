from os import path
from utilities.error import send_error_response
import time
import config
import requests
import sys


def parse_dome_uuids():
    file_uuids = config.get("dome_uuids").split(",")
    parsed_dome_uuids = {}

    for file_uuid in file_uuids:
        (file, uuid) = file_uuid.split("//")
        print(file)
        print(uuid)
        parsed_dome_uuids[file] = uuid

    return parsed_dome_uuids


def backup(context):
    files = ["actions.json", "logs.json", "tokens.json", "users.json"]
    dome_uuids = parse_dome_uuids()
    storage_dir = path.join(path.dirname(__file__), "..", "storage")

    for file in files:
        file_path = path.join(storage_dir, file)
        uuid = dome_uuids[file]
        request_files = {"backup": open(file_path, "rb")}
        request_headers = {
            "Authorization": "Bearer {0}".format(config.get("dome_api_key"))
        }
        request_url = "{0}/{1}".format(config.get("dome_api_url"), uuid)
        request_data = {"format": "json"}

        try:
            response = requests.post(
                request_url,
                data=request_data,
                files=request_files,
                headers=request_headers,
            )
            response.raise_for_status()
            print(response)
        except Exception:
            exception = sys.exc_info()
            send_error_response(None, None, exception)

        time.sleep(60)
