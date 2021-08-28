from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.api import fetch_symbols
from utilities.error import send_error_response
import utilities.users as users
from requests.exceptions import HTTPError


def list_handler(update, context):
    chat_id = str(update.effective_chat.id)
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    user = users.get()[chat_id]
    name = user["name"].split(" ")[1]

    try:
        response = fetch_symbols(user["id"])
    except HTTPError as error:
        return send_error_response(context, chat_id, error)
    except Exception as error:
        return send_error_response(context, chat_id, error)

    record_action(chat_id, "list")
    symbols = response.get("symbols")
    symbols = list(
        map(
            lambda symbol: {
                "name": symbol["name"],
                "company": symbol["company"],
                "type": symbol["type"],
            },
            symbols,
        )
    )
    if len(symbols) == 0:
        text = "You are not subscribed to any stocks or cryptocurrencies {0}".format(
            name
        )
        return context.bot.send_message(chat_id=chat_id, text=text)

    text = get_response(symbols, name)
    return context.bot.send_message(chat_id=chat_id, text=text)


def get_response(symbols, name):
    count = len(symbols)
    text = (
        "Here are your {0} subscriptions {1}\n\n".format(count, name)
        if count > 1
        else "Here is your single subscription {0}\n\n".format(name)
    )

    for symbol in symbols:
        symbol_text = "{0} - {1}\n{2}\n\n".format(
            symbol["name"].upper(),
            symbol["type"],
            symbol["company"].replace("-", " ").title(),
        )
        text = text + symbol_text

    return text
