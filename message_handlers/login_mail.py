from telegram import ChatAction
from utilities.mail import login as mail_login
from random import randint
from utilities.actions import record as record_action
import config
import os.path as path
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
    
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    mail_login(user[0], user[1], user[2], chat_id)

    text = 'I just sent you an email with a verification code. Send me that code and I will log you in.'
    record_action(chat_id, 'login_email')
    return context.bot.send_message(chat_id=chat_id, text=text)