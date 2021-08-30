from threads.reminder import Reminder
import utilities.users as users


def send_reminders(context):
    users_data = users.get()
    for chat_id, data in users_data.items():
        name = "thread-{0}".format(chat_id)
        reminder = Reminder(name, data, context, chat_id)
        reminder.start()
