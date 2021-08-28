from telegram import ChatAction
from utilities.mail import update as mail_update
from utilities.actions import record as record_action
import utilities.verify as verify
import utilities.users as users
import config


def update_complete(update, context):
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    verify_data = verify.get()[chat_id]
    user_id = verify_data["id"]
    name = verify_data["name"]
    email = verify_data["email"]

    if message == "resend":
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        mail_update(user_id, name, email, chat_id)
        text = "I just resent the email. Get the correct code and send it to me."
        return context.bot.send_message(chat_id=chat_id, text=text)

    if message != verify_data["code"]:
        text = "{0} is not the correct code. I'll need you to retype it. Type resend if you want me to send the email again.".format(
            message
        )
        return context.bot.send_message(chat_id=chat_id, text=text)

    db = config.get()["db"]
    cursor = db.cursor()
    query = 'SELECT * FROM users WHERE email="{0}"'.format(email)
    cursor.execute(query)
    user = cursor.fetchone()
    users_data = users.get()
    user_data = users_data.get(str(user[6]))
    users.delete(str(user[6]))
    users.set(chat_id, user_data)
    verify.delete(chat_id)

    update_user(chat_id, user_id)
    text = "I have updated your Telegram details {0}. From now on, this is the Telegram account I am associating you with.".format(
        name.split(" ")[1]
    )
    record_action(chat_id, "update_complete")
    context.bot.send_message(chat_id=chat_id, text=text)


def update_user(chat_id, user_id):
    db = config.get()["db"]
    cursor = db.cursor()
    query = 'UPDATE users SET telegram_id="{0}" WHERE id="{1}"'.format(chat_id, user_id)
    cursor.execute(query)
