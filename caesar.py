alfavit_EU = 'abcdefghijklmnopqrstuvwxyz'
alfavit_RU = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def caesar_cipher(text, shift):
    encrypted_text = ""
    shift = int(shift)
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я' or char == 'ё' or char == 'Ё':
                if char.islower():
                    encrypted_text += get_shifted_char_ceaser(char, shift, alfavit_RU)
                else:
                    encrypted_text += get_shifted_char_ceaser(char, shift, alfavit_RU.upper())
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                if char.islower():
                    encrypted_text += get_shifted_char_ceaser(char, shift, alfavit_EU)
                else:
                    encrypted_text += get_shifted_char_ceaser(char, shift, alfavit_EU.upper())
        else:
            encrypted_text += char
    return encrypted_text


def get_shifted_char_ceaser(char, shift, alphabet):
    alphabet_length = len(alphabet)
    index = alphabet.index(char)
    shifted_index = (index + shift) % alphabet_length
    return alphabet[shifted_index]


# Функция для дешифрования текста с использованием шифра Цезаря
def caesar_decipher(text, shift):
    decrypted_text = ""
    shift = int(shift)
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я' or char == 'ё' or char == 'Ё':
                if char.islower():
                    decrypted_text += get_deshifted_char(char, shift, alfavit_RU)
                else:
                    decrypted_text += get_deshifted_char(char, shift, alfavit_RU.upper())
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                if char.islower():
                    decrypted_text += get_deshifted_char(char, shift, alfavit_EU)
                else:
                    decrypted_text += get_deshifted_char(char, shift, alfavit_EU.upper())
        else:
            decrypted_text += char
    return decrypted_text


def get_deshifted_char(char, shift, alphabet):
    alphabet_length = len(alphabet)
    index = alphabet.index(char)
    shifted_index = (index - shift) % alphabet_length
    return alphabet[shifted_index]
