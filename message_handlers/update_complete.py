from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.api import send_update_mail, update_yeet_user, get_yeet_user
from utilities.error import send_error_response
import utilities.verify as verify
import utilities.users as users
import random
import string
import sys


def update_complete(update, context):
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    verify_data = verify.get()[chat_id]
    user_id = verify_data["id"]
    name = verify_data["name"]
    email = verify_data["email"]

    if message == "resend":
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        code = "".join(random.sample(string.digits, 6))
        try:
            response = send_update_mail(email, code)
            user = response.get("user")
            verify.set(
                chat_id,
                {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "code": code,
                },
            )
            text = "I just resent the email. Get the correct code and send it to me."
            return context.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            exception = sys.exc_info()
            return send_error_response(context, chat_id, exception)

    if message != verify_data["code"]:
        text = "{0} is not the correct code. I'll need you to retype it. Type resend if you want me to send the email again.".format(
            message
        )
        return context.bot.send_message(chat_id=chat_id, text=text)

    try:
        response = get_yeet_user(user_id)
        old_telegram_id = response.get("user").get("telegram_id")
        update_yeet_user(user_id, chat_id)
    except Exception:
        exception = sys.exc_info()
        return send_error_response(context, chat_id, exception)

    users_data = users.get()
    user_data = users_data.get(str(old_telegram_id))
    users.delete(str(old_telegram_id))
    users.set(chat_id, user_data)
    verify.delete(chat_id)

    text = "I have updated your Telegram details {0}. From now on, this is the Telegram account I am associating you with.".format(
        name.split(" ")[1]
    )
    record_action(chat_id, "update_complete")
    context.bot.send_message(chat_id=chat_id, text=text)
