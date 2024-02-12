from translate import Translator
from pathlib import Path
import json


def _translate(string, language):
    translator = Translator(to_lang=language)
    translation = translator.translate(string)
    return translation


class Language:

    def __init__(self, *languages):
        # Make a template dictionary for all strings in english
        template = dict()
        
        # General messages
        template["yes"] = "Yes"
        template["no"] = "No"
        template["enter"] = "Enter"
        template["cancel"] = "Cancel"
        template["remove"] = "Remove"
        template["return"] = "Go back"

        # Messages first screen
        template["one"] = "One"
        template["two"] = "Two"
        template["three"] = "Three"
        template["four"] = "Four"
        template["five"] = "Five or more"
        template["string1"] = "With how many people do you want to enter the park?"

        # Messages second screen
        template["age1"] = "Age 0-3"
        template["age2"] = "Age 4-18"
        template["age3"] = "Age 19-64"
        template["age4"] = "Age 65+"
        template["multi"] = "Multiselect {x} x"
        template["string2"] = "Click multiselect to add more people to an age group at once ({x} left)"

        # Messages third screen
        template["total1"] = "Age 0-3: {x} in total"
        template["total2"] = "Age 4-18: {x} in total"
        template["total3"] = "Age 19-64: {x} in total"
        template["total4"] = "Age 65+: {x} in total"
        template["discount"] = "Group discount? {x}"
        template["string3"] = "Is this correct?"

        # Messages fourth screen
        template["multiple"] = "Yes, multiple"
        template["string4"] = "Would you like to buy a parking ticket as well for €{x:.2f}?"

        # Messages fifth screen
        template["pay"] = "Pay"
        template["string5"] = "Your total will come out to be €{x:.2f}"

        # Messages sixth screen
        template["string6"] = "Would you like to get the receipt?"

        # Messages last screen
        template["string7"] = "Thanks for your purchase, have fun!"

        # Price total count
        template["price_count"] = "Price total: €{x:.2f}"


        for lang in languages:
            path = Path(f'{lang}_texts.json')
            if lang != "en":
                dummy_dict = {}
                for variable, string in template.items():
                    translated_string = _translate(string, lang)
                    dummy_dict[variable] = translated_string
                txt = json.dumps(dummy_dict)
            else:
                txt = json.dumps(template)

            path.write_text(txt)


Language("nl", "en", "de", "fr")
