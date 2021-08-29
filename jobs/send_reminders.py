from threads.reminder import Reminder
import utilities.users as users


def send_reminders(context):
    users_data = users.get()
    for data in users_data.values():
        reminder = Reminder(data)
        reminder.start()
