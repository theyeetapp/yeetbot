from utilities.mail import verify
from random import randint, sample
from utilities.actions import record as record_action
import config
import os.path as path
import re
import json
import string

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
    
    characters = string.ascii_letters + string.digits
    code = ''.join(sample(characters, 10))
    verify(user, code)

    verify_path = path.join(config.root, 'data', 'verify.json')
    with open(verify_path, 'r') as reader:
        data = json.load(reader)
    
    data[chat_id] = {"email":user[2], "code":code}

    with open(verify_path, 'w') as writer:
        json.dump(data, writer)

    text = 'I just sent you an email. Follow the instructions there to complete this process.'
    record_action(chat_id, 'login_email')
    return context.bot.send_message(chat_id=chat_id, text=text)