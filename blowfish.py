from Crypto.Cipher import Blowfish
from Crypto import Random
import base64


def pad_message(message):
    # PKCS#5 padding
    pad_bytes = 8 - (len(message) % 8)
    return message + bytes([pad_bytes] * pad_bytes)


def unpad_message(padded_message):
    pad_bytes = padded_message[-1]
    return padded_message[:-pad_bytes]


def encrypt_message(message, key):
    iv = Random.new().read(Blowfish.block_size)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padded_message = pad_message(message.encode())
    return base64.b64encode(iv + cipher.encrypt(padded_message)).decode()


def decrypt_message(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:Blowfish.block_size]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(encrypted_message[Blowfish.block_size:])
    return unpad_message(decrypted_message).decode()
