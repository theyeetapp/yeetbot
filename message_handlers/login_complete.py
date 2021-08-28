from telegram import ChatAction
from utilities.actions import record as record_action
from utilities.api import authenticate, count_subscriptions, update_yeet_user
from utilities.error import send_error_response
import utilities.verify as verify
import utilities.users as users
from requests.exceptions import HTTPError
import config
import random
import string
import os.path as path

def login_complete(update, context):
    chat_id = str(update.effective_chat.id)
    message = update.message.text

    verify_data = verify.get()[chat_id]
    user_id = verify_data["id"]
    name = verify_data["name"]
    email = verify_data["email"]

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    if message == "resend":
        code = "".join(random.sample(string.digits, 6))
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        try:
            response = authenticate(email, code)
        except HTTPError as error:
            return send_error_response(context, chat_id, error)
        except Exception as error:
            return send_error_response(context, chat_id, error)

        user = response.get("user")
        verify.set(chat_id, {"id": user['id'], "name": user['name'], "email": user['email'], "code": code})
        text = "I just resent the email. Get the correct code and send it to me."
        return context.bot.send_message(chat_id=chat_id, text=text)

    if verify_data["code"] != message:
        text = "{0} is not the correct code. I'll need you to retype it. Type resend if you want me to send the email again.".format(
            message
        )
        return context.bot.send_message(chat_id=chat_id, text=text)

    del verify_data["code"]
    users.set(chat_id, verify_data)
    verify.delete(chat_id)

    message_path = path.join(config.root, "messages", "verified.txt")
    with open(message_path, "r") as reader:
        text = reader.read().format(name.split(" ")[1])

    try:
        update_yeet_user(user_id, chat_id)
    except HTTPError as error:
        return send_error_response(context, chat_id, error)
    except Exception as error:
        return send_error_response(context, chat_id, error)
    
    record_action(chat_id, "login_complete")
    return context.bot.send_message(chat_id=chat_id, text=text)

