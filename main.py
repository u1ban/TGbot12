import telebot
import cryptography
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from collections import OrderedDict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = '6801275453:AAEb2hE1Za_hs2LaWRyjA9pUCRn1YC5z3_k'
bot = telebot.TeleBot(TOKEN)

# Генерируем ключ для Fernet
fernet_key = Fernet.generate_key()
cipher_suite_fernet = Fernet(fernet_key)

# Генерируем ключ и IV для AES
aes_key = get_random_bytes(32)  # 256 бит
aes_iv = get_random_bytes(16)  # 128 бит
cipher_suite_aes = AES.new(aes_key, AES.MODE_CFB, iv=aes_iv)


# Функции для Шифра Цезаря
def encrypt_caesar(message, key):
    encrypted_message = ''
    for char in message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - ascii_offset + key) % 26 + ascii_offset)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message


def decrypt_caesar(encrypted_message, key):
    decrypted_message = ''
    for char in encrypted_message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - ascii_offset - key) % 26 + ascii_offset)
            decrypted_message += decrypted_char
        else:
            decrypted_message += char
    return decrypted_message


# Функции для AES
def encrypt_aes(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(message.encode()) + encryptor.finalize()
    return encrypted_data.hex()


def decrypt_aes(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(bytes.fromhex(encrypted_data)) + decryptor.finalize()
    return decrypted_data.decode()


# Функции для Base64
def encrypt_base64(message):
    encrypted_data = b64encode(message.encode()).decode()
    return encrypted_data


def decrypt_base64(encrypted_data):
    decrypted_data = b64decode(encrypted_data).decode()
    return decrypted_data


# Функции для Виженера
def encrypt_vigenere(message, key):
    encrypted_message = ''
    key = key.upper()
    for i, char in enumerate(message):
        if char.isalpha():
            key_char = key[i % len(key)]
            shift = ord(key_char) - ord('A')
            encrypted_char = chr((ord(char) + shift) % 26 + ord('A'))
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message


def decrypt_vigenere(encrypted_message, key):
    decrypted_message = ''
    key = key.upper()
    for i, char in enumerate(encrypted_message):
        if char.isalpha():
            key_char = key[i % len(key)]
            shift = ord(key_char) - ord('A')
            decrypted_char = chr((ord(char) - shift) % 26 + ord('A'))
            decrypted_message += decrypted_char
        else:
            decrypted_message += char
    return decrypted_message


# Функции для шифра Плейфера
def prepare_playfair_key(key):
    key = key.upper().replace('J', 'I')
    key_without_duplicates = "".join(OrderedDict.fromkeys(key))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in key_without_duplicates:
            key_without_duplicates += char
    return key_without_duplicates


def generate_playfair_table(key):
    key = prepare_playfair_key(key)
    table = [key[i:i + 5] for i in range(0, 25, 5)]
    return table


def find_playfair_coordinates(char, table):
    for i, row in enumerate(table):
        for j, col_char in enumerate(row):
            if char == col_char:
                return i, j
    raise ValueError(f"Symbol {char} not found in the Playfair table")


def encrypt_playfair(message, key):
    table = generate_playfair_table(key)
    encrypted_message = ''
    message_pairs = [message[i:i + 2].upper() for i in range(0, len(message), 2)]

    for pair in message_pairs:
        if len(pair) == 1:
            pair += 'X'
        elif pair[0] == pair[1]:
            pair = pair[0] + 'X'

        try:
            row1, col1 = find_playfair_coordinates(pair[0], table)
            row2, col2 = find_playfair_coordinates(pair[1], table)
        except ValueError as e:
            print(f"Error processing pair {pair}: {e}")
            continue

        if row1 == row2:
            encrypted_pair = table[row1][(col1 + 1) % 5] + table[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_pair = table[(row1 + 1) % 5][col1] + table[(row2 + 1) % 5][col2]
        else:
            encrypted_pair = table[row1][col2] + table[row2][col1]
        encrypted_message += encrypted_pair

    return encrypted_message


def decrypt_playfair(encrypted_message, key):
    table = generate_playfair_table(key)
    decrypted_message = ''
    message_pairs = [encrypted_message[i:i + 2].upper() for i in range(0, len(encrypted_message), 2)]
    for pair in message_pairs:
        row1, col1 = find_playfair_coordinates(pair[0], table)
        row2, col2 = find_playfair_coordinates(pair[1], table)
        if row1 == row2:
            decrypted_pair = table[row1][(col1 - 1) % 5] + table[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_pair = table[(row1 - 1) % 5][col1] + table[(row2 - 1) % 5][col2]
        else:
            decrypted_pair = table[row1][col2] + table[row2][col1]
        decrypted_message += decrypted_pair
    return decrypted_message


@bot.message_handler(commands=['encrypt_fernet'])
def encrypt_fernet_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    fernet_encrypted_text = cipher_suite_fernet.encrypt(text_to_encrypt.encode()).decode()
    bot.reply_to(message, f'Encrypted Fernet: {fernet_encrypted_text}')


@bot.message_handler(commands=['encrypt_aes'])
def encrypt_aes_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    aes_encrypted_text = encrypt_aes(text_to_encrypt, aes_key, aes_iv)
    bot.reply_to(message, f'Encrypted AES: {aes_encrypted_text}')


@bot.message_handler(commands=['encrypt_caesar'])
def encrypt_caesar_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    caesar_key = 3  # Замените на свой ключ Шифра Цезаря
    caesar_encrypted_text = encrypt_caesar(text_to_encrypt, caesar_key)
    bot.reply_to(message, f'Encrypted Caesar: {caesar_encrypted_text}')





@bot.message_handler(commands=['encrypt_base64'])
def encrypt_base64_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    base64_encrypted_text = encrypt_base64(text_to_encrypt)
    bot.reply_to(message, f'Encrypted Base64: {base64_encrypted_text}')


@bot.message_handler(commands=['encrypt_vigenere'])
def encrypt_vigenere_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    vigenere_key = 'KEY'  # Замените на свой ключ Виженера
    vigenere_encrypted_text = encrypt_vigenere(text_to_encrypt, vigenere_key)
    bot.reply_to(message, f'Encrypted Vigenere: {vigenere_encrypted_text}')


@bot.message_handler(commands=['encrypt_playfair'])
def encrypt_playfair_command(message):
    text_to_encrypt = message.text.split(maxsplit=1)[1]
    playfair_key = 'KEYWORD'  # Замените на свой ключ Плейфера
    playfair_encrypted_text = encrypt_playfair(text_to_encrypt, playfair_key)
    bot.reply_to(message, f'Encrypted Playfair: {playfair_encrypted_text}')


# Обработчик команды /decrypt
@bot.message_handler(commands=['decrypt'])
def decrypt_command(message):
    text_to_decrypt = message.text.split(maxsplit=1)[1]

    try:
        # Attempt to decrypt with Fernet
        fernet_decrypted_text = cipher_suite_fernet.decrypt(text_to_decrypt.encode()).decode()
    except cryptography.fernet.InvalidToken:
        fernet_decrypted_text = "Invalid Fernet token"

    # Дешифрование AES
    aes_decrypted_text = decrypt_aes(text_to_decrypt, aes_key, aes_iv)

    # Дешифрование Шифра Цезаря
    caesar_key = 3
    caesar_decrypted_text = decrypt_caesar(text_to_decrypt, caesar_key)

    # Дешифрование Base64
    base64_decrypted_text = decrypt_base64(text_to_decrypt)

    # Дешифрование Виженера
    vigenere_key = 'KEY'
    vigenere_decrypted_text = decrypt_vigenere(text_to_decrypt, vigenere_key)

    # Дешифрование Плейфера
    playfair_key = 'KEYWORD'
    playfair_decrypted_text = decrypt_playfair(text_to_decrypt, playfair_key)

    bot.reply_to(message, f'Decrypted Fernet: {fernet_decrypted_text}\n'
                          f'Decrypted AES: {aes_decrypted_text}\n'
                          f'Decrypted Caesar: {caesar_decrypted_text}\n'
                          f'Decrypted Base64: {base64_decrypted_text}\n'
                          f'Decrypted Vigenere: {vigenere_decrypted_text}\n'
                          f'Decrypted Playfair: {playfair_decrypted_text}')


# Обработчик неизвестной команды
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Неизвестная команда. Попробуйте /encrypt <текст> для шифрования.')


# Запускаем бота
bot.polling()
