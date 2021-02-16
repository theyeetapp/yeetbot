from random import randint
import config
import re

def login_mail(update, context):
    chat_id = str(update.effective_chat.id)
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email = update.message.text

    if re.match(email_regex, email) is None:
        return context.bot.send_message(chat_id=chat_id, text=email + ' is not a valid email address')
        
    db = config.get()['db']
    cursor = db.cursor()
    query = 'SELECT * FROM users WHERE email="{0}"'.format(email)
    cursor.execute(query)
    user = cursor.fetchone()
    prefixes = ['Hmm,', 'Sorry,', 'I am sorry,', "I'm sorry,"]
    prefix = prefixes[randint(0, len(prefixes) - 1)]
    text = prefix + ' I cannot find any Yeet user with that email address'

    if user is None:
        return context.bot.send_message(chat_id=chat_id, text=text)