def send_error_response(context, chat_id, error):
    print(error)
    text = "I am sorry. I ran into an error trying to perform that operation"
    return context.bot.send_message(chat_id=chat_id, text=text)
