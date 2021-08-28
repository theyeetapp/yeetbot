from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.api import fetch_symbols
from utilities.error import send_error_response
import utilities.users as users
from requests.exceptions import HTTPError
import config


def list_type(update, context, type):
    chat_id = str(update.effective_chat.id)
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    user = users.get()[chat_id]
    name = user["name"].split(" ")[1]
    formatted_type = type + "s" if type == "stock" else "cryptocurrencies"

    try:
        response = fetch_symbols(user["id"], type)
    except HTTPError as error:
        return send_error_response(context, chat_id, error)
    except Exception as error:
        return send_error_response(context, chat_id, error)

    symbols = response.get("symbols")
    symbols = list(
        map(
            lambda symbol: {
                "name": symbol["name"].upper(),
                "company": symbol["company"].replace("-", " ").title(),
            },
            symbols,
        )
    )
    if len(symbols) == 0:
        text = "You are not subscribed to any {0} {1}".format(formatted_type, name)
        return context.bot.send_message(chat_id=chat_id, text=text)

    text = get_response(symbols, name, type)
    return context.bot.send_message(chat_id=chat_id, text=text)


def get_response(symbols, name, type):
    count = len(symbols)
    text = (
        "Here are your {0} {1} subscriptions {2}\n\n".format(count, type, name)
        if count > 1
        else "Here is your single {0} subscription {1}\n\n".format(type, name)
    )

    for symbol in symbols:
        symbol_text = "{0}\n{1}\n\n".format(symbol["name"], symbol["company"])
        text = text + symbol_text

    return text
