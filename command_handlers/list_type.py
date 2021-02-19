from telegram import ChatAction
import utilities.users as users
import config

def list_type(update, context, type):
    chat_id = str(update.effective_chat.id)
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    user = users.get()[chat_id]
    name = user['name'].split(' ')[1]
    db = config.get()['db']
    cursor = db.cursor()
    query = 'SELECT symbol_id FROM subscriptions WHERE user_id="{0}"'.format(user['id'])
    cursor.execute(query)
    symbol_ids = cursor.fetchall()

    if len(symbol_ids) == 0:
        text = 'You are not subscribed to any stocks or crypto {0}'.format(name)
        return context.bot.send_message(chat_id=chat_id, text=text)

    symbol_ids = ','.join(list(map(get_symbol_id, symbol_ids)))
    query = 'SELECT * FROM symbols WHERE id IN ({0}) AND type="{1}"'.format(symbol_ids, type)
    cursor.execute(query)
    symbols = cursor.fetchall()

    if len(symbols) == 0:
        formatted_type = type + 's' if type == 'stock' else type
        text = 'You are not subscribed to any {0} {1}'.format(formatted_type, name)
        return context.bot.send_message(chat_id=chat_id, text=text)
    
    text = get_response(symbols, name, type)
    return context.bot.send_message(chat_id=chat_id, text=text)

def get_symbol_id(symbol_tuple):
    return str(symbol_tuple[0])

def get_response(symbols, name, type):
    count = len(symbols)
    text = 'Here are your {0} {1} subscriptions {2}\n\n'.format(count, type, name) if count > 1 else 'Here is your single {0} subscription {1}\n\n'.format(type, name)

    for symbol in symbols:
        symbol_text = '{0}\n{1}\n\n'.format(symbol[1], symbol[2])
        text = text + symbol_text
    
    return text
