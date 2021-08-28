def unknown_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = "I'm sorry. I do not understand that"
    return context.bot.send_message(chat_id=chat_id, text=text)
