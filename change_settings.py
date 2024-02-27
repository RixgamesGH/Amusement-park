import PySimpleGUI as psg
from pathlib import Path
import json


class ChangeSettings:

    def __init__(self, main):

        self.settings = main.settings

        self.options = ["Password", "Park name", "Prices"]
        self.price_options = ["Babies", "Kids", "Adults", "Elderly", "Parking Ticket", "Groupsize discount", "Discount"]
        self.aborted = False

    def run(self):
        while True:

            event, values = self._select_option(self.options)
            if event == 'Ok':

                if not values[0]:
                    continue
                if values[0][0] == "Password":
                    self.settings.password = int(self._change_requested("Password"))

                if values[0][0] == "Park name":
                    text = psg.popup_get_text("Enter what to change the park name to", title="Change park name")
                    if text:
                        self.settings.park_name = text

                if values[0][0] == "Prices":
                    self._run_prices_options()

                if self.aborted:
                    self.aborted = False
                    continue

                ch = psg.popup_yes_no("Do you want to change anything else?")
                if ch == "Yes":
                    continue
                else:
                    self._save_changes()
                    psg.popup_auto_close("All changes were applied")
                    break
            else:
                self._save_changes()
                psg.popup_auto_close('User aborted, made changes were saved')
                break

    def _run_prices_options(self):
        while True:
            event, values = self._select_option(self.price_options)
            if event == 'Ok':

                if not values[0]:
                    continue
                if values[0][0] == "Babies":
                    self.settings.babies = self._change_requested("price Babies")

                if values[0][0] == "Kids":
                    self.settings.kids = self._change_requested("price Kids")

                if values[0][0] == "Adults":
                    self.settings.adults = self._change_requested("price Adults")

                if values[0][0] == "Elderly":
                    self.settings.elderly = self._change_requested("price Elderly")

                if values[0][0] == "Parking Ticket":
                    self.settings.parking_ticket = self._change_requested("price Parking Ticket")

                if values[0][0] == "Groupsize discount":
                    self.settings.minimum_groupsize_discount = int(self._change_requested("Groupsize Discount"))

                if values[0][0] == "Discount":
                    self.settings.discount = self._change_requested("Discount")

                break

            else:
                self.aborted = True
                break

    @staticmethod
    def _change_requested(request):
        while True:
            text = psg.popup_get_text(f"Enter the new {request}", title=f"Change {request}")
            if text:
                try:
                    return float(text)
                except ValueError:
                    psg.popup_auto_close("Input needs to be exclusively numbers")

    @staticmethod
    def _select_option(opts):
        event, values = psg.Window('Choose an option', [
            [psg.Text('Select one to change->'), psg.Listbox(opts, size=(25, len(opts)))],
            [psg.Button('Ok'), psg.Button('Cancel')]]).read(close=True)
        return event, values

    def _save_changes(self):

        data = [str(self.settings.password),
                str(self.settings.park_name),
                str(self.settings.babies),
                str(self.settings.kids),
                str(self.settings.adults),
                str(self.settings.elderly),
                str(self.settings.parking_ticket),
                str(self.settings.minimum_groupsize_discount),
                str(self.settings.discount)]

        path = Path('settings.json')
        txt = json.dumps(data)
        path.write_text(txt)
