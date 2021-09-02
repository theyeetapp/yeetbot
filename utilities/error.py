from utilities.logs import record as record_exception
import traceback


def send_error_response(context, chat_id, exception):
    parsed_exception = {
        "message": str(exception[1]),
        "type": str(exception[0]),
        "stack_trace": " ".join(traceback.format_exception(*exception)),
    }
    record_exception(parsed_exception)
    text = "I am sorry. I ran into an error trying to perform that operation"
    return context.bot.send_message(chat_id=chat_id, text=text)
