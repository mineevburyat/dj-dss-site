def translite(strinput):
    if isinstance(strinput, (int, float, str)):
        strinput = str(strinput)
        trans_table = str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_-.: ",
            "abvgdeejzijklmnoprstufhc4ss_y_euaABVGDEEJZIJKLMNOPRSTUFHC4SS_Y_EUA_-___"
        )
        return strinput.translate(trans_table)
    raise ValueError

if __name__ == '__main__':
    print(translite('фрукт был цитрус но экземпляр'))