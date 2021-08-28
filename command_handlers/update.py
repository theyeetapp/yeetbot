from utilities.actions import record as record_action


def update_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = "Cool. What is your Yeet email ?"
    record_action(chat_id, "update")
    context.bot.send_message(chat_id=chat_id, text=text)
