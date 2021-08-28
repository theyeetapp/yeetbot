from utilities.actions import record as record_action
import utilities.verify as verify


def login_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = "Alright!, send me your Yeet email so I can begin the process of logging you in."
    verify_data = verify.get()

    if verify_data.get(chat_id) is not None:
        text = "I sent you an email with instructions already."
    else:
        record_action(chat_id, "login")

    context.bot.send_message(chat_id=chat_id, text=text)
