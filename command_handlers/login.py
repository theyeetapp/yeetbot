from utilities.actions import record as record_action

def login_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = 'Alright!, send me your Yeet email so I can begin the process of logging you in'
    context.bot.send_message(chat_id=chat_id, text=text)
    record_action(chat_id, 'login')