from utilities.actions import record as record_action
from utilities.users import get as get_users


def update_handler(update, context):
    chat_id = str(update.effective_chat.id)

    if get_users().get(chat_id) is not None:
        text = "There is nothing to update. Use a different Telegram account."
        return context.bot.send_message(chat_id=chat_id, text=text)
        
    text = "Cool. What is your Yeet email ?"
    record_action(chat_id, "update")
    context.bot.send_message(chat_id=chat_id, text=text)
