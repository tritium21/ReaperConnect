import base64
import pathlib

import nacl.secret
import nacl.utils
import requests
import tomlkit
import yarl


IP_API_URL = "https://api.ipify.org?format=json"


def get_url():
    ip = requests.get(IP_API_URL).json()['ip']
    url = yarl.URL.build(
        scheme='http',
        host=ip,
        port=42069,
        path='/say'
    )
    return str(url)


def new_key():
    return base64.b64encode(
        nacl.utils.random(
            nacl.secret.SecretBox.KEY_SIZE,
        ),
    ).decode('ascii')


def generate(path):
    data = {
        'url': get_url(),
        'key': new_key(),
    }
    path = pathlib.Path(path).resolve()
    path.write_text(tomlkit.dumps(data), encoding='utf-8')
