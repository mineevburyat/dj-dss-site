def translite(strinput):
    if isinstance(strinput, (int, float, str)):
        strinput = str(strinput)
        trans_table = str.maketrans(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_-.: ",
            "abvgdeejzijklmnoprstufhc4ss_y_euaABVGDEEJZIJKLMNOPRSTUFHC4SS_Y_EUA_-___"
        )
        return strinput.translate(trans_table)
    raise ValueError

class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class CategoryMixin:
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

if __name__ == '__main__':
    print(translite('фрукт был цитрус но экземпляр'))