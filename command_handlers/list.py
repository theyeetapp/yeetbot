from telegram import ChatAction
from utilities.actions import record as record_action
import utilities.users as users
import config


def list_handler(update, context):
    chat_id = str(update.effective_chat.id)
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    user = users.get()[chat_id]
    name = user["name"].split(" ")[1]
    db = config.get()["db"]
    cursor = db.cursor()
    query = 'SELECT symbol_id from subscriptions WHERE user_id="{0}"'.format(user["id"])
    cursor.execute(query)
    symbol_ids = cursor.fetchall()
    record_action(chat_id, "list")

    if len(symbol_ids) == 0:
        text = "You are not subscribed to any stocks or cryptocurrencies {0}".format(
            name
        )
        return context.bot.send_message(chat_id=chat_id, text=text)

    symbol_ids = ",".join(list(map(get_symbol_id, symbol_ids)))

    query = "SELECT * FROM symbols WHERE id IN ({0})".format(symbol_ids)
    cursor.execute(query)
    symbols = cursor.fetchall()
    text = get_response(symbols, name)
    return context.bot.send_message(chat_id=chat_id, text=text)


def get_symbol_id(symbol_tuple):
    return str(symbol_tuple[0])


def get_response(symbols, name):
    count = len(symbols)
    text = (
        "Here are your {0} subscriptions {1}\n\n".format(count, name)
        if count > 1
        else "Here is your single subscription {0}\n\n".format(name)
    )

    for symbol in symbols:
        symbol_text = "{0} - {1}\n{2}\n\n".format(symbol[1], symbol[3], symbol[2])
        text = text + symbol_text

    return text
