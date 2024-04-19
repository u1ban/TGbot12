alfavit_EU = 'abcdefghijklmnopqrstuvwxyz'
alfavit_RU = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# Функция для шифрования текста с использованием шифра Виженера
def vigenere_cipher(text, key):
    encrypted_text = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я' or char == 'ё' or char == 'Ё':
                shift = alfavit_RU.index(key[key_index % len(key)].lower()) - alfavit_RU.index('а')
                encrypted_char = get_shifted_char_vigenere(char, shift, alfavit_RU)
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                shift = alfavit_EU.index(key[key_index % len(key)].lower()) - alfavit_EU.index('a')
                encrypted_char = get_shifted_char_vigenere(char, shift, alfavit_EU)
            else:
                encrypted_char = char
            encrypted_text += encrypted_char
            key_index += 1
        else:
            encrypted_text += " "
    return encrypted_text


def get_shifted_char_vigenere(char, shift, alphabet):
    if char.isalpha():
        is_lower = char.islower()
        char_index = alphabet.find(char.lower())
        if char_index != -1:
            shifted_index = (char_index + shift) % len(alphabet)
            shifted_char = alphabet[shifted_index]
            return shifted_char if is_lower else shifted_char.upper()
    return char


# Функция для дешифрования текста с использованием шифра Виженера
def vigenere_decipher(text, key):
    encrypted_text = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я' or char == 'ё' or char == 'Ё':
                shift = alfavit_RU.index(key[key_index % len(key)].lower()) - alfavit_RU.index('а')
                encrypted_char = get_deshifted_char_vigenere(char, shift, alfavit_RU)
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                shift = alfavit_EU.index(key[key_index % len(key)].lower()) - alfavit_EU.index('a')
                encrypted_char = get_deshifted_char_vigenere(char, shift, alfavit_EU)
            else:
                encrypted_char = char
                encrypted_text += encrypted_char
                key_index += 1
        else:
            encrypted_text += " "
    return encrypted_text


def get_deshifted_char_vigenere(char, shift, alphabet):
    if char.isalpha():
        is_lower = char.islower()
        char_index = alphabet.find(char.lower())
        if char_index != -1:
            shifted_index = (char_index - shift) % len(alphabet)
            shifted_char = alphabet[shifted_index]
            return shifted_char if is_lower else shifted_char.upper()
    return char
