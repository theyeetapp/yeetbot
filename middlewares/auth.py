import utilities.users as users
import functools


def authenticated(handler):
    @functools.wraps(handler)
    def middleware(update, context):
        chat_id = str(update.effective_chat.id)
        users_data = users.get()

        if users_data.get(chat_id) is None:
            text = "I'm sorry I do not know who you are. You need to log in."
            return context.bot.send_message(chat_id=chat_id, text=text)

        return handler(update, context)

    return middleware
