import requests
from tgbot_client.config import Config as BaseConfig

baseconfig = BaseConfig()
def send_text(message,wxid):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'function': 'send_text',
        'message': message,
        'wxid': int(wxid),
    }
    response = requests.post(f'http://{baseconfig.host}:{baseconfig.port}/tguser/send_text', headers=headers, json=json_data)