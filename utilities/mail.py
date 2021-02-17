import utilities.verify as verify
import config as configuration
import random
import os.path as path
import requests
import string

def login(id, name, email, chat_id):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.sample(characters, 10))
    mail_template_path = path.join(configuration.root, 'templates', 'verify.txt')
    with open(mail_template_path, 'r') as reader:
        mail_string = reader.read().format(code)
    
    config = configuration.get()

    requests.post(config['mail_base_url'],
    files=[("inline", open(path.join(configuration.root, 'images', 'favicon.png'), 'rb'))],
    auth=('api', config['mail_api_key']),
    data={"from": "{0} {1}".format(config['mail_from'], config['mail_from_url']),
    "to": [email],
    "subject": 'Verify your Telegram',
    "html": mail_string})

    verify.set(chat_id, {"id":id, "name":name, "email":email, "code":code})
    
