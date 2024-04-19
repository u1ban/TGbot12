import telebot
import unicodedata
import base64
import os
from dotenv import load_dotenv
from telebot import types
from Crypto.Cipher import Blowfish
from Crypto import Random
from caesar import caesar_cipher, caesar_decipher
from Crypto.Random import get_random_bytes
from vigenere import vigenere_cipher, vigenere_decipher
from playfair import removeSpaces, toLowerCase, Diagraph, FillerLetter, generateKeyTable, encryptByPlayfairCipher, \
    decryptByPlayfairCipher, listEn, replace_j_on_i, listRu
from aes import aes_encrypt, aes_decrypt
from morse import encrypt_morse, morse_code_ru, morse_code_en, decrypt_morse
from blowfish import decrypt_message, encrypt_message
from affine import decrypt, encrypt
from rsa import generate_key, encrypt_rsa, decrypt_rsa


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Цезарь', 'Виженер', 'Плейфер', 'AES', 'Морзе')
    bot.send_message(message.chat.id, "Привет! Выберите метод шифрования:", reply_markup=markup)


def detect_language(text):
    # Счетчики символов английского и русского алфавитов
    english_count = 0
    russian_count = 0

    for char in text:
        # Используем unicodedata.category, чтобы определить, является ли символ буквой
        if unicodedata.category(char).startswith('L'):
            # Проверяем, принадлежит ли символ английскому алфавиту
            if 'a' <= char.lower() <= 'z':
                english_count += 1
            # Проверяем, принадлежит ли символ русскому алфавиту
            elif 'а' <= char.lower() <= 'я':
                russian_count += 1

    # Сравниваем количество символов английского и русского алфавитов
    if russian_count > english_count:
        return 'Russian'
    elif english_count > russian_count:
        return 'English'
    else:
        return 'Unknown'


# Функция для проверки простоты числа
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text.lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    if user_input == 'цезарь':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_caesar_action)
    elif user_input == 'виженер':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_vigenere_action)
    elif user_input == 'плейфер':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_playfair_action)
    elif user_input == 'aes':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_aes_action)
    elif user_input == 'морзе':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_morse_action)
    elif user_input == 'blowfish':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_bf_action)
    elif user_input == 'affine':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_affine_action)
    elif user_input == 'rsa':
        markup.row('Шифровать', 'Дешифровать')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_rsa_action)
    else:
        markup.add('Цезарь', 'Виженер', 'Плейфер', 'AES', 'Морзе', 'BlowFish', 'Affine', 'RSA')
        bot.send_message(chat_id, "Пожалуйста, выберите метод шифрования из предложенных вариантов.",
                         reply_markup=markup)


# Обработчик выбора действия для шифра RSA
def process_rsa_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        public_key, private_key = generate_key()
        bot.send_message(message.chat.id, "Открытый ключ:\n" + public_key.decode())
        bot.send_message(message.chat.id, "Закрытый ключ:\n" + private_key.decode())
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_rsa_encryption)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите текст для дешифрования:")
        bot.register_next_step_handler(message, process_rsa_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_rsa_action)


# Обработчик шифрования текста шифром RSA
def process_rsa_encryption(message):
    chat_id = message.chat.id
    user_text = message.text

    bot.send_message(chat_id, "Введите открытый ключ для шифрования:")
    bot.register_next_step_handler(message, process_rsa_encryption_with_key, user_text)


def process_rsa_encryption_with_key(message, user_text):
    chat_id = message.chat.id
    public_key = message.text

    # Шифруем текст с использованием указанного ключа
    encrypted_message = encrypt_rsa(user_text, public_key)
    bot.send_message(chat_id, f"Зашифрованное сообщение: <b>{encrypted_message}</b>", parse_mode='HTML')
    handle_message(message)


# Обработчик дешифрования текста шифром RSA
def process_rsa_decryption(message):
    chat_id = message.chat.id
    user_text = message.text

    bot.send_message(chat_id, "Введите закрытый ключ для дешифрования:")
    bot.register_next_step_handler(message, process_rsa_decryption_with_key, user_text)


def process_rsa_decryption_with_key(message, user_text):
    chat_id = message.chat.id
    private_key = message.text

    # Шифруем текст с использованием указанного ключа
    decrypted_message = decrypt_rsa(eval(user_text), private_key)
    bot.send_message(message.chat.id, "Расшифрованное сообщение:\n" + decrypted_message)
    handle_message(message)


# Обработчик выбора действия для шифра Цезаря
def process_caesar_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_caesar_encryption)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите текст для дешифрования:")
        bot.register_next_step_handler(message, process_caesar_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_caesar_action)


# Обработчик шифрования текста шифром Цезаря
def process_caesar_encryption(message):
    chat_id = message.chat.id
    user_text = message.text

    bot.send_message(chat_id, "Введите ключ для шифрования:")
    bot.register_next_step_handler(message, process_ceaser_encryption_with_key, user_text)


def process_ceaser_encryption_with_key(message, user_text):
    chat_id = message.chat.id
    ceaser_key = message.text

    # Шифруем текст с использованием указанного ключа
    encrypted_text = caesar_cipher(user_text, ceaser_key)
    bot.send_message(chat_id, f"Зашифрованное сообщение: `{encrypted_text}`", parse_mode='MARKDOWN')
    handle_message(message)


# Обработчик дешифрования текста шифром Цезаря
def process_caesar_decryption(message):
    chat_id = message.chat.id
    user_text = message.text

    bot.send_message(chat_id, "Введите ключ для дешифрования:")
    bot.register_next_step_handler(message, process_ceaser_decryption_with_key, user_text)


def process_ceaser_decryption_with_key(message, user_text):
    chat_id = message.chat.id
    ceaser_key = message.text

    # Шифруем текст с использованием указанного ключа
    decrypted_text = caesar_decipher(user_text, ceaser_key)
    bot.send_message(chat_id, f"Зашифрованное сообщение: {decrypted_text}")
    handle_message(message)


# Обработчик выбора действия для шифра Виженера
def process_vigenere_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_vigenere_encryption)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите зашифрованное сообщение:")
        bot.register_next_step_handler(message, process_vigenere_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_vigenere_action)


# Обработчик шифрования текста шифром Виженера
def process_vigenere_encryption(message):
    chat_id = message.chat.id
    user_text = message.text

    bot.send_message(chat_id, "Введите ключ для шифрования:")
    bot.register_next_step_handler(message, lambda m: process_vigenere_encryption_with_key(m, user_text))


def process_vigenere_encryption_with_key(message, user_text):
    chat_id = message.chat.id
    vigenere_key = message.text

    # Шифруем текст с использованием указанного ключа
    encrypted_text = vigenere_cipher(user_text, vigenere_key)
    bot.send_message(chat_id, f"Зашифрованное сообщение: `{encrypted_text}`", parse_mode='MARKDOWN')
    handle_message(message)


# Обработчик дешифрования текста шифром Виженера
def process_vigenere_decryption(message):
    chat_id = message.chat.id
    encrypted_text = message.text

    bot.send_message(chat_id, "Введите ключ для дешифрования:")
    bot.register_next_step_handler(message, lambda m: process_vigenere_decryption_with_key(m, encrypted_text))


def process_vigenere_decryption_with_key(message, encrypted_text):
    chat_id = message.chat.id
    vigenere_key = message.text

    # Дешифруем текст с использованием указанного ключа
    decrypted_text = vigenere_decipher(encrypted_text, vigenere_key)
    bot.send_message(chat_id, f"Дешифрованное сообщение: {decrypted_text}")
    handle_message(message)


# Обработчик выбора действия для шифра Виженера
def process_playfair_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_playfair_encryption)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите зашифрованное сообщение:")
        bot.register_next_step_handler(message, process_playfair_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_playfair_action)


# Обработчик шифрования текста шифром Плейфер
def process_playfair_encryption(message):
    text_plain = message.text
    chat_id = message.chat.id
    language = detect_language(text_plain)
    text_plain = replace_j_on_i(text_plain, language)
    text_plain = removeSpaces(toLowerCase(text_plain))
    plain_text_list = Diagraph(FillerLetter(text_plain, language))
    if len(plain_text_list[-1]) != 2:
        if language == 'Russian':
            plain_text_list[-1] = plain_text_list[-1] + 'ъ'
        else:
            plain_text_list[-1] = plain_text_list[-1] + 'x'
    bot.send_message(chat_id, "Введите ключ для шифрования:")
    bot.register_next_step_handler(message,
                                   lambda m: process_playfair_encryption_with_key(m, plain_text_list, language))


def process_playfair_encryption_with_key(message, user_text, language):
    chat_id = message.chat.id
    key = message.text
    key = toLowerCase(key)

    if language == 'Russian':
        matrix = generateKeyTable(key, listRu, language)
    else:
        matrix = generateKeyTable(key, listEn, language)

    cipherlist = encryptByPlayfairCipher(matrix, user_text, language)
    ciphertext = ""
    for i in cipherlist:
        ciphertext += i

    # Шифруем текст с использованием указанного ключа
    bot.send_message(chat_id, f"Зашифрованное сообщение: `{ciphertext}`", parse_mode='MARKDOWN')
    handle_message(message)


# Обработчик шифрования текста шифром Плейфер
def process_playfair_decryption(message):
    text_plain = message.text
    language = detect_language(text_plain)
    text_plain = replace_j_on_i(text_plain, language)
    text_plain = removeSpaces(toLowerCase(text_plain))
    plain_text_list = Diagraph(FillerLetter(text_plain, language))
    if len(plain_text_list[-1]) != 2:
        plain_text_list[-1] = plain_text_list[-1] + 'x'
    chat_id = message.chat.id
    user_text = plain_text_list

    bot.send_message(chat_id, "Введите ключ для шифрования:")
    bot.register_next_step_handler(message, lambda m: process_playfair_decryption_with_key(m, user_text, language))


def process_playfair_decryption_with_key(message, user_text, language):
    chat_id = message.chat.id
    key = message.text
    key = toLowerCase(key)

    if language == 'Russian':
        matrix = generateKeyTable(key, listRu, language)
    else:
        matrix = generateKeyTable(key, listEn, language)

    cipherlist = decryptByPlayfairCipher(matrix, user_text, language)
    ciphertext = ""
    for i in cipherlist:
        ciphertext += i

    # Шифруем текст с использованием указанного ключа
    bot.send_message(chat_id, f"Зашифрованное сообщение: {ciphertext}")
    handle_message(message)


# Оброботчик выбора действии AES
def process_aes_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_aes_encryption)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите ключ и зашифрованное сообщение через пробел:")
        bot.register_next_step_handler(message, process_aes_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_aes_action)


def process_aes_encryption(message):
    key = get_random_bytes(16)  # Генерация случайного ключа длиной 16 байт
    plaintext = message.text
    ciphertext = aes_encrypt(key, plaintext)
    bot.send_message(message.chat.id,
                     f"Ключ: `{key.hex()}`\n"
                     f"Зашифрованный текст: `{ciphertext.hex()}`", parse_mode='MARKDOWN')
    handle_message(message)


def process_aes_decryption(message):
    text = message.text.split()
    if len(text) == 2 and len(text[0]) == 32 and len(text[1]) % 32 == 0:
        key = bytes.fromhex(text[0])
        ciphertext = bytes.fromhex(text[1])
        decrypted_text = aes_decrypt(key, ciphertext)
        bot.send_message(message.chat.id, f"Расшифрованный текст: {decrypted_text}")
    else:
        bot.send_message(message.chat.id, "Неправильный формат. Используйте: <ключ> <зашифрованный_текст>")
    handle_message(message)


# Обработчик выбора действия для шифра Морзе
def process_morse_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, process_morse_encryption_with_key)
    elif user_input == 'дешифровать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('english', 'russian')
        bot.send_message(chat_id, "Введите язык дешифрования:", reply_markup=markup)
        bot.register_next_step_handler(message, process_morse_decryption)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_morse_action)


def process_morse_encryption_with_key(message):
    chat_id = message.chat.id
    encrypted_text = ""

    # Шифруем текст с использованием указанного ключа
    language = detect_language(message.text)
    if language == "Russian":
        encrypted_text = encrypt_morse(message.text, morse_code_ru)
    elif language == "English":
        encrypted_text = encrypt_morse(message.text, morse_code_en)
    else:
        bot.send_message(chat_id, "Я не поддерживаю такой язык")
        bot.register_next_step_handler(message, process_morse_encryption_with_key)

    bot.send_message(chat_id, f"Зашифрованное сообщение: {encrypted_text}")
    handle_message(message)


# Обработчик дешифрования текста шифром Цезаря
def process_morse_decryption(message):
    chat_id = message.chat.id
    language = message.text

    if language.lower() in ['russian', 'русский']:
        bot.send_message(chat_id, "Введите текст для дешифрования:")
        bot.register_next_step_handler(message, process_morse_decryption_with_key, morse_code_ru)
    elif language.lower() in ['english', 'английский']:
        bot.send_message(chat_id, "Введите текст для дешифрования:")
        bot.register_next_step_handler(message, process_morse_decryption_with_key, morse_code_en)
    else:
        bot.send_message(chat_id, "Я не поддерживаю этот язык. Выберите другой.")
        bot.register_next_step_handler(message, process_morse_decryption)


def process_morse_decryption_with_key(message, user_text):
    chat_id = message.chat.id

    decrypted_text = decrypt_morse(message.text, user_text)

    bot.send_message(chat_id, f"Зашифрованное сообщение: {decrypted_text}")
    handle_message(message)


# Обработчик выбора действия для BlowFish
def process_bf_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите текст для шифрования:")
        bot.register_next_step_handler(message, echo_message)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите зашифрованное сообщение:")
        bot.register_next_step_handler(message, decrypt_message_handler)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_bf_action)


def echo_message(message):
    cid = message.chat.id
    try:
        key = Random.new().read(Blowfish.block_size)
        encrypted_message = encrypt_message(message.text, key)
        bot.send_message(cid, f"Зашифрованное сообщение: `{encrypted_message}` \n"
                              f"Ключ: `{base64.b64encode(key).decode()}`", parse_mode='MARKDOWN')
    except Exception as e:
        bot.send_message(cid, "Ошибка при шифровании. Попробуйте снова.")
    handle_message(message)


def decrypt_message_handler(message):
    cid = message.chat.id
    encrypted_message = message.text
    bot.send_message(cid, "Пожалуйста, введите ключ для дешифровки:")
    bot.register_next_step_handler(message, lambda msg: finish_decryption(msg, encrypted_message))


def finish_decryption(message, encrypted_message):
    cid = message.chat.id
    key = base64.b64decode(message.text)
    try:
        decrypted_message = decrypt_message(encrypted_message, key)
        bot.send_message(cid, f"Расшифрованное сообщение: {decrypted_message}")
    except Exception as e:
        bot.send_message(cid, "Ошибка при дешифровании. Проверьте правильность ключа.")
    handle_message(message)


# Обработчик выбора действия для Affine
def process_affine_action(message):
    chat_id = message.chat.id
    user_input = message.text.lower()

    if user_input == 'шифровать':
        bot.send_message(chat_id, "Введите ключ шифрования в формате <a b>, где 'a' - простое число.")
        bot.register_next_step_handler(message, process_encryption_key)
    elif user_input == 'дешифровать':
        bot.send_message(chat_id, "Введите ключ шифрования в формате <a, b>, где 'a' - простое число.")
        bot.register_next_step_handler(message, process_decryption_key)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, process_affine_action)


def process_encryption_key(message):
    chat_id = message.chat.id
    key_input = message.text
    try:
        # Проверяем, что введенный ключ имеет правильный формат
        key = tuple(map(int, key_input.split()))  # Преобразуем строку в кортеж чисел
        if len(key) != 2:
            raise ValueError
        a, b = key
        # Проверяем, что 'a' - простое число
        if not is_prime(a):
            bot.send_message(chat_id, "'a' должно быть простым числом.")
            return
        bot.send_message(chat_id, "Теперь введите сообщение для шифрования.")
        bot.register_next_step_handler(message, process_encryption_message, key)
    except:
        bot.send_message(chat_id, "Неверный формат ключа. Пожалуйста, введите ключ в формате a b.")


def process_encryption_message(message, key):
    chat_id = message.chat.id
    original_message = message.text
    encrypted_message, _ = encrypt(original_message, key)
    bot.send_message(chat_id, f"Зашифрованное сообщение: `{encrypted_message}`", parse_mode='MARKDOWN')
    handle_message(message)


def process_decryption_key(message):
    chat_id = message.chat.id
    key_input = message.text
    try:
        # Проверяем, что введенный ключ имеет правильный формат
        key = tuple(map(int, key_input.split()))  # Преобразуем строку в кортеж чисел
        if len(key) != 2:
            raise ValueError
        a, b = key
        # Проверяем, что 'a' - простое число
        if not is_prime(a):
            bot.send_message(chat_id, "'a' должно быть простым числом.")
            return
        bot.send_message(chat_id, "Теперь введите зашифрованное сообщение.")
        bot.register_next_step_handler(message, process_decryption_message, key)
    except:
        bot.send_message(chat_id, "Неверный формат ключа. Пожалуйста, введите ключ в формате a b.")


def process_decryption_message(message, key):
    chat_id = message.chat.id
    encrypted_message = message.text
    decrypted_message = decrypt(encrypted_message, key)
    bot.send_message(chat_id, f"Дешифрованное сообщение: {decrypted_message}")
    handle_message(message)


bot.polling()
