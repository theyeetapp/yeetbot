import config as configuration
import base64
import os.path as path
import requests

def verify(user, code):
    name = user[1].split(' ')[1]
    mail_template_path = path.join(configuration.root, 'templates', 'verify.txt')
    with open(mail_template_path, 'r') as reader:
        mail_string = reader.read().format(name, code)
    
    config = configuration.get()

    requests.post(config['mail_base_url'],
    files=[("inline", open(path.join(configuration.root, 'images', 'favicon.png'), 'rb'))],
    auth=('api', config['mail_api_key']),
    data={"from": "{0} {1}".format(config['mail_from'], config['mail_from_url']),
    "to": [user[2]],
    "subject": 'Verify your Telegram',
    "html": mail_string})
