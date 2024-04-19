from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# Функция для шифрования текста
def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext


# Функция для дешифрования текста
def aes_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(ciphertext)
    unpadded_text = unpad(decrypted_text, AES.block_size)
    return unpadded_text.decode('utf-8')
