from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.api import authenticate
from utilities.error import send_error_response
import utilities.verify as verify
import random
import string
import re
import sys

prefixes = ["Hmm,", "Sorry,", "I am sorry,", "I'm sorry,"]


def login_mail(update, context):
    chat_id = str(update.effective_chat.id)
    email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    email = update.message.text.lower()

    if re.match(email_regex, email) is None:
        return context.bot.send_message(
            chat_id=chat_id, text=email + " is not a valid email address"
        )

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    code = "".join(random.sample(string.digits, 6))

    try:
        response = authenticate(email, code)
    except Exception:
        exception = sys.exc_info()
        return send_error_response(context, chat_id, exception)

    if response.get("errorId"):
        prefix = prefixes[random.randint(0, len(prefixes) - 1)]
        text = prefix + " I cannot find any Yeet user with that email address"
        return context.bot.send_message(chat_id=chat_id, text=text)

    user = response.get("user")
    verify.set(
        chat_id,
        {"id": user["id"], "name": user["name"], "email": user["email"], "code": code},
    )
    text = "I just sent you an email with a verification code. Send me that code and I will log you in."
    record_action(chat_id, "login_email")
    return context.bot.send_message(chat_id=chat_id, text=text)
