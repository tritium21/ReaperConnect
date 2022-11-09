import base64
import dataclasses
import pathlib
import typing

import marshmallow_dataclass
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


@dataclasses.dataclass
class Streamer:
    host: str = '0.0.0.0'
    port: int = 42069


@dataclasses.dataclass
class Config:
    url: str
    key: typing.Optional[str]
    streamer: Streamer = dataclasses.field(default_factory=Streamer)

    @classmethod
    def new(cls):
        url = get_url()
        key = new_key()
        return cls(url=url, key=key)


config_schema = marshmallow_dataclass.class_schema(Config)()


def load(path):
    path = pathlib.Path(path)
    data = tomlkit.loads(path.read_text())
    return config_schema.load(data)


def save(config, path):
    path = pathlib.Path(path)
    data = tomlkit.dumps(config_schema.dump(config))
    path.write_text(data)
