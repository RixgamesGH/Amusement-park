from pathlib import Path
import PySimpleGUI as psg
import json


class Settings:

    def __init__(self):
        # Attributes to for screen scaling
        self.screen_width = 1920
        self.screen_height = 1080
        # Make ratio for width and height so all objects can be drawn on the screen, no matter the screensize
        self.r_width = self.screen_width / 1920
        self.r_height = self.screen_height / 1080

        self.bg_color = (3, 16, 45)
        self.button_color = (46, 169, 231)
        self.button_txt_color = (0, 0, 0)
        self.text_color = (19, 194, 148)
        self.N_width = 160
        self.N_height = 150

        # Extract data from json file
        try:
            path = Path('settings.json')
            contents = path.read_text()
            data = json.loads(contents)
        except FileNotFoundError:
            while True:
                data = self._initial_setup()
                if None not in data:
                    break
                else:
                    psg.popup_auto_close("Make sure to fill in all the fields.")
                    continue

        if None in data:
            psg.popup_auto_close("Some data is missing or corrupted, make sure to fill in every field.")
            data = self._initial_setup()

        while True:
            try:
                # Password to access settings
                self.password = int(data[0])

                # Park name
                self.park_name = data[1]

                # Pricing of tickets
                self.babies = float(data[2])
                self.kids = float(data[3])
                self.adults = float(data[4])
                self.elderly = float(data[5])
                self.parking_ticket = float(data[6])

                # Discount for larger groups
                self.minimum_groupsize_discount = int(data[7])
                self.discount = float(data[8])
                break
            except ValueError:
                psg.popup_auto_close("Make sure prices and password are exclusively numbers")
                data = self._initial_setup()
                continue

    @staticmethod
    def _initial_setup():
        title = "Initial setup"
        psg.popup_ok("Make sure all the answers will be exclusively numbers, except for the park name.\n"
                     "(numbers with decimals for pricing written like this: 10.00)", title=title+"Introduction")
        data = [psg.popup_get_text('Enter a password to access settings', title=title+"password"),
                psg.popup_get_text('What is the name of the park?', title=title+"name"),
                psg.popup_get_text('What will the price be for babies? (age 0-3)', title=title+"pricing"),
                psg.popup_get_text('What will the price be for kids? (age 4-18)', title=title+"pricing"),
                psg.popup_get_text('What will the price be for adults? (age 19-64)', title=title+"pricing"),
                psg.popup_get_text('What will the price be for elderly? (age 65+)', title=title+"pricing"),
                psg.popup_get_text('What will the price be for parking tickets?', title=title+"pricing"),
                psg.popup_get_text('What will the groupsize for a group discount be?', title=title+"pricing"),
                psg.popup_get_text('How much will a group discount be?', title=title+"pricing")]

        path = Path('settings.json')
        txt = json.dumps(data)
        path.write_text(txt)

        return data
