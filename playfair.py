listEn = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
listRu = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
          'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ',
          'ы', 'ь', 'э', 'ю', 'я']


# Function to convert the string to lowercase
def toLowerCase(text):
    return text.lower()


# Function to remove all spaces in a string
def removeSpaces(text):
    newText = ""
    for i in text:
        if i == " ":
            continue
        else:
            newText = newText + i
    return newText


# Function to group 2 elements of a string as a list element
def Diagraph(text):
    Diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        Diagraph.append(text[group:i])

        group = i
    Diagraph.append(text[group:])
    return Diagraph


# Function to fill a letter in a string element If 2 letters in the same string matches
def FillerLetter(text, language='English'):
    k = len(text)
    new_word = "Error"
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i + 1]:
                if language == 'Russian':
                    new_word = text[0:i + 1] + str('ъ') + text[i + 1:]
                else:
                    new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    else:
        for i in range(0, k - 1, 2):
            if text[i] == text[i + 1]:
                if language == 'Russian':
                    new_word = text[0:i + 1] + str('ъ') + text[i + 1:]
                else:
                    new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    return new_word


# Function to generate the 5x5 key square matrix
def generateKeyTable(word, list1, language):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    compElements = []
    for i in key_letters:
        if i not in compElements:
            compElements.append(i)
    for i in list1:
        if i not in compElements:
            compElements.append(i)

    matrix = []
    if language == 'Russian':
        while compElements != []:
            matrix.append(compElements[:8])
            compElements = compElements[8:]
    else:
        while compElements != []:
            matrix.append(compElements[:5])
            compElements = compElements[5:]

    return matrix


def search(mat, element, language):
    if language == 'Russian':
        for i in range(4):
            for j in range(8):
                if (mat[i][j] == element):
                    return i, j
    else:
        for i in range(5):
            for j in range(5):
                if (mat[i][j] == element):
                    return i, j


def encrypt_RowRule(matr, e1r, e1c, e2r, e2c, language):
    char1 = ''
    if language == 'Russian':
        if e1c == 7:
            char1 = matr[e1r][0]
        else:
            char1 = matr[e1r][e1c + 1]
    else:
        if e1c == 4:
            char1 = matr[e1r][0]
        else:
            char1 = matr[e1r][e1c + 1]

    char2 = ''
    if language == 'Russian':
        if e2c == 7:
            char2 = matr[e2r][0]
        else:
            char2 = matr[e2r][e2c + 1]
    else:
        if e2c == 4:
            char2 = matr[e2r][0]
        else:
            char2 = matr[e2r][e2c + 1]

    return char1, char2


def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c, language):
    char1 = ''
    if language == 'Russian':
        if e1r == 3:
            char1 = matr[0][e1c]
        else:
            char1 = matr[e1r + 1][e1c]
    else:
        if e1r == 4:
            char1 = matr[0][e1c]
        else:
            char1 = matr[e1r + 1][e1c]

    char2 = ''
    if language == 'Russian':
        if e2r == 3:
            char2 = matr[0][e2c]
        else:
            char2 = matr[e2r + 1][e2c]
    else:
        if e2r == 4:
            char2 = matr[0][e2c]
        else:
            char2 = matr[e2r + 1][e2c]

    return char1, char2


def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    char1 = matr[e1r][e2c]

    char2 = ''
    char2 = matr[e2r][e1c]

    return char1, char2


def replace_j_on_i(text, language):
    if language == 'Russian':
        return text.replace('ё', 'е')
    else:
        return text.replace('j', 'i')


def encryptByPlayfairCipher(Matrix, plainList, language):
    CipherText = []
    for i in range(0, len(plainList)):
        c1 = 0
        c2 = 0
        ele1_x, ele1_y = search(Matrix, plainList[i][0], language)
        ele2_x, ele2_y = search(Matrix, plainList[i][1], language)

        if ele1_x == ele2_x:
            c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y, language)
            # Get 2 letter cipherText
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y, language)
        else:
            c1, c2 = encrypt_RectangleRule(
                Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        CipherText.append(cipher)
    return CipherText


def decryptByPlayfairCipher(Matrix, plainList, language):
    CipherText = []
    for i in range(0, len(plainList)):
        c1 = 0
        c2 = 0
        ele1_x, ele1_y = search(Matrix, plainList[i][0], language)
        ele2_x, ele2_y = search(Matrix, plainList[i][1], language)

        if ele1_x == ele2_x:
            c1, c2 = decrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y, language)
            # Get 2 letter cipherText
        elif ele1_y == ele2_y:
            c1, c2 = decrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y, language)
        else:
            c1, c2 = decrypt_RectangleRule(
                Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        cipher = c1 + c2
        CipherText.append(cipher)
    return CipherText


def decrypt_RowRule(matr, e1r, e1c, e2r, e2c, language):
    char1 = ''
    if language == 'Russian':
        if e1c == 0:
            char1 = matr[e1r][7]
        else:
            char1 = matr[e1r][e1c - 1]
    else:
        if e1c == 0:
            char1 = matr[e1r][4]
        else:
            char1 = matr[e1r][e1c - 1]

    char2 = ''
    if language == 'Russian':
        if e2c == 0:
            char2 = matr[e2r][7]
        else:
            char2 = matr[e2r][e2c - 1]
    else:
        if e2c == 0:
            char2 = matr[e2r][4]
        else:
            char2 = matr[e2r][e2c - 1]

    return char1, char2


def decrypt_ColumnRule(matr, e1r, e1c, e2r, e2c, language):
    char1 = ''
    if language == 'Russian':
        if e1r == 0:
            char1 = matr[3][e1c]
        else:
            char1 = matr[e1r - 1][e1c]
    else:
        if e1r == 0:
            char1 = matr[4][e1c]
        else:
            char1 = matr[e1r - 1][e1c]

    char2 = ''
    if language == 'Russian':
        if e2r == 0:
            char2 = matr[3][e2c]
        else:
            char2 = matr[e2r - 1][e2c]
    else:
        if e2r == 0:
            char2 = matr[4][e2c]
        else:
            char2 = matr[e2r - 1][e2c]

    return char1, char2


def decrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    char1 = matr[e1r][e2c]

    char2 = ''
    char2 = matr[e2r][e1c]

    return char1, char2
