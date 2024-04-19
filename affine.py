# Функция для шифрования сообщения методом аффинного преобразования
def encrypt(message, key):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                encrypted_message += chr(((ord(char) - 65) * key[0] + key[1]) % 26 + 65)
            else:
                encrypted_message += chr(((ord(char) - 97) * key[0] + key[1]) % 26 + 97)
        else:
            encrypted_message += char
    return encrypted_message, key

# Функция для дешифрования сообщения методом аффинного преобразования
def decrypt(message, key):
    decrypted_message = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                decrypted_message += chr(((ord(char) - 65 - key[1]) * mod_inverse(key[0], 26)) % 26 + 65)
            else:
                decrypted_message += chr(((ord(char) - 97 - key[1]) * mod_inverse(key[0], 26)) % 26 + 97)
        else:
            decrypted_message += char
    return decrypted_message


# Функция для нахождения обратного элемента в кольце вычетов
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None