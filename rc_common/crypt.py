import base64

import nacl.exceptions
import nacl.secret
import nacl.utils


class NoCrypt:
    def encrypt(self, message):
        return message

    decrypt = encrypt


class Crypt:
    def __init__(self, key):
        self.key = base64.b64decode(key)
        self.box = nacl.secret.SecretBox(self.key)

    @classmethod
    def new_key(cls):
        return base64.b64decode(
            nacl.utils.random(
                nacl.secret.SecretBox.KEY_SIZE,
            ),
        ).decode('ascii')

    def encrypt(self, message):
        message = message.encode('utf-8')
        cyphertext = self.box.encrypt(message)
        return base64.b64encode(cyphertext)

    def decrypt(self, message):
        message = base64.b64decode(message)
        try:
            return self.box.decrypt(message).decode('utf-8')
        except nacl.exceptions.CryptoError:
            return None


def from_key(key):
    if key is None:
        return NoCrypt()
    return Crypt(key)
