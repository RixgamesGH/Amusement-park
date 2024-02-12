from pathlib import Path
import json


class Msg:

    def __init__(self, language):
        path = Path(f'{language}_texts.json')
        contents = path.read_text()
        file_texts = json.loads(contents)

        # General messages
        self.yes = file_texts["yes"]
        self.no = file_texts["no"]
        self.enter = file_texts["enter"]
        self.cancel = file_texts["cancel"]
        self.remove = file_texts["remove"]
        self.return_page = file_texts["return"]

        # Messages first screen
        self.one = file_texts["one"]
        self.two = file_texts["two"]
        self.three = file_texts["three"]
        self.four = file_texts["four"]
        self.five = file_texts["five"]
        self.string1 = file_texts["string1"]

        # Messages second screen
        self.age1 = file_texts["age1"]
        self.age2 = file_texts["age2"]
        self.age3 = file_texts["age3"]
        self.age4 = file_texts["age4"]
        self.multi = file_texts["multi"]
        self.string2 = file_texts["string2"]

        # Messages third screen
        self.total1 = file_texts["total1"]
        self.total2 = file_texts["total2"]
        self.total3 = file_texts["total3"]
        self.total4 = file_texts["total4"]
        self.discount = file_texts["discount"]
        self.string3 = file_texts["string3"]

        # Messages fourth screen
        self.multiple = file_texts["multiple"]
        self.string4 = file_texts["string4"]

        # Messages fifth screen
        self.pay = file_texts["pay"]
        self.string5 = file_texts["string5"]

        # Messages sixth screen
        self.string6 = file_texts["string6"]

        # Messages last screen
        self.string7 = file_texts["string7"]

        # Price total count
        self.price_count = file_texts["price_count"]


