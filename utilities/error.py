def send_error_response(context, chat_id, error, exit=True):
    print(error)
    text = "I am sorry. I ran into an error trying to perform that operation"
    if exit:
        return context.bot.send_message(chat_id=chat_id, text=text)
