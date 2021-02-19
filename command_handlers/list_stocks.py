from command_handlers.list_type import list_type

def list_stocks_handler(update, context):
    list_type(update, context, 'stock')