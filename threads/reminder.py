from utilities.api import fetch_subscriptions
from utilities.stocks import get as get_stocks
from utilities.crypto import get as get_crypto
from datetime import datetime
from requests.exceptions import HTTPError
import threading
import traceback
import sys


class Reminder(threading.Thread):
    symbols = None

    def __init__(self, name, data, context, chat_id):
        threading.Thread.__init__(self)
        self.name = name
        self.data = data
        self.context = context
        self.chat_id = chat_id

    def run(self):
        try:
            response = fetch_subscriptions(self.data["id"])
            symbols = response.get("symbols")
            self.symbols = list(
                map(
                    lambda symbol: {
                        "name": symbol["name"],
                        "company": symbol["company"],
                        "type": symbol["type"],
                    },
                    symbols,
                )
            )
            self.send()
        except HTTPError as error:
            traceback.print_exception(*sys.exc_info())
        except Exception as error:
            traceback.print_exception(*sys.exc_info())

    def send(self):
        name = self.data["name"].split(" ")[1]
        text = "Hello {0}. Here is your roundup for today {1}. All values are in US dollars.\n\n{2}{3}".format(
            name,
            self.get_formatted_date(),
            self.get_type_response("stock"),
            self.get_type_response("crypto"),
        )
        return self.context.bot.send_message(chat_id=self.chat_id, text=text)

    def get_type_response(self, type):
        symbols = filter(lambda symbol: symbol["type"] == type, self.symbols)
        symbols_data = get_stocks() if type == "stock" else get_crypto()
        message = "{0}\n\n".format("Stocks" if type == "stock" else "Cryptocurrencies")

        for symbol in symbols:
            key = symbol["name"] if type == "stock" else symbol["company"]
            data = symbols_data.get(key)
            if data is not None:
                text = "{0}\n".format(symbol["name"].upper())
                for param, value in data.items():
                    text += "{0} - {1}\n".format(param, value)
                message += "{0}\n".format(text)

        return message

    def get_formatted_date(self):
        now = datetime.now()
        dt = int(now.strftime("%d"))
        dt = (
            str(dt) + "th"
            if 11 <= dt <= 13
            else str(dt) + {1: "st", 2: "nd", 3: "rd"}.get(dt % 10, "th")
        )
        return "{0}, {1} {2}".format(now.strftime("%A"), dt, now.strftime("%B, %Y"))
