import os
import subprocess
import sys
import printfactory
import PySimpleGUI as psg
from pathlib import Path


class Printer:

    def __init__(self):
        """Initialize printer assets"""

        # Determine which Adobe Reader is installed
        self.app_path = self._find_exe_file("Acrobat.exe", "AcroRd32.exe")

    def send_file_to_printer(self, file):
        """Sends a file to be added to the queue of the default printer"""
        printer = printfactory.Printer()
        print_tool = printfactory.AdobeAcrobat(printer, self.app_path, timeout=8)

        try:
            print_tool.print_file(file)
        except subprocess.TimeoutExpired:
            # To prevent the entire program to stop doing anything we pass over the error
            pass

    @staticmethod
    def _find_exe_file(*filenames):
        """
            Searching for the exe file of Adobe
            If the file is not found after having searched all files,
            communicate to the user to install a version of Adobe Reader/Acrobat
        """

        system_path = Path(r"C:\\")
        result = []
        # Walking top-down from the root
        for root, dr, files in os.walk(system_path):
            for filename in filenames:
                if filename in files:
                    result.append(os.path.join(root, filename))
                    break
            if result:
                path = Path(result[0])
                return path

        if not result:
            print("User does not have Adobe Reader/Acrobat installed.")
            psg.popup_auto_close("Make sure you have Adobe Reader/Acrobat installed on your device (on the C drive)",
                                 auto_close_duration=15)
            sys.exit()
