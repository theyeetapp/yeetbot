from utilities.api import fetch_subscriptions
from requests.exceptions import HTTPError
import threading


class Reminder(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        try:
            response = fetch_subscriptions(self.data["id"])
            print(response)
        except HTTPError as error:
            print(error)
        except Exception as error:
            print(error)
