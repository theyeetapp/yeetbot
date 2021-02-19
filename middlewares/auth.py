import utilities.users as users
import functools

def authenticated(handler):
    @functools.wraps(handler)
    def middleware(update, context):
        chat_id = str(update.effective_chat.id)
        users_data = users.get()

        if users_data[chat_id] is None:
            text = 'I\'m sorry I cannot grant you access. You are not logged in.'
            return context.bot.send_message(chat_id=chat_id, text=text)
        
        return handler(update, context)
    
    return middleware

