from telegram import ChatAction
from random import randint, sample
from requests.exceptions import HTTPError
from utilities.api import send_update_mail
from utilities.actions import record as record_action
from utilities.error import send_error_response
import utilities.verify as verify
import string
import re

prefixes = ["Hmm,", "Sorry,", "I am sorry,", "I'm sorry,"]


def update_mail(update, context):
    chat_id = str(update.effective_chat.id)
    email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    email = update.message.text

    if re.match(email_regex, email) is None:
        return context.bot.send_message(
            chat_id=chat_id, text=email + " is not a valid email address"
        )

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        code = "".join(sample(string.digits, 6))
        response = send_update_mail(email, code)
    except HTTPError as error:
        return send_error_response(context, chat_id, error)
    except Exception as error:
        return send_error_response(context, chat_id, error)

    if response.get("errorId") is not None:
        prefix = prefixes[randint(0, len(prefixes) - 1)]
        text = prefix + " I cannot find any Yeet user with that email address"
        return context.bot.send_message(chat_id=chat_id, text=text)

    user = response.get("user")
    verify.set(
        chat_id,
        {"id": user["id"], "name": user["name"], "email": user["email"], "code": code},
    )

    text = "I just sent you an email with an update code. Send me that code and I will update your Telegram details."
    record_action(chat_id, "update_email")
    context.bot.send_message(chat_id=chat_id, text=text)
