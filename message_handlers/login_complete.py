from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.mail import login as mail_login
import utilities.verify as verify
import utilities.users as users
import config
import os.path as path

def login_complete(update, context):
    chat_id = str(update.effective_chat.id)
    message = update.message.text

    verify_data = verify.get()[chat_id]
    user_id = verify_data["id"]
    name = verify_data["name"]
    email = verify_data["email"]

    if message == 'resend':
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        mail_login(user_id, name, email, chat_id)
        text = 'I just resent the email. Get the orrect code and send it to me.'
        return context.bot.send_message(chat_id=chat_id, text=text)

    if verify_data["code"] != message:
        text = '{0} is not the correct code. I\'ll need you to retype it. Type resend if you want me to send the email again.'.format(message)
        return context.bot.send_message(chat_id=chat_id, text=text)
    
    del verify_data['code']
    users.set(chat_id, verify_data)
    verify.delete(chat_id)

    db = config.get()['db']
    cursor = db.cursor()
    query = 'SELECT count(*) FROM subscriptions WHERE user_id="{0}"'.format(user_id)
    cursor.execute(query)
    count = cursor.fetchone()

    message_path = path.join(config.root, 'messages', 'verified.txt')
    with open(message_path, 'r') as reader:
        text = reader.read().format(name.split(' ')[1], count[0])
    
    record_action(chat_id, 'login_complete')
    return context.bot.send_message(chat_id=chat_id, text=text)
    
    
    