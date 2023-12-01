import base64

from Cryptodome.Cipher import Blowfish
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad


def generate_key():
    return get_random_bytes(16)


def encrypt(plain_text, key):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    cipher_text = cipher.encrypt(pad(plain_text.encode('utf-8'), Blowfish.block_size))
    return base64.b64encode(cipher.iv + cipher_text)


def decrypt(cipher_text, key):
    cipher_text = base64.b64decode(cipher_text)
    iv = cipher_text[:Blowfish.block_size]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text[Blowfish.block_size:]), Blowfish.block_size)
    return plain_text.decode('utf-8')
