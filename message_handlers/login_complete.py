from telegram import ChatAction
from utilities.mail import login as mail_login
import utilities.verify as verify
import utilities.users as users

def login_complete(update, context):
    chat_id = str(update.effective_chat.id)
    message = update.message.text

    verify_data = verify.get()[chat_id]

    if message == 'resend':
        name = verify_data["name"]
        email = verify_data["email"]
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        mail_login(name, email, chat_id)
        text = 'I just resent the email. Get the orrect code and send it to me.'
        return context.bot.send_message(chat_id=chat_id, text=text)

    if verify_data["code"] != message:
        text = '{0} is not the correct code. I\'ll need you to retype it. Type resend if you want me to send the email again.'.format(message)
        return context.bot.send_message(chat_id=chat_id, text=text)
    
    del verify_data['code']
    users.set(chat_id, verify_data)

    text = '''Hey there {0}. So nice to finally put a face to the conversation. You are all set up and ready to go. '''

    
    