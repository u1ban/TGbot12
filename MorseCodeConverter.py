class CipherConverter:
    @staticmethod
    def text_to_morse(text):
        morse_code_dict = {'A': '.-', 'B': '-...',
                           'C': '-.-.', 'D': '-..', 'E': '.',
                           'F': '..-.', 'G': '--.', 'H': '....',
                           'I': '..', 'J': '.---', 'K': '-.-',
                           'L': '.-..', 'M': '--', 'N': '-.',
                           'O': '---', 'P': '.--.', 'Q': '--.-',
                           'R': '.-.', 'S': '...', 'T': '-',
                           'U': '..-', 'V': '...-', 'W': '.--',
                           'X': '-..-', 'Y': '-.--', 'Z': '--..',
                           '0': '-----', '1': '.----', '2': '..---',
                           '3': '...--', '4': '....-', '5': '.....',
                           '6': '-....', '7': '--...', '8': '---..',
                           '9': '----.', ' ': '/'}

        morse_code = ' '.join([morse_code_dict[char.upper()] for char in text])
        return morse_code

    @staticmethod
    def morse_to_text(morse_code):
        morse_code_dict = {'.-': 'A', '-...': 'B',
                           '-.-.': 'C', '-..': 'D', '.': 'E',
                           '..-.': 'F', '--.': 'G', '....': 'H',
                           '..': 'I', '.---': 'J', '-.-': 'K',
                           '.-..': 'L', '--': 'M', '-.': 'N',
                           '---': 'O', '.--.': 'P', '--.-': 'Q',
                           '.-.': 'R', '...': 'S', '-': 'T',
                           '..-': 'U', '...-': 'V', '.--': 'W',
                           '-..-': 'X', '-.--': 'Y', '--..': 'Z',
                           '-----': '0', '.----': '1', '..---': '2',
                           '...--': '3', '....-': '4', '.....': '5',
                           '-....': '6', '--...': '7', '---..': '8',
                           '----.': '9', '/': ' '}

        morse_code = morse_code.split(' ')
        text = ''.join([morse_code_dict[code] for code in morse_code])
        return text

    @staticmethod
    def atbash_cipher(text):
        atbash_dict = {chr(i): chr(219 - i) for i in range(97, 123)}
        atbash_dict.update({chr(i): chr(155 - i) for i in range(65, 91)})
        return ''.join([atbash_dict.get(char, char) for char in text])

    @staticmethod
    def a1z26_cipher(text):
        return ' '.join([str(ord(char) - ord('A') + 1) if char.isalpha() else char for char in text])

    @staticmethod
    def caesar_cipher(text, shift):
        result = ''
        for char in text:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - start + shift) % 26 + start)
            else:
                result += char
        return result
