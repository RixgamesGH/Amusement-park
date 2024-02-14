from print_doc import PrintDoc
from make_ticket import Ticket
from pathlib import Path
from make_receipt import Receipt
import json


class Generator:

    def __init__(self, main):
        self.settings = main.settings
        self.stats = main.stats
        self.doc = PrintDoc()
        self.receipt = Receipt(self.settings.park_name)
        self.items = {}

    def generate_tickets(self):
        """Making the tickets and printing them on a Word document"""
        for _ in range(self.stats.age1):
            Ticket("Age 0-3", self.settings.babies, self.stats.ticket_id, self.settings.park_name)
            self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
            self.stats.ticket_id += 1
        for _ in range(self.stats.age2):
            Ticket("Age 4-18", self.settings.kids, self.stats.ticket_id, self.settings.park_name)
            self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
            self.stats.ticket_id += 1
        for _ in range(self.stats.age3):
            Ticket("Age 19-64", self.settings.adults, self.stats.ticket_id, self.settings.park_name)
            self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
            self.stats.ticket_id += 1
        for _ in range(self.stats.age4):
            Ticket("Age 65+", self.settings.elderly, self.stats.ticket_id, self.settings.park_name)
            self.doc.add_ticket(f"ticket{self.stats.ticket_id}.png")
            self.stats.ticket_id += 1

        self.doc.print_doc(self.stats.ticket_id, "ticket")

        path = Path('id_tickets.json')
        txt = json.dumps(self.stats.ticket_id)
        path.write_text(txt)

    def generate_parking_tickets(self):
        """Making the parking tickets and printing them on a Word document"""
        for _ in range(self.stats.parking_tickets):
            Ticket("Parking ticket", self.settings.parking_ticket,
                   self.stats.parking_ticket_id, self.settings.park_name)
            self.doc.add_ticket(f"parking_ticket{self.stats.parking_ticket_id}.png")
            self.stats.parking_ticket_id += 1

        self.doc.print_doc(self.stats.parking_ticket_id, "parking_ticket")

        # Save the ticket ID so each guest gets unique ID's
        path = Path('id_parking_tickets.json')
        txt = json.dumps(self.stats.parking_ticket_id)
        path.write_text(txt)

    def generate_receipt(self):
        if self.stats.age1 != 0:
            self.items[f"{self.stats.age1}x Ticket Baby (age 0-3)"] = \
                float(f"{self.settings.babies * self.stats.age1}")
        if self.stats.age2 != 0:
            self.items[f"{self.stats.age2}x Ticket Kid (age 4-18)"] = \
                float(f"{self.settings.kids * self.stats.age2}")
        if self.stats.age3 != 0:
            self.items[f"{self.stats.age3}x Ticket Adult (age 19-64)"] = \
                float(f"{self.settings.adults * self.stats.age3}")
        if self.stats.age4 != 0:
            self.items[f"{self.stats.age4}x Ticket Elderly (age 65+)"] = \
                float(f"{self.settings.elderly * self.stats.age4}")
        if self.stats.parking_tickets != 0:
            self.items[f"{self.stats.parking_tickets}x Ticket Parking"] = \
                float(f"{self.settings.parking_ticket * self.stats.parking_tickets}")
        if self.stats.total_people >= 5:
            self.items["Group discount"] = float(f"{self.settings.discount * -1}")

        self.receipt.save_receipt_to_docx(self.stats.receipt_id, self.items)

        self.stats.receipt_id += 1
        path = Path('id_receipts.json')
        txt = json.dumps(self.stats.receipt_id)
        path.write_text(txt)
